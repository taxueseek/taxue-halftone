---
name: taxue-halftone
description: "半调海报：用限墨+网点把任意主题做成有结构、有质感、可复用的艺术封面。支持多种印刷语言（半调/孔版/双色/木刻/蓝晒/复印机、1-bit 剪影、撕纸拼贴），按风格给出一致又有特色的封面。六项不变式出图前先定：纸色、墨色角色、叠印方式、印刷机制、主体走向、字图音量。触发词：半调海报、艺术封面、网点、孔版、双色、Riso、duotone、木刻、蓝晒、复印机美学、不完美印刷拼贴、撕纸拼贴、编辑型印刷拼贴、有意不完美、点阵解构、丝网海报、剪纸、窗花、中式剪纸、网点剪纸、平台封面（B站/小红书/抖音/公众号/头像/超宽）、主题结构印刷封面、限墨封面。不用于：全彩实拍、UI、图表、模板拼贴。"
---
# 半调海报 · 艺术封面

第一性原理：**限墨不是滤镜，是可校验的印版系统。** 无论选哪种机制，一张图都必须先回答六个互斥且穷尽的问题（见 §0），缺一则不是本系统。风格 = 六轴各取一组确定值形成的指纹组合，不是把某个滤镜套上去。

> 判语：如果无法指出每块颜色来自哪支墨、哪个角或哪一层阶、纸在哪里露出，就还不是本系统。

## §0 六不变式（规范的最小不变式，MECE）

任何一张图，无论什么机制、什么风格，都必须在这六个轴上各自给出**一个确定值**。缺任一轴，图不是本系统；轴内取值模糊，图不鲜明。

| # | 轴 | 必须回答 | 数据源 | 量化约束 |
|---|---|---|---|---|
| 1 | **纸（Ground）** | 纸是哪一块、什么色 | `roles.json` | 底衬色不算墨；暗底白衬必须 choke |
| 2 | **墨（Ink/Mist）** | 哪几支墨、各干什么 | `roles.json` | 主 70–85%，辅/雾且各 1 职务；imperfect_collage 专属第三通道（跳色 ≤5%，不进主体结构），其余风格 ≤2 墨 |
| 3 | **印刷布尔** | 两色相交怎么处理 | `bools.json` | knockout/overprint/trap 三选一 |
| 4 | **机制** | 用什么印刷机制 | `mechanisms.json` | 一次一个；机制内角/点/密度须有结构 |
| 5 | **主体行为** | 图的「势」往哪走 | `behaviors.json` | still/dissipate/densify/horizon/vertical-extend |
| 6 | **字图音量** | 字和图的音量谁大 | `volume.json` | 字大声则图退；禁止双开 11 |

七轴外：**主体结构链** 与 **平台画幅** 是两个独立的约束系统（`subject.json`、`platform.json`），它们不改变六轴取值，但决定「主体是否可识别」「画幅是否被裁坏」。

## §1 重新定义问题（接案 → 六轴配方）

先问清楚，能填齐才有资格出图。产出一份内部配方（用户未问过程则不整段展示）：

```yaml
# 一、主体与目的
subject: <一个可识别主体，见 subject.json>
subject_chain: <解剖/生长/功能/材料的连续结构链，见 subject.json>
intent: <公告|观察|宣言|包装|标本|封面|转绘>
exact_text: <用户原文 | 按语言发明 | none>
text_language: <用户语言，除非另指定>
representation: <faithful | abstract>
source_policy: <preserve 保像素 | distill 提炼 | invent 无源图>

# 二、六轴取值（缺一不可，见对应 json）
ground: <Ground_id>                # roles.json
ink_role: <角色赋墨：role + hex + 占比>  # roles.json
boolean: <knockout | overprint | trap>  # bools.json
mechanism: <mechanism_id>          # mechanisms.json
behavior: <still|dissipate|densify|horizon|vertical-extend>  # behaviors.json
volume: <type_lead | image_lead | balanced>  # volume.json

# 三、画幅与产出
ratio: <platform_id 或显式比例>     # platform.json
viewing_distance: <handheld | wall | far>
layout: <layout_id>                # compositions（见 references/compile.md）
tension: <relaxed | balanced | assertive>
focal_event: <恰好一个>
release_zone: <一个更安静的区域>
avoid_named_patterns: <逐个列出 references/patterns.md 里命中本单的命名模式名；无命中填 none>   # 出图前反模式雷达，见 §5
```

