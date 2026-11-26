# 组件手册（复制即用）

全部类名来自 `assets/theme.css`。**只改 `:root` 里的 token，页面里不写死字号**；
确有单页特殊需求才用内联 `style`，且必须保持 ≥18px。

## 一、页面骨架

```html
<section class="slide">
  <div class="sh">
    <div class="kick">模块 03 · 小节名</div>
    <h1 class="stitle">页面主标题：一句话给出结论</h1>
  </div>
  <div class="sb">
    <p class="lead">引导语，写这一页要记住的那句话。</p>
    <!-- 主要内容：给一块 .grow 撑满剩余高度 -->
    <div class="g2 grow"> … </div>
  </div>
  <div class="foot"><span>主题名 · 模块三</span><span class="pn">19</span></div>
</section>
```

三条硬坐标（改版式时先记这几个数）：

| 区域 | 位置 | 可用高度 |
|---|---|---|
| `.sh` 页眉 | `top: 30px`，`left/right: 46px` | 约 100px（kick 15px + 标题 40px） |
| `.sb` 内容区 | `top: 150px` ~ `bottom: 58px` | **512px（唯一需要记住的数字）** |
| `.foot` 页脚 | `bottom: 16px` | 13px 文本，不参与内容排版 |

`.sb` 是 `flex column` + `gap: 16px`，且 `.sb > *:not(.grow)` 已经 `flex-shrink: 0`：
**内容不会被静默压缩，超了就是溢出**，所以配合 `audit.js` 一定抓得到。
内容多到 512px 放不下时，只有两条路——精简文案或拆页，不要缩字号。

## 二、设计 token（`:root`）

```css
--paper #FAF6E9  --paper-2 #F4EDDA  --paper-3 #E9DFC4
--ink #22302A    --ink-2 #4B584F    --ink-3 #7E8478
--green #2F4A38  --green-2 #3F5B4A  --gold #A87F3F
--warn #A34A28   --ok #2C6E4F       --rule #DCD2B9

--fs-cover 76  --fs-sec 60  --fs-h1 40  --fs-lead 23  --fs-h2 27
--fs-card 23   --fs-body 21 --fs-th 18  --fs-td 20    --fs-code 18
--fs-note 16   --fs-kick 15 --fs-foot 13

--pad-x 46  --pad-t 30  --gap-l 22  --gap 16  --gap-s 10
```

字体：标题 `var(--serif)`（思源宋体/宋体族），正文 `var(--sans)`（苹方/微软雅黑），数字 `var(--num)`（Bahnschrift/DIN）。**不要引入网络字体**，教室机器可能断网。

## 三、栅格

```html
<div class="g2">…</div>   <!-- 1fr 1fr，gap 22 -->
<div class="g2u">…</div>  <!-- 1.15fr .85fr 主次 -->
<div class="g2v">…</div>  <!-- .85fr 1.15fr -->
<div class="g3">…</div>   <!-- 3 等分，gap 16 -->
<div class="g4">…</div>   <!-- 4 等分，gap 14，适合参数条 -->
<div class="row">…</div>  <!-- flex，align-items:center，gap 12 -->
<div class="col">…</div>  <!-- flex column，需自己给 gap -->
```

非等分优先用内联 `grid-template-columns`，例如 `style="display:grid;grid-template-columns:1fr 560px;gap:28px"`。
**相邻页不要连续用同一种栅格**，这是最容易被一眼看出“模板感”的地方。

## 四、卡片

```html
<div class="card flat">          <!-- --c 控制描边色，可 style="--c:var(--warn)" -->
  <div class="ct">卡片标题</div>
  <div class="cb">正文，21px。</div>
  <div class="cb sm">次要正文，19px。</div>
  <div class="cf">脚注，16px。</div>
</div>
```

- `.card` 默认 `padding: 18px 20px`，`flex column`；`.flat` 去掉阴影。
- 卡片**不要求等高**。内容少就让它矮，不要拉高留白。
- 同样的信息如果能排成表，就别做成 N 张卡片。

## 五、强调条 `.bar`

```html
<div class="bar">一条结论：只放最容易被忽略的那句话。</div>
<div class="bar sm" style="--c:var(--warn)">警告类结论走 --warn。</div>
```

`--c` 可选 `--green`（默认）/`--gold`/`--warn`/`--ok`。左侧 4px 竖条 + 7% 底色，
是这套版式最主要的“结论锚点”，**每页最多一条**，多了就不叫强调。

## 六、表格

```html
<table class="tbl rows tight">
  <thead><tr><th style="width:150px">项目</th><th style="width:220px">建议值</th><th>为什么是它</th></tr></thead>
  <tbody>
    <tr><td><b>画幅</b></td><td class="mono">16:9</td><td class="mut">开做之前定。</td></tr>
  </tbody>
</table>
```

