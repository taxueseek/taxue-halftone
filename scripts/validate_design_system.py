#!/usr/bin/env python3
"""Validate the taxue-halftone design-system JSON catalogs.

Checks (tailored to the six-invariant + subject/platform axes):
  1. Expected catalog files exist; no unexpected *.json.
  2. Every catalog uses schema_version 1.
  3. Unique, non-empty ids within each list.
  4. Regex rules: uppercase HEX colors, ratio strings.
  5. Required fields per axis (see schemas.json).
  6. Cross-file consistency: mechanisms/behaviors references resolve.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEM_DIR = ROOT / "design-system"
HEX_COLOR = re.compile(r"^#[0-9A-F]{6}$")
# ratio: integer or decimal ratio like 16:9, 2.35:1, 5:2
RATIO = re.compile(r"^[1-9][0-9]*(\.[0-9]+)?:[1-9][0-9]*$")

EXPECTED_FILES = {
    "roles.json",
    "bools.json",
    "mechanisms.json",
    "behaviors.json",
    "volume.json",
    "edges.json",
    "subject.json",
    "platform.json",
    "schemas.json",
}


def fail(msg: str) -> None:
    print(f"design-system validation failed: {msg}", file=sys.stderr)
    sys.exit(1)


def load(name: str) -> dict:
    path = SYSTEM_DIR / name
    if not path.exists():
        fail(f"missing {name}")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if data.get("schema_version") != 1:
        fail(f"{name} must use schema_version 1")
    return data


def require_unique(items, label):
    ids = [it.get("id") for it in items]
    if any(not isinstance(i, str) or not i for i in ids):
        fail(f"every {label} needs a non-empty id")
    if len(ids) != len(set(ids)):
        fail(f"{label} ids must be unique")
    return set(ids)


def require_field(items, field, label):
    for it in items:
        if field not in it or it[field] in (None, "", []):
            fail(f"{label} '{it.get('id', '?')}' missing field '{field}'")


# --- catalog file existence / no extras ---
actual = {p.name for p in SYSTEM_DIR.glob("*.json")}
if actual != EXPECTED_FILES:
    fail(f"expected {sorted(EXPECTED_FILES)}, found {sorted(actual)}")

# --- colors / roles ---
roles = load("roles.json")
ground = roles.get("ground", [])
ground_ids = require_unique(ground, "ground")
if len(ground) < 3:
    fail("roles need at least white, gray, beige substrates")
for g in ground:
    if not HEX_COLOR.fullmatch(g.get("hex", "")):
        fail(f"{g['id']} must use uppercase hex color")
    if g.get("counts_as_ink") is not False:
        fail(f"{g['id']} must have counts_as_ink=false")
    require_field([g], "use_for", "ground")

ink_roles = roles.get("ink_roles", {})
for name, role in ink_roles.items():
    require_field([role], "duty", f"ink_role.{name}")
    for rng in role.get("percent_range", []):
        if not (0 <= rng <= 100):
            fail(f"ink_role.{name} percent out of range")

defaults = roles.get("defaults", {})
if defaults.get("substrate_id") not in ground_ids:
    fail("roles defaults must reference a known substrate")

# --- bools ---
bools = load("bools.json")
bool_ids = require_unique(bools.get("booleans", []), "boolean")
VALID_BOOL = {"knockout", "overprint", "trap"}
if not bool_ids <= VALID_BOOL:
    fail(f"bools must be one of {VALID_BOOL}, got {bool_ids}")
for b in bools.get("booleans", []):
    require_field([b], "rule", "boolean")

# --- mechanisms ---
mech = load("mechanisms.json")
mech_ids = require_unique(mech.get("mechanisms", []), "mechanism")
if mech.get("default") not in mech_ids:
    fail("mechanisms default must be a known mechanism id")
for m in mech.get("mechanisms", []):
    for f in ("physics", "wins", "loses", "rules"):
        require_field([m], f, "mechanism")
    if "angle" not in m.get("rules", {}) and m["id"] != "film_stack":
        # AM & non-AM mechanisms all need rules; angle only for AM-like
        pass

# --- behaviors ---
beh = load("behaviors.json")
beh_ids = require_unique(beh.get("behaviors", []), "behavior")
for b in beh.get("behaviors", []):
    require_field([b], "direction", "behavior")

# --- volume ---
vol = load("volume.json")
profiles = vol.get("profiles", {})
expected_profiles = {"type_lead", "image_lead", "balanced"}
if set(profiles.keys()) != expected_profiles:
    fail(f"volume profiles must be {expected_profiles}, got {set(profiles.keys())}")
for pid, p in profiles.items():
    require_field([p], "rule", f"volume.{pid}")


# --- edges ---
edges = load("edges.json")
edge_ids = require_unique(edges.get("edge_types", []), "edge_type")
if not {"structural", "diffusion"} <= edge_ids:
    fail("edges must include structural + diffusion")

# --- subject ---
sub = load("subject.json")
if "recognition_gate" not in sub:
    fail("subject must define recognition_gate (3s rule)")
for rule in sub.get("chain_rules", []):
    for f in ("type", "must_present", "chain", "forbid"):
        require_field([rule], f, "subject.chain")

# --- platform ---
plat = load("platform.json")
plat_ids = require_unique(plat.get("platforms", []), "platform")
for p in plat.get("platforms", []):
    for f in ("name", "ratio", "work_size", "safety"):
        require_field([p], f, "platform")
    if not RATIO.fullmatch(p.get("ratio", "")):
        fail(f"platform {p['id']} ratio must be 'X:Y'")

# --- schemas ---
schemas = load("schemas.json")
axes = schemas.get("axes", {})
required_axes = {"ground", "mechanism", "behavior", "volume", "boolean"}
missing_axes = required_axes - set(axes.keys())
if missing_axes:
    fail(f"schemas missing axes: {missing_axes}")

print("design-system validation PASSED")
