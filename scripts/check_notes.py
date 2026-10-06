#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_notes.py — self-check for Markdown study notes (pure stdlib, zero dependencies)

Usage:
    python check_notes.py <notes directory> [--mode obsidian|plain] [--json] [--quiet]

Exit codes:
    0 = all passed / 1 = ERROR present / 2 = WARN only

See section 1 of references/verification.md for the check list.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- constants

FRONTMATTER_KEYS = ["tags", "created", "source"]
PLACEHOLDER_RE = re.compile(
    r"\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b|\?\?\?|待补充|待填写|待补全|[（(【\[]待|\[\[待"
)
NUMBERED_RE = re.compile(r"^(\d{2})-(.+)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
INLINE_MATH_RE = re.compile(r"(?<!\$)(?<!\\)\$([^$\n]+?)\$(?!\$)")
BLOCK_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.S)
OBSIDIAN_LINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
MD_LINK_RE = re.compile(r"(?<!\!)\[([^\[\]]*?)\]\(([^()\s]+?)\)")
INDEX_OVERVIEW = "00-"
MIN_BODY_CHARS = 200

# Escapes that are legal in LaTeX
SAFE_ESCAPED = {"#": r"\#", "%": r"\%", "&": r"\&"}

# Used to detect a "literal dollar sign": content contains CJK and has no math features
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
LATEX_HINT_RE = re.compile(r"\\[a-zA-Z]+|[_^{}=+]")


# ---------------------------------------------------------------- helpers


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def strip_code(text: str) -> str:
    """Replace fenced code blocks and inline code with equal-length blanks, keeping line numbers and column offsets unchanged."""
    out = []
    in_fence = False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(" " * len(line))
            continue
        if in_fence:
            out.append(" " * len(line))
            continue
        out.append(CODE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), line))
    return "\n".join(out)


def blank_frontmatter(clean: str, fm_end: int) -> str:
    """Replace the frontmatter region with equal-length blanks (keeps line numbers).

    Why blank it out: the `related:` / `source:` fields in frontmatter may
    reference notes that do not exist yet; treating them as dead links would
    guarantee false positives.
    """
    if not fm_end:
        return clean
    lines = clean.split("\n")
    for i in range(min(fm_end, len(lines))):
        lines[i] = " " * len(lines[i])
    return "\n".join(lines)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def parse_frontmatter(text: str):
    """Return (frontmatter_dict | None, first body line number). Shallow parse: key: value / key: [a, b]."""
    if not text.startswith("---"):
        return None, 0
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return None, 0
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            end = i
            break
    if end is None:
        return None, 0
    fm = {}
    for ln in lines[1:end]:
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", ln)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm, end + 1


def unescape_wikilink_target(raw: str) -> str:
    """[[path\\|alias]] / [[path|alias]] / [[path#section]] → path"""
    raw = raw.replace("\\|", "|")
    target = raw.split("|", 1)[0]
    target = target.split("#", 1)[0]
    return target.strip()


def looks_literal_dollar(tex: str) -> bool:
    """Content reads like prose rather than a formula → most likely a literal $ mistaken for math.

    Real case: `价格是 100$ 和 200$ 两个数。` is matched by the inline-math regex
    as `$ 和 200$`; going straight to C9 (leading/trailing spaces) would produce a
    diagnosis pointing in the wrong direction.
    """
    return bool(CJK_RE.search(tex)) and not LATEX_HINT_RE.search(tex)


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, file, line, code, message):
        self.items.append(
            {"level": level, "file": str(file), "line": line, "code": code, "message": message}
        )

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


# ---------------------------------------------------------------- checks


def check_frontmatter(path, raw, fm, rep):
    if fm is None:
        rep.add("WARN", path.name, 1, "C1", "missing YAML frontmatter")
        return
    missing = [k for k in FRONTMATTER_KEYS if not fm.get(k)]
    if missing:
        rep.add("WARN", path.name, 1, "C1", "frontmatter missing " + ", ".join(missing))


