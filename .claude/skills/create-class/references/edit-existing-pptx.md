# Editing an existing branded deck in place (python-pptx)

Use this when you must revise an existing, branded `.pptx` (delete, reorder, retitle,
clone, or split slides) rather than generate a new deck. Regenerating from scratch
discards the deck's theme, layouts, images, and hand-tuned slides, so edit in place.
The file is binary; work on a git-tracked copy so every change is revertible.

Requires `python-pptx` and `lxml` (`python -c "import pptx, lxml"`).

## Windows encoding gate (do this first)

Branded decks routinely contain zero-width spaces (`​`) and emoji. On Windows the
default `cp1252` console encoding crashes any `print` of that text with
`UnicodeEncodeError`. Start every script with:

```python
import sys
sys.stdout.reconfigure(encoding="utf-8")
```

and run it with `PYTHONUTF8=1 python script.py`. Strip `​` from text you print.

## The order-vs-partname gotcha (read before deleting anything)

`slideN.xml` part-file numbers are NOT presentation order, and python-pptx
**resequences the part names on save**. Never address a slide by its `slideN.xml`
number across a save. Enumerate `prs.slides` for live order, and map slides by their
title text (or by live index) instead:

```python
by_title = {s.shapes.title.text.strip(): s for s in prs.slides if s.shapes.title}
```

Verify order first by printing `enumerate(prs.slides, 1)` with each title.

## Core helpers

```python
import copy
from pptx.oxml.ns import qn
from pptx.text.text import _Paragraph

RELS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

def set_para_text(p, text):                     # set text, keep first run's formatting
    runs = p.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.add_run().text = text

def set_title(slide, text):
    set_para_text(slide.shapes.title.text_frame.paragraphs[0], text)

def biggest_body(slide):                        # the main content placeholder
    t = slide.shapes.title
    c = [sh for sh in slide.shapes if sh.has_text_frame
         and (t is None or sh._element is not t._element) and sh.height]
    return max(c, key=lambda x: x.height) if c else None

def set_bullets(slide, bullets):                # rebuild a bullet list, any length
    tf = biggest_body(slide).text_frame
    template = copy.deepcopy(tf.paragraphs[0]._p)   # preserve bullet/font formatting
    for p in list(tf.paragraphs):
        p._p.getparent().remove(p._p)
    for b in bullets:
        newp = copy.deepcopy(template)
        tf._txBody.append(newp)
        set_para_text(_Paragraph(newp, tf), b)
```

## Delete and reorder

Operate on `prs.slides._sldIdLst`. Deleting: remove the `sldId` element and drop its
relationship so no orphan repair prompt appears. Reordering: remove then re-append the
`sldId` children in the desired sequence.

```python
def sldid_map(prs):
    return {i: e for i, e in enumerate(list(prs.slides._sldIdLst), 0)}  # by live index

def delete_slides(prs, slides_to_remove):
    lst = prs.slides._sldIdLst
    targets = {id(s._element) for s in slides_to_remove}
    for sldid, slide in list(zip(list(lst), list(prs.slides))):
        if id(slide._element) in targets:
            rId = sldid.get(qn("r:id"))
            lst.remove(sldid)
            try: prs.part.drop_rel(rId)
            except KeyError: pass
```

## Clone a slide (preserve theme)

python-pptx has no native "duplicate slide". Deep-copy the shapes onto a new slide that
reuses the source's layout, then copy the relationships with an rId remap so images and
hyperlinks still resolve. Cloning a **text-only, same-layout** template is safest because
there are no media rIds to remap.

```python
def duplicate(prs, source):
    new = prs.slides.add_slide(source.slide_layout)
    for sh in list(new.shapes):                 # clear layout placeholders
        sh._element.getparent().remove(sh._element)
    for sh in source.shapes:
        new.shapes._spTree.append(copy.deepcopy(sh._element))
    id_map = {}
    for rId, rel in source.part.rels.items():
        if "slideLayout" in rel.reltype or "notesSlide" in rel.reltype:
            continue                            # add_slide already made the layout rel
        if rel.is_external:
            id_map[rId] = new.part.relate_to(rel.target_ref, rel.reltype, is_external=True)
        else:
            id_map[rId] = new.part.relate_to(rel._target, rel.reltype)
    for el in new.shapes._spTree.iter():        # remap r:embed / r:id / r:link
        for a in ("embed", "id", "link"):
            k = f"{{{RELS}}}{a}"
            if el.get(k) in id_map:
                el.set(k, id_map[el.get(k)])
    return new
```

`add_slide` appends to the end of `_sldIdLst`, so create slides in the final order you
want, or reorder afterward. A cloned slide inherits the template's placeholder geometry,
so keep bullet counts near the template's to avoid overflow.

## Two gotchas that cause a silent redo

**Set all four of left/top/width/height when you move a placeholder.** Assigning only
`.left`/`.width` (or any subset) makes python-pptx write an `<a:xfrm>` with the unset
coordinates as **0**. A body you widened but did not reposition collapses to top=0,
height=0, overflows from the top, and overlaps the title, an overlap the numbers hide until
you render. Always set all four together:

```python
b.left, b.top, b.width, b.height = Inches(0.5), Inches(1.55), Inches(12.33), Inches(5.2)
```