- `rows` 给表头加底色；`tight` 行高 7px，`xs` 行高 3px（仅用于 7 行以上的密集参数表）。
- `td.mut` 弱化颜色，`td.dim` 更弱，`td.n` / `.mono` 走数字字体。
- `hi` + `tr.on` 可高亮当前行（讲分镜表时用）。
- 表格只用横线，不用竖线，不要斑马纹。

## 七、提示词框

```html
<div class="pbox" style="--c:var(--gold)">
  <div class="pl">发给模型 · 原样复制</div>
  <div class="pt">正文里的 <mark>新增约束</mark> 用 mark 高亮，<b>固定要点</b> 加粗。</div>
</div>
```

`.pt` 默认 20px / 1.85；内容多时用 `.pt.sm`（19px / 1.8），**不要低于 19px**。
`mark` 只标“这一版新加的那句”，全篇都标等于没标。

## 八、图片与视频

```html
<div class="frame" style="height:300px;background:#FFFDF6">
  <img src="assets/x.jpg" alt="说明" style="object-fit:contain">
  <div class="fl">镜 A 尾帧 · 4.0 秒</div>
</div>
<div class="figcap">图注：说明在看什么，不要重复标题。</div>
```

- **永远 `object-fit:contain` + 浅色底**。默认 `cover` 会裁掉主体，关键图不能裁；唯一例外是下方图片墙。
- 横图给宽度、竖图给高度：先量原图比例，再定容器高宽，避免两侧大片留白。

### 图片墙（多图排版）

一页并置 4 张以上同题材图片时用 `.wall` 加一个修饰类，**不要给每张图各包一张卡**。
立体感只靠四件事：暖白拼缝、沿轮廓的柔投影、边缘顶亮底暗、位置错落；不做发光与玻璃：

```html
<!-- A 齐边错落：四张照片卡，白边 + 投影 + 底部渐隐 + 上下错落 -->
<div class="wall w-stag">
  <div class="pc"><img src="assets/a1.jpg" alt=""></div>
  <div class="pc"><img src="assets/a2.jpg" alt=""></div>
  <div class="pc"><img src="assets/a3.jpg" alt=""></div>
  <div class="pc"><img src="assets/a4.jpg" alt=""></div>
</div>
<div class="wcap"><div class="wt">同一场景的四次取景</div><div class="figcap">图注：只承担并置比较。</div></div>

<!-- B 波浪贯通：墙宽必须等于内容区 1188px -->
<div class="wall w-wave">
  <img src="assets/b1.jpg" alt=""><img src="assets/b2.jpg" alt=""><img src="assets/b3.jpg" alt="">
  <img src="assets/b4.jpg" alt=""><img src="assets/b5.jpg" alt="">
</div>

<!-- C 斜切网格：左文右墙，外面再包一层 .w-scene 提供悬空投影带 -->
<div class="grow" style="display:grid;grid-template-columns:34% 1fr;gap:28px">
  <div class="col" style="justify-content:center;gap:10px">
    <div class="wt" style="margin:0">八张过程图沿斜线铺开</div>
    <div class="cb sm">左列只给结论，图墙承担细节与数量。</div>
  </div>
  <div class="w-scene">
    <div class="wall w-grid w-skew">
      <img src="assets/c1.jpg" alt=""><img src="assets/c2.jpg" alt=""><img src="assets/c3.jpg" alt=""><img src="assets/c4.jpg" alt="">
      <img src="assets/c5.jpg" alt=""><img src="assets/c6.jpg" alt=""><img src="assets/c7.jpg" alt=""><img src="assets/c8.jpg" alt="">
    </div>
  </div>
</div>

<!-- D 弧形底托：标题在墙上方，宽 1188px -->
<div class="wcap">
  <div class="wt" style="font-size:var(--fs-h1)">五张图托住一句结论</div>
  <div class="figcap">图注：弧裙裁掉的是边角，主体先挪到安全区。</div>
</div>
<div class="wall w-arc">
  <img src="assets/d1.jpg" alt=""><img src="assets/d2.jpg" alt=""><img src="assets/d3.jpg" alt="">
  <img src="assets/d4.jpg" alt=""><img src="assets/d5.jpg" alt="">
</div>
```

- **缝**：3px，容器底色 `#FFFDF6`；缝要读成白纸，不能是透明间隙。
- **投影**：裁剪类（B/C/D）一律 `drop-shadow`，`box-shadow` 会被 `clip-path` 裁掉；
  A 的照片卡反过来——阴影挂在 `.pc` 上，挂在 `img` 上会被底部渐隐一起淡掉。