def check_math(path, raw, clean, rep):
    """C2 $ pairing / C3 bare # % & inside math / C9 leading-trailing spaces in inline math / C11 cross-line inline math"""
    block_spans = []
    for m in BLOCK_MATH_RE.finditer(clean):
        block_spans.append((m.start(), m.end()))
        check_math_chars(path, m.group(1), line_of(clean, m.start()), "C3", rep, block=True)

    masked = list(clean)
    for s, e in block_spans:
        for i in range(s, e):
            if masked[i] != "\n":
                masked[i] = " "
    masked = "".join(masked)

    inline_spans = []
    for m in INLINE_MATH_RE.finditer(masked):
        inline_spans.append((m.start(), m.end()))
        tex = m.group(1)
        ln = line_of(masked, m.start())
        if looks_literal_dollar(tex):
            rep.add("ERROR", path.name, ln, "C2",
                    f"suspected literal '$' treated as math (content has CJK and no math features): {tex!r} "
                    f"→ write a literal dollar sign as \\$")
            continue
        if tex[:1] in (" ", "\t") or tex[-1:] in (" ", "\t"):
            rep.add("ERROR", path.name, ln, "C9",
                    f"inline math has leading/trailing spaces; Obsidian will not render it: ${tex}$ → ${tex.strip()}$")
        check_math_chars(path, tex, ln, "C3", rep, block=False)

    # C2 / C11: after masking out recognized formulas, any remaining unescaped $ is stray
    residue = list(masked)
    for s, e in inline_spans:
        for i in range(s, e):
            if residue[i] != "\n":
                residue[i] = " "
    residue = "".join(residue)

    cross_lines = find_cross_line_dollars(residue)
    for ln_no, line in enumerate(residue.split("\n"), start=1):
        if not re.search(r"(?<!\\)\$", line):
            continue
        if ln_no in cross_lines:
            rep.add("ERROR", path.name, ln_no, "C11",
                    "'$' spread across multiple lines within a paragraph and even in total: "
                    "possibly a cross-line inline formula (which does not render), or several "
                    "unrelated literal '$' (which would pair up incorrectly once merged onto one line) "
                    "→ write one complete formula on a single line, or escape literal $ as \\$")
        else:
            rep.add("ERROR", path.name, ln_no, "C2",
                    "unpaired '$' (inline formulas must come in pairs; to display a literal $, escape it as \\$)")


def find_cross_line_dollars(residue: str) -> set:
    """Find stray $ spread across multiple lines of the same paragraph — almost always a cross-line inline formula.

    A single-line stray $ is reported by C2; here the "paired across lines" case is
    singled out because its diagnosis is completely different (the user believes it is
    written correctly, while the whole paragraph actually renders broken).
    """
    per_line = {}
    for n, line in enumerate(residue.split("\n"), start=1):
        c = len(re.findall(r"(?<!\\)\$", line))
        if c:
            per_line[n] = c
    if not per_line:
        return set()

    segs, cur = [], []
    for n in sorted(per_line):
        if cur and n != cur[-1] + 1:
            segs.append(cur)
            cur = []
        cur.append(n)
    if cur:
        segs.append(cur)

    cross = set()
    for seg in segs:
        if len(seg) >= 2 and sum(per_line[n] for n in seg) % 2 == 0:
            cross.update(seg)
    return cross


def check_math_chars(path, tex, ln, code, rep, block):
    """Bare # % & inside math (inside \\begin{...} the & is an alignment character and is exempt)"""
    has_env = "\\begin{" in tex
    for ch, esc in SAFE_ESCAPED.items():
        if ch == "&" and has_env:
            continue
        probe = re.sub(re.escape(esc), "", tex)   # still a bare char after removing legal escapes → error
        if ch in probe:
            where = "Block" if block else "Inline"
            rep.add("ERROR", path.name, ln, code,
                    f"{where} math contains unescaped '{ch}' → should be '{esc}', "
                    f"otherwise the whole formula fails to render: {tex.strip()[:50]}")


