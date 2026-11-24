# Changelog

版本号遵循 [Semantic Versioning](https://semver.org/)。

## 1.4.0 — 2026-11-24

工程完整性修复：让包内元数据与规范、与实际文件对齐。

**修复**
- `manifest.json` 枚举值落在规范外：`maturity_tier`/`lifecycle_stage` 由 `scaffold`/`personal` 改为 `library`，`review_cadence` 由 `as-needed` 改为 `per-release`，删除非法字段 `context_budget_tier: "lean"`。
- `pyproject.toml` 版本号与 SKILL.md、manifest 同步到 1.4.0（此前三处不一致）。
- 补回 `.github/workflows/ci.yml`（此前 CHANGELOG 1.3.0 声称已有，实际缺失）：单元测试 + 渲染冒烟 + 元数据一致性检查。

**变更**
- frontmatter 三份 `description`（`description` / `description_zh` / `description_en`）合并为一份：宿主只读 `description`，另两份只增加初始加载成本。
- `SKILL.md` 去重：皮克斯六轴表、语音四轴表、版式要点与 `references/pixar-style.md`、`voice-casting.md`、`sheet-layout.md` 重复的部分改为压缩要点 + 指针（9.8k → 8.5k 字符）。

**新增**
- `evals/trigger_cases.json`：12 条机器可读路由用例（含 4 条近邻负例），可与 `evals/cases.md` 的行为/回归用例配合使用。
- `examples/renders/` 两张真实出图（单场景闹剧 / 双人对白），1672 × 941、未修图；README 中英两版新增「出来长什么样 / What comes out」小节，把它们当作单页密度与三类失守点（分层漂成 3D 渲染、文字量超预算、道具形制漂移）的可视证据。

## 1.3.0 — 2026-10-24

首个公开发布。

**新增**
- `references/pixar-style.md`：皮克斯风格六轴渲染契约（造型 / 材质 / 光 / 色 / 空间 / 表演），三段可粘贴片段（场景段 / 角色段 / 负面段）、30 秒自检、出处。
- `references/board-schema.md`：board JSON 字段表与校验规则速览。
- `tests/test_assemble.py`：16 项测试，纯标准库，覆盖渲染与校验两侧。
- `.github/workflows/ci.yml`：Python 3.9 / 3.11 / 3.13。
- `pyproject.toml`：`storyboard-sheet` 命令行入口。

**变更**
- 皮克斯风格升级为第 4 条硬前提，与用户偏好无关，每单都执行。
- 默认交付改为**回复里两段提示词**（英文在前、中文在后），不落文件、不产 JSON、不产台账。Bible 转为过程产物。
- 中文段改为"同一份常量的中文表述"，不再是对英文的逐句直译——直译会把 `#2F6FB0` 写成"一种蓝色"。
- `assemble.py` 命令行重组：默认写 `./prompt.md`，新增 `--stdout` / `--en-only` / `--full` / `--no-cells` / `--check-only`。
- 一致性红线从 12 条扩到 13 条（加入风格锚）。

**修复**
- 面板描述曾输出 `the ceramic seed bowl [bowl]` 与 `state: bowl=heaped`，方括号与等号会被出图模型当作画面文字绘出；改为自然语言并限制 id 不外泄。

## 1.0.0 — 2026-10-23

内部初版，未公开发布。建立 Scene Bible 优先的三层管线、十三条一致性约束与 `assemble.py` 校验器。
