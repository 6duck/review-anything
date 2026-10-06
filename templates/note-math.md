---
tags: [<subject type>, <knowledge point category>, <specific keywords>]
created: <date YYYY-MM-DD>
updated: <date YYYY-MM-DD>
source: <source: file name + chapter / page, or URL + access date>
status: draft
related: []          # <wikilink to a related note, optional; leave it blank if unsure, don't write a broken link>
---

<!--
[When to use this template]
A Theory: math / physics / chemistry / statistics. The correctness of this kind of knowledge is guaranteed by "logic".
Use this template when the material is mainly definitions, theorems, formulas, derivations, and proofs.

[Difference from the other two templates]
· Theory (this template): the core actions are "justify every step" + "remember the formula trio (statement / applicability conditions / equality condition)";
  verification relies on a derivation self-check + spot-checking key values; running is not required.
· Engineering note-cs.md: the core is "actually run and paste the output verbatim" + "error analysis block"; verification relies on execution and environment annotation.
· Humanities note-humanities.md: the core is "backbone skeleton first" + "cite provenance everywhere"; verification relies on complete provenance and spot-checking facts.
Decision mnemonic: what happens if this is wrong? Can't derive it (this category) / can't run it (engineering) / can't find a source (humanities).

[Usage] Copy the whole thing, replace all <angle-bracket placeholders>, and delete this comment block when you're done.
Except for the "abstract", this document uses Obsidian callouts (> [!warning], etc.). If the target is GitHub / plain mode,
replace `> [!xxx]` with a bold prefix like `> **Tip**:`, and replace `[[some note]]` with `[some note](some-note.md)`.
Section headings here are illustrative: render them in the output language (the user's language), not necessarily in English.
-->

# <number> · <title>

> **Abstract**: <what this knowledge point solves and where its boundary is. Once you've written this sentence you should be able to judge where this note ends.>

## 1. Objects and notation

<The definitions involved in this section. Give a definition the first time a symbol appears; keep the same symbol meaning the same thing throughout to avoid notation drift.>

| Symbol | Meaning | Notes |
|---|---|---|
| $<symbol>$ | <meaning> | <which easily-confused symbol to distinguish it from> |

## 2. Statement of the proposition (write out both the condition + conclusion)

**Theorem <number>**: <full statement; don't write just the conclusion.>

- **Condition**: <premise assumptions>
- **Conclusion**: <the derived result>

## 3. Derivation / proof (justify every step)

<This template's soul: marking the justification is the only criterion that separates "useful notes" from "transcription". Below is a format example; replace it with your content.>

$$
\begin{aligned}
\frac{d}{dx} x^2 &= \lim_{\Delta x \to 0} \frac{(x + \Delta x)^2 - x^2}{\Delta x} && \text{← definition of derivative} \\
                 &= \lim_{\Delta x \to 0} \frac{2x\,\Delta x + (\Delta x)^2}{\Delta x} && \text{← expand } (x + \Delta x)^2 \\
                 &= 2x && \text{← cancel } \Delta x \text{ and take the limit}
\end{aligned}
$$

> [!tip] Self-check
> Three months from now, looking at any intermediate step, can you immediately say why it is that step? If not, add the justification.

<!-- Physics / chemistry / statistics specific (pure math can delete this):
     Dimensional check —— both sides of the equation must have consistent dimensions;
     Limit regression —— push a parameter to the extreme and see whether it degenerates to a known result. Two free self-check rulers; write them next to the derivation. -->

## 4. Applicability conditions and equality

<The range within which the formula holds; the conditions under which the equality / extremum holds. A formula missing the latter two is a dangerous formula.>

| Formula | Applicability conditions | Equality / extremum holds |
|---|---|---|
| $<formula statement>$ | <range, premises> | <equality condition> |

## 5. Worked example

> [!tip] When to use it
> <What features of this kind of problem mean you should use this method. This line is worth more than the example itself; it determines whether you can recall which tool to use in the exam.>

**Problem**: <problem statement>

**Solution**: <key steps, still justifying every step; if you skip a step, restore the step whose dependency you skipped.>

## 6. Variants and counterexamples

<For every theorem, ask: if you remove some condition, does the conclusion still hold?>

> [!warning] Conditions can't be dropped
> <After removing some condition the conclusion fails.> Counterexample: <construct a very small counterexample you can compute by hand.>

- **One problem, many solutions**: <the second and third routes to the same problem; compare their costs and identify the invariants.>
- **Many problems, one solution**: <group problems scattered in different places under the same method, forming that method's domain of applicability.>

## 7. Common mistakes

| Wrong form / idea | Why it's wrong | Correct approach |
|---|---|---|
| <omitting an applicability condition> | <what wrong conclusion it leads to> | <how to avoid it> |

## 8. Relationships (depends on / used by)

```text
<upstream concept>
    ↓
<this proposition> ──→ <downstream conclusion>
    ↑
<parallel or prerequisite concept>
```

- **Depends on**: <what this note depends on; what is a special case of it.>
- **Used by**: <who uses this note.>
- **Which larger cluster it belongs to**: <cluster name> — <who else is in the cluster.>

## Quick self-test

<3–5 questions, covering the core mechanism + at least one boundary. Ask more "why / what if…", less "what is".>

> [!question]- 1. <question>
> <answer: point out the mechanism, don't restate the conclusion.>

> [!question]- 2. <question>
> <answer>

> [!question]- 3. <question>
> <answer>

---
**Upstream**: [[<previous note>]] **Downstream**: [[<next note>]] · [[<sibling note>]]

<!-- Only fill upstream/downstream with notes that already exist; write ones not yet created as plain text <to be created>, not as links, otherwise they're broken links. -->
