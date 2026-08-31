---
name: sequential-navigation
description: Transform large markdown documents into organized, guided navigation workflows. Breaks monolithic files into sequential sections with bidirectional navigation (back to hub, next section). Creates seamless user experiences for tutorials, exercises, step-by-step guides, and learning materials across multiple files.
---

## Overview

The sequential-navigation skill provides a complete framework for organizing and navigating multi-file markdown documentation. It enables you to:

- **Break down** large documents into manageable, sequential sections
- **Add intelligent navigation** with three link types:
  - ↑ **Internal**: Jump to top of current file
  - ← **Contextual**: Return to main documentation hub
  - → **Sequential**: Move to next file in workflow
- **Create guided workflows** where users progress through documentation in a logical order

## When to Use This Skill

Use sequential-navigation when you have:

- **Monolithic documentation** that would benefit from being split into multiple files
- **Tutorial or exercise guides** with ordered steps across multiple documents
- **Workflow documentation** where users need to progress through sections sequentially
- **Learning materials** where navigation helps maintain orientation and context
- **Step-by-step procedures** that span multiple markdown files
- **Documentation sets** that require easy jumping between related topics

## How This Skill Works

### The Three Navigation Link Types

#### 1. Contextual Navigation (← Back to Hub)

Appears at the top and throughout each file, provides a permanent link back to the central documentation hub.

```markdown
[← Back to Exercise Instructions](../readme.md#exercise-instructions)
```

#### 2. Internal Navigation (↑ Back to top)

Allows users to instantly return to the file's beginning from the navigation bar.

```markdown
[↑ Back to top](#main-heading)
```

#### 3. Sequential Navigation (→ Next Section)

Guides users to the next file in the workflow, displayed in the navigation bar.

```markdown
[→ Next: Section Name](next-file.md)
```

---

## Step-by-Step Implementation

### Phase 1: Analyze Your Large Document

1. **Read through** the entire document and identify all major sections (marked with `##` headings)
2. **List sections** in logical order
3. **Sequence them** - determine the order users should read/process them
4. **Identify dependencies** - which sections require knowledge from previous ones?
5. **Group content** - decide which subsections should stay together vs. split

### Phase 2: Create Your File Structure

1. **Preserve a central hub** - usually the main README with overview and links
2. **Create a subdirectory** for instruction files (e.g., `/instructions`)
3. **Name files** sequentially or descriptively:
   - Sequential: `01-setup.md`, `02-config.md`, `03-implement.md`
   - Descriptive: `setup.md`, `configuration.md`, `implementation.md`

### Phase 3: Extract Content into Files

1. **Copy content** from the original document into individual files
2. **Preserve headings** as the main file heading (`#`)
3. **Keep subsections** as secondary headings (`##`, `###`)
4. **Remove extracted content** from the hub document and replace with links

### Phase 4: Reorganize the Hub Document

Update your main documentation file to:

1. **Keep the overview/introduction** explaining the documentation's purpose
2. **Add a links section** pointing to each instruction file
3. **Organize links** under category headings that match your workflow
4. **Use descriptive text** explaining what each file contains

Example:

```markdown
# Main Documentation

Brief overview of the documentation.

## Getting Started

- [Set up the project](instructions/setup.md)
- [Configure your environment](instructions/configuration.md)

## Implementation

- [Build the feature](instructions/implementation.md)
- [Test your work](instructions/testing.md)
```

### Phase 5: Add Navigation Links

Now add the three navigation types to each file:

**At the top of each file (after title):**

```markdown
# File Title

[← Back to Exercise Instructions](../readme.md#exercise-instructions)

**Table of Contents:**
- [Section 1](#section-1)
- [Section 2](#section-2)

---
```

**At the bottom of each file (except the last), use a full-width navigation bar:**

```html
---

<div style="display: flex; justify-content: space-between; padding: 1rem 0; border-top: 1px solid #ccc; border-bottom: 1px solid #ccc;">
  <a href="../readme.md#exercise-instructions">← Back to Exercise Instructions</a>
  <a href="#file-title">↑ Back to top</a>
  <a href="next-file.md">→ Next: Next File Title</a>
</div>
```

**At the bottom of the last file, use:**

