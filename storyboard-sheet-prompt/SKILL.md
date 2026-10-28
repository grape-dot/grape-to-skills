---
name: storyboard-sheet-prompt
version: 1.3.0
display_name: 手绘分镜脚本提示词
display_name_en: Storyboard Sheet Prompt
description: "Turn a scene into a locked-consistent 16:9 hand-drawn storyboard sheet prompt (3x3 red-ink panels, right-side character design panel with graphite sketch + Pixar-style 3D portrait, three handwritten note boxes). Every character and every scene must be designed in Pixar's stylized-realistic language — silhouette-first, one shape language, eyes about a third of the face height, tactile non-glossy materials, single warm key with one-sided rim, lifted blacks — never generic 'in the style of Pixar' 3D. Builds a Scene Bible internally so props, colors and characters never drift between panels, then returns TWO paste-ready prompts — English first, then the full Chinese version from the same constants. No JSON, no ledger, no per-cell files unless asked. 把一段情景转成手绘动画分镜脚本页的出图提示词，角色与场景强制按皮克斯风格化写实语言设计；触发词：分镜、分镜脚本、九宫格分镜、storyboard、角色设计页、皮克斯风格、镜头提示词、情景转提示词。"
description_zh: |-
  把一段故事情景转成一张 16:9「手绘动画分镜脚本页」的出图提示词：左侧 3×3 九格分镜（细红框、蓝箭头注释、手写镜号与动作说明）、右侧「角色设计与选角」面板（铅笔素描 + 皮克斯风 3D 肖像 + 图注）、底部三个手写笔记框（流程意图 / 镜头笔记 / 五色调色板）。
  核心不是逐格翻译画面，而是**先在内部建一份场景资产锁定表（Scene Bible）**——空间方位、道具清单与状态链、角色造型常量、五色板、光位、视轴——再让九格共用同一份字符串，从底层掐掉"这格黑那格红、这格杯子那格盒子"的漂移。
  **默认在回复里直接交付中英两段可直接粘贴的提示词**（同一份 Bible 写出来，不是互译），不产 JSON、不产台账、不产单格稿；Bible 是过程材料，活在提示词里，不单独成文。
  触发词：分镜、分镜脚本、storyboard、九宫格分镜、3×3 分镜、镜头提示词、角色设计页、动画电影前期、情景转提示词、把这幕画成分镜。
description_en: |-
  Turn a scene description into a production-grade image prompt for a hand-drawn 16:9 storyboard sheet: 3x3 red-ink panels with handwritten shot numbers and blue arrow notes, a right-side character design & casting panel (graphite sketch + Pixar-style 3D portrait + captions), and three handwritten note boxes at the bottom.
  Enforces a Scene Bible (space, prop registry with state chains, character locks, palette, light direction, screen axis) internally before any panel wording, so all nine panels cite one set of constants and props never drift.
  Default output is TWO paste-ready prompts — English, then the full Chinese version built from the same constants. No JSON, no continuity ledger, no per-cell files, no delivery doc — those only on explicit request.
  Triggers: storyboard, storyboard sheet, 3x3 storyboard, animatic board, character design page, scene to prompt.
metadata:
  author: yanfang
  philosophy: "lock the bible first, then write nine panels that all cite it — but ship one prompt, not a filing cabinet"
---

# 手绘分镜脚本提示词

## 交付规则（先看这段，违反即返工）

**默认交付 = 两段可直接粘贴的提示词（英文 + 中文），写在回复里，不建任何文件。**

回复就这几段，顺序别换：

1. 代码块 A：**英文**完整提示词，一段到底，不留占位符、不写"此处按需替换"。
2. 代码块 B：**中文**提示词，同一份设定写出来的完整版，不是节选、不是摘要。
3. 3–6 行：我替你补了什么（逐条）、哪几处你可能想改。
4. 一句话：要文件 / 要看九格怎么办，说一声就行。

