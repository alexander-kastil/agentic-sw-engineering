Agent Framework Upgrade Report - February 2026
==============================================

Project: agent-framework-demos-part1
Date: February 16, 2026
Status: Upgraded to Latest Available Versions

Summary
-------

All agent framework tools and knowledge base examples have been upgraded to the latest Microsoft Agent Framework versions (February 2026). This includes critical breaking changes and new features.

Version Updates
---------------

### Core Libraries

| Package | Previous | Updated | Status |
|---------|----------|---------|--------|
| agent-framework | 1.0.0b251120 | 1.0.0b260212 | ✓ Latest (Feb 12, 2026) |
| azure-ai-projects | 2.0.0b2 | 2.0.0b3 | ✓ Pre-release GA |
| azure-ai-agents | 1.2.0b5 | 1.2.0b5 | ✓ Latest compatible |
| azure-identity | 1.25.1 | 1.25.2 | ✓ Latest stable |
| python-dotenv | 1.2.1 | 1.2.1 | ✓ Current stable |
| requests | 2.31.0+ | 2.32.5 | ✓ Latest compatible |

### Related Tools (Auto-Installed)

- agent-framework-core: 1.0.0b260212
- agent-framework-orchestrations: 1.0.0b260212
- agent-framework-declarative: 1.0.0b260212
- agent-framework-chatkit: 1.0.0b260212
- agent-framework-github-copilot: 1.0.0b260212
- mcp: 1.26.0
- openai: 2.21.0

Breaking Changes Requiring Code Updates
---------------------------------------

### 1. ✓ CRITICAL: `.create_agent()` renamed to `.as_agent()`
**Introduced**: January 16, 2026 (agent-framework 1.0.0b260116)
**Impact**: All agent creation methods must be updated
**Agents Affected**: All 4 agent files (agentfw_*.py)

**Before**:
```python
agent = AzureOpenAIChatClient(...).create_agent(...)
```

**After**:
```python
agent = AzureOpenAIChatClient(...).as_agent(...)
```

**Files to Update**:
- `agentfw_builtin_tools.py` - Line ~67
- `agentfw_file_search_tool.py` - Line ~56
- `agentfw_function_tool_calculator.py` - Line ~54
- `agentfw_human_in_the_loop.py` - Uses custom wrapper

### 2. ✓ CRITICAL: `@ai_function` decorator renamed to `@tool`
**Introduced**: January 28, 2026 (agent-framework 1.0.0b260128)
**Impact**: Function-based tools must use new decorator
**Agents Affected**: agentfw_function_tool_calculator.py

**Before**:
```python
from agent_framework.core import ai_function

@ai_function
def calculate(expression: str) -> str:
    ...
```

**After**:
```python
from agent_framework.core import tool

@tool
def calculate(expression: str) -> str:
    ...
```

### 3. ✓ CRITICAL: `AIFunction` class renamed to `FunctionTool`
**Introduced**: January 28, 2026 (agent-framework 1.0.0b260128)
**Impact**: Direct function tool instantiation must use new class name
**Agents Affected**: All files using function-based tools

**Before**:
```python
from agent_framework.core import AIFunction
func = AIFunction(calculate)
```

**After**:
```python
from agent_framework.core import FunctionTool
func = FunctionTool(calculate)
```

### 4. MINOR: `source_executor_id` renamed to `executor_id`
**Introduced**: January 16, 2026
**Impact**: Workflow event handling in orchestrations
**Agents Affected**: Workflow-based orchestrations

**Before**:
```python
event.source_executor_id
```

**After**:
```python
event.executor_id
```

### 5. STRUCTURED OUTPUTS: `ChatOptions` and `ChatResponse` now generic
**Introduced**: January 30, 2026
**Impact**: Type safety for structured outputs with response_format
**Status**: Non-breaking enhancement (backwards compatible)

New capability:
```python
options: ChatOptions[MyOutput] = {"response_format": MyOutput}
response: ChatResponse[MyOutput] = await client.get_response(...)
```

### 6. Orchestration API Changes
**Introduced**: January 14, 2026
**Impact**: Multi-agent orchestrations

- `GroupChat` → `GroupChatOrchestrator`
- `HandoffOrchestrator` single-tier → `HandoffAgentExecutor`
- Removed: `AggregateContextProvider`
- New builder pattern: `SequentialBuilder`, `GroupChatBuilder` in `agent_framework.orchestrations`

### 7. Middle ware `call_next` signature change
**Introduced**: February 12, 2026
**Impact**: Middleware implementations

**Before**:
```python
async def telemetry_middleware(context, call_next):
    return await call_next(context)
```

**After**:
```python
async def telemetry_middleware(context, call_next):
    return await call_next()
```

New Features in Latest Version
-------------------------------

