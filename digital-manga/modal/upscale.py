"""Upscale a directory of images on a Modal GPU with a spandrel-loadable model.

Whole-image inference only (no tiling), so output is seamless by construction.

Usage:

    uv run modal run upscale.py \\
        --model ~/Downloads/IllustrationJaNai_V3detail/4x_IllustrationJaNai_V3detail_FDAT_XL_27k_bf16.safetensors \\
        --input ./input --output ./output

Options:

    --gpu       Modal GPU id: H100 (default), A100-40GB, A100-80GB, RTX-PRO-6000, H200, B200, ...
    --dtype     bf16 (default, ~half the VRAM and GPU time of fp32), fp16, fp32
    --workers   Number of GPU containers to run in parallel (default 1)
    --overwrite Re-process images whose output already exists (default: skip them)

The model file is uploaded once into a persistent Modal Volume and reused on
later runs. Each finished image is written to --output as soon as it arrives,
so an interrupted run loses at most the images in flight; rerunning resumes.
"""

import io
import threading
import time
from pathlib import Path

import modal

APP_NAME = "upscale"
MODELS_VOLUME = "upscale-models"
MODELS_DIR = "/models"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
DTYPES = ("bf16", "fp16", "fp32")

app = modal.App(APP_NAME)
models = modal.Volume.from_name(MODELS_VOLUME, create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "torch==2.10.0",
        "torchvision==0.25.0",
        "spandrel==0.4.2",
        "pillow",
        "numpy",
        extra_index_url="https://download.pytorch.org/whl/cu128",
    )
    # Reduces allocator fragmentation so reserved VRAM tracks allocated VRAM.
    .env({"PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
)


@app.cls(
    image=image,
    volumes={MODELS_DIR: models},
    gpu="H100",  # overridden per run via with_options(gpu=...)
    timeout=60 * 60,
    scaledown_window=30,  # seconds of idle before the container (and billing) stops
)
@modal.concurrent(max_inputs=2)  # lets PNG encoding of image N overlap inference of N+1
class Upscaler:
    model_file: str = modal.parameter()
    dtype: str = modal.parameter(default="bf16")

    @modal.enter()
    def load(self) -> None:
        import torch
        from spandrel import ModelLoader

        if self.dtype not in DTYPES:
            raise ValueError(f"dtype must be one of {DTYPES}, got {self.dtype!r}")
        torch_dtype = {
            "bf16": torch.bfloat16,
            "fp16": torch.float16,
            "fp32": torch.float32,
        }[self.dtype]

        path = Path(MODELS_DIR) / self.model_file
        t0 = time.perf_counter()
        desc = ModelLoader().load_from_file(str(path))
        # spandrel validates dtype support for the architecture here.
        self.desc = desc.to(torch.device("cuda"), torch_dtype).eval()
        self.torch_dtype = torch_dtype
        self.gpu_lock = threading.Lock()  # serialise GPU work so VRAM peak is one image
        gpu = torch.cuda.get_device_properties(0)
        print(
            f"loaded {self.model_file} ({desc.architecture.name}, {desc.scale}x, "
            f"tags={desc.tags}) as {self.dtype} on {gpu.name} "
            f"{gpu.total_memory / 2**30:.0f} GiB in {time.perf_counter() - t0:.1f}s"
        )

    @modal.method()
    def upscale(self, name: str, data: bytes) -> dict:
        import numpy as np
        import torch
        from PIL import Image

        t0 = time.perf_counter()
        src = Image.open(io.BytesIO(data))
        img = src.convert("RGB")
        # Treat as grayscale if the file says so, or if it is an RGB file whose
        # channels are (near) identical, which is how many manga JPEGs are stored.
        grayscale = src.mode in ("1", "L", "LA", "I;16")
        if not grayscale:
            a = np.asarray(img, dtype=np.int16)
            spread = np.abs(a - a.mean(axis=2, keepdims=True)).max()
            grayscale = bool(spread <= 2)

        with self.gpu_lock:
            t1 = time.perf_counter()
            with torch.inference_mode():
                x = (
                    torch.from_numpy(np.array(img))
                    .permute(2, 0, 1)
                    .unsqueeze(0)
                    .to("cuda", self.torch_dtype)
                    .div_(255)
                )
                torch.cuda.synchronize()
                torch.cuda.reset_peak_memory_stats()
                t2 = time.perf_counter()
                # The descriptor handles size padding, no_grad and clamp(0, 1).
                y = self.desc(x)[0].float()  # (3, H, W)
                torch.cuda.synchronize()
                t3 = time.perf_counter()
                peak_alloc = torch.cuda.max_memory_allocated() / 2**30
                peak_reserved = torch.cuda.max_memory_reserved() / 2**30
                if grayscale:
                    # Same luma weights Pillow uses for RGB -> L.
                    w = torch.tensor([0.299, 0.587, 0.114], device=y.device).view(3, 1, 1)
                    y = (y * w).sum(0)  # (H, W)
                else:
                    y = y.permute(1, 2, 0)  # (H, W, 3)
                out = y.mul(255).round().to(torch.uint8).cpu().numpy()
                del x, y

        result = Image.fromarray(out)
        buf = io.BytesIO()
        result.save(buf, format="PNG", compress_level=6)
        t4 = time.perf_counter()

        return {
            "name": name,
            "png": buf.getvalue(),
            "in_size": img.size,
            "out_size": result.size,
            "mode": result.mode,
            "wait_s": t1 - t0,  # time spent queued behind another image on the GPU
            "infer_s": t3 - t2,
            "encode_s": t4 - t3,
            "peak_alloc_gib": peak_alloc,
            "peak_reserved_gib": peak_reserved,
        }


def ensure_model_uploaded(model_path: Path) -> None:
    """Upload the model into the Volume unless a same-sized copy is already there."""
    size = model_path.stat().st_size
    for entry in models.listdir("/"):
        if Path(entry.path).name == model_path.name and entry.size == size:
            print(f"model already in volume {MODELS_VOLUME!r}: {model_path.name}")
            return
    print(f"uploading {model_path.name} ({size / 2**20:.1f} MiB) to volume {MODELS_VOLUME!r}...")
    t0 = time.perf_counter()
    with models.batch_upload(force=True) as batch:
        batch.put_file(str(model_path), f"/{model_path.name}")
    print(f"uploaded in {time.perf_counter() - t0:.1f}s")


@app.local_entrypoint()
def main(
    model: str,
    input: str,
    output: str,
    gpu: str = "H100",
    dtype: str = "bf16",
    workers: int = 1,
    overwrite: bool = False,
) -> None:
    model_path = Path(model).expanduser().resolve()
    in_dir = Path(input).expanduser().resolve()
    out_dir = Path(output).expanduser().resolve()
    if not model_path.is_file():
        raise SystemExit(f"model not found: {model_path}")
    if not in_dir.is_dir():
        raise SystemExit(f"input directory not found: {in_dir}")
    if dtype not in DTYPES:
        raise SystemExit(f"--dtype must be one of {DTYPES}")
    out_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in in_dir.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES)
    todo = [p for p in files if overwrite or not (out_dir / f"{p.stem}.png").exists()]
    skipped = len(files) - len(todo)
    print(f"{len(files)} images in {in_dir}, {skipped} already done, {len(todo)} to process")
    if not todo:
        return

    ensure_model_uploaded(model_path)

    upscaler = Upscaler.with_options(gpu=gpu, max_containers=workers)(
        model_file=model_path.name, dtype=dtype
    )
    print(f"gpu={gpu} dtype={dtype} workers={workers} -> {out_dir}")

    names = [p.name for p in todo]
    datas = [p.read_bytes() for p in todo]
    t0 = time.perf_counter()
    gpu_s = 0.0
    done = 0
    for r in upscaler.upscale.map(names, datas, order_outputs=False):
        dest = out_dir / f"{Path(r['name']).stem}.png"
        dest.write_bytes(r["png"])
        done += 1
        gpu_s += r["infer_s"]
        w, h = r["in_size"]
        ow, oh = r["out_size"]
        print(
            f"[{done}/{len(todo)}] {r['name']}: {w}x{h} -> {ow}x{oh} {r['mode']}, "
            f"infer {r['infer_s']:.2f}s, encode {r['encode_s']:.2f}s, "
            f"peak VRAM {r['peak_alloc_gib']:.1f} GiB allocated "
            f"({r['peak_reserved_gib']:.1f} reserved), {len(r['png']) / 2**20:.1f} MiB"
        )
    wall = time.perf_counter() - t0
    print(f"done: {done} images, {gpu_s:.0f}s of inference, {wall:.0f}s wall clock")
