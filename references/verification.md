# Verification Handbook

> **"It's organized" is not a conclusion; it is a hypothesis awaiting verification.**
> This handbook lays down which three layers of verification a set of review documents must pass before delivery — **and how much of each is enough** (see §0: verification is bounded, not exhaustive).

```
Layer 1  machine  → syntax, links, rendering (whatever a script can do, never by eye)
Layer 2  subject  → prove the content correct the way this subject "fails when wrong"   ← varies by subject
Layer 3  self-containment  → can it be reproduced from the document alone (proving the reader can use it independently)
```

Only when all three layers pass may you say "done". Miss one and the notes merely "look like" a document.

**Why layer two varies by subject**: mathematics' correctness is guaranteed by **derivation** — you can't "run" a theorem;
engineering's correctness is guaranteed by **execution** — don't run it and you don't know; humanities' correctness is guaranteed by **provenance** — however self-consistent the logic, it can still be
a second-hand claim quoted wrongly. Applying one standard to three kinds of knowledge necessarily under-checks one and over-checks the other.

---

## 0. Budget: verification is bounded, not exhaustive (read this first)

**Verification is where a long run silently doubles its cost.** Measured on one real 168-step run: an
independent "verifier" agent spent **130 steps and 24 M tokens — 38 % of the whole job** — re-deriving the
subject from scratch to confirm what a three-item sample would have caught.

| Rule | What it means |
|---|---|
| **One pass** | Machine check + a **3-item** subject sample + a 30-second self-containment read, then stop. |
| **Sample, don't sweep** | Check the **three highest-risk claims**. If one fails, widen *that* area — never escalate to a full sweep. |
| **≤ 20 % of the run's steps** | Above that you are verifying the wrong thing: shrink the sample, not the standard. |
| **Independent verifier: optional, capped** | Only for high-stakes delivery or on request: ≤ ~12 tool calls, findings written to a **file**, **one line** returned. Its data must never be pasted back into the main conversation — there it is re-billed on every later step. |
| **Negative control: once** | When the checker or the note structure changes — not on every delivery. |

Sections 1–8 below describe **what** each layer looks for. They are a menu, not a licence to check everything.

---

## 1. Machine self-check (layer one)

```bash
python scripts/check_notes.py <notes-dir>
python scripts/check_notes.py <notes-dir> --json       # CI / pre-commit
python scripts/check_notes.py <notes-dir> --mode plain  # non-Obsidian output
```

Eleven checks:

