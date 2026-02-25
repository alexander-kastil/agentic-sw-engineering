# Constitution, Specification and Technical Plan

This module covers the three core artifacts that drive GitHub Spec Kit development: the constitution that establishes immutable project principles, the specification that defines what you need to build, and the technical plan that describes how you'll build it. These artifacts work together to provide persistent guidance that keeps AI-assisted development aligned with organizational standards and project requirements.

## Constitution: Establish project principles

The constitution file captures non-negotiable principles, constraints, and standards that govern your project and serve as guardrails for AI-assisted development. When you generate specifications, plans, or code, GitHub Copilot references the constitution to ensure proposals comply with your standards. Use the /speckit.constitution command to create an initial constitution based on your project context, then refine it to include sections for technology standards, security requirements, performance targets, coding standards, and compliance obligations.

A well-defined constitution provides consistency enforcement across long-running projects with multiple developers, making regulatory requirements and security policies explicit and auditable. Your constitution captures institutional knowledge in a form that guides AI code generation, automating enforcement of organizational policies during development. The constitution is a living document but changes infrequently—once established, it provides stable guidance throughout feature development.

## Specification: Define what you need to build

The specification file (spec.md) is the single source of truth for what your software should do and becomes your contract with GitHub Copilot. A well-structured specification includes sections for summary, user stories, acceptance criteria, functional requirements, nonfunctional requirements, and edge cases. Use the /speckit.specify command to generate an initial specification from natural language descriptions, then refine it with /speckit.clarify to surface ambiguities and fill gaps.

Writing effective specifications is foundational to successful spec-driven development—specifications define requirements without prescribing implementations. Use specific, measurable values instead of vague terms, maintain consistent terminology throughout, cover error handling explicitly, and validate specifications against your constitution before finalizing. When specifications are detailed and unambiguous, AI code generation produces implementations that precisely match your actual needs instead of making assumptions about your requirements.

## Technical Plan: Design how you'll build it

The technical plan file (plan.md) serves as your design document, bridging the gap between high-level requirements in spec.md and concrete implementation tasks. A comprehensive technical plan contains architecture overviews, technology stack decisions with rationales, implementation sequences, explicit verification of constitution compliance, and documentation of assumptions and open questions. Use the /speckit.plan command to generate a plan based on your specification and constitution, providing architectural context about your existing technology stack and infrastructure.

Plans require critical review before implementation—verify coverage of specification requirements, check alignment with technical standards, and validate constitution adherence to prevent costly conflicts discovered later. Address ambiguities by asking follow-up questions to GitHub Copilot, validate technical feasibility with team members, and consider nonfunctional requirements like performance, security, scalability, and accessibility. The validated plan becomes your reference throughout implementation as developers consult it regularly to ensure code aligns with documented architecture.

## Key Topics covered in this module

- Constitution creation and refinement using /speckit.constitution
- Security requirements, technology standards, and compliance governance
- Specification structure and best practices for enterprise scenarios
- Gap analysis with /speckit.clarify for complete requirements
- Technical planning with separation of concerns between spec and plan
- Architecture documentation and decision rationale
- Constitution verification and compliance checking in plans
