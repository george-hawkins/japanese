import spacy

# Load the GiNZA model into the spaCy framework
nlp = spacy.load("ja_ginza") 

def to_readings(text):
    doc = nlp(text) # This is where the magic happens

    for token in doc:
        # `get` always returns list but for "Reading", it always had 0 or 1 elements.
        reading_list = token.morph.get("Reading")
        reading = reading_list[0] if reading_list else "<no reading>"
        print(f"{token.text} --> {reading}")

examples = [
    ["人気 reads as hitoke (rather than ninki)", "真夜中の公園には全く人気がなかった。"], # ja_ginza fails
    ["上手 reads as kamite (rather than jōzu)", "役者が舞台の右側、上手へと移動した。"], # ja_ginza passes
    ["上手 reads as jōzu", "彼はテニスが上手ですね。"], # ja_ginza passes
    ["生物 reads as namamono (rather than seibutsu)", "生物ですので、冷蔵庫に入れてください。"], # ja_ginza fails
    ["一階 reads as いっかい", "トイレは一階にあります。"], # ja_ginza fails
    ["一日 reads as ついたち", "五月一日は私の誕生日です。"], # ja_ginza passes
    ["明後日 reads as あさって", "明後日、友達と映画を見ます。"], # ja_ginza fails
    ["一日中 reads as いちにちじゅう", "今日は一日中雨が降っていました。"], # ja_ginza fails
    ["一ヶ月 read as いっかげつ", "一ヶ月に一回、実家に帰ります。"], # ja_ginza fails
]

for exampe in examples:
    print(exampe[0])
    to_readings(exampe[1])
    print("----")
