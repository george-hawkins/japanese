#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Say what kind of Japanese character a single Unicode character is."""

import argparse
import csv
import sys
import textwrap
import unicodedata
from pathlib import Path

TABLE = Path(__file__).resolve().parent / "kanji-categories.tsv"

# name: (short title, longer explanation for --help)
CATEGORIES = {
    "jōyō": (
        "general-use kanji",
        "Jōyō kanji (常用漢字): the 2,136 kanji of the official list for general use, plus the 4 accepted alternative forms (叱 剥 頬 填) that most fonts produce. The output says when each joined the list; the 196 added in 2010 mostly weren't simplified the way earlier ones were.",
    ),
    "jinmeiyō": (
        "name kanji",
        "Jinmeiyō kanji (人名用漢字): the 864 further kanji allowed in personal names, including old forms of jōyō kanji (亞, 國) and the 5 kanji dropped from the jōyō list in 2010.",
    ),
    "hyōgai": (
        "common kanji outside the official lists",
        "Common hyōgai kanji (表外漢字): in neither official list, but met in ordinary modern print (嘘, 醤, 鮪). In the 表外漢字字体表 or JIS X 0208 level 1.",
    ),
    "rare": (
        "kanji used in Japan, but uncommon",
        "Kanji used in Japan but uncommon: name variants, old forms, and literary or specialist kanji (學, 嶌, 髙). In JIS X 0208 level 2 or JIS X 0213.",
    ),
    "chinese": (
        "used in modern Chinese, not Japanese",
        "A character of modern Chinese that isn't used in Japanese (们, 她, 东): in no Japanese standard, but in a current Chinese one.",
    ),
    "obscure": (
        "ideograph with no modern use",
        "Any other CJK ideograph: historical, dictionary-only or regional, with no modern use in Japanese or standard Chinese.",
    ),
    "component": (
        "a part of kanji, not a kanji",
        "A part of kanji rather than a kanji: a radical or stroke code point (⼈, ⺅, ㇏), or a part that Unicode encodes as an ideograph (氵, 宀, 辶).",
    ),
    "hiragana": (
        "hiragana",
        "Modern hiragana: あ to ん, their voiced forms, and small ぁぃぅぇぉっゃゅょ.",
    ),
    "katakana": (
        "katakana",
        "Modern katakana: ア to ン, their voiced forms and the small forms, plus ヴ, ヵ, ヶ and the long vowel mark ー.",
    ),
    "halfwidth": (
        "half-width katakana",
        "Half-width katakana (ｱ, ｶ, ｰ): legacy forms of modern katakana.",
    ),
    "kana-rare": (
        "rare kana",
        "Kana that are still valid but seldom seen: ゎ ヮ ゔ ゕ ゖ ヷ ヸ ヹ ヺ, and the iteration marks ゝ ゞ ヽ ヾ.",
    ),
    "kana-obsolete": (
        "obsolete kana",
        "Kana no longer used: ゐ ゑ ヰ ヱ, the ligatures ゟ and ヿ, archaic letters, and historical small kana.",
    ),
    "hentaigana": (
        "variant hiragana",
        "Hentaigana (変体仮名): variant hiragana dropped when one form per syllable was fixed in 1900, now only on shop signs and in calligraphy.",
    ),
    "kana-ext": (
        "kana for other languages",
        "Kana for other languages: the small katakana for Ainu (ㇰ to ㇿ) and the tone marks for Taiwanese.",
    ),
    "symbol": (
        "Japanese punctuation or symbol",
        "Japanese punctuation and symbols (。、「」・々〆〒), and full-width forms of other characters (Ａ, １, ！).",
    ),
    "other": (
        "not a Japanese character",
        "Not a Japanese character at all (a, é, 한).",
    ),
}

# Characters worth a specific remark: {char: (category, note)}.
SPECIAL = {
    "々": ("symbol", "Kanji iteration mark (踊り字): repeats the kanji before it."),
    "〃": ("symbol", "Ditto mark."),
    "〆": ("symbol", "Closing mark, read しめ."),
    "〇": ("symbol", "Kanji numeral zero."),
    "ー": ("katakana", "Long vowel mark (長音符)."),
    "ｰ": ("halfwidth", "Half-width form of the long vowel mark ー."),
    "ヵ": ("katakana", "Small ka; as a counter (三ヵ月) it stands for 箇."),
    "ヶ": ("katakana", "Small ke; as a counter (一ヶ月) or in place names it stands for 箇 or が."),
    "・": ("symbol", "Middle dot (中黒), separating words or list items."),
    "゠": ("symbol", "Double hyphen, used in transcribed foreign names."),
}

# General symbols that aren't specific to Japanese but are a normal part of Japanese text.
COMMON_SYMBOLS = "※…‥―○◯×△□◎●☆★♪"