- **明暗**：`::after` 压一层顶亮底暗（白 50% → 透明 14%、暗 34% → 透明 18%），补弯曲受光。
- **错落**：A 只改位置（`margin-top`），不旋转照片；B/D 的弧线不要用 `border-radius` 代替 `path`。
- `.wall` 已带 `min-height:0`；`.w-arc` / `.w-skew` 的 `overflow:hidden` 只裁图片，容器内不放文字。
- `cover` 只在「同题材并置、单张不承担唯一证据」时使用，主体落居中 60% 安全区；唯一证据图仍 `contain` + 浅色底。
- 四式的尺寸、坑与选型见 `page-patterns.md` 第 12 节。

## 九、流程与步骤

```html
<div class="flow">
  <div class="fstep"><div class="fn">01</div><div class="ft">第一步</div><div class="fa">说明</div><div class="fx">交出：某物</div></div>
  <div class="farrow">→</div>
  …
</div>
```

`.fx` 有 `margin-top:auto`，会贴到节点底部——**节点被拉高时用它兜底**，比留白好看。
横向流程 ≥5 步时改纵向 `.col`，或拆成两行，否则每格宽度不足 200px，文字必然挤。

## 十、其他高频件

| 类 | 用途 | 注意 |
|---|---|---|
| `.note` | 第三层补充说明，16px | 一页最多两条 |
| `.sub-h` | 卡片群上方的小节标题，20px | 与 `.ct` 不要同时用 |
| `.pillx` | 圆角小标签（`.g` 绿 / `.o` 金） | 只放关键词，别放句子 |
| `.kv` | 键值行，`justify-content:space-between` | 参数页比表格省地方 |
| `.code` | 代码块，18px 等宽 | 行高 ≥1.6，别超 14 行 |
| `.term` | 术语词典条目 | 4 列 × 4 行最密，再多拆页 |
| `.snum` | 圆形序号 | 与 `.fstep .fn` 二选一，别混用 |
| `.vrail` | 版本进度（V0→V4） | 放页眉右侧，`.cur`/`.done` 标状态 |
| `.film` / `.fr` | 帧条 | 一格一帧，`.cur` 标当前帧 |

## 十一、封面 / 章节 / 结语

三者的完整标记见 `assets/starter.html`，直接改文案即可：

- 封面 `.slide.cover`：`.cv-art`（右侧渐变或配图）+ `.cv-top` + `.cv-pill` + `.cv-t1` + `.cv-t2` + `.cv-hr` + `.cv-sub` + `.cv-feats`（固定 4 个 `.cv-feat`，多一个就换行）。
- 章节页（**深绿章板** `<section class="slide plate">`）：`.sec-rule` + `.sec-num`（超大编号）+ `.sec-body`（`.sec-en`/`.sec-h`/`.sec-lead`）+ `.sec-pts`（3 条）+ `.sec-foot` + `.sec-mark` + **`.sec-emblem`（徽记）**。
  `.plate` 会把标题、引导、要点、编号、页脚整套换成米白/金配色，不用逐页写内联色。
- 结语 `.slide.end`：深绿底，`.end-t` 大字结论 + `.end-l` 分隔线 + `.end-s` 收束段 + `.end-sign` 落款。

### 页码：四个挂点，一个格式

一律「当前页 / 总页」（`04 / 57`），按**物理页序**数，章节页也占号；`deck.js` 会按 DOM 顺序重新回填：

| 页面 | 类 | 位置 |
|---|---|---|
| 正文页 | `.foot .pn` | 页脚右侧，跟 `.foot` 同一行 |
| 章节页 | `.sec-pn` | `right:96px; bottom:30px`，与左侧 `.sec-foot` 同一基线 |
| 封面 | `.cv-pn` | `right:56px; top:664px`，米纸上的字要浅色 `rgba(247,240,222,.74)` |
| 结语 | `.end-pn` | `left:66px; bottom:46px`，深绿底上用 `#6E7D6A` |

### 章节页徽记 `.sec-emblem`

```html
<div class="sec-emblem">
  <div class="ring"><svg viewBox="0 0 120 120" …>…</svg></div>
  <div class="em-rule"></div>
  <div class="em-lb">STORYBOARD</div>
</div>
```

`.ring` 是 184px 圆环（内嵌 9px 虚线金圈），图标固定 96×96，`.em-lb` 是 12.5px 加宽字距的英文小标。
图标用 `stroke="currentColor"`，颜色跟着 `.sec-emblem { color }` 走（章板上自动变米白）。
图标库与选型见 `page-patterns.md` 第 2b 节。
