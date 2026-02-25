---
name: create-docx
description: Create, edit, analyze, and validate Word documents (.docx files) programmatically. Use when generating reports, creating templates, automating document generation, editing existing documents with tracked changes, or converting documents to other formats. Supports JavaScript (docx-js) for creation and XML editing for fine-grained control. Keywords: create docx, generate word document, edit docx, document automation, word template, tracked changes, docx conversion.
---

# DOCX Creation and Editing

Comprehensive guide for creating, editing, analyzing, and converting Word documents (.docx files) using JavaScript and XML manipulation.

Use this skill when:

- Generating reports or documents from data
- Creating Word templates programmatically
- Automating document workflows
- Editing existing documents with tracked changes or comments
- Converting documents between formats
- Extracting text and metadata from DOCX files
- Adding tables, images, headers/footers, or complex formatting

## Quick Start

### Create a Simple Document

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageOrientation } = require('docx');
const fs = require('fs');

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: {
          width: 12240,   // 8.5 inches (US Letter)
          height: 15840   // 11 inches
        },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins
      }
    },
    children: [
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Document Title")]
      }),
      new Paragraph({
        children: [new TextRun("This is the document body.")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("document.docx", buffer);
  console.log("Document created!");
});
```

### Edit an Existing Document

```bash
# 1. Unpack the document
python scripts/office/unpack.py input.docx unpacked/

# 2. Edit XML files in unpacked/word/

# 3. Repack the document
python scripts/office/pack.py unpacked/ output.docx --original input.docx
```

## Creating New Documents

Generate .docx files with docx-js JavaScript library.

Installation: `npm install -g docx`

### Critical Page Size Rules

docx-js defaults to A4. Always set page size explicitly for consistent results:

```javascript
// US Letter (most common)
size: {
  width: 12240,    // 8.5 inches in DXA units
  height: 15840,   // 11 inches
  margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins
}

// A4 (alternative)
size: {
  width: 11906,
  height: 16838,
  margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
}

// Landscape: Pass portrait dimensions, set orientation, docx-js handles swap
size: {
  width: 12240,    // SHORT edge
  height: 15840,   // LONG edge
  orientation: PageOrientation.LANDSCAPE  // docx-js swaps internally
}
```

Unit conversion: 1440 DXA = 1 inch

### Basic Structure

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // Add paragraphs, tables, images, etc.
    ]
  }]
});
```

### Styles (Override Built-in Headings)

Use Arial as the default font. Override heading styles with exact IDs:

```javascript
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Arial", size: 24 } } // 12pt
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: {
          spacing: { before: 240, after: 240 },
          outlineLevel: 0  // REQUIRED for TOC
        }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: {
          spacing: { before: 180, after: 180 },
          outlineLevel: 1  // REQUIRED for TOC
        }
      }
    ]
  },
  sections: [{
    children: [
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Title")]
      })
    ]
  }]
});
```

### Paragraphs and Text

Never use `\n` for line breaks. Use separate Paragraph elements:

```javascript
// ❌ WRONG
new Paragraph({ children: [new TextRun("Line 1\nLine 2")] })

// ✅ CORRECT
new Paragraph({ children: [new TextRun("Line 1")] }),
new Paragraph({ children: [new TextRun("Line 2")] })
```

Paragraph options:

```javascript
new Paragraph({
  heading: HeadingLevel.HEADING_1,
  alignment: AlignmentType.CENTER,
  spacing: { before: 240, after: 120, line: 360 }, // in DXA
  indent: { left: 720, right: 720, firstLine: 360 },
  children: [new TextRun({
    text: "Text content",
    bold: true,
    italics: true,
    size: 24, // 12pt
    font: "Arial",
    color: "0066CC"
  })]
})
```

### Lists

Never use unicode bullet characters (`•`, `\u2022`). Use LevelFormat.BULLET with numbering config:

```javascript
const { Document, Paragraph, TextRun, NumberFormat, LevelFormat, AlignmentType } = require('docx');

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: {
                indent: { left: 720, hanging: 360 }
              }
            }
          }
        ]
      },
      {
        reference: "numbers",
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "%1.",
            alignment: AlignmentType.LEFT,
            style: {
              paragraph: {
                indent: { left: 720, hanging: 360 }
              }
            }
          }
        ]
      }
    ]
  },
  sections: [{
    children: [
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item 1")]
      }),
      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item 2")]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Numbered item 1")]
      })
    ]
  }]
});
```

Important: Each numbering reference tracks independently. Same reference continues (1,2,3 then 4,5,6). Different reference restarts (1,2,3 then 1,2,3).

### Tables

CRITICAL: Tables require dual widths - set both `columnWidths` on the table AND `width` on each cell:

```javascript
const { Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, VerticalAlign } = require('docx');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // Content width: page width - margins
  columnWidths: [4680, 4680], // Must sum to table width
  rows: [
    new TableRow({
      children: [
        new TableCell({
          width: { size: 4680, type: WidthType.DXA }, // Match columnWidth
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // Use CLEAR not SOLID
          borders,
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // Cell padding
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ children: [new TextRun("Header 1")] })]
        }),
        new TableCell({
          width: { size: 4680, type: WidthType.DXA },
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          borders,
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ children: [new TextRun("Header 2")] })]
        })
      ]
    })
  ]
})
```

Width calculation rules:

- Always use `WidthType.DXA` (never PERCENTAGE - breaks in Google Docs)
- Table width must equal sum of columnWidths
- Cell width must match corresponding columnWidth
- Cell margins are internal padding (reduce content area, not add to width)
- Full-width table: use content width = page width minus left/right margins

Example: US Letter with 1" margins

```
Page width: 12240 DXA
Left margin: 1440 DXA
Right margin: 1440 DXA
Content width: 12240 - 1440 - 1440 = 9360 DXA
```

### Images

CRITICAL: ImageRun requires `type` parameter. All altText properties are required:

```javascript
const { ImageRun } = require('docx');
const fs = require('fs');

new Paragraph({
  children: [new ImageRun({
    type: "png", // REQUIRED: png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 }, // pixels
    altText: {
      title: "Image Title",
      description: "Image description",
      name: "image-name"
    }
  })]
})
```

### Page Breaks

PageBreak MUST be inside a Paragraph (standalone creates invalid XML):

```javascript
const { PageBreak } = require('docx');

// ✅ CORRECT
new Paragraph({ children: [new PageBreak()] })

// Alternative approach
new Paragraph({
  pageBreakBefore: true,
  children: [new TextRun("First line of new page")]
})
```

### Headers and Footers

```javascript
const { Header, Footer, PageNumber } = require('docx');

sections: [{
  properties: {
    page: {
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
    }
  },
  headers: {
    default: new Header({
      children: [
        new Paragraph({
          children: [new TextRun("Company Name")]
        })
      ]
    })
  },
  footers: {
    default: new Footer({
      children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun("Page "),
            new TextRun({ children: [PageNumber.CURRENT] })
          ]
        })
      ]
    })
  },
  children: [/* content */]
}]
```

### Table of Contents

CRITICAL: Headings must use HeadingLevel ONLY - no custom styles:

```javascript
const { TableOfContents, HeadingLevel } = require('docx');

new TableOfContents("Table of Contents", {
  hyperlink: true,
  headingStyleRange: "1-3"  // Include H1, H2, H3
})
```

Then use HeadingLevel in paragraphs:

```javascript
new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun("Section")]
})
```

### Validation

After creating the document, validate it:

```bash
python scripts/office/validate.py doc.docx
```

If validation fails, unpack, fix the XML, and repack.

## Editing Existing Documents

Three-step process: unpack → edit XML → pack

### Step 1: Unpack

```bash
python scripts/office/unpack.py input.docx unpacked/
```

This:

- Extracts XML files
- Pretty-prints for readability
- Merges adjacent runs
- Converts smart quotes to XML entities (`&#x201C;` etc.)

Skip run merging: `--merge-runs false`

### Step 2: Edit XML

Edit files in `unpacked/word/` directly.

Use "Claude" as the author for tracked changes, unless the user requests otherwise.

Use Edit tool for string replacement - do not write Python scripts.

Smart quotes for professional typography:

```xml
<!-- Use these entities for new content -->
<w:t>Here &#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```

Common entities:

- `&#x2018;` - ' (left single quote)
- `&#x2019;` - ' (right single quote / apostrophe)
- `&#x201C;` - " (left double quote)
- `&#x201D;` - " (right double quote)

### Tracked Changes

Track edits when modifying documents:

Insertion:

```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

Deletion:

```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

Note: Use `<w:delText>` instead of `<w:t>` inside deletions.

Deleting entire paragraphs - mark both the content AND the paragraph mark:

```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Paragraph being deleted...</w:delText></w:r>
  </w:del>
</w:p>
```

Minimal edits - only mark what changes:

```xml
<w:r><w:t>The term is </w:t></w:r>
<w:del w:id="1" w:author="Claude" w:date="...">
  <w:r><w:delText>30</w:delText></w:r>
</w:del>
<w:ins w:id="2" w:author="Claude" w:date="...">
  <w:r><w:t>60</w:t></w:r>
</w:ins>
<w:r><w:t> days.</w:t></w:r>
```

### Comments

Add comments with the comment.py script (handles boilerplate):

```bash
python scripts/comment.py unpacked/ 0 "Comment text"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0  # Reply to comment 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"
```

Then add markers to document.xml:

```xml
<!-- Comment markers are siblings of <w:r>, never inside -->
<w:commentRangeStart w:id="0"/>
<w:r><w:t>text being commented</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r>
  <w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>
  <w:commentReference w:id="0"/>
</w:r>
```

### Step 3: Pack

```bash
python scripts/office/pack.py unpacked/ output.docx --original input.docx
```

This:

- Validates XML with auto-repair
- Auto-repair fixes common issues (`durableId`, missing `xml:space="preserve"`)
- Won't fix: malformed XML, invalid nesting, missing relationships

Skip validation: `--validate false`

## XML Reference

### Schema Compliance

Element order matters. In `<w:pPr>` (paragraph properties):

```
<w:pStyle> → <w:numPr> → <w:spacing> → <w:ind> → <w:jc> → <w:rPr> (last)
```

Whitespace: Add `xml:space="preserve"` to `<w:t>` with leading/trailing spaces:

```xml
<w:t xml:space="preserve">  indented text</w:t>
```

RSIDs: Must be 8-digit hex (e.g., `00AB1234`)

### Images in XML

1. Add image to `word/media/image1.png`
2. Add relationship in `word/_rels/document.xml.rels`:

```xml
<Relationship Id="rId5" Type=".../image" Target="media/image1.png"/>
```

3. Add content type to `[Content_Types].xml`:

```xml
<Default Extension="png" ContentType="image/png"/>
```

4. Reference in document.xml:

```xml
<w:drawing>
  <wp:inline>
    <wp:extent cx="914400" cy="914400"/>  <!-- EMUs: 914400 = 1 inch -->
    <a:graphic>
      <a:graphicData uri=".../picture">
        <pic:pic>
          <pic:blipFill><a:blip r:embed="rId5"/></pic:blipFill>
        </pic:pic>
      </a:graphicData>
    </a:graphic>
  </wp:inline>
</w:drawing>
```

## Conversions

### Convert DOCX to DOCX (clean/merge)

```bash
python scripts/office/validate.py document.docx
```

### Convert DOCX to Markdown

```bash
pandoc --track-changes=all document.docx -o output.md
```

### Convert DOCX to PDF

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
```

### Convert DOCX to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### Convert .doc to .docx

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### Accept All Tracked Changes

```bash
python scripts/accept_changes.py input.docx output.docx
```

## Dependencies

- docx: `npm install -g docx` (for creating new documents)
- pandoc: Text extraction and conversion
- LibreOffice: PDF/image conversion (auto-configured)
- Poppler: `pdftoppm` for PDF to image conversion
- Python 3: For utility scripts (unpack, pack, validate, comments)

## Critical Rules Summary

1. Set page size explicitly - never rely on defaults (docx-js uses A4)
2. Landscape: pass portrait dimensions, set orientation, let docx-js swap
3. Never use `\n` - use separate Paragraph elements
4. Never use unicode bullets - use LevelFormat.BULLET
5. PageBreak must be in Paragraph
6. ImageRun requires `type` parameter
7. Always set table `width` with DXA - never PERCENTAGE
8. Tables need dual widths - `columnWidths` AND cell `width`, both must match
9. Always add cell margins - use `{ top: 80, bottom: 80, left: 120, right: 120 }`
10. Use `ShadingType.CLEAR` - never SOLID for table shading
11. TOC requires HeadingLevel only - no custom styles
12. Override built-in styles with exact IDs: "Heading1", "Heading2"
13. Include `outlineLevel` in heading styles (0 for H1, 1 for H2, etc.)
14. For tracked changes, preserve formatting by copying `<w:rPr>` from original run
15. Comment markers are siblings of `<w:r>`, never inside
16. Use smart quotes in XML content (`&#x2019;`, `&#x201C;`, etc.)
