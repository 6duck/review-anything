# Review Anything

![version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![licence](https://img.shields.io/badge/licence-MIT-green.svg)

**Turn any study material into a set of Markdown review notes that stand on their own and survive checking.**

A textbook chapter, a lecture slide deck, a scanned handout, a class transcript, a chat log with an LLM,
a web article, code you wrote — anything you actually want to *learn from later*.

This is an [agent skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview):
a folder of instructions an AI assistant loads when the task matches. Works with Hermes Agent, Claude Code,
Cursor, Cline, or anything else that reads a `SKILL.md`.

---

## The 30-second before / after

You hand it three lecture decks on special relativity (114 slides, 8 of them with no text layer — pure
images). You get:

```
相对论复习笔记/
├── 00-总览与知识链.md                knowledge chain, symbol table, 12-question FAQ
├── 01-经典时空观与伽利略变换.md
├── 02-光速不变与迈克耳孙-莫雷实验.md
├── 03-狭义相对论两条基本原理.md
├── 04-洛伦兹变换.md                  the five-step derivation, every step justified
├── 05-同时性的相对性与因果律.md
├── 06-时间延缓与双生子佯谬.md
├── 07-长度收缩.md
├── 08-洛伦兹速度变换.md
├── 09-相对论质量与动量.md            why m = γm₀ — from a symmetric collision, in four lines
├── 10-相对论动能与质能关系.md
├── 11-能量动量关系与相对论碰撞衰变.md
├── 12-速查表.md                      one-page formula sheet for the last five minutes before the exam
└── 13-勘误与未解问题.md              6 content errors in the deck, 5 open uncertainties
```

That last file is the point. In this example the notes caught **the deck's own worked example contradicting
the equation printed directly above it** (a "1 MeV electron" momentum computed as if 1 MeV were the kinetic
energy), a Michelson-interferometer `ΔN` that does not follow from the numbers on the same slide, and a
published experiment cited to the wrong paper. Each entry shows the arithmetic that exposes the discrepancy
*and* says what a reader should use instead.

It also shows the restraint the method asks for — no scripts, no "ran it" blocks. The note that proves
*m = γm₀* does it with a symmetric collision and four lines of algebra: a derivation is verified by
re-deriving it, not by running a programme. And the errata page refuses to list things that merely look
wrong — a `590` vs `589 nm` rounding, numbers that vanished **in our own render**, a slide that is really a
homework page. Those are collected in an "excluded, and why" table at the end instead.

→ Browse the full output: [`examples/相对论复习笔记/`](examples/相对论复习笔记/)

---

## The core idea

**Knowledge does not look the same across subjects, so the notes must not either.**
A theorem, a snippet of C, and a historical event are three different things to have "learned" —
guaranteed by **logic**, by **running it**, and by **provenance**.

| Type | Material | Correctness guaranteed by | The notes emphasize |
|---|---|---|---|
| **A · theory** | maths, physics, chemistry, statistics | **logic** | formulas, derivations, relationships, worked examples |
| **B · engineering** | programming, networking, OS, databases, electronics | **running it** | code, error analysis, measured behaviour, environment differences |
| **C · humanities** | history, philosophy, law, literature, social science | **provenance** | backbone extraction, classification, searchability |

**Tie-breaker**: *if this is wrong, how would you find out?* — you can't derive it (A) / you can't run it
(B) / you can't trace the source (C).

One template forced onto all three is why most auto-generated study notes are useless.
Full skeletons, actions, verification methods and worked examples: [`references/subject-strategies.md`](references/subject-strategies.md).

## The Five Rules

1. **Rewrite, don't transcribe** — if deleting a passage costs nothing to learning, delete it
2. **Complete the cluster** — every concept gets the larger cluster it belongs to (`3NF` without
   `1NF/BCNF/denormalization` is a floating fragment)
3. **Stable numbered slots** — `01-`, `02-`, … so the folder can grow without renames or broken links
4. **Self-contained** — send one file to a classmate who never saw the source; can they follow it?
5. **Cite and grade** — every statement answers "where is this from": source / `[extension]` / ✅ verified /
   📖 documented / ⚠️ unverified. **Rather look weak than claim credit.**

**Verification follows the subject, not a template.** Maths and physics are checked by **re-deriving** (three
sampled values, recomputed by hand); humanities by **provenance**; only engineering is checked by **actually
running** things. Code, scripts and "ran it" blocks have no place in a theory note — a script proves nothing
about a derivation, and the folder reads better without them.

## ⚡ Context economy

An agent's bill is not the work it does — it is **the sum of the context re-sent on every step**. On one
measured 168-step run that produced 9 notes, 63.9 M tokens were billed and only **1.4 %** of that was
actual work; 98.6 % was the same context being replayed. The biggest single line item was *reading files
back into the conversation* (14.5 M), and loading this skill's own docs cost 5.6 M.

So the skill carries a cost model and seven hard rules: **content lives on disk, not in the conversation** ·
never re-read what you already wrote · load only the section of docs you need · shard the work into short
sessions · subagents return a path plus one line · never enumerate a whole tree · three images per call,
transcribe once. Source extracts are read in slices, never whole — on a later run, three whole-file reads of
extracted source text were 23 % of the entire bill on their own. Verification is bounded to match — a
machine check, a **3-item** sample, and an optional capped verifier. Nothing exhaustive.

Measured on the next real run after those rules landed: **63.9 M → 14.4 M tokens, 340 → 88 steps, 30 → 14
minutes** for a comparable job (three decks → 14 notes), in one session instead of three.

The money is usually small (that first run cost about US$0.5 on a cache-heavy model). **The real cost is
wall-clock time, and it has the same root cause.** Shrinking the context buys back both.

---

## ⚠️ Language

The skill is written in English — that is what the agent reads, and English is the cheapest option for it.

**The notes are not.** Output is written in **the user's language**, not the skill's: a Chinese user's
notes come out in Chinese, headings included. See [SKILL.md](SKILL.md#language-rule).

---

## Install

**Hermes Agent**

```bash
git clone https://github.com/6duck/review-anything.git "$HERMES_HOME/skills/note-taking/review-anything"
```

**Claude Code / Cursor / Cline**

```bash
git clone https://github.com/6duck/review-anything.git ~/.claude/skills/review-anything   # user level
git clone https://github.com/6duck/review-anything.git .claude/skills/review-anything     # or per project
```

> If your platform rejects the `metadata:` block in the frontmatter, delete that block —
> `name` / `description` / `version` / `license` are the portable fields.

**No skill system at all**: paste [`SKILL.md`](SKILL.md) into the conversation as a system prompt, then
append the relevant files from `references/` and `templates/` when needed.

### Dependencies (scripts only)

```bash
pip install pymupdf                   # PDF extraction
pip install python-pptx python-docx   # PPTX / DOCX
# scripts/check_notes.py is standard-library only — zero dependencies
```

## Use

```
整理 @第3章-1.pdf，按 review-anything，输出到 notes/数据库系统原理/
```

```
把这份相对论课件做成复习笔记，公式要准，例题要给我完整推导
```

The assistant runs five stages — **recon → extract → structure → write → verify → deliver** — and hands
back a report with statistics rather than "all done":

```
✅ Done: 相对论复习笔记/ — 14 notes (type: A · theory)
   overview + 11 notes + cheatsheet + errata
   body 81,287 chars · 1,555 formula spans · MathJax 0 failures · 0 dead links
   hand-checked 3 high-risk values → found 6 knowledge-point errors in the source (recorded on the errata page)
   ⚠️ not checked: the remaining numeric conclusions (listed explicitly on the errata page), marked ⚠️ where they matter
   📁 kept: _sources/ — 3 text extracts + 1 visual transcript (≈56 KB); delete the folder to drop them
```

## What's in here

| Path | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | the skill itself — five rules, three strategies, the five-stage workflow |
| [`references/subject-strategies.md`](references/subject-strategies.md) | ★ full skeletons and verification per subject (**read before writing**) |
| [`references/extraction-playbook.md`](references/extraction-playbook.md) | extraction per material type, batch image reading, sharding, context budget |
| [`references/note-conventions.md`](references/note-conventions.md) | folder layout, frontmatter, MOC, callouts, ASCII diagrams, link syntax |
| [`references/verification.md`](references/verification.md) | verification per subject, its budget, and the eleven machine checks |
| [`templates/`](templates/) | note skeletons: A / B / C / generic / overview / cheatsheet |
| [`scripts/check_notes.py`](scripts/check_notes.py) | eleven automated note checks (standard library only, exit code = verdict) |
| [`scripts/extract_material.py`](scripts/extract_material.py) | material extraction + extraction-route recon |
| [`scripts/merge_ranges.py`](scripts/merge_ranges.py) | coverage reconciliation for sharded transcripts |
| [`examples/相对论复习笔记/`](examples/相对论复习笔记/) | a real run: three lecture decks → 14 notes, transcripts kept in `_sources/` |
| [`docs/full-guide.zh.md`](docs/full-guide.zh.md) | the full-length Chinese guide |

The three scripts are tested on Linux / macOS / Windows, including non-ASCII paths.

## Status — what is and is not proven

- The three scripts have a **negative control**: deliberately broken notes were confirmed to trigger all
  eleven checks, and two real note folders pass with **0 errors and 0 warnings** — including the bundled
  example (14 notes, 1,555 formula spans, 0 / 0).
- The `examples/` folder is a real end-to-end run, not a mock-up — errors and all. Its errata page lists
  mistakes that are really in the source, each with the hand arithmetic that shows it, and it names what was
  deliberately *not* swept.
- The efficiency claims are measured, not estimated: 88 steps / 14.4 M tokens / 14.1 minutes for the example
  run, and ≈8 s of model round-trip per scanned page when images go one at a time (three per call cuts that
  by roughly 3×).
- **Not** proven: general quality across many subjects. This has been driven hard on physics, maths and
  database course material. Treat the strategy sections as a strong default, not a guarantee.

---

## 中文速览

**把任何学习素材，变成能独立阅读、经得起校验的 Markdown 复习文档。**

- **三种学科三套策略**：理论类靠**逻辑**（公式/推导/每步标依据）、工程类靠**运行**（实跑/贴输出/环境差异）、
  文科类靠**出处**（主干先行/分类归纳/处处标页码）。判断口诀：*这东西错了会怎样*——推不出来／跑不起来／查不到出处。
- **五条铁律**：重写不摘抄 · 补全知识簇 · 固定编号槽位 · 自足可读 · 标注来源与置信度。
- **五阶段流程**：侦察 → 提取 → 结构 → 写作 → 校验 → 交付（交付时报统计、并告知保留了哪些中间产物）。
- **核验随学科，且是有界的**：理论类**手算抽样 3 个高风险数值**（不写脚本、不跑程序）、工程类**实跑**、
  文科类**查出处**；脚本十一项机器自检 + 阴性对照；核验预算不超过全程步数的 20%。
- **勘误只记"知识点错误"**：跟着它会学错的才收；错别字、字体、与结论无关的取整、自己渲染时掉的字都不收。
- **序号码是一串**：`00` 总览、正文 `01…`、速查表与勘误接着排（如 `12-`、`13-`），不保留 98/99。
- **英文写 skill，中文写笔记**：本仓库的指令是英文（给模型读，省 token），**生成出来的笔记跟随用户语言**。
- **上下文经济**：账单不是"干了多少活"，而是"每一步重发了多少上下文"。所以内容落盘不进对话、不读回自己写过的东西、
  文档按需读小节、分会话分片、子代理只回一行。

完整中文说明见 [`docs/full-guide.zh.md`](docs/full-guide.zh.md)；
真实效果展示见 [`examples/相对论复习笔记/`](examples/相对论复习笔记/)。

## Credits

MIT © 2026 [6duck](https://github.com/6duck).
Built from repeated real use — every pitfall in [SKILL.md](SKILL.md#known-pitfalls-all-hit-for-real)
is one that was actually hit, with the fix measured rather than guessed.
