# 场景资产锁定表（Scene Bible）

这一份表是九格的**唯一事实来源**。表里没有的，画面上就不许有；表里怎么写的，九格就怎么抄。

## 为什么需要它

逐格写提示词时，模型每次都在重新"想象"这个场景。第 1 格它觉得食盆该是白瓷的，第 7 格同一个盆变成不锈钢的；第 3 格的木屑是浅黄，第 9 格变成粉红。这不是模型笨，是**你没给它一个不可变的引用**。

Bible 的作用：把"可以变的东西"和"不许变的东西"分开。角色在动、道具在移位，但**外观字符串、颜色、尺寸比、光位、视轴**这五样是冻结的。

## 一、空间（World）

### 必填

| 字段 | 说明 | 反例 |
| --- | --- | --- |
| `space` | 一句话说清这是什么空间、什么视角、多大 | ❌"一个厨房" ✅"住宅厨房台面区域，含大理石台面、上方双门吊柜、地面木屑区，平视略俯" |
| `axis` | 屏幕左右各是什么，写死 | ✅"screen-left = 仓鼠笼与木屑区，screen-right = 大理石台面与高处吊柜，全页不镜像" |
| `scale` | 主角 vs 场景的具体尺寸比 | ✅"台面高 90cm，仓鼠体长 15cm，约 6:1；吊柜离台面 60cm" |
| `light` | key light 方向 + 色温 + 补光 | ✅"单一暖白窗光从画面左侧 45° 打入，右侧冷灰补光，无顶光" |

### 规则

- **轴不可翻**。这条比什么都重要。观众靠左右方位建立空间感，第 5 格一旦镜像，整页就散了。需要反打（看到角色背面朝向柜子）时，必须显式写 `reverse angle, axis intentionally flipped` 并在台账里标注。
- **比例必须数字化**。写"巨大的厨房"模型给你一个普通厨房；写"台面 90cm / 仓鼠 15cm"它才会压低机位。
- **光位一次定死**。除非剧情有时间跨越，否则九格同一个光。改变光位等于换了一个时空。

## 二、道具注册表（Props）

每个出现在画面里的物件都要注册。**没注册的物件出现 = 事故**。

### 字段

```json
{
  "id": "nut_bag",
  "name_en": "the burlap nut bag",
  "name_zh": "粗麻坚果袋",
  "lock_en": "a small burlap nut bag, warm mid-brown #8A5A2B, one frayed corner, sits upright, about one-third the hamster's height",
  "lock_zh": "粗麻小坚果袋，暖中棕 #8A5A2B，一角磨毛，直立放置，高度约为仓鼠的三分之一",
  "states": ["upright_on_shelf", "tilting", "falling", "burst_open", "flattened_on_floor"],
  "scale": "8cm tall"
}
```

### 规则

- **`name_en` 是唯一合法名字**。正文里不许出现同义词。`nut bag` 就是 `nut bag`，不许写 `seed sack`、`bag of nuts`、`the sack`。
- **`lock_en` 一次性写完，以后逐字复制**。包括颜色 hex、磨损细节、朝向。这句是防漂移的锚。
- **`states` 是枚举，不是描述**。跨格移动只能在枚举值之间走，而且要**合法转移**：`upright_on_shelf → tilting → falling → burst_open → flattened_on_floor` 是链；从 `flattened_on_floor` 直接跳回 `upright_on_shelf` 必须有一格交代"谁把它扶起来"。
- **道具数量守恒**。坚果袋爆开后有 40 颗坚果，那第 8 格地上就该还有一堆；突然全消失，观众会觉得跳帧。允许"被扫走"，但要在台账里记一句。
- **可互动小物单独注册**。葡萄干望远镜、橡皮筋弹射器、吸管冰镐、草饼——这些是喜剧支点，必须有自己的 id，不能临时"从口袋掏出一个"。

### 状态链台账（Continuity Ledger）

Bible 定完后，排一张表。每格一行，每道具一列，填该格的枚举值。

| 格 | nut_bag | nut_pile | slipper | robot |
| --- | --- | --- | --- | --- |
| 01 | —（在柜上，未入画） | `full` | `by_door` | `docked` |
| 02 | — | `full` | `by_door` | `docked` |
| 03 | — | `full` | `by_door` | `docked` |
| 04 | — | `full` | `worn_by_hamster` | `carrying_slipper` |
| 05 | `upright_on_shelf` | `full` | `by_door` | `idle` |
| 06 | `upright_on_shelf` | `full` | `by_door` | `idle` |
| 07 | `burst_open` | `full` | `by_door` | `idle` |
| 08 | `flattened_on_floor` | `full` | `by_door` | `idle` |
| 09 | `flattened_on_floor` | `full` | `by_door` | `passing` |

这张表的用处：写第 7 格提示词时，你知道 `nut_pile` 还必须是 `full`（因为结局要用它），所以第 7 格的散落坚果只能是 **袋子里掉出来的**，不能动盆里的。这个约束会自动让画面变合理。

## 三、角色锁（Characters）

