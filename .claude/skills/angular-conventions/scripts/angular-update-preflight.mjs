#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join, dirname, basename } from 'node:path';

const args = process.argv.slice(2);
const flag = (name, def = null) => {
  const i = args.indexOf(`--${name}`);
  return i === -1 ? def : args[i + 1];
};
const has = (name) => args.includes(`--${name}`);

if (has('help')) {
  console.log(`angular-update-preflight: read every Angular workspace's compatibility gate off disk and the registry.

  --root <dir>        scan <dir> recursively (depth 3) for angular.json
  --workspace <dir>   check one workspace; repeatable
  --offline           skip npm registry lookups (no "latest" columns)
  --json              emit JSON instead of the table
  --help

Exit code is 1 when any workspace is BLOCKED, else 0.`);
  process.exit(0);
}

const OFFLINE = has('offline');
const npmView = (spec, field) => {
  if (OFFLINE) return null;
  try {
    const out = execFileSync('npm', ['view', spec, field, '--json'], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
      shell: process.platform === 'win32',
    });
    return JSON.parse(out);
  } catch {
    return null;
  }
};

const readJson = (p) => {
  try {
    return JSON.parse(readFileSync(p, 'utf8'));
  } catch {
    return null;
  }
};

const findWorkspaces = (root, depth = 3) => {
  const found = [];
  const walk = (dir, d) => {
    if (d < 0) return;
    let entries;
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    if (entries.some((e) => e.isFile() && e.name === 'angular.json')) found.push(dir);
    for (const e of entries) {
      if (!e.isDirectory()) continue;
      if (e.name === 'node_modules' || e.name.startsWith('.')) continue;
      walk(join(dir, e.name), d - 1);
    }
  };
  walk(root, depth);
  return found;
};

const workspaces = [];
for (let i = 0; i < args.length; i++) if (args[i] === '--workspace') workspaces.push(args[i + 1]);
if (!workspaces.length) {
  const root = flag('root', process.cwd());
  workspaces.push(...findWorkspaces(root));
}
if (!workspaces.length) {
  console.error('no angular.json found; pass --root or --workspace');
  process.exit(2);
}

const satisfiesRange = (version, range) => {
  if (!version || !range) return null;
  const [maj, min, pat] = version.split('.').map(Number);
  const cmp = (a, b) => {
    const [x, y, z] = b.split('.').map(Number);
    if (a[0] !== x) return a[0] - x;
    if ((a[1] ?? 0) !== (y ?? 0)) return (a[1] ?? 0) - (y ?? 0);
    return (a[2] ?? 0) - (z ?? 0);
  };
  const v = [maj, min ?? 0, pat ?? 0];
  let unparsed = false;
  const satisfied = range.split('||').some((clause) => {
    const parts = clause.trim().split(/\s+/).filter(Boolean);
    return parts.every((p) => {
      let m;
      if ((m = p.match(/^[~^](\d+\.\d+(?:\.\d+)?)$/))) {
        const b = m[1].split('.').map(Number);
        if (p[0] === '~') return v[0] === b[0] && v[1] === (b[1] ?? 0) && cmp(v, m[1]) >= 0;
        return v[0] === b[0] && cmp(v, m[1]) >= 0;
      }
      if ((m = p.match(/^>=(\d+(?:\.\d+)*)$/))) return cmp(v, m[1]) >= 0;
      if ((m = p.match(/^>(\d+(?:\.\d+)*)$/))) return cmp(v, m[1]) > 0;
      if ((m = p.match(/^<=(\d+(?:\.\d+)*)$/))) return cmp(v, m[1]) <= 0;
      if ((m = p.match(/^<(\d+(?:\.\d+)*)$/))) return cmp(v, m[1]) < 0;
      if ((m = p.match(/^=?(\d+(?:\.\d+)*)$/))) return cmp(v, m[1]) === 0;
      unparsed = true;
      return false;
    });
  });
  if (unparsed && !satisfied) return null;
  return satisfied;
};

const msalMatrix = (readmePath) => {
  if (!existsSync(readmePath)) return null;
  const txt = readFileSync(readmePath, 'utf8');
  const rows = [];
  for (const line of txt.split('\n')) {
    if (!line.trim().startsWith('|')) continue;
    const cells = line.split('|').slice(1, -1).map((c) => c.trim());
    if (cells.length < 2) continue;
    const msal = cells[0].match(/v(\d+)\s*$/);
    const last = cells[cells.length - 1];
    if (!msal || !/^\d+(\s*,\s*\d+)*$/.test(last)) continue;
    rows.push({ msal: Number(msal[1]), angular: last.split(',').map((s) => Number(s.trim())) });
  }
  return rows.length ? rows : null;
};

