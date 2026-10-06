#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_ranges.py — coverage reconciliation and merging for sharded transcription (pure stdlib)

Purpose: after a 200+ page book is transcribed in parallel by 2–4 workers,
**nobody can tell by feel whether every page in 1..N is covered**. This script
answers that question.

It does two things, independently of each other (this is double verification):
    1. Look at the **ranges declared in file names** (p0001-0040.md) — is the layout complete?
    2. Look at the **page markers inside the files** (===== p12 =====) — is the actual content complete?

If the two disagree, it warns: the file name says 40 pages but there are only 38
page markers → 2 pages were missed. Relying on file names alone, such missing pages
can never be caught.

Usage:
    # Reconcile (default, writes no files)
    python merge_ranges.py ./_sources/pages/ --total 241

    # Reconcile and merge into one full transcript
    python merge_ranges.py ./_sources/pages/ --total 241 --concat ./_sources/full.md

    # Shard files without a range in the name (e.g. a.md / b.md); reconcile by inner page markers only
    python merge_ranges.py ./_sources/ --total 241 --no-range-check

Exit codes:
    0 = full coverage, no overlap, no missing pages
    1 = gaps / overlaps / missing pages present
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# matches names like p0001-0040 / 1-40 / p1_40 / 0001-0040.md
RANGE_RE = re.compile(r"p?(\d{1,4})\s*[-_~]\s*(\d{1,4})", re.IGNORECASE)
# matches the page separator marker in transcripts: ===== p12 ===== / == p12 ==
MARK_RE = re.compile(r"^=+\s*p\s*(\d{1,4})\s*=+\s*$", re.MULTILINE | re.IGNORECASE)


def parse_range(name: str):
    """Parse (start, end) from a file name; return None if it cannot be parsed"""
    m = RANGE_RE.search(name)
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2))
    return (a, b) if a <= b else (b, a)


def scan_dir(d: Path):
    """Return [(path, declared range|None, list of actual page markers)]"""
    out = []
    for f in sorted(d.rglob("*.md")) + sorted(d.rglob("*.txt")):
        text = f.read_text(encoding="utf-8", errors="replace")
        marks = [int(x) for x in MARK_RE.findall(text)]
        out.append((f, parse_range(f.stem), marks))
    return out


def merge_ranges(ranges):
    """Merge a list of ranges → [(start, end), ...], used to compute the union"""
    if not ranges:
        return []
    rs = sorted(ranges)
    merged = [list(rs[0])]
    for a, b in rs[1:]:
        if a <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [tuple(x) for x in merged]


def find_overlaps(items):
    """items: [(file, (start, end)), ...] → [(file1, file2, overlap range), ...]"""
    pairs = []
    rs = sorted(items, key=lambda x: x[1])
    for i in range(len(rs)):
        for j in range(i + 1, len(rs)):
            f1, (a1, b1) = rs[i]
            f2, (a2, b2) = rs[j]
            if a2 <= b1:
                pairs.append((f1, f2, (a2, min(b1, b2))))
    return pairs


