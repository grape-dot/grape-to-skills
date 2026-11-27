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
立体感只靠四件事：暖白拼缝、沿轮廓的柔投影、边缘顶亮底暗、尺寸或位置错落；不做发光与玻璃：

```html
<!-- 1 齐边错落式：四张照片卡，白边 + 投影 + 底部渐隐 + 上下错落 -->
<div class="wall w-stag">
  <div class="pc"><img src="assets/a1.jpg" alt=""></div>
  <div class="pc"><img src="assets/a2.jpg" alt=""></div>
  <div class="pc"><img src="assets/a3.jpg" alt=""></div>
  <div class="pc"><img src="assets/a4.jpg" alt=""></div>
</div>
<div class="wcap"><div class="wt">同一场景的四次取景</div><div class="figcap">图注：只承担并置比较。</div></div>

<!-- 2 波浪贯通式：四张，左右出血铺满；墙宽写死在 path 里，必须 1280px -->
<div class="wall w-wave">
  <img src="assets/b1.jpg" alt=""><img src="assets/b2.jpg" alt="">
  <img src="assets/b3.jpg" alt=""><img src="assets/b4.jpg" alt="">
</div>
<div class="wcap-l"><div class="wt">四张接成一条季节带</div><div class="figcap">图注：整条只起伏一次。</div></div>

<!-- 3 纵深渐进式：左文右墙，右缘出血贴边；rotateY 必须有 perspective -->
<div class="grow" style="display:grid;grid-template-columns:30% 1fr;gap:20px">
  <div class="col" style="justify-content:center;gap:12px">
    <div class="wt" style="margin:0">八张过程图沿纵深铺开</div>
    <div class="cb sm">左列只给结论，图墙承担细节与数量。</div>
  </div>
  <div class="w-depth-stage">
    <div class="w-depth">
      <img src="assets/c1.jpg" alt=""><img src="assets/c2.jpg" alt=""><img src="assets/c3.jpg" alt=""><img src="assets/c4.jpg" alt="">
      <img src="assets/c5.jpg" alt=""><img src="assets/c6.jpg" alt=""><img src="assets/c7.jpg" alt=""><img src="assets/c8.jpg" alt="">
    </div>
  </div>
</div>

<!-- 4 不对称叶片式：标题在上、图注在叶片下方的凹口里 -->
<div class="sb" style="justify-content:center">
  <div class="wcap"><div class="wt" style="font-size:var(--fs-h1); margin:0">五张图托住一句结论</div></div>
  <div class="wall w-fan">
    <img src="assets/d1.jpg" alt=""><img src="assets/d2.jpg" alt=""><img src="assets/d3.jpg" alt="">
    <img src="assets/d4.jpg" alt=""><img src="assets/d5.jpg" alt="">
  </div>
  <div class="figcap" style="margin:0; text-align:center">图注：左端最厚，中间最薄，右端回升但不超过左端。</div>
</div>

<!-- 5 螺旋长卷式（旧称盘旋丝带）：七块拼成一条绕行的带子，右列竖塔；每块 <image> 铺满自己的 bbox 独立取景
     viewBox 外扩 3px 是留给轮廓描边的，改成 0 0 380 430 会把最外圈描边裁掉 -->
<div class="grow" style="display:grid;grid-template-columns:1fr 430px;gap:44px;align-items:start">
  <div class="col" style="justify-content:flex-start;gap:16px">
    <p class="lead">图墙不是把图贴上去，是<b>给一组并置的图像一条共同的走向</b>。</p>
    <div class="wt" style="font-size:var(--fs-h1);margin:0">自上而下，绕出三段风景</div>
    <div class="cb">每块只放一张图，块与块之间留纸白缝，整条读成一个动作。</div>
    <div class="cb sm">横带承担起势与转折，竖带承担停留；末端两块并排，收住全篇。</div>
    <div class="figcap" style="margin:0">图注：七块同题材取景沿丝带盘绕，逐段投影（SVG 滤镜）、交替受光读出层叠。</div>
  </div>
  <svg class="w-coil" viewBox="-3 -3 386 423.4" preserveAspectRatio="none" role="img" aria-label="七段取景沿一条盘绕的丝带自上而下铺开">
    <defs>
      <clipPath id="coil1"><path d="M0.0 0.0 Q14.9 5.9 22.4 8.1 Q29.8 10.4 37.3 12.0 Q44.7 13.7 52.2 15.2 Q59.6 16.7 67.1 18.3 Q74.5 19.9 82.0 21.0 Q89.5 22.2 96.9 23.7 Q104.4 25.3 111.8 26.3 Q119.3 27.3 126.7 28.8 Q134.2 30.3 141.6 31.6 Q149.1 33.0 156.5 34.8 Q164.0 36.6 171.4 38.6 Q178.9 40.7 180.9 41.3 L183.0 42.0 L183.0 47.4 183.0 47.4 Q178.9 48.8 171.4 50.9 Q164.0 53.0 156.5 54.5 Q149.1 56.0 141.6 57.6 Q134.2 59.2 126.7 60.8 Q119.3 62.5 111.8 64.4 Q104.4 66.4 96.9 66.4 Q89.5 66.4 82.0 66.4 Q74.5 66.4 67.1 66.4 Q59.6 66.4 52.2 66.4 Q44.7 66.4 37.3 66.4 Q29.8 66.4 22.4 66.4 Q14.9 66.4 7.5 65.7 L0.0 65.1 Z"/></clipPath>
      <clipPath id="coil2"><path d="M115.2 71.8 Q130.1 66.9 137.6 65.2 Q145.0 63.6 152.5 62.0 Q159.9 60.5 167.4 59.0 Q174.8 57.4 182.3 55.1 Q189.7 52.9 191.8 52.2 L193.8 51.5 L193.8 96.2 193.8 96.2 Q189.7 95.0 182.3 93.7 Q174.8 92.3 167.4 90.9 Q159.9 89.5 152.5 88.0 Q145.0 86.6 137.6 85.1 Q130.1 83.6 122.7 81.1 L115.2 78.6 Z"/></clipPath>
      <clipPath id="coil3"><path d="M109.8 86.7 Q124.7 89.5 132.1 90.9 Q139.6 92.3 147.1 93.8 Q154.5 95.3 162.0 96.7 Q169.4 98.0 176.9 99.8 Q184.3 101.5 191.8 103.0 Q199.2 104.5 206.7 106.5 Q214.1 108.4 221.6 111.0 Q229.0 113.5 234.5 117.1 L239.9 120.6 L239.9 130.1 239.9 130.1 Q229.0 138.7 221.6 142.7 Q214.1 146.7 206.7 150.1 Q199.2 153.5 191.8 156.5 Q184.3 159.6 176.9 162.6 Q169.4 165.7 162.0 168.5 Q154.5 171.2 147.1 174.2 Q139.6 177.2 132.1 180.1 Q124.7 183.0 117.2 185.0 L109.8 187.0 Z"/></clipPath>
      <clipPath id="coil4"><path d="M8.1 246.7 Q23.0 234.8 30.5 230.8 Q37.9 226.8 45.4 223.4 Q52.9 219.9 60.3 216.6 Q67.8 213.2 75.2 210.1 Q82.7 207.0 90.1 204.0 Q97.6 201.1 105.0 198.3 Q112.5 195.5 119.9 192.5 Q127.4 189.4 134.9 186.6 Q142.3 183.9 149.8 180.9 Q157.2 178.0 164.7 175.1 Q172.1 172.1 179.6 169.0 Q187.0 165.8 194.5 162.7 Q201.9 159.6 209.4 156.2 Q216.8 152.8 224.3 148.5 Q231.8 144.1 236.5 140.5 L241.2 136.9 L241.2 275.1 241.2 275.1 Q231.8 275.1 224.3 274.4 Q216.8 273.8 209.4 273.8 Q201.9 273.8 194.5 273.1 Q187.0 272.4 179.6 272.4 Q172.1 272.4 164.7 271.8 Q157.2 271.1 149.8 271.1 Q142.3 271.1 134.9 270.6 Q127.4 270.2 119.9 269.9 Q112.5 269.7 105.0 269.0 Q97.6 268.4 90.1 268.1 Q82.7 267.9 75.2 267.4 Q67.8 267.0 60.3 266.2 Q52.9 265.5 45.4 264.3 Q37.9 263.1 30.5 261.6 Q23.0 260.2 15.6 257.5 L8.1 254.8 Z"/></clipPath>
      <clipPath id="coil5"><path d="M6.8 261.6 Q21.7 267.0 29.1 268.3 Q36.6 269.7 44.0 270.4 Q51.5 271.1 59.0 271.8 Q66.4 272.6 73.9 273.2 Q81.3 273.8 88.8 274.5 Q96.2 275.1 103.7 275.4 Q111.1 275.6 118.6 276.0 Q126.0 276.5 133.5 276.7 Q141.0 276.9 148.4 277.4 Q155.9 277.8 160.6 278.5 L165.3 279.2 L165.3 416.1 165.3 416.1 Q155.9 417.4 148.4 417.4 Q141.0 417.4 133.5 417.4 Q126.0 417.4 118.6 417.4 Q111.1 417.4 103.7 417.4 Q96.2 417.4 88.8 417.4 Q81.3 417.4 73.9 417.4 Q66.4 417.4 59.0 417.4 Q51.5 417.4 44.0 417.4 Q36.6 417.4 29.1 417.4 Q21.7 417.4 14.2 416.8 L6.8 416.1 Z"/></clipPath>
      <clipPath id="coil6"><path d="M173.5 277.8 Q188.4 279.2 195.8 279.2 Q203.3 279.2 210.8 279.4 Q218.2 279.7 225.7 280.1 Q233.1 280.5 240.6 281.0 Q248.0 281.4 255.5 281.7 Q262.9 281.9 270.4 282.6 Q277.8 283.3 285.3 283.9 Q292.7 284.6 300.2 285.3 Q307.7 286.0 315.1 287.1 Q322.6 288.2 330.0 289.6 Q337.5 290.9 344.9 293.4 Q352.4 295.8 357.1 299.7 L361.9 303.6 L361.9 314.4 361.9 314.4 Q352.4 327.5 344.9 334.5 Q337.5 341.5 330.0 347.6 Q322.6 353.6 315.1 359.1 Q307.7 364.6 300.2 369.9 Q292.7 375.3 285.3 380.9 Q277.8 386.4 270.4 392.4 Q262.9 398.5 255.5 407.1 Q248.0 415.7 240.6 416.6 Q233.1 417.4 225.7 417.4 Q218.2 417.4 210.8 417.4 Q203.3 417.4 195.8 417.4 Q188.4 417.4 180.9 416.8 L173.5 416.1 Z"/></clipPath>
      <clipPath id="coil7"><path d="M258.9 413.4 Q273.8 398.5 281.2 392.4 Q288.7 386.4 296.1 380.9 Q303.6 375.4 311.0 369.9 Q318.5 364.5 326.0 358.9 Q333.4 353.3 340.9 347.4 Q348.3 341.5 355.8 333.8 Q363.2 326.2 365.9 323.0 L368.6 319.9 L368.6 420.1 368.6 420.1 Q363.2 420.1 355.8 420.1 Q348.3 420.1 340.9 420.1 Q333.4 420.1 326.0 420.1 Q318.5 420.1 311.0 420.1 Q303.6 420.1 296.1 420.1 Q288.7 420.1 281.2 420.1 Q273.8 420.1 266.3 420.1 L258.9 420.1 Z"/></clipPath>
      <filter id="coilShadow" x="-40%" y="-40%" width="180%" height="180%">
        <feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#4A3A22" flood-opacity=".30"/>
        <feDropShadow dx="0" dy="1.2" stdDeviation="1" flood-color="#4A3A22" flood-opacity=".16"/>
      </filter>
      <linearGradient id="coilLiteA" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#FFFDF6" stop-opacity=".28"/><stop offset=".45" stop-color="#FFFDF6" stop-opacity="0"/><stop offset="1" stop-color="#4A3A22" stop-opacity=".26"/>
      </linearGradient>
      <linearGradient id="coilLiteB" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#4A3A22" stop-opacity=".20"/><stop offset=".5" stop-color="#4A3A22" stop-opacity="0"/><stop offset="1" stop-color="#FFFDF6" stop-opacity=".16"/>
      </linearGradient>
    </defs>
    <g clip-path="url(#coil1)" class="seg" filter="url(#coilShadow)"><image href="assets/e1.jpg" x="0.0" y="0.0" width="191.0" height="74.4" preserveAspectRatio="xMidYMid slice"/></g>
    <g clip-path="url(#coil2)" class="seg" filter="url(#coilShadow)"><image href="assets/e1.jpg" x="115.2" y="51.5" width="86.6" height="52.7" preserveAspectRatio="xMidYMid slice"/></g>
    <g clip-path="url(#coil3)" class="seg" filter="url(#coilShadow)"><image href="assets/e2.jpg" x="109.8" y="85.4" width="138.1" height="111.0" preserveAspectRatio="xMidYMid slice"/></g>
    <g clip-path="url(#coil4)" class="seg" filter="url(#coilShadow)"><image href="assets/e3.jpg" x="8.1" y="136.9" width="241.1" height="146.2" preserveAspectRatio="xMidYMid slice"/></g>
    <g clip-path="url(#coil5)" class="seg" filter="url(#coilShadow)"><image href="assets/e4.jpg" x="6.8" y="261.6" width="166.6" height="163.9" preserveAspectRatio="xMidYMid slice"/></g>
    <g clip-path="url(#coil6)" class="seg" filter="url(#coilShadow)"><image href="assets/e5.jpg" x="173.5" y="277.8" width="196.4" height="147.6" preserveAspectRatio="xMidYMid slice"/></g>
    <g clip-path="url(#coil7)" class="seg" filter="url(#coilShadow)"><image href="assets/e5.jpg" x="258.9" y="319.9" width="117.8" height="108.3" preserveAspectRatio="xMidYMid slice"/></g>
    <g fill="none" stroke="#FFFDF6" stroke-width="2.2" stroke-linejoin="round">
      <path d="M0.0 0.0 Q14.9 5.9 22.4 8.1 Q29.8 10.4 37.3 12.0 Q44.7 13.7 52.2 15.2 Q59.6 16.7 67.1 18.3 Q74.5 19.9 82.0 21.0 Q89.5 22.2 96.9 23.7 Q104.4 25.3 111.8 26.3 Q119.3 27.3 126.7 28.8 Q134.2 30.3 141.6 31.6 Q149.1 33.0 156.5 34.8 Q164.0 36.6 171.4 38.6 Q178.9 40.7 180.9 41.3 L183.0 42.0 L183.0 47.4 183.0 47.4 Q178.9 48.8 171.4 50.9 Q164.0 53.0 156.5 54.5 Q149.1 56.0 141.6 57.6 Q134.2 59.2 126.7 60.8 Q119.3 62.5 111.8 64.4 Q104.4 66.4 96.9 66.4 Q89.5 66.4 82.0 66.4 Q74.5 66.4 67.1 66.4 Q59.6 66.4 52.2 66.4 Q44.7 66.4 37.3 66.4 Q29.8 66.4 22.4 66.4 Q14.9 66.4 7.5 65.7 L0.0 65.1 Z"/>
      <path d="M115.2 71.8 Q130.1 66.9 137.6 65.2 Q145.0 63.6 152.5 62.0 Q159.9 60.5 167.4 59.0 Q174.8 57.4 182.3 55.1 Q189.7 52.9 191.8 52.2 L193.8 51.5 L193.8 96.2 193.8 96.2 Q189.7 95.0 182.3 93.7 Q174.8 92.3 167.4 90.9 Q159.9 89.5 152.5 88.0 Q145.0 86.6 137.6 85.1 Q130.1 83.6 122.7 81.1 L115.2 78.6 Z"/>
      <path d="M109.8 86.7 Q124.7 89.5 132.1 90.9 Q139.6 92.3 147.1 93.8 Q154.5 95.3 162.0 96.7 Q169.4 98.0 176.9 99.8 Q184.3 101.5 191.8 103.0 Q199.2 104.5 206.7 106.5 Q214.1 108.4 221.6 111.0 Q229.0 113.5 234.5 117.1 L239.9 120.6 L239.9 130.1 239.9 130.1 Q229.0 138.7 221.6 142.7 Q214.1 146.7 206.7 150.1 Q199.2 153.5 191.8 156.5 Q184.3 159.6 176.9 162.6 Q169.4 165.7 162.0 168.5 Q154.5 171.2 147.1 174.2 Q139.6 177.2 132.1 180.1 Q124.7 183.0 117.2 185.0 L109.8 187.0 Z"/>
      <path d="M8.1 246.7 Q23.0 234.8 30.5 230.8 Q37.9 226.8 45.4 223.4 Q52.9 219.9 60.3 216.6 Q67.8 213.2 75.2 210.1 Q82.7 207.0 90.1 204.0 Q97.6 201.1 105.0 198.3 Q112.5 195.5 119.9 192.5 Q127.4 189.4 134.9 186.6 Q142.3 183.9 149.8 180.9 Q157.2 178.0 164.7 175.1 Q172.1 172.1 179.6 169.0 Q187.0 165.8 194.5 162.7 Q201.9 159.6 209.4 156.2 Q216.8 152.8 224.3 148.5 Q231.8 144.1 236.5 140.5 L241.2 136.9 L241.2 275.1 241.2 275.1 Q231.8 275.1 224.3 274.4 Q216.8 273.8 209.4 273.8 Q201.9 273.8 194.5 273.1 Q187.0 272.4 179.6 272.4 Q172.1 272.4 164.7 271.8 Q157.2 271.1 149.8 271.1 Q142.3 271.1 134.9 270.6 Q127.4 270.2 119.9 269.9 Q112.5 269.7 105.0 269.0 Q97.6 268.4 90.1 268.1 Q82.7 267.9 75.2 267.4 Q67.8 267.0 60.3 266.2 Q52.9 265.5 45.4 264.3 Q37.9 263.1 30.5 261.6 Q23.0 260.2 15.6 257.5 L8.1 254.8 Z"/>
      <path d="M6.8 261.6 Q21.7 267.0 29.1 268.3 Q36.6 269.7 44.0 270.4 Q51.5 271.1 59.0 271.8 Q66.4 272.6 73.9 273.2 Q81.3 273.8 88.8 274.5 Q96.2 275.1 103.7 275.4 Q111.1 275.6 118.6 276.0 Q126.0 276.5 133.5 276.7 Q141.0 276.9 148.4 277.4 Q155.9 277.8 160.6 278.5 L165.3 279.2 L165.3 416.1 165.3 416.1 Q155.9 417.4 148.4 417.4 Q141.0 417.4 133.5 417.4 Q126.0 417.4 118.6 417.4 Q111.1 417.4 103.7 417.4 Q96.2 417.4 88.8 417.4 Q81.3 417.4 73.9 417.4 Q66.4 417.4 59.0 417.4 Q51.5 417.4 44.0 417.4 Q36.6 417.4 29.1 417.4 Q21.7 417.4 14.2 416.8 L6.8 416.1 Z"/>
      <path d="M173.5 277.8 Q188.4 279.2 195.8 279.2 Q203.3 279.2 210.8 279.4 Q218.2 279.7 225.7 280.1 Q233.1 280.5 240.6 281.0 Q248.0 281.4 255.5 281.7 Q262.9 281.9 270.4 282.6 Q277.8 283.3 285.3 283.9 Q292.7 284.6 300.2 285.3 Q307.7 286.0 315.1 287.1 Q322.6 288.2 330.0 289.6 Q337.5 290.9 344.9 293.4 Q352.4 295.8 357.1 299.7 L361.9 303.6 L361.9 314.4 361.9 314.4 Q352.4 327.5 344.9 334.5 Q337.5 341.5 330.0 347.6 Q322.6 353.6 315.1 359.1 Q307.7 364.6 300.2 369.9 Q292.7 375.3 285.3 380.9 Q277.8 386.4 270.4 392.4 Q262.9 398.5 255.5 407.1 Q248.0 415.7 240.6 416.6 Q233.1 417.4 225.7 417.4 Q218.2 417.4 210.8 417.4 Q203.3 417.4 195.8 417.4 Q188.4 417.4 180.9 416.8 L173.5 416.1 Z"/>
      <path d="M258.9 413.4 Q273.8 398.5 281.2 392.4 Q288.7 386.4 296.1 380.9 Q303.6 375.4 311.0 369.9 Q318.5 364.5 326.0 358.9 Q333.4 353.3 340.9 347.4 Q348.3 341.5 355.8 333.8 Q363.2 326.2 365.9 323.0 L368.6 319.9 L368.6 420.1 368.6 420.1 Q363.2 420.1 355.8 420.1 Q348.3 420.1 340.9 420.1 Q333.4 420.1 326.0 420.1 Q318.5 420.1 311.0 420.1 Q303.6 420.1 296.1 420.1 Q288.7 420.1 281.2 420.1 Q273.8 420.1 266.3 420.1 L258.9 420.1 Z"/>
    </g>
    <g class="lit">
      <g clip-path="url(#coil1)"><rect x="-3" y="-3" width="386" height="426.4" fill="url(#coilLiteA)"/></g>
      <g clip-path="url(#coil2)"><rect x="-3" y="-3" width="386" height="426.4" fill="url(#coilLiteB)"/></g>
      <g clip-path="url(#coil3)"><rect x="-3" y="-3" width="386" height="426.4" fill="url(#coilLiteA)"/></g>
      <g clip-path="url(#coil4)"><rect x="-3" y="-3" width="386" height="426.4" fill="url(#coilLiteB)"/></g>
      <g clip-path="url(#coil5)"><rect x="-3" y="-3" width="386" height="426.4" fill="url(#coilLiteA)"/></g>
      <g clip-path="url(#coil6)"><rect x="-3" y="-3" width="386" height="426.4" fill="url(#coilLiteB)"/></g>
      <g clip-path="url(#coil7)"><rect x="-3" y="-3" width="386" height="426.4" fill="url(#coilLiteA)"/></g>
    </g>
  </svg>
</div>
```

