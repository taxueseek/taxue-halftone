#!/usr/bin/env python3
"""Validate evals/evals.json.

Each eval references a style that must exist in styles/, and its assertions
must agree with that style's resolved six-axes values (so the eval actually
tests "did we follow the style recipe"). Also checks the tonal gate field is
present for every eval.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS_FILE = ROOT / "evals" / "evals.json"
STYLE_DIR = ROOT / "styles"


def fail(msg):
    print(f"eval validation failed: {msg}", file=sys.stderr)
    sys.exit(1)


def load_style(style_id):
    p = STYLE_DIR / f"{style_id}.json"
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def main():
    with EVALS_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
    if data.get("schema_version") != 1:
        fail("evals must use schema_version 1")

    evals = data.get("evals", [])
    if len(evals) < 6:
        fail("need at least 6 evals (one per style)")

    ids = [e.get("id") for e in evals]
    if len(ids) != len(set(ids)):
        fail("eval ids must be unique")

    for ev in evals:
        eid = ev.get("id")
        style_id = ev.get("style")
        st = load_style(style_id)
        if st is None:
            fail(f"eval {eid}: style '{style_id}' not found in styles/")

        a = ev.get("assertions", {})
        if "tonal_gate" not in a:
            fail(f"eval {eid}: missing tonal_gate assertion")

        axes = st.get("six_axes", {})
        # mechanism / ground / volume must agree
        for key in ("mechanism", "ground", "volume", "behavior"):
            if key in a and a[key] != axes.get(key):
                fail(f"eval {eid}: {key} assertion {a[key]} != style {axes.get(key)}")

        # ink hexes vs style ink roles
        if "ink_hexes" in a:
            style_hexes = []
            for k in ("primary", "accent"):
                pl = axes.get("ink_role", {}).get(k)
                if pl and pl.get("hex"):
                    style_hexes.append(pl["hex"])
            if set(a["ink_hexes"]) != set(style_hexes):
                fail(f"eval {eid}: ink_hexes {a['ink_hexes']} != style {style_hexes}")

        # mode
        if "mode" in a and a["mode"] != axes.get("ink_role", {}).get("mode"):
            fail(f"eval {eid}: mode {a['mode']} != style mode")

            # empty_paper range within style's declared emptiness
        if "empty_paper_range" in a and "empty_paper" in st:
            lo, hi = a["empty_paper_range"]
            slo, shi = st["empty_paper"]
            if not (slo <= lo and hi <= shi):
                fail(f"eval {eid}: empty_paper_range {a['empty_paper_range']} outside style {st['empty_paper']}")

    print(f"eval validation PASSED ({len(evals)} evals)")


if __name__ == "__main__":
    main()
