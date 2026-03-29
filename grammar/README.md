# Japanese Grammar

Tofugu:

* [Verb conjugation](https://www.tofugu.com/japanese-grammar/verb-conjugation-groups/).
* [て form](https://www.tofugu.com/japanese-grammar/te-form/).
* [い-adjectives](https://www.tofugu.com/japanese-grammar/i-adjective/)
* [な-adjectives](https://www.tofugu.com/japanese-grammar/na-adjective/)

Tools:

* Use <https://tableconvert.com/html-to-markdown> to convert Gemini tables to Markdown (ChatGPT has a direct copy-table-to-markdown button).
* To add furigana use [Get Furigana](https://furigana.netlify.app/) (see [`tale-with-all-hiragana/README.md`](tale-with-all-hiragana/README.md) for more details and other similar sites).

TODO:

* Add more of the all kana stories to `tale-with-all-hiragana` subdirectory.
* Find lists of most common katakana loanwords.
* Get good at reading both the kana stories and the loanwords out loud.
* Clause Connectors cheat sheet (けど etc.) - <https://chatgpt.com/c/68cae15a-3c64-832a-b4f1-9d51ae2d4c85>

# Verbs

**TLDR;** learn the dictionary form with the ~ます form to keep ichidan and godan verbs clear in your head.

Groups:

* Ichidan / 一段 / ru-verbs
* Godan / 五段 / u-verbs
* Irregular verbs

Many textbooks tell students to look for い-sound + る or え-sound + る in the hiragana trailing the kanji (called okurigana).

* 食べる (Ta-be-ru): The **べ (be)** is visible. It’s an え sound. Ichidan.
* 起きる (O-ki-ru): The **き (ki)** is visible. It’s an い sound. Ichidan.

This works for most verbs, but it fails for **two-syllable** verbs like **見る**.


In 見る (mi-ru), the "mi" is part of the kanji's reading. Because Japanese kanji usually represent at least one full syllable, there’s no room to "pull" the mi out into hiragana. If we wrote it as 見いる, it would be pronounced mi-i-ru, which isn't the word.
### How to tell for sure?

Since you can't always trust your eyes, you have to trust the conjugation.If a verb were Godan, the る would change to り before adding ます.

* 作る (tsuku-ru) $\rightarrow$ **作ります (tsuku-ri-masu)**. (Godan)
* 見る (mi-ru) $\rightarrow$ If it were Godan, it would be mi-ri-masu. But it’s not! It’s **見ます (mi-masu)**.

## Ichidan / Ru-verbs

Ru-verbs are easy, just drop the る.

| Form                | Example                 |
| ------------------- | ----------------------- |
| **Polite (ます)**    | 食べる → **食べ**ます          |
| **Negative (ない)**  | 食べる → **食べ**ない          |
| **て / た form**     | 食べる → **食べ**て / **食べ**た |
| **Volitional**      | 食べる → **食べ**よう          |

## Godan / u-verbs

| Form                | Example                |
| ------------------- | ---------------------- |
| **Polite (ます)**   | 書く → **書き**ます          |
| **Negative (ない)** | 書く → **書か**ない          |
| **て / た form**    | see below |
| **Volitional**      | 書く → **書こ**う           |

The て / た form depends on final consonant group (-く, -ぐ, -す, -つ, -ぬ, etc.). See below.

## Fake ichidan verbs

* 50% of verbs ending in ~iru are Godan.
* 1% of verbs ending in ~eru are Godan.

The only common ~eru Godan verbs:

* 帰る (kaeru): To return home
* 減る (heru): To decrease
* 蹴る (keru): To kick
* 焦る (aseru): To be in a hurry

Don't confuse 帰る (kaeru) with 変える (kaeru) - to change - which is a real Ichidan verb.

Most common ~iru Godan verbs:

| The "Fake" Ichidan | Meaning | Why it's a trap                                        |
|---|---|--------------------------------------------------------|
| 要る (iru) | To need | Sounds like いる (to exist), a "real" Ichidan verb.      |
| 知る (shiru) | To know | Very high frequency.                                   |
| 入る (hairu) | To enter | Very high frequency.                                   |
| 走る (hashiru) | To run | Very high frequency.                                   |
| 切る (kiru) | To cut | Sounds like 着る (to wear), a "real" Ichidan. |
| 参る (mairu) | To go/come | Essential for polite/humble speech.                    |

## Irregular verbs

There are only four irregular verbs - する, 来る, 行く and ある.

And only する (to do) and <ruby>来<rp>(</rp><rt>く</rt><rp>)</rp></ruby>る (to come) are fully irregular.

| Form             | Conjugation |
| ---------------- | ----------- |
| Dictionary       | する          |
| Stem | し           |
| Polite           | します         |
| Negative         | しない         |
| Volitional       | しよう         |
| Te-form          | して          |
| Past             | した          |

来る is stranger, notice the こ reading in the negative and volitional forms (even though the kanji remains the same).

| Form        | Conjugation |
| ----------- | ----------- |
| Dictionary  | 来る（くる）      |
| Stem        | 来（き）        |
| Polite      | 来ます（きます）    |
| Negative    | 来ない（こない）    |
| Volitional  | 来よう（こよう）    |
| Te-form     | 来て（きて）      |
| Past        | 来た（きた）      |


行く is only irregular in the て/た forms:

| Form | Expected regular form | Actual irregular form |
|------|-----------------------|-----------------------|
| Te-form | いて | いって |
| Past | いた | いった |

It's sometimes called a **pseudo-irregular** because it’s really just an exception to the phonological rule, not a different conjugation pattern.

ある (to exist – inanimate) has a regular polite form (ありません) but the plain negative is ない rather than あらない.

And as ない it behaves like an i-adjective:

| Form      | Example |
| --------- | ------- |
| Present   | ない      |
| Past      | なかった    |
| Te-form   | なくて     |
| Adverbial | なく      |

**Note**: technically くれる (someone gives to me), あげる (I give to someone) and くださる (a superior gives to me) are also irregular when it comes to honorific forms but let's ignore that for now.

## Copula conjugation

です looks like a verb, behaves a bit like one, and often gets conjugated as if it were — but technically, it’s not a verb at all. In grammatical terms, it's a copula - a special kind of auxiliary word used to link a subject to a predicate (like “A is B”). While it acts like a verb in many ways, it doesn't in these ways:

* It doesn’t have a “stem” form.
* It doesn’t have a true て-form.
* It doesn’t take inflections like verbs do (no ですます-style variation beyond politeness).

| Meaning                      | Polite                           | Plain (Casual)           | Notes                                            |
|------------------------------| -------------------------------- | ------------------------ |--------------------------------------------------|
| **Affirmative<br>(Present)** | です                           | だ                    | “is / am / are”                                  |
| **Negative<br>(Present)**    | ではありません or じゃありません       | ではない or じゃない     | Both では and じゃ are common;<br>じゃ is more casual. |
| **Affirmative<br>(Past)**    | でした                          | だった                  | “was / were”                                     |
| **Negative<br>(Past)**       | ではありませんでした or じゃありませんでした | ではなかった or じゃなかった | Again, じゃ is the casual contraction.             |


# て form

Ichidan verbs are easy! Replace る with て. For example, the て form of 見る (to see) is:

> 見る → 見　+　て　=　見て

Short aside - adjectives also have a て form:
* い-adjectives: 高い → 高 + く + て = 高くて (たかくて)
* な-adjectives: 元気です → 元気で (で is the て form of です)

## Godan

| Ending | て-form ending | Example | て-form (with furigana) |
|---|---|---|---|
| う | って | <ruby>買<rp>(</rp><rt>か</rt><rp>)</rp></ruby>う | 買って（かって） |
| つ | って | <ruby>待<rp>(</rp><rt>ま</rt><rp>)</rp></ruby>つ | 待って（まって） |
| る | って | <ruby>取<rp>(</rp><rt>と</rt><rp>)</rp></ruby>る | 取って（とって） |
| く | いて | <ruby>書<rp>(</rp><rt>か</rt><rp>)</rp></ruby>く  | 書いて（かいて） |
| す | して | <ruby>話<rp>(</rp><rt>はな</rt><rp>)</rp></ruby>す | 話して（はなして） |
| ぐ | いで | <ruby>泳<rp>(</rp><rt>およ</rt><rp>)</rp></ruby>ぐ | 泳いで（およいで） |
| ぬ | んで | <ruby>死<rp>(</rp><rt>し</rt><rp>)</rp></ruby>ぬ | 死んで（しんで） |
| ぶ | んで | <ruby>遊<rp>(</rp><rt>あそ</rt><rp>)</rp></ruby>ぶ | 遊んで（あそんで） |
| む | んで | <ruby>飲<rp>(</rp><rt>の</rt><rp>)</rp></ruby>む | 飲んで（のんで） |

## 1. Recognize the “sound families”

Godan verbs’ て-form endings are based on **phonetic groups** of their dictionary-form endings. Think of it as:

| Final kana | て-form ending | Sound pattern hint                                                           |
| ---------- | ------------- | ---------------------------------------------------------------------------- |
| う, つ, る | って            | The “small つ” doubles the consonant. Imagine a *hard stop* in pronunciation. |
| ぬ, ぶ, む | んで            | Think nasal “ん” + past. It’s a soft stop for these ‘m/b/n’ sounds.           |
| く         | いて            | The k-sound “k→i” before て                                                   |
| ぐ         | いで            | The g-sound “g→i” before で                                                   |
| す         | して            | Just add して; “s→sh” sound change                                             |

Mnemonic for んで group:

> The verbs that “carry weight” (む = carry, ぶ = play, ぬ = die) get the nasal “n” in the past. Silly, but it sticks.

Mnemonic for って group:

> The “t” group verbs (う, つ, る) **hit hard**, like tapping a table → double つ → って.

## 2. Sound drills

Reading and saying the transformations aloud is **key**. For example:

| Dictionary | て-form | Pronounce-aloud drill          |
| ---------- | ------ | ------------------------------ |
| 飲む         | 飲んで    | No‑nda → No‑nda → No‑nda       |
| 遊ぶ         | 遊んで    | A‑so‑nda → A‑so‑nda → A‑so‑nda |
| 待つ         | 待って    | Mat‑ta → Mat‑ta → Mat‑ta       |
| 書く         | 書いて    | Kai‑ta → Kai‑ta → Kai‑ta       |

**Trick**: exaggerate the consonant or nasal sound while repeating; your brain forms a **muscle memory link**.

## 3. Mini “flashcard loop” for rapid recall

1. Write **dictionary form** on one side, て-form on the other (with furigana if needed).
2. Drill 5–10 verbs per day, **say them out loud**.
3. Shuffle the cards, repeat until you can recall the て-form **instantly**.
4. Bonus: group by **final kana ending**, e.g., all ぶ/む/ぬ verbs together. This reinforces the sound pattern.

## 4. Recognize exceptions

* 行く → 行って
* する → して
* 来る → 来て（きて）

## Godan て-Form Cheat Sheet

| Sound Group | て-form ending     | Example Verbs |
|-----------------------------------------------------------------------------------|-------------------|------------------------------------------------------------------------------|
| **う・つ・る → って**                                                                    | って                | 会う（あって）、<br>待つ（まって）、<br>取る（とって）                                              |
| **む・ぶ・ぬ → んで**                                                                    | んで                | 飲む（のんで）、<br>遊ぶ（あそんで）、<br>死ぬ（しんで）                                             |
| **く → いて**                                                                        | いて                | 書く（かいて）、<br>歩く（あるいて）                                                         |
| **ぐ → いで**                                                                        | いで                | 泳ぐ（およいで）、<br>急ぐ（いそいで）                                                        |
| **す → して**                                                                        | して                | 話す（はなして）、<br>出す（でして）                                                         |
| **Irregular Exception**                                                           | 行って、<br>して、<br>来て | 行く（いって）、<br>する（して）、<br>来る（きて）                                                |

### How to drill with this cheat sheet

1. **Say it aloud**: Emphasize the double consonant (って) or nasal (んで).
2. **Use flashcards**: Write dictionary form on one side, て-form (with furigana) on the other.

## Example sentences

| Verb                                           | Present                                                                                         | て form                                                                                                                                                                                                              | English                                         |
|------------------------------------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| <ruby>買<rp>(</rp><rt>か</rt><rp>)</rp></ruby>う  | パンを<ruby>買<rp>(</rp><rt>か</rt><rp>)</rp></ruby>う。                                               | パンを&ZeroWidthSpace;**<ruby>買<rp>(</rp><rt>か</rt><rp>)</rp></ruby>って**、<ruby>家<rp>(</rp><rt>いえ</rt><rp>)</rp></ruby>に<ruby>帰<rp>(</rp><rt>かえ</rt><rp>)</rp></ruby>りました。                                              | I bought bread and went home.                   |
| <ruby>待<rp>(</rp><rt>ま</rt><rp>)</rp></ruby>つ  | <ruby>友達<rp>(</rp><rt>ともだち</rt><rp>)</rp></ruby>を<ruby>待<rp>(</rp><rt>ま</rt><rp>)</rp></ruby>つ。 | <ruby>友<rp>(</rp><rt>とも</rt><rp>)</rp></ruby>だちを&ZeroWidthSpace;**<ruby>待<rp>(</rp><rt>ま</rt><rp>)</rp></ruby>って**、<ruby>映画<rp>(</rp><rt>えいが</rt><rp>)</rp></ruby>を<ruby>見<rp>(</rp><rt>み</rt><rp>)</rp></ruby>ました。 | I waited for my friend and watched a movie.     |
| <ruby>取<rp>(</rp><rt>と</rt><rp>)</rp></ruby>る  | <ruby>本<rp>(</rp><rt>ほん</rt><rp>)</rp></ruby>を<ruby>取<rp>(</rp><rt>と</rt><rp>)</rp></ruby>る。    | <ruby>本<rp>(</rp><rt>ほん</rt><rp>)</rp></ruby>を&ZeroWidthSpace;**<ruby>取<rp>(</rp><rt>と</rt><rp>)</rp></ruby>って**、<ruby>読<rp>(</rp><rt>よ</rt><rp>)</rp></ruby>みました。                                                  | I took a book and read it.                      |
| <ruby>書<rp>(</rp><rt>か</rt><rp>)</rp></ruby>く  | <ruby>手紙<rp>(</rp><rt>てがみ</rt><rp>)</rp></ruby>を<ruby>書<rp>(</rp><rt>か</rt><rp>)</rp></ruby>く。  | <ruby>手紙<rp>(</rp><rt>てがみ</rt><rp>)</rp></ruby>を&ZeroWidthSpace;**<ruby>書<rp>(</rp><rt>か</rt><rp>)</rp></ruby>いて**、<ruby>送<rp>(</rp><rt>おく</rt><rp>)</rp></ruby>りました。                                               | I wrote a letter and sent it.                   |
| <ruby>話<rp>(</rp><rt>はな</rt><rp>)</rp></ruby>す | <ruby>先生<rp>(</rp><rt>せんせい</rt><rp>)</rp></ruby>と<ruby>話<rp>(</rp><rt>はな</rt><rp>)</rp></ruby>す | <ruby>先生<rp>(</rp><rt>せんせい</rt><rp>)</rp></ruby>と&ZeroWidthSpace;**<ruby>話<rp>(</rp><rt>はな</rt><rp>)</rp></ruby>して**、<ruby>質問<rp>(</rp><rt>しつもん</rt><rp>)</rp></ruby>しました。                                          | I talked with the teacher and asked a question. |
| <ruby>泳<rp>(</rp><rt>およ</rt><rp>)</rp></ruby>ぐ | <ruby>海<rp>(</rp><rt>うみ</rt><rp>)</rp></ruby>で<ruby>泳<rp>(</rp><rt>およ</rt><rp>)</rp></ruby>ぐ。   | <ruby>海<rp>(</rp><rt>うみ</rt><rp>)</rp></ruby>で&ZeroWidthSpace;**<ruby>泳<rp>(</rp><rt>およ</rt><rp>)</rp></ruby>いで**、<ruby>楽<rp>(</rp><rt>たの</rt><rp>)</rp></ruby>しかったです。                                              | I swam in the sea and it was fun.               |
| <ruby>死<rp>(</rp><rt>し</rt><rp>)</rp></ruby>ぬ  | その<ruby>魚<rp>(</rp><rt>さかな</rt><rp>)</rp></ruby>が<ruby>死<rp>(</rp><rt>し</rt><rp>)</rp></ruby>ぬ。 | その<ruby>魚<rp>(</rp><rt>さかな</rt><rp>)</rp></ruby>は&ZeroWidthSpace;**<ruby>死<rp>(</rp><rt>し</rt><rp>)</rp></ruby>んで**しまいました。                                                                                          | That fish ended up dying.                       |
| <ruby>遊<rp>(</rp><rt>あそ</rt><rp>)</rp></ruby>ぶ | <ruby>公園<rp>(</rp><rt>こうえん</rt><rp>)</rp></ruby>で<ruby>遊<rp>(</rp><rt>あそ</rt><rp>)</rp></ruby>ぶ | <ruby>公園<rp>(</rp><rt>こうえん</rt><rp>)</rp></ruby>で&ZeroWidthSpace;**<ruby>遊<rp>(</rp><rt>あそ</rt><rp>)</rp></ruby>んで**います。                                                                                            | I am playing in the park.                       |
| <ruby>飲<rp>(</rp><rt>の</rt><rp>)</rp></ruby>む  | コーヒーを<ruby>飲<rp>(</rp><rt>の</rt><rp>)</rp></ruby>む。                                             | コーヒーを&ZeroWidthSpace;**<ruby>飲<rp>(</rp><rt>の</rt><rp>)</rp></ruby>んで**、<ruby>働<rp>(</rp><rt>はたら</rt><rp>)</rp></ruby>きました。</div>                                                                                   | I drank coffee and worked.                      |

## Songs

* [Hatsune Miku imitation](https://www.youtube.com/watch?v=Cj-P-nEPoe0)
* [ToKini Andy](https://www.youtube.com/watch?v=Dfh5FyVdhUI)
* [Nihongo Ninja / My Neighbor Totoro](https://www.youtube.com/watch?v=2ARid5LeHAw)
* [Yuko Sensei](https://www.youtube.com/watch?v=PWQacyKoiT0)
* [Shino Sensei](https://www.youtube.com/watch?v=W_M3KHy3z48)
* [Thanawan Pinlaem](https://www.youtube.com/watch?v=uW1YcozsWh4)

# Adjectives

い-adjectives like "self-powered" cars—they have their own engines (conjugations) built-in. な-adjectives are more like "trailers"—they are basically nouns that need a hitch (a copula like です/だ) to go anywhere.

| Context | い-adjective (e.g., 寒い) | な-adjective (e.g., 元気) |
|---|---|---|
| Modifying a Noun | 寒い日 (Cold day) | 元気な人 (Energetic person) |
| Ending a Sentence | 寒い。 (It's cold.) | 元気です。 (I'm energetic.) |
| Connecting to a Verb | 寒くて、寝た。 (It was cold and I slept.) | 元気で、食べた。 (I was energetic and I ate.) |

Watch out, not all adjectives that end in ~い are い adjectives.

$i$-adjectives: These always end in ~ai, ~ii, ~ui, or ~oi. They are "true" adjectives that carry their own conjugation power
* $na$-adjectives: These essentially behave like nouns. Even if they end in "i" (like kirei), they need a helper verb (like desu or dewa arimasen) to function.

Both kirei and kawaii have kanji and all kana forms:

* 可愛い / かわいい - the kana form is more common but the kanji form is generally used in standard/formal contexts.
* 綺麗 / きれい - generally written in kana form.

かわいい is a true i-adjective while きれい is a na-adjective.

Example conjugation with ありません. Since $na$-adjectives behave like nouns, you don't change the word at all. You just change the polite ending (です) to the negative ending (ではありません).

* かわいい → かわい + く + ありません → かわいくありません
* きれいです → きれい + ではありません → きれいではありません

Other common fake i-adjectives:

* 有名 (ゆうめい) - famous
* 嫌い (きらい) - dislike / hate
* 得意 (とくい) - good at

### The "Noun Mimicry" Test

The easiest way to see that kirei is a noun in disguise is to compare it to a standard noun, like gakusei (student). Watch how they behave identically in these sentences:

| Sentence Type    | Noun (Gakusei)        | Na-Adjective (Kirei) | I-Adjective (Kawaii) |
|------------------|-----------------------|----------------------|----------------------|
| Modifying a Noun | Gakusei no hon        | Kirei na hito        | Kawaii hito          |
| Present Polite   | Gakusei desu          | Kirei desu           | Kawaii desu          |
| Negative Polite  | Gakusei dewa arimasen | Kirei dewa arimasen  | Kawaiku arimasen     |
| Past Polite      | Gakusei deshita       | Kirei deshita        | Kawaikatta desu      |

Notice that gakusei and kirei rely entirely on the copula (the "to be" verb like desu or dewa arimasen) to tell you the tense. The words themselves are static. Kawaii, the "true" adjective, actually changes its own internal structure.

### ではないです - formal to polite

If you look at the phrase as a hierarchy of formality, it looks like this:

* きれいではないです (Formal/Written/Careful speech)
* きれいじゃないです (Daily polite speech - most common)
* きれいではない (Plain/Formal written)
* きれいじゃない (Casual/Informal)

The で (de) is the te-form of the copula です. You use the te-form of the copula to link a noun or na-adjective to the next part of the sentence. Historically, this evolved from にて (ni te) in Classical Japanese. Over time, ni te shortened to de. So, when you say de nai, you are literally saying "Being [X], [it] does not exist."

The は (wa) is the topic market, in negative sentences, its job is contrast. It implies: "As for this specific quality (cleanliness), it is not."

In casual, spoken Japanese the sounds in では blended in over centuries: では → じゃ.

ない means "not", but is grammatically an i-adjective. Because きれい (kirei) is a na-adjective (which behaves like a noun), you can't just stick the adjective nai directly onto it. You need a bridge.

* **Structure**: [Noun/Na-Adj] + で + [Negative Adjective]
* **Literal logic**: "In the state of being clean, [it] does not exist."

きれいではない is a complete, grammatically correct sentence. However, ending a sentence with an adjective is considered "plain form" (casual). To make an adjective polite in Japanese, you simply tack です onto the very end of the sentence.

#### The Meaning of "Na"

You might wonder: "If it's a noun, why is it called a na-adjective?"

When you want to describe a noun directly (e.g., "a beautiful flower"), you can't just put two nouns together without a bridge.

* **Noun + Noun**: Gakusei **no** hon (The student's book).
* **Adjectival Noun + Noun**: Kirei **na** hana (A beautiful flower).

Historically, **na** is a contraction of **ni aru** (to exist as). So, kirei na hana literally meant "a flower that exists in a state of beauty." Because they need this special particle (na) to modify things, we call them na-adjectives, but their "bones" are purely noun-based.

Aside: In Japanese, the group of i-adjectives is a "closed class." It is very rare for a new i-adjective to be created. Almost every new descriptive word added to the language—whether it's a loanword or a new concept—becomes a na-adjective (a noun).

### Nouns and true adjectives

In Japanese, the distinction between "verbs" and “adjectives” is not as sharp as it is in English. Traditional Japanese grammar treats both of them as types of inflecting predicates — words that can function as the main predicate of a sentence, change form for tense or polarity, and don’t need a copula like “to be.”

For more on this and where na-adjectives fit in, see this [ChatGPT answer](https://chatgpt.com/share/69c9400d-2828-832f-80bc-231d2f6a8638).


### 少ない and other adjectives that end in -ない

少ない and some other adjectives end in -ない in their base forms (and their core meaning is negative). They aren't negations of some other positive adjective. For a bit more, see this [Gemini answer](https://gemini.google.com/app/f607e9c3d1684311).

## The only irregular adjective - いい / よい

The adjective いい (“good”) is irregular because its historical form よい is used in most conjugations:

| Form       | Example |
| ---------- | ------- |
| Dictionary | いい      |
| Past       | よかった    |
| Negative   | よくない    |
| Te-form    | よくて     |

Note: よく (often) is actually the adverbial form of いい.
