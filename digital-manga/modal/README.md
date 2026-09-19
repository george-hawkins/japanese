Upscaling manga pages on Modal
==============================

A command-line replacement for the Colab upscaling notebook. The GPU work runs
on [Modal](https://modal.com), but you drive it from a local shell and the
results land directly on your local disk.

Whole-image inference only. There is no tiling, so the output is seamless by
construction.

Setup
-----

Requires [uv](https://docs.astral.sh/uv/). Everything runs on Python 3.14
locally; the Modal container uses Python 3.12 because that is what the CUDA
PyTorch wheels are pinned against.

```
$ uv sync
$ uv run modal setup     # one-time browser login, writes ~/.modal.toml
```

Usage
-----

```
$ uv run modal run upscale.py \
    --model ~/Downloads/IllustrationJaNai_V3detail/4x_IllustrationJaNai_V3detail_FDAT_XL_27k_bf16.safetensors \
    --input ./input \
    --output ./output
```

Options:

| Flag | Default | Notes |
|------|---------|-------|
| `--gpu` | `H100` | Any Modal GPU id: `A100-40GB`, `A100-80GB`, `RTX-PRO-6000` (96 GB), `H200`, `B200`, ... |
| `--dtype` | `bf16` | `fp32` for bit-for-bit parity with the old notebook, `fp16` is supported but risks overflow |
| `--workers` | `1` | Number of GPU containers running in parallel |
| `--overwrite` | off | Re-process images that already have an output file |

The first run builds the container image (a few minutes, cached afterwards)
and uploads the model into a persistent Modal Volume called `upscale-models`
(once per model file, matched on name and size).

Each finished page is written to `--output` as soon as it comes back, so an
interrupted run loses at most the pages in flight. Running the same command
again skips pages that already have output and picks up where it left off.

Grayscale pages produce grayscale (`L`) PNGs, colour pages produce RGB PNGs.
Detection is by content, not file mode: many manga JPEGs are stored as RGB
with identical channels. Collapsing those to `L` cuts file size by two thirds
and drops the slight colour fringing the model otherwise adds to line art.

Cost
----

Billing is per second while a container is alive. Containers shut down about
30 seconds after the last page finishes. Check current prices at
<https://modal.com/pricing>.

Measured on a 1303x2048 page with the 4x FDAT XL detail model
(September 2026 prices):

| GPU | dtype | s/page | peak VRAM | approx. cost/page |
|-----|-------|--------|-----------|-------------------|
| A100-40GB | fp32 | 42.5 | 25.7 GiB | $0.025 |
| A100-40GB | bf16 | 18.1 | 12.8 GiB | $0.011 |
| RTX-PRO-6000 | bf16 | 13.4 | 12.8 GiB | $0.011 |
| H100 | bf16 | 9.6 | 12.9 GiB | $0.011 |

A100 and H100 cost the same per page, so H100 is the default: a 200-page
volume is about 35 minutes of GPU time, or roughly $2. Use `--workers N` to
split that wall-clock time across N GPUs at the same total cost.

bf16 halves VRAM use and cuts GPU time by more than half compared with fp32.
The `.safetensors` file stores fp32 weights despite the `bf16` in its name;
that refers to the training precision. On the synthetic test page, bf16 and
fp32 output differ by a mean of 0.04 levels, with 0.4% of pixels differing by
more than one level, all along stroke edges; that is about the same as the
difference between two GPU models running the same bf16 model. Visually they
are indistinguishable. Use `--dtype fp32` and `compare.py` if you want to
check on your own pages.

Comparing outputs
-----------------

```
$ uv run compare.py ./output-fp32 ./output-bf16 --diff-dir ./diffs
```

Prints max and mean absolute difference, the fraction of pixels differing by
more than one level, and PSNR per page. With `--diff-dir` it writes amplified
difference images so seams or structured differences are obvious by eye.

Downscaling to AVIF
-------------------

```
$ ./to-avif.sh ./output-flying-witch     # writes to ./output-flying-witch-avif
```

Halves the 4x PNGs (Triangle filter) and encodes them as AVIF (quality 65,
4:4:4 chroma, speed 2), about 5 s per page. Output goes to a sibling
directory with `-avif` appended; pages that already have an AVIF there are
skipped, so it resumes.

The resize is deliberately done in sRGB, not linear light. Tested on the
Flying Witch volume 1 cover (the only colour page) and an interior page:
resizing in linear light (`-colorspace RGB ... -colorspace sRGB`) thins dark
strokes on white. In a speech bubble with furigana the share of solid-black
pixels fell by 17%, and the text is visibly lighter side by side. On the
cover it made the white title slightly bolder and the artwork itself was
indistinguishable, so there is no gain to offset the damage to text. AVIF
sizes were within 1% either way.

Packaging as a .cbz
-------------------

Generate a `ComicInfo.xml` with the `comicinfo.py` script from the `manga`
directory, then zip it together with the AVIFs:

```
$ uv run --no-project --python 3.14 ../manga/comicinfo.py \
    --publisher Shogakukan --imprint 'Monthly Shōnen Sunday' \
    'Teasing Master Takagi-san' 1 -o output-teasing-avif/ComicInfo.xml
$ cd output-teasing-avif/
$ zip ../teasing-v1.cbz ComicInfo.xml *.avif
```

Run `comicinfo.py` via `uv` rather than a bare `python3`: the python.org
build of Python that is first on `PATH` has no certificate bundle, so its
HTTPS metadata lookup fails with `CERTIFICATE_VERIFY_FAILED`. The uv-managed
interpreter verifies fine. `--no-project` stops uv from trying to use this
directory's own environment.

Comic readers sort pages by filename rather than archive order, so the order
in which `zip` adds the files does not matter.

Test page
---------

```
$ uv run make_test_page.py     # writes input/test-page.jpg
```

Generates a synthetic 1303x2048 JPEG with panel borders, Japanese text down
to furigana size, a halftone gradient and thin strokes. Useful as a smoke test
without needing real pages in the repo.

Files
-----

* `upscale.py` - the Modal app and CLI entrypoint.
* `to-avif.sh` - halve the PNGs and encode as AVIF into a `-avif` sibling directory.
* `compare.py` - local pixel comparison of two output directories.
* `make_test_page.py` - synthetic test page generator.
* `input/`, `output*/`, `diffs*/` and `*.safetensors` are git-ignored.
