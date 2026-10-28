# 提示词模板（可直接粘贴）

四个模板，按用途选。方括号 `{}` 是要替换的槽位，其余**原样保留**——保留部分就是防漂移的骨架。

> 默认路径是**照模板 A 手写英文段 + 中文段，两段一起回复给用户**，不落盘、不建 JSON。
> 只有要复用 / 要逐格返工 / 九格跨多轮做时，才把内容写成 `storyboard.json` 交给 `assemble.py`。

## 皮克斯常量（每一份提示词都要带，不能省）

角色与场景的皮克斯风格是硬约束，规格、数字、出处见 `references/pixar-style.md`。落到模板里就是三处：

| 位置 | 写什么 | 模板 A/B 里的落点 |
| --- | --- | --- |
| `RENDER LANGUAGE` 段 | 风格化写实、面积光单方向、单侧轮廓光、阴影带天光色、大气透视、抬黑不切白、35mm 浅景深、一格一个最亮焦点 | 紧跟在 `LIGHT` 行后面 |
| `DESIGN LANGUAGE` 行 | 剪影优先、一种形状语言、眼高≈脸高 1/3 且偏低、五官做减法、留一处不完美、SSS 只在毛边/耳/鼻/颊、哑光不反光 | 紧跟在 `CHARACTERS` 段后面 |
| `NEGATIVE` 追加 | 塑料蜡感、镜面高光、双侧轮廓光、处处黄金时刻、死黑、切白、霓虹过饱和、正中对称、堆细节、无高光的死鱼眼、近写实恐怖谷 | 负面段末尾 |

**别用"in the style of Pixar"这五个词顶替上面三段**——它只会让模型自动补上"圆脸大眼 + 塑料高光"，那是最像 AI 的假皮克斯。

## 中英两段怎么写（默认交付形态）

1. 先用模板 A 写完英文段，九格连着写。
2. 再对着**同一份 Bible** 写中文段——不是翻译，是重述：句序可以按中文习惯改，但下列东西必须逐字照抄：
   - 所有 hex（`#2F6FB0` 就是 `#2F6FB0`，不许写成"天蓝色"）
   - 道具英文名（`the giant paint roller` 在中文段仍写英文名，或"英文名（中文注释）"）
   - 镜别（NEAR / MED-WIDE / WIDE / BEAUTY 照抄，别译成"近景/中宽"后不标原词）
   - 对白原文（英文台词不动，中文只补一句译注）
3. 中文段要**完整**：页眉、SETTING、CHARACTERS、PROPS、九格、右栏、页脚、色板、负面、一致性规则，一段不少。删繁就简的中文段等于没有。

---

## 模板 A：整页九格（默认）

