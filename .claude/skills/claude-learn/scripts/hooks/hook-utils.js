const fs = require('node:fs');
const path = require('node:path');

const repoRoot = path.resolve(__dirname, '..', '..');

function readStdinJson() {
  const input = fs.readFileSync(0, 'utf8').trim();
  if (!input) return {};
  try { return JSON.parse(input); } catch { return {}; }
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function appendJsonl(filePath, value) {
  fs.appendFileSync(filePath, `${JSON.stringify(value)}\n`, 'utf8');
}

function nowIso() {
  return new Date().toISOString();
}

function inferCategory(skill = '', text = '') {
  const h = `${skill} ${text}`.toLowerCase();
  if (h.includes('seo')) return 'seo';
  if (/(image|banner|design|color|layout)/.test(h)) return 'design';
  if (/(deploy|workflow|oidc|swa)/.test(h)) return 'deployment';
  if (/(config|feature-flag|bicep|infra)/.test(h)) return 'configuration';
  if (/(doc|readme|markdown)/.test(h)) return 'documentation';
  if (/(debug|verify|audit|test)/.test(h)) return 'debugging';
  if (/(plan|planner|spec)/.test(h)) return 'planning';
  if (/(create|build|page|content|template)/.test(h)) return 'implementation';
  return 'general';
}

function inferReason(text = '') {
  const stop = new Set(['the','and','with','for','from','into','this','that','your','our','their','page','file','task','use','using','update','create','fix','new','area']);
  return text.toLowerCase().replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/)
    .filter(t => t.length >= 3 && !stop.has(t)).slice(0, 4).join('-') || 'general';
}

function buildDecisionRecord(payload) {
  const i = payload.tool_input || {};
  const skill = i.skill || i.name || 'unknown';
  const summary = i.description || i.prompt || '';
  return {
    ts: nowIso(),
    agent: payload.agent_name || i.agent || i.invoking_agent || i.subagent_type || 'unknown',
    skill,
    category: i.category || i.task_category || inferCategory(skill, summary),
    reason: i.reason || i.reasoning_keyword || i.short_reason || inferReason(summary),
    summary: summary || null,
  };
}

module.exports = { appendJsonl, buildDecisionRecord, ensureDir, nowIso, readStdinJson, repoRoot };
