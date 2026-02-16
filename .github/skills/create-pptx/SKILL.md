---
name: create-pptx
description: Create, edit, analyze, and validate PowerPoint presentations (PPTX files). Use when asked to build presentations from scratch, modify existing templates, visualize presentation content, convert slides to images, or verify design quality. Supports text extraction, slide thumbnail generation, design validation, and QA workflows. Requires python-pptx, markitdown, pptxgenjs, LibreOffice, and Poppler.
---

# PowerPoint Presentation Skill

Create professional PowerPoint presentations with design best practices, content validation, and quality assurance workflows.

## When to Use This Skill

Use this skill when you need to:

- Create presentations from scratch without a template using PptxGenJS
- Edit or modify existing presentation templates
- Extract and analyze presentation content as markdown
- Generate visual thumbnails of slides
- Convert presentations to images for visual inspection
- Validate presentation quality (content, layout, contrast, typography)
- Unpack and manipulate presentation XML structure
- Verify design compliance before final delivery

Triggers on requests like: create presentation, build PowerPoint, edit PPTX, generate slides, presentation QA, validate slides, analyze presentation structure.

## Prerequisites and Setup

### Required Dependencies

Install all required tools:

```powershell
# Python libraries
pip install "markitdown[pptx]"
pip install Pillow

# Node.js global package
npm install -g pptxgenjs

# LibreOffice (Windows - if not installed)
winget install LibreOffice

# Poppler (PDF conversion utilities)
# Windows: via Chocolatey or direct download from https://github.com/oschwartz10612/poppler-windows/releases/
choco install poppler
# Or manually add poppler to system PATH
```

### Verification

Verify installation:

```powershell
python -m pip list | findstr /I "pptx pillow markitdown"
npm list -g pptxgenjs
soffice --version  # LibreOffice
pdfimages -v       # Or pdftoppm -v (Poppler utilities)
```

## Workflow: Create Presentation from Scratch

Use PptxGenJS when creating presentations without a template.

### Step 1: Plan Content and Design

Before coding, define:

- Color palette (pick 1-2 supporting tones plus 1 accent; avoid generic blue)
- Typography (header font + body font pair)
- Layout pattern (two-column, icon+text rows, grids, or half-bleed images)
- Visual elements for each slide (images, icons, charts, shapes; avoid text-only)

### Step 2: Create Presentation Structure

```powershell
npm install pptxgenjs
# Or in a Node.js/JavaScript project: npm install pptxgenjs
```

### Step 3: Build Slides Programmatically

Use PptxGenJS to add slides with consistent styling:

```javascript
const PptxGenJS = require("pptxgenjs");
const prs = new PptxGenJS();

prs.defineLayout("TITLE_SLIDE", {
  name: "Title Slide",
  width: 10,
  height: 7.5
});

const slide = prs.addSlide("TITLE_SLIDE");
slide.background = { color: "1E2761" };
slide.addText("Your Title", {
  x: 0.5,
  y: 2.5,
  w: 9,
  h: 2,
  fontSize: 44,
  bold: true,
  color: "FFFFFF",
  fontFace: "Georgia",
  align: "left"
});

prs.writeFile("output.pptx");
```

### Step 4: Apply Design Best Practices

| Element         | Rule                                                                    |
| --------------- | ----------------------------------------------------------------------- |
| Color dominance | 60-70% primary color, 1-2 supporting, 1 accent                          |
| Typography      | 36-44pt (titles), 20-24pt (headers), 14-16pt (body), 10-12pt (captions) |
| Spacing         | 0.5" minimum margins, 0.3-0.5" between blocks                           |
| Layouts         | Vary layouts across slides (columns, cards, callouts)                   |
| Visuals         | Every slide must have an image, icon, chart, or shape element           |
| Text alignment  | Left-align body paragraphs and lists; center only titles                |
| Contrast        | Ensure 4.5:1 contrast for text, 3:1 for focus indicators                |

## Workflow: Edit Existing Template

Use when a template or reference presentation exists.

### Step 1: Analyze Template

```powershell
# Generate thumbnail view of template
python scripts/thumbnail.py template.pptx

# Extract text with formatting context
python -m markitdown template.pptx > content.md
```

### Step 2: Unpack and Modify

```powershell
# Unpack presentation for XML-level editing
python scripts/office/unpack.py template.pptx unpacked/

# Edit slide files (e.g., unpacked/ppt/slides/slide1.xml)
# Then repack
python scripts/office/pack.py unpacked/ output.pptx
```

### Step 3: Validate Changes

