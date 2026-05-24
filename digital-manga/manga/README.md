CBZ and readers
===============

CBZ is the most common format for community-made digital manga.

It's just a normal ZIP file of JPEGs, PNGs, WEBPs, AVIFs or whatever image format you prefer (and is supported by your reader).

It can contain an optional `ComicInfo.xml` with metadata.

Metadata
--------

This directory contains the [`comicinfo.py`](comicinfo.py), created with Claude, that can pull metadata from the [AniList](https://anilist.co/) API and create a `ComicInfo.xml`.

It doesn't require any additional packages, so you can just run it like so:

```
$ python3 comicinfo.py --publisher 'Kodansha' 'Witch Hat Atelier' 1 -o witch-hat-atelier-v1/ComicInfo.xml
```

For whatever reason, the AniList API doesn't provide publisher data so, if you want, you can provide e.g. `--publisher 'Kodansha' --imprint 'Morning KC'`, or just leave out one or both.

Check the resulting `ComicInfo.xml` and e.g. trim out any information that you don't want in the `<Summary>` tag block.

Creating a CBZ file
-------------------

Creating a CBZ file is trivial:

```
$ cd witch-hat-atelier-v1
$ zip ../witch-hat-atelier-v1.cbz ComicInfo.xml *.avif
```

macOS readers
-------------

I tried various readers for macOS:

* [Koodo reader](https://www.koodoreader.com/en) - it's more a classic e-book reader, it can handle AVIFs but doesn't read `ComicInfo.xml` metadata.
* [YACReader](https://www.yacreader.com/) - it seems to be the king of macOS comic book readers for the comic book hard-core, but while the mobile versions support AVIF, the desktop version still does not have native AVIF support (but does support WEBP).
* [OpenComic](https://opencomic.app/) - supports AVIF and `ComicInfo.xml` metadata.

In the end, I settled of OpenComic but primarily because I'd used AVIF and wanted `ComicInfo.xml` metadata support. I wasn't particularly impressed by it. It's an Electron app and isn't fine-tuned for macOS, e.g. the shortcut for fullscreen is F11 which is already taken by macOS (and toggles _Show Desktop_). It also seemed quite brittle, e.g. I repackaged my `.cbz` file and loading that volume broke (the fact that one of the main menus is _Debug_ which opens the Electron _Developer Tools_ suggests this may be an often needed feature).

Once your manga is open, click the _Page layout_ button in the toolbar and:

* Toggle on _Reading manga_ (for a back-to-front reading direction).
* Toggle on _Double page_ if you like seeing double-page art together on screen.
* Toggle on _Blank page at the beginning_ if double-page art ends up broken across pages.

Use the _View / Full screen_ menu item, rather than the usual green circle in the window's title bar, if you want a minimalist fullscreen experience without toolbar and sidebar.

Android readers
---------------

On Android, I tried the _paid_ versions of [CDisplayEx](https://www.cdisplayex.com/) and [Kuro Reader](https://kurotoshiro.dev/).

[Mihon](https://mihon.app/) is open source and seems to be the most popular comic book reader for Android. However, it's had various issues with Google Play around its plugins architecture and is now only available via [sideloading](https://en.wikipedia.org/wiki/Sideloading).
