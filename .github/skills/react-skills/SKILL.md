---
name: react-skills
description: Build clean, accessible React components with TypeScript and Fluent UI. Use when creating new React components, converting designs to code, building reusable UI patterns, optimizing component performance, implementing accessibility guidelines, or structuring React projects. Supports component scaffolding, hook creation, data separation, and testing workflows.
---

# React Component Development

Create production-quality React components following Microsoft best practices, accessibility standards, and industry patterns.

## When to Use This Skill

Generate React components when you need to:

- Build new UI components from scratch
- Convert design mockups or prototypes to React code
- Create reusable UI patterns for projects
- Optimize existing components for performance
- Implement accessibility features (WCAG 2.2 compliance)
- Structure project layout with hooks, data layers, and component separation
- Set up TypeScript interfaces and prop validation
- Create template scaffolds for consistent component development

## Prerequisites

Ensure your project has:

- Node.js and npm installed
- React 18+ (16.13+ minimum)
- TypeScript configured with strict mode enabled
- Either Fluent UI or preferred component library already installed
- ESLint configured for React and TypeScript
- Tailwind CSS configured (optional but recommended for styling)

## Architectural Rules

Follow these guidelines for clean, maintainable components:

### Component Structure

- Break designs into independent, single-responsibility components
- Avoid large monolithic files; aim for focused, testable components
- Place each component in its own file under src/components/

### Type Safety

- Every component must export a Readonly TypeScript interface for props named ComponentNameProps
- Use strict null checking and non-null assertions sparingly
- Define component return type explicitly as React.ReactElement or JSX.Element

### Logic and Data Separation

- Move event handlers and business logic into custom hooks in src/hooks/
- Create hooks for state management, side effects, and reusable logic
- Place all static text, image URLs, lists, and mock data in src/data/mockData.ts
- Keep components pure; avoid modifying props or external state

### Styling Approach

- Use Fluent UI components for consistent, accessible styling when available
- Map project design tokens to Tailwind CSS classes for custom styling
- Extract color values and spacing from a design system file
- Use theme-mapped Tailwind classes instead of arbitrary hex values
- For Fluent UI imports, use path-based imports to reduce bundle size:
  import { Button } from '@fluentui/react/lib/Button' instead of import { Button } from '@fluentui/react'

### Performance Optimization

- Use React.memo for function components to prevent unnecessary re-renders
- Memoize callbacks with useCallback when passed to child components
- Optimize expensive computations with useMemo
- Only call ReactDOM.render when bound properties or framework aspects change
- Use PureComponent for class components or React.memo for function components

### Accessibility (WCAG 2.2 Level AA)

- Provide keyboard navigation alternatives to mouse/touch events
- Set proper ARIA attributes for screen readers
- Ensure sufficient color contrast (4.5:1 for normal text, 3:1 for large text)
- Implement visible focus indicators on all interactive elements
- Avoid keyboard traps; ensure logical tab order
- Use semantic HTML elements and Fluent UI accessible components
- Provide alt text for images, hide decorative images with aria-hidden
- Test with keyboard-only navigation and screen readers

## Step-by-Step Workflow

1. Environment Setup
   - Verify node_modules exists; run npm install if needed
   - Check TypeScript configuration (tsconfig.json) targets es2015 or higher
   - Confirm Fluent UI and styling libraries are installed

2. Create Data Layer
   - Build src/data/mockData.ts with static content referenced by the component
   - Export constants, arrays, and configuration as named exports
   - Use meaningful names; avoid magic strings

3. Define Component Interface
   - Create a Readonly TypeScript interface named ComponentNameProps
   - Define all props with explicit types (avoid any)
   - Mark optional props with ? and provide JSDoc comments
   - Include event handler prop types (e.g., onClick: () => void)

4. Build Component
   - Start with a functional component using const syntax
   - Accept props destructured and typed with ComponentNameProps
   - Use Fluent UI components from path-based imports for UI elements
   - Implement any hooks (useState, useCallback, useMemo) needed for interactivity
   - Return JSX with semantic HTML and accessible patterns
   - Export component as default export

5. Implement Custom Hooks (if needed)
   - Create src/hooks/useComponentLogic.ts for reusable state and effects
   - Use custom hooks for form handling, API calls, or complex state
   - Keep hooks pure and testable

6. Wire Into Application
   - Import component into App.tsx or parent container
   - Pass required props from parent state or context
   - Map component to route or layout section

7. Quality Checks
   - Run npm run lint to check for TypeScript and ESLint issues
   - Verify component with npm run dev in local dev environment
   - Test keyboard navigation, screen reader compatibility, focus management
   - Check contrast ratios and visual appearance
   - Validate accessibility with browser dev tools or Accessibility Insights
   - Test performance with React DevTools Profiler

8. Validate Against Checklist
   - Component exported as default with clear file naming
   - Props interface defined and properly typed
   - All interactive elements are keyboard accessible
   - Accessibility attributes (aria-\*, role, alt) are present where needed
   - Styling uses design tokens; no hardcoded hex values in component code
   - Logic separated into custom hooks
   - Static data moved to mockData.ts
   - No console errors, warnings, or linting issues

## Troubleshooting

| Issue                        | Solution                                                                                     |
| ---------------------------- | -------------------------------------------------------------------------------------------- |
| TypeScript errors with props | Ensure ComponentNameProps interface is defined and props parameter is typed with it          |
| Component not rendering      | Verify component is exported as default or named export; check parent imports and props      |
| Styling not applied          | Confirm Fluent UI or Tailwind CSS packages are installed; check class names match config     |
| Accessibility issues         | Run browser accessibility inspector; verify ARIA attributes, focus, and color contrast       |
| Bundle size too large        | Use path-based imports from Fluent UI; enable tree-shaking in tsconfig.json                  |
| Unnecessary re-renders       | Add React.memo to component or use useCallback for event handlers                            |
| Focus not visible            | Check CSS includes clear :focus styles; apply outline or border-based focus indicator        |
| Screen reader not announcing | Test ARIA labels, roles, and semantic HTML; use aria-label on unlabeled interactive elements |

## References

- Microsoft Learn: Best practices for React code components
- Fluent UI React documentation and component API
- WCAG 2.2 accessibility guidelines
- React official documentation on hooks, performance, and accessibility
- TypeScript strict mode configuration guide
- Tailwind CSS configuration and theme mapping