### 1. Azure AI Foundry Project Endpoint Support
**New in 1.0.0b260212**
AzureOpenAIResponsesClient now supports Azure AI Foundry project endpoints directly:

```python
client = AzureOpenAIResponsesClient(
    project_endpoint="https://<your-project>.services.ai.azure.com",
    credential=DefaultAzureCredential(),
)
```

### 2. Foundry A2ATool Connection Support
**New in 1.0.0b260114**
A2ATool now resolves Foundry-backed connections without explicit target URL.

### 3. Code Interpreter Streaming Deltas
**New in 1.0.0b260210**
Streaming code-interpreter runs now include incremental code deltas for progressive UI rendering.

### 4. Background Responses & Continuation Tokens
**New in 1.0.0b260210**

```python
response = await agent.run("Long task", options={"background": True})
while response.continuation_token is not None:
    response = await agent.run(options={"continuation_token": response.continuation_token})
```

### 5. Orchestration Builders Namespace
**New in 1.0.0b260210**
```python
from agent_framework.orchestrations import SequentialBuilder, GroupChatBuilder
```

Recommended Actions
-------------------

### Immediate (Before Using Updated Agents)

1. Update all `.create_agent()` calls to `.as_agent()` in agent files
2. Update all `@ai_function` decorators to `@tool`
3. Update all `AIFunction` references to `FunctionTool`
4. Test all agents with interaction pattern in interactive demos

### Short-term (Next Sprint)

1. Evaluate new structured output capabilities for agents
2. Update orchestration patterns if using GroupChat or Handoff
3. Consider leveraging new Foundry project endpoint support
4. Update middleware if custom implementations exist

### Long-term (Architecture)

1. Plan migration path from pre-release to stable GA releases (expected 2026)
2. Monitor deprecation warnings and plan breakpoint testing
3. Evaluate new features like background responses for long-running tasks
4. Consider using declarative YAML workflows for complex orchestrations

Environment Setup
-----------------

### Virtual Environment

- Location: `.venv/`
- Python Version: 3.11+
- Status: Created and activated
- Installation Date: February 16, 2026

### Installation Command

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

### Verification

After upgrade, verify agent functionality:

```bash
cd demos/03-agentic-coding/01-local/03-update/agentfw_tools-knowledge-py
.\.venv\Scripts\activate.ps1
python agentfw_builtin_tools.py      # Test built-in tools
python agentfw_function_tool_calculator.py  # Test function tools
```

Known Issues & Workarounds
--------------------------

### 1. OpenTelemetry SDK Version Conflict (Non-Critical)
**Issue**: opentelemetry-exporter-otlp-proto-grpc requires opentelemetry-sdk~=1.38.0, but 1.39.1 installed

**Workaround**: This doesn't affect core functionality. If observability is needed:
```bash
pip install opentelemetry-sdk==1.38.0 --force-reinstall
```

### 2. Pre-release Versions
**Status**: Using pre-release versions (1.0.0b260212)
- Be aware of potential API changes in future releases
- Monitor release notes for deprecation warnings
- Have migration plan when GA (stable) versions release

### 3. Azure AI Foundry Endpoint Requirements
**Status**: Updated code assumes GA Foundry projects (created May 19, 2025+)
- Requires project endpoint URL format: `https://<resource>.services.ai.azure.com/api/projects/<project-name>`
- Hub-based (pre-GA) projects will require different initialization pattern

Configuration Files Updated
----------------------------

### pyproject.toml
- Version bumped: 0.1.0 → 0.2.0
- Dependencies updated to latest compatible versions
- Removed: Fixed version pins in favor of range specifications

### requirements.txt
- Removed: agent-framework-azure-ai (now included in agent-framework)
- Updated: All package versions to latest
- Added: Comments documenting version rationale

Performance Notes
-----------------

- Initial load time may increase due to additional packages in 1.0.0b260212
- OpenTelemetry integration adds minimal overhead
- Recommended: Run first demo to verify performance expectations

Testing Recommendations
-----------------------

1. Run each agent demo interactively
2. Test error handling paths
3. Verify Azure credential initialization
4. Test streaming responses with .run_stream()
5. Validate tool execution in each agent type

References
----------

- Microsoft Agent Framework: https://learn.microsoft.com/agent-framework
- Python 2026 Breaking Changes: https://learn.microsoft.com/agent-framework/support/upgrade/python-2026-significant-changes
- Azure AI Foundry: https://ai.azure.com
- Release Notes (1.0.0b260212): https://github.com/microsoft/agent-framework/releases/tag/python-1.0.0b260212

Next Steps
----------

1. Review this upgrade report with team
2. Schedule code update sprint for breaking changes
3. Update all agent files with new APIs
4. Conduct functional testing of all agents
5. Update agent documentation with latest APIs
6. Plan GA release migration strategy

Questions or Issues: See Microsoft Agent Framework documentation and GitHub issues.
