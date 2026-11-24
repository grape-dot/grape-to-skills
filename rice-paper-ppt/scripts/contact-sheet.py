#!/usr/bin/env python3
"""把 audit.js 的逐页截图拼成缩略图总览，用于肉眼复核。

用法：
    python contact-sheet.py <shots目录> [-o 输出目录] [--per 6] [--cols 2]

默认每张拼 6 页（2 列 × 3 行），输出到 <shots>/sheets/。
逐页看 57 张原图太慢，先扫一遍总览定位可疑页，再单独放大看。
"""
import argparse
import glob
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow：pip install pillow")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots", help="截图目录")
    ap.add_argument("-o", "--out", default=None, help="输出目录，默认 <shots>/sheets")
    ap.add_argument("--per", type=int, default=6, help="每张拼几页，默认 6")
    ap.add_argument("--cols", type=int, default=2, help="列数，默认 2")
    ap.add_argument("--width", type=int, default=640, help="单页缩略图宽度，默认 640")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.shots, "p*.png")))
    if not files:
        sys.exit(f"{args.shots} 里没找到 p*.png")

    out_dir = args.out or os.path.join(args.shots, "sheets")
    os.makedirs(out_dir, exist_ok=True)
    for old in glob.glob(os.path.join(out_dir, "*.jpg")):
        os.remove(old)

    per = args.per
    cols = args.cols
    rows = (per + cols - 1) // cols
    w = args.width
    h = round(w * 720 / 1280)
    gap = 10

    for si in range(0, len(files), per):
        group = files[si:si + per]
        sheet = Image.new("RGB", (w * cols + gap * (cols + 1), h * rows + gap * (rows + 1)), (235, 232, 222))
        for k, f in enumerate(group):
            im = Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS)
            x = gap + (k % cols) * (w + gap)
            y = gap + (k // cols) * (h + gap)
            sheet.paste(im, (x, y))
        name = f"s{si // per + 1:02d}.jpg"
        sheet.save(os.path.join(out_dir, name), quality=88)
        print(f"{name}  P{si + 1}-P{si + len(group)}")

    print(f"共 {len(files)} 页 → {out_dir}")


if __name__ == "__main__":
    main()
