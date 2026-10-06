---
name: review-anything
description: "Use when turning study material into structured Markdown review notes — a textbook/lecture-slide PDF, a scanned handout, a class transcript, a chat log, a web article, or source code that should become a topic folder of notes, an overview (MOC), a cheatsheet, or an errata page. Rewrites the material instead of transcribing it, applies a theory/engineering/humanities strategy depending on the subject, works under an explicit context/cost budget, and verifies with a bounded sample before delivery. The notes are always written in the USER's language, not in the skill's language or English."
version: 1.0.0
author: 6duck
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [notes, review, markdown, obsidian, pdf, textbook, study, summarize]
    category: note-taking
    related_skills: [pdf, ocr-and-documents, obsidian]
---

# Review Anything

**Input: any study material. Output: a set of Markdown review notes that stand on their own and survive checking.**

Textbooks, lecture slides, handouts, subtitles from a recorded class, a teaching conversation with an
LLM, an article someone sent you, code you wrote — none of it should just sit on disk in its raw form.
This skill turns it into notes that **the you of three months from now can still read**: one folder per
topic, numbered, extensible, with self-tests and a knowledge dependency map.

**Core claim: knowledge does not look the same across subjects, so notes must not either.**
A theorem, a snippet of C, and a historical event are three different things to have "learned" —
guaranteed by **logic**, by **running an it**, and by **provenance**. So three strategies, not one template.

---

## ⚡ Context economy (read this before anything else)

An agent's billed cost is **not** the work it does. It is the *sum of the context sent on every step*:

```
billed tokens ≈ Σ over steps ( system + all prior messages + all tool results )
```

A tool result of size `S` that enters the context at step `k` of `N` is re-sent on **every** later step,
so its true cost is `S × (N − k)`, not `S`. Consequences, all measured on a real 168-step run that
produced 9 notes:

| Fact | Measured |
|---|---|
| Total billed | 63.9 M tokens across 3 sessions |
| Actual new work (fresh input + output) | 862 k — **1.4 %** |
| Everything else | **98.6 % was the same context being replayed** |
| `read`-ing files back into the conversation | 14.5 M — the single biggest cost |
| Loading this skill's own docs into context | 5.6 M — 16 % of the main session |
| Cost of ~1,000 tokens of skill docs, once replayed | **≈165,000 billed tokens** |

**Cost is quadratic in steps × context.** Halving both halves the bill by 4×. Two levers only:
**shrink the context, and shrink the step count.**

### The seven rules

1. **Content lives on disk, not in the conversation.** Transcripts, note bodies, extraction dumps and
   verification data are *files*. The conversation carries a path plus a ≤3-line summary. Never paste a
   transcript or a note body into the conversation — writing it once means re-sending it on every step after.
