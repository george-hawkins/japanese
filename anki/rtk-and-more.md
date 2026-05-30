### RTK cards

Creating minimalist cards for RTK: <https://gemini.google.com/app/0a6f92bfcba35888>

Note: it makes clear, it feels these should always be one-way cards - from keyword to kanji.

This is exactly what Heisig says in the retrospective he includes at the start of chapter 11 (I do think it would have been helpful if he'd made all these points earlier - but I guess the idea, is you should have learned enough at this stage that you can really appreciate the points while it's also not to late to correct if you've been doing things badly).

### Kanji Koohii phono-semantic readings

On [Kanji Koohii](https://kanji.koohii.com/), each RTK card comes with a single reading.

I asked Gemini about these [here](https://gemini.google.com/app/424d8ec79e36eb0d).

Basically, it's either the most common reading or the phono-semantic reading.

Phono-semantic readings sound interesting, and I discussed including them on Anki cards.

The Gemini chat includes suggestions on including this information on Anki RTK cards.

RTK 2 covers phono-semantic readings but some people consider it a little heavy going and there's some consensus that [The Kanji Code](https://thekanjicode.com/) is more useful/accessible (there's not much on the website besides the [list of phonetic components](https://thekanjicode.com/list-of-phonetic-components/)), the book is available [here](https://www.amazon.com/gp/product/0648488608) on Amazon.

### RTK primitives

Many of Heisig's RTK primitives have no Unicode representation which makes them hard to include in Anki cards.

I asked Gemini about this and it just repeatedly hallucinated solutions [here](https://gemini.google.com/app/da4f94368baf29f6). The only concrete thing it came up was pointing the GitHub repo [cyphar/heisig-rtk-index](https://github.com/cyphar/heisig-rtk-index) where SVGs are provided for all the primitives. Go to the releases section and download the `.zip` file, it includes the SVGs and `INDEX_VOL1.csv` which is laid out like this:

```
75,乙,,fish guts,,1,,
75.2,,"<img class=""rtk-primitive"" src=""mRtK6-0075.2-hook-bottom.svg""/>",hook (bottom),,1,y,
75.1,⺃,"<img class=""rtk-primitive"" src=""mRtK6-0075.1-hook-right.svg""/>",hook (right),,1,y,
76,乱,,riot,,7,,
77,直,,straightaway,,8,,
P-010,,"<img class=""rtk-primitive"" src=""mRtK6-P-010-tool.svg""/>",tool,,3,y,
78,具,,tool,,8,,
79,真,,true,,10,,
```

I.e. it has the 2000+ kanji with the primitives interleaved in the same order as you come across them in the book. Many of the primitives do have Unicode representations, e.g. see ⺃ above, but others, e.g. `tool` and `hook (bottom)` do not.

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
