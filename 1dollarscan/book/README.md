Trim edges from pages
=====================

On many of the scanned pages, there's at least one edge of the page where you can see the transition between the page and the scanner bed. 

The `trim.py` script here attempts to trim them off.

The results end up in `out`:

```
$ ls out
page-001.png        page-068.png        page-135.png        page-202.png
page-001_annot.png  page-068_annot.png  page-135_annot.png  page-202_annot.png
page-002.png        page-069.png        page-136.png        page-203.png
...
```

The `_annot.png` files are just annotated versions of the original that hightlight in red exactly what was trimmed and can just be removed.

Once run, I manually fixed up the pages marked `BAIL` and then upscaled the result.

I then ran `file *` and worked out the typical width and height and padded/trimmed everything to match this:

```
$ magick mogrify -background white -gravity center -extent 2534x4060 -alpha off *.png
```

And finally, I downscaled, normalized and coverted to AVIF (as covered in [`../README.md`](../README.md).

Setup
-----

Create Python `venv`:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
```

Install NumPy and OpenCV:

```
$ pip install numpy opencv-python
```

Run the script:

```
$ python trim.py page-*.jpg | tee trim.log
```

Look for pages that the script gave up on:

```
$ grep BAILED trim.log
```
