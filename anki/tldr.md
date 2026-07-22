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
{{#Reading}}
<div class="signal-primitive jp">{{Reading}}</div>
{{/Reading}}
<div class="story">{{Story}}<div>
{{#Note}}
<div class="note">Note: {{Note}}<div>
{{/Note}}
<script src="_kanjivg-animate.js"></script>
```

That's it.

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

## Notes

Only ever use _Again_ and _Good_.

Make sure you've resolved the <span lang="ja">直</span> / <span lang="zh">直</td> Japanese font issue.

## Add-ons

The only add-ons, that I've added, are the [Japanese Support](https://ankiweb.net/shared/info/3918629684) one and [AnkiConnect](https://ankiweb.net/shared/info/2055492159) (and even the "Japanese Support" one is just nice to have, I haven't actually made any real use of it).
