# rice-paper-ppt

**米纸质感 HTML 幻灯片** — 一套「暖米纸 + 深林绿 + 哑光金」的中文编辑版式系统（Skill），
把纸感配色、衬线大标题、投影级字号规范与逐页版式验收固化下来，
让 Agent 直接产出可讲、可投影、可离线分发的 HTML 幻灯片。

**它是一套风格，不是一个用途。** 汇报、路演、方案宣讲、复盘、培训、分享会、
文化展陈、课程——凡是需要在屏幕上讲、且希望它看起来像一本装帧考究的册子，都适用。

A warm rice-paper HTML slide style — 16:9, 1280×720, forest green and matte gold with
serif display type, typography scaled for projection, plus a Playwright-based layout audit.

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
- **十种版式配方**：按「页面作用」选版面，相邻页强制换版式，避免通篇卡片网格。
- **可验证的验收**：`scripts/audit.js` 用 Playwright 逐页真实渲染，检出内容溢出、越界、
  静默裁切、容器内溢、过小字号五类问题，返回退出码可当 CI 闸门。
- **样式单点控制**：所有字号 / 间距都是 `:root` 里的 CSS 变量，整体放大缩小改一处即可。
- **完整交互**：方向键 / Home / End / 数字键翻页、`f` 全屏、`p` 打印、`#N` 深链、
  窗口自适应等比缩放、视频播放与声音开关。

## 目录结构 / Structure

```text
rice-paper-ppt/
├── SKILL.md                       # AI Skill 主文件（工作流、硬约束、版式选择表）
├── README.md                      # 本文件
├── LICENSE                        # MIT
├── assets/
│   ├── theme.css                  # 版式系统：设计 token + 全部组件（508 行）
│   ├── deck.js                    # 缩放 / 翻页 / 全屏 / 打印（86 行，无需修改）
│   ├── starter.html               # 6 页可运行骨架
│   └── example.jpg                # 占位图
├── references/
│   ├── typography-spec.md         # 排版与字号规范原文（11 节，验收标准）
│   ├── components.md              # 类名词典 + 可复制组件片段 + 硬坐标
│   └── page-patterns.md           # 10 种版式配方 + 空旷 / 拥挤症状表
├── scripts/
│   ├── audit.js                   # 逐页版式审计（Node + Playwright）
│   └── contact-sheet.py           # 截图拼缩略图总览（Python + Pillow）
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