def iter_links(clean, mode):
    """Yield (target, line, is_table_row)"""
    for m in OBSIDIAN_LINK_RE.finditer(clean):
        ln = line_of(clean, m.start())
        row_start = clean.rfind("\n", 0, m.start()) + 1
        head = clean[row_start:m.start()]
        yield unescape_wikilink_target(m.group(1)), ln, head.lstrip().startswith("|")
    if mode == "plain":
        for m in MD_LINK_RE.finditer(clean):
            target = m.group(2)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            ln = line_of(clean, m.start())
            row_start = clean.rfind("\n", 0, m.start()) + 1
            head = clean[row_start:m.start()]
            yield target, ln, head.lstrip().startswith("|")


def check_links(path, clean, mode, md_names, rep):
    for target, ln, _is_table in iter_links(clean, mode):
        base = target.split("#", 1)[0].strip()
        if not base:
            continue
        if base.endswith(".md"):
            base = base[:-3]
        if "/" in base:
            base = base.split("/")[-1]
        if base not in md_names:
            close = [n for n in sorted(md_names) if base[:6] in n or n[:6] in base] if base else []
            hint = f" (closest: {close[0]})" if close else ""
            rep.add("ERROR", path.name, ln, "C4", f"dead link: [[{base}]] does not exist{hint}")


def check_wikilink_alias_escape(path, raw, clean, rep):
    """C10: inside a table row the alias must be written [[path\\|alias]]; in body text, [[path|alias]]"""
    for ln_no, line in enumerate(clean.split("\n"), start=1):
        is_table = line.lstrip().startswith("|")
        for m in OBSIDIAN_LINK_RE.finditer(line):
            inner = m.group(1)
            if is_table and "|" in inner and "\\|" not in inner:
                rep.add("ERROR", path.name, ln_no, "C10",
                        "a wikilink alias inside a table must be escaped: [[path\\|alias]] (a bare | tears the table apart)")
            if not is_table and "\\|" in inner:
                rep.add("ERROR", path.name, ln_no, "C10",
                        "do not escape a wikilink alias in body text: [[path|alias]] (\\| shows up as literal residue)")


def check_placeholders(path, raw, clean, rep):
    for ln_no, line in enumerate(clean.split("\n"), start=1):
        m = PLACEHOLDER_RE.search(line)
        if m:
            rep.add("WARN", path.name, ln_no, "C5", f"placeholder left over: '{m.group(0)}'")


def check_size(path, fm_end, text, rep, body_len):
    if body_len < MIN_BODY_CHARS:
        rep.add("WARN", path.name, 1, "C8",
                f"body too short ({body_len} chars, threshold {MIN_BODY_CHARS}); likely only a skeleton was created")


def check_numbering(paths, rep):
    """C6: gaps and duplicates in numbering"""
    nums = {}
    for p in paths:
        m = NUMBERED_RE.match(p.stem)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 97:
                nums.setdefault(n, []).append(p.name)

    for n, names in sorted(nums.items()):
        if len(names) > 1:
            rep.add("WARN", names[0], 1, "C6",
                    f"duplicate number {n:02d}: {', '.join(names)} (links and index will point at an ambiguous target)")

    if not nums:
        return
    lo, hi = min(nums), max(nums)
    for n in range(lo, hi + 1):
        if n not in nums:
            rep.add("WARN", f"{n:02d}-?", 1, "C6", f"number {n:02d} missing (gap within {lo:02d}–{hi:02d})")


def check_overview(paths, texts, rep):
    """C7: two-way cross-check — on disk but not in the index / in the index but not on disk"""
    overview = next((p for p in paths if p.name.startswith(INDEX_OVERVIEW)), None)
    if overview is None:
        rep.add("WARN", "00-overview", 1, "C7", "missing 00-overview (MOC)")
        return
    ov = texts.get(overview.name, "")

    # forward: are all notes on disk listed in the index?
    for p in paths:
        if p.name.startswith(INDEX_OVERVIEW):
            continue
        if p.stem not in ov:
            rep.add("WARN", overview.name, 1, "C7", f"not indexed: {p.name} (new notes must be added back to the overview)")

    # reverse: does every link in the index have a matching file?
    stems = {p.stem for p in paths}
    for m in OBSIDIAN_LINK_RE.finditer(ov):
        target = unescape_wikilink_target(m.group(1)).split("#", 1)[0].strip()
        if not target:
            continue
        if target.endswith(".md"):
            target = target[:-3]
        if "/" in target:
            target = target.split("/")[-1]
        if target not in stems:
            rep.add("WARN", overview.name, line_of(ov, m.start()), "C7",
                    f"index points to a non-existent [[{target}]] (either create the file, or write a link-free \"to build\" row as per convention)")