中英两段**不是互译**：它们都从同一份 Bible 常量写出来，hex、造型锁、道具英文名、镜别、对白必须一一对应。中文段是"同一套设定的中文表述"，不是英文的逐句直译——直译会把 `#2F6FB0` 写成"一种蓝色"，模型就自由发挥了。对白在中文段里仍保留英文原句（台词是给配音用的），说明性文字用中文。

| 用户说了什么 | 你交付什么 |
| --- | --- |
| 只给一段情景（默认） | **英文 + 中文**两段提示词 + 3–6 行补全说明 |
| 「只要英文」/「省 token」 | 只给英文段 |
| 「存成文件」/「给我 md」 | **只写一个** `prompt.md`，里面仍是中英两段 |
| 「要复用」/「改第 3 格」/「九格分多轮做」 | `storyboard.json` + `assemble.py`（用户要文件时才落盘） |
| 点名要台账 / 单格稿 / 配音卡 | 只出点名那一份 |

**不许顺手产出**（这是最常见的返工）：Scene Bible 表格、道具状态台账、九格 JSON、`cell-01..09.md`、交付说明 / README / 索引、中英分家的一堆 md。

Bible 是**过程**，不是交付物。它必须存在于提示词的 SETTING / CHARACTERS / PROPS / PALETTE 段落里，但不单独成文、不进回复、不落盘。

## 它做什么 / 不做什么

做：把用户口述的一段情景，变成**一段可直接粘进出图模型的提示词**。

不做：不直接生成图片。用户要图时再调出图工具，把同一份常量喂进去（见「出图策略」）。

## 四条硬前提

违反任意一条，返工重来，不要"先出个大概再修"。

1. **先 Bible，后格子。** 心里没有资产锁定就没有第一格。九格是同一世界的九个窗口，不是九张独立插画。
2. **一格只出现 Bible 里登记过的东西。** 未登记的物件、颜色、角色特征一律不许即兴添加。要加，先回 Bible 加一条，再回来改受影响的格。
3. **描述字符串逐字复用。** 同一件道具、同一个角色在九格里必须用同一串词。禁止同义改写——`seed bowl` 到第 7 格变成 `nut bowl`，模型会当成两个东西。
4. **角色与场景必须是皮克斯风格。** 不是"写实 3D"，也不是"加一句 in the style of Pixar"。造型、材质、光、色、空间、表演六轴都要过 `references/pixar-style.md` 的规格。这一条与用户偏好无关——**每单都要**，用户没提也照做。

## 风格硬约束：皮克斯（第 4 条前提的展开）

皮克斯自己的立场是"写实从来不是目标"——造型往外推、材质往里收、光被人为编排，三样同时对才像。只加风格词，模型会退化成"圆脸大眼 + 塑料高光"，那是最像 AI 的假皮克斯。

| 轴 | 硬指标（写进提示词时要数字化） |
| --- | --- |
| 造型 | 剪影填黑缩小仍可辨；每角色**一种**主动力形状（圆/方/三角）；幼态头身比 1:2–1:3；眼高约占脸高 1/3 且位置偏低；五官做减法；留一处刻意的不完美 |
| 材质 | 次表面散射只给毛边/耳/鼻/颊，短散射距离偏暖；粗糙度毛 0.35–0.55、布 0.6–0.8；手绘感纹理；次要物件降细节；**禁止塑料/蜡感高光** |
| 光 | 单一主光方向，面积光为主；轮廓光**只打一侧**；阴影可带天光色；允许违反物理补光；禁止处处黄金时刻 |
| 色 | 一段落一组色彩关系；高饱和靠明度分层与冷暖对比，不靠堆色相；暗部不死黑、高光不切白；一格只有一个最亮焦点 |
| 空间 | 大气透视把远景化开；尺度可夸张但重力/接触阴影必须对；35mm 上下、低机位、浅景深；构图不许正中对称 |
| 表演 | 表情夸张 15–20% 到破形为止；眼睛必须有服从主光的 catchlight；一个镜头只演一个情绪 |

