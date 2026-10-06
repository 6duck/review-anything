---
tags: [{{subject type}}, overview, MOC]
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
source: {{material source: file name / textbook chapter / URL}}
---

<!--
Section headings here are illustrative: render them in the output language (the user's language), not necessarily in English.
-->

# {{topic}} · Overview and knowledge chain

> [!abstract] What this topic solves
> {{One or two sentences. What you'll be able to do and what kinds of questions you'll be able to answer once you're done.
>  Can't write this paragraph = you haven't thought through this note's boundary yet; go back over the material.}}

---

## 1. Knowledge chain

{{Express the **dependency relations** between concepts with an ASCII diagram or mermaid,
 not a table-of-contents listing.
 mermaid example (natively supported by Obsidian; remove the backticks wrapping the code block below to use it):

 ```mermaid
 flowchart TD
   a["01 · {{Concept A}}"] --> b["02 · {{Concept B}}"]
   b --> c["03 · {{Concept C}}"]
   b --> d["04 · {{Concept D}}"]
 ```

 ASCII diagram example:

     {{Concept A}} → {{Concept B}} → {{Concept C}}
                     ↑
              {{Concept D}} / {{Concept E}} (two parallel approaches)
}}

---

## 2. Concept responsibility table

{{What each component/concept "is responsible for, and not responsible for". One table clears away the boundaries and prevents confusion.}}

| Concept | Responsibility | Not responsible for |
|---|---|---|
| {{Concept A}} | {{what it does}} | {{what it's easily mistaken for doing}} |
| {{Concept B}} | | |

---

## 3. Learning path

{{Review order that follows the dependency order, annotated with prerequisites and estimated time.}}

| Order | Content | Prerequisite | Estimate |
|---|---|---|---|
| 1 | {{01 Concept A}} | — | 20 min |
| 2 | {{02 Concept B}} | 01 | 30 min |

---

## 4. Note index

{{**Come back and update this table every time you add a note.** It is the table of contents for the whole folder.}}

| # | Note | Status | One-liner |
|---|---|---|---|
| 00 | This page | ✅ | Overview |
| 01 | [[01-{{title}}]] | ✅ done / 🔄 to fill in / ⬜ to create | {{one-liner}} |
| 02 | [[02-{{title}}]] | | |

> Status legend: ✅ done · 🔄 to fill in (state clearly which part is missing) · ⬜ to create (**don't write it as a wikilink**, to avoid a broken link)

---

## 5. Quick Q&A

{{The points you get stuck on most while reviewing; one answer per line. **This is the most-used block, and it's worth maintaining over and over.**}}

| Question | One-line answer | See |
|---|---|---|
| {{How to tell apart the two most confusable concepts}} | {{one line}} | [[0N-{{title}}]] |
| {{Some counter-intuitive conclusion}} | {{one line}} | [[0N-{{title}}]] |

---

## 6. Open questions / TODO

- [ ] {{Point you still don't get → come back and update it once you find out}}
- [ ] {{Point the material didn't explain clearly, to be filled in from the official docs}}

---

**Upstream**: {{if there's a preceding topic, link it}}
**Downstream**: {{if there's a following topic, link it}}