<!-- E2 整页通栏：path 与上面完全一样，改四处 —— class 加 cv-coil、stroke 2.2 → 6、
     svg 加 preserveAspectRatio="none"（viewBox 已收到内容底 420.1+3=423.4）、
     CSS 由 .cv-coil 定 height:720 拉满，塔底与页底出血衔接。
     文字不另设类：.sh（kick 15px + stitle 40px）+ .sb（宽限到 520px）+ .lead + .figcap + .foot，
     与其他十式同一套规格；样式只剩 .cv-coil，在 theme.css「5 式整页通栏盘绕塔」段。 -->
<section class="slide">
  <div class="sh">
    <div class="kick">图片墙 · 第 5 式</div>
    <h1 class="stitle">螺旋长卷式</h1>
  </div>
  <div class="sb" style="width:520px;right:auto">
    <p class="lead">图片<b>沿 S 形曲线连续展开</b>，形成叙事性长卷。</p>
    <div class="figcap">图注：七段共用一条带子盘绕一圈半，起点在顶部横带、终点两块并排落地；逐段投影、交替受光读出扭转。</div>
  </div>
  <!-- 这里放同一个 <svg>，class="w-coil cv-coil" preserveAspectRatio="none"，stroke-width="6" -->
  <div class="foot"><span>图片墙 · 第 5 式　螺旋长卷式</span><span>05 / 11</span></div>
