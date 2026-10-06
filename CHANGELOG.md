# Changelog

All notable changes to Review Anything are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

> **1.0.0 is the first public release.** The tool was developed in private over a few days of real use;
> those intermediate versions were never meant for anyone else, so the history starts here.

## [1.0.0] - 2026-10-07

### What it does

Turns any learning material — textbook PDFs, lecture slide decks, scanned handouts, class transcripts, chat
logs with an LLM, web articles, code you wrote — into a folder of Markdown notes that stand on their own and
survive checking. Output is written in **the user's language**; the skill itself is in English.

### The method

- **Five iron rules** — rewrite rather than transcribe · complete the knowledge cluster · fixed numbered
  slots · self-contained · cite and grade every statement (source / `[extension]` / ✅ verified /
  📖 documented / ⚠️ unverified). *Rather look weak than claim credit.*
- **Three subject strategies** (A theory · B engineering · C humanities) with the tie-breaker question
  *"if this is wrong, how would you find out?"* — you cannot derive it / cannot run it / cannot trace it.
- **Verification follows the subject.** Theory is checked by **re-deriving** — three sampled values,
  recomputed **by hand**; humanities by **provenance**; only engineering by **actually running** things.
  Scripts, programme runs and pasted output have no place in a theory note, and a verification script is a
  *regenerable* artifact that never belongs in `_sources/`.
- **Bounded verification, not exhaustive** — a machine check → a 3-item subject sample → a 30-second
  self-containment read, inside a budget of ≤20 % of the run's steps. The negative control runs when the
  checker or the note structure changes, not on every delivery.
- **Errata pages accept only knowledge-point errors** — the ones that would teach you something false
  (a wrong formula, a number contradicting its own equation, a conclusion that dropped its premise, a
  mis-attributed citation). Typos, fonts, a rounded constant, page-order oddities, or glyphs lost in *your
  own* render do not earn entries.
- **Sequential note numbering** — `00-overview`, body notes `01…`, then the cheatsheet and errata continue
  the sequence (`12-`, `13-`); when a source later adds body notes they move to the end and the links are
  fixed. No reserved `98`/`99`.
- **Context economy as a rule, not a tip** — an agent's bill is the context re-sent on every step, so:
  content lives on disk rather than in the conversation · artifacts are never read back · documentation is
  read by section · work is sharded into short sessions · a subagent returns "a path plus one line" ·
  source extracts are read in slices, not whole · images go three per call and are transcribed once.
- **Five stages** — reconnaissance → extraction → structure → writing → verification → delivery, ending in a
  report with statistics and an explicit list of what was kept in `_sources/` and how to delete it.

### The tooling

- [`scripts/check_notes.py`](scripts/check_notes.py) — eleven automated note checks (numbering continuity
  and duplicates, `$` pairing, broken wikilinks, index↔file agreement, frontmatter, render-breaking
  constructs), standard library only, exit code = verdict.
- [`scripts/extract_material.py`](scripts/extract_material.py) — unified extraction (PDF / PPTX / DOCX /
  TXT) plus **route reconnaissance**: the route is chosen by the share of near-zero-character pages, not by
  average characters per page. `--render-png` reconciles page coverage; `--batch 3` writes a manifest of
  three separate images per batch.
- [`scripts/merge_ranges.py`](scripts/merge_ranges.py) — coverage reconciliation and merging for sharded
  transcripts.
- [`references/`](references/) — subject strategies, extraction playbook, note conventions, verification.
- [`templates/`](templates/) — note skeletons for A / B / C / generic / overview / cheatsheet.
- [`examples/相对论复习笔记/`](examples/相对论复习笔记/) — a real run: three special-relativity lecture decks
  (114 slides, 8 of them with no text layer) → 14 notes, with **6 content errors found in the source**,
  transcripts kept under `_sources/`, and the checker reporting 0 errors / 0 warnings.
- [`docs/full-guide.zh.md`](docs/full-guide.zh.md) — the full-length Chinese guide.
- MIT licence.

### Measured

- On the example run: **88 steps, 14.4 M billed tokens, 14.1 min** for three decks → 14 notes; only 1.8 % of
  the bill was actual work, the remaining 98.2 % being context replay — which is why context economy is
  enforced as a rule.
- Transcribing scanned pages one image per model call costs ≈**8 s of round-trip per page** (110 pages ≈
  14 min); sending three **separate** images per call cuts that by roughly 3×, and sharding cuts it further.