```
A single flat sheet of white production paper, scanned overhead, no perspective on
the paper itself. Aspect ratio 16:9. This is a professional animation pre-production
storyboard sheet — mixed media, part graphite pencil, part red and blue ink, part
finished 3D render.

PAGE HEADER, top left: handwritten Chinese marker script reading "镜头1.1.1至1.1.9".
Top right, small handwritten caps: "SC 1.1 · {PRODUCTION} · {SCENE TITLE}".
A thin hand-ruled horizontal line under the header.

LEFT TWO THIRDS — STORYBOARD GRID
Exactly nine panels, arranged in 3 rows and 3 columns, each panel a thin hand-drawn
red ink rectangle (1.5–2 px, slightly wobbly, corners slightly overrunning) with a
16:9 image area inside. Shot number written by hand at the lower-left OUTSIDE each
frame, with a small caps framing label beside it. One short handwritten action note
per panel (max 8 words), outside the frame. Blue ballpoint arrows drawn outside the
frames, pointing in at the relevant object, each with a 2–5 word handwritten note at
its tail.

SETTING (identical in all nine panels, do not vary): {WORLD.space}
SCREEN AXIS (never mirrored): {WORLD.axis}
SCALE: {WORLD.scale}
LIGHT (same in all nine panels): {WORLD.light}

RENDER LANGUAGE (identical in all nine panels): a Pixar-style 3D animated feature
frame — stylized realism, not photoreal: forms pushed and simplified, materials kept
tactile and believable. Soft area-light key with a single direction, one-sided rim
light separating the subject from the background, shadows tinted toward the sky
colour rather than neutral black, atmospheric perspective dissolving distance,
blacks lifted (no crushed black), highlights rolled off (no clipped white),
35mm-equivalent lens with shallow depth of field, one brightest focal point per frame.
Each panel is a graphite production sketch OF a Pixar-style 3D film frame — the
drawing medium is pencil, the world inside the frame is Pixar.

CHARACTERS (identical in all nine panels, copy verbatim):
{CHARACTER A lock_en}
{CHARACTER B lock_en}
DESIGN LANGUAGE: Pixar character design — silhouette-first, one dominant shape
language per character, eyes about one third of the face height and set low,
features reduced to the minimum that reads, one deliberate imperfection kept,
subsurface scattering only at fur edges, ears, nose and cheeks, soft short-scatter
warm tone, matte non-glossy surfaces, believable weight and contact shadows.

PROPS (the only objects allowed to appear; nothing else may be invented):
{PROP lock_en} ×N

PANEL 01 — {FRAMING} — {action_en} — props present: {ids} — hand note: "{arrow}"
PANEL 02 — ...
...through PANEL 09

RIGHT THIRD — "CHARACTER DESIGN & CASTING" (handwritten caps header)
Two character entries stacked vertically, plus a small villain/prop block at the
bottom. Each character entry: name in large handwritten caps, three short trait
tags, a loose graphite pencil sketch on the left, a finished Pixar-style 3D
character portrait on the right, and a two-line handwritten caption underneath.

{CHAR A}: tags "{t1} · {t2} · {t3}".
  graphite sketch: {sketch_en}
  3D portrait: Pixar-style 3D character render, {lock_en}, soft subsurface scattering
  on fur, individual fur strands catching rim light, oversized expressive eyes with
  wet catchlights, three-quarter view, shallow depth of field, warm key light from
  upper left, cool rim light from behind, neutral warm-grey studio backdrop.
  caption: "AGE: {age} · LENGTH: {len}" / "CODENAME: {code}"

{CHAR B}: same structure, caption "AGE · LENGTH" / "ROLE: {role}"

VILLAIN / PROPS block (small, about one quarter of the right column):
  graphite mini-sketch + small 3D render of {VILLAIN}, caption
  "THREAT LEVEL: {x}" / "ACTUAL FUNCTION: {y}"

BOTTOM STRIP — three hand-drawn boxes with hand-ruled borders:
Box 1 "NOTES / FLOW INTENT": {3–4 short lines}
Box 2 "CAMERA / STORY NOTES": {4 short lines}
Box 3 "COLOR PALETTE": five small cross-hatched colored-pencil swatches, labelled
  {palette names}, plus one small dark metallic grey swatch for the robot.

PALETTE — the ONLY colors permitted anywhere on this sheet:
{palette id: hex — use}
Page neutrals (not counted): paper white, graphite grey, red ink #C0392B,
blue ink #2F4C8A.

STYLE: authentic film pre-production document, drawn from a Pixar-style 3D feature.
Loose confident graphite sketching, visible construction lines and smudged hatching,
thin wobbly red frames, quick blue arrows, handwritten uppercase notes, two polished
3D character renders pasted into the right column. Clean white paper with faint fiber
texture. NOT digital-flat, NOT vector, NOT neon, NOT gradient-heavy.

NEGATIVE: more than nine panels, empty panel, photo-real human, extra characters,
clothing or accessories on the animals, glossy plastic toy look, wax-like surfaces,
specular sheen, rim light on both sides, golden-hour haze everywhere, crushed blacks,
clipped whites, neon oversaturation, perfectly symmetrical composition, over-detailed
clutter, doll eyes without catchlights, neon rim light, gradient backgrounds, long
paragraphs of text, garbled lettering, colored frames, thick borders, watermark,
signature.
```

---

## 模板 B：单格放大（关键帧高清）