</section>
```

```html
<!-- 6 半圆扇面式：四片从同一圆心拉出的三角形，外弧/内弧由舞台一条 path 统一裁出；
     贴条必须挂 .sec-wrap（写进 .w-sec 会被整块裁掉）；换张数/张角用 scripts/fan-wall.py 重算 -->
<div class="sec-wrap">
  <div class="wall w-sec">
    <div class="sd"><img src="assets/f1.jpg" alt=""></div>
    <div class="sd"><img src="assets/f2.jpg" alt=""></div>
    <div class="sd"><img src="assets/f3.jpg" alt=""></div>
    <div class="sd"><img src="assets/f4.jpg" alt=""></div>
  </div>
  <div class="sec-cap">
    <div class="sec-t">四帧一把扇</div>
    <div class="sec-s">同题四帧 · 放射接缝</div>
  </div>
</div>

<!-- 7 弧形切幅式：只弯上缘、下缘齐平贴底；文字块 .crest-head 挂墙外，进墙就被 clip-path 裁掉 -->
<div class="crest-wrap">
  <div class="wall w-crest">
    <img src="assets/g1.jpg" alt=""><img src="assets/g2.jpg" alt="">
    <img src="assets/g3.jpg" alt=""><img src="assets/g4.jpg" alt="">
  </div>
