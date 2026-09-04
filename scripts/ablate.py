#!/usr/bin/env python3
"""Ablation variant generator for taxue-halftone SKILL.md.

Blocks are marked with [ABLATE:ID] on their heading line (## or ###).
A parent block marked [ABLATE:ALL] is removed when none of its child
blocks survive. Writes variants to /tmp/ablation/SKILL-<cfg>.md
where cfg in ALL, NONE, C1, C2, C3, C4, C5.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "SKILL.md"
OUT = Path("/tmp/ablation")
OUT.mkdir(parents=True, exist_ok=True)

HEADING = re.compile(r"^(#{2,3})\s+")
MARK = re.compile(r"\[ABLATE:([A-Z0-9,]+)\]")
COMPONENTS = {"C1", "C2", "C3", "C4", "C5"}


def parse_blocks(text: str):
    lines = text.splitlines(keepends=True)
    idxs = [i for i, ln in enumerate(lines) if HEADING.match(ln)]
    blocks = []
    for j, i in enumerate(idxs):
        end = idxs[j + 1] if j + 1 < len(idxs) else len(lines)
        m = MARK.search(lines[i])
        ids = set(m.group(1).split(",")) if m else set()
        level = len(HEADING.match(lines[i]).group(1))
        blocks.append((i, end, level, ids))
    return lines, blocks


def render(variant: str) -> str:
    text = SRC.read_text(encoding="utf-8")
    lines, blocks = parse_blocks(text)

    if variant == "NONE":
        drop = set(COMPONENTS)
    elif variant == "ALL":
        drop = set()
    else:
        drop = {variant}

    removed = [False] * len(blocks)
    for idx, (_, _, _, ids) in enumerate(blocks):
        # parent ALL blocks are handled after children
        if not ids or "ALL" in ids:
            continue
        if ids & drop:
            removed[idx] = True

    for idx, (_, _, level, ids) in enumerate(blocks):
        if "ALL" not in ids:
            continue
        children = [
            j
            for j, (_, _, lv, cids) in enumerate(blocks)
            if j != idx and lv > level and cids and "ALL" not in cids
        ]
        if children and all(removed[c] for c in children):
            removed[idx] = True

    out = []
    for i, ln in enumerate(lines):
        if any(removed[idx] and start <= i < end for idx, (start, end, _, _) in enumerate(blocks)):
            continue
        # inline marker lines: whole line dropped when marker ids are dropped
        m = MARK.search(ln)
        if m and not HEADING.match(ln):
            ids = set(m.group(1).split(","))
            if ids & drop:
                continue
        out.append(ln)
    return "".join(out)


if __name__ == "__main__":
    for cfg in ("ALL", "NONE", "C1", "C2", "C3", "C4", "C5", "C6"):
        out = render(cfg)
        (OUT / f"SKILL-{cfg}.md").write_text(out, encoding="utf-8")
        n = len([l for l in out.splitlines() if l.strip()])
        print(f"SKILL-{cfg}.md: {n} non-empty lines")