# Kana outside modern standard spelling, with what to say about each.
RARE_KANA = {
    "ゎ": "Small wa, only in historical spellings such as くゎ (kwa), now written か.",
    "ヮ": "Small wa, only in historical spellings such as クヮ (kwa), now written カ.",
    "ゔ": "Vu: the hiragana form of ヴ, which is nearly always written in katakana.",
    "ゕ": "Small ka: the hiragana counterpart of ヵ.",
    "ゖ": "Small ke: the hiragana counterpart of ヶ.",
    "ヷ": "Va: an older way of writing ヴァ.",
    "ヸ": "Vi: an older way of writing ヴィ.",
    "ヹ": "Ve: an older way of writing ヴェ.",
    "ヺ": "Vo: an older way of writing ヴォ.",
    "ゝ": "Iteration mark (踊り字): repeats the kana before it. Now mostly seen in names.",
    "ゞ": "Voiced iteration mark (踊り字): repeats the kana before it, voiced, as in いすゞ. Now mostly seen in names.",
    "ヽ": "Iteration mark (踊り字): repeats the kana before it. Now mostly seen in names.",
    "ヾ": "Voiced iteration mark (踊り字): repeats the kana before it, voiced. Now mostly seen in names.",
}
OBSOLETE_KANA = {
    "ゐ": "Wi: written い since the 1946 spelling reform.",
    "ゑ": "We: written え since the 1946 spelling reform.",
    "ヰ": "Wi: written イ since the 1946 spelling reform, though it survives in names such as ウヰスキー.",
    "ヱ": "We: written エ since the 1946 spelling reform, though it survives in names such as ヱビス.",
    "ゟ": "Ligature of より.",
    "ヿ": "Ligature of コト.",
}

# Blocks holding Japanese punctuation, symbols and full-width forms.
SYMBOL_RANGES = [
    (0x2FF0, 0x2FFF),  # ideographic description characters
    (0x3000, 0x303F),  # CJK symbols and punctuation
    (0x3099, 0x309C),  # kana voicing marks
    (0x3190, 0x319F),  # kanbun marks
    (0x31EF, 0x31EF),  # ideographic description character
    (0x3200, 0x33FF),  # enclosed CJK letters and months, CJK compatibility
    (0xFE10, 0xFE1F),  # vertical forms
    (0xFE30, 0xFE4F),  # CJK compatibility forms
    (0xFF00, 0xFF65),  # full-width ASCII, half-width punctuation
    (0xFF9E, 0xFF9F),  # half-width voicing marks
    (0xFFE0, 0xFFEE),  # full-width and half-width signs
    (0x1F200, 0x1F2FF),  # enclosed ideographic supplement
]
COMPONENT_RANGES = [(0x2E80, 0x2EFF), (0x2F00, 0x2FDF), (0x31C0, 0x31EE)]
IDEOGRAPH_RANGES = [(0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF), (0x20000, 0x3FFFF)]
KANA_NAMES = (
    "HIRAGANA LETTER", "HIRAGANA ITERATION", "HIRAGANA VOICED ITERATION", "HIRAGANA DIGRAPH", "HENTAIGANA LETTER",
    "KATAKANA LETTER", "KATAKANA ITERATION", "KATAKANA VOICED ITERATION", "KATAKANA DIGRAPH", "HALFWIDTH KATAKANA LETTER",
)


def in_ranges(ch, ranges):
    return any(first <= ord(ch) <= last for first, last in ranges)


def load_table():
    if not TABLE.exists():
        sys.exit(f"{TABLE.name} is missing; run build.py to generate it")
    with open(TABLE, encoding="utf-8", newline="") as f:
        return {row["char"]: row for row in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)}


def classify_kana(ch, name):
    """Return (category, title, list of detail lines) for a kana; title is None for the category's usual one."""
    script = "katakana" if "KATAKANA" in name else "hiragana"
    if "HENTAIGANA" in name:
        # Names look like "HENTAIGANA LETTER KA-3": the third variant for ka.
        syllable = name.removeprefix("HENTAIGANA LETTER ").split("-")
        which = f" the syllable {syllable[0].lower()}" if len(syllable) == 2 else " a syllable"
        return "hentaigana", None, [f"A variant way of writing{which}, not used in modern Japanese."]
    if "MINNAN" in name:
        return "kana-ext", None, ["Tone mark for writing Taiwanese in katakana."]
    if 0x31F0 <= ord(ch) <= 0x31FF:
        return "kana-ext", None, ["Small katakana for writing Ainu."]
    if name.startswith("HALFWIDTH"):
        return "halfwidth", None, [f"Half-width form of {unicodedata.normalize('NFKC', ch)}."]
    if ch in OBSOLETE_KANA:
        return "kana-obsolete", f"obsolete {script}", [OBSOLETE_KANA[ch]]
    if "ARCHAIC" in name:
        return "kana-obsolete", f"obsolete {script}", ["Archaic kana for a sound that the modern syllabary doesn't distinguish."]
    if ord(ch) >= 0x1B130:
        return "kana-obsolete", f"obsolete {script}", ["Small kana from historical texts."]
    if ch in RARE_KANA:
        return "kana-rare", f"rare {script}", [RARE_KANA[ch]]
    return script, None, ["Small kana."] if "SMALL" in name else []


