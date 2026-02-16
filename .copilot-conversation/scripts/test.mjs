import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { describe, it, before, after } from 'node:test';
import assert from 'node:assert';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dataDir = path.join(__dirname, '../data');

const testSessionId = 'test-session-001';

const testHistory = {
  sessionId: testSessionId,
  startTime: '2026-02-08T10:00:00.000Z',
  endTime: '2026-02-08T10:05:00.000Z',
  status: 'completed',
  messages: [
    { role: 'user', timestamp: '2026-02-08T10:00:01.000Z', content: 'Fix the authentication bug' },
    { role: 'user', timestamp: '2026-02-08T10:02:00.000Z', content: 'Now add unit tests' }
  ]
};

const testTools = {
  sessionId: testSessionId,
  tools: [
    { timestamp: '2026-02-08T10:00:30.000Z', phase: 'pre', toolName: 'read_file' },
    { timestamp: '2026-02-08T10:00:31.000Z', phase: 'post', toolName: 'read_file', resultType: 'success' },
    { timestamp: '2026-02-08T10:01:00.000Z', phase: 'pre', toolName: 'replace_string_in_file' },
    { timestamp: '2026-02-08T10:01:05.000Z', phase: 'post', toolName: 'replace_string_in_file', resultType: 'success' },
    { timestamp: '2026-02-08T10:03:30.000Z', phase: 'pre', toolName: 'run_in_terminal' },
    { timestamp: '2026-02-08T10:03:35.000Z', phase: 'post', toolName: 'run_in_terminal', resultType: 'failure' }
  ]
};

const testAgent = {
  sessionId: testSessionId,
  agentName: 'Angular',
  events: [
    { timestamp: '2026-02-08T10:03:00.000Z', phase: 'start' },
    { timestamp: '2026-02-08T10:04:00.000Z', phase: 'stop' }
  ]
};

function writeTestData() {
  fs.mkdirSync(dataDir, { recursive: true });
  fs.writeFileSync(path.join(dataDir, `history-${testSessionId}.json`), JSON.stringify(testHistory));
  fs.writeFileSync(path.join(dataDir, `tools-${testSessionId}.json`), JSON.stringify(testTools));
  fs.writeFileSync(path.join(dataDir, `agents-Angular-${testSessionId}.json`), JSON.stringify(testAgent));
}

function cleanTestData() {
  const files = [
    path.join(dataDir, `history-${testSessionId}.json`),
    path.join(dataDir, `tools-${testSessionId}.json`),
    path.join(dataDir, `agents-Angular-${testSessionId}.json`),
    path.join(__dirname, `../conversations/conv-${testSessionId}.md`)
  ];
  files.forEach(f => { if (fs.existsSync(f)) fs.unlinkSync(f); });
}

