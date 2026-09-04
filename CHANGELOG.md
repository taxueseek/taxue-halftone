# Changelog

All notable changes to this project are documented in this file.

## 1.4.1 - 2026-09-04

### Added

- 示例图集扩充六张实测样张（`examples/`）：突破极限（复古编辑）、SOLITUDE（复古编辑）、营业中·深夜便利店（复古编辑·双语变体，still open / 营业中）、最后一公里（复古编辑·双语变体，THE LAST KILOMETER / 最后一公里）、咫尺天涯（蓝染）、蓝色骑士·极速抵达（蓝染）；蓝染风格首次补齐样张，复古编辑扩到五张（含双语变体两张）。
- 示例作品页同步更新（README 中英）：说明改为「十一种风格中十种有样张」，两版新增 6 张图片卡片；`examples/README.md` 清单同步 19 张。

### Changed

- 全部示例图剥离生成元数据：8 张 JPEG 移除 EXIF 追踪字段（Artist UUID / Signature / UserComment），4 张 PNG 移除 TC260:AIGC 标识块（ContentProducer / ProduceID）；chunk 级无损清理，像素与原图完全一致（PIL 解码后 MD5 比对通过）。
- README（中英）版本徽章更新为 1.4.1，更新记录补齐 v1.2.0 / v1.3.0 / v1.4.0 / v1.4.1 条目。

## 1.4.0 - 2026-09-04

### Added

- 文案标点硬约束全面落地：全部 6 个内置元提示词模板（editorial 精炼版与中英双文案变体、dot_dissolve、paper_cut_group、paper_cut_halftone、aizome、tribute）的文案段落统一加入「直接展示文案，没有多余的标点符号」；SKILL.md §4 摘要与 language.md 规则 11 同步为全局纪律（标题与正文只允许逗号、句号及必需中日引号，禁装饰标点、编号、破折号、下划线）；顺带修正 paper_cut_group 模板变量表槽位名（{高山仰止}→{主题}）。
- editorial 内置精炼元提示词模板（经典半调）：复古印刷海报 + 双色调 AM 半调 + 字撞物 + 无摄影感 + 无日期年份，七个槽位（主题、颜色1、颜色2、图像描述、字体类型、文案、纸色）只需填主题与图像描述即可出图；与蓝染/点阵长模板互补，保持基准风格六轴不变。附中英双文案变体（editorial_bilingual）：文案一组变两组并列（英文短语 + 中文短语，语义对应非直译），如「still open」+「营业中」；变体内置两个参考填法（深夜便利店、马拉松——THE LAST KILOMETER / 最后一公里 沿用 still open / 营业中的双关结构，且「最后一公里」兼指马拉松末程与做事收尾）。
- 第十一套风格 tribute（经典致敬路）：任意名画/艺术流派/年代美学为视觉母题，仅抽象转译构图母题、视觉动机与情绪氛围，不复刻任何可辨认画面；巨大粗体英文标题 × 极小形象的纪念碑式尺度反差，中文短句为主 + 英文短句更小字号呼应（语义呼应非逐字直译）；双色叠印加深、未涂布纸、平版细 AM 半调、轻微褪色油墨与轻微错版；内置元提示词模板，风格来源与主题为必填。
- 第十套风格 aizome（蓝染艺术海报路）：绝对纯白数字平面（#FFFFFF，design-system 新增 ground_pure_white）+ 深靛蓝 #1E3A64 + 钴蓝 #2148B8 叠印出多次浸染的最深蓝；机制 photogram_stencil（蓝晒式 2-3 明度平阶剪影，不用半调网点），行为 dissipate（染液向外晕散），字图音量 balanced；染液浓淡、颗粒、短排线与毛边只存在于蓝色图形内部，禁止自动做旧与独立悬浮线条。
- 内置元提示词模板（`styles/aizome.json` 的 meta_prompt）：融合两份蓝染元提示词——结构化槽位版（主题/核心表达/主标题/副标题/情绪/点缀色 + 九方位隐式变奏硬规则）+ 第一性原理流程版（重定义问题 → 核心矛盾 → 主体动作×主题环境的专属视觉隐喻 → 逐项消融 → 3 秒/10 秒验收）；主题为唯一必填，标题留空自动创作，支持中英混合标题。
- 设计系统新增 `ground_pure_white`（数字纯白 #FFFFFF）：蓝染/蓝晒现代海报专用，绝对均匀、不做旧；roles.json 同步。
- 评测用例补到第 11 条（`evals/evals.json`），断言六轴取值、叠印深蓝非第三墨、纯白平面可指认。

### Changed

- SKILL.md（触发词加「蓝染/蓝染海报」、§10 风格清单标注 editorial 精炼模板）、入口桥（10 风格 + 1 变体、内置模板清单加 editorial）、README（中英，十种风格全表 + 色卡）、术语反查（「像经典半调/复古印刷海报」→ editorial；「像晒蓝图/像蓝染/靛蓝染布」→ aizome）同步。
- 色卡 `swatches/aizome.svg` 新增。
- 全套校验通过：design-system 结构、风格六轴完整性（10 风格 + 1 变体）、11 条 evals 断言一致（`scripts/run_tests.sh` 3/3）。

## 1.3.0 - 2026-09-03

### Added

