"""Detect and trim scanner-bed band artifacts from book page scans.

Approach: for each of the four edges, scan inward and find the first column/row
where the pixels are "consistently page-bright" for RUN_LENGTH consecutive
pixels. Do this once per scanline, giving a (possibly skewed) edge profile.
Take a conservative crop at the innermost band end (with a small safety margin).

Outputs (under out/):
  page-NNN_cropped.jpg  - the trimmed image
  page-NNN_annot.png    - downsampled overview with detected band line + crop rect
"""

import sys
import cv2
import numpy as np
from pathlib import Path

# --- tunables ---
MAX_SEARCH = 60          # search up to this many px from each edge (band depth ceiling)
DARK_DELTA = 60          # pixel is "band-dark" if (bg - pixel) >= this
SAFETY_MARGIN = 4        # extra px to trim into the page beyond detected band
DARK_FRAC_THRESH = 0.15  # depth is "band" if at least this fraction of pixels are dark
N_CHUNKS = 8             # split each edge into this many chunks along the edge (skew handling)

OUT_DIR = Path("out")


def estimate_bg(gray: np.ndarray) -> int:
    """Estimate page-background brightness from the center 50% of the image."""
    h, w = gray.shape
    center = gray[h // 4 : 3 * h // 4, w // 4 : 3 * w // 4]
    return int(np.percentile(center, 95))


def edge_strip(gray: np.ndarray, edge: str) -> np.ndarray:
    """Return a strip oriented with depth=0 at the boundary and shape (n_scanlines, MAX_SEARCH).
    n_scanlines runs along the edge direction.
    """
    h, w = gray.shape
    if edge == "left":
        return gray[:, :MAX_SEARCH]
    if edge == "right":
        return gray[:, w - MAX_SEARCH :][:, ::-1]
    if edge == "top":
        return gray[:MAX_SEARCH, :].T
    if edge == "bottom":
        return gray[h - MAX_SEARCH :, :][::-1, :].T
    raise ValueError(edge)


def band_depth(strip: np.ndarray, dark_thresh: int) -> int:
    """Find the band-end depth = 1 past the deepest depth whose per-depth dark
    fraction is above DARK_FRAC_THRESH. (Bands are not necessarily contiguous
    from the boundary — a white gap can sit between the edge and the band.)
    Returns 0 if no band-dark depth found.
    """
    dark_frac = (strip <= dark_thresh).mean(axis=0)
    band = np.where(dark_frac >= DARK_FRAC_THRESH)[0]
    return int(band[-1]) + 1 if band.size else 0


def edge_inset(gray: np.ndarray, edge: str, dark_thresh: int) -> tuple[int, bool]:
    """Compute the conservative band depth for one edge, handling skew via chunking.

    Returns (depth, bailed). bailed=True means the band appears to extend past the
    search depth on this edge — likely a decorative page-design border rather than
    a scanner band — so we return depth=0 and leave that edge alone.
    """
    strip = edge_strip(gray, edge)
    chunks = np.array_split(strip, N_CHUNKS, axis=0)
    depths = [band_depth(c, dark_thresh) for c in chunks]
    if any(d >= MAX_SEARCH for d in depths):
        return 0, True
    return max(depths), False


def crop_box(gray: np.ndarray):
    """Return (x0, y0, x1, y1, insets, bailed_edges, bg)."""
    h, w = gray.shape
    bg = estimate_bg(gray)
    dark_thresh = max(0, bg - DARK_DELTA)

    inset_left, bail_l = edge_inset(gray, "left", dark_thresh)
    inset_right, bail_r = edge_inset(gray, "right", dark_thresh)
    inset_top, bail_t = edge_inset(gray, "top", dark_thresh)
    inset_bottom, bail_b = edge_inset(gray, "bottom", dark_thresh)

    x0 = min(inset_left + SAFETY_MARGIN, w // 2)
    y0 = min(inset_top + SAFETY_MARGIN, h // 2)
    x1 = max(w - inset_right - SAFETY_MARGIN, w // 2)
    y1 = max(h - inset_bottom - SAFETY_MARGIN, h // 2)

    insets = (inset_left, inset_right, inset_top, inset_bottom)
    bailed = (bail_l, bail_r, bail_t, bail_b)
    return x0, y0, x1, y1, insets, bailed, bg


def annotate(img: np.ndarray, box, insets, bailed) -> np.ndarray:
    """Draw the detected crop box on a downsampled preview."""
    h, w = img.shape[:2]
    scale = 1000 / max(h, w)
    preview = cv2.resize(img, (int(w * scale), int(h * scale)))
    x0, y0, x1, y1 = box
    p = lambda v: int(v * scale)
    cv2.rectangle(preview, (p(x0), p(y0)), (p(x1), p(y1)), (0, 0, 255), 2)

    def fmt(name, inset, bailed_flag):
        return f"{name}={'BAIL' if bailed_flag else inset}"

    inset_left, inset_right, inset_top, inset_bottom = insets
    bail_l, bail_r, bail_t, bail_b = bailed
    text = (f"{fmt('L', inset_left, bail_l)} {fmt('R', inset_right, bail_r)} "
            f"{fmt('T', inset_top, bail_t)} {fmt('B', inset_bottom, bail_b)}")
    cv2.putText(preview, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return preview


def process(path: Path) -> None:
    img = cv2.imread(str(path))
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x0, y0, x1, y1, insets, bailed, bg = crop_box(gray)
    page_bailed = any(bailed)

    OUT_DIR.mkdir(exist_ok=True)
    stem = path.stem

    if page_bailed:
        # Don't crop — pass through unchanged (no re-encode) but write annotation showing bails.
        cv2.imwrite(str(OUT_DIR / f"{stem}.png"), img)
        cv2.imwrite(str(OUT_DIR / f"{stem}_annot.png"),
                    annotate(img, (0, 0, w, h), insets, bailed))
    else:
        cropped = img[y0:y1, x0:x1]
        cv2.imwrite(str(OUT_DIR / f"{stem}.png"), cropped)
        cv2.imwrite(str(OUT_DIR / f"{stem}_annot.png"),
                    annotate(img, (x0, y0, x1, y1), insets, bailed))

    def show(name, inset, bailed_flag):
        return f"{name}={'BAIL' if bailed_flag else inset}"

    inset_left, inset_right, inset_top, inset_bottom = insets
    bail_l, bail_r, bail_t, bail_b = bailed
    out_w, out_h = (w, h) if page_bailed else (x1 - x0, y1 - y0)
    tag = " [BAILED: passed through unchanged]" if page_bailed else ""
    print(f"{path.stem}: bg={bg} {show('L', inset_left, bail_l)} {show('R', inset_right, bail_r)} "
          f"{show('T', inset_top, bail_t)} {show('B', inset_bottom, bail_b)} "
          f"-> {out_w}x{out_h}{tag}")


if __name__ == "__main__":
    targets = sys.argv[1:] or ["page-007.jpg", "page-069.jpg"]
    for t in targets:
        process(Path(t))
