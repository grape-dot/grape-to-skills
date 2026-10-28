# 语音反差设定（Voice Casting）

## 核心原则：反差是差值，不是形容词

写 `a funny squeaky voice and a lazy slow voice` 是无效的——模型（和配音演员）得到的是两个模糊印象，出来的结果是"两个都挺可爱"，没有张力。

有效写法是**在四个轴上把差值拉开并量化**：

```
PITCH CENTER     320–420 Hz   ←→   140–180 Hz        （差一个八度以上）
SYLLABLE RATE    4.5–5.5 /s   ←→   2.5–3 /s          （差近两倍）
SENTENCE LENGTH  3–7 words    ←→   3–6 words, 但句尾拖 0.6s
BREATH           inhale before every line   ←→   long exhale, chewing
MIC POSITION     5 cm, dry    ←→   1.5 m, small room  （差一个空间）
```

只要这五行成立，即使台词平庸，听感上的反差也已经在了。反过来，两边都写"活泼"和"慵懒"，台词写再好也平。

## 四轴对照表

| 轴 | 主导者（仓鼠阿坚） | 吐槽者（豚鼠豆豆） | 听感结果 |
| --- | --- | --- | --- |
| **音高中心** | 高、窄、上扬，句尾必挑；紧张时轻微破音 | 中低、平、几乎单音；重音靠拉长而非提高 | 一个在"演"，一个在"评" |
| **语速** | 4.5–5.5 音节/秒，抢在对方反应之前；连珠式 | 2.5–3 音节/秒，永远慢半拍；句间停 0.4–0.6s | 一个推，一个拖 |
| **句长** | 短命令句、代号自称、排比三连 | 3–6 词，结论式；绝不超过一句 | 一个话多，一个一锤 |
| **气口** | 句前抢吸一口气（可听见）、喘、清嗓、鼻音 | 长呼气、咀嚼草叶的黏连音、叹气收尾 | 一个"紧张的身体"，一个"松弛的身体" |
| **混音** | 贴麦 5cm，干声，无混响，推 2dB，带对讲机感 | 离麦 1.5m，带小房间早期反射，永不提音量 | 一个在你耳朵里，一个在房间那头 |
| **音色质感** | 明亮、鼻音重、薄、脆 | 圆、暗、略闷、带一点糊 | 薄对厚 |

**第六条（混音）最容易被忽略，但它是"距离感"的来源。** 两个人音量一样、混响一样，观众会觉得他们在同一个话筒前念稿。混音差一出来，"一个在冲你喊，一个在远处看戏"的关系立刻成立。

## 为什么是这两个方向

仓鼠体型小、代谢快、时刻紧张——高、快、薄是这个身体的物理结果，不是性格设定。
豚鼠体型大、代谢慢、吃草为生——低、慢、厚同理。

**从身体推声音，比从性格推声音稳得多**，因为身体参数不会在第 5 格变。

## 提示词块（可直接粘贴）

### 全局语音导演条

```
VOICE DIRECTION — bilingual animation, dialogue in ENGLISH only.
Two characters must sit at opposite ends of the same four axes. Never let them
share pitch center, syllable rate, reverb, or mic distance.

AGENT JIAN (hamster, the one who believes he is a spy):
bright nasal tenor, fundamental around 320–420 Hz, upward terminal contour on every
line, 4.5–5.5 syllables per second, clipped plosives, audible inhale before each
utterance, occasional voice crack under stress, close-mic at 5 cm, completely dry,
no reverb, pushed +2 dB as if leaning into a walkie-talkie.

DOUDOU (guinea pig, unwilling tech support):
low flat baritone, fundamental around 140–180 Hz, near-monotone, elongation instead
of pitch rise for stress, 2.5–3 syllables per second with 0.4–0.6 s gaps between
phrases, vowels smeared by half-chewed grass, ends lines on a long exhale or a sigh,
positioned 1.5 m back, small-room early reflections, never raises volume.

CONTRAST FLOOR: every exchange must differ by at least one octave in pitch center
and at least 1.8x in syllable rate. If a line reads as interchangeable between the
two characters, rewrite it.
```

### 单角色语音卡（配音/语音合成用）

