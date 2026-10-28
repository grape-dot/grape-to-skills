# 皮克斯风格规格（硬约束，每次都要过一遍）

角色设计与场景**必须是皮克斯风格**。这不是"加一句 in the style of Pixar"就完事——那五个词在模型里会退化成"圆脸大眼 + 塑料高光"，正是最像 AI 的那种皮克斯。

先记住皮克斯自己的立场，它决定了后面所有取舍：

> "It looked so real! ... we realized we had to go further with stylization than we'd ever gone before."
> —— John Lasseter，谈《海底总动员》第一次珊瑚礁测试

> "Realism has never been a goal. You can just get pulled out of 'realistic' so quickly."
> —— Danielle Feinberg，皮克斯灯光摄影指导

所以皮克斯 ≠ 写实渲染，是**风格化写实**：造型往外推，材质往里收，光被人为编排。三条同时成立才像，缺一条就变成"廉价 3D"或"写实怪兽"。

## 六轴规格

### 一、造型：剪影优先，一种形状语言

| 项 | 规格 | 为什么 |
| --- | --- | --- |
| 剪影测试 | 缩到拇指大、填成纯黑，仍能认出是谁 | 皮克斯的第一道关，剪影糊了后面全白做 |
| 形状语言 | 每个角色只允许**一种**主动力形状：圆＝友善、方＝可靠/笨重、三角＝威胁/紧张 | 混用两种形状，观众读不出性格 |
| 头身比 | 幼态角色 1:2–1:3；成年角色 1:4–1:5 | 越小越幼，这是硬比例不是风格 |
| 眼睛占比 | 眼高约占脸高 **1/3**，位置偏低 | 洛伦兹 1943 的"婴儿图式"，皮克斯全片在用 |
| 五官数量 | 简化。鼻、耳、眉能省就省，省下的细节全给眼睛和嘴 | 表情带宽有限，细节一多就摊薄 |
| 不完美 | 每个角色至少留一处：歪笑、磨损、补丁、乱毛 | 完美＝塑料，缺口才是 appeal |

**不要**把"可爱"写成形容词。写成数字：头身比、眼脸比、几个爪子、几撮毛、身高几厘米。

### 二、材质：可信但不写实

| 项 | 规格 |
| --- | --- |
| 次表面散射 | 只出现在毛发边缘、耳、鼻、颊；散射距离**短**，散射色偏暖。全身发亮＝蜡像 |
| 粗糙度 | 皮肤/毛 0.35–0.55，布料 0.6–0.8，金属 0.25–0.4 但带脏污与指纹 |
| 纹理 | 手绘感、色阶清晰、噪点少；布料见织纹，木头见纤维与磕碰，金属见划痕 |
| 减法 | 次要物件一律降细节。皮克斯的远景是"剪影化的体块"，不是密密麻麻的零件 |

### 三、光：一束主光 + 一层轮廓，且是人编的

- **单一主光方向**，全片一致。面积光为主（影子边缘柔），阴影终止线可以偏硬以便读形。
- **轮廓光把角色从背景剥离**，只打一侧。两侧都有轮廓光是最典型的 AI 破绽。
- 阴影**可以带颜色**（皮克斯在《夏日友晴天》里专门做了 shadow fringe，把阴影染成夏天的暖紫）。
- 允许违反物理：反光板不存在也补光、灰尘在光柱里悬停——只要"看着对"。
- 禁止"处处黄金时刻"。每张图都逆光暖雾，等于没有光。

### 四、色：一个段落一个色彩关系

- 每个情绪段落定一组主色关系（互补或邻近），**不是每格换一套**。
- 高饱和但不刺眼：靠明度分层和冷暖对比造丰富度，不靠堆色相。
- **暗部不死黑**：最暗处仍保留色相信息，压到近黑会让画面"数码味"。
- **高光不切白**：留出高光层次，纯白只给最亮的那个点。
- 一格里只允许一个"最亮焦点"，眼睛永远在这个位置上。

### 五、空间：可信的重量，夸张的尺度

- 大气透视：越远越降对比、降饱和、偏向天光色。远景必须"化开"。
- 尺度可以夸张，但**重力、接触阴影、材质厚度必须对**——可信的物理撑住不可信的造型。
- 相机：35mm 上下，低机位强化体量，浅景深把主体从背景里切出来。
- 构图不许正中对称。三分、偏心、刻意失衡。

