#!/usr/bin/env python3
"""Validate every style in styles/*.json resolves the six invariants.

A "style" must:
  * declare a value for each of the six invariants (ground/ink_role/boolean/
    mechanism/behavior/volume) — this is what makes it "规范";
  * reference ids that exist in design-system (mechanism, behavior, ground);
  * keep ≤2 inks (third only via overprint), with quantified percents.
Missing any axis => the style is not a complete style (not 鲜明).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_DIR = ROOT / "styles"
DS = ROOT / "design-system"

HEX_COLOR = re.compile(r"^#[0-9A-F]{6}$")
REQUIRED_AXES = ["ground", "ink_role", "boolean", "mechanism", "behavior", "volume"]


def fail(msg):
    print(f"style validation failed: {msg}", file=sys.stderr)
    sys.exit(1)


def load_ds(name):
    with (DS / name).open(encoding="utf-8") as f:
        return json.load(f)


def valid_ids(ds, key):
    items = ds.get(key, [])
    return [it.get("id") for it in items]


def main():
    styles = sorted(STYLE_DIR.glob("*.json"))
    if not styles:
        fail("no styles found in styles/")

    mech_ids = set(valid_ids(load_ds("mechanisms.json"), "mechanisms"))
    beh_ids = set(valid_ids(load_ds("behaviors.json"), "behaviors"))
    ground_ids = set(it["id"] for it in load_ds("roles.json").get("ground", []))
    bool_ids = set(it["id"] for it in load_ds("bools.json").get("booleans", []))
    vol_profiles = set(load_ds("volume.json").get("profiles", {}).keys())

    for path in styles:
        with path.open(encoding="utf-8") as f:
            s = json.load(f)
        if s.get("schema_version") != 1:
            fail(f"{path.name} must use schema_version 1")
        sid = s.get("style_id")
        if not sid:
            fail(f"{path.name} missing style_id")

        # 1) six axes resolved
        axes = s.get("six_axes", {})
        missing = [a for a in REQUIRED_AXES if a not in axes]
        if missing:
            fail(f"{sid} missing axes: {missing}")

        # 2) cross-reference existence
        mech = axes.get("mechanism")
        if mech not in mech_ids:
            fail(f"{sid} mechanism '{mech}' not in mechanisms.json")

        beh = axes.get("behavior")
        if beh not in beh_ids:
            fail(f"{sid} behavior '{beh}' not in behaviors.json")

        ground = axes.get("ground")
        if ground not in ground_ids:
            fail(f"{sid} ground '{ground}' not in roles.json")

        boolean = axes.get("boolean")
        if boolean not in bool_ids:
            fail(f"{sid} boolean '{boolean}' not in bools.json")

        vol = axes.get("volume")
        if vol not in vol_profiles:
            fail(f"{sid} volume '{vol}' not in volume.json")

        # 3) ink role quantified & ≤2 inks
        ink = axes.get("ink_role", {})
        hexes = []
        for key in ("primary", "accent"):
            plate = ink.get(key)
            if plate:
                h = plate.get("hex")
                if h and not HEX_COLOR.fullmatch(h):
                    fail(f"{sid} ink.{key} has invalid hex '{h}'")
                if h:
                    hexes.append(h)
                pr = plate.get("percent")
                if pr:
                    if not isinstance(pr, list) or len(pr) != 2:
                        fail(f"{sid} ink.{key} percent must be [min,max]")
                    lo, hi = pr
                    if not (0 <= lo <= hi <= 100):
                        fail(f"{sid} ink.{key} percent {pr} out of range")
                duty = plate.get("duty", "")
                if not duty:
                    fail(f"{sid} ink.{key} needs a duty")
        if len(hexes) > 2:
            fail(f"{sid} uses more than two inks: {hexes}")

        # 4) mode consistency
        mode = ink.get("mode", "")
        if mode not in {"pure_one_ink", "chromatic_plus_black", "complementary_duotone", "overprint_duotone"}:
            fail(f"{sid} invalid ink mode '{mode}'")
        if mode == "pure_one_ink" and len(hexes) != 1:
            fail(f"{sid} pure_one_ink but got {len(hexes)} inks")

        # 5) emptiness & subject chain guard
        if "empty_paper" in s:
            ep = s["empty_paper"]
            if not isinstance(ep, list) or len(ep) != 2 or not (0 <= ep[0] <= ep[1] <= 100):
                fail(f"{sid} empty_paper {ep} invalid")

    print(f"style validation PASSED ({len(styles)} styles)")


if __name__ == "__main__":
    main()
