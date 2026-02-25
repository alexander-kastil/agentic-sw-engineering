# Custom Agents Overview

## What are Custom Agents?

Custom agents are specialized AI personas configured with specific tools, instructions, and handoffs to handle targeted development tasks. Instead of manually selecting tools and switching context for each workflow, you define an agent once with the exact capabilities and behavior needed, then seamlessly switch to it in chat.

Agents can work independently or orchestrate multi-step workflows using handoffs—guided transitions that pass context and pre-filled prompts between agents.

## Why Use Custom Agents?

Different tasks require different capabilities and behaviors. A planning agent might only need read-only tools to research architecture without risking accidental code changes, while an implementation agent needs full editing power. Custom agents ensure the AI has exactly the right tools and instructions for each task, delivering consistent, task-appropriate responses.

Handoffs enable guided sequential workflows—for example, planning → implementation → code review—giving developers control to review and approve each step before moving forward.

## Sample Agent Configuration

```yaml
---
description: Generate an implementation plan
tools: ['search', 'fetch']
handoffs:
  - label: Start Implementation
    agent: implementation
    prompt: Now implement the plan outlined above.
    send: false
    model: GPT-5.2 (copilot)
---
```

## Handoffs

Handoffs enable guided sequential workflows that transition between agents with suggested next steps and pre-filled prompts. After a chat response completes, handoff buttons let users switch to the next agent in multi-step workflows like planning → implementation → code review.

Define handoffs in the agent file frontmatter (YAML) with the following properties:

- label: The display text shown on the handoff button
- agent: The target agent identifier to switch to
- prompt: The prompt text to send to the target agent
- send (optional): Boolean flag to auto-submit the prompt (default is false)
- model (optional): The language model to use when the handoff executes

## Links & Resources

- [VS Code Custom Agents Documentation](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Third-party agents in Visual Studio Code](https://code.visualstudio.com/docs/copilot/agents/third-party-agents)