</div>

<!-- 8 矩阵网格式：5×3 十五格卷成圆柱面；每列 .cc 是棱柱面的一片（列内三格纵排），
     transform: translateZ(-R) rotateY(φ) translateZ(R)，φ=−36/−18/0/18/36、R=678=列宽212÷2sin9°；
     五列 absolute 叠在容器中点（flex 排开会与圆柱位移叠加散开）；容器禁 filter（压平 3D），投影走 ::before -->
<div class="wall w-cyl">
  <div class="cc"><img src="assets/h1.jpg" alt=""><img src="assets/h2.jpg" alt=""><img src="assets/h3.jpg" alt=""></div>
  <div class="cc"><img src="assets/h4.jpg" alt=""><img src="assets/h1.jpg" alt=""><img src="assets/h2.jpg" alt=""></div>
  <div class="cc"><img src="assets/h3.jpg" alt=""><img src="assets/h4.jpg" alt=""><img src="assets/h1.jpg" alt=""></div>
  <div class="cc"><img src="assets/h2.jpg" alt=""><img src="assets/h3.jpg" alt=""><img src="assets/h4.jpg" alt=""></div>
  <div class="cc"><img src="assets/h1.jpg" alt=""><img src="assets/h2.jpg" alt=""><img src="assets/h3.jpg" alt=""></div>
