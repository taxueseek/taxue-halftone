#!/usr/bin/env python3
"""Render a visual style card (SVG) for one style in styles/.

Produces a compact swatch showing: the substrate + ink(s) + mechanism
signature, so the six-axes recipe is visually inspectable alongside the
prompt. No external assets needed; pure stdlib + svg string.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_DIR = ROOT / "styles"
SW_DIR = ROOT / "swatches"
DS_DIR = ROOT / "design-system"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def load_json(p):
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def render(style_path):
    s = load_json(style_path)
    sid = s["style_id"]
    name = s["name"]
    axes = s["six_axes"]

    # ground color
    ground = load_json(DS_DIR / "roles.json")
    g = next((x for x in ground["ground"] if x["id"] == axes["ground"]), None)
    g_hex = g["hex"] if g else "#FAFAF7"

    inks = []
    for key in ("primary", "accent"):
        plate = axes.get("ink_role", {}).get(key)
        if plate and plate.get("hex"):
            inks.append(plate["hex"])

    mech = axes.get("mechanism")
    beh = axes.get("behavior")
    vol = axes.get("volume", {})

    w, h = 380, 240
    sw = 90
    x0 = 24
    y0 = 60
    # substrate rectangle
    parts = []
    parts.append(f'<rect x="{x0}" y="{y0}" width="{w-48}" height="120" fill="{g_hex}" stroke="#999" stroke-width="1"/>')
    # ink bands
    for i, c in enumerate(inks):
        x = x0 + i * (sw + 6)
        parts.append(f'<rect x="{x}" y="{y0}" width="{sw}" height="120" fill="{c}" opacity="0.85"/>')
        parts.append(f'<text x="{x+sw/2}" y="{y0+140}" font-size="11" fill="#333" text-anchor="middle">{c}</text>')

    parts.append(f'<text x="{x0}" y="28" font-size="15" font-weight="bold" fill="#222">{name}</text>')
    parts.append(f'<text x="{x0}" y="44" font-size="11" fill="#666">mech={mech} · behavior={beh} · volume={vol}</text>')
    parts.append(f'<text x="{x0}" y="{y0+170}" font-size="11" fill="#444">{s.get("signature", "")[:70]}</text>')

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"
    out = SW_DIR / f"{sid}.svg"
    out.write_text(svg, encoding="utf-8")
    return out


def main():
    SW_DIR.mkdir(parents=True, exist_ok=True)
    target = sys.argv[1] if len(sys.argv) > 1 else None
    paths = []
    if target:
        p = STYLE_DIR / f"{target}.json"
        if not p.exists():
            print(f"style '{target}' not found", file=sys.stderr)
            sys.exit(1)
        paths = [p]
    else:
        paths = sorted(STYLE_DIR.glob("*.json"))
    for p in paths:
        out = render(p)
        print(f"rendered {out}")
    print(f"done: {len(paths)} style card(s)")


if __name__ == "__main__":
    main()
