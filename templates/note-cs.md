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
B Engineering: programming / computer networks / operating systems / databases / electronics. The correctness of this kind of knowledge is guaranteed by "running".
Use this template when the material contains code, commands, or configuration that only counts once you run it.

[Difference from the other two templates]
· Engineering (this template): the core actions are "actually run and paste the output verbatim" + "error analysis block";
  verification relies on actually running + a copy-only test + environment annotation; conclusions must be written conditionally ("measured to be so on <environment A>").
· Theory note-math.md: the core is "justify every step" + "the formula trio"; running is not required.
· Humanities note-humanities.md: the core is "backbone skeleton first" + "cite provenance everywhere"; no code, no running.
Decision mnemonic: what happens if this is wrong? Can't run it (this category) / can't derive it (theory) / can't find a source (humanities).

[Usage] Copy the whole thing, replace all <angle-bracket placeholders>, and delete this comment block when you're done.
This document uses Obsidian callouts. If the target is GitHub / plain mode,
replace `> [!xxx]` with a bold prefix like `> **Tip**:`, and replace `[[some note]]` with `[some note](some-note.md)`.
Section headings here are illustrative: render them in the output language (the user's language), not necessarily in English.
-->

# <number> · <title>

> **Abstract**: <what problem it solves; before it appeared, how people would do things. Motivation drives memory.>

## 1. What problem it solves

<Without this tool / mechanism, how people would do things. Explain clearly "what happens without it" — that's the hook for memory.>

## 2. Minimal runnable example

<Can be copy-pasted and run; paste the output verbatim, don't beautify. If it won't run, that means it disagrees with the material: keep the correct form and record it on the errata page.>

```<language>
<the shortest copy-pasteable code or command, with the necessary import / cd / arguments. Example: SELECT * FROM t;>
```

```text
<real output, pasted verbatim>
```

> [!info] Test environment
> <OS / runtime / dependencies / date>. Example: Windows 11 · Python 3.12 · 2026-01-01

> [!tip] Copy-only test
> Copying just the code above (without running your own project scripts), can you reproduce the same output? If not, the note is missing context.

## 3. Mechanism

<Why this works the way it does, not just "how to use it". Use an ASCII diagram for complex flows / memory layouts / call chains.>

```text
<flow or layout ASCII diagram>
```

## 4. Error analysis (the most valuable section of this template)

<One real debugging session beats ten successful examples. All four elements are essential: scenario → root cause → how you confirmed it → fix / lesson.>

> [!bug] Error: `<full error text>`
> - **Scenario**: <what operation / environment triggers it>
> - **Root cause**: <the real cause, not the surface symptom>
> - **How I confirmed it**: <which command / which doc pinpoints the root cause>
> - **Fix**: <correct approach>
> - **Lesson**: <one sentence, transferable elsewhere. Example: an error that says "syntax error" doesn't mean the syntax is wrong.>

## 5. Environment and version differences (the mirror that exposes "it runs on my machine")

| Item | This environment | What changes in another environment |
|---|---|---|
| Operating system | <environment A> | <path separator / line endings / filename case sensitivity> |
| Runtime | <version> | <a feature missing below a certain version> |
| Dependencies | <version> | <an API removed / behavior changed from a certain version> |
| Engine / charset | <version> | <a feature unsupported / an error on non-ASCII paths> |

> [!warning] Write the conclusion conditionally
> "Measured to be so on <environment A>; untested on <environment B>, may differ." Don't write it as true everywhere.

## 6. Boundaries and pitfalls

| Input / form | Symptom | Notes |
|---|---|---|
| <normal input> | <expected result> | |
| <boundary input> | <error / abnormal result> | <workaround> |
| <failure condition> | <symptom> | <why> |

## 7. Variants / alternatives

| Approach | Form | Cost / scale it suits |
|---|---|---|
| <option A> | `<code or command>` | <complexity / applicable scenario> |
| <option B> | | |

## 8. Quick reference

```text
<common commands / APIs in one table: what I want to do → use this → don't use this>
```

## Quick self-test

<3–5 questions, covering the core mechanism + at least one boundary; make them executable where possible ("write the command…", "what does this code output").>

> [!question]- 1. <question>
> <answer>

> [!question]- 2. <question>
> <answer>

> [!question]- 3. <question>
> <answer>

---
**Upstream**: [[<previous note>]] **Downstream**: [[<next note>]] · [[<sibling note>]]

<!-- Only fill upstream/downstream with notes that already exist; write ones not yet created as plain text <to be created>, not as links, otherwise they're broken links. -->