</div>

<!-- 9 折页长卷式：四片等宽共边梯形 .lf，竖边高矮交替成之字（两端与中缝高）；gap:0，折缝=左高光+右暗边 -->
<div class="wall w-fold">
  <div class="lf"><img src="assets/i1.jpg" alt=""></div>
  <div class="lf"><img src="assets/i2.jpg" alt=""></div>
  <div class="lf"><img src="assets/i3.jpg" alt=""></div>
  <div class="lf"><img src="assets/i4.jpg" alt=""></div>
</div>

<!-- 10/11 弧幕连屏式：共边梯形，.ai 必须包住 img；缝靠每片左右各裁 3px，不能用 gap；
     内弧加 .sag（中段鼓、两端收），五张加 .n5 -->
<div class="wall w-arc">
  <div class="ai"><img src="assets/j1.jpg" alt=""></div>
  <div class="ai"><img src="assets/j2.jpg" alt=""></div>
  <div class="ai"><img src="assets/j3.jpg" alt=""></div>
  <div class="ai"><img src="assets/j4.jpg" alt=""></div>
</div>

<!-- 12 峰谷天际线式：九扇底边对齐（奇数扇），高度表 .w-sky nth-child 左右镜像（端塔 300 →
     158 → 178 → 198 → 主塔满高 380）；.pk 压暗做全页唯一深色锚点，内容优先选暗调图 -->
