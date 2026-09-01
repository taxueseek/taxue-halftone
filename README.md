<div align="center">

# taxue-halftone · 半调海报

**限墨不是滤镜，是可校验的印版系统。**

用 ≤2 支墨和网点，把任意主题做成有结构、有质感、可复用的艺术封面。

[![Version](https://img.shields.io/badge/VERSION-1.0.0-2ea44f?style=flat-square&labelColor=333)](./CHANGELOG.md)
[![Skills](https://img.shields.io/badge/SKILLS-1-2ea44f?style=flat-square&labelColor=333)](./SKILL.md)
[![Stars](https://img.shields.io/github/stars/taxueseek/taxue-halftone?style=flat-square&label=STARS&color=e37f2c&labelColor=333)](https://github.com/taxueseek/taxue-halftone/stargazers)
[![Validate](https://github.com/taxueseek/taxue-halftone/actions/workflows/validate.yml/badge.svg)](https://github.com/taxueseek/taxue-halftone/actions/workflows/validate.yml)
[![SKILL.md](https://img.shields.io/badge/Agent-SKILL.md-214f9b?style=flat-square&labelColor=333)](./SKILL.md)

</div>

> **判语**：如果无法指出每块颜色来自哪支墨、哪个角或哪一层阶、纸在哪里露出，就还不是本系统。

无论选哪种印刷机制，一张图都必须先回答六个互斥且穷尽的问题（纸、墨、叠印、机制、主体走向、字图音量），缺一则不是本系统。风格不是「把某个滤镜套上去」，而是六轴各取一组确定值形成的指纹组合。输入一句话、一个主题或一张照片，输出一张可校验的印刷风艺术封面，连同它的完整配方。

## 示例作品

> 图集待补充：本区图片按 `examples/` 目录预留，由技能实际出图后挂入（版权见 [ASSET-LICENSE.md](./ASSET-LICENSE.md)）。

| 待补充 | 待补充 | 待补充 |
|:---:|:---:|:---:|
| 示例图 1 | 示例图 2 | 示例图 3 |

## 它是什么

| 系统 | 方向 |
|---|---|
| **输入** | 一句话、一个主题、一个词，或一张提供的照片 |
| **油墨** | 单墨或受控双墨；主墨 70–85%，辅墨 15–30% 且必须有一份具体职务 |
| **纸** | 中性白 / 冷灰 / 浅米，随图像与墨色对比自适应；纸不算第三色 |
| **机制** | AM 半调、1-bit 剪影、photogram 高反差、胶片叠层、复印机美学；一次一个 |
| **字图音量** | 字大声则图退，图大声则字退；禁止双开 |
| **空纸** | 25–55% 可见纸面（孔版 zine 路 70–90%），留白是构图的一部分 |
| **输出** | 生成的图 + 可直接复用的完整提示词 + 一份命名印版、色墨、版式、字声、机制、原创性变更的配方 |

## 六不变式（出图先答六个问题）

任何一张图，任何风格，六轴各取一个确定值。轴内取值模糊，图不鲜明。

| # | 轴 | 必须回答 | 量化约束 |
|---|---|---|---|
| 1 | 纸（Ground） | 纸是哪一块、什么色 | 底衬色不算墨；暗底白衬必须 choke |
| 2 | 墨（Ink / Mist） | 哪几支墨、各干什么 | 主 70–85%，辅/雾各 1 职务 |
| 3 | 印刷布尔 | 两色相交怎么处理 | knockout / overprint / trap 三选一 |
| 4 | 机制 | 用什么印刷机制 | 一次一个；机制内角/点/密度须有结构 |
| 5 | 主体行为 | 图的「势」往哪走 | still / dissipate / densify / horizon / vertical-extend |
| 6 | 字图音量 | 字和图的音量谁大 | 字大声则图退；禁止双开 |

七轴外还有两个独立约束系统：主体结构链（`subject.json`，决定主体能否 3 秒认出）和平台画幅（`platform.json`，决定画幅是否被裁坏）。它们不改变六轴取值。

## 风格与色票

六套风格 = 六轴指纹组合。每套风格有专属色墨、机制、行为与平台偏好：

| 风格 | 色票 | 六轴取值 | 常用平台 |
|---|---|---|---|
| **editorial** 当代编辑印刷风 | ![editorial](./swatches/editorial.svg) | Cobalt `#2148B8` + Terracotta `#C65F38`，AM 半调，overprint，一物主导 45–80%，字撞物一次碰撞 | 小红书 3:4、B站 16:9、公众号 2.35:1 |
| **polish** 波兰海报路 | ![polish](./swatches/polish.svg) | Charcoal `#30343A` 单墨，photogram 高反差，字即物，空纸 35–55% | B站 16:9、超宽 5:2 |
| **swiss** 瑞士海报路 | ![swiss](./swatches/swiss.svg) | Signal Red `#C83232` + Charcoal `#30343A`，清晰摄影阶调、实色字、大量纸白 | B站 16:9、公众号 2.35:1、超宽 5:2 |
| **riso_zine** 孔版 zine 路 | ![riso_zine](./swatches/riso_zine.svg) | Botanical `#008A4B` + Aubergine `#63365F`，主体小、空纸 70–90%，当代纸不做旧 | 小红书 3:4、头像 1:1 |
| **filmstack** 胶片叠层路 | ![filmstack](./swatches/filmstack.svg) | Ultramarine `#263E99` + Safety Orange `#E55D2B`，粗网本身是图形，不规则宽边 | B站 16:9、公众号 2.35:1 |
| **archival** 标本档案路 | ![archival](./swatches/archival.svg) | Botanical `#008A4B` + Charcoal `#30343A`，标题 + 规整图像板 + 多栏图注 | 小红书 3:4、公众号 2.35:1 |

色墨换算：纸 = Ground 不算第三色；双色叠印变深不算第三墨；Mist 是主墨浅阶或叠印密度，不算第三色相。辅墨必须有职务（日期、注释、一个物件、一处叠印交叉），禁止把第二色当装饰洒满页。

## 适合做什么

- 海报：活动、派对、展览、城市漫游、概念海报
- 平台封面：小红书封面、公众号头图、播客封面、B站封面、头像、超宽头图
- 品牌物料：明信片、邀请函、门票、菜单、包装贴纸
- 纪念物：旅行手账、相册封面、周年卡
- 书刊：封面、扉页、章节页、zine 内页
- 文字：文学摘句、诗歌、个人宣言

想直接做「半调海报、艺术封面、网点、孔版、双色、Riso、木刻、蓝晒、复印机美学」的封面，说用途就行，它按六轴配好再出图。

## 不是这个

- 不是全彩照片加个单色滤镜
- 不是两色随意装饰，也不是超过两支印版
- 不是光滑样机、3D 渲染、渐变海报、电影场景
- 不是居中模板、卡片网格、贴纸拼贴、装饰性色块系统
- 不是密集拼贴做旧或撕纸风格
- 不是一用半调/限墨就自动泛黄、怀旧、做旧
- 不是营销文案、虚构品牌、假赞助、URL、二维码
- 不是复刻任何参考海报或艺术家签名
- 不是把 Riso（印刷机）和 Halftone（加网）当可互换的滤镜名

## 怎么工作

```text
1  接案并重定义     →  主体、用途、文字、图与字的角色，六轴配方
2  印版推导         →  单墨或双色，辅墨必须有职务，写死 HEX
3  构图语序         →  一物主导，字撞物，纸切入图像，一个手工手势
4  编译提示词       →  按 compile.md 五段式编成完整可执行指令
5  出图前校验       →  跑 validate_styles.py，六轴取值齐全且引用存在
6  出图后自检       →  逐项对照，失败只重生一次只改一项
```

## 开始使用

```bash
npx skills add taxueseek/taxue-halftone
```

装好后直接说上面任何一句，或在对话中触发 `/taxue-halftone`。

## 工程校验

「规范」落到机器可校验的数据层：六轴在 `design-system/` 各有 JSON，风格在 `styles/` 是六轴的取值组合，评测用例在 `evals/`。改任一轴，全套校验挡着。

```bash
scripts/run_tests.sh                      # 全套：design-system 结构 + styles 六轴完整性 + evals 断言
scripts/validate_styles.py <style_id>     # 校验单个风格是否六轴齐全、引用存在
scripts/render_style_card.py <style_id>   # 生成 swatches/ 可视化色票
```

PR 和 push 自动跑 CI（`.github/workflows/validate.yml`），坏了会直接标红。

## 更新记录

- **v1.0.0**（2026-09-01）：初始发布。六不变式 + 六套风格 + 机器可校验设计系统 + 全套验证脚本 + 六个评测用例。详见 [CHANGELOG.md](./CHANGELOG.md)。

## License

代码与技能内容按 [MIT License](./LICENSE) 分发；`examples/` 等视觉示例资产按 [ASSET-LICENSE.md](./ASSET-LICENSE.md) 单独管理。