| # | Check | Why it matters | Level |
|---|---|---|---|
| C1 | frontmatter contains `tags`/`created`/`source` | without `source` there is no way to trace back and verify | warn |
| C2 | `$` pairing (inline / block); recognize a **literal dollar sign** taken as a formula | one missing `$` turns **a whole passage** into a formula | error |
| C3 | bare `#` `%` `&` inside a formula region | the entire formula fails to render (see section 4) | error |
| C4 | link targets exist (**skip frontmatter**) | a dead link = a hole in the graph = a lost reader | error |
| C5 | leftover placeholders | `TODO`/`TBD` slipped into the deliverable | warn |
| C6 | numbering continuity: **missing numbers + duplicate numbers** | a missing number usually means a dropped piece; a duplicate makes a link point to an ambiguous target | warn |
| C7 | `00-overview` index vs. what is actually on disk (**both directions**) | the overview is the entry point; out of sync equals nonexistent | warn |
| C8 | empty / too-short files | created but never written | warn |
| C9 | leading / trailing space in inline formulas | `$ x $` does **not render** in Obsidian | error |
| C10 | a wikilink with a bare `\|` inside a table | a bare `\|` tears the table apart | error |
| C11 | `$` scattered across several lines within a paragraph with an even total | a cross-line inline formula (doesn't render), or several literal `$` merging into one line pair up wrongly | error |

> **Why C4 skips frontmatter**: the `related:` / `source:` fields by design may reference notes **not yet created**
> (planning first and filling in later is a normal flow). Treating them as dead links produces guaranteed false positives — and once false positives pile up,
> nobody looks at the real dead links.

> **Why C2 can recognize a literal `$`**: the same failure hits CJK prose hard — in Chinese, `$` commonly trails a number with no space — so a sentence like
> `the price is 100$ and the surcharge is 200$` gets matched by the inline-formula regex as `$ and the surcharge is 200$`.
> If you simply report "there are spaces at the ends", the user goes and deletes the spaces — **the direction is entirely wrong**;
> the real problem is that the literal dollar sign should be escaped as `\$`.

Exit codes: `0` all pass · `1` has errors · `2` warns only.

### The checker must be checked too (negative control)

**Run this once** — when the checker, the note structure or the templates change. It does **not** belong in
every delivery (see §0).

**When it reports 0 errors, deliberately insert a bad formula and see whether it reports.** Otherwise "0 errors" may just mean the detector is broken.

```bash
# Negative control: temporarily add a bad formula, confirm the script errors, then remove it
mkdir -p ./_probe && cp 01-*.md ./_probe/         # use a relative path; /tmp/ does not exist on Windows
printf '\n$#G$\n' >> ./_probe/01-test.md
python scripts/check_notes.py ./_probe/            # expected: C3 ERROR
rm -rf ./_probe
```

Seeding a single fixture that covers all 11 checks at once is more economical — that is how this project was developed (see `CHANGELOG.md`).
**If the detector itself has never been verified, "0 errors" is not a conclusion.**

---

## 2. Subject check (layer two, varies by subject)

### A Theory (math / physics / chemistry / statistics)

Correctness is guaranteed by **derivation**. **No full actual run** — there is no such thing as "running a theorem".

| Action | Notes |
|---|---|
| **Formula rendering check (required)** | Compile every formula through MathJax/KaTeX; see section 4 |
| **Derivation-chain self-check** | At every "=", ask: what is the justification? Which theorem / condition did this step use? |
| **Sample and recheck 3–5 key values** | Recompute the sampled points with sympy/numpy, catching **systematic** arithmetic tendencies (sign errors, constant errors) |
| **Completeness of applicability conditions** | For every formula / theorem: are the conditions all written? Is the equality condition written? |
| **Counterexamples and boundaries** | Remove some condition — does the conclusion still hold? Write the counterexample into the notes |
| **Numbered cross-check** | See section 3 (required when a numbering system exists) |

**Why sample rather than recompute everything**: an error in a theory document is usually "a step of reasoning is wrong", not "a step of arithmetic is wrong"; sampling catches systematic arithmetic tendencies (say, treating $\ln$ as $\log_{10}$ all the way down),
while reasoning errors can only be found by the derivation-chain self-check.

**Physics has two extra free rulers**: the dimensional check (the two sides of an equation must have the same dimension) and limit regression (at $v \ll c$ it should degrade back to the classical conclusion).

### B Engineering (programming / networks / operating systems / databases / electronics)

Correctness is guaranteed by **execution**.

| Action | Notes |
|---|---|
| **Actually run (required)** | Run each example for real and **paste the output as-is** (not "it should output …") |
| **Copy-test** | Copy only the notes' code (not your own scaffolding) into a clean environment — does it reproduce the same output? |
| **Environment annotation (required)** | OS / runtime version / dependency versions / engine / charset, written beside the conclusion |
| **Error reproduction verification** | For an error written in the notes, trigger it once for real — against "inventing an error from memory" |
| **Write conclusions conditionally** | "measured on A; not tested on B, may differ" |

**Why the copy-test cannot be skipped**: the answers in the notes were often produced with **your own** build script / config file,
while the reader copies only those few lines in the notes. One missing `INSERT` and it derails.
**The final verification method: run the code in the notes directly.**

### C Humanities (history / philosophy / law / literature / social science)

Correctness is guaranteed by **provenance**. **No actual run.**

| Action | Notes |
|---|---|
| **Source completeness (required)** | Cite a page for every assertion; distinguish **primary** from **secondary**, and a second-hand citation must say who it is quoted from |
| **Term / name consistency** | The same personal name or concept must be written the same way across the whole set of notes (keep a mapping table) |
| **Backbone self-test** | Cover the expansion; can the 3–7 backbone points alone recite the whole piece? |
| **Claim–fact separation self-check** | A scholar's claim must be written as "X argues …"; **writing a claim as a fact is the most serious distortion** |
| **Spot-check 3–5 hard facts externally** | Dates, personal names, places, treaty titles — the easiest to propagate wrongly; spot-check against authoritative sources |

**Why "spot-check" rather than check everything**: much of the material in humanities cannot be verified one-click against an external source (claims, interpretations,
evaluations). Spend the effort on **falsifiable hard facts**, and let source citations let the reader judge the rest.

### Mixed types

Split by piece; each piece uses its matching strategy. A programming unit in a math textbook: main body follows A, code blocks follow B.

### Number and material re-verification (common to all subjects; intensity set by subject)

| Subject | Intensity |
|---|---|
| A Theory | **Three** key values, recomputed **by hand** (catch systematic arithmetic tendencies) |
| B Engineering | **Full** actual run, output reconciled item by item — the only type where running a programme is evidence |
| C Humanities | Not applicable → instead spot-check hard facts (dates / names / places) externally |

**Bound the sample; never sweep every number.** Three values, picked where an error would change a
conclusion. A sweep of every number in the notes is exactly the exhaustive verification §0 rules out, and for
a **theory** deliverable a script is not stronger evidence than a careful hand-check — it is weaker, because
the reader cannot follow it. Run code only in **type B**, where execution *is* the subject:

```python
# Type B only: reconcile one documented result against a real run
claimed = 56.96                                   # value as printed in the note
actual = run_sql("SELECT AVG(Grade) FROM SC")     # one query, not a sweep
assert abs(claimed - actual) < 0.01, f"doc {claimed} vs computed {actual}"
```

**Measured payoff**: for notes from a 306-page slide deck, re-verification caught **4 hand-calculation errors**
(`52.28`→`56.96`, comparison row `7`→`9`, affected row `16`→`9`, total rows `32`→`33`).
The error rate of mental arithmetic is astonishingly high.

At the same time, re-verify **the material itself**: wherever a run disagrees with the material, the material is wrong. Record it on the errata page (`<next>-errata-and-open-questions.md`):

**Only knowledge-point errors get an entry.** It qualifies only if following the source would teach you
something **false** — a wrong formula, a number contradicting its own equation, a conclusion that drops its
premise, a mis-attributed citation. Typos, fonts, `589` vs `590 nm`, which page is the cover, a truncated
sentence, or a glyph missing from your own render are **not** errata: the last one is an extraction artifact
and belongs in the extraction log, if anywhere. Trivia earns at most one line in the delivery report.

```markdown
## Errata in the source material

| # | Location | Original text | Problem | Correct form |
|---|---|---|---|---|
| 1 | Example 3.48 | `HAVING Grade>=90` | `HAVING` references a non-grouped column | `HAVING AVG(Grade)>=90` |
| 2 | p19 | `WHERE Grade = NULL` | NULL cannot be compared with `=` | `WHERE Grade IS NULL` |
```

> This table is **often the single most valuable page in the whole set of notes** — it records the places where "learning straight from the book teaches you wrong".
> But note: **don't silently fix the original book**; keep a record of "where the original was wrong".

#### Cross-environment conclusions must state the environment

```markdown
✅ Verified: SQLite 3.50.4 (Windows) — `GROUP BY` may select a non-grouped column
📖 Documented: MySQL 8.0 with the default `ONLY_FULL_GROUP_BY` raises ERROR 1055
⚠️ Unverified: PostgreSQL behavior not tested
```

"Measured on A" does not equal "the same on B". The version number must be written clearly.

---

## 3. Numbered cross-check

**Used for: material that carries numbering (definition / theorem / example / formula) and has gone through OCR or visual transcription.** Applies to any subject.

Purpose: answer "**did a whole item get dropped**". This is the failure mode manual reading most easily overlooks —
you read it through and think "it's complete", when in fact the definition at 4-4 was eaten by OCR.

```python
import re
ocr = open('ocr_dump.txt', encoding='utf-8').read()
notes = open('04-relational-operations.md', encoding='utf-8').read()

flat_ocr   = re.sub(r'[\s\-,]', '', ocr)     # strip whitespace, hyphens and commas before matching
flat_notes = re.sub(r'[\s\-,]', '', notes)

def ids(text, kw):
    return sorted({int(m.group(1)) for m in re.finditer(kw + r'(\d{1,2})', text)})

for kw in ['Definition', 'Theorem', 'Example']:
    a, b = set(ids(flat_ocr, kw)), set(ids(flat_notes, kw))
    print(f"{kw}: OCR={sorted(a)}")
    print(f"     notes={sorted(b)}")
    if a - b: print(f"  ⚠️ in OCR but not in notes → likely dropped: {sorted(a - b)}")
    if b - a: print(f"  ℹ️ in notes but not in OCR → OCR miss, recheck the original image: {sorted(b - a)}")
```

How to read the result:

| Direction | Meaning | Handling |
|---|---|---|
| **OCR has it, notes don't** | **Danger signal** — it may really be missing | Must go back to the original page, confirm, and add it |
| Notes have it, OCR doesn't | OCR missed it (very common) | Go back to the original image; confirming it exists is enough |

> Think in reverse: if the notes are "more" than the OCR but **the notes are right** (you checked against the original), then the OCR is unreliable —
> which is exactly why the rule "formulas and numbers always go back to the original image for verification" holds.

**What if there is no OCR**: have each transcription shard's worker append the list of numbers in its range to the end of the transcript,
then reconcile after merging with `scripts/merge_ranges.py`. See [`extraction-playbook.md`](extraction-playbook.md).

---

## 4. Formula rendering verification

**Don't rely on the eye alone.** Actually compile every formula with MathJax/KaTeX.

```bash
npm install mathjax-full
```

```js
// check_math.mjs — usage: node check_math.mjs <notes-dir>
import fs from 'fs';
import path from 'path';
import {mathjax} from 'mathjax-full/js/mathjax.js';
import {TeX} from 'mathjax-full/js/input/tex.js';
import {SVG} from 'mathjax-full/js/output/svg.js';
import {liteAdaptor} from 'mathjax-full/js/adaptors/liteAdaptor.js';
import {RegisterHTMLHandler} from 'mathjax-full/js/handlers/html.js';
import {AllPackages} from 'mathjax-full/js/input/tex/AllPackages.js';

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const doc = mathjax.document('', {
  InputJax: new TeX({packages: AllPackages}),
  OutputJax: new SVG({fontCache: 'none'}),
});

const dir = process.argv[2];
let total = 0, bad = 0;
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.md'))) {
  const text = fs.readFileSync(path.join(dir, f), 'utf8');
  // inline $...$ and block $$...$$ (inline formulas deliberately don't span lines: line-crossing
  // ones Obsidian won't render either, and that missed case is reported by check_notes.py's C11)
  const re = /\$\$[\s\S]+?\$\$|\$[^$\n]+?\$/g;
  let m, i = 0;
  while ((m = re.exec(text))) {
    i++;
    const isBlock = m[0].startsWith('$$');
    const tex = m[0].slice(isBlock ? 2 : 1, isBlock ? -2 : -1);
    total++;
    const html = adaptor.innerHTML(doc.convert(tex, {display: isBlock, em: 16, ex: 8, containerWidth: 1200}));
    if (html.includes('merror')) {                 // (1) fatal syntax error
      bad++; console.log(`[ERROR] ${f} formula #${i} merror: ${tex.slice(0, 60)}`);
    } else if (/fill="red"/.test(html)) {          // (2) unknown command/symbol (red but no merror)
      bad++; console.log(`[WARN ] ${f} formula #${i} unknown command: ${tex.slice(0, 60)}`);
    }
  }
}
console.log(`\nformulas ${total} · failed ${bad}`);
process.exit(bad ? 1 : 0);
```

### Negative-control table (must read)

When the checker reports 0 failures, you **must** confirm it isn't broken. Known behavior:

| Input | MathJax behavior | Detectable |
|---|---|---|
| `a^{#G}` | `merror` | ✅ detected |
| `\foobar{x}` | red mtext, **no merror** | ⚠️ must check `fill="red"` |
| `f(x = y` (unbalanced parens) | auto-closed, no error | ➖ not a problem |
| `\text{CJK}` | normal | ➖ legal |

### The most fatal pitfall: `#` inside a formula

**Symptom**: in Obsidian an **entire** block formula displays as source, while the inline formulas beside it render normally.

**Root cause**: in LaTeX math mode, `#` is a **macro parameter placeholder** and must be written `\#`:

- `$\#G$` → displays `#G` normally
- `$#G$` → MathJax reports `You can't use 'macro parameter character #' in math mode`, and **the whole formula fails to render**

High-risk areas: group order `#G`, set cardinality `#A`, numbering reference `#1`. Same-class risky characters: `%` (comment), `&` (alignment),
bare `_` `^` (outside `\text{}`), `$` itself.

**Fix script** (touch only formula regions, to avoid damaging markdown `###` headings):

```python
import re
PAT = re.compile(r"\$\$.+?\$\$|\$[^$\n]+?\$", re.S)

def fix_formula_hashes(text):
    def fix_block(b):
        tmp = b.replace('\\#', '\x00')            # protect already-escaped \#
        return tmp.replace('#', '\\#').replace('\x00', '\\#')
    return PAT.sub(lambda m: fix_block(m.group(0)) if '#' in m.group(0) else m.group(0), text)
```

**Regression**: after the fix you must rerun the full MathJax compile.

### Escape order in a local preview generator (error-prone)

When writing an md→HTML preview, **first extract formulas into placeholders, then escape the body, and finally substitute the SVGs back in**:

```js
s = s.replace(/\$([^$]+?)\$/g, (m, x) => { ph.push(mj(x, false)); return '\u0001' + (ph.length-1) + '\u0001'; });
s = esc(s);   // if you esc first: a < inside a formula becomes &lt;, and MathJax renders the & as a black block
```

---

## 5. Mermaid diagram verification

If a dependency graph (the knowledge chain in `00-overview`) has a syntax error, Obsidian silently shows it as a code block.

**Offline approach**: Obsidian ships its own mermaid; pull `mermaid.min.js` straight out of its `obsidian.asar` and use it —
verification results match Obsidian **exactly** (more reliable than installing a node package).

```python
# extract mermaid.min.js out of the asar
import struct, json
with open(r'<obsidian-install-dir>/resources/obsidian.asar', 'rb') as f:
    _, _hs, _, js = struct.unpack('<IIII', f.read(16))   # ⚠️ the asar header is 16 bytes; don't read(4) first
    tree = json.loads(f.read(js).decode('utf-8', 'ignore'))
    data_start = 16 + js
    ent = tree['files']['lib']['files']['mermaid.min.js']
    f.seek(data_start + int(ent['offset']))
    open('mermaid.min.js', 'wb').write(f.read(int(ent['size'])))
```

> **This pitfall deserves its own note**: the asar header is `UInt32×4 = 16` bytes. If you write `f.read(4)` + `f.read(16)`,
> you read 4 bytes too many and the JSON starts at the wrong offset → parsing fails or yields garbage. Measured on this machine (Obsidian's asar,
> 24 MB), the four fields are `(4, 91932, 91928, 91924)`; reading 16 bytes directly parses out
> `lib/mermaid.min.js` (2.57 MB, mermaid@11).

```js
// Validate each diagram: a syntax error throws
for (const src of diagrams) {
  try { await mermaid.parse(src); }
  catch (e) { console.log('[ERROR] mermaid syntax error:', e.message); }
}
```

Or render with `await mermaid.render(id, src)` and visually confirm the layout is sensible.

---

## 6. Self-containment verification (layer three)

**Prove a reader can reproduce it independently.** This layer doesn't ask "is the content right" but "**can someone else use it**".

### 6.1 Subject-specific retelling test

| Subject | How to test | Pass criterion |
|---|---|---|
| A Theory | **Cover the derivation**; from the statement and the example conditions alone, can you redo it yourself? | You can reproduce the key derivation independently |
| B Engineering | **Copy-test** (see 2.B): copy only the document's code, don't run your own scripts | Same input → same output |
| C Humanities | **Backbone self-test**: cover the expansion; can the 3–7 backbone points recite the whole piece? | The backbone holds together |

> A lesson from practice: the answers I wrote in a SQL note were produced with **my** build script;
> a reader, however, copies only the SQL in the notes. If the two disagree (I forgot to copy one `INSERT` into the notes), it derails.
> Final practice: **run the SQL in the notes directly**.

### 6.2 Blind-read test

Send one note on its own (or have a model with no context read it) to someone who has never seen the source material, and ask three questions:

1. What is this about? (checks whether there is a lead)
2. Why is the Nth concept needed? (checks the "why you need it" section)
3. What is X mentioned here? (checks whether a term is explained at first occurrence)

Can't answer = not self-contained = go back and fill it in.

### 6.3 First-occurrence term check

```bash
# scan a note for unexplained abbreviations
grep -oE '\b[A-Z]{2,6}\b' 03-single-table-queries.md | sort -u
# check each one: is the full form given at first occurrence?
```

---

## 7. Delivery report

**Report statistics, not "done".** Only concrete numbers are verifiable:

```markdown
✅ Done: <topic>/ — 13 notes (type: A · theory)
   00-overview + 11 body notes + 12-cheatsheet + 13-errata
   body total 8,400 chars · 176 formulas · render check 0 failures · 0 dead links
   2 mermaid dependency graphs, all parse
   subject sample (A): 1 formula re-derived ✓ · 3 key values recomputed by hand ✓ · conditions checked ✓
   ⚠️ Unverified: proof of theorem 5.4 (the textbook skips it; marked ⚠️)
   Open questions: one boundary case (recorded on the errata page)
   📁 Kept: 39 transcription files in _sources/ (~4.2 MB; deleting them means rerunning the whole extraction chain)
```

**This report is itself quality evidence.** It exposes "the parts not done" at the same time — which is exactly where credibility comes from.

---

## 8. Pre-delivery checklist

```
[ ] check_notes.py exits 0 (or has errors that have been confirmed acceptable)
[ ] formulas compiled in ONE batched pass, failures only reported (not a per-formula review)
[ ] mermaid parses (skip if there is none)
[ ] subject sample done: THREE highest-risk items (A sample / B actual run / C sources) — three, not thirty
[ ] self-containment: the 30-second read of 00-overview alone was done
[ ] unverified items marked ⚠️ / 📖; open questions recorded on the errata page
[ ] verification stayed within budget (≤ ~20 % of the run's steps)
[ ] intermediate artifacts disposed of by "regenerable / non-regenerable", and **the user was told** what was kept
[ ] regenerable temp files cleaned up; the workspace restored
```

Dropped from this checklist on purpose (they belong to development, not to each delivery):

```
✗ negative control per delivery        → run it once, when the checker changes
✗ exhaustive numbered cross-check      → covered by check_notes.py C6 (gaps + duplicates)
✗ per-formula render review            → one batched pass, failures only
✗ a separate verifier agent            → optional; the writer runs the 3-item sample inline
✗ term-by-term first-occurrence sweep  → covered by 00-overview self-containment read
```