- 参考创作模式（§1.6）：用户提供参考图时先判定角色——与 `examples/` 样张或 `swatches/` 色卡同指纹则锁定对应 `styles/<style_id>.json` 六轴为起点（仅经诊断映射、构图语序、字形调整，禁止复刻其场景/文案/排版）；不属于本系统指纹则走 §7 机制迁移（2–4 个可见机制 + 掏空判定）。验收：迁移项必须是五段第 2–3 段的可指认动作；判不了归属按机制样本处理。
- 消融补验（4 个回放：本系统成品参考 / 外部作品参考 × 有无该模式）：风格锁定路径在有/无模式下输出质量接近，模式的净增是「与指纹显式比对 + 否决」的决策过程；据此把模式从 16 行压缩到 5 行（保留判据与否决，去掉长篇双路径叙述），回归 3/3 通过。

## 1.2.0 - 2026-09-03

### Added

- 图源输入诊断（§1.5）：照片先写五行诊断卡（构图轴 / 主体占幅 / 负空间 / 主导色 / 唯一缺陷），再按「特征 → 轴映射」表取六轴值；每条来源写成注记（`behavior=horizon ← 诊断 axis=水平`），补 scenes.md 只按主题路由的盲区。
- 四域命题（§1.5）：主体域 / 背景域 / 互动域 / 排版动作 + 一个主问题 + 唯一修复动作；判语「原样保留 / 普通渐变 / 标题居中即不合格」；无源或 defect=none 时只写「无主问题」，禁止用反模式预防充当修复动作。
- 中文展示字形速查（§4.5）：6 谱系 × 5 可见特征（宽窄 / 重心 / 横竖对比 / 收笔 / 字腔），type-in 标题须选一谱系 + 至少 3 个特征，锁定字标保持共高共基。
- 参考迁移一行规则（§7）：仅用户提供参考图时启用，迁移 2–4 个从参考上直接可见的机制；掏空判定（禁项删去后只剩形容词则弃用）。
- 消融工具：`scripts/ablate.py`（按 [ABLATE] 标记生成版本变体）+ `scripts/checker.py`（配方字段 / 轴合法性 / 反模式扫描 / 诊断一致性检查）；`docs/IMPROVEMENT-ANALYSIS.md` 记录三方对比、改进设计与 21 次回放消融结果。

### Changed

- 配方模板 `behavior: vertical-extend` → `vertical_extend`，与 `design-system/behaviors.json` 一致（此前校验器会误判非法）。
- 消融删除：诊断卡独立小节（并入「诊断与映射」节）；原 §2.5 参考迁移独立节（14 行精简为 §7 一行检查点，掏空判定保留）。
- 回归：design-system / styles / evals 三套校验 3/3 通过，10 条既有 eval 无回退。

## 1.1.0 - 2026-09-03

### Added

- 第七套风格 imperfect_collage（不完美印刷拼贴）：撕纸拼贴三层结构，专色场 + 黑白半调主体，上图下卡，有意的不完美。
- 第八套风格 dot_dissolve（点阵解构海报路）：复古丝网圆点阵，具象主体解构为点阵、颗粒与流动波纹，粗体字融入点阵场，标点极简（正文与标题仅逗号句号）；内置元提示词模板与槽位填充规则，主题为唯一必填。
- 第九套风格 paper_cut_group（中式剪纸路）：剪纸剪影群像层层交错，细节全靠白色负空间镂空，一枚跳色例外成员，上图下卡；内置元提示词模板与槽位推演规则，主题为唯一必填。
- 第七种印刷机制 paper_cut_collage（剪纸拼贴）：刀口轮廓 + 负空间镂空，无网点无投影，与撕纸拼贴（torn_paper_collage）签名不混用。
- 点阵剪纸变体 paper_cut_halftone：点阵解构与中式剪纸的混搭，剪纸窗花轮廓 + 粗圆 AM 网点铺形，暗部 70–90%不断网，跳色克制（默认灰陶），用色倾向单色克制/主色配底色两色/主色底色跳色三色三选一，上图下卡；内置元提示词模板与槽位推演规则，主题为唯一必填。
- 评测用例补到第 7–10 条（`evals/evals.json`）与色卡 `swatches/imperfect_collage.svg`、`swatches/dot_dissolve.svg`、`swatches/paper_cut_group.svg`、`swatches/paper_cut_halftone.svg`。
- 全套校验通过：design-system 结构、风格六轴完整性（9 风格 + 1 变体）、10 条 evals 断言一致（`scripts/run_tests.sh` 3/3）。
- 点阵解构三张实测样张（雾中灯塔、深海之灯、风花雪月）与中式剪纸一张实测样张（海阔天空），入 `examples/` 并同步 README（中英）示例区与示例图集清单。
- README（中英）新增「随机性与创造力」一节：Design Skill 刻意不做僵化约束、不追求复刻固定效果，同一提示词在 GPT Image 2、Grok Imagine 2、Nano Banana 2、Seedream 5.0 Pro 上风格会有较大不同；模型建议——主力 GPT Image 2、Grok Imagine 2，后备 Nano Banana 2、Seedream 5.0 Pro。

### Changed

- 辅墨量化口径补充：职务极小的辅墨可下探（paper_cut_group 跳色成员 5–10%；paper_cut_halftone 前两档用色倾向不启用跳色记 0%，第三档三色倾向启用跳色 ≤10%）（DESIGN.md §四）。
- 风格更名（style_id 不变）：中式剪纸群像路→中式剪纸路，网点剪纸群像路→点阵剪纸路——后者定性为点阵解构与中式剪纸的混搭**变体**（非独立第十风格），旧名未体现；README（中英）、SKILL.md、evals、术语反查、DESIGN.md、色卡、入口桥同步。
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
