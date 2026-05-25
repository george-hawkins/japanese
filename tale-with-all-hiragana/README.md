Furigana
--------

I used <https://nihongodera.com/tools/convert> to add furigana to the text and used Google Chrome _Inspect_ to copy the resulting HTML.

However, the author of NihongoDera is shutting down his site.

An alternative might be <https://github.com/mornir/get-furigana>

The associated app <https://furigana.netlify.app/> seems to work well (but oddly localizes the UI language to Vietnamese for me).

Or:

* <https://muriapp.com/en/furigana/>
* <https://kanjikana.com/en/tools/furigana>
* <https://www.jcinfo.net/en/tools/kana> (ad laden).

Note: I later found that none of these are entirely satisfactory for things like 一階 (they're a bit too simple minded and produce the reading いちかい rather than いっかい). See [here](../furiganaize/README.md) for more on this topic.

Text-to-speech
--------------

For text conversion try: <https://console.cloud.google.com/vertex-ai/studio/media/speech>

Use:

* Model: Chirp 3: HD Voices
* Language: Japanese (Japan)
* Voice: Aoede (Female) or Achird (Male)

Note: according to Gemini, Aoede is the current flagship voice and Achird is the best male voice.

Gemini says that when using the API, Aoede has ID `ja-JP-Chirp3-HD-D` and Achird has ID `ja-JP-Chirp3-HD-B`.

According to Gemini and ChatGPT, Microsoft Azure Neural HD should also be very good.

Toggling furigana
-----------------

Also included here is [`tale-with-js.html`](tale-with-js.html) along with a `.js` and `.css` file.

If you open this in a browser, you can toggle the furigana on and off in the story at the click of a button.

The page also uses the [Klee One](https://fonts.google.com/specimen/Klee+One) font. It's the nearest thing to a [textbook-style font](../kyoukasho-fonts.md) that's freely available.
