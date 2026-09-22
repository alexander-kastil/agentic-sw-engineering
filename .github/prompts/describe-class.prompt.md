---
name: describe-class
description: Describe when to use this prompt
model: Claude Haiku 4.5 (copilot)
---

# Prompt: Generate Engaging Class Description

## Task

- Generate an engaging, narrative-driven class description from the modules listed in `demos/readme.md`. 
- This description should replace any existing description in the readme and be placed immediately below the class title.
- Act as an experienced IT instructor who enjoys teaching and write like a human.
- Audience: Software Engineers, Solution Architects, and Power Platform Makers interested in learning about low-code agents using Copilot Studio.

## Instructions

### 1. Output Structure
Generate a narrative-driven description with:
- **Opening Paragraph**: Compelling introduction establishing the course purpose (e.g., "Embark on a four-day, hands-on journey...")
- **Module Paragraphs**: One engaging paragraph per module (7 total), weaving all key buzzwords and technical concepts into flowing prose
- **Closing Paragraph**: Conclusion reinforcing value and outcomes
- **Restrictions**: No bullet points, no lists, no use of "—" instead of commas.

### 2. Writing Guidelines
For each module paragraph:
- Start with a transitional phrase connecting to the learning journey (e.g., "Your learning adventure begins...", "The journey continues as you...", "A major focus is placed on...")
- Convert all module topics into flowing narrative—explain the *why* and *how*, not just list items
- Include all technical concepts and buzzwords, but write them naturally into sentences
- Use active voice and metaphors (e.g., "journey," "adventure," "progression")
- Balance accessibility for non-technical makers with technical depth for engineers and architects
- Show how each module builds on previous learning
- **Keep each module paragraph to a maximum of 4 sentences (goal: 3 sentences)**

Avoid: bullet lists, oversimplification, listing-style formats. Instead, weave topics seamlessly into compelling prose for your mixed audience (Power Platform Makers, Software Engineers, Solution Architects).

### 3. Output Placement
Replace the existing class description in `demos/readme.md` by placing this narrative:
- Immediately after the main title heading (`# Designing, Implementing & Maintaining Low-Code Agents using Copilot Studio`)
- Above the `## Duration` section
- Followed by a blank line before the next section
- Do not modify any other content in the file