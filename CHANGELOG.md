# Changelog

All notable changes to this project are documented in this file.

## 1.0.0 - 2026-09-01

### Added

- 初始发布：半调海报 · 艺术封面技能。
- 六不变式（纸 / 墨 / 印刷布尔 / 机制 / 主体行为 / 字图音量），任何风格出图前必须六轴各取一个确定值。
- 六套风格：editorial（当代编辑印刷风）、polish（波兰海报路）、swiss（瑞士海报路）、riso_zine（孔版 zine 路）、filmstack（胶片叠层路）、archival（标本档案路）。
- 机器可校验设计系统：`design-system/` 十份 JSON（六轴 + 主体结构链 + 平台画幅 + 枚举 schema）。
- 全部验证脚本：design-system 结构校验、styles 六轴完整性校验、evals 断言校验、风格卡片渲染，`scripts/run_tests.sh` 一键全套。
- 六个结构化评测用例（`evals/evals.json`），含六轴取值与「能否指认墨色来源」的判语断言。
- 印刷机制支持：AM 半调、1-bit 剪影、photogram 高反差、胶片叠层、复印机美学。
- CI 工作流：push / PR 自动跑全套校验。

### 说明

- 示例图集（`examples/`）后续补充，版权按 `ASSET-LICENSE.md` 单独管理。