**分层落法（别把整页做成 3D）**：纸面仍是白纸 + 细抖红框 + 石墨速写 + 蓝墨箭头；九格里的**世界**读作皮克斯电影分镜；右栏 3D 肖像是全页唯一的"完成品"。提示词里写一句就够：

```
Each panel is a graphite production sketch OF a Pixar-style 3D film frame — the
drawing medium is pencil, the world inside the frame is Pixar.
```

**与限色预算不冲突**：皮克斯的"色彩丰富"来自明度分层和冷暖对比，不是色相数量。六色够用，不够时先加明度台阶，别加色相。

完整规格、三段可粘贴片段（场景 / 角色 / 负面）、30 秒自检与出处见 `references/pixar-style.md`。

## 四步

### Step 0 判类型（决定 Bible 粒度）

| 类型 | 特征 | Bible 重点 |
| --- | --- | --- |
| 单场景闹剧（最常见） | 一个空间内 9 个动作节拍 | 道具**状态链**（同一个东西从 A 走到 B） |
| 有地理跨度 | 换了房间 / 换了地点 | 每个地点一组空间常量，并声明转场格 |
| 有时间跨度 | 白天到夜晚、季节变化 | 光位常量单独成行，允许按格切换但不能漂 |
| 群像 / 多人 | 3 个以上角色 | 站位上墙，规定左右顺序不许乱 |

角色、场景、任务目标三项缺任一项，**只问一句**（别盘问）；其余自行补全，交付时说明。

有地理跨度但用户没要求多个场景时，**优先把地点收敛成一个**（例：把"公司内部 + 天空"收成"云平台 + 远处彩虹"），九格同轴更容易读。

### Step 1 在心里建 Bible（不落盘）

按这六行写完，写完才开始写第一格。这个格式够用，不用建表：

```
SPACE   一句话：什么空间、什么视角、多大
AXIS    屏幕左＝ … ／ 屏幕右＝ …；全页不镜像
SCALE   主角 ??cm : 场景 ??cm 的具体比
LIGHT   主光方向 + 色温 + 补光，九格不变
CHARS   每角色一行：lock（形状/颜色/尺寸/no clothing）· anchors 三件 · ratio 数字化
PROPS   每物件一行：唯一英文名（states 枚举）
PALETTE 5 色 hex + 1 例外，每个写排他用途
```

皮克斯常量**不进 Bible**，它由 `references/pixar-style.md` 统一提供，每单原样粘贴三段（场景段 / 角色段 / 负面段）。Bible 管"这个世界有什么"，皮克斯段管"这个世界怎么被渲出来"，两者不混写。

- 颜色给 hex，尺寸给厘米，道具给唯一英文名——这三样不数字化，模型就自由发挥。
- 造型锁里**不要写性格形容词**，只写形状 / 颜色 / 尺寸；性格进对白和动作。
- `no clothing, no accessories` 必须显式写，不写会冒出小领结或墨镜。
- 角色毛色不许拿去画道具，道具色不许沾到角色身上，否则角色会融进背景。
- 五色不够用时，先想**能不能用交叉排线（蓝+黄读作绿）或"限量印刷"逻辑**解决，再考虑加第六色；加例外色必须显式声明"仅此一处"。

字段细则、状态链合法性、比例锚，只在拿不准时读 `references/scene-bible.md`。

### Step 2 排九拍

正好 9 格。每拍要有：镜别、主体动作、情绪落点、蓝箭头注释（可选，2–5 词）、英文对白（0–2 句）、道具状态。

默认节奏（可直接用）：

| 01 NEAR | 02 MEDIUM | 03 NEAR | 04 NEAR | 05 MED-WIDE | 06 MEDIUM | 07 NEAR | 08 BEAUTY | 09 WIDE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

