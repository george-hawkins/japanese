Anki setup for Japanese learning
================================

**TLDR;** there are lots of videos about setting up Anki for Japanese learners and I thought this was going to be more involved than it is. For a beginner, I don't think anything more is needed than installing the _Japanese Support_ add-on and ensuring you're seeing Japanese versions of all characters rather than Chinese ones (where the two differ).

See also
---------

For creating cards outside Anki using `vim` and Markdown, see my [`markdown-to-anki` repo](https://github.com/george-hawkins/markdown-to-anki).

For more on creating cards with a nice kyoukasho-tai font, kanji-stroke colorization and animation, see the [`cards`](cards) subdirectory.

For creating minimalist RTK specific cards, see [`rtk-cards.md`](rtk-cards.md).

Shortcuts and more
------------------

For a good overview of Anki shortcuts to make like easier, see the Gemini generated [`anki-workflow.md`](anki-workflow.md).

Controlling the release of cards
--------------------------------

When I import an existing deck from someone else, I'd like to explicitly control the release of new cards, e.g. decide today to release 10 cards but tomorrow, if I do nothing, then no additional cards should be released.

This brief [page](controlled-release.md) describes doing this either by:

* Setting _New cards/day_ to 0 and using _Custom Study_ to explicitly release new cards.
* Suspending everything in the deck and then using unsuspend to release cards.

Drilling
--------

Anki doesn't have an obvious drilling workflow, i.e. a phase where you go over new cards repeatedly just to get them into your brain first time. This [page](drill.md) discusses how you can drill in Anki but also asks if Anki is really the right place for this. Perhaps simply the act of writing the basics out on a piece of paper, then scanning that repeatedly, would get things into your head as first pass before working with the corresponding cards in Anki.

Vocabulary in context
---------------------

I'm convinced it only makes sense to learn vocabulary in context. This [page](context.md) tries to justify this approach and also goes into how much effort you should put into thinking about the readings involved in new vocabulary (are they on-yomi or kun-yomi reading, is the word jujujikun) - the answer is "a bit but not _too_ much".

### Irregular kanji readings

| Term | How Kanji Are Used | Example |
|---|---|---|
| 熟字訓 (Jukujikun) | Chosen for meaning as a collective unit; individual sounds are ignored. | 煙草 (Read as tabako / Meaning: "smoke grass") |
| 当て字 (Ateji) | Chosen purely for sound; individual meanings are ignored. | 寿司 (Read as su-shi / Meaning: "longevity" + "administer") |
| 義訓 (Gikun) | Creative or non-standard readings applied for stylistic effect, heavily used in manga and lyric writing. | Writing 地球 (Earth) but forcing the reader to pronounce it as āsu (the English word "Earth"). |

Trenton
-------

Much of the material below is from Jouzu Juls's various Anki videos. I also watched Trenton's [You Should Be Using Anki](https://www.youtube.com/watch?v=_MWtbI4IwfU). Most of it is the same as Jouzu Juls's advice. Two things he mentions are FSRS (see below) and the Anki deck [Kaishi 1.5K deck](https://github.com/donkuri/Kaishi) (which I'd come across before).

Usage advise
------------

Much of what's below is from about the 6m 10s onward mark in Jouzu Juls's ["secret to learning Japanese 10x faster"](https://www.youtube.com/watch?v=DcY2Svs3h8M).

### Settings

In the main window, click the cog icon to the right of your deck and:

* In _Daily Limits_, change _Maximum reviews/day_ to 9999.
* In the same section adjust down _New cards/day_ if you feel 20 is too much.

Note: Trenton suggests 10 new words a day for beginners. If you're aiming to learn all the RTK Kanji though, that's probably too low. Remember that some Anki card types generate two cards, so ten words might result in twenty cards - take this into account when setting the value.

If you've taken a break from Anki, you should set the _New cards/day_ to 0 until you're caught up.

### Again and Good

In the same video he argues you should only use _Again_ and _Good_ and completely ignore _Hard_ and _Easy_ (Trenton repeats this).

If forgetting a card was just a temporary brain fart or you made some very minor mistake, don't press _Again_, **instead press `-`, this will bury the card for today but ask you again tomorrow.

### Shortcuts

* `E` - edit the current card to correct it.
* `cmd-Z` - undo your last response.
* `shift-8` - star a card, particularly ones you suspect are leeches, if you keep having problems and you see the star, something probably needs to be done.
* `Y` - to manually sync (important see _Syncing_ section below).

### Vocab vs sentence cards

Trenton notes that sentence cards provide context and all that good stuff but he still does vocab cards, e.g. Saturn --> 土星, as they're cheap to create (versus trying to find a good n+1 sentence for your word) and often good enough for e.g. simple nouns with no ambiguity (think apple --> りんご).

Vocab cards can become more valuable if/once you go monolingual, i.e. mapping to a Japanese definition will be far better than a poor match in English.

### FSRS

Anki considers the default algorithm to be legacy. However, the new FSRS one isn't enabled by default as it requires all clients to also support it. The desktop and iOS versions have longs supported it and AnkiDroid added support in late February 2024 (in release 2.17).

I've turned on FSRS (you just have to enable it in the desktop version - it's then picked up by the clients from metadata in the decks).

There's a bewildering array of options if you toggle on FSRS. The only one I changed was setting _Desired retention_ to 85% rather than 90% (at Trenton's suggestion).

### Syncing

FSRS doesn't like it if you don't keep everything in sync - AnkiDroid syncs every 10 minutes automatically (if you've got automatic syncing enabled, which I do). But desktop Anki only syncs on start and exit or you manually sync.

See my [`syncwatcher`](https://github.com/george-hawkins/syncwatcher) repo (created with Claude Code) to automatically sync desktop Anki.

Font setup
----------

Make sure that Anki is correctly setup for displaying the Japanese form of all kanji and not the Chinese form (in those occassional cases where the two differ).

See Jouzu Juls [How to Fix the Japanese Font Issue on Anki/Chrome](https://www.youtube.com/watch?v=wlmfncz-Wxg).

Once you've done this, 直 should appear as <span lang="ja">直</span> and not <span lang="zh">直</td> (it you see the same character three times then you have other problems).

Jouzu Juls - 6 essential add-ons
--------------------------------

Most of the add-ons covered below come from the YouTube video [6 Essential Anki Addons for Learning Japanese in 2024](https://www.youtube.com/watch?v=ahGkFX4JPc8) by Jouzu Juls. He's done a number of Anki add-on videos and this is the most recent one (as of May 10th, 2026).

In practice, I don't think any of these add-ons (except for the first one which adds furigana abilities) are _essential_. In fact, I only installed the Japanese Support add-on and the Anki-Connect one.

The add-on that I would consider installing but didn't is the **heatmap add-on** that seems to pop up in many people's Anki videos (including Trenton's).

### 1. Japanese Support add-on

There are a number of fundamental add-ons that are maintained by the author of Anki, alongside Anki itself. The [Japanese Support add-on](https://ankiweb.net/shared/info/3918629684) is one of them.

Install it using code `3918629684`.

In Jouzu Juls's "6 Essential Anki Addons" video he introduces the Japanese Support add-on first but immediately bounces you to this [section](https://www.youtube.com/watch?v=gTX3v6zHiIA&t=20s) of his earlier video "5 Life Changing Anki Addons for Learning Japanese in 2022".

This add-on adds three new card types ("Japanese (recognition)" and [two more](https://ankiweb.net/shared/info/3918629684).

With these types, if you type e.g. `日本語` into the _Reading_ field and tab out, it will automatically fill the _Reading_ field with `日本語[にほんご]` which will be displayed as <ruby>日本語<rp>(</rp><rt>にほんご</rt><rp>)</rp></ruby> when reviewing the card.

Note: the add-on uses MeCab, so won't do great on things like 一階 so double check the furigana it generates are really what you want.

You don't have to use these card types but if you want the automatica filling in of one of your card type's fields with `日本語[にほんご]` then it'll only work if:

* The note type includes the word "Japanese" somewhere in its name, e.g. "My Textbook Japanese".
* You have a source field called "Expression" and a destination field called "Reading".

This feels a little restrictive to me. If you can live with adding readings manual to a field, i.e. entering the `[にほんご]` bit of `日本語[にほんご]` yourself then you just need to ensure that in the cards template, instead of having just `{{MyFieldName}}` (where `MyFieldName` is the name of the field where you enter things like `日本語[にほ>んご]`), you have `{{furigana:MyFieldName}}`.

**IMPORTANT:** The [Ruby Characters](https://docs.ankiweb.net/templates/fields.html#ruby-characters) section of the Anki manual warns that you need a space before the kanji for which a reading applies (or it'll mistakenly assume it applies to all preceding characters):

* Correct: `世[よ]の 中[なか]` becomes <ruby><rb>世</rb><rt>よ</rt></ruby>の<ruby><rb>中</rb><rt>なか</rt></ruby> (なか is correctly above 中).
* Incorrect: `世[よ]の 中[なか]` becomes <ruby><rb>世</rb><rt>よ</rt></ruby><ruby><rb>の中</rb><rt>なか</rt></ruby> (なか is displayed over の中 as if they were a unit).

### 2. Pitch accent add-on

In his "6 Essential Anki Addons" video, Jouzu Juls goes on to cover:

* The pitch accent graph generator
* The quick color changing add-on (a general purpose color add-on that he uses to color cards according to pitch accent type, i.e. heiban etc.).

As you can batch apply these later, I'm leaving them for now.

### 3. Migaku

He then covers the Migaku add-on for producing n+1 cards, i.e. cards that contain one additional word beyond what you already know.

Again, I'm leaving this for now.

### 4. Anki-Connect and Yomitan

Along similar lines, is integrating Yomitan. This doesn't involve a Yomitan specific add-on, it just uses Anki-Connect (which I covered in my [`markdown-to-anki` repo `README`](https://github.com/george-hawkins/markdown-to-anki).

Once, you've got Anki-Connect installed, you need to go to Yomitan's settings in your browser and there, there's an Anki section where you can enable Anki integration (the notice for macOS users applies to ancient versions of macOS and _shouldn't_ be an issue for more recent versions).

Again, as a beginner, I'm leaving this for the moment (even tho' I've got Anki-Connect installed).

For more on Yomitan and Anki, see this [video](https://youtu.be/OJxndUGN8Cg) from _ToKini Andy_.

### 5. Native audio and play audio in browser

Add-on 5 is for retrieving native audio from the [Forvo site](https://forvo.com/languages/ja/#google_vignette).

Forvo _may_ be great but it's one of those ad overloaded sites.

At this stage, AI generated text-to-speech is so good that it's probably a good enough alternative.

See the text-to-speech section [here](../tale-with-all-hiragana/README.md) for pointers on which cloud models to use.

Note: back in his earlier 2022 video, Jouzu Juls actually instead recommends the Migaku add-on for native audio (and notes that the pitch-accent audio included in Yomichan, as it was before Yomitan, is sometimes wrong).

### 6. Beautify Anki add-on

A general Anki add-on to give Anki a more modern look.

Unfortunately, this add-on seems to break per-release:

* The original version, from Shorouk Abdelaziz, can be found [here](https://github.com/ShoroukAziz/Beautify-Anki) but the last commit was March 2023.
* Then hafatsat-anki maintained a [fork](https://github.com/hafatsat-anki/Beautify-Anki_2.0) for a while.
* But that too went stale and the current most active fork (last commit 3 months ago as of May 2026) is this [fork](https://github.com/MagicHome007/Beautify-Anki_2.0) from MagicHome007.

### More add-ons

#### Review Heatmap

In a much earlier [video](https://www.youtube.com/watch?v=gIZW_OimI9M), Jouzu Juls recommends the [Review Heatmap add-on](https://ankiweb.net/shared/info/1771074083) as a valuable motivation tool.

There are various heatmap add-ons but this is the only highly used one, it's [GitHub repo](https://github.com/glutanimate/review-heatmap) hasn't been updated since May 2022 but the fact that it's [support forum thread](https://forums.ankiweb.net/t/review-heatmap-official-support-thread/928) has recent messages that aren't all complaints implies it still works.

#### Edit Field During Review (Cloze)

I suspect correcting fields during review is a common thing to want to do, _ToKini Andy_ (in his video linked to above) uses [Edit Field During Review (Cloze)](https://ankiweb.net/shared/info/385888438).

I'm not sure what this adds over just pressing `e` while reviewing a card.

Deactivating a deck
-------------------

I have a deck that I use for experiments but which I don't want to review. A little oddly (IMHO), there's no direct way to disbale/deactivate/pause a deck to remove its cards from review.

The generally accepted way to do this is:

* Go to the Browser in Anki.
* On the left sidebar, click the deck you want to disable.
* Press Ctrl+A (Windows/Linux) or Cmd+A (Mac) to select all cards.
* Press Ctrl+J (Windows/Linux) or Cmd+J (Mac) to toggle suspend. The cards will turn yellow.