const results = [];
for (const ws of workspaces) {
  const pkg = readJson(join(ws, 'package.json'));
  if (!pkg) continue;
  const dep = (n) => pkg.dependencies?.[n] ?? pkg.devDependencies?.[n] ?? null;
  const installed = (n) => readJson(join(ws, 'node_modules', n, 'package.json'))?.version ?? null;

  const r = { workspace: ws, name: basename(ws), findings: [], verdict: 'OK' };
  const add = (level, msg) => {
    r.findings.push(`${level}: ${msg}`);
    if (level === 'BLOCKED') r.verdict = 'BLOCKED';
    else if (level === 'WARN' && r.verdict === 'OK') r.verdict = 'WARN';
  };

  r.core = { declared: dep('@angular/core'), installed: installed('@angular/core') };
  r.core.latest = npmView('@angular/core', 'version');
  if (!r.core.installed) add('WARN', 'no node_modules: run npm install before trusting anything below');
  if (r.core.installed && r.core.latest && r.core.installed !== r.core.latest)
    add('WARN', `@angular/core ${r.core.installed} behind latest ${r.core.latest}`);

  const compilerCli = readJson(join(ws, 'node_modules', '@angular/compiler-cli', 'package.json'));
  r.typescript = {
    declared: dep('typescript'),
    installed: installed('typescript'),
    peerRange: compilerCli?.peerDependencies?.typescript ?? null,
  };
  if (r.typescript.installed && r.typescript.peerRange) {
    const ok = satisfiesRange(r.typescript.installed, r.typescript.peerRange);
    r.typescript.inRange = ok;
    if (ok === false)
      add('BLOCKED', `typescript ${r.typescript.installed} outside compiler peer range ${r.typescript.peerRange}`);
  }

  const cliPkg = readJson(join(ws, 'node_modules', '@angular/cli', 'package.json'));
  r.node = {
    required: cliPkg?.engines?.node ?? npmView(`@angular/cli@${r.core.declared?.replace(/[^\d.]/g, '') || 'latest'}`, 'engines')?.node ?? null,
    running: process.version.replace(/^v/, ''),
  };
  if (r.node.required) {
    const ok = satisfiesRange(r.node.running, r.node.required);
    r.node.runningInRange = ok;
    if (ok === false) add('BLOCKED', `running node ${r.node.running} outside required ${r.node.required}`);
  }

  const dockerfile = join(ws, 'Dockerfile');
  if (existsSync(dockerfile)) {
    const line = readFileSync(dockerfile, 'utf8')
      .split('\n')
      .find((l) => /^\s*FROM\s+node:/i.test(l));
    if (line) {
      const tag = line.match(/node:([^\s]+)/)?.[1] ?? '';
      const version = tag.replace(/-alpine|-slim|-bookworm.*/g, '');
      r.image = { line: line.trim(), tag, floating: /^\d+$/.test(version) || version === 'latest' };
      if (r.image.floating)
        add('WARN', `Dockerfile base tag node:${tag} floats; Angular's node floor moves inside a minor line, pin an explicit version`);
      else if (r.node.required && satisfiesRange(version, r.node.required) === false)
        add('BLOCKED', `Dockerfile node ${version} outside required ${r.node.required}`);
    }
  }

  const msalVer = installed('@azure/msal-angular') ?? dep('@azure/msal-angular');
  if (msalVer) {
    const major = Number(String(msalVer).replace(/[^\d.]/g, '').split('.')[0]);
    const matrix = msalMatrix(join(ws, 'node_modules', '@azure/msal-angular', 'README.md'));
    const angularMajor = Number(String(r.core.installed ?? r.core.declared ?? '').replace(/[^\d.]/g, '').split('.')[0]);
    r.msal = { version: String(msalVer), major, matrix: matrix?.find((x) => x.msal === major)?.angular ?? null };
    if (r.msal.matrix && angularMajor && !r.msal.matrix.includes(angularMajor))
      add('BLOCKED', `@azure/msal-angular v${major} does not support Angular ${angularMajor} (supports ${r.msal.matrix.join(', ')}); README matrix, not the peer range`);
  }

  r.unmetPeers = [];
  for (const name of Object.keys({ ...pkg.dependencies, ...pkg.devDependencies })) {
    if (name.startsWith('@angular/')) continue;
    const peer = readJson(join(ws, 'node_modules', name, 'package.json'))?.peerDependencies?.['@angular/core'];
    if (!peer || !r.core.installed) continue;
    if (satisfiesRange(r.core.installed, peer) === false) {
      const tags = npmView(name, 'dist-tags');
      r.unmetPeers.push({ name, peer, latest: tags?.latest ?? null, next: tags?.next ?? null });
      add('WARN', `${name} peers @angular/core ${peer}, unmet by ${r.core.installed}${tags?.latest ? ` (latest ${tags.latest}${tags.next ? `, next ${tags.next}` : ''})` : ''}`);
    }
  }

  results.push(r);
}

if (has('json')) {
  console.log(JSON.stringify(results, null, 2));
} else {
  for (const r of results) {
    console.log(`\n=== ${r.name}  [${r.verdict}]`);
    console.log(`    path        ${r.workspace}`);
    console.log(`    core        declared ${r.core.declared ?? '-'} | installed ${r.core.installed ?? '-'} | latest ${r.core.latest ?? '-'}`);
    console.log(`    typescript  declared ${r.typescript.declared ?? '-'} | installed ${r.typescript.installed ?? '-'} | peer ${r.typescript.peerRange ?? '-'}`);
    console.log(`    node        required ${r.node.required ?? '-'} | running ${r.node.running}`);
    if (r.image) console.log(`    image       ${r.image.line}${r.image.floating ? '  (floating)' : ''}`);
    if (r.msal) console.log(`    msal        v${r.msal.version} | supports Angular ${r.msal.matrix?.join(', ') ?? '?'}`);
    for (const f of r.findings) console.log(`    - ${f}`);
  }
}

const blocked = results.filter((r) => r.verdict === 'BLOCKED').length;
const warn = results.filter((r) => r.verdict === 'WARN').length;
console.log(`\npreflight: workspaces=${results.length} blocked=${blocked} warn=${warn} ok=${results.length - blocked - warn}`);
process.exit(blocked ? 1 : 0);
