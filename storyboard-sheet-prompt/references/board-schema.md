# Board JSON schema

`assemble.py` 的输入格式。只用它做三件事时**才需要**写这个文件：同一套设定要复用、九格要逐格改、九格跨多轮做。一次性任务直接手写提示词更快。

完整可运行范例：`examples/nut-crisis.json`。

## 校验规则速览

| 规则 | 违反后 |
| --- | --- |
| `shots` 必须正好 9 条 | exit 2，`必须正好 9 格` |
| 每格 `props` / `state` 里的 id 必须在 `props[]` 注册 | exit 2，`未登记的道具` |
| `state` 的值必须在对应 `states[]` 枚举内 | exit 2，`不在枚举内` |
| 对白必须全英文 | exit 2，`对白混入中文` |
| `hex` 必须 `#RRGGBB` | exit 2，`hex 不合法` |
| `props[].id` / `characters[].id` 不得重复 | exit 2，`重复` |
| 色板 ≥ 4 色 | exit 2 |
| 单句对白 > 8 词、同镜别连续 3 格、第 9 格非 WIDE、第 5/6 格无尺度跳跃 | **警告**，不阻断 |

## 顶层

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `meta` | ✅ | 页眉 |
| `world` | ✅ | 空间 / 视轴 / 比例 / 光位 |
| `palette` | ✅ | ≥ 4 条 |
| `characters` | ✅ | 造型锁 |
| `props` | ✅ | ≥ 3 条 |
| `shots` | ✅ | 正好 9 条 |
| `notes` | ✅ | 底部三框的文字内容 |
| `villain` | 可选 | 反派/道具小栏 |
| `inferred` | 可选 | 你替用户补全的设定，交付时要说明 |
| `negative_extra` | 可选 | 覆盖默认 negative 串 |

## meta

```json
{
  "production": "NUT CRISIS",
  "scene_id": "SC 1.1",
  "scene_title": "THE KITCHEN JOB",
  "shots_label_zh": "镜头1.1.1至1.1.9",
  "aspect": "16:9"
}
```

`shots_label_zh` 是页面左上角那行**中文手写镜号**，全页唯一允许的中文。

## world

四个 `_en` 全部必填，`_zh` 供中文版使用（缺省回退到 `_en` 并标 `[待译]`）。

| 字段 | 写什么 | 反例 |
| --- | --- | --- |
| `space_en` | 什么空间、什么视角、多大 | ❌ a kitchen ✅ a domestic kitchen seen from counter height: marble counter screen-right, wire cage screen-left, wall cabinet above |
| `axis_en` | 屏幕左右各是什么 | ✅ screen-left = cage, screen-right = counter; never mirrored |
| `scale_en` | 主角与场景的具体比例 | ✅ counter 90 cm, hamster 15 cm, roughly 6:1 |
| `light_en` | 主光方向 + 色温 + 补光 | ✅ single warm window key from frame-left 45°, cool fill from right, no overhead |

皮克斯风格常量**不写进这里**，由 `references/pixar-style.md` 统一提供，脚本会自动注入。

## characters[]

```json
{
  "id": "jian",
  "name_en": "AGENT JIAN",
  "name_zh": "仓鼠特工阿坚",
  "lock_en": "a very round golden hamster, fur #B07B3E, cheeks stuffed wider than his head, no clothing and no accessories",
  "lock_zh": "……",
  "anchors": ["over-stuffed cheeks", "pear silhouette", "cream belly"],
  "traits_en": "OVERCONFIDENT · THEATRICAL · LOYAL",
  "traits_zh": "自信爆棚 · 戏多 · 嘴硬心软",
  "sketch_en": "loose pencil study, three quick gesture poses",
  "render_pose_en": "standing with paws on hips, chin lifted",
  "caption_lines": ["AGE: 1-2 YRS · LENGTH: 15 CM", "CODENAME: NUT-01"],
  "voice_en": "bright nasal tenor 320-420 Hz, 4.5-5.5 syl/s"
}
```

硬要求：

- `lock_en` 只写**形状 / 颜色 / 尺寸 / 缺省**，不写性格形容词。
- 必须显式 `no clothing and no accessories`。
- `anchors` 至少 3 条，每条都要能在画面上看见。

## props[]

```json
{
  "id": "nut_bag",
  "name_en": "the burlap nut bag",
  "name_zh": "粗麻坚果袋",
  "lock_en": "a small burlap nut bag, warm mid-brown #8A5A2B, one frayed corner",
  "lock_zh": "……",
  "states": ["upright_on_shelf", "tipping", "burst_open", "flattened_on_floor"],
  "scale_en": "8 cm tall"
}
```

- `name_en` 是唯一合法称呼，正文不许出现同义词。
- `states` 是非空枚举时必须填；跨格只能取枚举内的值，且转移要讲得通。

## shots[]

```json
{
  "n": 1,
  "framing": "NEAR",
  "action_en": "extreme close-up on the seed bowl as a weapons cache",
  "action_zh": "把食盆当军火库拍极近特写",
  "props": ["bowl", "raisin"],
  "state": { "bowl": "heaped", "raisin": "beside_bowl" },
  "arrow_en": "primary objective",
  "arrow_zh": "首要目标",
  "dialogue": [{ "who": "jian", "line_en": "Inventory check. Nuts: secured." }],
  "camera_en": "macro, lens touching the bowl rim"
}
```

| 字段 | 说明 |
| --- | --- |
| `framing` | `NEAR` / `MEDIUM` / `MED-WIDE` / `WIDE` / `BEAUTY` |
| `action_en` | 一句画面描述，尽量 ≤ 40 词 |
| `props` | 本格**入画**的道具 id |
| `state` | 本格道具状态，key 为 id |
| `arrow_en` | 蓝箭头注释，2–5 词 |
| `dialogue[].who` | 角色 id；`line_en` 必须英文、≤ 8 词 |
| `camera_en` | 可选，单格放大稿会用 |

默认节奏：`NEAR / MEDIUM / NEAR / NEAR / MED-WIDE / MEDIUM / NEAR / BEAUTY / WIDE`。

## notes

```json
{
  "flow_en": "Every errand is a heist. INHALE — scout, plan, order. EXHALE — launch, crash, roast.",
  "flow_zh": "每个任务都是一场大戏……",
  "camera_en": "Open tight on the hardware; drop low so the kitchen towers; pull back as the farce grows; land wide and warm.",
  "camera_zh": "……"
}
```

对应页面底部三个手写框的前两个；第三个由 `palette` 自动生成。

## 校验不过时怎么办

脚本会一次列出**所有**错误再退出，不会只报第一条。按报错顺序改，改完重跑 `--check-only` 确认，再正式渲染：

```bash
python scripts/assemble.py board.json --check-only
```