每个角色三块内容：**造型锁**（每格复用）、**素描描述**（右侧素描用）、**3D 肖像描述**（右侧渲染用）。

### 造型锁字段

```json
{
  "id": "jian",
  "name_en": "AGENT JIAN",
  "lock_en": "a very round golden hamster, plump pear-shaped body, fur warm golden-brown #B07B3E with cream belly, cheeks permanently stuffed and bulging beyond the head width, tiny pink paws, black bead eyes, no clothing, no accessories",
  "anchors": ["over-stuffed cheeks", "pear silhouette", "cream belly"],
  "ratio": "body twice as wide as the head"
}
```

规则：

- **`anchors` 是三件套**，每格必须至少出现两件。这是观众认出"这是同一只"的依据。
- **`no clothing, no accessories` 必须显式写**。不写，模型会自作主张给仓鼠加个小领结或墨镜，第 4 格又没了。
- **`ratio` 数字化**。"圆滚滚"没意义，"体宽是头宽的两倍"才有意义。
- **不要写性格形容词进 lock**。`scrappy and confident` 对造型没约束，只会让模型给它摆个威风姿势。性格进对白和动作，造型锁只写形状/颜色/尺寸。

### 3D 肖像描述模板

右侧那一栏是**全页唯一的 3D 皮克斯渲染**，也是模型最容易画成"塑料玩具"的地方。必须给材质与灯光词：

```
Pixar-style 3D character portrait, {character}, {lock_en},
soft subsurface scattering on fur, individual fur strands catching rim light,
oversized expressive eyes with wet catchlights, three-quarter view, shallow depth of field,
warm key light from upper left with cool rim light from behind,
neutral warm-grey studio backdrop, high-end animation character sheet render, 8k
```

### 图注规范

图注是**手写小字**，2 行、每行 ≤ 12 个字符最稳。写成：

```
AGE: 1–2 YRS   ·   LENGTH: 15 CM
CODENAME: NUT-01
```

超过 3 行模型会糊。中文图注同理，每行别超过 8 个字。

## 四、色板（Palette）

**5 色 + 1 个例外**。这不是装饰建议，是硬预算。

| 用途 | 数量 |
| --- | --- |
| 角色毛色 | 2（每角色 1） |
| 环境主色 | 2（地面材质 + 硬表面） |
| 道具/食物 | 1 |
| 例外：反派金属 | 1（可省） |

加页面的中性色：纸白、石墨灰、红框、蓝箭头。**这些不算进 5 色**——它们是媒介色，不是场景色。

```json
{ "id": "hamster_gold", "name_zh": "仓鼠金棕", "name_en": "hamster gold-brown", "hex": "#B07B3E", "use_en": "Jian's fur only, nowhere else" }
```

规则：

- 每个色写 `use_en`（用在哪），且**排他**。`#B07B3E` 只能用在阿坚毛上，不许出现在坚果上，否则角色会"融进"背景。
- hex 要真的互斥。五个都是暖棕，等于只有一个颜色。
- 底部那个"五色交叉阴影色块"就是这五块，按顺序排，每块用铅笔画交叉排线。

## 五、右侧面板与底部三框

### 右侧面板结构

```
CHARACTER DESIGN & CASTING
├─ 角色 A：名字（大字手写）
│   ├─ 特征行：3 个短标签
│   ├─ 铅笔素描（左侧，6 成大小）
│   └─ 3D 肖像（右侧，4 成大小）
│   └─ 图注：年龄 / 体长 / 代号
├─ 角色 B：同上
└─ VILLAIN / PROPS（小栏，约 1/4 高度）
    ├─ 铅笔小图 + 3D 小图
    └─ 图注：威胁等级 / 实际功能
```

注意"特征"一栏是**短标签不是句子**：`自信爆棚 · 戏多 · 嘴硬心软`。写长句会挤掉素描位置。

反派图注用**反差幽默**格式：`THREAT LEVEL: LOW` / `ACTUAL FUNCTION: spins in circles, eats slippers`。这一栏是整页的笑点收尾，别写成正经的技术参数。

### 底部三框

| 框 | 内容规范 | 长度 |
| --- | --- | --- |
| 笔记/流程意图 | 用"吸气—呼气"式的节拍隐喻写整场的能量曲线 | 3–4 行，每行 ≤ 20 字 |
| 镜头/故事笔记 | 4 条运镜意图，每条一个理由 | 4 行，每行 ≤ 18 字 |
| 色彩调色板 | 5 个交叉阴影色块 + 名称 | 只放色块，不放解释 |

三框都是**手写体，横线画歪一点**。这是"真实前期文档"的质感来源。

## 六、推断项要声明

用户给的情景通常不全。你补的东西（比如"厨房有窗"）要标出来：

```json
"inferred": ["厨房有左侧窗户（用户未提及，为解释暖侧光而补）", "地面为木地板 + 木屑区"]
```

交付时用一句话告诉用户："我补了三处，你看要不要改。" 这样他不会以为你在瞎编，也知道该改哪里。
