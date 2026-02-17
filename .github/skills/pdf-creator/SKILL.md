---
name: pdf-creator
description: Create, edit, analyze, and validate PDF files and documents. Use when generating reports, merging PDFs, extracting text and tables, creating documents dynamically, or processing scanned PDFs with OCR. Supports both Python libraries (pypdf, pdfplumber, reportlab) and command-line tools. Keywords: create PDF, merge PDF, split PDF, extract text, OCR, generate report, PDF form, PDF manipulation.
---

# PDF Creation and Processing

Comprehensive guide for creating, manipulating, analyzing, and extracting data from PDF documents using Python and command-line tools.

Use this skill when:

- Creating PDFs dynamically from data or templates
- Merging, splitting, or rotating PDF pages
- Extracting text, tables, or metadata from PDFs
- Adding watermarks, passwords, or annotations
- Processing scanned PDFs with OCR (optical character recognition)
- Generating reports or documents as PDFs
- Filling PDF forms programmatically

## Quick Start

### Create a Simple PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

c.drawString(100, height - 100, "Hello World!")
c.line(100, height - 140, 400, height - 140)
c.save()
```

### Extract Text from PDF

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()
print(text)
```

### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

## Python Libraries

### pypdf - Basic Operations

Handle merging, splitting, rotating, and manipulating PDF pages.

**Merge PDFs**

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

**Split PDF into Individual Pages**

```python
from pypdf import PdfWriter, PdfReader

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

**Extract Metadata**

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

**Rotate Pages**

```python
from pypdf import PdfWriter, PdfReader

reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

**Add Watermark**

```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]

reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

**Password Protection**

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

Extract text with layout preservation and analyze tables within PDFs.

**Extract Text with Layout**

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

**Extract Tables**

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

**Advanced Table Extraction (Export to Excel)**

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

Build professional PDFs from scratch with layout control, styling, and multi-page support.

**Basic PDF Creation**

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")
c.line(100, height - 140, 400, height - 140)
c.save()
```

**Create PDF with Multiple Pages**

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

doc.build(story)
```

**Subscripts and Superscripts**

Use XML markup tags within Paragraph objects. Never use Unicode subscript/superscript characters as they render as black boxes.

```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

## Command-Line Tools

### pdftotext (poppler-utils)

Extract text from PDFs at the command line.

```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages (pages 1-5)
pdftotext -f 1 -l 5 input.pdf output.txt
```

### qpdf

Merge, split, rotate, decrypt, and manipulate PDFs.

```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages (pages 1-5)
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate page 1 by 90 degrees clockwise
qpdf input.pdf output.pdf --rotate=+90:1

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdfimages (poppler-utils)

Extract images from PDFs.

```bash
# Extract all images as JPEG
pdfimages -j input.pdf output_prefix
# Outputs: output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

## Common Tasks

### Extract Text from Scanned PDFs with OCR

Convert PDF pages to images and use OCR to recognize text.

```python
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

Requirements: `pip install pytesseract pdf2image`

### Extract Images from PDF

```bash
# Using command line
pdfimages -j input.pdf output_prefix
```

Or with Python:

```python
from PIL import Image
from pdf2image import convert_from_path

images = convert_from_path('input.pdf')
for i, image in enumerate(images):
    image.save(f'page_{i+1}.png', 'PNG')
```

### Generate Report PDF from Data

```python
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

doc = SimpleDocTemplate("report.pdf", pagesize=landscape(letter))
styles = getSampleStyleSheet()
story = []

# Title
story.append(Paragraph("Sales Report Q4 2025", styles['Title']))
story.append(Spacer(1, 12))

# Table data
data = [
    ['Product', 'Q1', 'Q2', 'Q3', 'Q4', 'Total'],
    ['Widget A', '1000', '1200', '1500', '1800', '5500'],
    ['Widget B', '800', '900', '950', '1100', '3750'],
    ['Widget C', '1500', '1600', '1700', '1900', '6700'],
]

table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

story.append(table)
doc.build(story)
```

### Extract and Analyze PDF Metadata

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")

# Page count
print(f"Total pages: {len(reader.pages)}")

# Metadata
meta = reader.metadata
if meta:
    for key, value in meta.items():
        print(f"{key}: {value}")

# Check if encrypted
print(f"Is encrypted: {reader.is_encrypted}")
```

## Quick Reference

| Task             | Library       | Code                            |
| ---------------- | ------------- | ------------------------------- |
| Merge PDFs       | pypdf         | PdfWriter + add_page()          |
| Split PDFs       | pypdf         | Loop and write individual pages |
| Extract text     | pdfplumber    | page.extract_text()             |
| Extract tables   | pdfplumber    | page.extract_tables()           |
| Create PDFs      | reportlab     | Canvas or SimpleDocTemplate     |
| Rotate pages     | pypdf         | page.rotate()                   |
| Merge PDF        | qpdf CLI      | qpdf --empty --pages ...        |
| Extract images   | pdfimages CLI | pdfimages -j input.pdf prefix   |
| OCR scanned      | pytesseract   | Convert to image first          |
| Add watermark    | pypdf         | page.merge_page(watermark)      |
| Password protect | pypdf         | writer.encrypt()                |

## Installation

Install required libraries:

```bash
# Core PDF libraries
pip install pypdf pdfplumber reportlab

# For OCR on scanned PDFs
pip install pytesseract pdf2image pillow

# For enhanced table extraction
pip install pandas openpyxl

# Command-line tools (macOS)
brew install poppler

# Command-line tools (Linux)
sudo apt-get install poppler-utils qpdf

# Command-line tools (Windows)
# Install via choco or download from project sites
```

## Tips

1. Use pdfplumber for text extraction if layout matters
2. Use reportlab for creating fully styled PDFs from scratch
3. Use pypdf for page manipulation (merge, split, rotate)
4. Always check if PDF is encrypted before processing
5. For scanned PDFs, OCR is necessary to extract readable text
6. Use command-line tools for batch processing in shell scripts
7. Test subscripts/superscripts in reportlab with XML tags, not Unicode characters
