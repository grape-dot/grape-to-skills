# Examples

`nut-crisis.json` 是唯一的手写输入，其余都是它跑出来的产物。

| 路径 | 是什么 | 怎么产生 |
| --- | --- | --- |
| `nut-crisis.json` | 完整 board：2 角色 / 10 道具 / 6 色 / 9 格 / 14 句对白 | 手写。写新 board 时照它抄结构 |
| `out/prompt.md` | **默认输出**：英文段 + 中文段，可直接粘贴 | `python scripts/assemble.py examples/nut-crisis.json -o examples/out` |
| `full/sheet-prompt.en.md` | 拆分包：英文单独一份 | `--full` |
| `full/sheet-prompt.zh.md` | 拆分包：中文单独一份 | `--full` |
| `full/continuity-table.md` | 道具状态链台账，9 行 × 10 列 | `--full` |
| `full/cell-01..09.en.md` | 单格放大稿，关键帧重绘用 | `--full` |

## 看什么

- 想判断"好"长什么样 → 读 `out/prompt.md`，注意 `SETTING` / `RENDER LANGUAGE` / `CHARACTERS` / `PROPS` 四段是常量，九格共用。
- 想理解状态链 → 读 `full/continuity-table.md`。`nut_bag` 一行走过 `upright_on_shelf → burst_open → flattened_on_floor`，没有回头。
- 想写自己的 board → 抄 `nut-crisis.json`，先改 `meta` 与 `world`，再改角色锁，最后改九格。
- 想看单格怎么写 → `full/cell-08.en.md`（beauty shot，柔光 + 中心构图）。

## 重新生成

```bash
cd ..
python scripts/assemble.py examples/nut-crisis.json -o examples/out
python scripts/assemble.py examples/nut-crisis.json -o examples/full --full
```

产物会覆盖，属正常。