Extract and verify content:

```powershell
python -m markitdown output.pptx > output.md
# Check for placeholder text or errors
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder"
```

## Workflow: Content Extraction and Analysis

Extract presentation content for review or repurposing.

```powershell
# Extract all text as markdown (fastest for review)
python -m markitdown presentation.pptx

# Generate visual thumbnail grid of all slides
python scripts/thumbnail.py presentation.pptx

# Extract raw XML for advanced analysis
python scripts/office/unpack.py presentation.pptx unpacked/
```

## Workflow: Quality Assurance (Required Before Submission)

**Critical: Assume there are problems. Your first render is almost never correct.**

### Content QA

```powershell
# Extract presentation text
python -m markitdown output.pptx

# Check for placeholder text or missing content
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

Fix any issues found before proceeding to visual QA.

### Visual QA

Convert slides to images for inspection:

```powershell
soffice --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
# Creates slide-01.jpg, slide-02.jpg, etc.
```

### Inspection Checklist

Review slide images for:

- Overlapping elements (text through shapes, lines through words)
- Text overflow or cut-off at edges
- Insufficient spacing (< 0.3" gaps between elements; < 0.5" from edges)
- Uneven gaps (large empty areas near cramped sections)
- Low contrast text (e.g., light gray on cream background)
- Low contrast icons (dark icons on dark backgrounds without contrasting circle)
- Decorative lines misaligned (positioned for single-line text but title wraps two lines)
- Elements not consistently aligned
- Placeholder content remaining

### Verification Loop

1. Generate slides → Convert to images → Inspect visually
2. List all issues found (even minor ones)
3. Fix issues in code
4. Re-render affected slides only: `pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed`
5. Repeat until full inspection reveals no new issues

Do not declare success until completing at least one full fix-and-verify cycle.

## Color Palettes (Reference)

Choose a palette specific to your topic:

| Palette            | Primary            | Secondary           | Accent            |
| ------------------ | ------------------ | ------------------- | ----------------- |
| Midnight Executive | 1E2761 (navy)      | CADCFC (ice blue)   | FFFFFF (white)    |
| Forest & Moss      | 2C5F2D (forest)    | 97BC62 (moss)       | F5F5F5 (cream)    |
| Coral Energy       | F96167 (coral)     | F9E795 (gold)       | 2F3C7E (navy)     |
| Ocean Gradient     | 065A82 (deep blue) | 1C7293 (teal)       | 21295C (midnight) |
| Berry & Cream      | 6D2E46 (berry)     | A26769 (dusty rose) | ECE2D0 (cream)    |
| Teal Trust         | 028090 (teal)      | 00A896 (seafoam)    | 02C39A (mint)     |

## Common Mistakes to Avoid

- Do not use the same layout across slides
- Do not center body text; left-align paragraphs and lists
- Do not skimp on size contrast; titles need 36pt+ to stand out from 14-16pt body text
- Do not default to blue; pick colors reflecting the specific topic
- Do not create text-only slides; add images, icons, charts, or visual elements
- Do not use accent lines under titles (hallmark of AI-generated slides)
- Do not use low-contrast colors for text or icons
- Do not forget text box padding when aligning shapes with text

## Troubleshooting

| Issue                                  | Solution                                                                                                         |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| LibreOffice not found                  | Install via `winget install LibreOffice` and ensure it is in system PATH                                         |
| Poppler utilities missing              | Download from https://github.com/oschwartz10612/poppler-windows/releases/ or install via `choco install poppler` |
| PDF conversion fails                   | Verify LibreOffice with `soffice --version` and restart terminal session after install                           |
| Text extraction shows placeholders     | This is expected; manually edit extracted content and regenerate slides                                          |
| Slide images show overlapping elements | Reduce font sizes, increase box spacing, or use multi-column layouts                                             |
| PptxGenJS not recognized as command    | Install globally: `npm install -g pptxgenjs` and ensure npm is in PATH                                           |

## References

- [PptxGenJS Documentation](https://gitbrent.github.io/PptxGenJS/)
- [markitdown Documentation](https://microsoft.github.io/markitdown/)
- [LibreOffice Headless Commands](https://help.libreoffice.org/latest/en-US/text/shared/guide/scripting.html)
- [Open XML SDK - PowerPoint](https://learn.microsoft.com/office/open-xml/presentation/)
- [PowerPoint Design Best Practices](https://support.microsoft.com/office/design-a-professional-presentation-in-powerpoint-18f83e4f-2a1b-4fcf-b46d-ad87fac8fbb6)