describe('visualize.mjs', () => {
  before(() => writeTestData());
  after(() => cleanTestData());

  it('generates conv-{sessionId}.md for a specific session', () => {
    execSync(`node visualize.mjs ${testSessionId}`, { cwd: __dirname });

    const mdPath = path.join(__dirname, `../conversations/conv-${testSessionId}.md`);
    assert.ok(fs.existsSync(mdPath), 'output markdown file should exist');

    const md = fs.readFileSync(mdPath, 'utf-8');
    assert.ok(md.includes('```mermaid'), 'should contain mermaid code block');
    assert.ok(md.includes('sequenceDiagram'), 'should contain sequence diagram');
    assert.ok(md.includes('GH Copilot'), 'should have GH Copilot participant');
    assert.ok(md.includes('Tool Use'), 'should have Tool Use participant');
  });

  it('includes user prompts in the diagram', () => {
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${testSessionId}.md`), 'utf-8');
    assert.ok(md.includes('Fix the authentication bug'), 'should contain first user prompt');
    assert.ok(md.includes('Now add unit tests'), 'should contain second user prompt');
  });

  it('includes tool calls in the diagram', () => {
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${testSessionId}.md`), 'utf-8');
    assert.ok(md.includes('read_file'), 'should contain read_file tool call');
    assert.ok(md.includes('replace_string_in_file'), 'should contain replace tool call');
    assert.ok(md.includes('run_in_terminal'), 'should contain terminal tool call');
  });

  it('includes sub-agent in the diagram', () => {
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${testSessionId}.md`), 'utf-8');
    assert.ok(md.includes('Angular'), 'should contain Angular sub-agent');
    assert.ok(md.includes('Sub:'), 'should have Sub: prefix for agent participant');
  });

  it('includes inferred assistant responses', () => {
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${testSessionId}.md`), 'utf-8');
    assert.ok(md.includes('Bot-->>User:') && md.includes('processing'), 'should have inferred response arrow');
  });

  it('includes conversation start/end notes', () => {
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${testSessionId}.md`), 'utf-8');
    assert.ok(md.includes('Conversation starts'), 'should have start note');
    assert.ok(md.includes('Conversation ends'), 'should have end note');
  });

  it('includes metrics section', () => {
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${testSessionId}.md`), 'utf-8');
    assert.ok(md.includes('## Metrics'), 'should have metrics heading');
    assert.ok(md.includes('Total Tool Calls'), 'should have total calls metric');
    assert.ok(md.includes('Successful'), 'should have success metric');
    assert.ok(md.includes('Failed'), 'should have failed metric');
  });

  it('includes session metadata', () => {
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${testSessionId}.md`), 'utf-8');
    assert.ok(md.includes('**Started:**'), 'should have start time');
    assert.ok(md.includes('**Ended:**'), 'should have end time');
    assert.ok(md.includes('**Status:** completed'), 'should have status');
  });

  it('processes all sessions when no id provided', () => {
    execSync('node visualize.mjs', { cwd: __dirname });
    const mdPath = path.join(__dirname, `../conversations/conv-${testSessionId}.md`);
    assert.ok(fs.existsSync(mdPath), 'should generate output for discovered session');
  });

  it('handles session with no tools gracefully', () => {
    const noToolsId = 'test-no-tools';
    fs.writeFileSync(path.join(dataDir, `history-${noToolsId}.json`), JSON.stringify({
      sessionId: noToolsId,
      startTime: '2026-02-08T11:00:00.000Z',
      status: 'active',
      messages: [{ role: 'user', timestamp: '2026-02-08T11:00:01.000Z', content: 'Hello' }]
    }));

    execSync(`node visualize.mjs ${noToolsId}`, { cwd: __dirname });
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${noToolsId}.md`), 'utf-8');
    assert.ok(md.includes('Hello'), 'should contain user message');
    assert.ok(!md.includes('Tool Use'), 'should not have Tool Use participant');
    assert.ok(!md.includes('[response]'), 'no response without agent activity');

    fs.unlinkSync(path.join(dataDir, `history-${noToolsId}.json`));
    fs.unlinkSync(path.join(__dirname, `../conversations/conv-${noToolsId}.md`));
  });

  it('handles malformed data from hooks (null toolName, object timestamps)', () => {
    const badId = 'test-bad-data';
    fs.writeFileSync(path.join(dataDir, `history-${badId}.json`), JSON.stringify({
      sessionId: badId,
      startTime: {},
      status: 'active',
      messages: [
        { role: 'user', timestamp: {}, content: 'Test prompt' }
      ]
    }));
    fs.writeFileSync(path.join(dataDir, `tools-${badId}.json`), JSON.stringify({
      sessionId: badId,
      tools: [
        { timestamp: {}, phase: 'pre', toolName: null },
        { timestamp: {}, phase: 'pre', toolName: null },
        { timestamp: '2026-02-08T11:00:01.000Z', phase: 'pre', toolName: 'read_file' },
        { timestamp: '2026-02-08T11:00:02.000Z', phase: 'post', toolName: 'read_file', resultType: 'success' }
      ]
    }));

    execSync(`node visualize.mjs ${badId}`, { cwd: __dirname });
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${badId}.md`), 'utf-8');

    assert.ok(md.includes('Test prompt'), 'should contain user message despite bad timestamp');
    assert.ok(md.includes('read_file'), 'should include valid tool calls');
    assert.ok(!md.includes('null'), 'should not render null toolName in diagram');
    assert.ok(md.includes('**Started:** N/A'), 'should show N/A for object startTime');

    fs.unlinkSync(path.join(dataDir, `history-${badId}.json`));
    fs.unlinkSync(path.join(dataDir, `tools-${badId}.json`));
    fs.unlinkSync(path.join(__dirname, `../conversations/conv-${badId}.md`));
  });

  it('infers response before second user message after tool activity', () => {
    const respId = 'test-response-inference';
    fs.writeFileSync(path.join(dataDir, `history-${respId}.json`), JSON.stringify({
      sessionId: respId,
      startTime: '2026-02-08T12:00:00.000Z',
      status: 'active',
      messages: [
        { role: 'user', timestamp: '2026-02-08T12:00:01.000Z', content: 'First prompt' },
        { role: 'user', timestamp: '2026-02-08T12:01:00.000Z', content: 'Second prompt' }
      ]
    }));
    fs.writeFileSync(path.join(dataDir, `tools-${respId}.json`), JSON.stringify({
      sessionId: respId,
      tools: [
        { timestamp: '2026-02-08T12:00:10.000Z', phase: 'pre', toolName: 'grep_search' },
        { timestamp: '2026-02-08T12:00:15.000Z', phase: 'post', toolName: 'grep_search', resultType: 'success' }
      ]
    }));

    execSync(`node visualize.mjs ${respId}`, { cwd: __dirname });
    const md = fs.readFileSync(path.join(__dirname, `../conversations/conv-${respId}.md`), 'utf-8');

    const lines = md.split('\n');
    const responseIdx = lines.findIndex(l => l.includes('[response]'));
    const secondPromptIdx = lines.findIndex(l => l.includes('Second prompt'));
    assert.ok(responseIdx > -1, 'should have inferred response');
    assert.ok(responseIdx < secondPromptIdx, 'response should appear before second user prompt');

    fs.unlinkSync(path.join(dataDir, `history-${respId}.json`));
    fs.unlinkSync(path.join(dataDir, `tools-${respId}.json`));
    fs.unlinkSync(path.join(__dirname, `../conversations/conv-${respId}.md`));
  });
});
