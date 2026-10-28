"""assemble.py 的回归测试。

只跑标准库，不需要安装任何依赖：
    python -m unittest discover -s tests -v

测试的重心是**校验器是否真的拦得住**——这是脚本相对人肉写提示词的全部价值。
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "assemble.py"
SAMPLE = ROOT / "examples" / "nut-crisis.json"


def load_sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(ROOT),
            env=env,
        )

    def render(self, board: dict, *extra: str) -> str:
        path = self.tmp / "board.json"
        path.write_text(json.dumps(board, ensure_ascii=False), encoding="utf-8")
        result = self.run_cli(str(path), "--stdout", *extra)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def assert_rejected(self, board: dict, needle: str) -> None:
        path = self.tmp / "board.json"
        path.write_text(json.dumps(board, ensure_ascii=False), encoding="utf-8")
        result = self.run_cli(str(path), "--stdout")
        self.assertEqual(result.returncode, 2, "破坏性输入应当被拦下")
        self.assertIn(needle, result.stdout + result.stderr)


class TestRender(Base):
    def test_nine_panels_no_tenth(self) -> None:
        out = self.render(load_sample())
        for n in range(1, 10):
            self.assertIn(f"PANEL {n:02d}", out)
        self.assertNotIn("PANEL 10", out)

    def test_character_lock_is_verbatim(self) -> None:
        db = load_sample()
        out = self.render(db)
        for ch in db["characters"]:
            self.assertIn(ch["lock_en"].strip(), out)

    def test_palette_is_closed(self) -> None:
        db = load_sample()
        out = self.render(db)
        for sw in db["palette"]:
            self.assertIn(sw["hex"], out)

    def test_no_prop_id_leaks_into_prompt(self) -> None:
        """id 和 key=value 会被出图模型当文字画出来，必须不出现在提示词里。"""
        db = load_sample()
        out = self.render(db)
        self.assertNotIn("[bowl]", out)
        self.assertNotIn("bowl=heaped", out)
        self.assertNotIn("nut_bag=", out)

    def test_english_only_skips_chinese_block(self) -> None:
        out = self.render(load_sample(), "--en-only")
        self.assertNotIn("一张白色制作稿纸", out)
        self.assertIn("PANEL 01", out)

    def test_default_output_contains_both_languages(self) -> None:
        out = self.render(load_sample())
        self.assertIn("PANEL 01", out)
        self.assertIn("一张白色制作稿纸", out, "默认应同时给出中文段")

    def test_full_package_writes_expected_files(self) -> None:
        outdir = self.tmp / "full"
        result = self.run_cli(str(SAMPLE), "-o", str(outdir), "--full")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        expected = ["sheet-prompt.en.md", "sheet-prompt.zh.md", "continuity-table.md"]
        for name in expected:
            self.assertTrue((outdir / name).is_file(), f"缺少 {name}")
        for n in range(1, 10):
            self.assertTrue((outdir / f"cell-{n:02d}.en.md").is_file(), f"缺少 cell-{n:02d}")

    def test_continuity_table_has_nine_rows(self) -> None:
        outdir = self.tmp / "full"
        self.run_cli(str(SAMPLE), "-o", str(outdir), "--full")
        table = (outdir / "continuity-table.md").read_text(encoding="utf-8")
        rows = [line for line in table.splitlines() if line.startswith("| ") and line[2:4].strip().isdigit()]
        self.assertEqual(len(rows), 9, f"台账应有 9 行，实得 {len(rows)}")

    def test_source_order_is_stable(self) -> None:
        """同一份输入渲染两次必须逐字相同（提示词里不许有随机成分）。"""
        self.assertEqual(self.render(load_sample()), self.render(load_sample()))


class TestValidation(Base):
    def test_rejects_unregistered_prop(self) -> None:
        db = load_sample()
        db["shots"][0]["props"].append("ghost_prop")
        self.assert_rejected(db, "未登记的道具")

    def test_rejects_state_outside_enum(self) -> None:
        db = load_sample()
        db["shots"][0]["state"]["bowl"] = "on_fire"
        self.assert_rejected(db, "不在枚举内")

    def test_rejects_chinese_dialogue(self) -> None:
        db = load_sample()
        db["shots"][0]["dialogue"][0]["line_en"] = "清点库存"
        self.assert_rejected(db, "对白混入中文")

    def test_rejects_wrong_panel_count(self) -> None:
        db = load_sample()
        db["shots"] = db["shots"][:8]
        self.assert_rejected(db, "正好 9 格")

    def test_rejects_duplicate_prop_id(self) -> None:
        db = load_sample()
        dup = dict(db["props"][0])
        db["props"].append(dup)
        self.assert_rejected(db, "重复")

    def test_rejects_invalid_hex(self) -> None:
        db = load_sample()
        db["palette"][0]["hex"] = "gold"
        self.assert_rejected(db, "hex")

    def test_rejects_missing_world_axis(self) -> None:
        db = load_sample()
        del db["world"]["axis_en"]
        self.assert_rejected(db, "axis_en")


if __name__ == "__main__":
    unittest.main()
