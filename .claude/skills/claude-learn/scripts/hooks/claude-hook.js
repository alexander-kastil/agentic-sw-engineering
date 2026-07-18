const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { appendJsonl, buildDecisionRecord, ensureDir, repoRoot, readStdinJson } = require('./hook-utils');

const hookName = process.argv[2] || 'unknown';
const payload = readStdinJson();

const conversationRoot = path.join(repoRoot, '.conversations-claude');
const stateDir = path.join(conversationRoot, 'state');
const statePath = path.join(stateDir, 'current-session.json');
const rawDir = path.join(conversationRoot, 'raw');
const analysisDir = path.join(conversationRoot, 'analysis');

ensureDir(stateDir);
ensureDir(rawDir);
ensureDir(analysisDir);

function toIso(value) {
  if (typeof value === 'number' && Number.isFinite(value)) return new Date(value).toISOString();
  if (typeof value === 'string' && value) {
    const n = Number(value);
    if (Number.isFinite(n) && value.trim() !== '') return new Date(n).toISOString();
    const p = Date.parse(value);
    if (!Number.isNaN(p)) return new Date(p).toISOString();
  }
  return new Date().toISOString();
}

function readJson(filePath, fallback) {
  if (!fs.existsSync(filePath)) return fallback;
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch { return fallback; }
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function resolveSessionId(currentHook, currentPayload, iso) {
  const explicit = currentPayload.sessionId || currentPayload.session_id || currentPayload.session?.id || null;
  if (explicit) {
    writeJson(statePath, { sessionId: explicit, startedAt: iso, cwd: currentPayload.cwd || null });
    return explicit;
  }
  const current = readJson(statePath, null);
  if (currentHook === 'sessionStart') {
    if (currentPayload.source === 'resume' && current?.sessionId) return current.sessionId;
    const sessionId = crypto.randomUUID();
    writeJson(statePath, { sessionId, startedAt: iso, cwd: currentPayload.cwd || null });
    return sessionId;
  }
  if (current?.sessionId) return current.sessionId;
  const orphan = crypto.randomUUID();
  writeJson(statePath, { sessionId: orphan, startedAt: iso, cwd: currentPayload.cwd || null });
  return orphan;
}

function resolveToolName(p) {
  return p.toolName || p.tool_name || p.tool?.name || p.tool?.toolName || p.tool?.tool_name || 'unknown';
}

function resolveToolArgs(p) {
  const raw = p.toolArgs || p.tool_args || p.toolInput || p.tool_input || p.tool?.input || p.tool?.toolInput || null;
  if (!raw) return {};
  if (typeof raw === 'object') return raw;
  try { return JSON.parse(raw); } catch { return {}; }
}

function resolveToolResult(p) {
  const r = p.toolResult || p.tool_result || p.toolResponse || p.tool_response || null;
  if (!r) return { resultType: 'success' };
  if (typeof r === 'string') return { resultType: 'success' };
  return {
    resultType: r.resultType || r.result_type || r.status || 'success',
    textResultForLlm: r.textResultForLlm || r.text_result_for_llm || r.text || r.output || null,
  };
}

function appendRaw(dateStamp, event) {
  appendJsonl(path.join(rawDir, `${dateStamp}.jsonl`), event);
}

function isSkillInvocation(toolName, toolArgs) {
  const lower = String(toolName || '').toLowerCase();
  return lower === 'skill' || lower.includes('skill') || Boolean(toolArgs.skill || toolArgs.skillName);
}

function normalizeFilePath(toolName, toolArgs) {
  return toolArgs.file_path || toolArgs.filePath || toolArgs.path || toolArgs.target_file || null;
}

function maybeCaptureDecision(sessionId, iso, dateStamp, toolName, toolArgs) {
  if (!isSkillInvocation(toolName, toolArgs)) return;
  const decision = buildDecisionRecord({
    agent_name: payload.agentName || payload.agent_name || toolArgs.agentName || toolArgs.subagent_type || 'unknown',
    tool_input: { ...toolArgs, skill: toolArgs.skill || toolArgs.skillName || toolArgs.name, name: toolArgs.name || toolArgs.skill },
  });
  decision.ts = iso;
  decision.session = sessionId;
  appendJsonl(path.join(analysisDir, 'decisions.jsonl'), decision);
  appendRaw(dateStamp, { ts: iso, session: sessionId, tool: 'Skill', skill: decision.skill, agent: decision.agent, category: decision.category, reason: decision.reason });
}

function handlePreToolUse(sessionId, iso, dateStamp) {
  const toolName = resolveToolName(payload);
  const toolArgs = resolveToolArgs(payload);
  maybeCaptureDecision(sessionId, iso, dateStamp, toolName, toolArgs);
}

function handlePostToolUse(sessionId, iso, dateStamp) {
  const toolName = resolveToolName(payload);
  const lower = String(toolName).toLowerCase();
  const toolArgs = resolveToolArgs(payload);
  const toolResult = resolveToolResult(payload);

  if (lower === 'edit' || lower === 'write' || lower === 'apply_patch' || lower === 'create_file' || lower === 'edit_notebook_file') {
    appendRaw(dateStamp, {
      ts: iso, session: sessionId,
      tool: lower === 'edit' || lower === 'apply_patch' || lower === 'edit_notebook_file' ? 'Edit' : 'Write',
      file: normalizeFilePath(toolName, toolArgs), sourceTool: toolName,
    });
    return;
  }

  if (lower === 'bash' || lower === 'run_in_terminal' || lower === 'terminal') {
    appendRaw(dateStamp, {
      ts: iso, session: sessionId, tool: 'Bash',
      cmd: String(toolArgs.command || toolArgs.cmd || '').slice(0, 200),
      exit_code: toolResult.resultType === 'success' ? 0 : toolResult.resultType === 'failure' ? 1 : null,
      success: toolResult.resultType === 'success',
    });
    return;
  }

  if (lower === 'agent' || lower === 'runsubagent') {
    appendRaw(dateStamp, { ts: iso, session: sessionId, tool: 'Agent', type: toolArgs.agentName || toolArgs.agent || toolArgs.name || 'unknown', desc: toolArgs.description || toolArgs.prompt || null });
  }
}

function runAnalyzer(dateStamp, sessionId) {
  const result = spawnSync(process.execPath, [path.join(__dirname, 'analyze-session.js'), '--date', dateStamp, '--session', sessionId], { cwd: repoRoot, encoding: 'utf8' });
  if (result.status !== 0) {
    appendJsonl(path.join(analysisDir, 'analyzer-errors.jsonl'), { ts: new Date().toISOString(), session: sessionId, stderr: (result.stderr || '').trim() || null });
  }
}

function handleSessionEnd(sessionId, iso, dateStamp) {
  appendRaw(dateStamp, { ts: iso, session: sessionId, event: 'stop' });
  runAnalyzer(dateStamp, sessionId);
  const current = readJson(statePath, null);
  if (current?.sessionId === sessionId) fs.rmSync(statePath, { force: true });
}

function main() {
  const iso = toIso(payload.timestamp);
  const dateStamp = iso.slice(0, 10);
  const sessionId = resolveSessionId(hookName, payload, iso);

  if (hookName === 'preToolUse') { handlePreToolUse(sessionId, iso, dateStamp); return; }
  if (hookName === 'postToolUse') { handlePostToolUse(sessionId, iso, dateStamp); return; }
  if (hookName === 'sessionEnd') { handleSessionEnd(sessionId, iso, dateStamp); }
}

main();