硬规则：同镜别不得连续 3 格；第 5 或 6 格必须有一次尺度跳跃；第 8 格是 beauty shot（柔光/浅景深/正中），和第 7 格的混乱形成断崖；第 9 格必须 WIDE 收拢空间。

### Step 3 拼提示词

**默认手写**：照 `references/prompt-templates.md` 的模板 A 一次写完英文段，九格每格一行、连着写，不要拆成"第 1 格一段"分开写；写完再对着**同一份 Bible** 写中文段。中文段里 hex、道具英文名、镜别、对白原样照抄，只把说明性文字换成中文。

只有这三种情况才建 `storyboard.json` 跑脚本：要复用同一套设定、要逐格返工、九格要跨多轮做。

```bash
python scripts/assemble.py board.json                 # → prompt.md（英文 + 中文两段）
python scripts/assemble.py board.json --stdout        # 直接打印，不落盘（首选）
python scripts/assemble.py board.json --en-only       # 只要英文段
python scripts/assemble.py board.json --full          # 拆分包（中英分文件+台账+单格稿），仅点名要时
```

脚本的价值是**校验**，不是产出：道具未登记、格数不对、对白混中文、状态越界，都会当场报错。写完仍然要人读一遍。

一次性任务不要为脚本留 JSON：把 board.json 放在临时目录（如 `.workbuddy/tmp/`），`--stdout` 取走结果后删掉，结论留在回复里。

### Step 4 自检（只看五项）

色板越界 / 道具未登记 / 视轴翻转 / 镜别单一 / **风格锚丢了**（剪影认不出、两侧都有轮廓光、塑料高光、暗部死黑）。其余细项见 `references/delivery-checklist.md` 与 `references/pixar-style.md` 的 30 秒版。

## 一致性红线 13 条

| # | 规则 | 一句话后果 |
| --- | --- | --- |
| 1 | 单一来源：颜色/道具/外形只从 Bible 取字符串 | 现场造句必走形 |
| 2 | 道具注册制：一个物件一个英文名 | 同义词 = 两个东西 |
| 3 | 状态链闭合，只走枚举内合法转移 | 跳帧感 |
| 4 | 色彩预算：色板 + 石墨灰 + 红框 + 蓝箭头 | 第五种彩色就是失败 |
| 5 | 角色三锚每格在，用同一串词 | 观众认不出是同一只 |
| 6 | 光位写死，反打要显式声明 | 改光 = 换时空 |
| 7 | 视轴写死，九格不许镜像 | 第 5 格一翻整页就散 |
| 8 | 比例锚数字化（台面 90cm / 主角 15cm） | "巨大"会被画成普通 |
| 9 | 二次出现写 `same … as panel 01`，不重描述 | 重描述必漂 |
| 10 | 格数锁死 9，不凑第 10 格、不留空 | 版式崩塌 |
| 11 | 同镜别不连续 3 格 | 节奏死 |
| 12 | 文字最小化：镜号 + 2–4 词标签 + 图注 | 长句必成乱码 |
| 13 | 风格锚写死：皮克斯六轴常量每单原样粘贴，不靠"in the style of Pixar"五个词 | 出来的是塑料假 3D |

## 版式要点

16:9 单页、白纸微纹理、**一张纸的俯视扫描**（不是立体场景）。页眉 6–8%；左区 63–66% 放 3×3 红框网格，每格 16:9；右区 30–33% 竖排「CHARACTER DESIGN & CASTING」；页脚 16–20% 三个手写框（宽比 1 : 1.15 : 0.85）。

- 红框要**细**（1.5–2px、略抖、四角略出头），一加粗就变成 PPT 描边。
- 标注写在框**外**，压在画面里必糊。
- 页面文字用英文（模型对英文手写更稳），只有左上角大镜号用中文。
- 三种笔：石墨铅笔（画面）、红墨（框）、蓝墨（箭头）；右栏两张 3D 肖像是唯一"精细"的东西，别把 3D 也画成手绘。
- 崩坏点全集见 `references/sheet-layout.md`。