# ---------------------------------------------------------------- main flow


# Directory names excluded from checks (templates, extraction output, editor config)
SKIP_DIRS = {"templates", "examples", ".obsidian", "_sources", "_extract", "_probe"}


def run(root: Path, mode: str) -> Report:
    rep = Report()
    paths = sorted(p for p in root.rglob("*.md") if p.is_file())
    texts = {}
    stats = {"files": 0, "math": 0, "chars": 0}
    checked = []

    for p in paths:
        raw = read_text(p)
        # Skip template/extraction-output directories (not counted in stats).
        # ⚠️ Must use path segments relative to root: using p.parts (absolute path)
        # would skip an entire notes directory whose path merely happens to contain
        # examples / templates (observed: 2 notes reported as "0 total").
        rel_parts = p.relative_to(root).parts
        if any(part in SKIP_DIRS for part in rel_parts[:-1]) or root.name in SKIP_DIRS:
            continue
        checked.append(p)
        texts[p.name] = raw
        stats["files"] += 1
        clean = strip_code(raw)
        fm, fm_end = parse_frontmatter(raw)
        body = "\n".join(raw.split("\n")[fm_end:])
        stats["chars"] += len(body)
        stats["math"] += len(BLOCK_MATH_RE.findall(clean)) + len(INLINE_MATH_RE.findall(clean))

        check_frontmatter(p, raw, fm, rep)
        check_math(p, raw, clean, rep)
        check_wikilink_alias_escape(p, raw, clean, rep)
        check_placeholders(p, raw, clean, rep)
        body_len = len(re.sub(r"\s", "", body))
        check_size(p, fm_end, raw, rep, body_len)

    md_names = {p.stem for p in checked}
    for p in checked:
        raw = texts[p.name]
        clean = strip_code(raw)
        _, fm_end = parse_frontmatter(raw)
        # links in frontmatter are excluded from the dead-link check (related/source may reference notes not yet created)
        check_links(p, blank_frontmatter(clean, fm_end), mode, md_names, rep)

    check_numbering(checked, rep)
    check_overview(checked, texts, rep)

    return rep, stats


def main(argv=None):
    ap = argparse.ArgumentParser(description="Self-check for Markdown study notes")
    ap.add_argument("directory", help="notes directory")
    ap.add_argument("--mode", choices=["obsidian", "plain"], default="obsidian",
                    help="obsidian (default) checks wikilinks; plain checks relative links")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--quiet", action="store_true", help="print only the summary")
    args = ap.parse_args(argv)

    root = Path(args.directory)
    if not root.is_dir():
        print(f"directory does not exist: {root}", file=sys.stderr)
        return 1

    rep, stats = run(root, args.mode)
    errors, warns = rep.count("ERROR"), rep.count("WARN")

    if args.json:
        print(json.dumps({
            "directory": str(root), "mode": args.mode, "stats": stats,
            "errors": errors, "warnings": warns, "items": rep.items,
        }, ensure_ascii=False, indent=2))
    else:
        if not args.quiet:
            print(f"Checking directory: {root}")
            print(f"Mode: {args.mode}\n")
            for it in rep.items:
                print(f"[{it['level']:<5}] {it['file']}:{it['line']}  {it['code']} {it['message']}")
            if rep.items:
                print()
        print(f"{stats['files']} notes · body {stats['chars']} chars · math {stats['math']} spans "
              f"· ERROR {errors} · WARN {warns}")

    return 1 if errors else (2 if warns else 0)


if __name__ == "__main__":
    sys.exit(main())