def main(argv=None):
    ap = argparse.ArgumentParser(description="Coverage reconciliation and merging for sharded transcription")
    ap.add_argument("directory", help="directory containing the sharded transcripts")
    ap.add_argument("--total", type=int, required=True, help="total pages N of the material (must match the source file)")
    ap.add_argument("--concat", metavar="OUT", help="merge into one full transcript in page order")
    ap.add_argument("--no-range-check", action="store_true",
                    help="ignore ranges in file names; reconcile by inner page markers only")
    args = ap.parse_args(argv)

    d = Path(args.directory)
    if not d.is_dir():
        print(f"directory does not exist: {d}", file=sys.stderr)
        return 1

    files = scan_dir(d)
    if not files:
        print(f"no .md/.txt shards in directory: {d}", file=sys.stderr)
        return 1

    total = args.total
    print(f"Reconcile dir: {d}")
    print(f"Total pages: {total}\n")

    problems = []

    # ---- 1) ranges declared in file names
    declared = [(f, r) for f, r, _ in files if r]
    print("Shard list:")
    if args.no_range_check:
        print("  (file-name range check disabled)")
    for f, rng, marks in files:
        if rng:
            span = rng[1] - rng[0] + 1
            flag = "" if len(marks) == span else f"  ⚠️ declares {span} pages but has only {len(marks)} page markers"
            print(f"  {f.name:<28} declares p{rng[0]:>4}–p{rng[1]:<4} ({span:>3} pages)  markers {len(marks):>3}{flag}")
            if flag:
                problems.append(f"{f.name} declares {span} pages but has only {len(marks)} page markers")
        else:
            print(f"  {f.name:<28} no range in name                   markers {len(marks):>3}"
                  f" (pages {marks[0]}–{marks[-1]})" if marks else f"  {f.name:<28} no range in name  markers 0")
            if not marks and not args.no_range_check:
                problems.append(f"{f.name} has neither a range in its name nor page markers; cannot reconcile")

    if declared and not args.no_range_check:
        merged = merge_ranges([r for _, r in declared])
        print(f"\nDeclared-range union: {len(merged)} segments → "
              + "  ".join(f"p{a}–p{b}" for a, b in merged))

        covered = set()
        for a, b in merged:
            covered.update(range(a, b + 1))
        gaps = [p for p in range(1, total + 1) if p not in covered]
        if gaps:
            show = gaps[:30]
            print(f"❌ {len(gaps)} pages missing: {show}{' …' if len(gaps) > 30 else ''}", file=sys.stderr)
            problems.append(f"declared ranges have {len(gaps)} missing pages")
        else:
            print(f"✓ declared ranges cover all pages 1..{total}")

        overs = find_overlaps(declared)
        if overs:
            for f1, f2, ov in overs:
                print(f"⚠️ overlap: {f1.name} and {f2.name} both transcribe p{ov[0]}–p{ov[1]}",
                      file=sys.stderr)
            problems.append(f"{len(overs)} overlapping shard ranges")
        else:
            print("✓ no range overlap")

    # ---- 2) page markers inside the files (the stronger layer)
    all_marks = {}
    dupes = []
    for f, _, marks in files:
        for m in marks:
            if m in all_marks:
                dupes.append((m, all_marks[m].name, f.name))
            all_marks[m] = f

    print(f"\nInner page markers: {len(all_marks)} distinct page numbers")
    mark_gaps = [p for p in range(1, total + 1) if p not in all_marks]
    if mark_gaps:
        show = mark_gaps[:30]
        print(f"❌ {len(mark_gaps)} pages missing by page markers: {show}{' …' if len(mark_gaps) > 30 else ''}",
              file=sys.stderr)
        problems.append(f"page markers have {len(mark_gaps)} missing pages")
    else:
        print(f"✓ page markers cover all pages 1..{total}")
    if dupes:
        for m, a, b in dupes[:10]:
            print(f"⚠️ p{m} transcribed in both {a} and {b}", file=sys.stderr)
        problems.append(f"{len(dupes)} duplicated pages")

    # ---- 3) optional merge
    if args.concat:
        out = Path(args.concat)
        out.parent.mkdir(parents=True, exist_ok=True)
        # split by page markers and reorder to guarantee strict page order in the output
        blocks = {}
        for f, _, _ in files:
            text = f.read_text(encoding="utf-8", errors="replace")
            parts = re.split(r"(^=+\s*p\s*\d{1,4}\s*=+\s*$)", text, flags=re.MULTILINE)
            for i in range(1, len(parts), 2):
                num = int(re.search(r"\d+", parts[i]).group())
                body = parts[i + 1] if i + 1 < len(parts) else ""
                blocks.setdefault(num, []).append(body.rstrip())
        with out.open("w", encoding="utf-8") as fh:
            for p in sorted(blocks):
                fh.write(f"\n\n===== p{p} =====\n")
                fh.write("\n".join(blocks[p]).strip() + "\n")
        print(f"\nMerged: {out} ({len(blocks)} pages, in page order, duplicate pages kept side by side)")

    # ---- summary
    print()
    if problems:
        print(f"❌ Reconciliation failed with {len(problems)} problem(s):")
        for p in problems:
            print(f"   - {p}")
        print("\nDo not start writing notes — gaps cause silently missing chapters that are very hard to spot later.")
        return 1

    print(f"✅ Reconciliation passed: every page 1..{total} is transcribed; no gaps, no overlap, no missing pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
