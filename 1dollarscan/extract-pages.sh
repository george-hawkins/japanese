#!/usr/bin/env bash
set -euo pipefail

[[ $# -eq 2 ]] || { echo "usage: $0 <pdf> <output-dir>" >&2; exit 1; }
pdf=$1 out=$2

mkdir -p -- "$out"
pdfimages -all -- "$pdf" "$out/page"

# Drop tiny inline-mask artifacts (e.g. 1x1 stencils from Acrobat Paper Capture).
find "$out" -maxdepth 1 -type f -size -1k -delete

# Renumber survivors sequentially as page-001.<ext>, preserving each file's extension.
i=1
for f in "$out"/page-*.*; do
  mv -- "$f" "$out/tmp-$(printf '%04d' "$i").${f##*.}"
  ((i++))
done
i=1
for f in "$out"/tmp-*.*; do
  mv -- "$f" "$out/page-$(printf '%03d' "$i").${f##*.}"
  ((i++))
done
