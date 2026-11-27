# rice-paper-ppt

**米纸质感 HTML 幻灯片** — 一套「暖米纸 + 深林绿 + 哑光金」的中文演示文稿规范（Skill），
视觉层固化纸感配色、衬线大标题、投影级字号与逐页版式验收，
文案层固化标题、句式、术语与标点规范，让 Agent 直接产出可讲、可投影、可离线分发、
语言严谨的 HTML 幻灯片。

**它是一套规范，不是一个用途。** 汇报、路演、方案宣讲、复盘、培训、分享会、
文化展陈、课程——凡是需要在屏幕上讲、且希望它看起来像一本装帧考究的册子，都适用。

A warm rice-paper HTML slide style — 16:9, 1280×720, forest green and matte gold with
serif display type, projection-scaled typography, a writing-style spec, and a Playwright layout audit.

<p align="center">
  <img src="examples/preview.jpg" width="820" alt="六页骨架：封面 / 章节 / 图文 / 表格 / 流程 / 结语" />
</p>

上排：封面 · 章节分隔 · 图文案例　下排：表格对比 · 横向流程 · 结语

## 特性 / Features

- **风格统一、用途不限**：一套 token 管住全篇气质；换主题只需改 `--paper` / `--green` / `--gold` 三个值。
- **投影级字号**：正文 21px 起（`--fs-body`），表格 18/20px，代码 18px，页脚 13px。
  不用「缩小字体塞内容」换空间，放不下就改结构。
- **一支文件即成品**：`index.html` + `theme.css` + `deck.js` + `assets/`，双击就能讲，
  不依赖网络、不依赖构建、不需要 Office。
- **六页可运行骨架**：封面 / 章节 / 图文 / 表格 / 流程 / 结语，改文案即成片，不从空白页写起。
- **十二种版式配方**：按「页面作用」选版面，相邻页强制换版式，避免通篇卡片网格。
- **多图排版四式**：一组同题材图并置时，先定几何母题再抬起整组——矩形错落讲并列（4–5 张照片卡）、
  波浪贯通讲连续（4 张通栏大 S，只起伏一次）、纵深梯形讲层进（8 张沿垂直轴旋转，右缘贴边、
  近大远小）、不对称扇形讲收束（5 张高度渐变，左高、中小、右回）。墙内等宽白缝、不给每张图单独
  配卡片；立体感来自暖白拼缝、沿轮廓的柔和投影、边缘顶亮底暗与尺寸错落，不用发光和玻璃。
  近大远小必须 `perspective` + `rotateY`，`skewX` 只有斜切没有纵深。`theme.css` 已内置四式、
  标题带与 0.7s 入场动画，参数换算与坑见 `references/page-patterns.md` 第 12 节。
- **可选增强层**：HTML 是载体，不是能力上限。`assets/fx.js` 只在检测到 GSAP 时才接管编排
  （图墙浮起 / 扇形逐张 / 纵深转正），没有 GSAP 就自动退回纯 CSS，不多一个依赖；
  需要真实顶点位移或网格 warp 时，用 `data-fx` + `RP.fx.register` 挂 WebGL / Canvas，
  返回清理函数即可在离页时销毁上下文。约束的是交付物——静态可回退、依赖本地化、
  打印与截图回到终态——不是技术选型。
- **页码「当前 / 总页」**：正文、章节页、封面、结语四处统一格式，`deck.js` 按 DOM 顺序自动回填，不会逐段漂号。
- **章节首页是深绿章板**：底色一重，翻章立刻能感觉到；板上放大编号 + 本章徽记（印章圆环 + 单色线稿），
  图案就是这一章要讲的东西。七个现成图标可复制，品牌工具（Remotion 等）可放官方图标改单色。
  开工前会先问一次：默认由 AI 设计，还是你出创意。
- **文案语言规范**：`references/copywriting-spec.md` 约束标题命名、句式、正文结构、术语口径与标点，
  禁用机械化对比句式、口语化引导语与空泛营销表达。
- **信息结构规范**：`references/content-structure-spec.md` 约束专业术语提炼、信息层级重构、内容压缩、
  章节封面定位与信息可视化，禁用「两条链 / 几个步骤」等模糊代称；成稿后语言审查（第 08 节）与
  结构审查（A–H）双轨执行，骨架示例文案已按两份规范改写。
- **可验证的验收**：`scripts/audit.js` 用 Playwright 逐页真实渲染，检出内容溢出、越界、
  静默裁切、容器内溢、过小字号五类问题，返回退出码可当 CI 闸门。
- **样式单点控制**：所有字号 / 间距都是 `:root` 里的 CSS 变量，整体放大缩小改一处即可。
- **完整交互**：方向键 / Home / End / 数字键翻页、`f` 全屏、`p` 打印、`#N` 深链、
  窗口自适应等比缩放、视频播放与声音开关，视频自带暂停按钮与可拖拽进度条（`.vctl` 自动挂载）。

## 目录结构 / Structure

