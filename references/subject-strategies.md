# Three Subject Strategies

> **Knowledge differs by subject, so notes should not all look the same.**
> A theorem in mathematics, a piece of C code, and having "learned" a historical event are three completely different things.
> This file lays down: once material is in hand, first decide which category it belongs to, then apply the matching strategy.

---

## Step 0 · Decide the type

| Type | Typical material | Characteristics | Go to |
|---|---|---|---|
| **Theory** | Mathematics, physics, chemistry, statistics, economic theory | Definitions / theorems / formulas / derivations / proofs dominate; correctness is guaranteed by **logic** | [A](#a-theory-math--physics--chemistry--statistics) |
| **Engineering** | Programming, computer networks, operating systems, electronics, databases | Has executable code / commands / configuration; correctness is guaranteed by **execution** | [B](#b-engineering-computer-science--networks--electronics) |
| **Humanities** | History, philosophy, law, literature, linguistics, social science | Concepts / claims / threads / schools / cases dominate; correctness is guaranteed by **provenance** | [C](#c-humanities-history--philosophy--law--social-science) |

**Mixed types are common** — don't force-fit a single one:

| Mixed case | How to handle |
|---|---|
| MATLAB / Python lab units in a mathematics textbook | Main body follows A; handle the code parts as B (actually run + annotate the environment) |
| Protocol formulas and derivations in a computer-networking textbook | Main body follows B; handle the formula parts as A (state applicability conditions) |
| An economics textbook (models + data + history of ideas) | Apply per chapter; note each piece's type in `00-overview` |
| One conversation / one slide deck spanning several subjects | **Split by piece**; keep each piece internally consistent |

**Rule of thumb**:
> What happens if this is **wrong**? — the logic won't go through (A) / it won't run (B) / no source can be found (C).
> That is its core strategy.

---

## A. Theory (math / physics / chemistry / statistics)

### What "learning" means for this kind of knowledge

Not memorizing the conclusion, but: **being able to derive the conclusion independently, and knowing under which conditions it holds and under which it fails.**

A proof in a mathematics textbook matters because the "reusable thinking moves" are hidden in each step of the proof —
substitution, induction, bounding, change of basis. **Copying only the conclusion means learning nothing at all.**

### Note skeleton (in order)

| # | Section | Required | Notes |
|---|---|---|---|
| 1 | **Objects and notation** | ✅ | The definitions this piece involves; **a symbol must be defined the first time it appears** |
| 2 | **Statement of the proposition** | ✅ | The theorem / formula **stated in full** (conditions + conclusion), not the conclusion alone |
| 3 | **Derivation / proof** | ✅ | Keep the key steps; **justify every step** (see below) |
| 4 | **Applicability conditions and equality** | ✅ | The range in which the formula holds; the conditions for equality / for taking an extremum |
| 5 | **Worked examples** | ✅ | Open each example with a "**when to use**" line |
| 6 | **Variants and counterexamples** | ✅ | What happens when a condition is removed; one problem many solutions / many problems one solution |
| 7 | **Common mistakes** | ✅ | Misused notation, omitted conditions, computational traps |
| 8 | **Relations** | ✅ | Dependencies on upstream / downstream theorems (which implies which, which is a special case) |

### The eight moves (this is the entire craft of theory)

#### 1. Justify every step of the derivation

This is the only criterion that separates **useful notes** from **transcription**.

```markdown
$$
\begin{aligned}
|A - \lambda I| &= \begin{vmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{vmatrix} \\
&= (2-\lambda)^2 - 1 && \text{← 2x2 determinant: diagonal rule} \\
&= (\lambda-1)(\lambda-3) && \text{← factorization}
\end{aligned}
$$
```

**Check**: three months from now, when you look at the step `(2-\lambda)^2 - 1`, can you immediately recall why? If not, fill it in.

#### 2. Record a formula as the "formula trio"

The formula proper **+ applicability conditions + equality / extremum condition**. A formula missing the last two is **dangerous** — it will fail in places you don't realize.

```markdown
| Formula | Applicability conditions | Equality holds |
|---|---|---|
| $a+b \geqslant 2\sqrt{ab}$ | $a,b \geqslant 0$ | $a=b$ |
| Unbiasedness of $\bar{x}$ | Samples are i.i.d. | — |
```

> Mathematics' "verification" is **plugging boundary values into the formula to see whether it still holds**.

#### 3. Open each example with "when to use"

> **Use when**: the integrand contains "a function × its derivative" → substitution (let $u$ be the inner function)
> **Use when**: you see "for any $\varepsilon > 0$, there exists $N$" → this is the phrasing of the limit definition; lean on the definition

This line is worth more than the example itself — it decides whether, in an exam, you **can recall which tool to use**.

#### 4. One problem, many solutions / many problems, one solution

| Angle | How | Value |
|---|---|---|
| **One problem, many solutions** | Give 2–3 routes for the same problem and compare their cost | Spot the invariant (which route is shorter, and why) |
| **Many problems, one solution** | Group problems scattered across the text under a single method | Form the "applicability domain of the method" |

#### 5. Counterexamples and condition boundaries

After every theorem, follow up with: **"remove some condition — does the conclusion still hold?"**

```markdown
> [!warning] Conditions cannot be dropped
> $AB = O \nRightarrow A = O$ or $B = O$. Counterexample: $A = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$,
> $B = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}$, $AB = O$ but neither is zero.
```

#### 6. Physics-only: the dual check of dimensions and limits

Physics formulas come with two free automatic rulers:

- **Dimensional check**: the two sides of the equation must have the same dimension ($F = ma$: $\mathrm{N} = \mathrm{kg\cdot m/s^2}$ ✓)
- **Limit regression**: push a parameter to an extreme ($v \ll c$, $r \to \infty$, $\hbar \to 0$) and see whether it degrades into a known classical result

Both can be done without leaving your desk, and they catch the vast majority of slips. **Write them into the notes.**

#### 7. Relation graph (what the boss means by "relations")

Theorems are not flat. Use a dependency graph to express "who depends on whom":

```text
              Properties of determinants
                           ↓
        Cramer's rule ──→ Structure of solutions
                                    ↑
                           Rank of the matrix ←── Elementary row operations
```

Put it in the knowledge chain of `00-overview`, and mark each theorem in its own piece as `**depends on** / **used by**`.

#### 8. Notation table

The most common failure in math notes is **notation drift** — the same symbol meaning different things in different pieces.
If a piece introduces new notation, list it at the top:

| Notation | Meaning | Note |
|---|---|---|
| $r(A)$ | rank of the matrix $A$ | uniform throughout |
| $A^*$ | adjugate matrix | distinguish it from the conjugate transpose (this textbook doesn't use $A^H$) |

### Verification (theory is not actually run)

| What to do | Why |
|---|---|
| **Formula rendering check** (required) | `#` `%` `&` make an entire formula display as source code; in math notes this is fatal |
| **Derivation-chain self-check** | Does every step have a justification? Is there a skipped step that makes it unreconstructable? |
| **Key-value spot check** (recommended: **three** values) | Recheck three key values **by hand** to catch arithmetic slips. No sweep, and **no script** — see the note below |
| **Completeness of applicability conditions** | Is every formula's conditions written out in full? |
| **Mathematical notation consistency** | The same symbol means the same thing throughout |
| **Numbered cross-check** | Are any of the source's definition / theorem / example numbers missing? |

> **Execution is not a theory tool.** Theory's correctness rests on the derivation, so a `sympy`/`numpy`
> script is not stronger evidence than a careful hand-check — it moves the work somewhere the reader cannot
> follow, and it tempts you into sweeping every number. Recheck three values on paper; the sample exists to
> catch **systematic** error tendencies (say, you always slip on signs) and to give the reader a rehearsal.
> **Code, "ran it" blocks and script output do not belong in a theory note at all** — running programmes is
> the type-B craft, not this one.

### Common pitfalls

- **Copying conclusions and dropping the process**: mathematics' soul is in the derivation; a note with no process can't reconstruct the reasoning at review time
- **Formulas without applicability conditions**: forgetting $a,b \geqslant 0$ for $a+b \geqslant 2\sqrt{ab}$ → you get it wrong on the exam
- **Skipping steps in a proof**: what you omit is usually exactly the "leap of thought" — and that is what you need to remember
- **No justification**: three months later you recognize every step but can't say why this step
- **Examples without "when to use"**: you can recognize it but can't use it
- **Physics without a dimensional check**: a free debugging tool left unused
- **Treating theory as engineering**: writing scripts, pasting programme output, or claiming "verified by running it" in a maths/physics note. It proves nothing about a derivation and buries the reasoning — execution belongs to type B

---

## B. Engineering (computer science / networks / electronics)

### What "learning" means for this kind of knowledge

Not memorizing the API, but: **being able to run it in your own environment, knowing where it went wrong when it fails, and knowing whether a different environment changes it.**

> The essence of engineering knowledge in one sentence: **"it runs" is the only judge, and "in whose environment it runs" is the second judge.**

### Note skeleton (in order)

| # | Section | Required | Notes |
|---|---|---|---|
| 1 | **What problem it solves** | ✅ | How people suffered without it (motivation drives memory) |
| 2 | **Minimal runnable example** | ✅ | Copy-paste and it runs; **paste the output as-is** |
| 3 | **Mechanism** | ✅ | Why this works (not just how to use it) |
| 4 | **Error analysis** | ✅ | Typical error + root cause + fix (see below) |
| 5 | **Environment and version differences** | ✅ | What your environment is; what changes in another |
| 6 | **Boundaries and traps** | ✅ | What input blows up, what style is a trap |
| 7 | **Variants / alternatives** | ⬜ | How to write it another way, cost comparison |
| 8 | **Cheatsheet** | ⬜ | One table of common commands / APIs |

### The six moves

#### 1. Actually run it, and paste the output as-is

Engineering **must** be actually run — this is the subject's core strategy (not a universal iron rule).

```markdown
```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t(a INTEGER, b INTEGER)")
con.execute("INSERT INTO t VALUES (1, NULL), (2, 3)")
print(con.execute("SELECT COUNT(*), COUNT(b) FROM t").fetchone())
```

```text
(2, 1)          ← actual output (SQLite 3.50.4 / Windows / 2026-10-06)
```
```

If it won't run, it disagrees with the material; disagreement means the material is wrong (very common) — record it on the errata page.

#### 2. The error analysis block (the most valuable part of engineering)

One real debugging session has more teaching value than ten successful examples. Use a fixed template:

```markdown
> [!bug] Error: `sqlite3.OperationalError: near "WITH": syntax error`
> - **Scenario**: `CREATE VIEW ... WITH CHECK OPTION` on SQLite
> - **Root cause**: SQLite does not support `WITH CHECK OPTION` (this is not a syntax mistake)
> - **Confirmed**: `SELECT sqlite_version()` → 3.50.4; the official docs state the clause is unsupported
> - **Fix**: switch to `CREATE TRIGGER`, or validate at the application layer
> - **Lesson**: **an error saying "syntax error" does not mean the syntax is wrong** — it may be that "this engine simply doesn't support the feature"
```

Four elements, none optional: **scenario → root cause → how you confirmed it → lesson**.

#### 3. The environment matrix (the mirror for "it runs on my machine")

The same code behaves differently in different environments — the most expensive trap in engineering:

| Item | This environment | What a difference affects |
|---|---|---|
| OS | Windows 11 / WSL2 Ubuntu 22.04 | path separators, line endings, filesystem case sensitivity |
| Runtime | Python 3.12.14 | no `match` statement below 3.10 |
| Dependency | numpy 2.3.5 | `np.float_` removed as of 2.0 |
| DB engine | SQLite 3.50.4 | doesn't support `ANY` / `ALL` / view CHECK OPTION |
| Charset | UTF-8 | Chinese paths and emoji error out under some locales |

**Write conclusions conditionally**: "measured on A; not tested on B, may differ" — don't write it as universally true.

#### 4. Minimal reproduction

When debugging, the most valuable thing is not "the complete code" but **the smallest fragment that reproduces the problem**.
Keep the minimal reproduction in the notes, not the big blob of engineering code from that moment.

#### 5. Copyable commands

Shell commands must be **complete and directly pasteable**, including the necessary `cd`, environment variables, and arguments:

```bash
# ✗ incomplete form often seen in notes
python extract.py --dpi 150

# ✓ directly copyable
cd /d/project && python3 -m venv .venv && .venv/Scripts/python extract.py scan.pdf --dpi 150
```

#### 6. Complexity and cost (if relevant)

| Style | Time complexity | Applicable scale |
|---|---|---|
| Nested loops | $O(n^2)$ | n < 1000 |
| Hash table | $O(n)$ | any |

### Verification (engineering = actually run + annotate the environment)

| What to do | Why |
|---|---|
| **Actually run every example** (required) | Only execution can prove code is correct |
| **Copy-test** | Copy only the notes' code (not your own scripts) — does it reproduce the same output? |
| **Environment annotation** (required) | Every "measured" conclusion must carry version / OS / date |
| **Error reproduction** | For an error written in the notes, trigger it once for real and confirm the error text is verbatim |
| **Link and rendering check** | As in the general terms |

### Common pitfalls

- Writing "I tried it and it worked" as a universal conclusion → you must add the environment
- Pasting only the first half of an error → paste the full error plus context
- Recording only the happy path, not the traps → a debugging record is worth far more than a success record
- Code snippets missing context (imports, prior state) → can't be copied and run
- Ignoring **versions**: APIs can change in every release

---

## C. Humanities (history / philosophy / law / social science)

### What "learning" means for this kind of knowledge

Not memorizing every detail, but: **remembering the backbone skeleton, being able to locate things again quickly when needed, and telling "who said what, from which position".**

Humanities material is voluminous, dense in detail, and **mixes claims with facts**. So the strategy's center of gravity is:
**extract the backbone → classify and generalize → make it retrievable → cite sources and positions.**

### Note skeleton (in order)

| # | Section | Required | Notes |
|---|---|---|---|
| 1 | **One-sentence thesis** | ✅ | What this material sets out to argue |
| 2 | **Backbone skeleton** | ✅ | 3–7 points, one sentence each (memorizable) |
| 3 | **Expansion** | ✅ | The arguments, examples, and data under each point |
| 4 | **Concept discrimination** | ✅ | A comparison table of easily confused concepts |
| 5 | **People / events / chronology table** | ⬜ | Depends on the subject, see below |
| 6 | **Schools and debates** | ⬜ | Who opposes whom, where the disagreement lies |
| 7 | **Sources** | ✅ | Every assertion cites its source (page / reference) |
| 8 | **Self-test** | ✅ | Cornell-style cue questions |

### The six moves

#### 1. Backbone first (skeleton before flesh)

**Write 3–7 backbone points first, one sentence each**, then hang details under each.
At review time read the backbone first; only once you can recite it, move on to the details.

```markdown
> [!abstract] This section's backbone (memorize this first)
> 1. Cause: contradiction X intensifies
> 2. Turning point: event Y shifts the balance of power
> 3. Outcome: pattern Z takes shape
> 4. Dispute: scholarship splits into camps A/B over Z's characterization
```

**Test**: cover the expansion, look only at the backbone — can you explain this section to someone else?

#### 2. Classify and generalize (regroup by "useful dimensions", not by the book's table of contents)

A textbook's chapter order serves lecturing, not retrieval. Reorder by the dimension you will use:

| Regrouping dimension | Applies to | Example |
|---|---|---|
| Timeline | history, intellectual history | a chronology of events |
| School / position | philosophy, literary criticism | each school's different answer to the same question |
| Theme | social science, law | group by "question", not by "chapter" |
| Point of contention | fields with disagreement | pro / con / evidence |
| Level | institutions, statutes | general provisions → specific provisions |

In `00-overview`, place a **multi-dimensional index**: the same content findable by either dimension.

#### 3. Concept comparison table (humanities' biggest memory burden)

```markdown
| Aspect | Concept A | Concept B |
|---|---|---|
| Core claim | …… | …… |
| Proposer / era | …… | …… |
| Key difference | **state the difference in one sentence** | |
| Common confusion | what wrong conclusion the confusion leads to | |
```

#### 4. People–events–chronology table (the hard-core, retrieval-friendly part)

| Person | Identity | Claim | Related note |
|---|---|---|---|
| …… | …… | …… | <link to the related note> |

This is one of the **most frequently used** retrieval entry points in humanities notes.

#### 5. Source tracing (humanities' "verification")

Theory rests on derivation, engineering on execution; **humanities rest on sources**.

```markdown
> Weber argues that the Protestant ethic gave rise to the spirit of capitalism [^1].
> But this claim has been questioned from several sides, e.g. … [^2]
>
> [^1]: Weber, *The Protestant Ethic and the Spirit of Capitalism*, ch. 5, p. 108
> [^2]: So-and-so, "…", *XX Journal* 2019(3), p. 45 (**quoted at second hand; original not seen**)
```

**Rules**:
- Cite a source for every assertion (down to the page)
- Distinguish **primary** (the original work) from **secondary** (quoted at second hand) — **a second-hand citation must say so**
- The material gives no source and you can't find one → mark **⚠️ source unknown**; don't assume it's true

#### 6. Separate claims from facts (humanities' foremost honesty requirement)

| This is | Write it as |
|---|---|
| Historical fact / data | state it directly (and cite) |
| Someone's claim | **must state whose claim it is**: "X argues …" |
| Scholarly consensus | "scholars generally hold …" + source |
| Disputed | "school A holds M, school B holds N; the disagreement lies in …" |
| The material author's leaning | "this textbook takes position P" — textbooks have positions too |

**Counterexample**: writing some scholar's claim directly as "fact" makes readers take it for a settled conclusion.
In humanities material, **this is the most serious distortion**.

### Verification (humanities = sources + consistency)

| What to do | Why |
|---|---|
| **Source completeness** (required) | every assertion has a page / reference; second-hand citations are marked |
| **Term consistency** | the same concept's translated name / usage is uniform throughout (chaotic translated names are extremely common in humanities) |
| **Backbone self-test** | cover the expansion; can you recite from the backbone? |
| **Claim–fact separation self-check** | check whether any scholar's claim was written as objective fact |
| **Retrievability** | when you want "the date and impact of an event", you find it within 30 seconds |
| **Formula / quotation rendering** | if there are foreign-language quotations, check the typesetting |

> Humanities **doesn't need** code to be actually run. But it does need **spot checks of external facts**:
> sample 3–5 hard facts such as dates, personal names, and places and check them online once, to catch memory and transcription errors.

### Common pitfalls

- **Transcribing it into a compressed cracker**: shrink the original and the backbone gets drowned instead
- **Writing claims as facts**: treating a scholar's assertion as objective truth
- **No sources**: at review time you want to verify but have nowhere to start
- **Chaotic translated names**: the same person / concept named differently across pieces → you must keep a glossary
- **Organizing only in the book's order**: you can't find anything at review time
- **Details drowning the backbone**: you remember a pile of examples but can't say what the chapter is about

---

## Three-strategy cheatsheet

| | Theory | Engineering | Humanities |
|---|---|---|---|
| **Core** | derivation | execution | provenance |
| **Required** | justify every step | actually run + paste output | cite sources |
| **Skeleton keywords** | definition · theorem · proof · example | example · error · environment · boundary | thesis · backbone · classification · index |
| **Verification** | formula rendering + derivation self-check + numeric spot check | actually run + copy-test + environment annotation | sources complete + terms consistent + fact spot checks |
| **Most valuable section** | applicability conditions and counterexamples | error analysis | separating claims from facts |
| **Biggest trap** | copying only conclusions | treating "it runs for me" as universal | treating claims as facts |
| **Self-test form** | cover the derivation and redo it | cover the code and rewrite it | cover the expansion and recite the backbone |

**The shared bottom line for all three** (unchanged by subject):
Rewrite, don't transcribe · Complete the cluster · Stable numbered slots · Self-contained · **cite and grade every assertion**.
