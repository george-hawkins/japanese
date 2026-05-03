import anthropic                                                                                                                                
                                                                                                                                                
SYSTEM_PROMPT = """You are a furigana annotator for Japanese text. Wrap every kanji in HTML5                                                    
ruby tags with the contextually correct reading in hiragana. Follow these rules exactly.                                                        
                                                                                                                                                
# Preservation (this is non-negotiable)                                                                                                         
- Reproduce the input character-for-character outside the ruby markup.                                                                          
  Do not correct typos, modernise 旧字体, normalise punctuation or                                                                              
  whitespace, expand numerals, swap 「」 for "", or change anything else.                                                                       
- Stripping every `<rt>...</rt>` from your output must yield the input                                                                          
  byte-for-byte.                                                                                                                                
- Output only the annotated text. No preamble, no trailing commentary,                                                                          
  no code fences, no markdown wrapping.                                                                                                         
                                                                                                                                                
# What to annotate                                                                                                                              
- Annotate EVERY kanji, including ones you think are obvious (私, 人,                                                                           
  日, 一, 中, 大, 上). No exceptions, no skipping for brevity.                                                                                  
- Group by word, not by character. Jukugo and inflected verbs/adjectives                                                                        
  take a single ruby block over their kanji portion; okurigana sits                                                                             
  outside the ruby:                                                                                                                             
    学校        →  <ruby>学校<rt>がっこう</rt></ruby>                                                                                           
    食べる      →  <ruby>食<rt>た</rt></ruby>べる                                                                                               
    出来事      →  <ruby>出来事<rt>できごと</rt></ruby>                                                                                         
    持ち帰る    →  <ruby>持<rt>も</rt></ruby>ち<ruby>帰<rt>かえ</rt></ruby>る                                                                   
- The iteration mark 々 stays inside the ruby of the kanji it repeats:                                                                          
    時々        →  <ruby>時々<rt>ときどき</rt></ruby>                                                                                           
- The small ヶ (in counter compounds like 一ヶ月, 三ヶ所, 数ヶ国) is
  not a standalone character with its own reading — it is part of
  the counter compound. Wrap the entire number + ヶ + counter
  sequence in a single ruby block, the same way 々 stays inside
  the ruby of the kanji it repeats:
    一ヶ月    →  <ruby>一ヶ月<rt>いっかげつ</rt></ruby>
    三ヶ所    →  <ruby>三ヶ所<rt>さんかしょ</rt></ruby>
    数ヶ国    →  <ruby>数ヶ国<rt>すうかこく</rt></ruby>
- Calendar dates are juxtaposed words, not compounds. Annotate the
  month and the day as separate ruby blocks:
    五月一日   →  <ruby>五月<rt>ごがつ</rt></ruby><ruby>一日<rt>ついたち</rt></ruby>
    七月七日   →  <ruby>七月<rt>しちがつ</rt></ruby><ruby>七日<rt>なのか</rt></ruby>
  This also lets context disambiguate day-of-month readings
  (一日 → ついたち in a date, いちにち for a duration; 二十日 →
  はつか in a date, にじゅうにち for a duration).
- Leave hiragana, katakana, digits, romaji, punctuation, and symbols                                                                            
  untouched.                                                                                                                                    
                                                                                                                                                
# Reading correctness                                                                                                                           
- Pick the reading a fluent Japanese reader would use in THIS context,                                                                          
  not the dictionary's most frequent reading. Disambiguate heteronyms                                                                           
  by surrounding text (上手, 何, 角, 入, 開, 描, 行く, 一日, 今日, 大人).                                                                       
- Render phonological surface forms, not concatenated dictionary                                                                                
  readings of components. Apply:                                                                                                                
    gemination (促音便):  一階 → いっかい,  出発 → しゅっぱつ,                                                                                  
                          一杯 → いっぱい,  失敗 → しっぱい                                                                                     
    rendaku (連濁):       花火 → はなび,    時々 → ときどき,                                                                                    
                          手紙 → てがみ                                                                                                         
    long vowels:          学校 → がっこう (not がくこう)                                                                                        
                                                                                                                                                
# Example                                                                                                                                       
Input:                                                                                                                                          
役者が舞台の右側、上手へと移動した。一階は満員だった。
                                                                                                                                                
Output:
<ruby>役者<rt>やくしゃ</rt></ruby>が<ruby>舞台<rt>ぶたい</rt></ruby>の<ruby>右側<rt>みぎがわ</rt></ruby>、<ruby>上手<rt>かみて</rt></ruby>へと<r
uby>移動<rt>いどう</rt></ruby>した。<ruby>一階<rt>いっかい</rt></ruby>は<ruby>満員<rt>まんいん</rt></ruby>だった。                              
"""
                                                                                                                                                
client = anthropic.Anthropic()

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

# Claude suggested the following snippet but admitted submitting SYSTEM_PROMPT on each turn
# of the loop wasn't great and suggested I ask it about how to do this batch style.
# Update: see book-annotation.md for a more cost-efficient approach.
for example in examples:
    print(example[0])
    text = example[1]
    print(f"{text} --> ", end="")

    # ----

    # To max out Claude, switch up the model and effort involved:
    # model="claude-opus-4-7",
    # output_config={"effort": "high"},
    message = client.messages.create(                                                                                                           
      model="claude-sonnet-4-6",
      max_tokens=16000,
      thinking={"type": "adaptive"},
      output_config={"effort": "medium"},
      system=[{
          "type": "text",
          "text": SYSTEM_PROMPT,
          "cache_control": {"type": "ephemeral"},
      }],
      messages=[{"role": "user", "content": text}],
    )                                                                                                                                           
                
    for block in message.content:
        if block.type == "text":
            print(block.text)

    # ----

    print("----")
