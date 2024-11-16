Pitch accent dictionary for Yomitan
===================================

The files here were downloaded Nov 16th, 2024.

They are:

* `accent.txt` from [here](https://github.com/mifunetoshiro/kanjium/tree/master/data/source_files/raw) in the `mifunetoshiro/kanjium` repo.
* `main.js` and `attribution.txt` from the root of the [`toasted-nutbread/yomichan-pitch-accent-dictionary`](https://github.com/toasted-nutbread/yomichan-pitch-accent-dictionary) repo.

From these a fresh version of `kanjium_pitch_accents.zip` was generated like so:

```
$ node main.js ./accents.txt ./output
$ 7zz a -tzip -mx=9 -mm=Deflate -mtc=off -mcu=on kanjium_pitch_accents.zip ./output/*.json
```

Note: on some (all?) Linux systems and if using `brew` on Mac, the command is `7zz` while on other setups it may be `7z` (see this Stack Exchange [answer](https://askubuntu.com/a/1465861/734204) for how the difference came about).

When using `brew` using can install the relevant package like so:

```
$ brew install 7-zip
```

Installing `node` is a different task and you should google for the easiest approach on your system.
