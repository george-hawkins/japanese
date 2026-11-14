# Modern kanji list

[`modern-kanji.tsv`](modern-kanji.tsv) is a list of the 3,534 kanji that can reasonably be expected to appear in modern Japanese text. It's the union of three official lists:

* **Jōyō kanji** (常用漢字, 2010 revision): the 2,136 kanji the government recommends for general writing.
* **Jinmeiyō kanji** (人名用漢字): the 863 additional kanji that may be used in personal names.
* **表外漢字字体表** (2000): 1,022 kanji outside the Jōyō list that the 国語審議会 (National Language Council) found to occur frequently in print (books, newspapers, magazines). The table set a standard printed form (印刷標準字体) for each, and also allowed a simplified everyday form (簡易慣用字体) for 22 of them.

Characters outside this set, such as the rest of JIS X 0208 level 2, do turn up in modern text, but rarely. JIS X 0208 levels 1 and 2 (6,355 kanji) are a reasonable upper limit.

## Columns

| Column | Meaning |
|---|---|
| `kanji` | The character. |
| `codepoint` | Unicode code point. |
| `category` | Which list the character comes from (see below). |
| `jis_level` | `1` or `2` for JIS X 0208 level 1 or 2; `0213` if the character is only in the later JIS X 0213, so older Shift_JIS systems can't type it. |
| `freq_rank` | Newspaper frequency rank from KANJIDIC2 (1 = most frequent, covering about the top 2,500); blank if unranked. |
| `meaning` | Short English meaning from KANJIDIC2, truncated to 60 characters. |

Rows are sorted by category, then by code point.

## Categories

Each character appears once, in the first category below that it belongs to.

| Category | Count | Description |
|---|---|---|
| `joyo` | 2,136 | Jōyō kanji. |
| `joyo-alt` | 4 | 叱, 剥, 頬 and 填: the accepted alternative forms (許容字体) of the Jōyō kanji 𠮟, 剝, 頰 and 塡. The official Jōyō forms are only in JIS X 0213, so these alternatives are what most fonts and input methods produce. |
| `jinmeiyo` | 651 | Jinmeiyō kanji that aren't variants of Jōyō kanji. Includes the five characters removed from the Jōyō list in 2010 (匁, 勺, 錘, 銑, 脹). |
| `jinmeiyo-variant` | 212 | Jinmeiyō kanji that are older or variant forms of Jōyō kanji (e.g. 亞 for 亜), allowed in names. |
| `hyogai` | 514 | 表外漢字字体表 kanji not already covered above. The other 508 of its 1,022 kanji became Jōyō or Jinmeiyō, mostly in the 2010 revision. |
| `hyogai-simplified` | 17 | The table's simplified everyday forms (簡易慣用字体), e.g. 噛 for 嚙 and 并 for 幷. The table lists 22, but 5 are already Jōyō or Jinmeiyō. |

## Limitations

* Some 2010 accepted alternative forms differ only in the number of dots on ⻌ or 飠 (遡, 遜, 謎, 餌). Both forms share one code point, so the list can't distinguish them.
* The `jis_level` for 表外漢字字体表 characters says whether the code point exists in JIS. It doesn't say whether the glyph matches the table's printed form; older JIS X 0208 fonts often use a simplified shape.

## Sources

* [KANJIDIC2](http://www.edrdg.org/kanjidic/kanjidic2.xml.gz) (EDRDG, CC BY-SA 4.0): the Jōyō and Jinmeiyō sets (its `grade` field: 1–8 Jōyō, 9 Jinmeiyō, 10 Jinmeiyō variant), JIS levels, frequency ranks and meanings. Downloaded 2026-11-14.
* [Wiktionary: 付録:表外漢字字体表の漢字一覧](https://ja.wiktionary.org/wiki/%E4%BB%98%E9%8C%B2:%E8%A1%A8%E5%A4%96%E6%BC%A2%E5%AD%97%E5%AD%97%E4%BD%93%E8%A1%A8%E3%81%AE%E6%BC%A2%E5%AD%97%E4%B8%80%E8%A6%A7): the 1,022 kanji of the 表外漢字字体表 and the 22 simplified forms. No machine-readable copy was available from the Agency for Cultural Affairs (文化庁), so this part comes from Wiktionary, not the government list itself. Its counts match the official 1,022 and 22.
* [表外漢字字体表](https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/sanko/hyogai/) (文化庁): the official table.
