---
tags: [{{subject type}}, {{knowledge point category}}, {{specific keywords}}]
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
source: {{file name + chapter/page, or URL + access date}}
status: complete
---

<!--
Section headings here are illustrative: render them in the output language (the user's language), not necessarily in English.
-->

# {{NN}} · {{title}}

> **Abstract**: {{What this knowledge point solves. Once you've written this sentence you should be able to judge where this note's boundary lies.}}

## Why it's needed

{{Motivation. Without this section, the reader won't know why this syntax/concept/mechanism has to exist.
 Spell out "what happens without it" — that's the hook for memory.}}

## Core mechanism

{{The body. **Rewrite, don't transcribe**:
 drop the original material's lecturing tone ("let's take a look", "it's not hard to see") and switch to a declarative tone.
 Split the subheadings by logic; don't copy the original book's chapter titles.

 Suggested structure: definition → mechanism → step-by-step expansion → boundaries
 Put complex flows in an ASCII diagram inside a code block.}}

```text
{{ASCII diagram example:
    ┌──────────┐
    │  {{A}}   │
    └────┬─────┘
         ↓
    ┌──────────┐
    │  {{B}}   │
    └──────────┘
}}
```

## Example (actually run)

{{Anything executable, **actually run it**, paste the real output.

 ✅ Run = executed on this machine, with environment/version
 📖 Docs = checked the official docs, with link
 ⚠️ Not run = can't be executed, or must be verified by yourself before use

 Output disagrees with the material → **the material is wrong**. Keep the correct form and record it on the errata page.}}

```{{language}}
{{copy-pasteable code / command}}
```

```text
{{real output (paste verbatim, don't beautify)}}
```

## Variants and boundaries

{{This is the section that raises the value; the material often gives only the happy path, and you have to supply the boundaries yourself.}}

| Scenario | Behavior | Notes |
|---|---|---|
| {{normal case}} | {{result}} | |
| {{edge case}} | {{result}} | {{easy pitfall}} |
| {{failure condition}} | {{error / abnormal}} | {{workaround}} |

> [!warning] Pitfall
> {{The point most easily misremembered. Write it as "many people assume X, but it's actually Y".}}

## Relationship to adjacent concepts

{{Point to the neighbors in the knowledge cluster, state the difference in one sentence, and give the wikilink.

 Example: `WHERE` handles rows, `HAVING` handles groups — see [[{{adjacent concept}}]]}}

- **Difference from {{concept X}}**: {{one sentence}}
- **{{concept Y}} is its prerequisite**: {{why}}
- **Which larger cluster it belongs to**: {{cluster name}} — {{who else is in the cluster}}

## Quick self-test

{{3–5 questions, covering the core mechanism + at least one boundary.
 Ask more "why" and "what if…", less "what is".
 Fold the answers (in Obsidian use `> [!question]-`, in plain mode use <details>).}}

> [!question]- 1. {{question}}
> {{answer}}

> [!question]- 2. {{question}}
> {{answer}}

> [!question]- 3. {{question}}
> {{answer}}

---
**Upstream**: [[{{previous note}}]]
**Downstream**: [[{{next note}}]] · [[{{sibling note}}]]