2. **Never read back what you (or a subagent) already wrote.** It is on disk and it is large. Need a
   detail? `grep` for it, then read that window (`offset`/`limit`). A full re-read of your own artifact is
   pure replay tax. **The extracted source counts too**: never read a whole `_extract/src*.txt` — read the
   page-range slice for the note at hand (three whole-source reads cost 23 % of one run's bill).
3. **Load only the section of documentation you need.** `grep` for the heading, read that window. Never
   read a whole `SKILL.md`/reference file "to be safe" — see the 165,000-token-per-1k line above.
4. **Shard the work into short sessions.** One note folder ≠ one giant session. Every 2–3 notes, start a
   fresh session carrying only `00-overview` and the relevant transcript slice. 168 steps at 200 k context
   is 34 M; 70 steps at 40 k context is 6 M for the same deliverable.
5. **Subagents: files out, one line in.** A subagent exists to keep bulk out of the parent context. It
   writes its artifact to disk and returns **≤3 lines** (path, conclusion, counts). A subagent that dumps
   its findings into the parent has made things worse than doing nothing.
6. **Never enumerate a whole tree or repo.** List one level, get sizes from `du`/`wc`/`stat` — do not print
   contents to discover them. One recursive directory listing cost 0.95 M tokens in the run above.
7. **Images: 3 independent images per call, transcribe once, then drop them.** Each image costs ~1.3 k
   tokens of context; the expensive mistake is not the image, it is *re-reading the same page later*.
   To re-check a page, send a subagent and take back one line.

> **The honest framing**: the money is usually small (a 63.9 M-token run on a cache-heavy model cost about
> US$0.5, because 98.6 % of it was cache-hit input at 1/50 the miss price). **The real price is wall-clock
> time**, and it has exactly the same root cause — every step re-prefills the whole context. Shrinking the
> context buys back both.

---

## Language rule

**The skill is written in English; the notes are not.**

- Everything you produce for the user is in **the user's own language** — the language they asked in, and
  normally the language of the source material. A Chinese user's notes are in Chinese.
- **Template section headings are illustrative.** Render them in the output language; keep YAML field
  *names* unchanged.
- If the user's language is ambiguous, ask once — do not default to English.

---

## When to use it

**Use:** "summarize this PDF / slide deck into Markdown", "tidy up these chapters", "turn this
conversation into notes", "review outline", "exam cheatsheet", "I just finished this topic, make notes" —
the material might be a book, a pile of screenshots, or a chat log. Also **extending existing notes**: a
new source on the same topic is appended to the existing numbering sequence.

**Don't use:** the user wants a single paragraph summary (no structure, nothing on disk) → just answer.
The user wants material for *other people* (paper, report, deck) → the matching document skill.
The material itself is the archive → store it as-is.

---

## The Five Rules (they do not vary by subject)

### 1. Rewrite, don't transcribe

The source is **written for someone else** (a lecturer talking, an author writing); the notes are **for
your own revision**. Drop the lecturing tone, the chapter introductions, the transitions. **Test**: if
deleting a passage costs nothing to your understanding of the point, delete it.

### 2. Complete the cluster

Source material is unevenly detailed (the lecturer mentioned it once; the exam may ask exactly that
half-sentence). **For every concept the material mentions, work out which larger cluster it belongs to, and
present the cluster.**

| The material mentions | The cluster you must complete |
|---|---|
| a network switch | packet vs. circuit switching, routing, multiplexing (the topic is only meaningful against the alternatives) |
| coaxial cable | twisted pair / fibre / wireless (you remember it by contrast) |
| `NOT EXISTS` | `EXISTS` / `IN` / set difference, and behaviour with NULL |
| normalization to 3NF | 1NF / 2NF / BCNF / denormalization |
| a determinant | matrices, rank, invertibility, linear dependence |
| a historical event | its causes, its aftermath, what was happening elsewhere |

Ask: **"Which larger cluster does this belong to, and where does that cluster end?"**

### 3. Stable numbered slots

Note files use **two-digit numbers** (`01-`, `02-`, …) because the folder will keep growing. Each new
source appends to the sequence — no renames, no broken links. Every note ends with **upstream/downstream
links** (rendered in the output language) so the folder forms a chain:

```markdown
---
**Upstream**: [[01-SQL Overview and the Three-Level Schema]]
**Downstream**: [[03-Single-Table Queries]] · [[10-SQL Cheatsheet]]
```

### 4. Self-contained

**Test**: send one file to a classmate who never saw the source. Can they follow it? Therefore: full form
of every abbreviation on first use; a source figure becomes an ASCII diagram or table, or at least a page
citation; key numbers, formulas and conclusions carry provenance (section / page / URL).

### 5. Cite and grade — **the floor**

Every statement must answer **"where did this come from?"**:

| Marker | Meaning |
|---|---|
| (none) | from the source material |
| `[extension]` | you added it; the source does not have it (say so) |
| ✅ verified | you proved it and said how: **ran it** (type B — environment + version) or **recomputed / re-derived it by hand** (type A — show the arithmetic, no script) |
| 📖 documented | from official docs or an authoritative source, with the link |
| ⚠️ unverified | neither proved nor sourced; treat as open |
| **provenance unknown** | stated by the source but untraceable |

**Rather look weak than claim credit.** Presenting a guess as a fact is the worst failure of this document type.

---

## Three subject strategies (decide the type in Phase 0)

| Type | Typical material | Correctness guaranteed by | Emphasize |
|---|---|---|---|
| **A · theory** | maths, physics, chemistry, statistics | **logic** | formulas, derivations, relationships, examples |
| **B · engineering** | programming, networking, OS, databases, electronics | **running it** | code, error analysis, measured behaviour, environment differences |
| **C · humanities** | history, philosophy, law, literature, social science | **provenance** | backbone extraction, classification, searchability |

**Tie-breaker**: *if this is wrong, how would you find out?* — you can't derive it (A) / you can't run it
(B) / you can't trace the source (C).

**The one rule that matters most per type** (the rest is in the reference, and you *will* read it):

- **A** — **justify every step of every derivation**, and record each formula as a *trio*: the formula
  itself + its applicability conditions + its equality condition. A formula missing the last two is dangerous.
- **B** — **actually run it and paste the output verbatim**. Engineering knowledge is only proven by
  execution; write conclusions as conditionals ("measured on A; not tested on B").
- **C** — **write the backbone first** (3–7 one-sentence items, then hang detail on them), and **separate
  claims from facts** ("X argues that …" — never present an opinion as a fact).

**Mixed material is common** (a maths textbook with programming labs, an economics textbook with models,
data and intellectual history). **Split by note**, keep each note internally consistent, and record each
note's type in `00-overview`.

> **Before writing a single note**, read the matching section of
> [`references/subject-strategies.md`](references/subject-strategies.md) — skeletons, the full move list,
> verification method and a worked example per type. This step is not optional; it is where the quality comes from.

---

## Workflow

```
Phase 0  recon      What is this? Which subject? Can it be extracted? Where are the boundaries? Where does output go?
Phase 1  extract    Get everything to disk as plain text (convert once, reuse many times)
Phase 2  structure  Knowledge-cluster map → folder → numbering → overview skeleton
Phase 3  write      Apply the subject strategy, note by note — one short session per 2–3 notes
Phase 4  verify     Machine check + a bounded 3-item sample. Nothing exhaustive.
Phase 5  deliver    Report statistics + state what intermediate artifacts were kept
```

### Phase 0 · Recon (do not skip)

**First: decide the subject type** (A / B / C). It drives every later action. Then answer four questions —
**never guess content from the filename**:

```bash
ls -la <material> && file <material>        # size, count, real format (extensions lie)

# text layer or scanned? -> this decides the extraction route
python scripts/extract_material.py <PDF> --probe
```

**Decision rule — one primary criterion: the share of near-zero-text pages.**

| Observation | Verdict | Route |
|---|---|---|
| near-zero-text pages **< 10 %** | usable text layer | **text route** (`get_text()`) |
| near-zero-text pages **> 50 %** | mostly scanned/images | **scan route** (vision transcription) |
| in between | mixed | text route for text pages, vision route for image pages |

Average characters per page is auxiliary only — **slides exported to PDF have few characters per page yet
do have a text layer**, so it cannot be the criterion.

Also settle: **chapter/page boundaries** (PDF bookmarks are often wrong — recover the offset from running
headers; a chapter opener with no printed number is inferred from a neighbour ±1) and **where the output
goes, in what language**. Ask; do not assume.

### Phase 1 · Extract

**One principle: everything onto disk as plain text before you write a single note.** Convert once, reuse
many times, and never let the conversion pass through the conversation (rule 1 — this is where a long run
quietly spends most of its budget).

Route per material type → [`references/extraction-playbook.md`](references/extraction-playbook.md), with
[`scripts/extract_material.py`](scripts/extract_material.py):

```bash
python scripts/extract_material.py chapter3.pdf --out _extract/src.txt          # text-layer PDF
python scripts/extract_material.py scan.pdf --render-png _extract/pages/ --dpi 150
python scripts/extract_material.py slides.pptx --out _extract/src.txt
```

- **Text-layer PDF**: `pymupdf` in batches of 20–50 pages, into a `.txt`.
  **Formulas in the text layer are usually mangled** → verify suspicious ones against the rendered image.
  Real case: `q = -λ grad T` extracted as `q`, `grad`, `T` on three separate lines.
- **Chat logs / web pages**: read directly; if a share link yields nothing, open it in a browser and read
  the accessibility tree (client-rendered pages usually extract empty).
- **PPT**: `python-pptx` text boxes (including speaker notes); figure-heavy decks go the vision route.
- **Video/subtitles**: get the transcript first, then treat it as text.

#### Scan route: batch the images (**the key point — never one page at a time, serially**)

```
✗ one image per call  → a full model round-trip per page (measured ≈ 8 s) → 110 pages = 14 minutes
✓ three independent images per call → round-trips ÷3, no loss of resolution
```

| Approach | Effect |
|---|---|
| two pages **stitched into one image** | ❌ downsampled to ≈620 px/page, **subscripts and superscripts turn to mush** |
| **three independent images** in one call | ✅ each page keeps full resolution, **round-trips drop to 1/3** |

**"Do not stitch images" ≠ "one page per call".** Take three at a time; if one page fails, re-read that page
alone. **dpi 150 is the sweet spot** — higher gets downsampled downstream anyway.

Prompt: *"Transcribe these pages completely, line by line, page by page, separated by `===== p<N> =====`.
LaTeX for formulas; keep numbering and proofs exactly as printed."*

**Write the transcription straight to `_sources/`** and keep only a page-count summary in the conversation.
The transcription is the single largest artifact you will produce — it must never live in the transcript.

Scripts you write along the way (probes, one-off checks, extraction helpers) are **regenerable**: they never
go into `_sources/`, and for a theory or humanities deliverable you should not be writing verification
scripts at all (Phase 4 explains why).

#### Long jobs: shard across sessions

| Practice | Why |
|---|---|
| **Shard** | 2–4 non-overlapping page ranges, one worker each, files named `pXXX-YYY.md` |
| **Context budget** | flush to disk every 20–30 pages; swap in a fresh session once a worker nears ~200 turns |
| **Coverage reconciliation** | after merging, `scripts/merge_ranges.py` proves every page 1..N is covered (**don't eyeball it**) |
| **Numbering manifest** | end each shard with its list of definition/theorem/example numbers, for cross-checking later |

> ⚠️ **OCR cannot read mathematics.** Measured: ~85 % accurate on printed Chinese prose, but in formula
> regions `$a_i$` becomes `α:`, `=` becomes `二`, subscripts turn to noise. **Verify formulas against the
> vision model or the original image; use OCR only to cross-check numbering.**

### Phase 2 · Structure

**Draw the knowledge-cluster map before writing anything**: which concepts, how they depend on each other,
which is the root, which is a leaf. Then fix the layout
(details: [`references/note-conventions.md`](references/note-conventions.md)):

```
<topic>/
├── 00-overview-and-knowledge-chain.md   ← MOC: chain, responsibilities, learning path, index, FAQ
├── 01-<first concept>.md                ← one knowledge cluster per note, not one slide per note
├── 02-<second concept>.md
├── <next>-cheatsheet.md                  ← printable one-pager (recommended)
├── <next>-errata-and-open-questions.md   ← errors in the source + open questions (recommended)
└── _sources/                            ← transcripts (see Phase 5)
```

**Numbering: one single sequence.** `00` is the overview, the body runs `01`, `02`, … and the cheatsheet and
errata page then take the **next** numbers (`12-cheatsheet.md`, `13-errata-and-open-questions.md` after body
note `11`). Don't reserve high numbers like `98`/`99` — it just makes the folder read out of order; if a later
source adds body notes, renumber these two to the end and let `check_notes.py` catch the links.

**Errata: knowledge-point errors only.** An entry qualifies only if following the source would teach you
something **false** — a wrong formula, a number contradicting its own equation, a conclusion that dropped its
premise, a mis-attributed citation. Typos, fonts, `589` vs `590 nm`, which page is the cover, a truncated
sentence, or a glyph missing from *your own render* (an extraction artifact) earn nothing; trivia gets one
line in the delivery report at most. Open questions still belong here.

Write the `00-overview` skeleton first (title + empty index) and fill it in at the end. It forces the
structure to be right before any prose exists.

### Phase 3 · Write

Start from the template for the subject — [`templates/note-math.md`](templates/note-math.md) ·
[`note-cs.md`](templates/note-cs.md) · [`note-humanities.md`](templates/note-humanities.md) ·
[`topic-note.md`](templates/topic-note.md) — after reading the matching section of
[`references/subject-strategies.md`](references/subject-strategies.md).

**Session discipline (this is where the budget is won or lost):**

- Write each note **to disk in one go**; do not paste its body into the conversation, and do not re-read it
  afterwards (rules 1–2).
- **Every 2–3 notes, start a fresh session** carrying only `00-overview` and the slice of transcript that
  note needs. A single 168-step session costs ~5× what the same work costs as three short ones.
- When you delegate a note to a subagent, hand it the **path** of the transcript slice, not the text, and
  ask for a path plus a ≤3-line summary back.
- Consult `00-overview` for numbering instead of re-reading finished notes.

### Phase 4 · Verify (one pass, bounded — nothing exhaustive)

Machine first, then a small sample. Verification is where a long run silently doubles its cost: in the
measured run, an independent "verifier" agent spent **130 steps and 24 M tokens (38 % of the whole job)**
re-deriving things that a three-item sample would have caught.

**1. Machine check — cheap, mandatory, one command**

```bash
python scripts/check_notes.py <notes-dir>          # exit 0 = clean
```

Eleven checks: frontmatter, `$` pairing, bare `# % &` in math, dead links, leftover placeholders, numbering
gaps *and* duplicates, two-way overview index, empty/too-short files, spaces inside inline math, bare `|`
in a table wikilink, unclosed `$`. If formulas are present, one **batched** render pass that reports only
failures — never a per-formula review.

**2. Subject sample — bounded, mandatory: three items, not thirty**

Pick the **three highest-risk claims** in the deliverable and check only those:

| Type | The three items |
|---|---|
| A · theory | re-derive **one** formula · recompute **one** number **by hand** · confirm **one** formula's conditions |
| B · engineering | run **one** example · reproduce **one** documented error · confirm **one** environment claim |
| C · humanities | verify **one** citation · check **one** hard fact · confirm claims-vs-facts separation |

> **Executable verification is a type-B tool only.** Never write scripts, run programs or paste programme
> output to verify a **theory** or **humanities** deliverable — a derivation is checked by re-deriving it,
> and a script in a physics note teaches nothing while costing the reader attention. The three sampled values
> are recomputed **by hand**: that hand-check is the point, since it is what catches your own slips.

If a sample item fails, widen that one area — do not escalate to exhaustive verification.

**3. Self-containment — 30 seconds**

Read `00-overview` alone. Does the chain make sense without the source material? That is the whole test.

**4. Independent verification — optional and capped**

Only when the delivery is high-stakes or the user asks for it. If you do it: the verifier writes findings
to a **file** and returns **one line** (`N checks, N failures, path`), capped at ~12 tool calls. It must
never re-derive the entire subject, and its findings must never be pasted back into the main conversation.

> **Budget rule**: verification should be **≤20 % of the run's steps**. Over that, you are verifying the
> wrong thing — shrink the sample, not the standard.
>
> **Negative control** (deliberately plant a broken item and confirm the checker reports it): run it **once**,
> when the checker or the note structure changes — **not on every delivery**.

### Phase 5 · Deliver

**① Report statistics, not "all done".** Small tables are fine — do not paste artifacts.

```
✅ Done: <topic>/ — 13 notes (type: A · theory)
   body 8,400 chars · 176 formulas · render check 0 failures · 0 dead links
   Sample verified (A): re-derived eq. (7) ✓ · recomputed 1 value ✓ · conditions checked ✓
   ⚠️ unverified: proof of theorem 5.4 (source omits it; marked ⚠️)
   📁 kept: _sources/ — 39 transcripts (≈4.2 MB)
```

**② Intermediate artifacts — first ask "can this be regenerated?"**

| Category | Examples | Action |
|---|---|---|
| **regenerable** | rendered PNGs, probe scripts, scratch txt | **delete** (cheap to redo) |
| **non-regenerable** | **vision transcripts of a scan**, extracted chat logs | **keep** in `_sources/` (redoing costs tens of minutes and many model calls) |
| **deliverable** | the notes themselves | keep |

> ⚠️ **You must tell the user**: what was kept, why, how much space, and how to delete it. Never keep or
> delete silently.

**③ Clean the workspace**: remove regenerable scratch files and leave the workspace as you found it.

---

## Quick start

```bash
# A. theory  /  B. engineering  /  C. humanities  — same extraction step, different writing strategy
python scripts/extract_material.py <file.pdf> --out _extract/src.txt
#   → cluster map → read the matching subject-strategies.md section → write notes to disk
#   → one short session per 2–3 notes → check_notes.py + a 3-item sample → deliver

# D. scanned material (any subject)
python scripts/extract_material.py <scan.pdf> --render-png _extract/pages/ --dpi 150
#   → three independent images per call → transcription straight to _sources/ → shard → merge_ranges.py
```

A complete worked example lives in [`examples/`](examples/) — a 9-page physics handout (mixed
text/scanned, type A) turned into 8 notes, transcripts kept in `_sources/`.

---

## Known pitfalls (all hit for real)

**Context and cost**
- Re-reading your own artifacts is the single most expensive habit: `read` cost 14.5 M tokens in a 63.9 M
  run — more than every other tool combined. `grep` first, read a window, never the whole file.
- A recursive listing of one repo cost 0.95 M tokens. List one level; measure with `du`, don't print contents.
- Loading this skill's own docs wholesale cost 5.6 M. Read the section you need.

**Formulas and rendering**
- `#` in LaTeX math mode is a **macro-parameter placeholder** and must be `\#`. `$#G$` makes MathJax fail and
  **the whole formula renders as source text**. Watch `%` `&` and bare `_` `^` the same way.
- Inline `$...$` must have **no leading/trailing space** (`$ x $` does not render); block `$$...$$` on its own line.
- **Multi-line** block math inside a blockquote, and math inside callouts, fail to render in Obsidian's editor
  → use inline `$...$` inside blockquotes.
- A wikilink alias inside a table cell must be `[[path\|alias]]`; **in body text it must be `[[path|alias]]`**.

**Material and extraction**
- **PDF bookmarks are not trustworthy**; recover the page offset from running headers; a chapter opener with
  no printed number is inferred from a neighbour ±1.
- Never stitch two pages into one image (downsampled, subscripts lost) — but **three independent images in
  one call is fine**. Do not read "no stitching" as "one page per call".
- Serial page-by-page reading is the biggest time sink (a full round-trip per page); batching + sharding cut
  it by ~3/4.
- When fixing escapes in formulas, **restrict the replacement to formula regions**, or you corrupt Markdown `###`.

**Tools and paths**
- A **non-ASCII (e.g. Chinese) path** makes some tools return zero results → confirm with `ls`/`grep` before
  concluding a file does not exist.
- On Windows, MSYS-style paths (`/c/...`) are often not understood by native programs → pass `C:/...`
  forward-slash paths. **`/tmp/` does not exist on Windows** → use `./_extract/`.
- Interactive CLI confirmation prompts: submit with `\r`, not `\n`.

**Judgement**
- **Source material contains errors** (textbooks, slides and handouts all do). Do not silently fix them —
  record the **knowledge-point** errors on the errata page. That is the most valuable part of the notes.
- Never write "in progress" as "done". The confidence markers exist for exactly this.
- **Do not mistake one subject's practice for a universal rule**: mathematics must not be asked to run every
  exercise, and the humanities must not be asked to run code.

---

## Companion files

| File | Purpose |
|---|---|
| **[`references/subject-strategies.md`](references/subject-strategies.md)** | **★ skeletons, moves, verification and examples per subject (read the matching section before writing)** |
| [`references/note-conventions.md`](references/note-conventions.md) | folder layout, frontmatter, MOC, callouts, ASCII diagrams, self-tests, link syntax |
| [`references/extraction-playbook.md`](references/extraction-playbook.md) | extraction per material type, batch image reading, sharding, context budget |
| [`references/verification.md`](references/verification.md) | the checks in detail: machine checks, sampling, render verification, budgets |
| [`templates/`](templates/) | note skeletons: A / B / C / generic / overview / cheatsheet |
| [`scripts/check_notes.py`](scripts/check_notes.py) | eleven automated note checks (standard library only, exit code = verdict) |
| [`scripts/extract_material.py`](scripts/extract_material.py) | material extraction + extraction-route recon |
| [`scripts/merge_ranges.py`](scripts/merge_ranges.py) | coverage and numbering reconciliation for sharded transcripts |

## Output modes

Default is **obsidian mode** (`[[wikilink]]` + callouts + `$formulas$`). For GitHub or plain Markdown,
switch to **plain mode**: relative links, blockquotes instead of callouts, formulas still in `$...$`.
`check_notes.py --mode plain` skips the Obsidian-only checks.
