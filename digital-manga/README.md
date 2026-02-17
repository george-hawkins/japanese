Upscaling manga
===============

I wanted to take another look at digital manga as a source of learner reading material.

After first looking into this and finding that Amazon release popular manga (e.g. Demon Slayer) at resolutions as low as 150dpi.

At this resolution many denser kanji, e.g. 蒼 (blue) or 魔 (demon), are just a blur of pixels. And forget about making out furigana.

Even at 300dpi, it's impossible to tell [dakuten from handakuten](https://en.wikipedia.org/wiki/Dakuten_and_handakuten) on furigana - they're just a small blur of pixels. So you can't tell furigana び from ぴ.

This is a great shame, especially for manga like [Frieren](https://en.wikipedia.org/wiki/Frieren) where every kanji has furigana - this should be a great resource for learners but just ends up being frustrating as you can clearly distinguish them.

Note: in my cheap &yen;500 Frieren [tankobon](https://en.wikipedia.org/wiki/Tank%C5%8Dbon), printed on plain paper, the furigana and their dakuten and handakuten are extremely clearly printed despite the small page size.

You need about 600dpi before the dakuten and handakuten on furigana are clear at the usual font sizes used in speech bubbles. And even then, it's only super clear it you're using a sensible lossless format like PNG or a modern lossy format like AVIF. Unfortunately, most e-book publishers use JPEG for manga - JPEG is terrible for black and white line art and introduces terrible artifacts.

Finding high-resolution manga
-----------------------------

In my previous search for legal sources of manga material, I'd found the best I could find was about 300dpi.

And when searching for Frieren volume 1, I found it available on no end of e-book publisher stores but none had it at better than 300dpi.

I found it at 300dpi at Kobo with each page encoded with JPEG. I also found it at 300dpi at EbookJapan where they used WEBP. The EbookJapan pages have _slightly_ fewer artifacts than the Kobo `.jpg` files but more than should be present in a `.webp` - I suspect the source for both was a larger JPEG that both scaled down.

You can see a sample pages from Kobo here: [`kobo-1303x2048-a.jpg`](kobo-1303x2048-a.jpg)

The EbookJapan pages are distributed as a scrambled set of tiles, e.g. [`ebookjapan.webp`](ebookjapan.webp).

Just to compare with the first of the Kobo pages, I cut up and rearranged _some_ of the tiles to make [`ebookjapan-tiles.png`](ebookjapan-tiles.png) (the original Gimp file, where each tile is still moveable as a layer is [`ebookjapan-tiles.xcf`](ebookjapan-tiles.xcf)).

If you compare, you can see their both the same DPI but, as noted, there's _slightly_ fewer JPEG style artifacts in the EbookJapan image.

Torrented content
-----------------

I'd heard that high-quality manga rips were often available on torrenting sites.

This sounds reasonable to me - one person finds the highest possible quality digital version available and that rises to the top of any seeding lists.

But, at least on public torrenting sites, like nyaa.si, in early 2026, this does not seem to be the case.

I found many torrents of collections of Frieren volumes or individual volumes with size ranging from around 800MiB to 3.1GiB. But in the end, the best any of them contained were 150dpi versions of volume 1, i.e. not even as good as Kobo (the 3.1GiB monster just contained n slightly different editions of particular volumes but none of them higher than 150dpi).

These are two samples of the highest quality I found on nyaa.si. It's worth zooming in on some of the kanji and seeing how they're little more than a blur.

* [`nyaa-764x1200-a.jpg`](nyaa-764x1200-a.jpg)
* [`nyaa-764x1200-b.jpg`](nyaa-764x1200-b.jpg)

Even though some kanji look like a blur, I was surprised that Preview on Mac could generally detect the right kanji even for characters like 蒼 that just looked like a mess to me. It's OCR software seems to be pretty good.

I found that Anna's Archive had higher quality editions at about 280dpi, i.e. still lower than Kobo. Here are two samples:

* [`annas-archive-1221x1920-a.jpg`](annas-archive-1221x1920-a.jpg)
* [`annas-archive-1221x1920-b.jpg`](annas-archive-1221x1920-b.jpg)

Conclusion: torrenting isn't some magic answer in the search for high quality manga.

Upscaling
---------

Upscaling can't recover dakuten and handakuten that have just become blurs but it can clean up all the JPEG artifact noise and make for much more visually pleasant pages.

I used both [Upscayl](https://github.com/upscayl/upscayl) and [waifu2x](https://github.com/nagadomi/nunif/blob/master/waifu2x/README.md) to upscale the sample Kobo page linked to up above. The results can be seen here:

* [`kobo-1303x2048-a_upscayl_4x_digital-art-4x.png`](kobo-1303x2048-a_upscayl_4x_digital-art-4x.png)
* [`kobo-1303x2048-a_waifu2x-scan-noise_scale4x.png`](kobo-1303x2048-a_waifu2x-scan-noise_scale4x.png)

As you can see, they take very different approaches, `waifu2x` is much more conservative, it cleans and sharpens things up but it preserves the [halftoning](https://en.wikipedia.org/wiki/Halftone). Upscayl (when using the Digital Art model) tries to go much further, look at all the areas that are grids of halftone dots in the `waifu2x` version, in the Upscayl version these become continuous tones or complex combinations of strokes which I think looks really impressive but some people may object to as its the AI guessing, essentially making artistic choices, about what was there before the halftoning occurred.

The models default to 4-times upscaling but this produces huges files. So I then downscaled them by 50% to produce essentially 600dpi pages (but as noted, the dakuten and handakuten are gone forever, replaced by things that look half-way between a dakuten and a handakuten):

* [`half-kobo-1303x2048-a_upscayl_4x_digital-art-4x.png`](half-kobo-1303x2048-a_upscayl_4x_digital-art-4x.png)
* [`half-kobo-1303x2048-a_waifu2x-scan-noise_scale4x.png`](half-kobo-1303x2048-a_waifu2x-scan-noise_scale4x.png)

The PNGs above are fairly large but if can tolerated a little lossiness AVIF produces much smaller files:

* [`half-kobo-1303x2048-a_upscayl_4x_digital-art-4x.avif`](half-kobo-1303x2048-a_upscayl_4x_digital-art-4x.avif)
* [`half-kobo-1303x2048-a_waifu2x-scan-noise_scale4x.avif`](half-kobo-1303x2048-a_waifu2x-scan-noise_scale4x.avif)

The AVIF files are about twice the size of the original Kobo JPEGs but four times the area (twice a tall and twice as wide) and far cleaner looking (with no unpleasant JPEG artifacts).

If only they could have been encoded like this originally before the dakuten and handakuten went the way of the dodo.

### waifu2x upscaling

`waifu2x` was originally released in its own repo [here](https://github.com/nagadomi/waifu2x) but for whatever reason the author has moved many of his projects, including `waifu2x` into a single repo called `nunif` and the latest version can be found in the [`waifu2x` subdirectory](https://github.com/nagadomi/nunif/tree/master/waifu2x) there.

You need to `git clone` the whole `nunif` repo, then `pip install` the dependencies in the [`requirements.txt`](https://github.com/nagadomi/nunif/blob/master/requirements.txt) along with `pytorch`.

Then you need to in the `nunif` directory to run `waifu2x.cli` (i.e. don't go into the `waifu2x` directory or go somewhere else and expect it to run):

```
$ python -m waifu2x.cli --style scan -m noise_scale4x -n 3 -i /path/to/input.jpg -o /path/to/upscaled-output.png
```

I tried various models and parameters and `-m noise_scale4x -n 3` worked best.

Note: I seem to remember that a necessary dependency was still missing after this but forget which, but it was easy enough to track down.

### Upscayl

Upscayl is far simpler - it comes as an app and all I changed in the settings was the _AI Model_ - I switched to _Digital Art_ and just let if upscale 4-times just like the `waifu2x` upscaler.

### MangaJaNai

I'd have liked to the [MangaJaNai models](https://github.com/the-database/mangajanai).

The model releases can be found [here](https://github.com/the-database/MangaJaNai/releases).

In version 1.0.0, they release `IllustrationJaNai` and `MangaJaNai` models but releases 2.0.0 and 3.0.0 just contain `IllustrationJaNai` models. I don't know if this means `MangaJaNai` is considered redundant now or the 1.0.0 version was simply never improved on.

I'd like to try:

* The 4x HAT L model from the 3.0.0 `IllustrationJaNai_V3denoise_onnx.zip` asset (HAT L is the highest quality one and the ONNX versions of the models should be the ones optimized for the lowest resource usage).
* The `4x_MangaJaNai_2048p_V1_ESRGAN_70k.pth` model from the 1.0.0 assets, 4x mean 4-times scaling and 2048p means it's for 2048px tall source images (and that's what the Kobo images used above are).

I couldn't get these models to run locally, I think the way to do it would be to use [Google Colab](https://colab.research.google.com/) and download use the Python backend to the Window-only [MangaJaNaiConverterGui](https://github.com/the-database/MangaJaNaiConverterGui) that has a CLI mode and a nice [README](https://github.com/the-database/MangaJaNaiConverterGui/tree/main/MangaJaNaiConverterGui/backend/src).

And then using [`ai-manga-upscale-colab.ipynb`](https://github.com/Spladenly/ai-manga-upscale-colab/blob/main/ai-manga-upscale-colab.ipynb) as a basis, one could do something similar with the MangaJaNaiConverterGui backend Python.

See how the `.ipynb` notebook has Python code blocks with functions like this:

```
def ai_process_bw():
  !python ESRGAN/upscale.py -se -i /content/gdrive/MyDrive/ESRGAN/bw \
  -o /content/gdrive/MyDrive/ESRGAN/output \
  ESRGAN/models/4x_eula_digimanga_bw_v2_nc1_307k.pth
```

I.e. it's calling out to Python scripts (that are actually on a linked Google Driver folder).

Downscaling
-----------

It's probably ridiculous downscaling after upscaling but the models do have an intended target upscaling factor, generally 4 (however, it seems OK-ish to override this).

Anyway, I downscaled to PNG like this:

```
$ magick kobo-1303x2048-a_upscayl_4x_digital-art-4x.png -colorspace RGB -distort Resize 50% -colorspace sRGB half-kobo-1303x2048-a_upscayl_4x_digital-art-4x.png
$ magick kobo-1303x2048-a_waifu2x-scan-noise_scale4x.png -colorspace RGB -distort Resize 50% -colorspace sRGB half-kobo-1303x2048-a_waifu2x-scan-noise_scale4x.png
```

The colorspace conversion (to `RGB` before scaling and back to `sRGB` after) is supposed to shift the image into a more perceptually uniform space so that when pixels are averaged in this space it produces a more true result.

Aside: I found that with the huge 4x upscaled images, Preview, for whatever reason, doesn't detect text in files this large (either its the file size or the characters themselves are larger than some threshold that Preview uses when searching for text).

Lanczos
-------

The `-distort Resize 50%` was suggested by Gemini, initially I tried using `-filter Lanczos` but this resulted in a weird artifact whereby a pale outline appeared just within the edge of what should have been solid black kanji strokes. This is apparently a known consequence of using Lanczos and is called [Gibbs ringing](https://en.wikipedia.org/wiki/Ringing_artifacts).

AVIF
----

Gemini suggested AVIF as the best modern format for black and white art, if one is prepared to tolerate losiness.

Doing the reduction but outputting as AVIF reduces the size to almost a 10th of the PNG size:

```
$ magick kobo-1303x2048-a_upscayl_4x_digital-art-4x.png -colorspace RGB -distort Resize 50% -colorspace sRGB -define heic:chroma=444 -define heic:speed=3 -quality 65 half-kobo-1303x2048-a_upscayl_4x_digital-art-4x.avif
$ magick kobo-1303x2048-a_waifu2x-scan-noise_scale4x.png -colorspace RGB -distort Resize 50% -colorspace sRGB -define heic:chroma=444 -define heic:speed=3 -quality 65 half-kobo-1303x2048-a_waifu2x-scan-noise_scale4x.avif
```

Gemini said the ImageMagick defaults for AVIF are best suited to color photos, i.e. what you'd have classically used JPEG for, and for black and white it suggested adding:

```
-define heic:chroma=444 -define heic:speed=3 -quality 65
```

### Browser support

All the major browsers now support AVIF with Chrome adding support first in 2020 and MS Edge coming last in 2024:

* Chrome - August 2020 (Version 85).
* Firefox - October 2021 (Version 93).
* Safari - September/October 2022 (iOS 16 and macOS Ventura).
* Edge - January 2024 (Version 121).

Note: Edge is based on the same Chromium engine as Chrome but for whatever reason MS only enabled its AVIF support in 2024 for Edge.
