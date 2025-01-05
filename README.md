Japanese
========

Notes on starting to learn Japanese

Yomichan
--------

[Yomichan](https://github.com/FooSoft/yomichan) is the main browser extension for hovering over words on any webpage to see dictionary definitions.

**However**, the extension repo has been archived and the project sunsetted (see announcement [here](https://foosoft.net/posts/sunsetting-the-yomichan-project/)).

And the batton has been passed to Yomitan (see announcement [here](https://foosoft.net/posts/passing-the-torch-to-yomitan/)).

The Yomitan website is [here](https://yomitan.wiki/) and its GitHub repo is [here](https://github.com/yomidevs/yomitan).

**Update:** [Migaku](https://migaku.com/) (covered below in relation to video) also has a reading extension - I wonder how it compares to Yomitan - does it complement or compete/beat Yomitan?

### Yomitan dictionaries

After installing Yomitan, you have to install dictionaries - this is a bit confusing and I think they could have just clearly pointed out that the there's a _Get recommended dictionaries_ button in the extension's settings and you can just get these to start with rather than being overwhelmed with options.

Another oddity of Yomitan is that they still support displaying pitch accents (which many people consider to be a super important but under discussed aspect of Japanese) but they no longer include a link to where to retrieve one. The reason for this is covered in issue [#227](https://github.com/yomidevs/yomitan/issues/227), **TL;DR** they've decided the licensing isn't clear so removed reference to the dictionary they were using and leave it up to you to discover and download it.

You can find an old version (from August 2022) on the archived Yomichan repo on the [`dictionaries` branch](https://github.com/FooSoft/yomichan/tree/dictionaries) (search for "kanjium_pitch_accents.zip").

However, the dictionary is generated from the `accents.txt` file found [here](https://github.com/mifunetoshiro/kanjium/tree/master/data/source_files/raw) in the Kanjium repo. And this is updated very occasionally with corrections and additions (see [commit history](https://github.com/mifunetoshiro/kanjium/commits/master/data/source_files/raw/accents.txt)) and has some updates since 2022.

The `accents.txt` file can be downloaded and then converted to a Yomitan dictionary using the script [here](https://github.com/toasted-nutbread/yomichan-pitch-accent-dictionary) from toasted-nutbread (this is the same script used to create the archived `kanjium_pitch_accents.zip` linked to above).

### Usage and layout

Hold down `shift` and hover over a Kanji to see a popup with dictionary definitions.

I'm not crazy on the layout used in the popup but maybe I'll get used to it with time.

Basically, it munges input from all the underlying dictionary into a definition for a particular reading of the kanji. As there are multiple readings for every kanji, you get a list of such definitions, starting with the most common reading.

A definition starts with the kanji (with furigana) which you can click on to see the stroke order (and further details from the JANJIDIC dictionary).

And you see little green boxes showing e.g. "[BCCWJ | 288, 335]" which means this is the 288th most frequently used reading of the kanji in the BCCWJ frequency dictionary.

Anyway, the frequency gives you some kind of indication as to the importance of a particular reading.

See [here](https://learnjapanese.moe/yomichan/#recommended-frequency-dictionaries) for some indication as to how to interpret these numbers. Basically if the number is higher than 30,000 then it's "kind of uncommon".

If you've installed `kanjium_pitch_accents.zip` then you'll see the hiragana for this reading with a bar over those where the pitch goes up.

And finally, you get a classic foreign-language-dictionary style entry (from Jitendex) where it shows what the kanji means in English, it's grammatical role etc.

### Audio

You can click the audio button beside an entry to hear it spoken. However, many many entries have this button but no related audio (you click the button, it tries to retrieve the audio and gets nothing - only then is a little X added to the icon to indicate there's no audio). Initially, I thought I'd hit some kind of bug but it just seems to be that there's only audio for some small subset of entries. It's a pity they can't hide the audio button in these cases.

### Japanese to Japanese

The native Japanese dictionary that both _Matt vs Japan_ ([here](https://www.youtube.com/watch?v=5oxdPY9eH48&t=132s)) and _ToKini Andy_ ([here](https://youtu.be/OJxndUGN8Cg?t=120s)) is Suupaa Daijirin.

Daijirin is a popular Japanese dictionary and Suupaa Daijirin (aka Sūpā Daijirin aka スーパー大辞林) is a version of this dictionary (see its Wikipedia [entry](https://en.wikipedia.org/wiki/Daijirin)).

I suspect you're supposed to buy the electronic version of this dictionary (which comes in a standardized [EPWING](https://en.wikipedia.org/wiki/EPWING) format) and then import it into Yomitan (which supports importing the EPWING format - see [here](https://github.com/yomidevs/yomitan-import)).

I haven't tried installing it - I suspect many people are simply "acquiring" ZIPs of the dictionary and I don't know where you can buy it legally.

### Yomitan and Anki

See _ToKini Andy_'s [video](https://youtu.be/OJxndUGN8Cg).

### Unknowns

I'm not sure why the green frequency dictionary boxes often show more than one number, e.g. "288, 335".

If you click on e.g. the purple Jitendex "bubble" a closeable box appears, with the dictionary's name, at the bottom of the entry - I've no idea what this is for and googling and looking at the Yomitan site didn't enlighten me.

Anki
----

Trenton has a nice into to setting up Anki for Japanese where he doesn't go mad on add-ons. He covers vocab vs sentence decks (he's not particularly anti vocab cards).

He also recommends the [Kaishi 1.5K deck](https://github.com/donkuri/Kaishi) as a good bootstrapping deck - i.e. acquire enough basic vocab that you can actually make sentence cards where all but one of the words in the sentence is unknown to you.

iOS and Android dictionary
--------------------------

_Japanese_ used to be a very popular Japanese dictionary for both iOS and Android.

The site still exists [here](https://www.japaneseapp.com/) but it seems to be dead at this stage, its Android [Play page](https://play.google.com/store/apps/details?id=com.renzo.japanese&pli=1) shows it isn't available for any recent phones. And its iOS [App Store page](https://apps.apple.com/us/app/japanese/id290664053) shows it hasn't got an update since 2019.

Netflix
-------

Subscribing to Netflix Japan seems to have become very difficult in recent years - they've really clamped down on VPNs. And it's unclear to me if one can subscribe without a Japanese credit card.

It's not obvious that one can get a Japanese credit card without a non-tourist residence visa and Japanese address. It _may_ be possible to get a prepaid virtual card, without such identity verification, from [WebMonkey](https://en.komoju.com/blog/payment-method/webmoney/) or possibly [Kyash](https://thebestjapan.com/kyash-an-easy-alternative-to-credit-cards/) (I don't know if they have a virtual card or just a physical one).

Both NordVPN and ExpressVPN make a big deal of being suitable for use with Netflix but users report being frequently blocked.

You can find whether Netflix in your region has much Japanese language content using [uNoGS](https://unogs.com/) (unofficial Netflix online Global Search).

Just click _Advanced Search_, then _Uncheck All_ countries and just check your country, then set _Audio_ to _Japanese [Original]_ (and maybe set _Order_ to _Rating_) and click _Search_.

If you're logged into the Netflix website you can also search like this <https://www.netflix.com/browse/audio/jp>

Note: even Netflix Japan has none of the anime listed in [Top 10 Anime for Learning Real Japanese (JLPT N5 N4 level)](https://youtu.be/lktcZc9dYSI).

Crunchyroll
-----------

Crunchyroll has lots of anime but oddly it doesn't have Japanese subtitles. There are many theories as to why, e.g. that it's content is specifically licensed for non-Japanese markets.

Beginner anime
--------------

[Top 10 Anime for Learning Real Japanese (JLPT N5 N4 level)](https://youtu.be/lktcZc9dYSI) mentions:

* TODO

That Japanese Man Yuta in [How to Learn Japanese with Anime](https://www.youtube.com/watch?v=AXmPavo_quc) (at 5m 50s) suggests:

* Teasing Master Takagi-san / からかい上手の高木さん / Karakai Jōzu no Takagi-san

Pitch accent
------------

See _Dogen_'s [playlist](https://www.youtube.com/playlist?list=PLxMXdmBM9wPvsySiMoBzgh8d68xqKz1YP). It starts with lots of short videos and then ends with a 2h 30m lecture. His [Patreon](https://www.patreon.com/dogen) also has lots of pitch-accent, pronunciation and phonetics material.

See _Jouzu Juls_'s japanese pronounciation [video](https://www.youtube.com/watch?v=aOxRYmWDaF4) that recommends _Dogen_'s video but adds really useful pointers, e.g.:

* Using [minimal pairs](https://en.wikipedia.org/wiki/Minimal_pair) - he recommends the paid [Migaku Pitch Trainer](https://pitch-demo.migaku.io/) (but also mentions a free alternative - see below, it's the one Trenton mentions too).
* And if the whole thing is a complete struggle, he recommends a similar minimal pairs site but for music that has a [pitch section](https://www.musicca.com/exercises/circle/12) and an [interval section](https://www.musicca.com/exercises/circle/18) to get your brain attuned to the whole idea.

Matt vs Japan has a video with the infamous Ken Cannon where they discuss pitch accent but importantly also have exercises (around the 6m 30s mark - but the bits before are also important, e.g. not confusing stress in English with pitch accent): <https://www.youtube.com/watch?v=SaNr2xa4n3Q>

The `README` for the deck they created is [here](matt-ken-pitch-accent-deck/README.md), for the actual deck itself you need to use the link in the description section of the YouTube video.

Trenton (in this [video](https://www.youtube.com/watch?v=7fvCb5_Nzq4)) suggests this [minimal pairs test](https://kotu.io/tests/pitchAccent/minimalPairs) (which is an open source GitHub project).

Basically every major Japanese YouTuber has a pitch accent lesson (in some cases I've used a title taken from the content if the real title wasn't very clear):

* _That Japanese Man Yuta_ - [How To Learn Japanese Pitch Accent The Simple Way](https://www.youtube.com/watch?v=jp22QXysMHg).
* _Jouzu Juls_ - [Learn pitch accent before speaking](https://www.youtube.com/watch?v=aOxRYmWDaF4) (already linked above).
* _Matt vs Japan_ - [How to hear pitch accent](https://www.youtube.com/watch?v=SaNr2xa4n3Q) (and see joint video with Ken Cannon linked above).
* _Japanese Ammo with Misa_ - [Pitch Accent & Pronunciation playlist](https://www.youtube.com/playlist?list=PLd5-Wp_4tLqYkSIsRtsPbLIa0HnHkNzQW).
* _Kaname Naito_ - [Japanese Pronunciation: Pitch Accent Basics](https://www.youtube.com/watch?v=K8E-cU19PMs) and the newer [Basics of Japanese Pitch Accent](https://www.youtube.com/watch?v=jt04eg9T2sE)
* _Mochi real Japanese_ - [Japanese Pronuciation Practice](https://www.youtube.com/watch?v=D6wCNoFa0jU) (only very briefly touches on pitch accent at the 12m 10s mark).
* _Trenton_ - see above.
* _Dogen_ - see above.

Videos with text
----------------

I've noticed various people using a tool that allows them to watch anime etc. and see the Japanese text along with all kinds of highlighting and additions for learners (e.g. pitch accent indicators, furigana and the ability to lookup words and export to Anki - in fact the Anki integrations seems very sophisticated, it can keep track of words that you've already got covered in your Anki decks).

I haven't looked into whether everyone is using the same tool but _Jouzu Juls_'s recommends Migaku. However, there's a legacy and new version, see his [video](https://www.youtube.com/watch?v=TGV1GrZlTvg) covering why you _may_ want to use the legacy version (his main issue may be resolved by the time you read this).

I haven't found a definitive video for the extension but try these:

* _Livakivi_'s [The ULTIMATE Guide to SENTENCE MINING!](https://www.youtube.com/watch?v=QBcQJESGQvc).
* _Budget Livakivi_'s [How to Use And Set-Up Migaku For Sentence Mining (Japanese)](https://www.youtube.com/watch?v=4tKINZwRzVs).

Yes, both are from the same person but he maintains two channels.

Migaku
------

Works with:

* Netflix
* Disney+
* YouTube
* Rakuten Viki

Rakuten Viki looks interesting in that it seems to be truly global (i.e. content available everywhere). However, it has only two Japanese anime series and seems to be mainly romantic dramas.

YouTubers
---------

* [_Dogen_](https://www.youtube.com/@Dogen/videos) - _Dogen_ seems to be the king of japanese YouTubers but he mixes comedy (which may be a bit confusing/unhelpful for beginners) with serious content. Some of his content is only available to Patreons (see [here](https://www.patreon.com/dogen).
* [_Jouzu Juls_](https://www.youtube.com/@JouzuJuls/videos) - he isn't in the top league as far as subscribers go but I really like a lot of his videos.
* [_Matt vs Japan_](https://www.youtube.com/@mattvsjapan/videos) - he's another japanese YouTube star but unfortunately he seems to have ruined his reputation through activities outside YouTube (basically don't buy anything that's pushed by Matt) and hasn't produced any new YouTube content since early 2022. This all seems very sad as he comes across as very personable and I enjoy his videos and his YouTube persona is hard to reconsile with his behavior elsewhere (which you can find covered in videos like [this](https://www.youtube.com/watch?v=cfuENBQdEYo), [this](https://www.youtube.com/watch?v=OAXEjGkICrs) and [this](https://www.youtube.com/watch?v=zChi-zofP18) - the last one from Metatron gives Matt the greatest benefit of the doubt - there are many more similar videos on YouTube).
* [_ToKini Andy_](https://www.youtube.com/@ToKiniAndy/videos) - he's another YouTube star in this space and he's the one who tries hardest to take a structured taught approach to his content, he has lots of [playlists](https://www.youtube.com/@ToKiniAndy/playlists) that e.g. go through learning the kanji or working thru Genki where he really tries to teach the content he's presenting. My feeling he's more practical than many other YouTubers and just gets down to learning rather than talking about learning. He's also migrated all his Patreon content to a subscription based [site](https://www.tokiniandy.com/) (that I suspect is well worth it, from what I've seen from him, but I haven't tried it yet).
* [_Robin MacPherson_](https://www.youtube.com/@RobinMacPhersonFilms/videos) - Robin is the least Japanese specific of my picks here but I find his content engaging, e.g. [developing speaking skills alone](https://www.youtube.com/watch?v=QxHKkfbcRKQ) and he does have some Japanese specific content, e.g. this [grammar reference playlist](https://www.youtube.com/playlist?list=PLuIhQdwUVqqpq-aOnrEUjEq2oidCXbp9J).

Added later:

* [_That Japanese Man Yuta_](https://www.youtube.com/@ThatJapaneseManYuta)
* [_Japanese Ammo with Misa_](https://www.youtube.com/@JapaneseAmmowithMisa/videos) - Misa shows a more academic understanding of what she's talking about than most YouTubers (pointing out terms like [_okurigana_](https://en.wikipedia.org/wiki/Okurigana) which I like but her content is still very accessible, she just points out such terms but doesn't weigh her discussions down with this kind of language).
* [_Kaname Naito_](https://www.youtube.com/@kanamenaito/videos) - takes a more "teacher" like approach (but without yet having any lesson plan-like playlists) with e.g. good introductions to the [rhythm of Japanese](https://www.youtube.com/@kanamenaito/videos).
* [_Trenton_](https://www.youtube.com/@%E3%83%88%E3%83%AC%E3%83%B3%E3%83%88%E3%83%B3/videos) - he has some interesting takes on some things (but doesn't have many videos out at this stage).

Honorable mentions:

* [_Mochi real Japanese_](https://www.youtube.com/@mochirealjapanese3430/videos) - some of the content seems a little light weight but there's some good stuff in there.
* [_Weeb Jail_](https://www.youtube.com/@WeebJail/videos) - he's definitely the most [_otaku_](https://en.wikipedia.org/wiki/Otaku) of the creators linked here and most of his content is actually just English language anime related stuff but he does have some interesting Japanese language stuff (which he might have more usefully separated out into a second channel rather than having it mixed in with a sea of other stuff).
* [_Game Gengo_](https://www.youtube.com/@GameGengo/videos) - I haven't really decided what I make of this but it's an interesting idea - teeaching Japanese through video game content, e.g. he has a full [Genki 1 playlist](https://www.youtube.com/playlist?list=PLT12i1gB38HGAc-zjgFA4YcJA2Z3gVZTL) where he goes chapter by chapter through Genki book 1 and covers all its vocab and grammar using video game content.

Finally:

* [_Learn Japanese with JapanesePod101.com_](https://www.youtube.com/@JapanesePod101/videos) - there's tons of great free content from [JapanesePod101.com](https://www.japanesepod101.com/) but if you can afford it, I think it's better to get a premium subscription on their site and consume the content there - even though their video player isn't as good as YouTube's, the content is presented with a lot of extras (e.g. transcriptions, extra text-based content and exercises) and in a lesson-plan structure. And the YouTube videos are sometimes heavily edited down versions of those on their site (e.g. the ones on hiragana are missing the stroke-order sections and the example words using the just learnt kana).

Textbooks
---------

There are obviously no end of textbooks for Japanese. However, I wanted one that used kana and kanji from the start rather than romaji and the king in this area is [Genki](https://genki3.japantimes.co.jp/en/).

Note: while Genki uses kanji and kana, it still uses a lot of English, i.e. it doesn't try to teach Japanese through Japanese.

The publisher has a [self-study site](https://genki3.japantimes.co.jp/en/student/) for the book. And _ToKini Andy_ has a full [playlist](https://www.youtube.com/playlist?list=PLA_RcUI8km1NMhiEebcbqdlcHv_2ngbO2) going through each chapter of the book. He also has this [video](https://www.youtube.com/watch?v=S55aWpRaV44) on how to really self-study with Genki.

Another YouTube playlist for Genki is this [one](https://www.youtube.com/playlist?list=PLouxzmENUE6RU9KZH-oCAvzwEKR1r9YP1) from _ShiroNekoJapanese_ - I haven't had a chance to look at it but it's an impressive amount of content and is linked to by others.

And see this [playlist](https://www.youtube.com/playlist?list=PLnEKCkcXNkol_qrzZBJDpwb7VQaJPnXiQ).

And I'm not really sure what [this](https://www.youtube.com/playlist?list=PLT12i1gB38HGAc-zjgFA4YcJA2Z3gVZTL) is but it looks interesting - it may even be completely unrelated!

TODO: see which playlists really have value.

A new contender in this space is [Tobira](https://tobiraweb.9640.jp/) - _ToKini Andy_ compares it to Genki in this [video](https://www.youtube.com/watch?v=p60pe02X2O0).

Kanji
-----

_Matt vs Japan_ makes a very convincing case for [Remembering the Kanji 1](https://uhpress.hawaii.edu/title/remembering-the-kanji-1-a-complete-course-on-how-not-to-forget-the-meaning-and-writing-of-japanese-characters/) by James W. Heisig [here](https://www.youtube.com/watch?v=TgRte6oSoF8) (though note that in video description section he says "I COMPLETELY DISAGREE WITH THIS VIDEO NOW" but the unfortunate consensus is that this coincides with Matt's attempt to monetize things with his own content and the content of this 2018 video is more valuable than his later monetization efforts).

Anyway, Remembering the Kanji (often referred to on forums as just RTK) looks like a great start to me.

And an interesting app for training stroke order looks to be [Skritter](https://skritter.com/) - it's subscription based and relatively and I don't know how much if anything it really adds over e.g. Anki (while paid, I believe you can continue revising all content you've seen/learned already forvever even if you end your subscription).

An interesting aspect to Skritter is that they also have lots of content that's tied to other learning resources, e.g. you can practice the kanji in the order and way they're introduced in Genki.

They have a nice [blog post](https://blog.skritter.com/2021/05/the-ultimate-guide-to-japanese-stroke-order/) that provides a far more in-depth set of rules for stroke order than just the common simple top-to-bottom left-to-right rule.

See this [StackExchange question](https://japanese.stackexchange.com/q/204/66028) about the stroke order of 右 and 左 for an example of how things aren't so simple (the first two answers are the most valuable).

See reviews [here](https://ltl-school.com/skritter-review/), [here](https://www.joyokanjikai.com/learning-japanese/skritter-review/) and [here](https://www.youtube.com/watch?v=5Pglt4az_N0) (the last is by _Robin MacPherson_ who's mentioned above).

### Misc

You can find beautiful stroke order diagrams on [KanjiVG](https://kanjivg.tagaini.net/viewer.html?kanji=%E5%8F%B3) and using the data they provide you can use the [`kanjivg2svg` tool](https://github.com/Kimtaro/kanjivg2svg) to generate the kind of stroke order diagrams seen on [jisho.org](https://jisho.org/). Or you can download the full set of converted diagrams [here](https://www.reddit.com/r/LearnJapanese/comments/awr5vw/downloading_stroke_order_image/) (but see follow-ups covering issues and see if those issues have been addressed in the latest version of the file available on Google Drive).

Lookup kanji by drawing them using the [sci.lang.japan FAQ site](https://kanji.sljfaq.org/) (click the _Handwritten_ button).

Hirigana and katakana
---------------------

This seems to be a slam dunk, almost everyone seems to recommend these pages from Tofugu:

* [Hirigana](https://www.tofugu.com/japanese/learn-hiragana/)
* [Katakana](https://www.tofugu.com/japanese/learn-katakana/)

Note: there's a lot of free content but they also suggest buying their hirigana and katakana workbooks.

### Japanese keyboard

My notes on kana and typing Japanese on a computer (which is done using hirigana) are in [`kana.md`](kana.md).

I never found the perfect up-to-date resouce on how to get started with typing but actually it's fairly simple once you've got over the initial WTF step.

In short search YouTube and, despite most of them being stale when it comes to describing the basic initial setup, you'll get there eventually.

There's also lots of web pages out there (also with lots of stale information). One I liked is Christopher Bolton's [guide](https://redcocoon.org/cab/j4mactyping.html) (but again, it's far from perfect - it describes how to manage speedier input without choosing your kanji after ever individual compound but doesn't cover basics like switching from hiragana to katakana).

Comprehensible input
--------------------

Something that comes again and again is comprehensible input - input you can understand without having to have it explained in your native language.

Finding comprehensible input when you don't yet know anything seems difficult.

What I've found so far:

* [_Comprehensible Japanese_](https://www.youtube.com/@cijapanese/playlists) - they have a number of playlist, including a [complete beginner one](https://www.youtube.com/playlist?list=PLPdNX2arS9Mb1iiA0xHkxj3KVwssHQxYP). They also suggest you may get more value watching their videos on their [paid content site](https://cijapanese.com/watch) rather than YouTube and they have a [guide](https://cijapanese.com/guide/intro) to getting the most out of their content.
* _Refold_ have a ["seeder" playlist](https://www.youtube.com/watch?v=j-umeYLvhtU&list=PLn4GkF3M9WXeGgs4G_N_BfT62sfm1DSa3) - they explain how to use this to create a YouTube immersion account for yourself [here](https://www.youtube.com/watch?v=-zf5DGuD-XA) and then how to use this with a seeder playlist [here](https://www.youtube.com/watch?v=z3DiQgVF5e0).

They have a [full guide](https://refold.la/how-to-learn-japanese/) specifically for Japanese and it's got lots of free content as well as links to content that they sell (and some that they give away).

Online dictionary
-----------------

[jiisho](https://jisho.org/) is the clear king here - they pull together information from a lot of sources (see the footer at the bottom of the example linked just below).

E.g. see their page for the kanji [四](https://jisho.org/search/%E5%9B%9B%20%23kanji).

You can also do English word lookup as well as Romaji and Japanese characters.

Refold
------

Refold has suffered reputation damage due its association with _Matt vs Japan_ (see above) but my impression is that it's genuine even if it tries to push courses etc. that are somewhat (only somewhat) pricier than the norm in a world where so much is free.

Their biggest thing is their [Teach yourself a language course](https://refold.la/category/courses/) which they sell for around US$150. Way back when there was a very popular approach called AJATT (all Japanese all the time), unfortunately the website went offline a long time ago (you can find it archived [here](https://web.archive.org/web/20220322030954/http://www.alljapaneseallthetime.com/blog/)). It was never a particularly structured approach and since then a number of shots have been made at coming up with a more structured formulation including MIA (massive immersion approach) which has also gone the way of the dodo. Refold seems to be the best that's been done so far in picking up the AJATT mantle.

Don't be confused - their main course isn't about learning Japanese, it's a course about how to learn a language, any language, i.e. how you should go about it, immersion, the steps etc. But they then have lots of content - much of it for Japanese (although Refold is used by many language learners, their biggest Discord community is Japanese). Some of the content for Japanese is free and some paid. Some of this content gets a poor rap as some of it was produced by _Matt vs Japan_ and some people claim its rather slap-dash - I can't comment. But my impression is that Refold genuinely have made an attempt to get past the whole _Matt vs Japan_ debacle since parting ways with him (while continuing to use some content developed by him).

Miraa
-----

I haven't seen much about AI and language learning but [miraa](https://miraa.app/) looks interesting - see this [review](https://www.youtube.com/watch?v=o1kVdyLaxOA) by _Yuki Chiu_.

Shadowing
---------

I keep hearing about shadowing and it sounds very powerful but I don't have anything for this section yet.

Grammar
-------

### Bunpro

I keep on seeing reference to the site/web-app [Bunpro](https://bunpro.jp/) as a way to speed run learning Japanese grammar for self study. See Tofugu's [review](https://www.tofugu.com/reviews/bunpro/), Weeb Jail's [review](https://www.youtube.com/watch?v=hBOj45xt0vI) and others.

### Tae Kim

I keep seeing references to Tae Kim’s [Grammar Guide](https://guidetojapanese.org/learn/grammar) as an amazingly accessible guide to Japanese grammar, e.g. this [one](samland.md).

There's a corresponding Anki [deck](https://ankiweb.net/shared/info/911122782). It comes from [Japanese like a breeze](https://www.japanese-like-a-breeze.com/) and the follow-up decks are only available via their [Patreon](https://www.patreon.com/jlabjapanese).

The deck requires an addon (or you can edit the template to achieve the same degree of control) in order to e.g. hide romaji and show Kanji with furigana. For full instructions, see the deck's [manual](https://www.japanese-like-a-breeze.com/guide-for-beginners/). As the manual notes, the only thing you can change, without affecting ones ability to update to a newer version of the deck, is the template.

You can also customize the cards, e.g. move images to the back, as covered [here](https://www.japanese-like-a-breeze.com/card-customization/). How the addon and the decks are intended to be used is described in a number of YouTube videos, starting with this [one](https://www.youtube.com/watch?v=GHFcHfvgX5c).

### Cure Dolly

Cure Dolly is another Japanese teacher with a near religous following (and she has some issues with Tae Kim's take on things that's covered in this [playlist](https://www.youtube.com/playlist?list=PLg9uYxuZf8x9hoAsh5-fjGDBw-17O5oTy)).

She has a huge "from scratch" lesson series [playlist](https://www.youtube.com/playlist?list=PLg9uYxuZf8x_A-vcqqyOFZu06WlhnypWj).

Note: Jouzu Juls has a grammar [playlist](https://www.youtube.com/playlist?list=PLAaPL96Q8dWHx4H0WxdXLZlu7-DdbszsV) where he takes his shot at presenting some of her material in his own way where he hopes to "provide the same information with some enhancements and present it in a way that is open to more ears"

Piracy
------

I don't condone piracy but I have wanted to get digital versions of physical books that I've bought so that it's easier to e.g. copy things from them into flash cards. I don't think it's reasonable that one should have to pay for a digital version for this purpose if one has already bought a physical copy and I'd rather not work with DRM encumbered digital copies.

The solution to this is to download digital copies from [Anna'a Archive](https://annas-archive.org/).

TODO
----

Look at this sites that come up again and again:

* [JapanesePod101](https://www.japanesepod101.com/), they have no end of free content, e.g. this [4 hour intro to Japanese](https://www.youtube.com/watch?v=XCILw-a0sdA) (despite the somewhat click-bait title, it seems good) but also have paid content (oddly the seem to have released this video a number of times on their channel, e.g. [here it is again](https://www.youtube.com/watch?v=8YV8KmfBbBM) four years earlier).
* [Rocket Japanese](https://www.rocketlanguages.com/japanese) - I know nothing about this but it seems to be a competitor to JapanesePod101.

