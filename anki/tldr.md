Anki RTK speedrun
=================

This is a speedrun of setting up and getting started with Anki for working through RTK 1. Elsewhere in this repo, I go into more detail about the steps here.

Preparation outside Anki
------------------------

Create the _Klee One_ `.woff2` font as described [here](cards#kyoukasho-tai) and copy it to your Anki media directory (the location on Windows, Mac and Linux can be found [here](cards#collectionmedia):

```
$ cp _KleeOne-SemiBold.woff2 ~/'Library/Application Support/Anki2/User 1/collection.media'
```

Create the directory of KanjiVG SVGs as described [here](https://github.com/george-hawkins/japanese/tree/master/anki/cards/kanjivg-animate), then copy them to your Anki media directory too:

```
$ cd kanjivg
$ cp *.svg ~/'Library/Application Support/Anki2/User 1/collection.media'
```

Finally, copy in the `kanjivg-animate.js` script:

```
$ cd ~/'Library/Application Support/Anki2/User 1/collection.media'
$ curl -O https://raw.githubusercontent.com/george-hawkins/japanese/refs/heads/master/anki/cards/kanjivg-animate/kanjivg-animate.js
$ mv kanjivg-animate.js _kanjivg-animate.js
```

Anki steps
----------

Start and create a new deck called `rtk1-v6`.

Go to _Tools_ / _Manage Note Types_, click _Add_, select _Clone: Basic_ and name it "Japanese RTK".

Click _Fields_ and rename "Front" and "Back" to "Keyword" and "Clue" respectively.

Add field "Kanji", "Reading", "Story" and "Note".

Click _Cards_. Note: the initial name of the card will be "1: Card 1: Keyword -> Clue". The "Keyword -> Clue" bit comes from the fields used in the front and back templates, and we're going to change that.

_Styling_ already contains:

```
.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
} 
```

Add `line-height: 1.5;` into this `.card` block and then, below, add:

```
@font-face {
    font-family: "Klee One";
    src: url("_KleeOne-SemiBold.woff2") format("woff2");
    font-weight: 600;
    font-style: normal;
    font-display: swap;
}
.jp {
    font-size: 1.5em;
    font-family: "Klee One", cursive;
    font-weight: 600;
}
.kanjivg-animate {
    display: inline-block;
    width: 8em;
    height:8em;
}
.keyword {
    text-transform: uppercase;
    font-weight: bold;
}
```

Change the _Front Template_ to:

```
<div class="keyword">{{Keyword}}</div>
{{#Clue}}
<div class="clues">({{Clue}})</div>
{{/Clue}}
```

And the _Back Template_ to:

```
<span class="kanjivg-animate">{{Kanji}}</span>
<div class="keyword">{{Keyword}}</div>
<div class="story">{{Story}}<div>
{{#Note}}
<div class="note">Note: {{Note}}<div>
{{/Note}}
<script src="_kanjivg-animate.js"></script>
```

That's it.

Readings
--------

This is supposed to be a TLDR; document, but I'm going to go on a short diversion to cover kanji readings.

RTK 1 does not cover readings at all, and the general consensus seems to be that doing so isn't very helpful.

However, Kanji Koohii includes a single on-yomi reading for every kanji that has at least one on-yomi reading (some kanji have only kun-yomi readings).

Initially, I assumed this reading was the _signal primitive_ reading from RTK 2 as it's clear it's not always chosen on the basis of highest usage.

However, on looking at the [code for Kanji Koohii](https://github.com/fabd/kanji-koohii), it turns out there's _no_ cleverness to how the reading is chosen. It uses the data from the [KANJIDIC Project](https://www.edrdg.org/wiki/KANJIDIC_Project.html) and, for any given kanji, takes the KANJIDIC list of on-yomi readings for that kanji and choses the first of those.

I've looked and KANJIDIC makes _no_ ordering guarantees (other than that ordinary readings come first, followed by other classes of readings). It happens that _most_ of the time, the reading with the highest usage frequency comes first but this certainly isn't always the case (KANJIDIC was compiled from various different sources, and it seems each applied its own rules).

So, while I intially included a `Reading` field in my the RTK 1 Anki cards, I dropped it once this became clear.

In the meantime, though, using Claude, I created my own table of readings for RTK 1 that you can find [here](https://github.com/george-hawkins/rtk-readings). It is _not_ based on usage frequency, instead it's based on something similar to the _signal primitives_ of RTK 2 or [The Kanji Code](https://thekanjicode.com/). You'll find a ["why" section](https://github.com/george-hawkins/rtk-readings#why) with my list, that justifies the choice for use with RTK 1.

### Readings with audio

If you add in readings, then you could add the following to the _Back Template_:

```
{{#Reading}}
<div class="signal-primitive jp">{{Reading}}{{tts ja_JP speed=0.7 voices=Apple_Kyoko_(Enhanced):Reading}}</div>
{{/Reading}}
{{^Reading}}
<div class="no-signal-primitive">[no reading]</div>
{{/Reading}}
```

The `{{tts ...}}` bit will automatically read aloud the value of the `Reading` field when the back of the card is shown.

**Update:** I eventually gave up on the the `{{tts ...}}` bit. It doesn't know how to pronounce on-yomi written as katakana correctly, e.g. ビョウ is pronounced as ビョ followed by ウ rather than as ビョー. You can do tricks like entering `ビョウ[ビョー]` and using the `kanji` and `kana` qualifiers to select the non-bracketed or bracketed bit, so you'd do:

```
{{kanji:Reading}}[anki:tts lang=ja_JP speed=0.7 voices=Apple_Kyoko_(Enhanced)]{{kana:Reading}}[/anki:tts]
```

Note: the `kanji` and `kana` qualifiers and the special square-bracket `[anki:tts ...]` form that allows you to surround a piece of text (the kana reading here).

### TTS voices

By default, Anki uses a robotic voice for the `tts` that would have sounded bad even in the 1990s. So, above, I've specified the macOS voice `Apple_Kyoko_(Enhanced)` for the reading. To see what languages your system supports, temporarily add this to the bottom of the front or back template:

```
{{tts-voices:Reading}}
```

If you then preview the template, it'll show you a list of known voices (or on AnkiDroid, it'll show a link that opens a dialog allowing you to select a voice).

On macOS, you need to go to settings and actively install the enhanced voices like "Kyoko (Enhanced)". Google for something like "macOS manage voices" as how this is done changes by macOS version.

The default voice used by AnkiDroid is fine, but if needed, you can specify a list of voices (separated by `,` with no space) so e.g. if `Apple_Kyoko_(Enhanced)` isn't available as you're currently using a Windows system then it'll fall back to the next item in the list.

First card
----------

Add a new card to the deck with:

* Keyword: elbow
* Clue: part of body
* Kanji: 肘
* Reading: チュウ
* Story: The **elbow** is the _flesh_ that _glues_ together the upper and lower arm.

Note: the clue is stupid for this example but is just included to show that you can include a small clue with the keyword if e.g. you keep confusing the keyword with another similar English word that's also used as a keyword.

For more on clues see [here](cards/clues.md). **TLDR;** a valid clue clarifies the _meaning or context of the English keyword_. An invalid clue _leaks information about the structure or components of the Japanese kanji_.

Click the _Cards..._ button for a preview of how it'll look. In particular, select the _Back Template_ and click the large KanjiVG kanji and see it redraw stroke-by-stroke.

Syncing to AnkiDroid
--------------------

I synced my first card to AnkiWeb, this also syncs the SVGs, font and JavaScript.

I then opened AnkiDroid. It always syncs with AnkiWeb on startup and I could see my first card.

However, when it tried to display it, it didn't show the nice stroke order diagram. Instead, a little dialog popped up about "content display" error. It seems it doesn't block you using it while waiting for all the media to sync, which goes on in the background. I just had to wait a minute or so for the full sync to complete (there's no visual indication that this is happening or has completed).

Creating cards
--------------

You can find stories for the RTK cards [here](https://kanji.koohii.com/study/kanji/1) on Kanji Koohii (you need to have [registered](https://kanji.koohii.com/account/create) first).

Each Kanji Koohii kanji also comes with a single reading, this is usually (always?) the _signal primitives_ from RTK 2. For more about this see [here](rtk-cards.md#kanji-koohii-phono-semantic-readings), but in short, it's nice to be aware of this reading, but it's not something you should be putting effort into remembering at this point.

It's a pity the _New & updated stories_ aren't always collapsed so you see the top-voted _Shared stories_ before anything else.

Shortcuts
---------

For answering, you basically just need `space` (for both _show answer_ and grade as _good_) and `1` (for grade as _again_).

The basics:

* **Show answer** - `space`.
* **Grading:** `1` = again, `3` or `space` = good.
* **Brain fart:** forgot a card but think it's a brain short-circuit, use `-` to bury for today and be asked again tomorrow (without affecting its grading).
* **Undo:** `cmd-Z` (if you fat-fingered 3 when you meant 1, press cmd-Z).
* **Edit current card:** `E`.
* **Add card:** `cmd-enter` (and clears fields).
* **Sync:** `Y`.
* **Leech:** `*` to star a problem card, see the star again and still having problems then it's probably a leech.

For more, see [here](https://github.com/george-hawkins/japanese/blob/master/anki/anki-workflow.md).

Anki setup and notes
--------------------

For justifications and more details on some of the points below, see [`README.md`](README.md).

## Setup

In the main Anki window, click the gear icon to the right of your new deck, select _Options_. Then...

**Limits**: set _New cards/day_ to 20 and _Maximum reviews/day_ to 9999 (for justifications, see [here](README.md#settings)).
**FSRS**: scroll down to the FSRS section and toggle it on (it's the new SRS algorithm and the only reason it's not on by default is that some older clients didn't support it - all iOS and AnkiDroid releases since February 2024 support it). Trenton suggests [here](https://youtu.be/_MWtbI4IwfU) that you reduce the desired retention to 85%.

**Note:** 20 new cards per day should be good for RTK but Trenton recommends 10 cards a day for vocab decks (like Kaishi 1.5K).

**Update:** I later changed this to 99 as I found if I started a few hours earlier one day than the previous then it wouldn't show me all the new cards I created in the course of the current day (at least that's my theory for why this happened). For this deck, it could be any high value as I was creating the cards, so this defined/limited how many new cards there were per day.

## Notes

Only ever use _Again_ and _Good_.

Make sure you've resolved the <span lang="ja">直</span> / <span lang="zh">直</td> Japanese font issue.

## Add-ons

The only add-ons, that I've added, are the [Japanese Support](https://ankiweb.net/shared/info/3918629684) one and [AnkiConnect](https://ankiweb.net/shared/info/2055492159) (and even the "Japanese Support" one is just nice to have, I haven't actually made any real use of it).
