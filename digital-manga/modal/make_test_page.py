"""Generate a synthetic manga-like JPEG page for smoke-testing the pipeline.

    uv run make_test_page.py [--out input/test-page.jpg] [--size 1303x2048]

White page, panel borders, Japanese text at several sizes (including tiny
furigana-sized text), a halftone dot field, and JPEG compression at quality
80 so there are real artifacts to clean up. Uses a macOS system font.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]

TEXT = "葬送のフリーレン 魔法使い 蒼 魔 びぴ ばぱ 千年 勇者ヒンメル"


def font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise SystemExit("no Japanese-capable font found; edit FONT_CANDIDATES")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("input/test-page.jpg"))
    ap.add_argument("--size", default="1303x2048")
    ap.add_argument("--quality", type=int, default=80)
    args = ap.parse_args()
    w, h = (int(v) for v in args.size.lower().split("x"))

    img = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(img)

    # Panel borders.
    m = w // 20
    d.rectangle([m, m, w - m, h // 2 - m // 2], outline=0, width=4)
    d.rectangle([m, h // 2 + m // 2, w // 2 - m // 2, h - m], outline=0, width=4)
    d.rectangle([w // 2 + m // 2, h // 2 + m // 2, w - m, h - m], outline=0, width=4)

    # Text at decreasing sizes, down to furigana scale.
    y = 2 * m
    for size in (72, 48, 32, 24, 18, 14, 11, 9):
        d.text((2 * m, y), TEXT, fill=0, font=font(size))
        y += int(size * 1.6)

    # Halftone dot field with a gradient in dot size.
    top, bottom = h // 2 + 2 * m, h - 2 * m
    left, right = 2 * m, w // 2 - 2 * m
    pitch = 8
    for yy in range(top, bottom, pitch):
        r = 0.5 + 3.0 * (yy - top) / (bottom - top)
        for xx in range(left, right, pitch):
            d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=0)

    # Some diagonal and curved strokes in the last panel.
    x0, y0 = w // 2 + 2 * m, h // 2 + 2 * m
    for i in range(12):
        d.line([x0, y0 + i * 40, w - 2 * m, h - 2 * m - i * 60], fill=0, width=1 + i % 4)
    d.arc([x0, y0, w - 2 * m, h - 2 * m], 200, 340, fill=0, width=3)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.out, quality=args.quality, subsampling=0)
    print(f"wrote {args.out} ({w}x{h}, JPEG q{args.quality})")


if __name__ == "__main__":
    main()
