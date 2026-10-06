# Extraction Playbook

> Extraction has just one goal: **turn material of any form into plain text you can consult again and again.**
> Convert once, reuse many times — don't keep going back to the original PDF while writing notes.

```
material ─┬─ text PDF ───────────→ get_text() in batches
          ├─ scanned PDF ────────→ render at dpi=150 → vision model: 3 **separate** images per batch
          ├─ PPTX ───────────────→ python-pptx: pull text boxes (+ export charts as images)
          ├─ DOCX ───────────────→ python-docx (mind tables and formulas)
          ├─ chat logs ──────────→ read directly (exported file / share link)
          ├─ web articles ───────→ web extraction (fall back to the browser)
          ├─ video/subtitles ────→ get the transcript first, then treat it as text
          └─ code repos ─────────→ map the structure first (file tree + entry points + deps), then read key files
                                 ↓
                              dump everything to .txt / .md
```

---

## 0. Recon: first decide which route to take

```bash
python scripts/extract_material.py <file> --probe
```

Or manually:

```python
import pymupdf, sys
doc = pymupdf.open(sys.argv[1])
chars = [len(doc[i].get_text().strip()) for i in range(len(doc))]
zero = sum(1 for c in chars if c < 5)
print(f"pages {len(doc)}  near-zero-char pages {zero} ({100*zero//len(chars)}%)  "
      f"avg {sum(chars)//len(chars)} chars/page (auxiliary info)")
print("scan-like pages:", [i+1 for i, c in enumerate(chars) if c < 5][:30])
print("images/page:", [len(doc[i].get_images()) for i in range(min(5, len(doc)))])
```

### Criterion: look at one metric only

| Share of near-zero-text pages | Verdict | Route |
|---|---|---|
| **< 10%** | Usable text layer | **A. Text-based** → `get_text()` |
| **> 50%** | Mostly scanned / images | **B. Scanned** → render + visual transcription |
| 10%–50% | Mixed | Body pages via A, no-text-layer pages via B |

**Why "average characters per page" is not the criterion** (an early mistake, since fixed):

- A Chinese textbook has 700–1000 characters per page, so "average > 100" **is always true** → the threshold has zero discriminating power for books
- A PDF converted from slides has only a few dozen characters per page yet **fully has a text layer** → the threshold misjudges it as a scanned document

"How many pages have no text layer at all" is the metric that actually decides the route. The average character count only distinguishes the **material form**:
≥300 characters/page = book type, < 300 = slide type (both take route A; only the spot-check focus differs).

```bash
# The recon script prints the verdict and the next command directly
python scripts/extract_material.py chapter3.pdf --probe
```

### Page offset (mandatory step, especially important for scanned documents)

**The PDF page ≠ the page number printed in the book**, and **PDF bookmarks are often wrong** — don't trust them.

1. Render the front pages and read the **table of contents** visually (the TOC is **not necessarily within the first 3–20 pages** — the preface may run several pages across multiple versions; in testing the TOC landed on PDF pages 13–14)
2. The TOC gives the "page number in the book"
3. Render any page and have the vision model read the **page number in the running header**
4. Get the offset: `PDF page = book page + offset`

> ⚠️ **Fallback rule**: **chapter-opening pages often don't print a page number** (in testing, the chapter openings of chapters 5, 6, and 7 had none).
> Reverse-computing the offset from the header fails on chapter-opening pages → **infer it ±1 from an adjacent page that has a page number, and record that exception in the extraction output**,
> don't guess silently.

Record the page numbers of chapter ends / exercise pages to cut boundaries (body vs worked examples vs exercises).

---

## A. Text-based PDF

```bash
python scripts/extract_material.py chapter3.pdf --out ./_extract/src.txt
```

**Batch the work**: 20–50 pages at a time, written to the same output file. The point isn't convenience but **avoiding blowing up the context**.

