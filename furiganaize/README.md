Adding furigana to Japanese text
================================

I thought adding furigana to Japanese text would be fairly simple.

But it turns out to be not as easy as it seems. Getting from 日本 to にほん is fairly do-able but I wanted to go further...

For ref., conversations with Gemini about tricky situations that I've seen online furigana tools fail at:

* 上手 can be read as じょうず, うわて and かみて. This and similar issues <https://gemini.google.com/share/a695e0640856>
* Rendaku and other issues (一階 is いっかい rather than いちかい) <https://chatgpt.com/share/69f79985-2fcc-83eb-a795-3b4eac7712d6> (in particular the "Top furigana failure cases" section).
* [`test_furiganaize.py`](test_furiganaize.py) - test cases constructed by Claude Code.

**Update:** I think Gemini got rendaku mixed up with onbin (and the form of onbin called sokuonbin, where a sokuon, a small tsu, is introduced).

See also <https://gemini.google.com/share/6c578c6974b6>

**Update:** I started with `fugashi` (see [`fugashi`](fugashi) subdirectory and section below), moved on to try GiNZA (see [`ginza`](ginza) subdirectory) and OpenJTalk (see [`openjtalk`](openjtalk) subdirectory). But in the end, only an LLM came close, Claude could handle my small set of example sentences that tripped up the others (see [`claude`](claude) subdirectory).

Per-kanji furigana
------------------

