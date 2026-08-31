# merge-slides

Merge two or more PPTX files into one. This is a sub-capability of the `create-slides` Gamma
path: Gamma caps at roughly 10 items per generation call, so a module with more than 10 slide
spec files is generated across multiple separate Gamma PPTX exports that then need combining
into a single deck.

## Two approaches: pick by environment and need

| | PowerPoint COM (below) | ZIP/XML script (rest of this doc) |
| --- | --- | --- |
| Needs | Windows + Office installed | python + lxml only (cross-platform) |
| Insert position | any position (after any slide) | append-only (end of deck) |
| Which source slides | any subset (`SlideStart..SlideEnd`) | all slides in the file |
| Media collisions | remapped automatically | handled by manual `f2_`-prefix rename |
| Fidelity | full (layouts, images, tables) | full, once rename is correct |

Prefer COM when Office is present and you need positional or subset insert (for example
unifying two overlapping decks). Use the ZIP script for headless/cross-platform runs or
when Office is unavailable. **Do not attempt a slide-copy with `python-pptx`**: it cannot
copy a slide with fidelity (its picture/table relationships break) — use COM or the ZIP
script.

## High-fidelity insert via PowerPoint COM (Windows + Office)

`Slides.InsertFromFile(FileName, Index, SlideStart, SlideEnd)` inserts source slides
`SlideStart..SlideEnd` (1-based) *after* position `Index` (1-based), preserving layouts,
images, and tables and remapping media automatically.

```python
import win32com.client as w
import os

base   = os.path.abspath("full-deck.pptx")     # deck to insert INTO
source = os.path.abspath("other-deck.pptx")    # deck to pull slides FROM
out    = os.path.abspath("merged.pptx")

app = w.Dispatch("PowerPoint.Application")
pres = app.Presentations.Open(base, WithWindow=False)
pres.Slides.InsertFromFile(source, 10, 2, 4)   # source slides 2-4, after slide 10
pres.SaveAs(out, 24)                            # 24 = ppSaveAsOpenXMLPresentation
pres.Close()
app.Quit()
```

Requires `pywin32` (`import win32com.client`) and a working install
(`Dispatch("PowerPoint.Application")`). Verify by enumerating titles with python-pptx
after the merge.

### Deciding what to merge ("take the best of both")

When unifying two overlapping decks, list both decks' slide titles first, mark which
source slides are *unique* (not already covered by the base), and insert only those, at
the topically correct position. Redundant title, summary, and duplicate-topic slides are
dropped, not inserted.

## When to invoke

- After generating slides in batches (Gamma caps at ~10 items per generation call)
- When a module has more than 10 slide spec files and was therefore split across multiple Gamma exports
- The user asks to "merge the pptx files" or "combine the parts"
- The user asks to unify/reorder decks and keep the best of both (use the COM path above)

## Invocation

The parent `create-slides` skill runs this inline. Given a module `pptx/` folder that holds
several Gamma exports, fill in the input list in slide order and the output name, run the
script, verify, then delete the script. Do not ask the user to run it manually.

Example target: `demos/09-agent-teams-remote/pptx`

## The problem: identical media filenames

Every Gamma PPTX export uses the same internal media filenames (`image-1-1.png`,
`image-2-1.png`, etc.). Naively copying slides from one ZIP into another overwrites those
media files, breaking images on all but the last merged file.

The fix: rename media from each additional source file with a unique prefix (`f2_`, `f3_`,
...) and rewrite each slide's relationship file to reference the renamed paths.

## Script

Save as `merge_pptx.py` at the repo root, run it, then delete it.

