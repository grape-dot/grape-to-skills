#!/usr/bin/env python3
"""storyboard-sheet-prompt / assemble.py

把 storyboard.json（Scene Bible + 9 个 beat）拼成**一段可直接粘贴的提示词**。
脚本的存在意义：Bible 里的造型锁、道具锁、色板会被**逐字注入**每一格，
人肉复述必然走形，机器不会。

默认只产出一份 prompt.md，内含**英文段 + 中文段**（同一份 Bible，两种语言）。拆分包是 opt-in，不要主动加。

零依赖，Windows 下 UTF-8 安全。

用法:
    python assemble.py board.json                 # → ./prompt.md（英+中）
    python assemble.py board.json --stdout        # 直接打印，不落盘（首选）
    python assemble.py board.json --en-only       # 只出英文段
    python assemble.py board.json --full          # 拆分包（中英分文件+台账+单格稿）
    python assemble.py board.json --check-only    # 只校验
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")

FRAMING_EN = {
    "NEAR": "near shot",
    "MEDIUM": "medium shot",
    "MED-WIDE": "medium-wide shot",
    "WIDE": "wide shot",
    "BEAUTY": "near shot, beauty lighting",
}
FRAMING_ZH = {
    "NEAR": "近景",
    "MEDIUM": "中景",
    "MED-WIDE": "中宽镜",
    "WIDE": "广角",
    "BEAUTY": "近景 beauty shot",
}

DEFAULT_NEGATIVE = (
    "more than nine panels, an empty panel, tenth panel, photo-real humans, "
    "extra characters, clothing or accessories on the animals, glossy plastic toy look, "
    "wax-like surfaces, specular sheen, rim light on both sides, golden-hour haze everywhere, "
    "crushed blacks, clipped whites, neon oversaturation, perfectly symmetrical composition, "
    "over-detailed clutter, doll eyes without catchlights, neon rim light, gradient backgrounds, "
    "long paragraphs of text, garbled lettering, thick colored borders, drop shadow on the frames, "
    "watermark, signature"
)

PIXAR_RENDER = (
    "RENDER LANGUAGE (identical in all nine panels): a Pixar-style 3D animated feature "
    "frame — stylized realism, not photoreal: forms pushed and simplified, materials kept "
    "tactile and believable. Soft area-light key with a single direction, one-sided rim "
    "light separating the subject from the background, shadows tinted toward the sky "
    "colour rather than neutral black, atmospheric perspective dissolving distance, "
    "blacks lifted (no crushed black), highlights rolled off (no clipped white), "
    "35mm-equivalent lens with shallow depth of field, one brightest focal point per frame. "
    "Each panel is a graphite production sketch OF a Pixar-style 3D film frame — the "
    "drawing medium is pencil, the world inside the frame is Pixar."
)

PIXAR_DESIGN = (
    "DESIGN LANGUAGE: Pixar character design — silhouette-first, one dominant shape "
    "language per character, eyes about one third of the face height and set low, "
    "features reduced to the minimum that reads, one deliberate imperfection kept, "
    "subsurface scattering only at fur edges, ears, nose and cheeks, soft short-scatter "
    "warm tone, matte non-glossy surfaces, believable weight and contact shadows."
)

PIXAR_NEG_ZH = (
    "塑料蜡感、镜面高光、双侧轮廓光、处处黄金时刻、死黑、切白、霓虹过饱和、"
    "正中对称、堆细节、无高光的死鱼眼、近写实恐怖谷"
)

PIXAR_RENDER_ZH = (
    "渲染语言（九格完全相同）：一部皮克斯风 3D 动画长片的画面——风格化写实，不是照片级写实："
    "造型往外推、做简化，材质保持可触可信。面积光单一方向主光，单侧轮廓光把主体从背景剥离，"
    "阴影带天光色而不是中性黑，大气透视把远处化开，暗部抬黑不死黑，高光滚降不切白，"
    "35mm 等效镜头浅景深，每格只有一个最亮焦点。"
    "每一格都是「一部皮克斯风 3D 电影画面」的石墨分镜稿——画的是铅笔，格子里那个世界是皮克斯的。"
)

PIXAR_DESIGN_ZH = (
    "设计语言：皮克斯式角色设计——剪影优先，每个角色只用一种主动力形状，"
    "眼高约占脸高三分之一且位置偏低，五官减到刚好能读的程度，保留一处刻意的不完美，"
    "次表面散射只给毛边、耳、鼻、颊，散射距离短、偏暖，表面哑光不反光，重量与接触阴影可信。"
)

ERRORS: list[str] = []
WARNS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNS.append(msg)


# --------------------------------------------------------------------------- load


def load(path: Path) -> dict:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        sys.exit(f"[FATAL] 找不到文件: {path}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        sys.exit(f"[FATAL] JSON 解析失败 ({path}): {exc}")


# --------------------------------------------------------------------------- validate


def validate(db: dict) -> None:
    meta = db.get("meta") or {}
    for key in ("production", "scene_id", "scene_title", "shots_label_zh"):
        if not meta.get(key):
            err(f"meta.{key} 缺失（页眉需要它）")

    world = db.get("world") or {}
    for key in ("space_en", "axis_en", "scale_en", "light_en"):
        if not world.get(key):
            err(f"world.{key} 缺失 —— 这四行定生死，不能空")

    chars = db.get("characters") or []
    if len(chars) < 2:
        warn("角色少于 2 个：本 skill 默认双主角，单角色请确认是否真的只需要一个")
    seen = set()
    for ch in chars:
        cid = ch.get("id")
        if not cid:
            err("某个 character 缺 id")
        elif cid in seen:
            err(f"character id 重复: {cid}")
        seen.add(cid)
        if not ch.get("lock_en"):
            err(f"character {cid} 缺 lock_en（造型锁）")
        if not ch.get("anchors"):
            warn(f"character {cid} 没写 anchors，跨格辨识度会下降")

    props = db.get("props") or []
    if len(props) < 3:
        err("道具少于 3 个：情景必然还有物件没登记")
    pids = {}
    for p in props:
        pid = p.get("id")
        if not pid:
            err("某个 prop 缺 id")
            continue
        if pid in pids:
            err(f"prop id 重复: {pid}")
        pids[pid] = p
        if not p.get("lock_en"):
            err(f"prop {pid} 缺 lock_en")

    palette = db.get("palette") or []
    if len(palette) < 4:
        err("色板少于 4 色（角色 ×2 + 环境 ×2 是下限）")
    for sw in palette:
        hexv = sw.get("hex", "")
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", hexv):
            err(f"palette 颜色 {sw.get('id')} 的 hex 不合法: {hexv!r}")
        if not sw.get("use_en"):
            warn(f"palette {sw.get('id')} 没写排他用途，颜色可能串场")

    shots = db.get("shots") or []
    if len(shots) != 9:
        err(f"必须正好 9 格，当前 {len(shots)} 格")
    prev_frames: list[str] = []
    for i, shot in enumerate(shots, start=1):
        tag = f"shot {i:02d}"
        framing = (shot.get("framing") or "").upper()
        if framing not in FRAMING_EN:
            err(f"{tag} framing 非法: {framing!r}，可选 {sorted(FRAMING_EN)}")
        if not shot.get("action_en"):
            err(f"{tag} 缺 action_en")
        for pid in shot.get("props") or []:
            if pid not in pids:
                err(f"{tag} 引用了未登记的道具: {pid}")
        for pid, state in (shot.get("state") or {}).items():
            if pid not in pids:
                err(f"{tag} state 里的道具未登记: {pid}")
                continue
            allowed = pids[pid].get("states") or []
            if allowed and state not in allowed:
                err(f"{tag} 道具 {pid} 的状态 {state!r} 不在枚举内 {allowed}")
        for line in shot.get("dialogue") or []:
            text = line.get("line_en", "")
            if not text:
                err(f"{tag} 有一条空对白")
            if CJK.search(text):
                err(f"{tag} 对白混入中文: {text!r} —— 对白必须全英文")
            if len(text.split()) > 8:
                warn(f"{tag} 对白超过 8 词，画面上会糊: {text!r}")
        prev_frames.append(framing)

    run = 1
    for i in range(1, len(prev_frames)):
        run = run + 1 if prev_frames[i] == prev_frames[i - 1] else 1
        if run >= 3:
            warn(f"第 {i - 1}–{i + 1} 格镜别连续相同（{prev_frames[i]}），节奏会死")
            run = 1
    if prev_frames and prev_frames[-1] != "WIDE":
        warn("第 9 格不是 WIDE，收尾收不拢空间关系")
    if not any(f in ("WIDE", "MED-WIDE") for f in prev_frames[4:6]):
        warn("第 5/6 格没有尺度跳跃，'巨大厨房 vs 渺小主角'的喜剧来源不成立")

    notes = db.get("notes") or {}
    for key in ("flow_en", "camera_en"):
        if not notes.get(key):
            err(f"notes.{key} 缺失（底部方框需要）")


# --------------------------------------------------------------------------- render en


def _chars_block(db: dict) -> list[str]:
    out = []
    for ch in db.get("characters", []):
        out.append(ch["lock_en"].strip())
    return out


def _props_block(db: dict) -> list[str]:
    """道具清单。附带出现格位，限制模型在无关的格里画它。"""
    where: dict[str, list[int]] = {}
    for shot in db.get("shots", []):
        ids = list(shot.get("props") or []) + list((shot.get("state") or {}).keys())
        for pid in ids:
            where.setdefault(pid, [])
            if shot["n"] not in where[pid]:
                where[pid].append(shot["n"])
    out = []
    for p in db.get("props", []):
        panels = where.get(p["id"], [])
        if panels:
            tag = "appears only in panel " if len(panels) == 1 else "appears in panels "
            tag += ", ".join(f"{n:02d}" for n in panels)
        else:
            tag = "not shown on this sheet"
        scale = f", {p['scale_en']}" if p.get("scale_en") else ""
        out.append(f"- {p['lock_en'].strip()}{scale} — {tag}")
    return out


def _palette_block(db: dict) -> list[str]:
    out = []
    for sw in db.get("palette", []):
        out.append(f"  {sw['hex']} — {sw.get('name_en', sw['id'])} — {sw['use_en']}")
    return out


def _panel_line(db: dict, shot: dict) -> str:
    """单格描述。注意：不输出道具 id、不输出 key=value —— 模型会把它们当文字画出来。"""
    n = shot["n"]
    framing = FRAMING_EN[shot["framing"].upper()]
    by_id = {p["id"]: p for p in db.get("props", [])}
    pnames = [by_id[pid].get("name_en", pid) for pid in shot.get("props") or [] if pid in by_id]
    states = shot.get("state") or {}
    state_txt = "; ".join(
        f"{by_id[k].get('name_en', k)} is {v.replace('_', ' ')}" for k, v in states.items() if k in by_id
    )
    arrow = (shot.get("arrow_en") or "").strip()
    dlg = " / ".join(
        f"{_who(db, d['who'])}: \"{d['line_en']}\"" for d in (shot.get("dialogue") or [])
    )
    bits = [f"PANEL {n:02d} — {framing.upper()} — {shot['action_en'].strip()}"]
    if pnames:
        bits.append("in frame: " + "; ".join(pnames))
    if state_txt:
        bits.append("prop state: " + state_txt)
    if arrow:
        bits.append(f'blue arrow note: "{arrow}"')
    if dlg:
        bits.append("handwritten speech note beside the frame — " + dlg)
    return " | ".join(bits)


def _who(db: dict, cid: str) -> str:
    for ch in db.get("characters", []):
        if ch["id"] == cid:
            return ch.get("name_en", cid).upper()
    return cid.upper()


def render_en(db: dict) -> str:
    meta, world = db["meta"], db["world"]
    L: list[str] = []

    L.append(
        "A single flat sheet of white production paper, scanned overhead, no perspective "
        f"on the paper itself. Aspect ratio {meta.get('aspect', '16:9')}. This is a "
        "professional animation pre-production storyboard sheet — mixed media, part "
        "graphite pencil, part red and blue ink, part finished 3D render."
    )
    L.append("")
    L.append("PAGE HEADER")
    L.append(
        f'Top left: handwritten Chinese marker script reading "{meta["shots_label_zh"]}". '
        f'Top right, small handwritten caps: "{meta["scene_id"]} · {meta["production"]} · '
        f'{meta["scene_title"]}". Thin hand-ruled line under the header.'
    )
    L.append("")
    L.append("LEFT TWO THIRDS — STORYBOARD GRID")
    L.append(
        "Exactly nine panels, arranged in 3 rows and 3 columns. Each panel is a thin "
        "hand-drawn red ink rectangle (1.5-2 px, slightly wobbly, corners slightly "
        f"overrunning) enclosing a {meta.get('aspect', '16:9')} image area. Shot number "
        "written by hand at the lower-left OUTSIDE the frame with a small caps framing "
        "label beside it. One short handwritten action note per panel (max 8 words), kept "
        "outside the frame. Blue ballpoint arrows drawn outside the frames, pointing in at "
        "the relevant object, each with a 2-5 word handwritten note at its tail."
    )
    L.append("")
    L.append("SETTING (identical in all nine panels, do not vary):")
    L.append(f"  {world['space_en']}")
    L.append(f"SCREEN AXIS (never mirrored): {world['axis_en']}")
    L.append(f"SCALE: {world['scale_en']}")
    L.append(f"LIGHT (same in all nine panels): {world['light_en']}")
    L.append("")
    L.append(PIXAR_RENDER)
    L.append("")
    L.append("CHARACTERS (identical in all nine panels, copy verbatim):")
    for line in _chars_block(db):
        L.append(f"  {line}")
    L.append(PIXAR_DESIGN)
    L.append("")
    L.append("PROPS (the only objects permitted to appear; invent nothing else):")
    L.extend(_props_block(db))
    L.append("")
    L.append("PANELS")
    L.append(
        "Any speech note is handwritten BESIDE the frame in a short line, at most two per "
        "panel, never set inside the image area."
    )
    for shot in db["shots"]:
        L.append(_panel_line(db, shot))
    L.append("")
    L.append('RIGHT THIRD — header handwritten caps: "CHARACTER DESIGN & CASTING"')
    L.append(
        "Two character entries stacked vertically, each: name in large handwritten caps, "
        "three short trait tags, a loose graphite pencil sketch on the left, a finished "
        "Pixar-style 3D portrait on the right, and a two-line handwritten caption beneath."
    )
    for ch in db.get("characters", []):
        L.append("")
        L.append(f"  {ch.get('name_en', ch['id']).upper()}")
        if ch.get("traits_en"):
            L.append(f"    tags: {ch['traits_en']}")
        if ch.get("sketch_en"):
            L.append(f"    graphite sketch: {ch['sketch_en']}")
        pose = ch.get("render_pose_en", "neutral three-quarter view")
        L.append(
            "    3D portrait: Pixar-style 3D character render, "
            f"{ch['lock_en'].strip()}. Pose: {pose}. " + PIXAR_DESIGN + " Individual fur "
            "strands catching rim light on ONE side only, oversized expressive eyes with wet "
            "catchlights placed on the key-light side, three-quarter view, shallow depth of "
            "field, warm key light from upper left, cool rim light from behind, neutral "
            "warm-grey studio backdrop, highlights rolled off (no clipped white), lifted "
            "blacks, high-end animation character sheet render, 8k."
        )
        caption = ch.get("caption_lines") or []
        if caption:
            L.append("    caption (2 lines, small handwritten caps): " + " / ".join(caption))

    villain = db.get("villain")
    if villain:
        L.append("")
        L.append("  VILLAIN / PROPS (small block, bottom quarter of the right column)")
        L.append(f"    graphite mini-sketch: {villain.get('sketch_en', 'quick loose sketch')}")
        L.append(
            f"    small 3D render: {villain['lock_en'].strip()}, clean studio render, "
            "soft key light, neutral grey backdrop"
        )
        caption = villain.get("caption_lines") or []
        if caption:
            L.append("    caption (2 lines): " + " / ".join(caption))

    L.append("")
    L.append("BOTTOM STRIP — three hand-drawn boxes with hand-ruled borders")
    flow = db["notes"]["flow_en"].strip()
    camera = db["notes"]["camera_en"].strip()
    L.append(f'  Box 1 "NOTES / FLOW INTENT": {flow}')
    L.append(f'  Box 2 "CAMERA / STORY NOTES": {camera}')
    L.append(
        '  Box 3 "COLOR PALETTE": '
        f"{len(db['palette'])} small cross-hatched colored-pencil swatches, labelled "
        + ", ".join(sw.get("name_en", sw["id"]) for sw in db["palette"])
        + "."
    )
    L.append("")
    L.append("PALETTE — the ONLY colors permitted anywhere on this sheet:")
    L.extend(_palette_block(db))
    L.append(
        "  Page neutrals (not counted): paper white, graphite grey, red ink #C0392B, "
        "blue ink #2F4C8A."
    )
    L.append("")
    L.append(
        "STYLE: authentic film pre-production document, drawn from a Pixar-style 3D feature. "
        "Loose confident graphite sketching, visible construction lines and smudged hatching, "
        "thin wobbly red frames, quick blue arrows, handwritten uppercase notes, polished 3D "
        "character renders pasted into the right column. Clean white paper with faint fiber "
        "texture. Not digital-flat, not vector, not neon, not gradient-heavy."
    )
    L.append("")
    neg = (db.get("negative_extra") or "").strip()
    L.append("NEGATIVE: " + (neg if neg else DEFAULT_NEGATIVE))
    L.append("")
    L.append("CONSISTENCY RULES (highest priority, override anything contradictory):")
    L.append("  1. All nine panels share one world, one light, one screen axis, one palette.")
    L.append("  2. Never substitute, recolor, or restyle a prop between panels.")
    L.append("  3. Never add an object that is not in the PROP list.")
    L.append("  4. Exactly nine panels. No tenth panel, no blank panel.")
    L.append("  5. The Pixar render and design language holds in all nine panels and in both portraits.")
    return "\n".join(L)


# --------------------------------------------------------------------------- render zh


def _zh(db: dict, obj: dict, key: str) -> str:
    val = obj.get(f"{key}_zh")
    if val:
        return val.strip()
    return "[待译] " + (obj.get(f"{key}_en") or "").strip()


def render_zh(db: dict) -> str:
    meta, world = db["meta"], db["world"]
    L: list[str] = []
    L.append(
        f"一张白色制作稿纸的平铺扫描图，纸面本身无透视。画幅 {meta.get('aspect', '16:9')}。"
        "这是一份专业动画电影前期分镜脚本页——混合媒介：石墨铅笔、红蓝墨水、以及完成度较高的 3D 渲染。"
    )
    L.append("")
    L.append("页眉")
    L.append(
        f"左上角：手写马克笔中文「{meta['shots_label_zh']}」。"
        f"右上角：手写大写小字「{meta['scene_id']} · {meta['production']} · {meta['scene_title']}」。"
        "页眉下方一道手绘横线。"
    )
    L.append("")
    L.append("左侧三分之二 —— 分镜网格")
    L.append(
        "严格九个分镜，三行三列排布。每个分镜为细红线手绘矩形框（1.5–2 像素，线条略抖、四角略微出头），"
        f"框内为 {meta.get('aspect', '16:9')} 画面。镜号手写在框外左下角，旁边是小号大写的镜别标注。"
        "每格框外一行手写动作说明（不超过 8 个词）。蓝色圆珠笔箭头画在框外，指向框内对应物件，箭尾配 2–5 个词的手写注释。"
    )
    L.append("")
    L.append("场景（九格完全相同，不得变化）：")
    L.append(f"  {_zh(db, world, 'space')}")
    L.append(f"屏幕视轴（不得镜像）：{_zh(db, world, 'axis')}")
    L.append(f"比例：{_zh(db, world, 'scale')}")
    L.append(f"光线（九格相同）：{_zh(db, world, 'light')}")
    L.append("")
    L.append(PIXAR_RENDER_ZH)
    L.append("")
    L.append("角色（九格完全相同，逐字照抄）：")
    for ch in db.get("characters", []):
        L.append(f"  {ch.get('name_zh', ch['id'])}：{_zh(db, ch, 'lock')}")
    L.append(PIXAR_DESIGN_ZH)
    L.append("")
    L.append("道具（画面中只允许出现以下物件，不得自行添加）：")
    for p in db.get("props", []):
        L.append(f"  - {_zh(db, p, 'lock')}")
    L.append("")
    L.append("九格内容")
    L.append("对白写成框外的短手写行，每格最多两句，绝不写进画面内部。")
    by_id = {p["id"]: p for p in db.get("props", [])}
    for shot in db["shots"]:
        framing = FRAMING_ZH[shot["framing"].upper()]
        bits = [f"{shot['n']:02d} {framing}：{_zh(db, shot, 'action')}"]
        if shot.get("props"):
            bits.append("出现：" + "、".join(by_id[i].get("name_zh", i) for i in shot["props"]))
        if shot.get("state"):
            bits.append(
                "道具状态："
                + "，".join(
                    f"{by_id[k].get('name_zh', k)}={v.replace('_', ' ')}"
                    for k, v in shot["state"].items()
                    if k in by_id
                )
            )
        if shot.get("arrow_zh") or shot.get("arrow_en"):
            bits.append(f"蓝箭头注释「{shot.get('arrow_zh') or shot.get('arrow_en')}」")
        if shot.get("dialogue"):
            bits.append(
                "对白 "
                + " / ".join(
                    f"{next((c.get('name_zh', d['who']) for c in db['characters'] if c['id'] == d['who']), d['who'])}：\"{d['line_en']}\""
                    for d in shot["dialogue"]
                )
            )
        L.append("  " + "；".join(bits))
    L.append("")
    L.append('右侧三分之一 —— 手写大写标题「角色设计与选角」')
    L.append(
        "竖排两条角色条目，每条包含：大字手写角色名、三个短特征标签、左侧铅笔素描、右侧皮克斯风 3D 肖像、下方两行手写图注。"
    )
    for ch in db.get("characters", []):
        L.append("")
        L.append(f"  {ch.get('name_zh', ch['id'])}")
        if ch.get("traits_zh"):
            L.append(f"    特征：{ch['traits_zh']}")
        if ch.get("sketch_zh"):
            L.append(f"    铅笔素描：{ch['sketch_zh']}")
        pose = ch.get("render_pose_zh", "四分之三侧身自然站姿")
        L.append(
            f"    3D 肖像：皮克斯风格 3D 角色渲染，{_zh(db, ch, 'lock')}。姿态：{pose}。"
            + PIXAR_DESIGN_ZH
            + "单根毛丝只在一侧承接轮廓光，夸张的大眼睛带湿润高光且高光位于主光侧，"
            "四分之三视角，浅景深，左上方暖色主光，背后冷色轮廓光，中性暖灰影棚背景，"
            "高光滚降不切白，暗部抬黑不死黑，高端动画角色设定渲染，8k。"
        )
        cap = ch.get("caption_zh") or ch.get("caption_lines")
        if cap:
            L.append("    图注（两行，手写小字）：" + " / ".join(cap))
    villain = db.get("villain")
    if villain:
        L.append("")
        L.append("  反派/道具设计（小栏，约占右栏下方四分之一）")
        L.append(f"    铅笔小图：{villain.get('sketch_zh', '快速松散草图')}")
        L.append(f"    3D 小图：{_zh(db, villain, 'lock')}，干净影棚渲染，柔和主光，中性灰背景")
        cap = villain.get("caption_zh") or villain.get("caption_lines")
        if cap:
            L.append("    图注（两行）：" + " / ".join(cap))
    L.append("")
    L.append("底部 —— 三个手绘方框，边框手绘横线")
    L.append(f"  方框一「笔记/流程意图」：{_zh(db, db['notes'], 'flow')}")
    L.append(f"  方框二「镜头/故事笔记」：{_zh(db, db['notes'], 'camera')}")
    L.append(
        "  方框三「色彩调色板（环境氛围）」："
        + "、".join(sw.get("name_zh", sw["id"]) for sw in db["palette"])
        + f" 共 {len(db['palette'])} 个色块，铅笔/蜡笔交叉阴影风格"
    )
    L.append("")
    L.append("色板 —— 全页只允许出现这些颜色：")
    for sw in db["palette"]:
        L.append(f"  {sw['hex']} — {sw.get('name_zh', sw['id'])} — {_zh(db, sw, 'use')}")
    L.append("  页面中性色（不计入色板）：纸白、石墨灰、红墨 #C0392B、蓝墨 #2F4C8A")
    L.append("")
    L.append(
        "风格：真实的电影前期制作文档，画的是皮克斯风 3D 长片。松而肯定的石墨速写，可见的辅助线与蹭开的排线，"
        "细而略抖的红框，利落的蓝色箭头，手写大写笔记，右栏贴入两张精细的 3D 角色渲染。"
        "干净白纸，极轻的纸纤维纹理。不要扁平数字感、不要矢量感、不要霓虹、不要重渐变。"
    )
    L.append("")
    L.append(
        "负面提示：超过九格、空分镜、第十格、照片级真人、多余角色、额外角色造型、"
        "塑料玩具光泽、霓虹轮廓光、渐变背景、成段文字、乱码字、粗彩色边框、投影、水印、签名、"
        + PIXAR_NEG_ZH
    )
    L.append("")
    L.append("一致性规则（最高优先级，与任何描述冲突时以此为准）：")
    L.append("  1. 九格共用同一个世界、同一束光、同一视轴、同一色板。")
    L.append("  2. 任何道具都不得换色、换形、换称呼。")
    L.append("  3. 不得添加道具清单以外的物件。")
    L.append("  4. 正好九格，不许有第十格，不许留空。")
    L.append("  5. 皮克斯的渲染语言与设计语言，九格与两张肖像全程成立。")
    return "\n".join(L)


# --------------------------------------------------------------------------- cells


def render_cell(db: dict, shot: dict, lang: str) -> str:
    by_id = {p["id"]: p for p in db.get("props", [])}
    world = db["world"]
    framing = FRAMING_EN[shot["framing"].upper()]
    props = [f"{by_id[i].get('name_en', i)} — {(shot.get('state') or {}).get(i, 'as described')}" for i in shot.get("props") or []]
    if lang == "zh":
        L = [
            f"单张分镜，{db['meta'].get('aspect', '16:9')}，呈现在白色制作稿纸上，仍保留细红线手绘外框。",
            f"镜号「{shot['n']:02d}」与镜别「{FRAMING_ZH[shot['framing'].upper()]}」手写在框外左下角，下方一行短动作说明。",
            "",
            f"画面内容：{_zh(db, shot, 'action')}",
            "角色（逐字照抄）：" + "；".join(_zh(db, c, 'lock') for c in db["characters"]),
            "画面内道具：" + "；".join(props) if props else "画面内道具：无",
            f"场景：{_zh(db, world, 'space')}",
            f"比例：{_zh(db, world, 'scale')}",
            f"光线：{_zh(db, world, 'light')}",
            f"机位：{shot.get('camera_zh') or '低机位，接近台面边缘高度，广角略变形以夸张台面体量'}",
            "",
            "风格：松散石墨铅笔，可见排线，一处彩色铅笔强调色，电影感构图，先读剪影再读细节。"
            "这一格描述的是皮克斯风 3D 电影画面：风格化写实，眼高约占脸高三分之一，单侧轮廓光，"
            "阴影带天光色，暗部抬黑不死黑，35mm 浅景深。",
            "色板：" + "、".join(f"{s['hex']} {s.get('name_zh', s['id'])}" for s in db["palette"]),
            "负面提示：成段文字、签名、多余肢体、错误毛色花纹、丢失红框、"
            + PIXAR_NEG_ZH,
        ]
    else:
        L = [
            f"Single storyboard panel, {db['meta'].get('aspect', '16:9')}, presented on white production "
            "paper with the thin hand-drawn red ink frame still visible.",
            f'Shot number "{shot["n"]:02d}" and framing label "{framing.upper()}" handwritten OUTSIDE '
            "the frame at lower left, one short action note underneath.",
            "",
            f"SUBJECT: {shot['action_en'].strip()}",
            "CHARACTERS: " + " | ".join(c["lock_en"].strip() for c in db["characters"]),
            "PROPS IN FRAME: " + ("; ".join(props) if props else "none"),
            f"SETTING: {world['space_en']}",
            f"SCALE: {world['scale_en']}",
            f"LIGHT: {world['light_en']}",
            f"CAMERA: {shot.get('camera_en') or 'low angle at counter-edge height, wide lens, slight distortion to exaggerate the counter mass'}",
            "",
            "STYLE: loose graphite pencil with visible hatching, one accent color blocked in with "
            "colored pencil, cinematic composition, readable silhouette first. This frame describes "
            "a Pixar-style 3D film frame: stylized realism, eyes about one third of the face height, "
            "one-sided rim light, shadows tinted toward the sky colour, lifted blacks, 35mm shallow "
            "depth of field.",
            "PALETTE: " + ", ".join(f"{s['hex']} {s.get('name_en', s['id'])}" for s in db["palette"]),
            "NEGATIVE: text paragraphs, signature, extra limbs, wrong fur pattern, missing red frame, "
            "plastic sheen, rim light on both sides, crushed blacks, photoreal uncanny human",
        ]
    return "\n".join(L)


# --------------------------------------------------------------------------- continuity


def continuity_table(db: dict) -> str:
    props = db.get("props", [])
    head = ["| 格 | 镜别 | " + " | ".join(p.get("name_zh", p["id"]) for p in props) + " |"]
    sep = ["| --- | --- | " + " | ".join("---" for _ in props) + " |"]
    rows = []
    for shot in db["shots"]:
        states = shot.get("state") or {}
        cells = [states.get(p["id"], "—") for p in props]
        rows.append(
            f"| {shot['n']:02d} | {FRAMING_ZH[shot['framing'].upper()]} | " + " | ".join(cells) + " |"
        )
    return "\n".join(
        ["# 道具状态链台账", "", "由 assemble.py 生成，用于核对道具是否跳帧。", ""]
        + head
        + sep
        + rows
    ) + "\n"


# --------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(
        description="把 storyboard.json 拼成一段可直接粘贴的分镜页提示词（默认只写一份 prompt.md）"
    )
    ap.add_argument("source", help="storyboard.json 路径")
    ap.add_argument(
        "-o",
        "--out",
        default=None,
        help="输出位置：默认 ./prompt.md；给目录则写 <目录>/prompt.md；仅 --full 时视为输出目录",
    )
    ap.add_argument("--stdout", action="store_true", help="直接打印到终端，不落盘（推荐）")
    ap.add_argument("--en-only", action="store_true", help="只输出英文段（默认英文 + 中文两段）")
    ap.add_argument("--zh", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument(
        "--full",
        action="store_true",
        help="导出拆分包：中英分文件 + 台账 + 单格稿（仅用户点名要时）",
    )
    ap.add_argument("--no-cells", action="store_true", help="--full 时不生成单格放大稿")
    ap.add_argument("--check-only", action="store_true", help="只做校验，不写文件")
    args = ap.parse_args()

    db = load(Path(args.source))
    validate(db)

    for w in WARNS:
        print(f"[WARN] {w}")
    for e in ERRORS:
        print(f"[ERROR] {e}")

    if ERRORS:
        print(f"\n{len(ERRORS)} 个错误，未生成提示词。先修 Bible 再跑。")
        return 2

    summary = (
        f"9 格 / {len(db['characters'])} 角色 / "
        f"{len(db['props'])} 道具 / {len(db['palette'])} 色"
    )
    if args.check_only:
        print(f"[OK] 校验通过：{summary}")
        return 0

    if args.full:
        return _write_bundle(db, args, summary)

    body = render_en(db)
    if not args.en_only:
        body += "\n\n---\n\n" + render_zh(db)

    if args.stdout:
        print(body)
        if WARNS:
            print(f"\n[{len(WARNS)} 条提醒] {summary}（未落盘）", file=sys.stderr)
        else:
            print(f"\n[OK] {summary}（未落盘）", file=sys.stderr)
        return 0

    target = Path(args.out) if args.out else Path("prompt.md")
    if target.is_dir() or not target.suffix:
        target = target / "prompt.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    print(f"[OK] {summary} → {target}")
    if WARNS:
        print(f"     {len(WARNS)} 条提醒，建议看一眼")
    return 0


def _write_bundle(db: dict, args, summary: str) -> int:
    """拆分包：仅在用户明确要台账 / 单格稿 / 中英分文件时使用。"""
    out = Path(args.out or "out")
    out.mkdir(parents=True, exist_ok=True)
    (out / "sheet-prompt.en.md").write_text(render_en(db), encoding="utf-8")
    (out / "sheet-prompt.zh.md").write_text(render_zh(db), encoding="utf-8")
    (out / "continuity-table.md").write_text(continuity_table(db), encoding="utf-8")
    if not args.no_cells:
        for shot in db["shots"]:
            (out / f"cell-{shot['n']:02d}.en.md").write_text(
                render_cell(db, shot, "en"), encoding="utf-8"
            )

    print(f"[OK] {summary}")
    print(f"     写入 {out.resolve()}（拆分包）")
    print("     sheet-prompt.en.md  粘贴给模型的英文提示词")
    print("     sheet-prompt.zh.md  中文版（国内模型 / 给人审校）")
    print("     continuity-table.md 道具状态链台账")
    if not args.no_cells:
        print("     cell-01..09.en.md   单格放大稿（关键帧高清）")
    if WARNS:
        print(f"     {len(WARNS)} 条提醒，建议看一眼")
    return 0


if __name__ == "__main__":
    sys.exit(main())
