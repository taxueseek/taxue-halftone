<div align="center">

**中文** · [English](./README.en.md)

# taxue-halftone · 半调海报

**把一句话、一个主题或一张照片，做成一张有印刷质感的封面。**

[![Version](https://img.shields.io/badge/VERSION-1.0.0-2ea44f?style=flat-square&labelColor=333)](./CHANGELOG.md)
[![Skills](https://img.shields.io/badge/SKILLS-1-2ea44f?style=flat-square&labelColor=333)](./SKILL.md)
[![Stars](https://img.shields.io/github/stars/taxueseek/taxue-halftone?style=flat-square&label=STARS&color=e37f2c&labelColor=333)](https://github.com/taxueseek/taxue-halftone/stargazers)
[![Validate](https://github.com/taxueseek/taxue-halftone/actions/workflows/validate.yml/badge.svg)](https://github.com/taxueseek/taxue-halftone/actions/workflows/validate.yml)
[![SKILL.md](https://img.shields.io/badge/Agent-SKILL.md-214f9b?style=flat-square&labelColor=333)](./SKILL.md)

</div>

它做的是「印刷感」的图：半调网点、Riso 孔版、木刻、蓝晒、复印机那种质感。默认双色（一主一辅），也可以只用单色，具体怎么配色、字放哪，它都会配好，最后给出一份完整可复用的提示词。

## 示例作品

> 图片放在 `examples/` 目录，由技能实际出图产出（版权见 [ASSET-LICENSE.md](./ASSET-LICENSE.md)）。七个风格各一张，不完美印刷拼贴有三张。

| 深夜便利店（复古编辑） | 标本档案（标本档案） | 无声的秩序（瑞士海报） |
|:---:|:---:|:---:|
| <img src="./examples/example-midnight-store.jpg" alt="蓝橙双色深夜便利店半调海报" width="280"> | <img src="./examples/example-herbarium.png" alt="绿色标本档案印刷海报" width="280"> | <img src="./examples/example-concert-hall.jpg" alt="红色摄影展海报无声的秩序" width="280"> |

| 午夜电台（胶片叠层） | 回声（波兰海报） | 海风集（孔版小册） |
|:---:|:---:|:---:|
| <img src="./examples/example-midnight-radio.png" alt="蓝色胶片叠层午夜电台海报" width="280"> | <img src="./examples/example-echo.png" alt="黑色高反差回声海报" width="280"> | <img src="./examples/example-seashell.png" alt="绿色紫色海风集封面" width="280"> |

| 雨天雨伞（不完美印刷拼贴） | 城市夜归（不完美印刷拼贴） | 夜骑（不完美印刷拼贴） |
|:---:|:---:|:---:|
| <img src="./examples/example-rain-umbrella.png" alt="蓝黑撕纸拼贴雨天雨伞海报" width="280"> | <img src="./examples/example-night-walk.png" alt="蓝色撕纸拼贴城市夜归海报" width="280"> | <img src="./examples/example-night-ride.png" alt="蓝色撕纸拼贴夜骑海报" width="280"> |

## 七种风格

| 风格 | 色卡 | 特点 |
|---|---|---|
| **复古编辑**（editorial） | ![editorial](./swatches/editorial.svg) | 蓝 + 陶土橙，半调网点，一个主体占大头、文字压上去，旧杂志编辑排版的复古感，最常用 |
| **波兰海报**（polish） | ![polish](./swatches/polish.svg) | 单色高反差，字本身就是画面，干净利落 |
| **瑞士海报**（swiss） | ![swiss](./swatches/swiss.svg) | 红 + 黑，照片阶调清楚、实色大字、留白多，克制规矩 |
| **孔版小册**（riso_zine） | ![riso_zine](./swatches/riso_zine.svg) | 绿 + 紫，主体小、纸留大片白，像手工印的小册子 |
| **胶片叠层**（filmstack） | ![filmstack](./swatches/filmstack.svg) | 蓝 + 橙，粗网点本身就是图形，几层叠片、宽边框住 |
| **标本档案**（archival） | ![archival](./swatches/archival.svg) | 绿 + 黑，标题 + 一张规整图版 + 多栏注文，像标本观察笔记 |
| **不完美印刷拼贴**（imperfect_collage） | ![imperfect_collage](./swatches/imperfect_collage.svg) | 暖白纸 + 大面积专色场 + 黑白半调主体，撕纸边揭示，上图下卡，有意的不完美 |

想用哪个风格，直接点名；不说风格它会按主题和用途选。

## 怎么用

安装：

```bash
npx skills add taxueseek/taxue-halftone
```

装好后直接说，例如：

- 「用半调做一张凌晨便利店的竖版海报，标题写 still open」
- 「把这张照片做成孔版 Riso 封面，标题是『深夜电台』」
- 「做一个单色高反差剪影海报，主题是孤独，不要文字」

也可以输入 `/taxue-halftone` 触发。每次会给你三样东西：一张图（有生图工具时）、一份完整提示词、一份配色和版式的说明。不满意就指出来，它一次只改一处。

## 适合做什么

- 海报：活动、展览、城市漫游、概念海报
- 平台封面：小红书、公众号、播客、B站、头像、超宽头图
- 品牌物料：明信片、邀请函、门票、菜单、包装贴纸
- 书刊：封面、扉页、章节页、zine 内页
- 纪念物：旅行手账、相册封面、周年卡
- 文字：文学摘句、诗歌、个人宣言

## 基本规矩

- **最多双色**：一个主色管主体和标题，一个辅色只做一件事（日期、注释、勾一个物件），不洒满页当装饰
- **纸是画面的一部分**：底色不算颜色，浅色纸配深色、深纸配浅字都算好
- **字和图分主次**：字大声图就退，图大声字就退，不两个都抢
- **印刷感靠网点不靠做旧**：用半调、Riso 不等于要泛黄、怀旧

## 工程校验

规范不只写在文档里：六种风格的取值、配色、机制都有机器可读的清单，配有评测用例。改任何一处，跑一遍检查就能发现有没有改坏，push 或提 PR 时 GitHub Actions 会自动跑。

```bash
scripts/run_tests.sh                    # 一次跑完所有检查
scripts/validate_styles.py <style_id>   # 单独查某个风格
scripts/render_style_card.py <style_id> # 重新生成色卡图
```

## 更新记录

- **v1.0.0**（2026-09-01）：首次发布。六种风格、六种印刷质感、机器校验和评测用例。详见 [CHANGELOG.md](./CHANGELOG.md)。

## License

代码和技能内容走 [MIT License](./LICENSE)；`examples/` 里的示例图走 [ASSET-LICENSE.md](./ASSET-LICENSE.md)，不随 MIT 分发。