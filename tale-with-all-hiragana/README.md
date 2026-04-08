I used <https://nihongodera.com/tools/convert> to add furigana to the text and used Google Chrome _Inspect_ to copy the resulting HTML.

However, the author of NihongoDera is shutting down his site.

An alternative might be <https://github.com/mornir/get-furigana>

The associated app <https://furigana.netlify.app/> seems to work well (but oddly localizes the UI language to Vietnamese for me).

Or:

* <https://muriapp.com/en/furigana/>
* <https://kanjikana.com/en/tools/furigana>
* <https://www.jcinfo.net/en/tools/kana> (ad laden).

For text conversion try: <https://console.cloud.google.com/vertex-ai/studio/media/speech>

Use:

* Model: Chirp 3: HD Voices
* Language: Japanese (Japan)
* Voice: Aoede (Female) or Achird (Male)

Note: according to Gemini, Aoede is the current flagship voice and Achird is the best male voice.

Gemini says that when using the API, Aoede has ID `ja-JP-Chirp3-HD-D` and Achird has ID `ja-JP-Chirp3-HD-B`.

According to Gemini and ChatGPT, Microsoft Azure Neural HD should also be very good.