```python
import zipfile
import os
import shutil
import re
from pathlib import Path
from lxml import etree

INPUT_FILES = [
    "demos/NN-module/pptx/NN-01-part-one.pptx",
    "demos/NN-module/pptx/NN-02-part-two.pptx",
]
OUTPUT_FILE = "demos/NN-module/pptx/NN-module-name.pptx"
TEMP = Path("merge_temp")

REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
PRS_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
CT_NS  = "http://schemas.openxmlformats.org/package/2006/content-types"
R_NS   = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

SLIDE_CT   = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
NOTES_CT   = "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"
SLIDE_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
IMAGE_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
NOTES_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide"

def extract_base(src, dst):
    with zipfile.ZipFile(src) as z:
        for name in z.namelist():
            if name.endswith('/'):
                continue
            out = dst / name.replace('/', os.sep)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(z.read(name))

def get_slide_nums(zf):
    return sorted(
        int(re.search(r'slide(\d+)\.xml$', n).group(1))
        for n in zf.namelist()
        if re.match(r'ppt/slides/slide\d+\.xml$', n)
    )

def get_notes_nums(zf):
    return sorted(
        int(re.search(r'notesSlide(\d+)\.xml$', n).group(1))
        for n in zf.namelist()
        if re.match(r'ppt/notesSlides/notesSlide\d+\.xml$', n)
    )

def get_base_max_slide(dst):
    slides = list((dst / 'ppt' / 'slides').glob('slide[0-9]*.xml'))
    return max(int(re.search(r'slide(\d+)', s.stem).group(1)) for s in slides) if slides else 0

def get_base_max_notes(dst):
    notes_dir = dst / 'ppt' / 'notesSlides'
    if not notes_dir.exists():
        return 0
    notes = list(notes_dir.glob('notesSlide[0-9]*.xml'))
    return max(int(re.search(r'notesSlide(\d+)', n.stem).group(1)) for n in notes) if notes else 0

def rewrite_rels(rels_bytes, media_rename_map, notes_rename_map=None):
    root = etree.fromstring(rels_bytes)
    for rel in root.findall(f'{{{REL_NS}}}Relationship'):
        rtype = rel.get('Type', '')
        target = rel.get('Target', '')
        if rtype == IMAGE_TYPE:
            basename = target.split('/')[-1]
            if basename in media_rename_map:
                rel.set('Target', f'../media/{media_rename_map[basename]}')
        if notes_rename_map and rtype == NOTES_TYPE:
            basename = target.split('/')[-1]
            if basename in notes_rename_map:
                rel.set('Target', f'../notesSlides/{notes_rename_map[basename]}')
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

if TEMP.exists():
    shutil.rmtree(TEMP)
TEMP.mkdir()

print(f"Extracting base: {INPUT_FILES[0]}")
extract_base(INPUT_FILES[0], TEMP)

for file_idx, src_file in enumerate(INPUT_FILES[1:], start=2):
    prefix = f"f{file_idx}_"
    print(f"Merging: {src_file} (prefix={prefix})")

    base_max_slide = get_base_max_slide(TEMP)
    base_max_notes = get_base_max_notes(TEMP)

    with zipfile.ZipFile(src_file) as zf:
        src_slide_nums = get_slide_nums(zf)
        src_notes_nums = get_notes_nums(zf)

        src_media = [n for n in zf.namelist() if re.match(r'ppt/media/.+', n) and not n.endswith('/')]
        media_rename = {n.split('/')[-1]: prefix + n.split('/')[-1] for n in src_media}

        notes_rename = {}
        for i, old_num in enumerate(src_notes_nums):
            new_num = base_max_notes + i + 1
            notes_rename[f'notesSlide{old_num}.xml'] = f'notesSlide{new_num}.xml'

        for name in src_media:
            basename = name.split('/')[-1]
            (TEMP / 'ppt' / 'media' / media_rename[basename]).write_bytes(zf.read(name))

        for i, old_num in enumerate(src_slide_nums):
            new_num = base_max_slide + i + 1
            (TEMP / 'ppt' / 'slides' / f'slide{new_num}.xml').write_bytes(
                zf.read(f'ppt/slides/slide{old_num}.xml'))
            rels_name = f'ppt/slides/_rels/slide{old_num}.xml.rels'
            if rels_name in zf.namelist():
                new_rels = rewrite_rels(zf.read(rels_name), media_rename, notes_rename)
                out_rels = TEMP / 'ppt' / 'slides' / '_rels' / f'slide{new_num}.xml.rels'
                out_rels.parent.mkdir(parents=True, exist_ok=True)
                out_rels.write_bytes(new_rels)

        for i, old_num in enumerate(src_notes_nums):
            new_num = base_max_notes + i + 1
            out_notes = TEMP / 'ppt' / 'notesSlides' / f'notesSlide{new_num}.xml'
            out_notes.parent.mkdir(parents=True, exist_ok=True)
            out_notes.write_bytes(zf.read(f'ppt/notesSlides/notesSlide{old_num}.xml'))
            notes_rels_name = f'ppt/notesSlides/_rels/notesSlide{old_num}.xml.rels'
            if notes_rels_name in zf.namelist():
                out_nr = TEMP / 'ppt' / 'notesSlides' / '_rels' / f'notesSlide{new_num}.xml.rels'
                out_nr.parent.mkdir(parents=True, exist_ok=True)
                out_nr.write_bytes(zf.read(notes_rels_name))

    ct_path = TEMP / '[Content_Types].xml'
    ct_root = etree.parse(str(ct_path)).getroot()
    new_max = get_base_max_slide(TEMP)
    new_max_notes = get_base_max_notes(TEMP)

    for num in range(base_max_slide + 1, new_max + 1):
        ov = etree.SubElement(ct_root, f'{{{CT_NS}}}Override')
        ov.set('PartName', f'/ppt/slides/slide{num}.xml')
        ov.set('ContentType', SLIDE_CT)

    for num in range(base_max_notes + 1, new_max_notes + 1):
        ov = etree.SubElement(ct_root, f'{{{CT_NS}}}Override')
        ov.set('PartName', f'/ppt/notesSlides/notesSlide{num}.xml')
        ov.set('ContentType', NOTES_CT)

    ct_path.write_bytes(etree.tostring(ct_root, xml_declaration=True, encoding='UTF-8', standalone=True))

    prs_rels_path = TEMP / 'ppt' / '_rels' / 'presentation.xml.rels'
    prs_rels_root = etree.parse(str(prs_rels_path)).getroot()
    existing_ids = [int(e.get('Id').replace('rId', '')) for e in prs_rels_root.findall(f'{{{REL_NS}}}Relationship')]
    next_rid = max(existing_ids) + 1

    new_slide_nums = list(range(base_max_slide + 1, get_base_max_slide(TEMP) + 1))
    rid_to_slide = {}
    for num in new_slide_nums:
        rid = f'rId{next_rid}'
        rid_to_slide[rid] = num
        next_rid += 1
        rel = etree.SubElement(prs_rels_root, f'{{{REL_NS}}}Relationship')
        rel.set('Id', rid)
        rel.set('Type', SLIDE_TYPE)
        rel.set('Target', f'slides/slide{num}.xml')

    prs_rels_path.write_bytes(
        etree.tostring(prs_rels_root, xml_declaration=True, encoding='UTF-8', standalone=True))

    prs_path = TEMP / 'ppt' / 'presentation.xml'
    prs_root = etree.parse(str(prs_path)).getroot()
    sld_lst = prs_root.find(f'.//{{{PRS_NS}}}sldIdLst')
    existing_ids_prs = [int(e.get('id')) for e in sld_lst.findall(f'{{{PRS_NS}}}sldId')]
    next_slide_id = max(existing_ids_prs) + 1

    for rid, num in rid_to_slide.items():
        sld_id_el = etree.SubElement(sld_lst, f'{{{PRS_NS}}}sldId')
        sld_id_el.set('id', str(next_slide_id))
        sld_id_el.set(f'{{{R_NS}}}id', rid)
        next_slide_id += 1

    prs_path.write_bytes(
        etree.tostring(prs_root, xml_declaration=True, encoding='UTF-8', standalone=True))

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as out_zip:
    for fp in TEMP.rglob('*'):
        if fp.is_file():
            arcname = str(fp.relative_to(TEMP)).replace(os.sep, '/')
            out_zip.write(fp, arcname)

shutil.rmtree(TEMP)

with zipfile.ZipFile(OUTPUT_FILE) as z:
    slides = [n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
    media  = [n for n in z.namelist() if re.match(r'ppt/media/.+', n) and not n.endswith('/')]
    print(f"Done: {OUTPUT_FILE}")
    print(f"  Slides : {len(slides)}")
    print(f"  Media  : {len(media)}")
```

## Steps to run

1. Fill in `INPUT_FILES` (in slide order) and `OUTPUT_FILE` (parent module name)
2. Save as `merge_pptx.py` at the repo root
3. Run: `python merge_pptx.py`
4. Delete `merge_pptx.py`

## Verify images are intact

```python
import zipfile, re
from lxml import etree

REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
IMAGE_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"

with zipfile.ZipFile("path/to/merged.pptx") as z:
    all_files = set(z.namelist())
    for rels_name in sorted(n for n in all_files if re.match(r'ppt/slides/_rels/slide\d+\.xml\.rels$', n)):
        root = etree.fromstring(z.read(rels_name))
        slide_num = re.search(r'slide(\d+)', rels_name).group(1)
        for rel in root.findall(f'{{{REL_NS}}}Relationship'):
            if rel.get('Type') == IMAGE_TYPE:
                media_path = 'ppt/media/' + rel.get('Target').split('/')[-1]
                status = "OK" if media_path in all_files else "BROKEN"
                print(f"  slide{slide_num}: {status} -> {media_path.split('/')[-1]}")
```

## Dependency

`pip install lxml` (already present if python-pptx is installed).