```
CHARACTER VOICE CARD
name: AGENT JIAN
body: 15 cm hamster, round, cheeks always full — the voice is squeezed by the cheeks
pitch center: 360 Hz (range 320–420)
tempo: 5.0 syl/s, back-chained, never waits for a reply
timbre: bright, nasal, thin, slightly brittle
breath: sharp audible inhale at every line start
articulation: clipped T/K/P, machine-gun rhythm
prosody: rises at the end of statements — he asks even when he commands
processing: close mic, dry, +2 dB, subtle walkie-talkie band-pass (300–3400 Hz)
never: warm, breathy, slow, resonant, whispery-villain
```

```
CHARACTER VOICE CARD
name: DOUDOU
body: 25 cm guinea pig, permanently horizontal, mouth usually full
pitch center: 160 Hz (range 140–180)
tempo: 2.7 syl/s, drags 0.5 s before answering
timbre: round, dark, slightly muffled, a little hoarse
breath: long exhale tail, chewing texture on consonants
articulation: soft, blurred sibilants, lazy lip closure
prosody: flat declaratives, stress by lengthening the stressed vowel
processing: 1.5 m distance, small room, low-pass at 6 kHz, never compressed upward
never: bright, fast, excited, squeaky, singsong
```

## 英文对白规范

### 长度

每格 **≤ 8 词**，整页 9 格**对白总数 ≤ 6 句**。分镜页不是剧本，塞满台词会毁掉画面。

### 阿坚的语法特征（三选一，别全用）

1. **代号自称**：`Agent Nut One, reporting.` / `Codename NUT-01 does not retreat.`
2. **军情腔套话**：`Intel confirmed.` / `Objective: the bag.` / `Extraction in three.`
3. **三连排比**：`Recon. Plan. Execute.` —— 他自己给自己下命令

不要给他写完整的长句。他的笑点来自"用最正式的措辞描述最蠢的事"。

### 豆豆的语法特征

1. **三个词结论**：`It's a bowl.` / `You'll fall.` / `I'm not going.`
2. **事实纠正**（冷面）：
   - 阿坚：`This is a precision instrument.`
   - 豆豆：`It's a spoon.`
3. **叹气收尾**：句末加 `...` 或一个 `Hm.` —— 书面标记他的长呼气

豆豆**永远不主动出主意**，他只在阿坚说完之后把事实摆出来。这个结构本身就是反差。

### 对白范例（可直接改用）

| 格 | 情境 | 对白 |
| --- | --- | --- |
| 01 | 装备特写 | **JIAN:** `Inventory check. Nuts: secured.` |
| 02 | 作战会议 | **JIAN:** `Recon. Infiltrate. Celebrate.` / **DOUDOU:** `That's a wheel.` |
| 03 | 弹射出发 | **JIAN:** `Launching!` / **DOUDOU:** `I did not agree to this.` |
| 04 | 圆盘将军 | **JIAN:** `Enemy armor! Evasive!` / **DOUDOU:** `It's a vacuum.` |
| 05 | 台面冰川 | **JIAN:** `Almost... there...` / **DOUDOU:** `Third time.` |
| 06 | 柜门潜入 | **JIAN:** `I am stuck. Tactically.` |
| 07 | 坚果雪崩 | **JIAN:** `Mission accomplished.` / **DOUDOU:** `You broke the bag.` |
| 08 | 生日反转 | **DOUDOU:** `...Happy birthday, agent.` |
| 09 | 广角收尾 | **JIAN:** `General Disc. Truce, today.` |

注意 08 格：豆豆第一次说完整的一句、且带 `...` 前缀。**全场唯一一次情感暴露**放在这里，比任何解释都有效。

## 出图提示词里怎么带语音

静态分镜页画不出声音，但可以带**三个视觉锚**：

1. **对白以气泡尾巴或手写引号附在格边**（不放画面里），长度 ≤ 8 词
2. **底部"镜头/故事笔记"里加一行** `VO: Jian fast/nasal · Doudou slow/flat` —— 提醒后期
3. **阿坚的嘴永远微张**（他在说话/喘），**豆豆的嘴永远在嚼**（他在吃）—— 一个视觉上的"节奏差"，替代声音

第 3 条最实用：即使读者听不到，也能从嘴部状态读出"一个急一个慢"。

## 自检：这段对白能互换吗

写完台词，问一句：**这句能不能换给另一个角色说？**

- 能换 → 没有反差，重写
- 换了明显不对 → 成立

这是唯一可靠的反差测试，比任何形容词表都准。
