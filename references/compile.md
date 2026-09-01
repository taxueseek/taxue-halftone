# 提示词编译（五段）

按此顺序写成英文可执行 prompt（画面内非拉丁文逐字引号保留）：

1. **Canvas and ink** — ratio; Ground as ink 0 + Ink/Mist hex; print mode; mechanism (默认 AM); angles/dot shape if AM; viewing distance (fuse OR texture, not both); every overlap as knockout|overprint|trap; crush mids then screen; flat front-facing page (no mockup).
2. **Composition** — layout family; photo_role (window|object|cutout|film-layer|solarized-slab); volume-mix (type loud / photo quiet or reverse); one focal event; one release zone; margins; empty-paper %; crop for leftover type pocket; one manual gesture.
3. **Subject** — subject chain first（见 subject.json）; photo_role first. window = scene through a plate; object = photo as a cut thing on a field; cutout = edge is the frame; film-layer = type and photo share one stack; solarized-slab = 2–3 printable values. faithful: preserve identity, crop, screening, paper knockouts. Abstract: 2–4 identity anchors → mass + contour + rhythm; paper cuts through ≥35% of source scene. Faces: round dots, highlight knockout to paper, no elliptical.
4. **Typography** — hierarchy; voices; EXACT display text in original language inside quotes; how type crosses/covers/splits the object. Or type-off empty band. Image screened, type solid unless stroke ≥ 2–3 dot pitches. type-in 是印刷事件（墨量 / 层 / 一处「破」），不是字体名.
5. **Material and avoids** — 该机制的痕迹（AM dots 或 1-bit 颗粒 / 平阶硬边 / 凸版压痕，勿堆）；fibers; bleed; 1–2mm registration; shadows 70–90% open; hard negatives (no third ink, no gradient, no same-angle plates, no type-and-image same screen, no stock hero, no auto-vintage, no fake CMYK Riso).

锁定句 2–3 条：只写最易翻车且能画的事。必须能回答「哪支墨、哪个角或哪一层、纸在哪」。正向。

机制不是 AM 时：第 5 段改写为该机制的痕迹（1-bit 颗粒/硬阈值；平阶孔版硬边；凸版压痕与露纸牙），不要仍写 coarse AM。

type-in：把字写成印刷事件（ink weight、layer under/same/over、at most one break），禁止只写字体名。字越大墨越淡。CJK 仍优先 type-off。

## 元提示词槽位

```
主题：{主题}          # 唯一必填
比例：{比例}          # 默认 3:4
语言：{语言}          # 显示文案语言；默认=用户语言
文案：{文案}          # 可空=按语言发明 2–8 字/词；填 none=无字
风格：{风格}          # 见 styles/*.json
场景：{场景 id}       # 见 references/scenes.md
```

附 ≥3 个主题填法对照 + 哪些段不动。