I was hoping to be able to split the furigana out on a per kanji basis, i.e. 日(に)本(ほん) rather than 日本(にほん). But this turned out to be suprisingly unsupported. It seems the best resource for doing this _accurately_ requires using the data available in the [JmdictFurigana project](https://github.com/Doublevil/JmdictFurigana). You can do it heuristically, e.g. given that you've worked out にほん is the furigana for 日本 lookup the readings for both and try to get the best combination but there are all kinds of issues that make this hard, e.g. the correct furigana for 一階 is いっかい but いっ isn't a reading of 一. And there are issues around names, ateji, gikun and more.

Distinguishing kun and on-yomi readings
---------------------------------------

I was hoping could clearly flag kun and on-yomi reading with katakana (for on-yomi) and hiragana (for kun-yomi) like this:

* <ruby>学生<rt>ガクセイ</rt></ruby> (both on-yomi)
* <ruby>建物<rt>たてもの</rt></ruby> (both kun-yomi)
* <ruby>本<rt>ホン</rt></ruby><ruby>棚<rt>だな</rt></ruby>  (on then kun-yomi)
* <ruby>合図<rt>あい</rt></ruby><ruby>ズ<rt>kana</rt></ruby> (kun then on-yomi)


I started using the library [`fugashi`](https://github.com/polm/fugashi). But after a while a few things made me realize this wouldn't be as simple as it seemed.

### 一階

The furigana for 一階 should be いっかい but if I feed 一階 into `fugashi` it breaks it into two unrelated words, i.e. 一 and 階, and if you combined the readings it provides you'd end up with いちかい. Interestingly, this is also what the Mac Pages application comes up with if you tell it to add furigana to 一階 - it's fairly dumb unfortunately:

```
$ echo '一階' | fugashi
一	名詞,数詞,,,,,イチ,一,一,イチ,一,イチ,漢,"","","チ促","基本形","N1","",数,イチ,イチ,イチ,イチ,"2","C3","",563508399972864,2050
階	名詞,普通名詞,助数詞可能,,,,カイ,階,階,カイ,階,カイ,漢,"カ濁","基本形","","","","B1S6SjShS,B1S6S8SjShS",体,カイ,カイ,カイ,カイ,"1","C3","",1545647094374912,5623
EOS
```

### 頑張って

MeCab splits 頑張って into 頑張っ and て - this looks a little odd to a novice like myself but apparently it's the correct split if you're prioritizing linguistic units. But it's not great if you want to add the given kana as furigana, you'd end up with <ruby>頑張っ<rt>がんばっ</rt></ruby>て which isn't what you want at all:

```
$ echo '頑張って' | fugashi
頑張っ	動詞,一般,,,五段-ラ行,連用形-促音便,ガンバル,頑張る,頑張っ,ガンバッ,頑張る,ガンバル,混,"","","","","","",用,ガンバッ,ガンバル,ガンバッ,ガンバル,"3","C1","",2259505052263044,8220
て	助詞,接続助詞,,,,,テ,て,て,テ,て,テ,和,"","","","","","",接助,テ,テ,テ,テ,"","動詞%F1,形容詞%F2@-1","",6837321680953856,24874
EOS
```

For this case, you can apply simple rules to work what was really wanted. But it turns out there are other similar quirks - you have to be aware of them and code for them. As a novice in this field, I'm only aware of the quirks I've come across.

Where I started
---------------

I started with [`fugashi`](https://github.com/polm/fugashi/) (using MeCab, see [repo](https://github.com/taku910/mecab) and [doc](https://taku910.github.io/mecab/)). See my notes on it below. However, I quickly realized it wasn't going to get me where I wanted to go.

### Where to next

I'd like to look at [SudachiPy](https://github.com/WorksApplications/sudachi.rs/tree/develop/python) and how it deals with things like 一階 to いっかい rather than いちかい. I'm told it should do better as it supports splitting modes that would see 一階 as a single unit (see its `A`, `B`, `C` modes).

Gemini suggested these options when I asked it about the 頑張って segmentation issue above:

* `pykakasi` (repo [here](https://codeberg.org/miurahr/pykakasi), docs [here](https://pykakasi.readthedocs.io/en/latest/index.html)).
* `cutlet` (from the author of `fugashi`) - repo [here](https://github.com/polm/cutlet)
* `ginza` - repo [here](https://github.com/megagonlabs/ginza) (uses SpaCy and Sudachi)

Though it seemed to suggest that `ginza` was the only one of the three that would get me where I want to go but warned that it's quite resource intensive.

As mentioned before the data from the [JmdictFurigana project](https://github.com/Doublevil/JmdictFurigana) might be useful.

[`skfurigana`](https://github.com/sugarkwork/furigana) might be interesting - even though it's only got two stars on GitHub, both Gemini and ChatGPT suggested it as one of their top choices - I wonder what additional data they based this on. Claude however wondered what if anything it was getting from using DeepSeek.

ChatGPT also mentioned [`furiganamaker`](https://github.com/dkollmann/furiganamaker), another low-start GitHub repo as a project that despite not using JmdictFurigana data, tried its best to apply heuristics etc. for a "robust" furigana solution.

Unit tests
----------

Before I got started I got Claude to write me some unit tests for edge cases that it thought I'd hit.

The result is in [`test_furiganaize.py`](test_furiganaize.py).

It doesn't run against any real API, instead the tests assume a method called `furiganaize` that retunds a lists like this:

```
furiganaize("学生") -> [Ruby("学","がく"), Ruby("生","せい")] is distinguishable from
furiganaize("今日") -> [Ruby("今日","きょう", jukujikun=True)].
furiganaize("食べる") -> [Ruby("食", "た"), Plain("べる")]
```

TODO: make sure it's got cases similar to 頑張って and 一階.

Fugashi
-------

**Update:** I moved the `fugashi` related stuff into the [`fugashi`](fugashi) subdirectory here.

See also [`fugashi/fugashi-api-doc.md`](fugashi/fugashi-api-doc.md).

First, set up a `venv`:

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
```

And install `fugashi` and the full-fat 780MiB UniDic dictionary:

```
(venv) $ pip install 'fugashi[unidic]'
(venv) $ python -m unidic download
```

Oddly, Python may not have any root SSL certs and you may get a long stacktrace that ends with an error like this:

```
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate        
(_ssl.c:1000)>
```

To resolve this:

```
(venv) $ export SSL_CERT_FILE=$(python -m certifi)
(venv) $ export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
(venv) $ python -m unidic download
download url: https://cotonoha-dic.s3-ap-northeast-1.amazonaws.com/unidic-3.1.0.zip
...
(venv) $ du -hs venv/lib/python*/site-packages/unidic/dicdir
780M	venv/lib/python3.12/site-packages/unidic/dicdir
```

Now, you can try getting a detailed breakdown:

```
(venv) $ echo '麩菓子は、麩を主材料とした日本の菓子' | fugashi
麩	名詞,普通名詞,一般,,,,フ,麩,麩,フ,麩,フ,漢,"フ濁","基本形","","","","",体,フ,フ,フ,フ,"0","C3","",17839859662201344,64901
```

Or break things into words:

```
$ echo '日本語' | fugashi -Owakati
日本 語
```

Then you can start coding something, see my [`fugashi_example.py`](fugashi_example.py). Basically, it just boils down to:

```
from fugashi import Tagger

AUXILIARY_SYMBOL = "補助記号"

tagger = Tagger()
text = "麩菓子は、麩を主材料とした日本の菓子。"

for word in tagger(text):
    # skip punctuation and symbols if you want
    if word.feature.pos1 == AUXILIARY_SYMBOL:
        continue
    print(f"{word.surface:4}  lemma={word.feature.lemma}  pos={word.pos}  unknown={word.is_unk}")
```


MeCab
-----

`fugashi` is a very thin wrapper around dynamic libraries for MeCab (GitHub repo [here](https://github.com/taku910/mecab) and GitHub Pages [here](https://taku910.github.io/mecab/)).

Behind the scenes `fugashi` just calls the entry point for the classic MeCab executable and gets it to do the real work.

But the way things are bundled, the MeCab executable isn't available to call directly.

So, I've added a small Python script here (created by Claude) that allows you to essntially do that:

```
$ python mecab_cli.py --help
MeCab: Yet Another Part-of-Speech and Morphological Analyzer

Copyright(C) 2001-2012 Taku Kudo 
Copyright(C) 2004-2008 Nippon Telegraph and Telephone Corporation

Usage: mecab [options] files
 -r, --rcfile=FILE              use FILE as resource file
 -d, --dicdir=DIR               set DIR  as a system dicdir
 ...
```

If you had the real `mecab` executable, you could `echo` text through it like so:

```
(venv) $ echo 日本語 | mecab -Owakati
日本 語
```

Unfortunately, my `mecab_cli.py` can't be used in pipelines like this. But you can achieve something similar like this:

```
(venv) $ python mecab_cli.py -Owakati <(echo '日本語')
日本 語 
```

Or you can use the `fugashi` command line tool that almost does the same thing:

```
(venv) $ echo '日本語' | fugashi -Owakati
日本 語
```

So, the downside of `mecab_cli.py` is that it can't be used in pipelines and the downside of the `fugashi` command line tool is that it just expects input and won't output anything for options like `--help`, `--version` and `--dictionary-info`.

Some of this is compensated for by two additional command line tools:

* `fugashi-info`
* `fugashi-build-dict`

In end though, knowing about options like `-Owakati` (break into words separated by spaces) is interesting but not particularly relevant to working with the programmatic interface provided by `fugashi`.