## 语音反差（要点）

反差来自四条可量化轴的差值，不是形容词：

| 轴 | 快角色 | 慢角色 |
| --- | --- | --- |
| 音高中心 | 高、窄、上扬 | 中低、平、几乎单音 |
| 语速 | 4.5–5.5 音节/秒 | 2.5–3 音节/秒 |
| 句长 | 短命令句 + 代号自称 | 3–6 词，拖尾收 |
| 气口 | 句前抢吸一口气 | 长呼气、咀嚼声、叹气 |

再叠两条混音差：一个贴麦（干声、+2dB），一个离麦（带房间感、永不提音量）。提示词里只写**声学参数**，不写 `funny voice`。

对白规范：全英文、每格 ≤2 句、每句 ≤8 词、整页 ≤6 句；写不出反差就做"互换测试"——换给另一个角色说还成立，就是没反差，重写。完整四轴与可粘贴声学块见 `references/voice-casting.md`。

## 出图策略

- **A 单张整页（默认）**：提案、氛围展示。提示词里必须写 `a single flat sheet, not a grid of separate images`，并压低每格细节（只画剪影关系与关键道具）。低于 4K 会糊。
- **B 分区生成再拼**：九宫格 / 右栏 / 页脚条各出一张，后期拼版。要清晰可读时用这个。
- **C 主图 + 单格放大**：整页当提案图，另出 2–3 张关键格高清。给客户看最实用。

用户没说就按 A，交付时用一句话提 B/C 的存在，别主动多做。

## 文件地图

| 文件 | 用途 | 什么时候读 |
| --- | --- | --- |
| `references/scene-bible.md` | 资产锁定表字段、状态链、反漂移规则 | 拿不准某个字段怎么写 |
| `references/pixar-style.md` | 皮克斯六轴规格、三段可粘贴片段、30 秒自检、出处 | **每一单都读**，写提示词前 |
| `references/sheet-layout.md` | 版式规格、九格节奏、崩坏点 | 版式细节 / 出图崩了 |
| `references/prompt-templates.md` | 四段可粘贴模板（整页/单格/角色卡/道具卡） | 每次写提示词都要 |
| `references/voice-casting.md` | 四轴、英文对白规范、声学块 | 有对白时 |
| `references/delivery-checklist.md` | 交付前自检清单 | 自检 |
| `scripts/assemble.py` | JSON → 提示词 + 校验 | 要复用 / 要逐格改 |
| `references/board-schema.md` | board JSON 字段表与校验规则 | 要写 JSON 时查字段 |
| `examples/nut-crisis.json` | 完整范例输入 | 要写 JSON 时照抄 |
| `examples/out/prompt.md` | 成品质感参照（中英两段） | 想知道"好"长什么样 |

## 反例（都是过度交付）

1. 用户只说"帮我把这段做成九宫格分镜"，回复里跟了 6 个文件：`storyboard.json`、`sheet-prompt.en.md`、`sheet-prompt.zh.md`、`continuity-table.md`、9 个 `cell-XX.md`、一份 README。**正确**：回复里一段提示词 + 3 行补充说明。
2. 把 Bible 当交付物贴出来，用户还得自己拼。**正确**：Bible 只体现为提示词里的常量和交付时那几行"我补了什么"。
3. 用户改一句台词，就把整包重新生成一遍。**正确**：只改那一格的描述行，其它原样。

## 下一步（skill 自身迭代方向）

1. 攒 3–5 个不同类型的 Bible 范例（群像、跨地点、夜戏），把"类型 → Bible 重点"补实。
2. 给 `assemble.py` 加 `--render`，直接调出图工具并把成品回填，形成提案闭环。
3. 把「九格节奏模板」做成三种预设（闹剧 / 悬疑 / 温情），减少每次手填。
