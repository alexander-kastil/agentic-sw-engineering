---
name: find-skills
description: Help users discover and install specialized skills that extend GitHub Copilot capabilities. Use when users ask how to do something, whether a skill exists for a task, or want to find tools and workflows. Covers skill discovery, installation, and capability extension. Keywords: find skill, search skill, install skill, extend capabilities, discover tools, agent skill.
---

# Find Skills

Help users discover and install skills that extend GitHub Copilot with specialized capabilities.

Use this skill when users:

- Ask "how do I do X" where X might have an existing skill
- Request "find a skill for X" or "is there a skill for X"
- Ask "can you do X" where X involves specialized capabilities
- Want to explore or extend Copilot capabilities
- Are looking for domain-specific tools, templates, or workflows
- Mention they wish they had help with a specific capability area (design, testing, deployment, etc.)

## Understanding the Skills Ecosystem

GitHub Copilot skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and bundled resources. Skills contain:

- Detailed instructions and workflows
- Code samples and templates
- Reference documentation
- Scripts and automation tools

Browse available skills at [https://skills.sh/](https://skills.sh/)

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help, identify:

1. The domain (React, testing, design, deployment, documentation, etc.)
2. The specific task (writing tests, creating animations, reviewing PRs, etc.)
3. Whether this is specialized enough that a skill likely exists

### Step 2: Search the Skills Directory

Navigate to skills.sh and search with relevant keywords:

- User asks "how do I make my React app faster?" → Search for "react performance"
- User asks "can you help me with PR reviews?" → Search for "pr review"
- User asks "I need to create a changelog" → Search for "changelog"

Explore popular skill sources:

- anthropics/skills
- vercel-labs/skills
- microsoft official skills
- community-contributed skills

### Step 3: Present Options to the User

When you find relevant skills, share:

1. The skill name and description
2. What problem it solves
3. When to use it
4. Link to skills.sh for installation details

Example response:

```
I found a skill that might help! The "react-state-management" skill provides
patterns for managing state across React projects using modern libraries.

Check it out: https://skills.sh/[organization]/[collection]/react-state-management
```

### Step 4: Offer Direct Installation

If the user wants to use a skill, help them install it by:

1. Providing the exact skill name and source
2. Directing them to the installation instructions on skills.sh
3. Explaining what the skill will add to their workflow

## Common Skill Categories

When searching, consider these common domains:

Web Development: React, Next.js, TypeScript, CSS, Tailwind, Angular, Vue
Testing: Playwright, Jest, unit testing, e2e, test automation
DevOps: Deployment, Docker, Kubernetes, CI/CD, cloud platforms
Documentation: README, changelog, API documentation, guides
Code Quality: Code review, linting, refactoring, best practices
Design: UI/UX, design systems, accessibility, visual design
Productivity: Workflow automation, git, CLI tools, scripts
Data: Analysis, visualization, database, queries

## Tips for Effective Skill Searches

Use specific, domain-focused keywords: "react testing" is better than just "testing"

Try alternative terms: If one search doesn't work, try related keywords

- "deploy" vs "deployment" vs "ci-cd"
- "style" vs "design" vs "css"
- "test" vs "testing" vs "qa"

Check multiple sources: Popular organizations publish many skills

- Anthropic's skill collection covers broad use cases
- Organization-specific skills (Vercel, Microsoft, etc.) provide deep expertise

Search skills.sh directly when unsure: The registry has filtering and detailed descriptions

## When No Matching Skill Exists

If you can't find a relevant skill:

1. Acknowledge the gap: "I searched for skills related to X but didn't find any matches"
2. Offer direct assistance: "I can still help you with this task directly using general capabilities"
3. Suggest creating a custom skill: Users can create domain-specific skills with their own instructions and workflows

Example response:

```
I searched for skills related to "custom-orm-setup" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill with
detailed instructions and bundled resources.
```

## Sharing Skills

Once you've found a useful skill:

1. Share the direct skills.sh link
2. Explain the skill's purpose and capabilities
3. Let the user decide if they want to install it
4. The skill installation process depends on their development environment setup
