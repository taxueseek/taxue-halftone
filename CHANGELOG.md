# Changelog

All notable changes to this project are documented in this file.

## 1.1.0 - 2026-09-03

### Added

- 第七套风格 imperfect_collage（不完美印刷拼贴）：撕纸拼贴三层结构，专色场 + 黑白半调主体，上图下卡，有意的不完美。
- 第八套风格 dot_dissolve（点阵解构海报路）：复古丝网圆点阵，具象主体解构为点阵、颗粒与流动波纹，粗体字融入点阵场，标点极简（正文与标题仅逗号句号）；内置元提示词模板与槽位填充规则，主题为唯一必填。
- 第九套风格 paper_cut_group（中式剪纸路）：剪纸剪影群像层层交错，细节全靠白色负空间镂空，一枚跳色例外成员，上图下卡；内置元提示词模板与槽位推演规则，主题为唯一必填。
- 第七种印刷机制 paper_cut_collage（剪纸拼贴）：刀口轮廓 + 负空间镂空，无网点无投影，与撕纸拼贴（torn_paper_collage）签名不混用。
- 第十套风格 paper_cut_halftone（点阵剪纸路）：点阵解构与中式剪纸的混搭，剪纸窗花轮廓 + 粗圆 AM 网点铺形，暗部 70–90%不断网，跳色克制（默认灰陶），用色倾向单色克制/主色配底色两色/主色底色跳色三色三选一，上图下卡；内置元提示词模板与槽位推演规则，主题为唯一必填。
- 评测用例补到第 7–10 条（`evals/evals.json`）与色卡 `swatches/imperfect_collage.svg`、`swatches/dot_dissolve.svg`、`swatches/paper_cut_group.svg`、`swatches/paper_cut_halftone.svg`。
- 全套校验通过：design-system 结构、10 风格六轴完整性、10 条 evals 断言一致（`scripts/run_tests.sh` 3/3）。
- 点阵解构三张实测样张（雾中灯塔、深海之灯、风花雪月）与点阵剪纸一张实测样张（海阔天空），入 `examples/` 并同步 README（中英）示例区与示例图集清单。
- README（中英）新增「随机性与创造力」一节：Design Skill 刻意不做僵化约束、不追求复刻固定效果，同一提示词在 GPT Image 2、Grok Imagine 2、Nano Banana 2、Seedream 5.0 Pro 上风格会有较大不同；模型建议——主力 GPT Image 2、Grok Imagine 2，后备 Nano Banana 2、Seedream 5.0 Pro。

### Changed

- 辅墨量化口径补充：职务极小的辅墨可下探（paper_cut_group 跳色成员 5–10%；paper_cut_halftone 前两档用色倾向不启用跳色记 0%，第三档三色倾向启用跳色 ≤10%）（DESIGN.md §四）。
- 风格更名（style_id 不变）：中式剪纸群像路→中式剪纸路，网点剪纸群像路→点阵剪纸路——实测效果为点阵解构与中式剪纸的混搭，旧名未体现；README（中英）、SKILL.md、evals、术语反查、DESIGN.md、色卡同步。
- SKILL.md、README（中英）、术语反查表、DESIGN.md 与入口桥同步为十风格。

## 1.0.0 - 2026-09-01

### Added

- 初始发布：半调海报 · 艺术封面技能。
- 六不变式（纸 / 墨 / 印刷布尔 / 机制 / 主体行为 / 字图音量），任何风格出图前必须六轴各取一个确定值。
- 六套风格：editorial（复古编辑印刷风）、polish（波兰海报路）、swiss（瑞士海报路）、riso_zine（孔版 zine 路）、filmstack（胶片叠层路）、archival（标本档案路）。
- 机器可校验设计系统：`design-system/` 十份 JSON（六轴 + 主体结构链 + 平台画幅 + 枚举 schema）。
- 全部验证脚本：design-system 结构校验、styles 六轴完整性校验、evals 断言校验、风格卡片渲染，`scripts/run_tests.sh` 一键全套。
- 六个结构化评测用例（`evals/evals.json`），含六轴取值与「能否指认墨色来源」的判语断言。
- 印刷机制支持：AM 半调、1-bit 剪影、photogram 高反差、胶片叠层、复印机美学。
- CI 工作流：push / PR 自动跑全套校验。

### 说明

- 示例图集（`examples/`）后续补充，版权按 `ASSET-LICENSE.md` 单独管理。
