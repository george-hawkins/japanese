"""Compare two directories of same-named images pixel by pixel.

Useful for checking e.g. bf16 against fp32 output, or a new run against an
old Colab run.

    uv run compare.py DIR_A DIR_B [--diff-dir DIFFS] [--amplify 16]

For each pair it prints the max and mean absolute difference (0-255 scale),
the fraction of pixels that differ by more than 1 (i.e. beyond rounding),
and PSNR. With --diff-dir it also writes an amplified difference image per
pair so any seams or structured differences are easy to spot by eye.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # 4x manga pages exceed Pillow's default bomb check


def load(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.int16)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir_a", type=Path)
    ap.add_argument("dir_b", type=Path)
    ap.add_argument("--diff-dir", type=Path, help="write amplified |A-B| images here")
    ap.add_argument("--amplify", type=int, default=16, help="multiplier for diff images")
    args = ap.parse_args()

    names_a = {p.stem: p for p in args.dir_a.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}}
    names_b = {p.stem: p for p in args.dir_b.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}}
    common = sorted(set(names_a) & set(names_b))
    if not common:
        raise SystemExit("no images with matching names in both directories")
    only_a, only_b = sorted(set(names_a) - set(names_b)), sorted(set(names_b) - set(names_a))
    if only_a:
        print(f"only in {args.dir_a}: {', '.join(only_a)}")
    if only_b:
        print(f"only in {args.dir_b}: {', '.join(only_b)}")
    if args.diff_dir:
        args.diff_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'image':<24} {'max':>4} {'mean':>7} {'>1':>8} {'psnr':>7}")
    worst = 0
    for stem in common:
        a, b = load(names_a[stem]), load(names_b[stem])
        if a.shape != b.shape:
            print(f"{stem:<24} size mismatch {a.shape[1]}x{a.shape[0]} vs {b.shape[1]}x{b.shape[0]}")
            continue
        d = np.abs(a - b)
        mx = int(d.max())
        mean = float(d.mean())
        frac = float((d > 1).mean())
        mse = float((d.astype(np.float64) ** 2).mean())
        psnr = math.inf if mse == 0 else 10 * math.log10(255**2 / mse)
        worst = max(worst, mx)
        print(f"{stem:<24} {mx:>4} {mean:>7.4f} {frac:>8.5f} {psnr:>7.2f}")
        if args.diff_dir:
            amp = np.clip(d.max(axis=2) * args.amplify, 0, 255).astype(np.uint8)
            Image.fromarray(255 - amp).save(args.diff_dir / f"{stem}.png")

    print(f"{len(common)} pairs compared, worst max difference {worst}")


if __name__ == "__main__":
    main()