**Spot-check** what you extract (don't fully trust the text layer):

- **Hyphenated line breaks**: a word split across lines must be merged — in CJK material a break like `数据-\n库` is a real case (and in English, `proper-\nties`)
- **Running headers/footers**: the chapter name and page number repeated on every page pollute the body; strip them before writing notes
- **Columns**: a two-column layout may be read as "all of the left column + all of the right column"; reorder by x-coordinate
- **Formulas**: formulas in the text layer are often a scattered sequence of characters (`x 2 + y 2 = r 2`) → **check against the original image**
- **Tables**: tables collapse in the text layer; use `page.find_tables()` or render to an image and read it visually

```python
# Column fix: sort by x-coordinate
blocks = page.get_text("blocks")           # (x0,y0,x1,y1,text,block_no,type)
mid = page.rect.width / 2
left  = sorted([b for b in blocks if b[2] < mid], key=lambda b: b[1])
right = sorted([b for b in blocks if b[0] >= mid], key=lambda b: b[1])
```

**Page reconciliation**: after extraction the script prints "target N pages · actually extracted M pages" and exits non-zero on a mismatch.
Don't skip this line — missing pages silently lose chapters from your notes.

---

## B. Scanned PDF

```bash
python scripts/extract_material.py scan.pdf --render-png ./_extract/pages/ --dpi 150
python scripts/extract_material.py scan.pdf --render-png ./_extract/pages/ --pages 40-80
```

### B.1 Reconcile right after rendering (the only guard against "a hundred missing images")

After rendering the script prints and **verifies**:

```
Page reconciliation: PDF has 241 pages · this run targets 7 pages · 7 rendered successfully · 7 PNGs currently in the dir
⚠️ the dir covers only 7/116 pages of the PDF; 109 pages are not rendered yet (eg: [8, 9, 10, ...])
```

Exit codes: `0` full coverage / `2` partial coverage only / `1` missing pages within the target range.

> **Real incident**: pages 1–24 were rendered first as a probe, but another worker got a directory that was "missing 217 images",
> and nothing at the time would have revealed it. **Rendering in segments is legitimate, but before transcribing you must confirm every segment has been rendered.**

### B.2 Read 3 independent images at a time (not "one page per call", not "stitching")

```bash
# Rendering produces a batch list, one batch per line, `batch` images each (default 3)
python scripts/extract_material.py scan.pdf --render-png ./_extract/pages/ --batch 3
# → ./_extract/pages/batches.txt
```

**Three concepts must be kept apart** (the biggest pitfall this project hit):

| Approach | Effect | Verdict |
|---|---|---|
| **Stitch two pages into one image** for the model | Downsampled to ~620px/page, **subscripts and superscripts smear** | ❌ Never do this |
| **Pass 3 independent images per call** | Each page keeps full resolution, round-trips ÷3 | ✅ Correct approach |
| One call per page | Resolution is fine, but one full model round-trip per page | ⚠️ Works, but **slowest** |

> **"Don't stitch" ≠ "one call per page."** The ambiguity of that wording once caused a real performance incident:
> 105 pages took 14 minutes, of which **13.8 minutes (99%) went to model round-trips**, while all tool execution took only 12 seconds
> (each page = one "read image → generate" round-trip ≈ 8 seconds). With batches of 3 + sharding it drops to about 1/3.

**dpi=150 is the sweet spot**: A4 (595×839pt) renders to about 1241×1748px, just high enough not to be downsampled downstream;
text and simple formulas stay legible, and going higher only gets compressed, wasting compute.

Fixed prompt (copy it verbatim, don't improvise):

> Transcribe the content of these pages completely, line by line (output per page, separated by `===== p<N> =====`).
> Use LaTeX for formulas, keep the numbering of definitions/theorems/examples as-is, and preserve proofs in full.

**If a page fails to transcribe, re-read just that page** — don't rerun the whole batch.

### B.3 Long jobs: parallel sharding + context budget

For a 200+ page scanned book, **don't let one worker do the whole thing** — the context keeps growing and it gets slower toward the end:

| Approach | Notes |
|---|---|
| **Sharding** | Split into 2–4 **non-overlapping** page ranges, one per worker; name files `p0001-0040.md` / `p0041-0080.md` |
| **Context budget** | Write to disk every **20–30 pages**; when a single worker's context reaches about **200 turns**, switch to a fresh window |
| **Coverage reconciliation** | After merging, run `merge_ranges.py` to confirm every page 1..N is covered (**don't go by feel**) |
| **Numbering list** | Append to each transcription a list of the definition/theorem/example numbers in its range, for later cross-checking |

### B.4 Coverage reconciliation (mandatory before merging)

```bash
python scripts/merge_ranges.py ./_extract/pages/ --total 241
python scripts/merge_ranges.py ./_extract/ --total 241 --concat ./_sources/full.md
```

It checks **two levels at once** (this is the double check):

1. **The range declared in the file name** — whether the layout is complete (gaps / overlaps)
2. **The `===== pN =====` page markers inside the file** — whether the actual content is complete

A mismatch raises an alarm: the file name says 40 pages but there are only 38 page markers inside → **2 pages were missed**.
**Relying on file names alone, this kind of miss can never be caught.**

```
❌ Reconciliation failed with 5 problem(s):
   - p0001-0004.md declares 4 pages but has only 3 page markers
   - declared ranges have 2 missing pages
   - 1 overlapping shard ranges
   - page markers have 2 missing pages
```

### B.5 Where OCR fits

OCR (e.g. `rapidocr-onnxruntime`) is about 85% accurate on printed Chinese body text and **completely unreliable on formula regions**:

| Actual content | OCR output |
|---|---|
| `$a_i$` | `α:` |
| `=` | `-` |
| Subscripts / commas | Confused |
| Greek letters | Garbled |

→ **Use OCR only for numbering cross-checks** (to see whether a theorem was missed); see
[`verification.md`](verification.md#3-numbered-cross-check).

---

## C. PPTX / slides

```bash
python scripts/extract_material.py slides.pptx --out ./_extract/src.txt
```

- Text-box extraction order is **by shape z-order, which is not the visual reading order** → you must reorder after extraction
- **Information inside charts/diagrams can't be extracted**: export each page as an image; when there are many charts, take the visual route (headless LibreOffice conversion, or PowerPoint COM export)
- Speaker notes often hold extra information the instructor said aloud — **extract them too**
- A handout PDF version is sometimes easier to extract than the PPTX (the layout is fixed)

---

## D. Conversation logs (teaching dialogues with an AI)

**Local exported files**: read them directly. The typical format is `## Prompt:` / `## Response:` blocks + timestamps + `---` separators.

**Online share links** (e.g. `chatgpt.com/share/...`):
these pages are **client-rendered**, so ordinary web extraction returns empty.
Solution: open it in the browser → the full accessibility tree is saved to a file → page through that file (code blocks, formulas, and tables are all in it).

**What to focus on**: 70% of the dialogue is lecturing tone and confirmation phrases ("great, let's take it step by step"),
**throw all of it away**, keep only the knowledge points, and reorganize them per [`note-conventions.md`](note-conventions.md).

---

## E. Web pages / articles

1. Prefer ordinary extraction; if it returns empty or errors (403/429/WAF/paywall) → switch to the browser
2. Code blocks and formulas must be **kept as-is**; don't let the extractor turn `<` into `&lt;`
3. Record the URL and access date into `source:`
4. Web content changes → **copy key quotes into the note body**, don't leave only a link

---

## F. Video / subtitles / audio

1. First get a transcript (platform subtitles / a local transcription tool)
2. The transcript is plain text, so take the text route
3. **Note**: transcripts have typos and wrong sentence breaks; fix technical terms against the context
4. Timestamps are valuable (you can go back to locate the original video); give a rough range in the note's `source:`, e.g. `Lecture 3, 12:30-25:10`

---

## G. Code repositories / projects

This isn't "extracting text" but **mapping the structure**:

```bash
# 1) Language and size
ls -la; cat package.json pyproject.toml Cargo.toml go.mod 2>/dev/null
# 2) File tree (ignore dependency dirs)
tree -L 3 -I 'node_modules|.git|venv|__pycache__'
# 3) Entry points and key paths
```

The note organization differs:

- One note covers the **overall architecture** (module responsibility table + data-flow diagram + dependency direction)
- Each other note covers **one mechanism** (how it works, why it's designed this way, where its boundary is)
- **Actually run the key code** (the core strategy for engineering) — only paste output once it runs

---

## Writing to disk and cleanup

### Where to put it

- Put extraction outputs together under the output directory in **`_extract/`** (rendered images) and **`_sources/`** (transcribed text); **don't mix them with the notes**
- **Always use relative paths**: `./_extract/`, `./_sources/`.
  **`/tmp/` does not exist on Windows**, and this skill claims to support three platforms — hardcoding `/tmp/` fails outright
- These two directory types are not version-controlled (`.gitignore` already includes them)

### What to do with it: first decide whether it's "regenerable"

| Category | Examples | Action |
|---|---|---|
| **Regenerable** | Rendered PNGs, probe scripts, temporary txt | **Delete** (just rerun; low cost) |
| **Non-regenerable** | **Visual transcription text** of scanned documents, conversation extracts | **Keep** in `_sources/` (redoing takes tens of minutes + many model calls) |
| **Deliverable** | The notes themselves | Keep |

> **Why "clean up intermediate files when the task ends" can't be a blanket rule**: rendering 241 PNG pages takes a few minutes; transcribing 212 pages page by page visually takes tens of minutes.
> Once deleted, any later spot-check (fix a formula, add a chapter, switch output mode) means **rerunning the whole extraction chain**.
> In testing this happened once — 39 transcription files and 212 PNGs were deleted together, and they were the most expensive artifacts.

> ⚠️ **You must tell the user**: at delivery, state plainly "what was kept, why it was kept, how much space it uses, and how to delete it".
> **Don't keep silently, and don't delete silently.**

## FAQ

| Symptom | Cause | Fix |
|---|---|---|
| Extraction comes out empty | Scanned document / client-rendered page | Switch to the visual route / switch to the browser |
| Judged as scanned though it clearly has text | Took "average character count" as the criterion | Look only at the **share of near-zero-text pages** (slide-type material has few characters on average but does have a text layer) |
| Transcription is very slow | Calling the vision model serially, page by page | 3 independent images per call + parallel sharding; don't stitch |
| Find a missing chapter after transcribing | Didn't do coverage reconciliation | `merge_ranges.py` (checks both file-name ranges and internal page markers) |
| Chapter-opening page numbers don't line up | Chapter openings don't print a page number | Infer ±1 from an adjacent page that has one, and record the exception |
| Chinese text garbled | Encoding isn't UTF-8 | `open(..., encoding='utf-8', errors='replace')` or detect the encoding first |
| Formulas all garbled | Formulas in the text layer are scattered to begin with | Check against the original image/page (this is **mandatory**, not optional) |
| Tables collapse | The text layer doesn't preserve table structure | `find_tables()` or render to an image and read visually |
| Order scrambled | Columns / z-order | Sort by coordinates |
| File not found under a Chinese path | Some search tools fail on non-ASCII paths | Verify directly with `ls` / `grep`; don't conclude from this that the file doesn't exist |
| Native program can't read `/c/...` | MSYS paths aren't converted | Pass a `C:/...` forward-slash native path |