<div class="wall w-sky">
  <div class="pc"><img src="assets/k1.jpg" alt=""></div>
  <div class="pc"><img src="assets/k2.jpg" alt=""></div>
  <div class="pc"><img src="assets/k3.jpg" alt=""></div>
  <div class="pc"><img src="assets/k4.jpg" alt=""></div>
  <div class="pc pk"><img src="assets/k5.jpg" alt=""></div>
  <div class="pc"><img src="assets/k4.jpg" alt=""></div>
  <div class="pc"><img src="assets/k3.jpg" alt=""></div>
  <div class="pc"><img src="assets/k2.jpg" alt=""></div>
  <div class="pc"><img src="assets/k1.jpg" alt=""></div>
</div>

<!-- 13 四季弧线式：整页通栏贴边（.w-tarc 负边距出血），整面一条贝塞尔 path——
     裁切挂内层 .cin（1280×420 坐标写死：顶弧左沉 159 → 弧顶偏右 ≈45 → 右端 52；
     底弧右满 420 → 中抬 ≈291 → 左 340），四栏被裁成左薄右厚（远小近大）；
     金弧线 + 四节点叠在外层 svg.axis（viewBox 1280×420，放 .cin 内会被裁） -->
<div class="wall w-tarc">
  <div class="cin">
    <div class="cl"><img src="assets/l1.jpg" alt=""></div>
    <div class="cl"><img src="assets/l2.jpg" alt=""></div>
    <div class="cl"><img src="assets/l3.jpg" alt=""></div>
    <div class="cl"><img src="assets/l4.jpg" alt=""></div>
  </div>
  <svg class="axis" viewBox="0 0 1280 420" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0 159 C522 74 892 23 1280 52" fill="none" stroke="#A87F3F" stroke-width="2.5"/>
    <circle cx="157" cy="134" r="6.5" fill="#A87F3F" stroke="#FFFDF6" stroke-width="2"/>
    <circle cx="480" cy="87" r="6.5" fill="#A87F3F" stroke="#FFFDF6" stroke-width="2"/>
    <circle cx="800" cy="54" r="6.5" fill="#A87F3F" stroke="#FFFDF6" stroke-width="2"/>
    <circle cx="1123" cy="45" r="6.5" fill="#A87F3F" stroke="#FFFDF6" stroke-width="2"/>
  </svg>
