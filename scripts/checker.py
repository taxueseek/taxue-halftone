#!/usr/bin/env python3
"""Deterministic ablation checker for taxue-halftone.

Scores one run (recipe yaml + prompt + optional diagnosis card) against:
  1. recipe field completeness (config-aware)
  2. six-axis value legality vs design-system catalogs
  3. named anti-pattern scan on the prompt
  4. diagnosis -> axis consistency rules
Writes per-run JSON result to stdout.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DS = ROOT / "design-system"

FIELDS = [
    "subject", "subject_chain", "intent", "exact_text", "text_language",
    "representation", "source_policy", "ground", "ink_role", "boolean",
    "mechanism", "behavior", "volume", "ratio", "viewing_distance", "layout",
    "tension", "focal_event", "release_zone", "avoid_named_patterns",
]
OPTIONAL_FIELDS = ["diagnosis", "priority_fix"]

ANTI_SIGNALS = {
    "third-color-leak": ["第三色", "第三色相", "第三种颜色", "new hex", "third ink"],
    "gradient-masquerade": ["渐变", "gradient", "smooth blend", "airbrush", "soft blur"],
    "neon-spray": ["霓虹", "荧光", "neon", "glow"],
    "full-color-photo": ["全彩", "full color", "full-colour", "四色"],
    "auto-vintage": ["做旧", "泛黄", "复古做旧", "sepia", "grain+scratch", "咖啡渍", "coffee stain"],
    "fake-cmyk-riso": ["CMYK", "四色印刷", "cmyk"],
    "same-angle-stack": ["同角", "same angle", "moiré", "摩尔纹"],
    "color-halftone-on-rgb": ["滤镜", "Color Halftone filter", "滤镜套"],
    "mechanism-as-mood": ["Riso 风", "riso vibe", "duotone vibes", "胶片感", "滤镜感"],
    "centered-template": ["居中", "centered", "对称", "中心对齐"],
    "same-screen-type": ["字图同网", "碎字", "same screen"],
    "logo-qr-screen": ["logo 加网", "二维码加网", "qr screen"],
    "stock-hero": ["英雄人像", "hero portrait", "完整人像面向镜头"],
    "reference-reprint": ["复刻", "照搬", "复制原图", "reprint", "原样复制"],
    "sticker-collage": ["贴纸", "圆角贴纸", "sticker"],
    "retro-movie-medley": ["拼盘", "medley", "星战拼盘", "电影海报拼盘"],
    "sales-cta": ["抢购", "立即购买", "限时", "buy now", "CTA"],
    "vector-flat": ["矢量平涂", "扁平插画", "flat vector"],
}


def load_json(name: str) -> dict:
    return json.loads((DS / name).read_text(encoding="utf-8"))


def validate_axis(recipe: str) -> list[str]:
    issues = []
    low = recipe.lower()
    # mechanism
    mechs = {m["id"] for m in load_json("mechanisms.json")["mechanisms"]}
    names = re.findall(r"mechanism:\s*([A-Za-z0-9_-]+)", recipe)
    mech = names[-1] if names else None
    if mech is None or mech not in mechs:
        issues.append(f"mechanism invalid/missing: {mech}")
    # behavior (normalize - to _)
    behavs = {b["id"] for b in load_json("behaviors.json")["behaviors"]}
    names = [n.replace("-", "_") for n in re.findall(r"behavior:\s*([A-Za-z0-9_-]+)", recipe)]
    beh = names[-1] if names else None
    if beh is None or beh not in behavs:
        issues.append(f"behavior invalid/missing: {beh}")
    # volume
    vols = set(load_json("volume.json")["profiles"].keys())
    names = re.findall(r"volume:\s*([A-Za-z0-9_-]+)", recipe)
    vol = names[-1] if names else None
    if vol is None or vol not in vols:
        issues.append(f"volume invalid/missing: {vol}")
    # boolean
    bools = {b["id"] for b in load_json("bools.json")["booleans"]}
    names = re.findall(r"boolean:\s*([A-Za-z0-9_-]+)", recipe)
    bo = names[-1] if names else None
    if bo is None or bo not in bools:
        issues.append(f"boolean invalid/missing: {bo}")
    # ground
    grounds = {g["id"] for g in load_json("roles.json")["ground"]}
    names = re.findall(r"ground:\s*(ground_[A-Za-z0-9_-]+)", recipe)
    gr = names[-1] if names else None
    if gr is None or gr not in grounds:
        issues.append(f"ground invalid/missing: {gr}")
    return issues


def body_paragraphs(prompt: str) -> str:
    """Prompt is five paragraphs; the 5th lists hard negatives by design.
    Anti-pattern scan applies to paragraphs 1-4 only (a mention inside the
    avoid-list is a correct usage, not a signal)."""
    # split on leading "1." "2." ... or "N. " or "Segment N" markers
    parts = re.split(r"\n\s*(?=\d+\.\s|[A-Z]{3,6}\s*\d+\s*[—–-]\s)", prompt)
    # fallback: numeric sentence starts
    if len(parts) < 5:
        starts = [m.start() for m in re.finditer(r"(?m)^\s*(?:\d+\.|[A-Z]+ \d+[—–-])", prompt)]
        if len(starts) >= 5:
            parts = [prompt[starts[i]: starts[i + 1] if i + 1 < len(starts) else None] for i in range(len(starts))]
    if len(parts) >= 5:
        return " ".join(parts[:4])
    return prompt


NEG_WORDS = ("no ", "never", "without", "not ", "avoid", "do not", "禁止", "不要", "不用", "no-", "rather than")


def is_negated(text: str, idx: int) -> bool:
    window = text[max(0, idx - 30): idx]
    return any(word in window for word in NEG_WORDS)


def scan_anti(recipe: str, prompt: str) -> list[str]:
    body = body_paragraphs(prompt)
    hits = []
    for name, signals in ANTI_SIGNALS.items():
        for sig in signals:
            idx = body.lower().find(sig.lower())
            if idx >= 0 and not is_negated(body.lower(), idx):
                hits.append(f"{name}('{sig}')")
                break
    return hits


def consistency(diag: str, recipe: str) -> list[str]:
    issues = []
    if not diag or diag.strip() in ("", "none", "null"):
        return []
    low = diag.lower()
    names = [n.replace("-", "_") for n in re.findall(r"behavior:\s*([A-Za-z0-9_-]+)", recipe)]
    beh = names[-1] if names else None
    if ("水平" in diag or "horizontal" in low) and beh != "horizon":
        issues.append(f"axis=horizontal but behavior={beh}")
    if ("垂直" in diag or "vertical" in low) and beh != "vertical_extend":
        issues.append(f"axis=vertical but behavior={beh}")
    names = [n.replace("-", "_") for n in re.findall(r"volume:\s*([A-Za-z0-9_-]+)", recipe)]
    vol = names[-1] if names else None
    m = re.search(r"subject_occupancy:\s*([<>]?\s*\d+%|[<>\s]+\s*25%|25–50%|>50%|<25%)", diag)
    if m:
        val = m.group(1).replace(" ", "")
        if val in ("<25%", "<25%"):
            if vol != "type_lead":
                issues.append(f"occupancy<25% but volume={vol}")
        elif val in (">50%", ">50%"):
            if vol != "image_lead":
                issues.append(f"occupancy>50% but volume={vol}")
    # defect handling: 歪斜 -> 扶正/crop in priority_fix or prompt
    if re.search(r"歪斜|倾斜", diag):
        if not re.search(r"扶正|校正|correct|straighten|crop", recipe + " " + diag):
            issues.append("defect=skew but no fix action found")
    return issues


def score(run: dict, cfg: str) -> dict:
    recipe = run.get("recipe", "")
    prompt = run.get("prompt", "")
    diag = run.get("diagnosis_card") or ""
    present = [f for f in FIELDS if re.search(rf"(?m)^{f}:", recipe)]
    missing = [f for f in FIELDS if f not in present]
    opt_missing = [f for f in OPTIONAL_FIELDS if not re.search(rf"(?m)^{f}:", recipe)]
    axis_issues = validate_axis(recipe)
    anti = scan_anti(recipe, prompt)
    cons = consistency(diag, recipe)
    return {
        "cfg": cfg,
        "fields_present": len(present),
        "fields_total": len(FIELDS),
        "missing_fields": missing,
        "axis_issues": axis_issues,
        "anti_pattern_hits": anti,
        "consistency_issues": cons,
        "has_diagnosis": bool(diag and diag.strip() not in ("none", "null")),
        "has_priority_fix": bool(re.search(r"(?m)^priority_fix:", recipe)),
        "prompt_len": len(prompt),
        "recipe_len": len(recipe),
        "ok": not (missing or axis_issues),
    }


if __name__ == "__main__":
    path = Path(sys.argv[1])
    cfg = sys.argv[2]
    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(score(data, cfg), ensure_ascii=False, indent=2))
