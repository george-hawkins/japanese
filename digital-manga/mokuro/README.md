Mokuru
======

Mokuro is a solution that OCRs your manga to generate a `.mokuro` file that can be uploaded in a `.zip` file with your images to the Mokuro Reader. In the Reader, you can hover over image text to see that text in a format that can be looked up by tools like [Yomitan](https://github.com/yomidevs/yomitan).

First upscale your images by 2 (or whatever factor is needed to result in images of around size 2606x4096) using Upscayl and its _Digital Art_ _AI Model_ with output format PNG.

On my M2 MacBook Air, it took 2 hours 15 minutes for Upscayl to upscale the 79 pages of the Frieren sample that I had.

Note: there's a meteor shower scene in the Frieren sample just before Himmel's death where he says "綺麗だ". The artifacts introduced by the upscaling are quite dramatic (smudges and a strange gridlike discontinuity in the gradient used in the more open areas of the sky). Similarly, see the bottom-left of the bottom panel on the previous page to this (where Himmel says "ありがとうフリーレン"), something has gone seriously wrong. And on the page previous to that, in the bottom-left panel with the sunlight. These issues are enough to make me consider trying another upscaling algorithm (see MangaJaNai and `waifu2x` mentioned [here](../README.md)).

Once I'd generated the PNGs, I converted them to AVIFs:

```
$ magick mogrify -format avif -define heic:chroma=444 -define heic:speed=3 -quality 65 *.png
```

This took 12 minutes, i.e. it's not exactly a speedy format conversion.

For size comparison, the original JPEGs totalled 33MiB, the PNGs 642MiB and the AVIFs 73MiB. Remember the AVIFs are four times the area of the original JPEGs and without the artifacts that make JPEG an awful format for black and white art.

Mokuro ignores `.avif` files, so I did things in two steps. I created a directory called `frieren-png/vol1-sample` that contained the upscaled PNGs and another directory called `frieren/vol1-sample` containing the AVIFs.

Install and run Mokuro
----------------------

The Mokuro repo is available [here on GitHub](https://github.com/kha-white/mokuro) but it is released regularly to PyPi (see release history [here](https://github.com/kha-white/mokuro)) so there's no need to clone the GitHub repo.

Install:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install mokuro
```

Run:

```
$ mokuro frieren-png
```

On the initial run, it sat and did nothing obvious for a minute or so before downloading various things and starting its OCRing.

At one point, it outputted this:

```
MangaOcrModel LOAD REPORT from: kha-white/manga-ocr-base
Key                                  | Status     | Details
-------------------------------------+------------+--------
decoder.bert.embeddings.position_ids | UNEXPECTED |        

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
```

This indeed seems to be harmless, i.e. it can be ignored.

After it's finished running, you should have:

```
$ ls
frieren-png/  frieren-png.html  frieren-png.mokuro
```

The `frieren-png.html` is the old HTML format that Mokuro still outputs but is no longer actively developing, you can open it in your browser (but it's very poor compared to the Mokuro Reader covered in the next section).

Note: I think the OCRing assumes or deduces a particular text orientation and sticks with it. Or this is my guess, as it seemed to do much worse at OCRing the table-of-contents page of my sample which had horizontal text compared with the other pages that had vertical text.

Take a look at the resulting `frieren-png.mokuro` file, you'll see that it includes paths to the image files that are relative to the directory you specified when starting `mokuro`, if, afterward, you change the paths or e.g. change the image format from `.png` to `.avif`, you'll need to update these.

As I wanted to use the AVIFs, rather than the PNGs, I then did:

```
$ cp frieren-png.mokuro frieren.mokuro
$ sed -i -e 's/-png//g' -e 's/\.png/.avif/g' frieren.mokuro
$ zip -r frieren.zip frieren.mokuro frieren
```

The resulting `.zip` file was 58MiB.

You can just go to <https://reader.mokuro.app/> and select the upload button and open the just created `.zip` file.

The short [table of keyboard shortcuts](https://github.com/Gnathonic/mokuro-reader?tab=readme-ov-file#%EF%B8%8F-keyboard-shortcuts) is worth reading.

The Mokuro Reader is an entirely client side app, i.e. there's no server component.

Oddly, the version at `reader.mokuro.app` isn't kept up-to-date with the repo (at the time of writing the version there was 1.2.3 while the version in the repo was 1.4.0).

If you want to build and upload the latest version of the Reader to e.g. GitHub Pages, the next section covers doing this.

Mokuro Reader
-------------

```
$ git clone https://github.com/Gnathonic/mokuro-reader
$ cd mokuro-reader
```

Update to the latest version of `node` (using `nvm`, the [Node Version Manager](https://github.com/nvm-sh/nvm)):

```
$ nvm install node
$ $ nvm current
v25.7.0
```

Switch to static site creation, i.e. create a static set of files that can e.g. be uploaded to GitHub Pages, rather than the default which requires being served via `npm` on a platform like Vercel.

Edit `svelte.config.js` and `package.json` and change the references to `adapter-auto` to `adapter-static`:

```
$ vim svelte.config.js package.json
```

In `package.json`, I set the `adapter-static` version to `^3.0.10` (the latest version shown [here](https://www.npmjs.com/package/@sveltejs/adapter-static) on `npmjs.com` at the time).

Additionally, in `svelte.config.js`, find this line:

```
adapter: adapter()
```

And change it to:

```
adapter: adapter({fallback: 'index.html'})
```

Then add a comma at the end of the line and add a base path, so you end up with:

```
adapter: adapter({fallback: 'index.html'}),
paths: {base: '/my-repo'}
```

You only need to set `base` if you're planning to upload the result to something like GitHub pages where the base URL isn't rooted at `/` but is something like this:

```
https://my-name.github.io/my-repo
                         ^^^^^^^^
```

Change `my-repo` to match your setup.

By default the build process will produce `.js.map` files that are only needed for Javascript debugging and which substantially increase the size of the static site (14MiB vs 3.8MiB).

To disable these:

```
$ vim vite.config.ts
```

And find `sourcemap: true` and change the `true` to `false`.

I created an empty repo on GitHub called `static-mokuro-reader` and after updating `base` to this value, built and deployed things like so (I keep all my Git projects in `~/git`):

```
$ npm run build
$ cp -r build ~/git/static-mokuro-reader
$ cd ~/git/static-mokuro-reader
```

By default GitHub Pages assumes your content is a Jekyll site and needs to be built. To disable this:

```
$ touch .nojekyll
```

Now, create the local repo, check everything in and push it:

```
$ git init
$ git checkout -b pages
$ git add .
$ git commit -m 'Initial commit.'
$ git remote add origin git@github.com:my-name/static-mokuro-reader.git
$ git push -u origin pages
```

Then in GitHub, on the `static-mokuro-reader` repo page, I went to _Setting_, selected _Pages_ and changed the _Branch_ value from _None_ to `pages`.

On the main page for your repo, you should see (within a few minutes at most) a _Deployments_ section with green tick mark beside _github-pages_. If you click this, it'll open a page showing a link something like:

```
https://my-name.github.io/static-mokuro-reader/
```

Click this to open your own version of the reader.