**A "text-only" template must have no picture PLACEHOLDER, not just no picture shape.** A
filled picture placeholder has `shape_type == PLACEHOLDER`, not `PICTURE`, so a check for
`MSO_SHAPE_TYPE.PICTURE` misses it. Cloning such a template repeats the same image on every
slide and the deck looks duplicated and useless. Detect and drop it:

```python
from pptx.enum.shapes import PP_PLACEHOLDER
for sh in list(slide.shapes):
    if sh.is_placeholder and sh.placeholder_format.type == PP_PLACEHOLDER.PICTURE:
        sh._element.getparent().remove(sh._element)   # then widen the body to full width
```

Pick a template with neither a picture shape nor a picture placeholder, or strip the
placeholder right after cloning and reposition the body (all four coordinates).

## Split one deck into per-topic decks (avoid cross-package copy)

Copying slides between two open packages (media, layouts, rels) is fragile. To carve a
section into its own deck, do the reverse: copy the whole file, then **keep only** the
target slides with `delete_slides`. Pure deletion needs no rId surgery.

```python
import shutil
shutil.copyfile(SRC, DEST)
prs = Presentation(DEST)
keep = {id(s._element) for s in wanted_slides}
delete_slides(prs, [s for s in prs.slides if id(s._element) not in keep])
```

Building a boilerplate deck is the same move: copy, keep title/about/agenda, rewrite text.

## Drawing diagrams natively (no image assets)

When you cannot generate or download images, build concept diagrams from shapes, with no
external assets. A left-to-right flow is rounded rectangles joined by right arrows; a rating
scale is colored segments side by side. Constrain the body height first so the diagram has a
clear band beneath it, then place shapes in that band:

```python
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
body.top, body.height = Inches(1.55), Inches(3.0)          # leave a band below the text
box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(5.0), w, Inches(1.15))
box.fill.solid(); box.fill.fore_color.rgb = accent
arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, gap_left, Inches(5.4), gap, Inches(0.34))
```

Space N boxes across `usable = slide_width - 2*margin` leaving a gap per arrow, and after
saving assert every shape's right and bottom edge falls within the slide bounds (nothing
autoflows an off-slide box back on). Then render and look.

## QA before declaring done

Reopen the saved file with `Presentation(path)`; a clean reopen means valid OOXML. Then,
whenever possible, render the changed slides to images and look at them: geometry checks
catch collapsed or off-slide boxes, but only pixels catch title/body overlap, overflow,
and low contrast. Every edit that sets shape geometry (position, size, cloned templates,
new diagrams) should be eyeballed rendered before you call it done.

### Install a renderer

The reliable, cross-platform combo is LibreOffice (`.pptx` -> PDF) plus PyMuPDF
(PDF -> PNG, pure pip, no poppler needed):

| OS | Install |
| --- | --- |
| Windows | `winget install -e --id TheDocumentFoundation.LibreOffice` then `pip install pymupdf` |
| macOS | `brew install --cask libreoffice` then `pip install pymupdf` |
| Linux | `sudo apt-get install -y libreoffice` then `pip install pymupdf` |

On Windows `soffice` is not on PATH by default; call it at
`C:\Program Files\LibreOffice\program\soffice.exe`. A system install (winget/brew/apt)
may need the user to run it; suggest it and continue with structural checks until it lands.

### Render to per-slide PNGs

```bash
soffice --headless --convert-to pdf --outdir out "deck.pptx"
python -c "import fitz; d=fitz.open('out/deck.pdf'); [p.get_pixmap(dpi=120).save(f'out/slide{p.number+1}.png') for p in d]"
```

Read the PNGs (they load as images) and check each changed slide. `dpi=120` is enough to
read text; raise it for fine detail. Poppler's `pdftoppm -png -r 150 out/deck.pdf out/slide`
is an equivalent second step if PyMuPDF is unavailable.

### Zero-install on Windows: PowerPoint COM

If Microsoft Office is installed, render straight from PowerPoint, no LibreOffice needed,
and at true PowerPoint fidelity (the most accurate option). Requires `pip install pywin32`.

```python
import os, win32com.client as w
ppt = w.Dispatch("PowerPoint.Application"); ppt.Visible = 1
pres = ppt.Presentations.Open(os.path.abspath(deck), ReadOnly=1, WithWindow=0)
for i in range(1, pres.Slides.Count + 1):          # or a chosen index list to render a subset
    fn = os.path.normpath(os.path.join(os.path.abspath(out), "slide%02d.png" % i))
    pres.Slides(i).Export(fn, "PNG", 1600, 900)     # pres.Export(out, "PNG") exports all at once
pres.Close(); ppt.Quit()
```

`Slide.Export` fails with a generic `PowerPoint can't save ^0 to ^1` COM error on a
mixed-separator, forward-slash, or 8.3 short-name path (`ALEXAN~1`). Always pass
`os.path.normpath(os.path.abspath(...))` so the path is absolute with backslashes.

### When no renderer is available

Verify structurally and say so: confirm each changed slide has its title and expected
body text, that the body's `top` sits below the title's bottom, and that every shape's
right and bottom edges fall within the slide bounds. Tell the user no visual render was
performed and that a quick eyeball is worth it. Never claim a slide "looks" correct
without having rendered it.