```html
---

<div style="display: flex; justify-content: space-between; padding: 1rem 0; border-top: 1px solid #ccc; border-bottom: 1px solid #ccc;">
  <a href="../readme.md#exercise-instructions">← Back to Exercise Instructions</a>
  <a href="#file-title">↑ Back to top</a>
</div>
```

---

## Complete Example

Here's a complete before/after example showing how to transform a large document:

### Directory Structure

```
readme.md (main hub - 100 lines total)
├── instructions/
│   ├── setup.md (30 lines)
│   ├── configuration.md (35 lines)
│   ├── implementation.md (40 lines)
│   └── testing.md (25 lines)
```

### Sample File: instructions/setup.md

```markdown
# Set up the project

[← Back to Exercise Instructions](../readme.md#exercise-instructions)

**Table of Contents:**
- [Installation](#installation)
- [Verification](#verification)

---

## Installation

Follow these steps to install the project...

## Verification

Verify the installation is correct...

---

<div style="display: flex; justify-content: space-between; padding: 1rem 0; border-top: 1px solid #ccc; border-bottom: 1px solid #ccc;">
  <a href="../readme.md#exercise-instructions">← Back to Exercise Instructions</a>
  <a href="#set-up-the-project">↑ Back to top</a>
  <a href="configuration.md">→ Next: Configure your environment</a>
</div>
```

### Sample File: instructions/configuration.md (last file)

```markdown
# Configure your environment

[← Back to Exercise Instructions](../readme.md#exercise-instructions)

**Table of Contents:**
- [Settings](#settings)
- [Verification](#verification)

---

## Settings

Configure these settings...

## Verification

Verify your configuration...

---

<div style="display: flex; justify-content: space-between; padding: 1rem 0; border-top: 1px solid #ccc; border-bottom: 1px solid #ccc;">
  <a href="../readme.md#exercise-instructions">← Back to Exercise Instructions</a>
  <a href="#configure-your-environment">↑ Back to top</a>
</div>
```

## Best Practices

1. **Consistent Link Format**: Use the same arrow symbols and formatting throughout
   - ↑ for internal navigation
   - ← for contextual navigation to hub
   - → for sequential next-section navigation

2. **Relative Paths**: Use relative paths (e.g., `../readme.md`) for cross-file navigation
   - More portable and works with local file viewing
   - Easier to reorganize folder structure

3. **Anchor Naming**: Keep heading text simple and anchor-friendly
   - Use lowercase letters and hyphens
   - Avoid special characters in headings
   - Make anchors human-readable

4. **Order Matters**: Ensure the sequential flow matches logical learning/usage progression
   - Start with foundational concepts
   - Progress to advanced topics
   - End with cleanup or next steps

5. **Main Hub Identification**: Clearly identify the central documentation hub with an `#exercise-instructions` or similar anchor for consistent linking back

6. **Test Links**: Verify all links work correctly
   - Test relative path navig
   - Always use the same arrow symbols (↑, ←, →)
   - Keep link styling consistent across all files
   - Use clear, descriptive link text

7. **Relative Paths**
   - Use `../` notation to navigate between directories
   - More portable than absolute paths
   - Works with local file browsing and GitHub

8. **Anchor Naming**
   - Convert heading to lowercase with hyphens: `# Create Specifications` → `#create-specifications`
   - Avoid special characters in headings
   - Keep anchors simple and readable

9. **Logical Flow**
   - Start with foundational concepts
   - Progress to intermediate topics
   - End with advanced or cleanup steps
   - Ensure sequential order matches user needs

10. **Hub Identification**
    - Use a consistent anchor name for your hub (e.g., `#exercise-instructions`)
    - Clearly mark the central location
    - Every file should link back to it

11. **Testing**
    - Test all relative path links
    - Verify anchors match actual headings exactly
    - Check that the last file returns properly to hub
    - Validate in both local editor and GitHub

---

## Common Use Cases

### Tutorial Series

Multiple lesson files guiding users through a complete course with sequential navigation between lessons.

### Step-by-Step Guides

Sequential procedure files where users work through tasks in order, with clear navigation between steps.

### Exercise Workflows

Training exercises with ordered phases (setup → specification → planning → implementation → testing).

### Contributing Guidelines

Onboarding documentation for new contributors with navigation through setup, coding standards, and submission processes.

### Learning Paths

Organized educational content where pre-requisite knowledge flows into advanced topics.

### Product Documentation

Feature documentation organized by complexity with clear navigation between related features.
