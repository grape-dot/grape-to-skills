#!/usr/bin/env python3
"""图片墙 6 半圆扇面式的几何计算器 —— 输出可直接粘贴的 CSS。

半圆扇面（6 式）的所有坐标都来自同一次计算：外弧、内弧、四片扇骨的三角形、每张图的
水平中心。手改其中一处，另外几处立刻错位，所以换张数 / 换张角时跑这个脚本，
把三段输出整段替换进 theme.css。

    python scripts/fan-wall.py                 # 默认 4 片、半张角 38°、厚 290
    python scripts/fan-wall.py -n 5 --theta 42 # 五片、更张开
    python scripts/fan-wall.py --thick 260     # 扇面更薄，墙更矮

约束（脚本只算、不校验）：圆心在舞台下方，外弧顶点贴 y=0，舞台左右出血铺满 1280。
墙高 H = r_out(1-cosθ) + T·cosθ，超过 470 就要回头压厚度或半张角，否则内容区放不下图注。
"""
import argparse
import math

W = 1280.0          # 画布宽（出血后铺满 1280）
GAP_DEG = 0.08      # 每片两端各让的角度；外弧约 2.9px、内弧约 2.1px
FAR_EXTRA = 260.0   # 三角形远点超出外弧的距离，保证被舞台 path 完整裁掉


def fmt(v):
    return ('%.0f' % v).replace('-0', '0')


def arc(r, p0, p1, segs, move):
    """r 半径、p0→p1（度）的圆弧，拆成 segs 段三次贝塞尔，返回 SVG path 片段。"""
    out = []
    step = (p1 - p0) / segs
    for i in range(segs):
        a0 = p0 + step * i
        a1 = a0 + step
        k = 4.0 / 3.0 * math.tan(math.radians(step) / 4.0)
        x0, y0 = sign[0] + r * math.sin(math.radians(a0)), cy - r * math.cos(math.radians(a0))
        x1, y1 = sign[0] + r * math.sin(math.radians(a1)), cy - r * math.cos(math.radians(a1))
        c1 = (x0 + k * r * math.cos(math.radians(a0)), y0 + k * r * math.sin(math.radians(a0)))
        c2 = (x1 - k * r * math.cos(math.radians(a1)), y1 - k * r * math.sin(math.radians(a1)))
        out.append(('M%s %s ' % (fmt(x0), fmt(y0)) if (i == 0 and move) else '') +
                   'C%s %s %s %s %s %s' % (fmt(c1[0]), fmt(c1[1]), fmt(c2[0]), fmt(c2[1]), fmt(x1), fmt(y1)))
    return ' '.join(x for x in out if x)


ap = argparse.ArgumentParser()
ap.add_argument('-n', '--n', type=int, default=4, help='扇叶数（默认 4）')
ap.add_argument('--theta', type=float, default=38.0, help='半张角，度（默认 38）')
ap.add_argument('--thick', type=float, default=290.0, help='扇面径向厚度（默认 290）')
ap.add_argument('--img-width', type=float, default=460.0, help='每张图的宽度（默认 460）')
a = ap.parse_args()

theta, n, T, iw = a.theta, a.n, a.thick, a.img_width
sign = (W / 2.0,)
r_out = (W / 2.0) / math.sin(math.radians(theta))
r_in = r_out - T
cy = r_out
H = cy - r_in * math.cos(math.radians(theta))
span = 2 * theta / n

print('# 几何：r_out %.1f  r_in %.1f  圆心 (640, %.1f)  舞台 1280×%.1f' % (r_out, r_in, cy, H))
print('# 外弧 顶点 y=0、两端 y=%.1f；内弧 中央 y=%.1f、两端 y=%.1f' %
      (cy - r_out * math.cos(math.radians(theta)), cy - r_in, H))
mid_w = (r_out + r_in) / 2 * math.radians(span)
print('# 每片中径可见宽 %.0fpx；缝 外弧 %.1fpx / 内弧 %.1fpx' %
      (mid_w, 2 * GAP_DEG * math.pi / 180 * r_out, 2 * GAP_DEG * math.pi / 180 * r_in))
print()

path = arc(r_out, -theta, theta, 4, True)
path += ' L%.0f %.0f' % (sign[0] + r_in * math.sin(math.radians(theta)),
                         cy - r_in * math.cos(math.radians(theta)))
path += ' ' + arc(r_in, theta, -theta, 4, False)
path += ' Z'
print('/* .w-sec 的舞台 path 与高度 */')
print('height: %.0fpx;' % H)
print('clip-path: path("%s");' % path)
print()

R = r_out + FAR_EXTRA
print('/* 每片扇骨：三角形远点在 r=%.0f，弧交给舞台裁 */' % R)
for i in range(n):
    a0 = -theta + span * i + GAP_DEG
    a1 = -theta + span * (i + 1) - GAP_DEG
    p0 = (sign[0] + R * math.sin(math.radians(a0)), cy - R * math.cos(math.radians(a0)))
    p1 = (sign[0] + R * math.sin(math.radians(a1)), cy - R * math.cos(math.radians(a1)))
    cm = (a0 + a1) / 2.0
    cx = sign[0] + ((r_out + r_in) / 2.0) * math.sin(math.radians(cm))
    print('.w-sec .sd:nth-child(%d) { --cx: %.0fpx; clip-path: polygon(%.0fpx %.0fpx, %spx %spx, %spx %spx); }' %
          (i + 1, cx, sign[0], cy, fmt(p1[0]), fmt(p1[1]), fmt(p0[0]), fmt(p0[1])))
print()
print('/* 图宽 %d、居中到 --cx：cover 只裁到本片附近 */' % iw)
print('.w-sec .sd img { position: absolute; top: 0; height: 100%%; width: %.0fpx; '
      'left: calc(var(--cx) - %.0fpx); object-fit: cover; display: block; }' % (iw, iw / 2.0))
print()
print('# 预算：墙 %.0f + 间隔 16 + 图注 24 = %.0f（内容区 512，余 %.0f）' % (H, H + 40, 512 - H - 40))
