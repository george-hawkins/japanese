# Kanji category

`kanji-category.py` takes a single Unicode character and says what kind of Japanese character it is: a jōyō kanji, a rare kanji, a kanji component, kana, and so on.

```
$ ./kanji-category.py 籠
籠 U+7C60: jōyō (general-use kanji)
  Added to the list in 2010. Taught in secondary school.
  Variants: 篭 (hyōgai, simpler form)
  JIS X 0208 level 2.
  Meaning: basket; devote oneself; seclude oneself; cage; coop; implied

$ ./kanji-category.py 篭
篭 U+7BED: hyōgai (common kanji outside the official lists)
  JIS level 1 kanji that is not in the 表外漢字字体表.
  Variants: 籠 (jōyō, more complex form)
  JIS X 0208 level 1, newspaper frequency rank 2237.
  Meaning: seclude oneself; cage; coop; implied
```

It needs Python 3.14 and [`uv`](https://docs.astral.sh/uv/), and has no other dependencies. `--help` lists the categories, and `--brief` prints only the category name.

## Categories

A kanji gets the first category in this table that applies to it.

| Category | Count | What it is | How it's decided |
|---|---|---|---|
| `jōyō` | 2,140 | Jōyō kanji (常用漢字): the official list for general use. | The 2,136 kanji of the 2010 list, plus the 4 accepted alternative forms (許容字体) 叱, 剥, 頬 and 填, which are what most fonts and input methods produce in place of the official 𠮟, 剝, 頰 and 塡. |
| `jinmeiyō` | 864 | Jinmeiyō kanji (人名用漢字): the further kanji allowed in personal names. | The official list, including the old or variant forms of jōyō kanji (亞, 國), the 5 kanji dropped from the jōyō list in 2010, and 勒, added in June 2026. |
| `hyōgai` | 676 | Common hyōgai kanji (表外漢字): in neither list, but met in ordinary modern print. | In the 表外漢字字体表 (530), or otherwise in JIS X 0208 level 1 (146). |
| `rare` | 6,379 | Kanji used in Japan but uncommon: name variants, old forms, literary and specialist kanji. | Otherwise in JIS X 0208 level 2 or JIS X 0213 levels 3 and 4, plus 86 kanji outside JIS that are in the IBM extensions to Shift_JIS or Unicode's core Japanese set. |
| `chinese` | 3,762 | Characters of modern Chinese that aren't used in Japanese (们, 她, 东). | None of the above, but in a current Chinese standard: the PRC's 通用规范汉字表, Hong Kong's glyph list, or level 1 of Taiwan's Big5. |
| `obscure` | about 85,000 | Any other CJK ideograph: historical, dictionary-only or regional. | Everything else in Unicode's ideograph blocks. These aren't listed in the table. |
| `component` | 490 | A part of kanji rather than a kanji. | The radical and stroke code points (⼈ U+2F08, ⺅, ㇏), plus 123 parts that Unicode encodes as ideographs (氵, 宀, 辶). |
| `hiragana` | 80 | Modern hiragana. | あ to ん, their voiced and semi-voiced forms, and small ぁぃぅぇぉっゃゅょ. |
| `katakana` | 84 | Modern katakana. | The same set, plus ヴ, ヵ, ヶ and the long vowel mark ー. |
| `halfwidth` | 56 | Half-width katakana (ｱ, ｶ, ｰ): legacy forms of modern katakana. | Unicode name. |
| `kana-rare` | 13 | Kana that are still valid but seldom seen. | ゎ ヮ ゔ ゕ ゖ ヷ ヸ ヹ ヺ, and the iteration marks ゝ ゞ ヽ ヾ. |
| `kana-obsolete` | 21 | Kana no longer used. | ゐ ゑ ヰ ヱ, the ligatures ゟ and ヿ, the archaic letters (𛀀, 𛀁 and four more), and the historical small kana (small wi, we, wo, ko and n). |
| `hentaigana` | 285 | Hentaigana (変体仮名): variant hiragana dropped when one form per syllable was fixed in 1900, now only on shop signs and in calligraphy. | Unicode name. |
| `kana-ext` | 29 | Kana for other languages. | The small katakana for Ainu (ㇰ to ㇿ) and the tone marks for Taiwanese. |
| `symbol` | | Japanese punctuation and symbols (。、「」・々〆〒), and full-width forms of other characters. | Unicode block, plus a few general symbols that are common in Japanese text (※, …, ○). |
| `other` | | Not a Japanese character at all. | Everything else. |

Some notes on the categories:

* **The 表外漢字字体表** (2000) is the 国語審議会 (National Language Council) table of 1,022 kanji outside the jōyō list that it found to occur frequently in books, newspapers and magazines. It set a printed standard form (印刷標準字体) for each, and allowed a simplified everyday form (簡易慣用字体) for 22 of them. Most of the 1,022 have since become jōyō or jinmeiyō kanji.
* **JIS X 0208 level 1** is added to `hyōgai` because the 表外漢字字体表 lists printed standard forms such as 噓, 摑 and 蟬, while the forms everyone actually types are the level 1 ones: 嘘, 掴 and 蝉. Level 1 was chosen as the commonly used half of JIS X 0208, so the rest of it (鮪, 鱈, 椙) belongs here too.
* **"Archaic" isn't a category**, because no dataset records it. An old form (旧字体) gets whatever category its official status gives it: 國 is `jinmeiyō` and 學 is `rare`, and both are shown as the old form of a jōyō kanji. Characters with no modern use anywhere are `obscure`.
* **Small ゎ and ヮ are `kana-rare`**, not to be confused with the ordinary わ and ワ. They only appear in historical spellings such as くゎ (kwa), now written か.
* **`kana-rare` and `kana-obsolete` cover both scripts.** The first line of the output says which: ゐ is `kana-obsolete (obsolete hiragana)` and ヰ is `kana-obsolete (obsolete katakana)`.
* **A component encoded as an ideograph** is one that all its dictionary entry says is that it's a radical (亠), or that Unicode has a radical code point for and that isn't a character in its own right (宀), or that is outside JIS X 0208 and described as a radical (氵). Real but rare kanji that are also radicals (戈, 匕) stay `rare`.

## Jōyō history

Each jōyō kanji's note says when it joined the list:

* **1946** (1,845 kanji): on the list since it was the tōyō kanji list (当用漢字). These are the kanji the post-war simplification into new forms (新字体) was applied to.
* **1981** (95 kanji): added when the jōyō list replaced the tōyō list. These were simplified in the same way (蛍, 渓, 竜).
* **2010** (196 kanji): added by the 2010 revision. These took their forms from the 表外漢字字体表, so apart from 曽, 痩 and 麺 they weren't simplified the way the earlier kanji were: 餌 and 遡 keep the full 𩙿 and two-dot ⻍, where 飯 and 道 have 飠 and ⻌. The list sets their printed form only; writing them by hand in the simpler shape is accepted, and the revision didn't expect every added kanji (鬱, 彙) to be written by hand at all.

The five kanji that the 2010 revision dropped (勺, 匁, 脹, 銑 and 錘) became jinmeiyō kanji. They are `jinmeiyō`, with a note saying they are former jōyō kanji.

## Variants

For kanji used in Japan, the output lists the other forms of the same kanji and says what each is relative to the one you asked about:

* `old form 旧字体` and `new form 新字体`, from the jōyō table.
* `printed standard form 印刷標準字体` and `simplified everyday form 簡易慣用字体`, from the 表外漢字字体表.
* `official jōyō form` and `accepted alternative form 許容字体`, for the four jōyō pairs.
* `simpler form`, `more complex form` or `variant` for everything else, decided only by comparing stroke counts. So 篭 is shown as a simpler form of 籠, but nothing here says whether one was derived from the other.

Links go both ways: 籠 mentions 篭 and 篭 mentions 籠. They aren't followed any further than that, so 國 lists 国 but not 圀, which is linked only to 国.

## Files

| File | Purpose |
|---|---|
| `kanji-category.py` | The lookup script. Reads `kanji-categories.tsv`, and classifies kana, symbols and anything not in the table by Unicode name and block; the lists of rare and obsolete kana are in the script itself. |
| `kanji-categories.tsv` | The generated table of 14,311 characters: every kanji and component that isn't `obscure`. |
| `build.py` | Regenerates the table. It fetches the sources into `downloads/` (ignored by git) the first time, and again with `--refresh`. |

The table's columns:

| Column | Meaning |
|---|---|
| `char` | The character. |
| `codepoint` | Unicode code point. |
| `category` | One of `jōyō`, `jinmeiyō`, `hyōgai`, `rare`, `chinese` or `component`. |
| `jis_level` | `1` or `2` for JIS X 0208 level 1 or 2, `3` or `4` for the levels added by JIS X 0213; blank if in neither. |
| `freq_rank` | Newspaper frequency rank from KANJIDIC2 (1 = most frequent, covering about the top 2,500); blank if unranked. |
| `variants` | Other forms of the kanji, as described above. |
| `note` | Anything else worth knowing, such as when a jōyō kanji joined the list, the school grade, or why a non-JIS kanji counts as `rare`. |
| `meaning` | English meanings from KANJIDIC2, or Unihan's definition for characters KANJIDIC2 doesn't cover. |

Rows are sorted by category, then by code point.

## Limitations

* The `chinese` and `component` rules are heuristics over what the sources record. A few borderline characters will be debatable, such as 韭, which is `component` because KANJIDIC2 only describes it as the leek radical, though it's also a way of writing にら.
* Variant links come from KANJIDIC2 and Unihan. Unihan's sometimes reflect Chinese usage and not Japanese: 听 is linked to 聽 because it's the simplified Chinese form, while in Japanese it's a separate kanji.
* Name variants that no Japanese character set standard includes are `obscure`, unless listed by hand in `build.py`. Only 𠮷 is at the moment.
* Some accepted alternative forms differ from the official form only in the number of dots on ⻌ or 飠 (遡, 遜, 謎, 餌, 餅). Both forms share one code point, so they can't be told apart.
* `jis_level` says whether the code point exists in JIS. It doesn't say whether a font's glyph matches the 表外漢字字体表 printed form; older JIS X 0208 fonts often use a simplified shape.
* Python 3.14 knows Unicode 16. Any kana added to Unicode after that come out as `other`, and newer symbols are classified by block alone, without notes.

## Sources

* [KANJIDIC2](http://www.edrdg.org/kanjidic/kanjidic2.xml.gz) (EDRDG, CC BY-SA 4.0): JIS levels, frequency ranks, school grades, stroke counts, meanings and variants.
* [Unihan](https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip) (Unicode 18.0): the jōyō and jinmeiyō lists (`kJoyoKanji`, `kJinmeiyoKanji`), the jōyō table's old forms (`kJapaneseNewVariant`), other variants, radicals, and membership of the Chinese standards and the IBM extensions.
* [EquivalentUnifiedIdeograph.txt](https://www.unicode.org/Public/UCD/latest/ucd/EquivalentUnifiedIdeograph.txt) (Unicode): the ideograph each radical or stroke code point corresponds to.
* [Wiktionary: 付録:表外漢字字体表の漢字一覧](https://ja.wiktionary.org/wiki/%E4%BB%98%E9%8C%B2:%E8%A1%A8%E5%A4%96%E6%BC%A2%E5%AD%97%E5%AD%97%E4%BD%93%E8%A1%A8%E3%81%AE%E6%BC%A2%E5%AD%97%E4%B8%80%E8%A6%A7): the 1,022 kanji of the 表外漢字字体表 and the 22 simplified forms. No machine-readable copy was available from the Agency for Cultural Affairs (文化庁), so this part comes from Wiktionary and not the [official table](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/sanko/hyogai/). `build.py` checks that the counts match the official 1,022 and 22.
* [Wikipedia: List of jōyō kanji](https://en.wikipedia.org/wiki/List_of_j%C5%8Dy%C5%8D_kanji): the year each jōyō kanji joined the list. Two of its rows give a non-jōyō variant as the kanji (篭 for 籠, 䇳 for 箋); `build.py` corrects those against Unihan and checks that the two sources then agree on all 2,136, and on the counts of 1,845, 95 and 196.

All five were downloaded on 2026-11-21.