### 六、表演：可读优先

- 表情夸张 15–20%，到"再推一点就破形"为止。
- 眼睛必须有高光（catchlight），且高光位置服从主光——死鱼眼是 3D 感最大来源。
- 一个镜头只演一个情绪，别让脸同时悲喜。

## 三个可粘贴片段

**场景段（跟在 SETTING / LIGHT 后面）**

```
RENDER LANGUAGE: a Pixar-style 3D animated feature frame — stylized realism, not
photoreal: forms pushed and simplified, materials kept tactile and believable.
Soft area-light key with a single direction, one-sided rim light separating the
subject from the background, shadows tinted toward the sky colour rather than
neutral black, atmospheric perspective dissolving distance, blacks lifted (no
crushed black), highlights rolled off (no clipped white), 35mm-equivalent lens
with shallow depth of field, one brightest focal point per frame.
```

**角色段（造型锁之后）**

```
DESIGN LANGUAGE: Pixar character design — silhouette-first, one dominant shape
language, eyes about one third of the face height and set low, features reduced to
the minimum that reads, one deliberate imperfection kept, subsurface scattering
only at fur edges, ears, nose and cheeks, soft short-scatter warm tone, matte
non-glossy surfaces, believable weight and contact shadows.
```

**负面段（追加到 NEGATIVE）**

```
plastic or wax-like surfaces, glossy specular sheen, rim light on both sides,
golden-hour haze everywhere, crushed blacks, clipped whites, neon oversaturation,
perfectly symmetrical composition, over-detailed clutter, doll eyes without
catchlights, near-photoreal uncanny human, generic "3D render" look, low-poly
faceted shading
```

## 落到分镜页上怎么用（关键）

这张交付物是**石墨分镜纸**，不是一张剧照。所以"皮克斯"分两层落：

| 层 | 规则 |
| --- | --- |
| 纸面形式 | 仍是白纸、细抖红框、石墨速写、蓝墨箭头、手写批注——**不要**把整页做成 3D 渲染 |
| 画面内容 | 九格里的世界必须读作"一部皮克斯电影的分镜"：造型比例、形状语言、光影逻辑、色彩关系全部按上面六轴 |
| 右栏肖像 | 全页唯一的"完成品"，皮克斯 3D 渲染，六轴全部生效 |
| 单格稿（模板 B） | 石墨为主，但**体块关系与光位**必须已经是皮克斯的；不许画成扁平插画 |

一句写进提示词的话，能省掉九格的解释：

```
Each panel is a graphite production sketch OF a Pixar-style 3D film frame — the
drawing medium is pencil, the world inside the frame is Pixar.
```

## 与限色预算的冲突（必须提前处理）

皮克斯看起来色彩丰富，靠的是**明度分层 + 冷暖对比**，不是色相数量。所以六色预算不需要放开：

- 同一色相给 3–4 个明度台阶（例如云朵奶白 #EFE7D8 到褪色天空 #A6B4BC 之间还有两层）。
- 用色温区分前后景：前景暖、远景冷，一个色相能演出两个空间。
- 真要"更多颜色"时，先加明度台阶，别加色相。

## 自检（30 秒版）

1. 把主角剪影填黑缩小——还认得出吗？
2. 每个角色是不是只有一种形状语言？
3. 眼睛占脸高够不够 1/3？高光在不在主光那一侧？
4. 轮廓光是不是只在一侧？
5. 暗部有没有死黑？高光有没有切白？
6. 远景有没有化开？还是和前景一样清楚？
7. 有没有一处故意的不完美？

七条里错两条以上，重写提示词，别指望后期修。

## 出处

- Pixar 官网《Finding Nemo》制作页：色彩脚本（Ralph Eggleston）、"too real → 必须更风格化"的原话
- RenderMan《Stylization at Pixar》：shadow fringe（Luca）、可艺术化操控的体积与水面、材质分层
- Business Insider / Tech Insider 对 Danielle Feinberg 的访谈：光如何服务叙事、"realism has never been a goal"、murk 光与大气透视
- 洛伦兹 1943 婴儿图式（baby schema）：大头、大眼、小鼻、圆身的幼态偏好
