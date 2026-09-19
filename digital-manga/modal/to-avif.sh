#!/usr/bin/env bash
# Downscale upscaled PNG pages by 50% and encode them as AVIF.
#
#   ./to-avif.sh INPUT_DIR
#
# Output goes to INPUT_DIR-avif (created if needed), one .avif per .png.
# Pages that already have an .avif in the output directory are skipped.
#
# Resizes with the Triangle filter in the image's own (sRGB) colorspace on
# purpose: resizing in linear light thins dark strokes on white, which hurts
# speech-bubble text, and does not visibly help the colour pages either.

set -euo pipefail

if [[ $# -ne 1 || ! -d $1 ]]; then
    echo "usage: $0 INPUT_DIR" >&2
    exit 1
fi

in_dir=${1%/}
out_dir="${in_dir}-avif"
mkdir -p "$out_dir"
echo "writing AVIFs to $out_dir"

shopt -s nullglob
for png in "$in_dir"/*.png; do
    name=$(basename "$png" .png)
    avif="$out_dir/$name.avif"
    if [[ -e $avif ]]; then
        echo "skip $name.avif (exists)"
        continue
    fi
    magick "$png" -filter Triangle -resize 50% \
        -depth 8 -define heic:speed=2 -define heic:chroma=444 -quality 65 -strip \
        "$avif"
    echo "$name.avif"
done
