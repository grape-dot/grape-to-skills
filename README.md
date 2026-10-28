# grape-to-skills

AI Agent Skill 集合仓库。每个子目录是一个独立的 Agent Skill（提示词工程型），遵循
`SKILL.md` + 资源文件的标准结构，可整体复制到 Agent 的技能目录（如 WorkBuddy 的
`~/.workbuddy/skills/`、Claude 的 `~/.claude/skills/`）直接使用。

## 包含的 Skills

| 目录 | 名称 | 用途 | 许可 |
| --- | --- | --- | --- |
| [`img-antiquity/`](img-antiquity/) | 东方文化编辑设计图像生成 | 组装「中国古典水墨卷轴 × 现代杂志编辑设计」风格的出图提示词，用于海报、封面、图录跨页等 | MIT |
| [`storyboard-sheet-prompt/`](storyboard-sheet-prompt/) | 手绘分镜脚本提示词（v1.3.0） | 把一段情景转成 16:9 九宫格手绘分镜脚本页的中英双语出图提示词，内置 Scene Bible 防止九格漂移，角色强制皮克斯风格化写实 | 见目录内 LICENSE |

## img-antiquity

一句话：给出主题和用途，产出一段可直接粘贴进 Midjourney / SD / DALL·E / 即梦 /
通义万相的东方编辑设计风格提示词。

- 核心逻辑在 `SKILL.md`（风格定位、工作流程、硬规则、纠错）
- 提示词模板在 `prompts/`（中/英两套，含变量表与负面提示词）
- 效果参考在 `examples/`（刺绣封面、青花瓷图录跨页两张样图）

## storyboard-sheet-prompt

一句话：一段故事情景 → 一张 16:9 手绘分镜脚本页提示词（3×3 红框九格分镜 +
右侧角色设计面板 + 底部三个手写笔记框），默认交付英文 + 中文两段可直接粘贴的提示词。

- 核心逻辑在 `SKILL.md`（交付规则、四条硬前提、皮克斯六轴风格规格）
- `references/` 下的规格文档按需查阅：板式 schema、Scene Bible、皮克斯风格、
  提示词模板、交付清单、选角配音等
- `scripts/assemble.py`：九格 JSON → 完整提示词的组装脚本（仅用户明确要文件时使用），
  校验方式：`python scripts/assemble.py examples/nut-crisis.json --stdout`
- `examples/`：完整九格示例（nut-crisis）、样张渲染图（`renders/`）
- `evals/`、`tests/`：质量评估用例与测试
- 另有 `README.zh-CN.md`、`CHANGELOG.md`、`CONTRIBUTING.md` 等仓库元文档

## 使用方式

把某个 skill 目录整体复制到 Agent 的技能目录即可；Agent 会根据 `SKILL.md` 的
description 自动匹配触发词（如「水墨国风海报」「分镜脚本」）。两个 skill 均为
提示词工程型——**只产出提示词，不直接生成图片**，出图由当前环境的图像生成工具完成。