</div>

<!-- 14 弧形内凹式：三向出血——.w-conc 在 .sb 内绝对定位（left/right 负边距贴纸边、
     bottom:-58px 铺到页底，不设页脚条）；裁切挂内层 .cin（1280×470 写死：
     上缘内凹弧端 40 → 中 145，下缘平直），投影挂外层 drop-shadow 向上打（clip 裁自身影子） -->
<div class="wall w-conc">
  <div class="cin">
    <div class="cl"><img src="assets/m1.jpg" alt=""></div>
    <div class="cl"><img src="assets/m2.jpg" alt=""></div>
    <div class="cl"><img src="assets/m3.jpg" alt=""></div>
  </div>
</div>

<!-- 15 斜切折页式：六扇竖幅顶边对齐，底边两段斜切向中央折脊（.spine）收拢；
     投影挂 .lf 的 drop-shadow（clip 裁自身影子），图注坐中脊下方的 .funnel 漏斗里 -->
<div class="wall w-tilt">
  <div class="lf"><img src="assets/n1.jpg" alt=""></div>
  <div class="lf"><img src="assets/n2.jpg" alt=""></div>
  <div class="lf"><img src="assets/n3.jpg" alt=""></div>
  <div class="spine"></div>
  <div class="lf"><img src="assets/n4.jpg" alt=""></div>
  <div class="lf"><img src="assets/n5.jpg" alt=""></div>
  <div class="lf"><img src="assets/n6.jpg" alt=""></div>
  <div class="funnel"><p class="fcap">图注……</p></div>
