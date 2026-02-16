import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dataDir = path.join(__dirname, '../data');

function parseDebugLog(filePath) {
  if (!fs.existsSync(filePath)) return [];

  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n');
  const events = [];

  for (const line of lines) {
    if (!line.includes('RAW:')) continue;

    const rawMatch = line.match(/RAW:\s*({.*})/);
    if (!rawMatch) continue;

    try {
      const data = JSON.parse(rawMatch[1]);
      const hook = line.match(/\[(\w+-\w+|\w+)\]/)?.[1];

      events.push({
        timestamp: data.timestamp,
        hookEventName: data.hookEventName,
        hook,
        toolName: data.tool_name,
        toolInput: data.tool_input,
        toolUseId: data.tool_use_id
      });
    } catch (e) {
      // Skip malformed JSON
    }
  }

  return events;
}

function buildLevel1(history) {
  const flow = [];
  
  if (history.messages) {
    history.messages.forEach((msg, idx) => {
      if (!msg || !msg.content) return;
      flow.push({
        sequence: idx + 1,
        type: 'message',
        role: msg.role,
        content: msg.content.substring(0, 200) + (msg.content.length > 200 ? '...' : ''),
        fullContent: msg.content,
        timestamp: msg.timestamp
      });
    });
  }

  return flow;
}

function consolidateSession(sessionId) {
  const historyPath = path.join(dataDir, `history-${sessionId}.json`);
  const toolsPath = path.join(dataDir, `tools-${sessionId}.json`);
  const debugPath = path.join(dataDir, `debug-${sessionId}.log`);

  if (!fs.existsSync(historyPath)) {
    console.error(`❌ History file not found: history-${sessionId}.json`);
    return null;
  }

  const history = JSON.parse(fs.readFileSync(historyPath, 'utf-8'));
  let tools = [];
  if (fs.existsSync(toolsPath)) {
    const toolsData = JSON.parse(fs.readFileSync(toolsPath, 'utf-8'));
    tools = Array.isArray(toolsData.tools) ? toolsData.tools : [];
  }

  const debugEvents = parseDebugLog(debugPath);

  // Create unified datasource
  const unified = {
    sessionId,
    metadata: {
      startTime: history.startTime,
      endTime: history.endTime,
      status: history.status,
      generatedAt: new Date().toISOString()
    },
    conversationFlow: {
      level1: buildLevel1(history),
      level1_5: buildLevel1WithSummaries(history, tools, debugEvents),
      level2: buildLevel2(history, tools, debugEvents)
    }
  };

  return unified;
}

function buildLevel1WithSummaries(history, tools, debugEvents) {
  const flow = [];
  
  if (!history.messages || history.messages.length === 0) {
    return flow;
  }

  history.messages.forEach((msg, msgIdx) => {
    if (!msg || !msg.content) return;

    const msgTime = new Date(msg.timestamp).getTime();
    const nextMsgTime = (msgIdx + 1 < history.messages.length) 
      ? new Date(history.messages[msgIdx + 1].timestamp).getTime()
      : Date.now();

    // Add user message
    flow.push({
      sequence: flow.length + 1,
      type: 'userMessage',
      role: msg.role,
      content: msg.content.substring(0, 200) + (msg.content.length > 200 ? '...' : ''),
      fullContent: msg.content,
      timestamp: msg.timestamp
    });

    // Find all tool calls between this message and the next
    const actionsInRange = tools.filter(t => {
      const toolTime = new Date(t.timestamp).getTime();
      return toolTime >= msgTime && toolTime < nextMsgTime;
    });

    if (actionsInRange.length > 0) {
      const summary = generateActionSummary(actionsInRange, msgIdx, msgTime, nextMsgTime);
      flow.push({
        sequence: flow.length + 1,
        type: 'actionSummary',
        userPromptIndex: msgIdx,
        actionCount: actionsInRange.length,
        summary: summary.text,
        details: summary.details,
        duration: `${((nextMsgTime - msgTime) / 1000).toFixed(1)}s`,
        timestampRange: {
          start: new Date(msgTime).toISOString(),
          end: new Date(nextMsgTime).toISOString()
        }
      });
    }
  });

  return flow;
}

