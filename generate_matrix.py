#!/usr/bin/env python3
import random

WIDTH = 800
HEIGHT = 100
COL_W = 16
ROW_H = 16
COLS = WIDTH // COL_W
ROWS = HEIGHT // ROW_H

PASTEL_GREEN  = "#a8e6a3"
MID_GREEN     = "#6dbf67"
BRIGHT_GREEN  = "#c8f7c5"
BG_COLOR      = "#0d1a0d"

CHARS = list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホ0123456789ABCDEF")

random.seed(42)

def make_col(col_idx):
    x = col_idx * COL_W + COL_W // 2
    delay = round(random.uniform(0, 4), 2)
    duration = round(random.uniform(2.5, 5), 2)
    stream_len = random.randint(4, ROWS)
    start_row = random.randint(0, ROWS - stream_len)

    items = []
    for i in range(stream_len):
        char = random.choice(CHARS)
        y = (start_row + i) * ROW_H + ROW_H
        # head char is brightest
        color = BRIGHT_GREEN if i == stream_len - 1 else (MID_GREEN if i >= stream_len - 3 else PASTEL_GREEN)
        opacity = 1.0 if i == stream_len - 1 else round(0.3 + 0.7 * i / stream_len, 2)
        anim_name = f"fall_{col_idx}"
        items.append(
            f'<text x="{x}" y="{y}" fill="{color}" opacity="{opacity}" '
            f'font-size="13" text-anchor="middle" '
            f'style="animation:{anim_name} {duration}s {delay}s infinite linear">'
            f'{char}</text>'
        )
    return items, anim_name, duration, stream_len

styles = []
texts = []
seen_anims = set()

for c in range(COLS):
    items, anim_name, duration, stream_len = make_col(c)
    texts.extend(items)
    if anim_name not in seen_anims:
        seen_anims.add(anim_name)
        travel = HEIGHT + stream_len * ROW_H
        styles.append(
            f"@keyframes {anim_name} {{"
            f" 0%{{transform:translateY(-{stream_len * ROW_H}px)}}"
            f" 100%{{transform:translateY({HEIGHT}px)}}"
            f"}}"
        )

style_block = "\n    ".join(styles)
text_block = "\n  ".join(texts)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BG_COLOR}"/>
  <style>
    text {{ font-family: 'Courier New', monospace; }}
    {style_block}
  </style>
  {text_block}
</svg>"""

with open("matrix.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated matrix.svg ({len(svg)} bytes, {COLS} columns)")