```text
rice-paper-ppt/
├── SKILL.md                       # AI Skill 主文件（工作流、硬约束、版式选择表）
├── README.md                      # 本文件
├── LICENSE                        # MIT
├── manifest.json                  # 版本 / 归属 / 成熟度 / 产出契约
├── agents/
│   └── interface.yaml             # 跨平台接口声明（默认 prompt、激活与降级策略）
├── assets/
│   ├── theme.css                  # 版式系统：设计 token + 全部组件（715 行）
│   ├── deck.js                    # 缩放 / 翻页 / 全屏 / 打印 / 页码回填 / 视频控件（172 行）
│   ├── starter.html               # 6 页可运行骨架（文案已按规范改写）
│   ├── fx.js                      # 可选增强层：GSAP 编排 + WebGL/Canvas 注册接口
│   └── example.jpg                # 占位图
├── references/
│   ├── typography-spec.md         # 视觉层：排版与字号规范原文（11 节，验收标准）
│   ├── copywriting-spec.md        # 文案层·语言：标题 / 句式 / 术语口径 / 标点（8 节，验收标准）
│   ├── content-structure-spec.md # 文案层·结构：术语提炼 / 压缩 / 章节封面 / 可视化（12 节，验收标准）
│   ├── components.md              # 类名词典 + 可复制组件片段 + 硬坐标
│   └── page-patterns.md           # 12 种版式配方 + 空旷 / 拥挤症状表
├── scripts/
│   ├── audit.js                   # 逐页版式审计（Node + Playwright）
│   └── contact-sheet.py           # 截图拼缩略图总览（Python + Pillow）
├── evals/
│   └── trigger_cases.json         # 路由用例（含触发与近邻负例）
└── examples/
    └── preview.jpg                # 六页骨架预览
```

## 快速开始 / Quick Start

### 1. 装进 Agent

```bash
cp -r rice-paper-ppt ~/.workbuddy/skills/     # WorkBuddy
cp -r rice-paper-ppt ~/.claude/skills/        # Claude Code
```

Agent 依据 `SKILL.md` 的 description 自动匹配触发词（「米纸风 PPT」「把这份 PPT 改成米纸风格」
「字放大一点、别那么空」等）。

### 2. 只用模板，不装 Skill

```bash
mkdir my-deck && cd my-deck
cp <repo>/rice-paper-ppt/assets/{theme.css,deck.js,starter.html} .
mv starter.html index.html
python -m http.server 8000        # 打开 http://localhost:8000
```

改 `index.html` 里的文案与图片即可。六个 `<section class="slide">` 分别演示一种版式。

### 3. 跑验收

```bash
npm i -D playwright-core && npx playwright install chromium   # 首次
node <repo>/rice-paper-ppt/scripts/audit.js http://localhost:8000/index.html ./shots
python <repo>/rice-paper-ppt/scripts/contact-sheet.py ./shots
```

输出示例：

```
页数 6｜硬问题页 0｜含微标签页 5
  仅小字号（人工判断是否为页码/图注）: P1,P2,P3,P4,P5
截图 → ./shots
```

有问题时逐条列出，例如 `P13  sb+42  out:DIV.card [b12]`，表示第 13 页内容区底部溢出 42px。
退出码：0 通过，1 有硬问题，2 环境未就绪。

已有 Chrome 时用 `CHROME_PATH=/path/to/chrome` 免下载浏览器；
`playwright-core` 装在非常规目录时用 `PW_CORE=/path/to/playwright-core`。

## 字号体系（1280×720 画布）

| 用途 | 变量 | 字号 |
|---|---|---:|
| 封面主标题 | `--fs-cover` | 76px |
| 章节标题 | `--fs-sec` | 60px |
| 页面主标题 | `--fs-h1` | 40px |
| 一级模块标题 | `--fs-h2` | 27px |
| 页面引导语 | `--fs-lead` | 23px |
| 卡片标题 | `--fs-card` | 23px |
| 正文 | `--fs-body` | 21px |
| 表格正文 | `--fs-td` | 20px |
| 表格表头 | `--fs-th` | 18px |
| 代码 | `--fs-code` | 18px |
| 注释 | `--fs-note` | 16px |
| 辅助标签 | `--fs-kick` | 15px |
| 页脚页码 | `--fs-foot` | 13px |

间距同理：`--pad-x` 46px、`--pad-t` 30px、`--gap` 16px；
内容区 `.sb` 从 y=150 到 y=662，**可用高度恒为 512px**，所有版式计算由这个数倒推。

## 配色 / Palette

| 变量 | 值 | 用途 |
|---|---|---|
| `--paper` | `#FAF6E9` | 页面底色（暖米纸） |
| `--paper-2` | `#F4EDDA` | 次级底 / 卡片 |
| `--green` | `#2F4A38` | 主色：标题、强调块、结语底 |
| `--gold` | `#A87F3F` | 辅助强调：编号、关键条 |
| `--ink` | `#22302A` | 正文墨色 |

换一套气质只改这三个主值即可，`--paper-2/3`、`--green-2` 等派生色会跟着变。

## 设计原则

内容优先级从高到低：**内容正确性 > 投影可读性 > 信息层级 > 空间利用率 > 视觉美观 > 装饰效果**。
文案分语言与结构两份，分别以 `references/copywriting-spec.md`（措辞/句式/标点）、
`references/content-structure-spec.md`（术语/层级/压缩/可视化）为验收标准，
视觉以 `references/typography-spec.md` 为验收标准；措辞冲突以前者为准、信息结构与术语命名以后者为准。
以准确传递信息为首要目标，以专业术语建立表达体系，以页面结构体现逻辑关系。

四条禁令（会掩盖问题，不是解决问题）：

1. 局部 `transform: scale()` 缩小内容
2. `zoom` 压缩页面
3. `overflow: hidden` 藏掉溢出的正文
4. 靠减小字号或滚动条承载放不下的内容

整页适配浏览器窗口的等比缩放是允许的，由 `deck.js` 统一处理。

## 兼容性

- Chromium / Chrome / Edge 现代版本；Firefox、Safari 亦可（渐变 `mask` 有轻微差异，不影响阅读）。
- 中文字体优先思源宋体 / 思源黑体 / 苹方 / 微软雅黑，缺失时回落到系统衬线 / 无衬线。
- 打印：`p` 键进入打印视图，每页一张 16:9；视频会显示首帧占位。

## 许可 / License

MIT，见 [LICENSE](LICENSE)。