未指定时的默认：机制 AM、双色、中性白纸、relaxed（旅行/生活）或 balanced（活动/信息）、空纸 25–55%、复古编辑（不做旧）、主墨 45°、双色差 ≥30°。Mist 不是第三色相，是主墨浅阶或叠印密度。

## §2 印版推导（勿锁死单一配方）

起点色（可改，须写 HEX）：
- 单墨：Cobalt `#2148B8` / Botanical `#008A4B` / Terracotta `#C65F38` / Signal Red `#C83232` / Aubergine `#63365F` / Charcoal `#30343A`
- 双色常用：Cobalt+Terracotta；Charcoal+Signal Red；Mint+Charcoal；Ultramarine+Safety Orange；Cyan+Brick Red

规则：辅墨必须有职务（日期、注释、一个物件、一处叠印交叉）。禁止把第二色当装饰洒满页。纸 = Ground 不算第三色；叠印变深 / Mist 不算第三色。

## §3 构图语序（不改变六轴，只在六轴内组织画面）

1. **一物主导**（或字作为物）：占 45–80%（信息海报可降 32–55%；still 陈列更小），至少一边裁切。
2. **字与图音量**：按 volume.json 定谁主谁辅；字撞物（穿越/覆盖/劈开）是其中一招。裁切要为字留口袋。
3. **纸切入图像**：高光 knockout 到纸；扩散边走网，结构边保持硬边（窗、字、几何不「融化」）。
4. **一个手工手势**：圈注、套准线、手绘短线、旋转小标签、或 Weingart 式不规则宽边——只选一族。工艺缺陷预算也算这一次：轻微套不准或一次并网，不要叠 grain+刮痕+咖啡渍。

行为逻辑（先于物体类别）：still 静置 / dissipate 向外变少（用点）/ densify 向内变重（用网纹）/ horizon 地平线 / vertical-extend 沿长边消失。点和网纹不要写在同一处渐变里。

## §4 多语言与多尺寸

见 `references/language.md`、`platform.json`。摘要：
- 用户文案原样；发明文案用用户语言。
- CJK 微字 → type-off；短 H1 可 type-in，笔画须 ≥ 2–3 个网距，校对失败则后期上字。
- type-in 时把字写成一次印刷事件（墨量 / 层 under|same|over / 一处「破」），不是字体名。
- 换画幅必须重写构图；先改观看距离/档位，再改字号，最后改构图。

## §5 提示词与出图

按 `references/compile.md` 五段编译。本环境 GenerateImage：`description` = 五段正文，`aspect_ratio` ∈ 1:1/4:3/3:4/16:9/9:16（5:2 降 20:9；21:9 降 16:9）。

出图前跑 `scripts/validate_styles.py <style>`，再过一遍**反模式雷达**（`references/patterns.md`，逐名扫描五段 description）。命中任一命名模式：先报「此处命中 `xxx`，信号是 `yyy`」，**只改所属那一段**，再出图。

出图后按三档评审卡自检（失败只重生一次，只改一项）：

- **blocker（命中任一项即不算通过）**：超过两墨 / 无选定机制痕迹 / 空纸越界 / 主体不可辨（遮标题 <3 秒认出）/ 自动做旧 / 假 CMYK 扮孔版 / 字图同网碎字 / 全通道同角 / 结构边被网融化 / 渐变冒充网点 / 命中任一命名反模式
- **可修（优先级低，留给下一版，不阻塞）**：无 5× 字号差 / 无焦点事件 / 商标/二维码加网 / 复刻参考图字句
- **通过判语**：能否说出「哪支墨、哪个角或哪一层、纸在哪」→ 说不出口即未过关
- 精确文字仍错 → type-off 底板 + 声明后期排字，不假装正确

