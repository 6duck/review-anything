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
C Humanities: history / philosophy / law / literature / social science. The correctness of this kind of knowledge is guaranteed by "provenance".
Use this template when the material is mainly concepts, claims, threads, schools of thought, and cases — when there's a lot of detail and claims are mixed with facts.

[Difference from the other two templates]
· Humanities (this template): the core actions are "backbone skeleton first" + "cite provenance everywhere" + "separate claims from facts";
  verification relies on complete provenance + consistent terminology + spot-checking hard facts; no code, no running.
· Theory note-math.md: the core is "justify every step" + "the formula trio"; relies on a derivation self-check.
· Engineering note-cs.md: the core is "actually run and paste the output verbatim" + "error analysis block"; relies on execution for verification.
Decision mnemonic: what happens if this is wrong? Can't find a source (this category) / can't derive it (theory) / can't run it (engineering).

[Usage] Copy the whole thing, replace all <angle-bracket placeholders>, and delete this comment block when you're done.
This document uses Obsidian callouts. If the target is GitHub / plain mode,
replace `> [!xxx]` with a bold prefix like `> **Tip**:`, and replace `[[some note]]` with `[some note](some-note.md)`.
Footnotes [^1] are supported in both modes.
Section headings here are illustrative: render them in the output language (the user's language), not necessarily in English.
-->

# <number> · <title>

> **Abstract**: <what this piece of material is trying to argue, in one sentence.>

## 1. Backbone skeleton (memorize this first)

<First write 3–7 items, one sentence each, memorizable; then hang details underneath.
Self-check: cover the expansions below, look at only this section — can you explain the whole thing to someone else?>

1. <origin / claim one>
2. <turning point / claim two>
3. <outcome / claim three>
4. <controversy / claim four>

## 2. Expansion (arguments / examples / data)

<Hang arguments under each backbone item. Mark the provenance after every assertion (page to page).>

### <backbone one · subheading>
<Arguments, examples, data. Example: some event happened in some year and subsequently triggered…… [^1].>

### <backbone two · subheading>
<……>

## 3. Concept comparison

| Comparison item | <concept A> | <concept B> |
|---|---|---|
| Core claim | <……> | <……> |
| Proposer / era | <……> | <……> |
| Key difference | **<state the difference in one sentence>** | |
| Common confusion | <what wrong conclusion the confusion leads to> | |

## 4. People / events / chronology table

<One of the most frequently used lookup entries in humanities notes.>

| Year | Person / event | Claim / impact | See |
|---|---|---|---|
| <year> | <……> | <……> | [[<related note>]] |

## 5. Schools and debates

| Issue | <view A> | <view B> | Point of divergence |
|---|---|---|---|
| <issue> | <……> | <……> | <……> |

## 6. Separating claims from facts (the main honesty requirement in the humanities)

> [!warning] Don't write a claim as a fact
> - Historical fact / data: state it directly, and give the provenance.
> - Someone's claim: must be written as "<someone> argues that……".
> - Scholarly consensus: "the consensus in the field is……" + provenance.
> - Contested: "school A argues M, school B argues N, the divergence lies in……".
> - The material author's / textbook's leaning: "this textbook takes a certain stance". Textbooks have stances too.

Writing a scholar's claim directly as "fact" is the most serious distortion in humanities material.

## 7. Provenance

<Theory relies on derivation, engineering on running, the humanities on provenance. Mark a page number for every assertion; distinguish primary (original work) from secondary citation; if you can't find it, mark ⚠️ source unknown.>

```markdown
<someone> argues that <some claim> [^1]; but this assertion has also been questioned, for example…… [^2].

[^1]: <author>, <book title>, ch. <number>, p.<page> (primary)
[^2]: <author>, <article title>, <journal>, <year>(<issue>), p.<page> (quoted from secondary material, original not seen)
```

## Quick self-test

<3–5 questions, covering the backbone + one easily-confused point. Ask more "who said what from which stance" and "what if…".>

> [!question]- 1. <question>
> <answer>

> [!question]- 2. <question>
> <answer>

> [!question]- 3. <question>
> <answer>

---
**Upstream**: [[<previous note>]] **Downstream**: [[<next note>]] · [[<sibling note>]]

<!-- Only fill upstream/downstream with notes that already exist; write ones not yet created as plain text <to be created>, not as links, otherwise they're broken links. -->
