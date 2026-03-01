Upscaling with MangaJaNai and Collab
====================================

Go to <https://colab.research.google.com/> and open a new notebook (and close the release notes panel if shown).

Change the notebook name from `Untitled0.ipynb` to `upscaling.ipynb`.

Click the _Files_ icon in the left-hand gutter to open a view on the files in the current project (for some reason, new projects automatically have a `sample_data` subdirectory).

Add this to the first cell and run it:

```
# @title 1. Install Dependencies
!pip install spandrel Pillow torch
!mkdir -p /content/input /content/output /content/models
```

In the _Files_ view, you'll see `input` etc.

Drag your input images into the `input` folder (I tried the _Upload to session storage_ button but it can only upload to the root folder and could only handle single files, according to Gemini it's _notoriously_ broken).

Note: any files uploaded like this will disappear once your session ends - a more durable solution is to mount Google Drive folders in your workspace.

At the time of writing the 3.0.0 release was the latest MangaJaNai [release](https://github.com/the-database/MangaJaNai/releases).

.onnx vs .safetensor
--------------------

The models are available in `.safetensor` and `.onnx` versions. Initially, I chose the `.onnx` downloads but couldn't get them to work. The MangaJaNai models use IR version 12, when I tried using the latest `onnxruntime-gpu`, 1.24.2 at the time of writing, I got the error:

```
Fail: [ONNXRuntimeError] : 1 : FAIL : Exception during initialization: /onnxruntime_src/onnxruntime/core/optimizer/transformer_memcpy.cc:253 bool onnxruntime::TransformerMemcpyImpl::IsNodeCompatibleWithProvider(const onnxruntime::Node&) const !node_provider_type.empty() was false. Provider type for GlobalAveragePool node with name '/layers.0/residual_group/blocks.0/conv_block/cab/cab.3/attention/attention.0/GlobalAveragePool' is not set.
```

I tried all the suggested solutions I could find but couldn't resolve this. The final suggestion, I tried, was to downgrade the `onnxruntime-gpu` version but this simply resulted in:

```
Unsupported model IR version: 12, max supported IR version: 10
```

I.e. the models used a later IR version than supporte by the downgraded `onnxruntime-gpu` version.

So I was forced to use the `.safetensor` downloads. Unfortunately, these are a bit slower (up to 25% worse, apparently) but more importantly use more GPU RAM.

Choosing the models
-------------------

I chose the _detail_ and _denoise_ `.safetensors` downloads:

* `IllustrationJaNai_V3detail.zip`
* `IllustrationJaNai_V3denoise.zip`

I extracted them and dragged the best models from each (see the associated release notes for details) into my Collab models folder:

* `4x_IllustrationJaNai_V3detail_HAT_L_28k_bf16.safetensors`
* `4x_IllustrationJaNai_V3detail_DAT2_28k_bf16.safetensors`
* `4x_IllustrationJaNai_V3denoise_DAT2_27k_bf16.safetensors`

Click the _+ Code_ to add another code cell and add:

```
# @title 2. Select Model
#model_file = "4x_IllustrationJaNai_V3detail_HAT_L_28k_bf16.safetensors"
model_file = "4x_IllustrationJaNai_V3detail_DAT2_28k_bf16.safetensors"
#model_file = "4x_IllustrationJaNai_V3denoise_DAT2_27k_bf16.safetensors"
#model_file = "4x_IllustrationJaNai_V3detail_FDAT_XL_27k_bf16.safetensors"
#model_file = "4x_IllustrationJaNai_V3denoise_FDAT_XL_32k_bf16.safetensors"
```

And run the cell. Add another cell with:

```
# @title 3. Check CUDA and maximize available RAM
if not torch.cuda.is_available():
    raise RuntimeError("CUDA is not available")

import gc
import torch
gc.collect()
torch.cuda.empty_cache()
```

The garbage collection and emptying of the CUDA cache are probably unnecessary black-magic steps that don't actually make anymore RAM or GPU RAM available. But I just liked to do it each time after changing the model selected in the previous cell.

When you run this cell, it'll fail on the CUDA check.

Go to the _Runtime_ menu and select _Change runtime type_. I chose the _T4 GPU_. This terminates your current session and throws away all the files you uploaded - hence Google Drive being a better long term solution.

If you're using the free tier, the only available suitable option is the _T4 GPU_. In the paid tier, the _A100_ and the even more powerful _H100_ are available. While raw power isn't really important here the of GPU memory is. The T4 has only 16GiB of GPU RAM (compared with 80GiB for the H100).

Note: the code below does _not_ attempt to do tiling, it either upscales the whole image or fails - this is what we want, tiling often introduces terrible discontinuities.

**Update:** when using `.safetensors`, the _T4_ didn't have enough GPU RAM to handle my images, so I purchased a [100 compute units](https://colab.research.google.com/signup) for EUR 10 and switched to the _A100 GPU_. But even the 40GiB of the _A100 GPU_ wasn't enough so I switched to the _H100 GPU_ and its 80GiB.

**IMPORTANT:** when finished, go to the _Runtime_ and select _Disconnect and delete runtime_ to stop consuming credits.

After restarting my session with a GPU, I had to rerun the first cell again, upload my input images again and my models, and run the remaining cells again.

Upscaling
---------

Now, add annother cell with:

```
# @title 4. Run Upscaling
import torch
import numpy as np
from PIL import Image
from spandrel import ModelLoader
from pathlib import Path

# Setup
device = torch.device("cuda")
print(f"model: {model_file}")
model_path = f"/content/models/{model_file}"
input_dir = Path("/content/input")
output_dir = Path("/content/output")

# Load Model
loader = ModelLoader()
model = loader.load_from_file(model_path).to(device).eval()

print(f"Processing images from {input_dir}...")

for img_path in input_dir.glob("*"):
    if img_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
        # Load image
        img = Image.open(img_path).convert("RGB")
        img_tensor = torch.from_numpy(np.array(img)).permute(2, 0, 1).float().divide(255).unsqueeze(0).to(device)

        # Upscale
        with torch.no_grad():
            output_tensor = model(img_tensor)

        # Save output
        output_img = output_tensor.squeeze(0).permute(1, 2, 0).clamp(0, 1).cpu().numpy()
        output_img = (output_img * 255).astype(np.uint8)
        Image.fromarray(output_img).save(output_dir / f"{img_path.stem}.png")
        print(f"Finished: {img_path.name}")

print("Done! Check the /content/output folder.")
```

Even with the _H100 GPU_, the best _detail_ model (4x HAT L) didn't have enough GPU RAM to run (my input images were 1303x2048). But the 4x DAT2 models ran. The release notes for the models suggests the 4x FDAT XL models should run considerably quicker than the higher quality 4x DAT2 models, but I didn't find this to be the case:

* `4x_IllustrationJaNai_V3detail_DAT2_28k_bf16.safetensors` - 60s for two images.
* `4x_IllustrationJaNai_V3denoise_DAT2_27k_bf16.safetensors` - 60s for two images.
* `4x_IllustrationJaNai_V3detail_FDAT_XL_27k_bf16.safetensors` - 54s for two images.
* `4x_IllustrationJaNai_V3denoise_FDAT_XL_32k_bf16.safetensors` - 53s for two images.

Note: even if one could get the `.onnx` models to work, I don't think it would be a game changer. My impression is that they would run maybe 25% faster and consume maybe 25% less GPU RAM.

Results
-------

I downscaled the images to be just double the original size and encoded the as AVIFs with:

```
$ for png in $(find . -name '*.png')
do
    avif=${png%.png}.avif
    magick $png -colorspace RGB -distort Resize 50% -colorspace sRGB -define heic:chroma=444 -define heic:speed=3 -quality 65 $avif
    echo $avif
done
```

Here are the results - to my eye, there's very little difference between the various models:

| &nbsp; | First image | Second image |
|--------|-------------|--------------|
| Originals | ![`originals/i-0008.jpg`](collab/originals/i-0008.jpg) | ![`originals/i-0029.jpg`](collab/originals/i-0029.jpg) |
| Detail 4x DAT2 | <img src="collab/detail-4x-DAT2/i-0008.avif" width="1303" height="2048"> | <img src="collab/detail-4x-DAT2/i-0029.avif" width="1303" height="2048"> |
| Denoise 4x DAT2 | <img src="collab/denoise-4x-DAT2/i-0008.avif" width="1303" height="2048"> | <img src="collab/denoise-4x-DAT2/i-0029.avif" width="1303" height="2048"> |
| Detail 4x FDAT XL | <img src="collab/detail-4x-FDAT-XL/i-0008.avif" width="1303" height="2048"> | <img src="collab/detail-4x-FDAT-XL/i-0029.avif" width="1303" height="2048"> |
| Denoise 4x FDAT XL | <img src="collab/denoise-4x-FDAT-XL/i-0008.avif" width="1303" height="2048"> | <img src="collab/denoise-4x-FDAT-XL/i-0029.avif" width="1303" height="2048"> |

Compared to the Upscayl results, the output images are far truer to the originals. I liked the way Upscayl tried to reverse the effects of halftoning but given its other issues (introducing blurring and splotches) being truer to the originals wins out. Basically, MangaJaNai gets rid of the JPEG artifacts and reduces bluriness but leaves everything else as is:

| Original image | MangaJaNai image |
|----------------|------------------|
| <img width="900" height="1106" src="collab/compare-original.png"> | <img src="collab/compare-detail-4x-dat2.png"> |

Compare e.g. the strokes on Frieren's boots, the artifacts around the text and the clarity of the text and the rest of the image.