function generateActionSummary(tools, promptIdx, startTime, endTime) {
  const grouped = {};
  const toolSequence = [];

  tools.forEach(t => {
    if (!grouped[t.toolName]) {
      grouped[t.toolName] = 0;
    }
    grouped[t.toolName]++;
    toolSequence.push(t.toolName);
  });

  // Find top actions and interesting ones
  const sorted = Object.entries(grouped).sort((a, b) => b[1] - a[1]);
  const topActions = sorted.slice(0, 3);

  let text = '**Copilot Actions**: ';
  const details = [];

  // Create readable summary
  if (topActions.length === 1 && topActions[0][1] === 1) {
    text += `Executed ${topActions[0][0]}`;
    details.push(topActions[0][0]);
  } else if (topActions.length === 1) {
    text += `Executed ${topActions[0][1]} ${topActions[0][0]} calls`;
    details.push(`${topActions[0][0]} (${topActions[0][1]})`);
  } else {
    text += `Executed ${tools.length} actions: `;
    const summary = topActions.map(([name, count]) => 
      count === 1 ? name : `${count}× ${name}`
    ).join(', ');
    text += summary;
    topActions.forEach(([name, count]) => {
      details.push(`${name} (${count})`);
    });
  }

  // Add timing
  const duration = ((endTime - startTime) / 1000).toFixed(1);
  text += ` in ${duration}s`;

  return { text, details, toolSequence };
}


function buildLevel2(history, tools, debugEvents) {
  const flow = buildLevel1(history);
  const toolCallMap = new Map();

  // Map debug events to tool calls
  debugEvents.forEach((evt) => {
    if (evt.hookEventName === 'PreToolUse') {
      if (!toolCallMap.has(evt.toolUseId)) {
        toolCallMap.set(evt.toolUseId, { start: evt, end: null, result: null });
      } else {
        toolCallMap.get(evt.toolUseId).start = evt;
      }
    }
  });

  // Match tool results
  tools.forEach((tool, idx) => {
    const toolEntry = {
      sequence: flow.length + idx + 1,
      type: 'toolCall',
      phase: tool.phase,
      toolName: tool.toolName,
      timestamp: tool.timestamp,
      resultType: tool.resultType || 'pending',
      sourceIndex: idx
    };

    // Try to find matching debug event
    const debugInfo = debugEvents.find(
      e => e.toolName === tool.toolName && 
           Math.abs(new Date(e.timestamp).getTime() - new Date(tool.timestamp).getTime()) < 1000
    );

    if (debugInfo) {
      toolEntry.debugInfo = {
        hookEventName: debugInfo.hookEventName,
        toolInput: debugInfo.toolInput,
        toolUseId: debugInfo.toolUseId
      };
    }

    flow.push(toolEntry);
  });

  // Sort by timestamp
  flow.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

  // Resequence
  flow.forEach((item, idx) => {
    item.sequence = idx + 1;
  });

  return flow;
}

function saveConsolidated(sessionId, unified) {
  const outPath = path.join(__dirname, '../data', `conv-${sessionId}.json`);
  fs.writeFileSync(outPath, JSON.stringify(unified, null, 2), 'utf-8');
  console.log(`✓ Consolidated data saved to conv-${sessionId}.json`);
  return outPath;
}

function main() {
  const sessionId = process.argv[2];

  if (sessionId) {
    console.log(`📍 Processing session: ${sessionId}`);
    const unified = consolidateSession(sessionId);
    if (unified) {
      saveConsolidated(sessionId, unified);
      console.log(`\n✓ Level 1 (User-Agent): ${unified.conversationFlow.level1.length} events`);
      console.log(`✓ Level 1.5 (Two-way + Summaries): ${unified.conversationFlow.level1_5.length} events`);
      console.log(`✓ Level 2 (with Tools): ${unified.conversationFlow.level2.length} events`);
    }
    return;
  }

  console.log('❌ No session ID provided');
  console.log('Usage: node consolidate.mjs <sessionId>');
}

export { consolidateSession, buildLevel1, buildLevel1WithSummaries, buildLevel2, parseDebugLog };

if (process.argv[1] && process.argv[1].endsWith('consolidate.mjs')) {
  main();
}
