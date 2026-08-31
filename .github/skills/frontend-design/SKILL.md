---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with exceptional aesthetic direction and full accessibility compliance. Use when building components, pages, or applications with clear visual identity. Covers design thinking, typography, color systems, animation, responsive layouts, and WCAG 2.2 accessibility standards. Supports HTML/CSS, React, Vue, Angular, and modern JavaScript frameworks. Keywords: design frontend, build UI, create component, style page, accessible design, design system.
---

# Frontend Design

Guide for creating distinctive, accessibility-compliant frontend interfaces that avoid generic aesthetics while meeting production-grade standards.

Use this skill when:

- Building new components, pages, or full applications
- Designing visual interfaces with clear aesthetic vision
- Implementing design systems with accessible components
- Styling for multiple themes or branding needs
- Creating responsive layouts for modern web standards

## Design Thinking

Before coding, establish clear context and aesthetic direction:

Define purpose: What problem does this interface solve? Who uses it? What's the user goal?

Choose aesthetic tone intentionally. Pick a strong direction:

- Minimalist and refined
- Brutally bold and maximalist
- Retro-futuristic
- Organic and natural
- Luxury and elevated
- Playful and whimsical
- Editorial and magazine-style
- Brutalist and raw
- Art deco and geometric
- Soft and pastel
- Industrial and utilitarian

Document constraints: Framework requirements, performance budgets, accessibility standards (WCAG 2.2 Level AA minimum), browser support, device targets.

Identify differentiation: What makes this memorable? What's the one thing users will remember about this design?

Execute with intention and precision. Bold, cohesive designs are more effective than timid, scattered choices.

## Frontend Aesthetics Guidelines

### Typography

Choose fonts that elevate and distinguish the interface:

- Use distinctive display fonts for headings, not generic choices like Arial, Roboto, or Inter
- Pair a bold, characterful display font with a refined, readable body font
- Ensure font choices align with your aesthetic direction
- Verify sufficient contrast ratio (4.5:1 minimum for body text, 3:1 for large text per WCAG 2.2)

### Color and Theme

Establish a cohesive color system:

- Define CSS variables for all colors to ensure consistency
- Use a dominant color with sharp accent colors; avoid timid, evenly-distributed palettes
- Create separate color systems for light and dark themes
- Test all interactive states (default, hover, active, focus, visited) for sufficient contrast
- In forced-colors mode, use system color keywords (ButtonText, ButtonBorder, CanvasText, etc.)

### Motion and Animation

Use animation purposefully:

- Prioritize CSS-only solutions for standard HTML/CSS interfaces
- In React, leverage animation libraries for sophisticated interactions
- Focus on high-impact moments: a well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions
- Add hover states and scroll-triggering animations that surprise without disorienting
- Ensure animations don't cause motion sickness (avoid flashing, rapid transitions)

### Spatial Composition

Create compelling layouts:

- Use unexpected layouts with asymmetry, overlap, and diagonal flow
- Break grid patterns with intentional off-axis elements
- Balance generous negative space with controlled density
- Implement responsive stacking that maintains visual hierarchy at all breakpoints
- At narrow widths (320px viewport), ensure two-directional scrolling is not required for any text or controls

### Backgrounds and Visual Details

Add depth and atmosphere:

- Move beyond solid colors with contextual visual effects and textures
- Use gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, or grain overlays
- Match all decorative elements to your established aesthetic direction
- In forced-colors mode, use borders instead of box-shadows (which are suppressed)

### Accessibility Requirements

Integrate accessibility from the start, not as an afterthought:

- Use semantic HTML elements (header, nav, main, footer, section, article)
- Ensure all interactive elements are keyboard operable with visible focus indicators
- Maintain logical tab order following reading order
- Provide visible labels for all form controls
- Use ARIA only when native HTML semantics don't work
- Ensure color is never the only cue for information (error, success, required state)
- Test at minimum 320px viewport width with no horizontal scrolling for normal text
- Support high contrast and forced colors mode with media queries

## Implementation Patterns

### HTML/CSS Approach

Build semantic, accessible markup:

- Use native elements: button, input, select, textarea, a (links), nav, main
- Add appropriate ARIA only when necessary
- Define CSS custom properties for colors, spacing, typography
- Test in multiple browsers and on real devices

### React/Vue/Angular Approach

Leverage component libraries when available:

- Use project-approved UI libraries to ensure consistency and accessibility
- Create reusable, self-contained components with clear props
- Handle focus management in interactive patterns (modals, menus, tabs)
- Test keyboard navigation and assistive technology

## Avoiding Generic AI Aesthetics

Never rely on overused, cookie-cutter patterns:

- Skip generic font families like Inter, Roboto, Arial, system fonts
- Avoid cliched color schemes (especially purple gradients on white)
- Break away from predictable layouts and standard component patterns
- Make unexpected choices that feel genuinely designed for context

Each design should have distinct character. Vary between projects: alternate light and dark, switch fonts and palettes, choose different aesthetic directions. Show what can be created when thinking outside the box and committing fully to a distinctive vision.

## Final Verification

Before delivery, verify:

- Clear aesthetic direction executed with precision
- Strong typography pairings with appropriate contrast
- Cohesive color system with CSS variables
- Responsive layout that works at 320px viewport
- All interactive elements keyboard operable with visible focus
- Color never the only cue for state or meaning
- Forced-colors mode compatibility
- Semantic HTML with appropriate ARIA when needed
- Production-grade code quality and performance
