KanjiVG animate
===============

The JavaScript here was created using Claude.

To use, download the latest [KanjiVG `main` release](https://github.com/KanjiVG/kanjivg/releases), unpack it here and covert it into a form that's nicer for use with Anki:

```
$ unzip  ~/Downloads/kanjivg-20250816-main.zip
$ ls kanji
0f9a8.svg  05d90.svg  06d36.svg  07d32.svg  ...
$ python3 ./kanjivg-rename.py
$ ls kanjivg
_kanjivg-0.svg  _kanjivg-去.svg _kanjivg-幔.svg _kanjivg-服.svg  ...
```

Then run a webserver that can serve `demo.html`:

```
$ python3 -m http.server 8000
```

And open the URL <http://localhost:8000/kanjivg-animate/demo.html> in your browser.

If you want to use the KanjiVG files directly, without the need to run `kanjivg-rename.py`, just replace the `script` tag in `demo.html` with:

```
<script src="kanjivg-animate.js" data-base-path="kanji" data-filename-format="hex" data-filename-prefix=""></script>
```