</div>
```

- **缝**：3px，2 / 3 用容器底色 `#FFFDF6`，缝读成白纸；A/D 不留底色，缝露纸底即可。
- **投影**：裁剪类（B）一律 `drop-shadow`，`box-shadow` 会被 `clip-path` 裁掉；
  1 的阴影挂 `.pc`（挂 `img` 会被底部渐隐一起淡掉）；4 的投影挂**容器**，
  沿图片实际轮廓走，逐张加就变成五张独立卡片。
- **明暗**：B/C 的 `::after` 压一层顶亮底暗（白 50% → 透明 14%、暗 34% → 透明 18%）。
- **出血**：2 / 4 用 `width: calc(100% + 92px); margin-left: calc(var(--pad-x) * -1)` 左右铺满；
  3 用 `right: calc(var(--pad-x) * -1)` 只让右缘贴边。
- **连续轮廓**：2 / 4 的上下缘都由容器一条 `clip-path:path()` 裁出，图片一律同一高度；
  逐张改高度会留台阶（4 以前就是这么错的）。4 的左端下缘画到了 406（容器 400 之外），
  所以 4 的图片取 `height: calc(100% + 20px); align-self: flex-start`，`::after` 补 `bottom:-20px`。
- **纵深**：3 是 `perspective(1600px) rotateY(-25deg)`，宽 1100、高 420、`transform-origin:100% 50%`。
  改角度要同步降高度，否则右缘放大后会压页脚。
- `.wall` 已带 `min-height:0`；`.w-depth` 绝对定位，容器 `.w-depth-stage` 必须留出高度。
- `cover` 只在「同题材并置、单张不承担唯一证据」时使用，主体落居中 60% 安全区；唯一证据图仍 `contain` + 浅色底。
- 十五式的尺寸、坑与选型见 `page-patterns.md` 第 12 节；要换 GSAP 编排或加 WebGL 特效，
  按同节末「技术选型与增强层」引入 `assets/fx.js`，用 `data-fx` + `RP.fx.register` 挂载。

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
