# Agentic Team

## Team Structure

```mermaid
graph TD
    User(["👤 User Request"])
    Orch["🎯 Team Orchestrator\nClaude Sonnet 4.6\nCoordinates · Never implements"]

    Planner["📋 Planner\nClaude Opus 4.6\nResearch · Plan · No code"]
    Coder["💻 Coder\nGPT-5.3-Codex\nWrite code · Fix bugs"]
    Frontend["🎨 Frontend\nGemini 3 Pro\nUI/UX · React · Accessibility"]
    Playwright["🎭 team-playwright\nClaude Sonnet 4.5\nE2E tests — explicit request only"]

    User --> Orch
    Orch -->|"Step 1: Get plan"| Planner
    Orch -->|"Step 3: Implement"| Coder
    Orch -->|"Step 3: Design & UI"| Frontend
    Orch -.->|"on explicit request"| Playwright

    style User fill:#e8f4f8,stroke:#2196F3,color:#000
    style Orch fill:#fff3e0,stroke:#FF9800,color:#000
    style Planner fill:#f3e5f5,stroke:#9C27B0,color:#000
    style Coder fill:#e8f5e9,stroke:#4CAF50,color:#000
    style Frontend fill:#fce4ec,stroke:#E91E63,color:#000
    style Playwright fill:#f1f8e9,stroke:#8BC34A,color:#000
```

## Workflow

```mermaid
flowchart LR
    A(["User Request"]) --> B["Team Orchestrator"]
    B --> C["Step 1\nPlanner → plan"]
    C --> D["Step 2\nParse phases\n(parallel if no file overlap)"]
    D --> E["Step 3\nExecute phases"]
    E --> F["Step 4\nVerify & report"]

    E --> G["Coder\nlogic · APIs · services"]
    E --> H["Frontend\nUI · styling · components"]
    E -.-> I["team-playwright\ne2e — explicit only"]
```

## Agents

| Agent | Model | Role | Tools |
|---|---|---|---|
| **Team Orchestrator** | Claude Sonnet 4.6 | Breaks down tasks, delegates, never implements | `read`, `agent`, `memory` |
| **Planner** | Claude Opus 4.6 | Research, plan implementation steps, no code | `read`, `search`, `web`, `microsoft-learn/*` |
| **Coder** | GPT-5.3-Codex | Write code, fix bugs, implement features | `edit`, `execute`, `search`, `vscode` |
| **Frontend** | Gemini 3 Pro | UI/UX design, React components, accessibility | `edit`, `figma/*`, `context7/*`, `chrome-devtools/*` |
| **team-playwright** | Claude Sonnet 4.5 | E2E tests — only on explicit request | `execute`, `playwright/*` |