def classify(ch, table):
    """Return (category, title, list of detail lines) for a single character; title is None for the category's usual one."""
    name = unicodedata.name(ch, "")
    if ch in table:
        row, details = table[ch], []
        if row["note"]:
            details.append(row["note"])
        if row["variants"]:
            details.append(f"Variants: {row['variants']}")
        standards = []
        if row["jis_level"]:
            standards.append(f"JIS X {'0208' if row['jis_level'] in '12' else '0213'} level {row['jis_level']}")
        if row["freq_rank"]:
            standards.append(f"newspaper frequency rank {row['freq_rank']}")
        if standards:
            details.append(", ".join(standards) + ".")
        if row["meaning"]:
            details.append(f"Meaning: {row['meaning']}")
        return row["category"], None, details

    if ch in SPECIAL:
        return SPECIAL[ch][0], None, [SPECIAL[ch][1]]
    if name.startswith(KANA_NAMES):
        return classify_kana(ch, name)

    if ch in COMMON_SYMBOLS:
        return "symbol", None, ["A general symbol, not specific to Japanese but common in Japanese text."]
    if in_ranges(ch, SYMBOL_RANGES) and "HANGUL" not in name and "KOREAN" not in name:
        details = []
        plain = unicodedata.normalize("NFKC", ch)
        if name.startswith("FULLWIDTH") and plain != ch:
            details.append(f"Full-width form of {plain!r}.")
        elif name.startswith("HALFWIDTH") and plain != ch:
            details.append(f"Half-width form of {plain}.")
        elif name:
            details.append(f"Unicode name: {name.capitalize()}.")
        return "symbol", None, details

    if in_ranges(ch, COMPONENT_RANGES):
        return "component", None, ["Radical or stroke code point, not a kanji."]

    if in_ranges(ch, IDEOGRAPH_RANGES):
        details = []
        unified = unicodedata.normalize("NFC", ch)
        if unified != ch:  # only compatibility ideographs change under NFC
            kind = table[unified]["category"] if unified in table else "obscure"
            details.append(f"CJK compatibility ideograph: a duplicate of {unified} ({kind}), encoded for conversion to and from older character sets.")
        return "obscure", None, details

    return "other", None, [f"Unicode name: {name.capitalize()}."] if name else []


def single_character(text):
    """Reduce the argument to one code point, or return None if it isn't one character."""
    notes = []
    if len(text) > 1 and (0xFE00 <= ord(text[-1]) <= 0xFE0F or 0xE0100 <= ord(text[-1]) <= 0xE01EF):
        notes.append(f"Ignored the variation selector U+{ord(text[-1]):04X}, which only picks a glyph variant.")
        text = text[:-1]
    if len(text) > 1:
        # A base letter plus a combining mark (か + ゛) becomes one character. Don't
        # do this to a lone character: it would replace compatibility ideographs.
        text = unicodedata.normalize("NFC", text)
    return (text, notes) if len(text) == 1 else (None, notes)


def help_epilog():
    lines = ["categories:"]
    for name, (_, explanation) in CATEGORIES.items():
        wrapped = textwrap.wrap(explanation, width=61)
        lines.append(f"  {name:13} {wrapped[0]}")
        lines.extend(f"  {'':13} {line}" for line in wrapped[1:])
    lines += ["", "A kanji gets the first category in this list that applies to it."]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog=help_epilog(), formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("character", help="the character to look up")
    parser.add_argument("-b", "--brief", action="store_true", help="print only the category name")
    args = parser.parse_args()

    ch, notes = single_character(args.character)
    if ch is None:
        parser.error(f"expected a single character, got {len(args.character)} code points: {args.character!r}")

    category, title, details = classify(ch, load_table())
    if args.brief:
        print(category)
        return
    title = title or CATEGORIES[category][0]
    print(f"{ch} U+{ord(ch):04X}: {category}" + (f" ({title})" if title != category else ""))
    for line in notes + details:
        print(textwrap.fill(line, width=78, initial_indent="  ", subsequent_indent="    "))


if __name__ == "__main__":
    main()