## §6 元提示词

用户要可复用模板时：输出带槽位正文 + ≥3 主题填法 + 替换规则。主题为唯一必填。

## §7 硬避免

完整命名的反模式表见 `references/patterns.md`（18 个命名模式，含视觉签名与正确替代），出图前必须跑反模式雷达。此处是简版索引，按层归类：

- **色调**：第三色相 / 渐变冒充网点 / 霓虹泼彩 / 全彩照片 / 自动做旧 / 假 CMYK 扮孔版
- **机制**：全通道同角 / RGB 上套 Color Halftone / 把 Riso（印刷机）和 Halftone（加网）当可互换滤镜名 / 印刷机制当情绪词写进 prompt
- **排版**：居中模板 / 字图同网碎字 / Logo/URL/二维码加网
- **主体**：复刻参考图独特字句排版 / 无来源完整广告英雄人像
- **拼贴**：贴纸拼贴 / 复古电影海报拼盘
- **表达**：销售 CTA / 矢量平涂网红海报

出图 description 若命中任一命名模式（见 `references/patterns.md`），先把那一段改到它的「正确替代」，再出图。

## §8 加载协议

先读本文件完全掌握六不变式，再按需读：

| 场景 | 必读 |
|---|---|
| 定机制与六轴 / 选风格 | `styles/*.json` + `design-system/` |
| 不完美印刷拼贴 / 撕纸拼贴 | `references/imperfect-collage.md` + `styles/imperfect_collage.json` |
| 主体结构链 / 3 秒识别 | `design-system/subject.json` |
| 平台画幅 / 安全区 | `design-system/platform.json` |
| 中英日韩 / 双语 | `references/language.md` |
| 写 prompt / 元提示词 | `references/compile.md` |
| 反模式雷达（命名反模式） | `references/patterns.md` |
| 术语对齐（用户词→机制） | `references/vocabulary.md` |
| 校验与测试 | `scripts/` + `evals/` |

## §10 风格清单（`styles/`）

| style_id | 名称 | 一句话 |
|---|---|---|
| editorial | 复古编辑印刷风 | AM 半调 + 字撞物 + 纸露白，一物主导（基准） |
| polish | 波兰海报路 | photogram 高反差，字即物，单墨或高反差 |
| swiss | 瑞士海报路 | 摄影阶调 + 实色字 + 大量纸白，克制秩序 |
| riso_zine | 孔版 zine 路 | 极疏构图，主体小、空纸大，当代纸不做旧 |
| filmstack | 胶片叠层路 | 粗网本身是图形，字与图共享一层，宽边框住 |
| archival | 标本档案路 | 标题 + 规整图像板 + 多栏图注，标本/观察笔记 |
| imperfect_collage | 不完美印刷拼贴 | 撕纸拼贴三层结构，专色场 + 黑白半调主体，上图下卡 |
| dot_dissolve | 点阵解构海报路 | 复古丝网圆点阵，具象解构为点阵颗粒波纹，字融入点阵场，内置元提示词模板（主题唯一必填） |
| paper_cut_group | 中式剪纸路 | 剪纸剪影群像+负空间镂空，上图下卡，一枚跳色例外成员，内置元提示词模板（主题唯一必填） |
| paper_cut_halftone | 点阵剪纸路 | 剪纸窗花轮廓+粗圆网点铺形，暗部 70–90%不断网，跳色克制，上图下卡，内置元提示词模板（主题唯一必填，用色倾向三选一） |

## §9 工程校验

本系统把「规范」落到可机器校验的数据层：六轴分别在 `design-system/` 各有 json，风格在 `styles/` 是六轴的取值组合。改任一轴须保证全系统一致。

```bash
scripts/run_tests.sh          # 全套：design-system 结构 + styles 完整性 + evals 断言
scripts/validate_styles.py <style_id>  # 校验单个风格六轴是否取值齐全且引用存在
scripts/render_style_card.py <style_id>  # 生成 swatches/ 可视化卡片
```
