const fs = require('node:fs');
const path = require('node:path');

function parseArgs(argv) {
  const args = { date: new Date().toISOString().slice(0, 10), session: '' };
  for (let i = 2; i < argv.length; i += 1) {
    if (argv[i] === '--date' && argv[i + 1]) { args.date = argv[i + 1]; i += 1; }
    else if (argv[i] === '--session' && argv[i + 1]) { args.session = argv[i + 1]; i += 1; }
  }
  return args;
}

function ensureDir(d) { fs.mkdirSync(d, { recursive: true }); }

function readJson(filePath, fallback) {
  if (!fs.existsSync(filePath)) return fallback;
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch { return fallback; }
}

function parseJsonl(filePath) {
  if (!fs.existsSync(filePath)) return [];
  return fs.readFileSync(filePath, 'utf8').split(/\r?\n/).map(l => l.trim()).filter(Boolean)
    .flatMap(l => { try { return [JSON.parse(l)]; } catch { return []; } });
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function toMs(ts) { const v = Date.parse(ts || ''); return Number.isNaN(v) ? 0 : v; }
function sortByTs(items) { return [...items].sort((a, b) => toMs(a.ts) - toMs(b.ts)); }
function unique(values) { return [...new Set(values.filter(Boolean))]; }

function skillFamily(s = '') {
  const l = s.toLowerCase();
  if (l.includes('seo')) return 'seo';
  if (l.includes('design') || l.includes('image') || l.includes('banner')) return 'design';
  if (l.includes('deploy')) return 'deployment';
  if (l.includes('config')) return 'configuration';
  if (l.includes('doc')) return 'documentation';
  if (l.includes('debug') || l.includes('reflect') || l.includes('verify')) return 'debugging';
  if (l.includes('plan')) return 'planning';
  if (l.includes('create') || l.includes('attach') || l.includes('add')) return 'implementation';
  return 'general';
}

function categoryFamily(c = '') {
  const l = c.toLowerCase();
  if (l.includes('seo')) return 'seo';
  if (l.includes('design') || l.includes('image') || l.includes('banner') || l.includes('layout')) return 'design';
  if (l.includes('deploy') || l.includes('workflow') || l.includes('oidc')) return 'deployment';
  if (l.includes('config') || l.includes('infra') || l.includes('feature-flag')) return 'configuration';
  if (l.includes('doc') || l.includes('markdown') || l.includes('readme')) return 'documentation';
  if (l.includes('debug') || l.includes('verify') || l.includes('test') || l.includes('audit')) return 'debugging';
  if (l.includes('plan') || l.includes('spec')) return 'planning';
  if (l.includes('create') || l.includes('build') || l.includes('page') || l.includes('template') || l.includes('content')) return 'implementation';
  return 'general';
}

function mergePattern(patterns, occ, date) {
  const cur = patterns[occ.type] || { count: 0, first_seen: date, last_seen: date, affected_skills: [], agents: [], examples: [], recommendation: occ.recommendation };
  cur.count += 1;
  cur.first_seen = cur.first_seen < date ? cur.first_seen : date;
  cur.last_seen = cur.last_seen > date ? cur.last_seen : date;
  cur.affected_skills = unique([...cur.affected_skills, occ.skill]);
  cur.agents = unique([...cur.agents, occ.agent]);
  cur.examples = [...cur.examples, occ.example].slice(-10);
  cur.recommendation = cur.recommendation || occ.recommendation;
  patterns[occ.type] = cur;
}

function detectOccurrences(decisions, rawEvents, date) {
  const occs = [];
  const skillEvents = sortByTs(decisions);
  const stopEvents = sortByTs(rawEvents.filter(e => e.event === 'stop'));

  for (let i = 0; i < skillEvents.length; i += 1) {
    const dec = skillEvents[i];
    const startMs = toMs(dec.ts);
    const nextSkillMs = i + 1 < skillEvents.length ? toMs(skillEvents[i + 1].ts) : Infinity;
    const nextStop = stopEvents.find(e => toMs(e.ts) > startMs);
    const windowEnd = Math.min(startMs + 10 * 60 * 1000, nextSkillMs, nextStop ? toMs(nextStop.ts) : Infinity);

    const nearby = rawEvents.filter(e => { const v = toMs(e.ts); return v > startMs && v <= windowEnd; });
    const edits = nearby.filter(e => e.tool === 'Write' || e.tool === 'Edit');
    const failures = nearby.filter(e => e.tool === 'Bash' && (e.exit_code !== 0 || e.success === false));

    if (edits.length > 0) occs.push({
      type: 'incomplete-skill-output', skill: dec.skill, agent: dec.agent,
      recommendation: `Update ${dec.skill} to finish the follow-up file changes it currently leaves behind.`,
      example: { session: date, skill: dec.skill, issue: `Manual edits followed ${dec.skill} before the next skill call.`, files: unique(edits.map(e => e.file)).slice(0, 5) },
    });

    if (failures.length > 0) occs.push({
      type: 'command-failure-after-skill', skill: dec.skill, agent: dec.agent,
      recommendation: `Harden ${dec.skill} with command validation before it emits shell steps.`,
      example: { session: date, skill: dec.skill, issue: `A shell command failed after ${dec.skill}.`, commands: unique(failures.map(e => e.cmd)).slice(0, 3) },
    });

    const df = categoryFamily(dec.category), sf = skillFamily(dec.skill);
    if (df !== 'general' && sf !== 'general' && df !== sf) occs.push({
      type: 'wrong-skill-routing', skill: dec.skill, agent: dec.agent,
      recommendation: `Clarify routing so ${dec.agent} sends ${dec.category} work to a ${df}-oriented skill instead of ${dec.skill}.`,
      example: { session: date, skill: dec.skill, issue: `Category "${dec.category}" does not align with ${dec.skill}.` },
    });
  }

  const counts = new Map();
  for (const dec of skillEvents) {
    const e = counts.get(dec.skill) || { count: 0, agents: new Set() };
    e.count += 1; e.agents.add(dec.agent || 'unknown');
    counts.set(dec.skill, e);
  }
  for (const [skill, e] of counts.entries()) {
    if (e.count >= 3) occs.push({
      type: 'repeated-invocation', skill, agent: [...e.agents][0] || 'unknown',
      recommendation: `Broaden ${skill} or adjust routing so the same task doesn't need ${e.count} passes.`,
      example: { session: date, skill, issue: `${skill} ran ${e.count} times in the same session.` },
    });
  }

  return occs;
}

function writeLearnings(filePath, date, session, decisions, patterns) {
  const skillsInvoked = unique(decisions.map(d => d.skill));
  const affected = unique(patterns.map(p => p.skill));
  const lines = [`# Session Learnings - ${date}`, '', '## High-Priority Skill Patterns Detected', ''];

  if (patterns.length === 0) {
    lines.push('No high-priority skill patterns were detected.', '');
  } else {
    patterns.forEach((p, i) => {
      lines.push(`${i + 1}. **${p.type}** (${p.skill}) - ${p.count} occurrence${p.count === 1 ? '' : 's'}`);
      lines.push(`   - Issue: ${p.issue}`);
      lines.push(`   - Recommendation: ${p.recommendation}`);
      lines.push('');
    });
  }

  lines.push('## Session Summary', '');
  if (session) lines.push(`- Session: ${session}`);
  lines.push(
    `- Skills invoked: ${skillsInvoked.length}`,
    `- Skill calls: ${decisions.length}`,
    `- Patterns detected: ${patterns.length}`,
    `- Affected skills: ${affected.length > 0 ? affected.join(', ') : 'none'}`,
    '',
  );
  lines.push('## Proposed Actions (awaiting your approval)', '');

  if (patterns.length === 0) {
    lines.push('- [ ] No action required');
  } else {
    unique(patterns.map(p => `${p.skill}|${p.recommendation}`)).forEach(entry => {
      lines.push(`- [ ] ${entry.split('|')[1]}`);
    });
  }

  fs.writeFileSync(filePath, `${lines.join('\n')}\n`, 'utf8');
}

function main() {
  const args = parseArgs(process.argv);
  const repoRoot = path.resolve(__dirname, '..', '..');
  const rawDir = path.join(repoRoot, '.conversations-claude', 'raw');
  const analysisDir = path.join(repoRoot, '.conversations-claude', 'analysis');

  ensureDir(analysisDir);

  const filter = e => (e.ts || '').startsWith(args.date) && (!args.session || e.session === args.session);

  const rawEvents = sortByTs(parseJsonl(path.join(rawDir, `${args.date}.jsonl`)).filter(filter));
  const decisions = sortByTs(parseJsonl(path.join(analysisDir, 'decisions.jsonl')).filter(filter).map(e => ({
    ts: e.ts, session: e.session || '', agent: e.agent || 'unknown',
    skill: e.skill || 'unknown', category: e.category || 'general', reason: e.reason || 'general', summary: e.summary || '',
  })));

  const patternsFile = path.join(analysisDir, 'patterns.json');
  const stored = readJson(patternsFile, { patterns: {} });
  const occs = detectOccurrences(decisions, rawEvents, args.date);
  for (const occ of occs) mergePattern(stored.patterns, occ, args.date);
  writeJson(patternsFile, stored);

  const grouped = (() => {
    const g = new Map();
    for (const o of occs) {
      const k = `${o.type}|${o.skill}`;
      const c = g.get(k) || { type: o.type, skill: o.skill, agent: o.agent, count: 0, recommendation: o.recommendation, issue: o.example.issue };
      c.count += 1; g.set(k, c);
    }
    return [...g.values()].sort((a, b) => b.count - a.count || a.skill.localeCompare(b.skill));
  })();

  const learningsPath = path.join(analysisDir, args.session ? `${args.date}-${args.session}-learnings.md` : `${args.date}-learnings.md`);
  writeLearnings(learningsPath, args.date, args.session, decisions, grouped);
}

main();
