RTK cards
=========

See [`minimalist-rtk-cards.md`](minimalist-rtk-cards.md) For Gemini's take on producing minimalist cards for RTK and the reasoning behind its choices. Gemini is clear that these should always be one-way cards - from keyword to kanji.

This is exactly what Heisig says in the retrospective he includes at the start of chapter 11 (I do think it would have been helpful if he'd made all these points earlier - but I guess the idea, is you should have learned enough at this stage that you can really appreciate the points while it's also not to late to correct if you've been doing things badly).

Kanji Koohii phono-semantic readings
------------------------------------

On [Kanji Koohii](https://kanji.koohii.com/), many RTK card comes with a single reading (the remainder come with no reading at all).

I asked Gemini about these. It _seems_ they correspond to the _on-yomi_ reading that are assigned to each character in RTK 2.

Basically, this is about phono-semantic readings, or what RTK 2 calls "kanji chains".

So one characters determines one of the on-yomi readings of the characters it appears in.

E.g. 青 (blue) is a "signal primitive" with the reading _sei_ and the characters in its kanji chain are:

* 清 (Water + Blue) = _sei_ (Pure/Clear water)
* 晴 (Sun + Blue) = _sei_ (Clear weather/Sunny)
* 静 (Contention + Blue) = _sei_ (Quiet/Still)
* 精 (Rice + Blue) = _sei_ (Refined/Spirit)

So the 青 half of the kanji provides the phonentics (of one on-yomi reading of the kanji) while the other provides a semantic component.

This single reading is _not_ included in RTK 1 and including them on RTK 1 cards seems to go against the principle of _keep it simple_ until you've learned all the kanji - only start layering things on later.

Gemini's suggestion is to include them on the card, but not to require recalling them as part of learning the card - you should simply note the reading each time you review the card and if some them stick through fairly passive acquisition like that, that's good enough.

RTK 2 covers phono-semantic readings but some people consider it a little heavy going and there's some consensus that [The Kanji Code](https://thekanjicode.com/) is more useful/accessible (there's not much on the website besides the [list of phonetic components](https://thekanjicode.com/list-of-phonetic-components/)), the book is available [here](https://www.amazon.com/gp/product/0648488608) on Amazon.

For more discussion with Gemini about all this, see [here](https://gemini.google.com/share/ac111982e828). I'm not convinced about its claim that the readings are sometimes the most common rather than an RTK 2 reading. Characters like 込 and 畑 that have no on-yomi readings, have no reading at all in Kanji Koohii. And for some characters, like 誰, its reading in Kanji Koohii is _sui_ even though this reading is vanishingly rare (in modern times, it only really has the kun-yomi reading だれ) but _sui_ is given because its signal primitive is 隹 which has the reading _sui_. For more on this, see this follow-up Gemini [chat](https://gemini.google.com/share/a5d8ed025c9a).

RTK primitives
--------------

Many of Heisig's RTK primitives have no Unicode representation which makes them hard to include in Anki cards.

When asked, Gemini just repeatedly hallucinated solutions around how to deal with this. In the end, the only concrete thing it came up was pointing the GitHub repo [cyphar/heisig-rtk-index](https://github.com/cyphar/heisig-rtk-index) where SVGs are provided for all the primitives. Go to the releases section and download the `.zip` file, it includes the SVGs and `INDEX_VOL1.csv` which is laid out like this:

|Heisig No.|Unicode|SVG                                                             |Keyword       |Mnemonic |Strokes|Primative|
|----------|-------|----------------------------------------------------------------|--------------|---------|-------|---------|
|   75     | 乙    |                                                                | fish guts    |         | 1     |         |
| 75.2     |       |<img class="rtk-primitive" src="mRtK6-0075.2-hook-bottom.svg"/> | hook (bottom)|         | 1     | y       |
| 75.1     | ⺃    |<img class="rtk-primitive" src="mRtK6-0075.1-hook-right.svg"/>  | hook (right) |         | 1     | y       |
|   76     | 乱    |                                                                | riot         |         | 7     |         |
|   77     | 直    |                                                                | straightaway |         | 8     |         |
|P-010     |       |<img class="rtk-primitive" src="mRtK6-P-010-tool.svg"/>         | tool         |         | 3     | y       |
|   78     | 具    |                                                                | tool         |         | 8     |         |
|   79     | 真    |                                                                | true         |         | 10    |         |

I.e. it has the 2000+ kanji with the primitives interleaved in the same order as you come across them in the book. Many of the primitives do have Unicode representations, e.g. see ⺃ above, but others, e.g. `tool` and `hook (bottom)` do not.

Note: some primitives aren't kanji in their own right and get their own "box" in RTK (but no Heisig no.), e.g. the 10th such primitive is the tool primitive (which is then followed by a kanji with the keyword tool) and appears above as `P-010`. Kanji, that are also later used as primitives, are introduce as kanji and then their primitive forms are introduced in the same "box", e.g. `75`, `75.1` and `75.2` above.

### Controlling the release of cards and drilling

If you import an existing deck into Anki, it'll automatically release cards from the deck at a defined rate per day for you to learn.

This [Gemini chat](https://gemini.google.com/app/55d755c72f3a16de) discusses turning off this feature and instead managine the release of cards yourself each day.

This chat also covers whether you should be drilling new cards initially within Anki (i.e. going thru a phase where you go over cards for the first time, essentially hitting _Again_ for most of them until they get into your head for the first time).

### More on Kanji readings and what to incorporate on cards

This [Gemini chat](https://gemini.google.com/app/0c7b5008cf5e88b3) covers learning vocabulary in context, how much to focus on readings (a little but not too much).

It suggests using the [Japanese Support Anki add-on](https://ankiweb.net/shared/info/3918629684) to:

* Paste the Kanji into a field.
* Press a shortcut.
* It automatically generates the 日[に]本[ほん]語[ご] format for you.

The Japanese Support Anki add-on is actually developed in the Ankitects space on GitHub, i.e. the same space as Anki itself, and the code can be found [here](https://github.com/ankitects/anki-addons/tree/main/code/japanese).