```
Single storyboard panel, 16:9, presented on white production paper with the thin
hand-drawn red ink frame still visible. Shot number "{NN}" and the framing label
"{FRAMING}" handwritten OUTSIDE the frame at lower left, one short action note
underneath, plus a small blue ballpoint arrow with a "{note}" annotation.

SUBJECT: {action_en}
CHARACTERS: {lock_en, verbatim — both if both appear}
PROPS IN FRAME: {prop ids and their states this frame}
SETTING: {WORLD.space}
SCALE: {WORLD.scale}
LIGHT: {WORLD.light}
CAMERA: {lens / height, e.g. low angle at counter-edge height, 35mm equivalent, slight
wide distortion to exaggerate the counter's mass}

STYLE: loose graphite pencil with visible hatching, one accent color blocked in with
colored pencil, cinematic composition, film storyboard clarity — readable silhouette
first, detail second. The frame describes a Pixar-style 3D film frame: stylized
realism, eyes about one third of the face height, one-sided rim light, shadows tinted
toward the sky colour, lifted blacks, 35mm shallow depth of field.
PALETTE: {palette hexes}
NEGATIVE: text paragraphs, signatures, extra limbs, wrong fur pattern, no red frame
(nothing: keep the red frame), plastic sheen, rim light on both sides, crushed blacks,
photoreal uncanny human.
```

> 单格版保留红框是有意的：它让成品仍然"看起来是分镜"，而不是一张插画。提案时这点很重要。

---

## 模板 C：角色肖像（右侧栏用）

```
Pixar-style 3D character portrait of {character}, {lock_en}.
{pose/expression: e.g. standing with tiny paws on hips, chin lifted, absolutely
certain of himself}
DESIGN LANGUAGE: silhouette-first, one dominant shape language, eyes about one third
of the face height and set low, features reduced to the minimum that reads, one
deliberate imperfection kept, believable weight and contact shadows.
Soft subsurface scattering limited to fur edges, ears, nose and cheeks, short
scatter distance, warm scatter tone, matte non-glossy surfaces, individual fur
strands catching rim light on ONE side only, oversized expressive eyes with wet
catchlights placed on the key-light side, three-quarter view, shallow depth of field,
warm key light from upper left, cool rim light from behind, neutral warm-grey studio
backdrop, highlights rolled off (no clipped white), lifted blacks, high-end animation
character sheet render, 8k.
PALETTE: fur {hex}, belly {hex}, eyes {hex}.
NEGATIVE: human clothes, accessories, glasses, hats, cartoon-flat shading, plastic
toy gloss, wax-like skin, harsh specular highlights, rim light on both sides,
perfect symmetry, extra fingers, anime style, photoreal uncanny human.
```

---

## 模板 D：反派/道具小卡

```
Small prop design card in the style of a pre-production prop sheet.
{PROP lock_en}.
Left: quick loose graphite sketch. Right: the same object as a small, clean 3D render.
Below: handwritten caption in two lines, "{THREAT LEVEL: x}" / "{ACTUAL FUNCTION: y}".
White paper, faint fiber texture, pencil construction lines visible on the sketch side.
NEGATIVE: text paragraphs, glossy product photography, dramatic lighting, background props.
```

---

## 拼装顺序（重要）

不要把所有槽位一次填满就去生成。按这个顺序写，出错时好定位：

1. 先写 `WORLD` 三行（space / axis / scale / light）——**这四行定生死**
2. 再写角色锁（逐字，不润色）
3. 再写道具锁
4. 再写九格（每格只填 action + framing + props + note）
5. 最后写右栏与页脚

顺序反了（先写九格的画面感），Bible 就会被九格"带跑"，最后九格各有各的世界。

## 常见填空错误

| 错误 | 后果 | 正确做法 |
| --- | --- | --- |
| 角色锁里写性格 | 模型给它摆威风姿势、加道具 | 只写形状/颜色/尺寸 |
| 同名道具两种写法 | 出现两个不同的东西 | 用 `name_en` 原文 |
| 每格重写一遍场景 | 场景在九格里漂移 | 场景只在 `SETTING` 写一次，九格写 `identical, do not vary` |
| 动作说明写完整句子 | 画面被文字挤占 | ≤ 8 词 |
| 忘了 `no clothing` | 第 4 格冒出小墨镜 | 造型锁里显式否定 |
| 色板只写名字不写 hex | 模型自由发挥 | hex 全写 |
