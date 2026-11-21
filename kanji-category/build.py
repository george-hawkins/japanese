#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Build kanji-categories.tsv, the lookup table used by kanji-category.py.

The table is generated from five sources, fetched into downloads/ on first use
(pass --refresh to fetch them again):

* KANJIDIC2 (EDRDG): JIS levels, frequency ranks, stroke counts, meanings, variants.
* Unihan (Unicode): the jōyō and jinmeiyō lists, old forms, Chinese standards.
* EquivalentUnifiedIdeograph.txt (Unicode): radical code point -> ideograph.
* Wiktionary: the kanji of the 表外漢字字体表.
* Wikipedia: the year each jōyō kanji joined the list.

See README.md for what the categories mean and how each is decided.
"""

import argparse
import collections
import gzip
import html
import re
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOWNLOADS = HERE / "downloads"
OUTPUT = HERE / "kanji-categories.tsv"

SOURCES = {
    "kanjidic/kanjidic2.xml.gz": "http://www.edrdg.org/kanjidic/kanjidic2.xml.gz",
    "unihan/Unihan.zip": "https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip",
    "ucd/EquivalentUnifiedIdeograph.txt": "https://www.unicode.org/Public/UCD/latest/ucd/EquivalentUnifiedIdeograph.txt",
    "wiktionary/hyogai.wikitext": "https://ja.wiktionary.org/w/index.php?title=%E4%BB%98%E9%8C%B2:%E8%A1%A8%E5%A4%96%E6%BC%A2%E5%AD%97%E5%AD%97%E4%BD%93%E8%A1%A8%E3%81%AE%E6%BC%A2%E5%AD%97%E4%B8%80%E8%A6%A7&action=raw",
    "wikipedia/joyo.wikitext": "https://en.wikipedia.org/w/index.php?title=List_of_j%C5%8Dy%C5%8D_kanji&action=raw",
}

# The categories this table covers, in the order rows are written. A character
# gets the first category whose rule matches, in the order main() applies them.
CATEGORIES = ["jōyō", "jinmeiyō", "hyōgai", "rare", "chinese", "component"]
JAPANESE = CATEGORIES[:4]  # the categories of kanji used in Japan

# Components that Unicode encodes as ordinary ideographs but gives no radical
# number or definition to, so no rule below can find them.
EXTRA_COMPONENTS = "丷乛龴龵龶龷龸龹龺龻𠂉𠂇𠂆𠂊𠆢𠃊𠃌𠃍𠄌𧘇"

# The five kanji of the 1981 jōyō list that the 2010 revision dropped, making them jinmeiyō kanji.
DROPPED_IN_2010 = "勺匁脹銑錘"

# Kanji in real use in Japan (in personal and company names) that no Japanese
# character set standard includes: {kanji: the kanji it is a variant of}.
EXTRA_RARE = {"𠮷": "吉"}

UNIHAN_FIELDS = {
    "kJoyoKanji", "kJinmeiyoKanji", "kJapaneseNewVariant", "kZVariant", "kSemanticVariant",
    "kSimplifiedVariant", "kTraditionalVariant", "kRSUnicode", "kDefinition",
    "kTGH", "kHKGlyph", "kBigFive", "kUnihanCore2020", "kIBMJapan", "kTotalStrokes",
}


def fetch(refresh):
    for rel, url in SOURCES.items():
        path = DOWNLOADS / rel
        if path.exists() and not refresh:
            continue
        print(f"fetching {url}", file=sys.stderr)
        path.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(url, headers={"User-Agent": "kanji-category-build/1.0"})
        with urllib.request.urlopen(request, timeout=120) as response:
            path.write_bytes(response.read())


def cp(ch):
    return f"U+{ord(ch):04X}"


def code_points(value):
    return [chr(int(code, 16)) for code in re.findall(r"U\+([0-9A-F]+)", value or "")]


def is_compatibility_ideograph(ch):
    return 0xF900 <= ord(ch) <= 0xFAFF or 0x2F800 <= ord(ch) <= 0x2FA1F


def read_kanjidic():
    """Return {char: {jis, freq, grade, strokes, meanings, variants}}; jis is '1'-'4' or ''."""
    with gzip.open(DOWNLOADS / "kanjidic/kanjidic2.xml.gz") as f:
        characters = list(ET.parse(f).getroot().iter("character"))
    by_code = {(e.get("cp_type"), e.text.lower()): c.findtext("literal") for c in characters for e in c.iter("cp_value")}
    kanji = {}
    for c in characters:
        codes = {e.get("cp_type"): e.text for e in c.iter("cp_value")}
        if "jis208" in codes:  # kuten is plane-row-cell; level 1 is rows 16-47
            jis = "1" if int(codes["jis208"].split("-")[1]) <= 47 else "2"
        elif "jis213" in codes:  # plane 1 is level 3, plane 2 is level 4
            jis = "3" if codes["jis213"].startswith("1-") else "4"
        else:
            jis = ""  # JIS X 0212 only
        variants = {by_code.get((v.get("var_type"), v.text.lower())) for v in c.iter("variant")}
        kanji[c.findtext("literal")] = {
            "jis": jis,
            "freq": c.findtext("misc/freq") or "",
            "grade": c.findtext("misc/grade") or "",
            "strokes": int(c.findtext("misc/stroke_count") or 0),
            "meanings": [m.text for m in c.iter("meaning") if m.get("m_lang") is None],
            "variants": variants - {None},  # variants given as dictionary index numbers don't resolve
        }
    return kanji


def read_unihan():
    unihan = collections.defaultdict(dict)
    with zipfile.ZipFile(DOWNLOADS / "unihan/Unihan.zip") as z:
        for name in z.namelist():
            for line in z.read(name).decode("utf-8").splitlines():
                if not line.startswith("U+"):
                    continue
                code, field, value = line.split("\t", 2)
                if field in UNIHAN_FIELDS:
                    unihan[chr(int(code[2:], 16))][field] = value
    return unihan


def read_radical_equivalents():
    """Return {radical or stroke code point: equivalent unified ideograph}."""
    equivalents = {}
    for line in (DOWNLOADS / "ucd/EquivalentUnifiedIdeograph.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        source, target = (part.strip() for part in line.split(";"))
        first, _, last = source.partition("..")
        for code in range(int(first, 16), int(last or first, 16) + 1):
            equivalents[chr(code)] = chr(int(target, 16))
    return equivalents


def read_hyogai_table():
    """Return (set of printed standard forms, {simplified form: standard form})."""
    text = html.unescape((DOWNLOADS / "wiktionary/hyogai.wikitext").read_text(encoding="utf-8"))
    listing = text.split("== 一覧 ==")[1].split("==")[0]
    standard, simplified, previous = set(), {}, None
    # Each kanji is a [[link]]; a simplified form follows its standard form in （）, sometimes in bold.
    for opening, ch in re.findall(r"(（(?:''')?)?\[\[(.)\]\]", listing):
        if opening:
            simplified[ch] = previous
        else:
            standard.add(ch)
            previous = ch
    if (len(standard), len(simplified)) != (1022, 22):
        sys.exit(f"表外漢字字体表: expected 1022 + 22 kanji, got {len(standard)} + {len(simplified)}")
    return standard, simplified


def read_joyo_years(is_joyo):
    """Return {jōyō kanji: year it joined the list}: 1946 (as a tōyō kanji), 1981 or 2010."""
    text = html.unescape((DOWNLOADS / "wikipedia/joyo.wikitext").read_text(encoding="utf-8"))
    years = {}
    for line in text.splitlines():
        if re.match(r"\|\d+\|\|", line):  # a table row: | number || kanji || old forms || ... || year added || ...
            cells = line.split("||")
            # A few rows have a non-jōyō variant (篭) as the kanji and the jōyō kanji (籠) as its old form.
            forms = re.findall(r"\[\[wikt:\s*(.)#Japanese", cells[1] + cells[2])
            years[next(filter(is_joyo, forms), forms[0])] = cells[6].strip() or "1946"
    counts = collections.Counter(years.values())
    if counts != {"1946": 1845, "1981": 95, "2010": 196}:
        sys.exit(f"jōyō list: expected 1845 + 95 + 196 kanji, got {dict(counts)}")
    return years


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", action="store_true", help="fetch the sources again even if already downloaded")
    args = parser.parse_args()
    fetch(args.refresh)

    kanjidic = read_kanjidic()
    unihan = read_unihan()
    equivalents = read_radical_equivalents()
    hyogai_standard, hyogai_simplified = read_hyogai_table()
    joyo_years = read_joyo_years(lambda ch: "kJoyoKanji" in unihan[ch])

    def jis(ch):
        return kanjidic[ch]["jis"] if ch in kanjidic else ""

    # The jōyō table's old forms (旧字体): {old: new}.
    old_forms = {old: new for old, fields in unihan.items() for new in code_points(fields.get("kJapaneseNewVariant"))}

    # Variant links, made symmetric. KANJIDIC2's are curated for Japanese.
    # Unihan's Z and semantic variants add more, but those sourced only from
    # Lau's Cantonese dictionary are mostly sound-alike substitutions, so skip them.
    variants = collections.defaultdict(set)
    for ch, entry in kanjidic.items():
        for other in entry["variants"]:
            variants[ch].add(other)
            variants[other].add(ch)
    for ch, other in EXTRA_RARE.items():
        variants[ch].add(other)
        variants[other].add(ch)
    for ch, fields in unihan.items():
        for field in ("kZVariant", "kSemanticVariant"):
            for code, sources in re.findall(r"U\+([0-9A-F]+)(?:<(\S+))?", fields.get(field, "")):
                other = chr(int(code, 16))
                if other != ch and sources != "kLau":
                    variants[ch].add(other)
                    variants[other].add(ch)
        # JIS X 0213 added the proper printed forms (噓) of kanji that JIS X 0208
        # only has in simplified form (嘘); Unihan links such pairs as traditional/simplified.
        for other in code_points(fields.get("kSimplifiedVariant")):
            if jis(ch) in ("3", "4") and jis(other) in ("1", "2"):
                variants[ch].add(other)
                variants[other].add(ch)

    category = {}
    if any(ch not in unihan or "kJinmeiyoKanji" not in unihan[ch] for ch in DROPPED_IN_2010):
        sys.exit("the kanji dropped from the jōyō list in 2010 should all be jinmeiyō kanji")

    # 1-2. The official lists, straight from Unihan.
    for ch, fields in unihan.items():
        if "kJoyoKanji" in fields:
            category[ch] = "jōyō"
        elif "kJinmeiyoKanji" in fields:
            category[ch] = "jinmeiyō"

    # 3. Common hyōgai: the 表外漢字字体表, and whatever else is in JIS level 1.
    for ch in hyogai_standard | set(hyogai_simplified) | {c for c in kanjidic if jis(c) == "1"}:
        category.setdefault(ch, "hyōgai")

    # Evidence of use in Japan beyond the JIS standards: the IBM extensions to
    # Shift_JIS (mostly name kanji), and Unicode's core Japanese set.
    japanese_extras = {ch for ch, f in unihan.items() if "kIBMJapan" in f or "J" in f.get("kUnihanCore2020", "")} | set(EXTRA_RARE)

    # 4. Components encoded as ideographs.
    def mentions_radical(ch):
        texts = (kanjidic[ch]["meanings"] if ch in kanjidic else []) + [unihan[ch].get("kDefinition", "")]
        return any(re.search(r"\bradical\b", t, re.I) for t in texts)

    def is_real_character(ch):
        # In general use in modern Chinese (or, within JIS X 0208, the traditional
        # form of such a character), or an old or name form of a current kanji.
        fields = unihan[ch]
        traditional = "kSimplifiedVariant" in fields and jis(ch) in ("1", "2")
        return "kTGH" in fields or traditional or ch in old_forms or "kIBMJapan" in fields or ch in EXTRA_RARE

    components = set(EXTRA_COMPONENTS)
    for ch, entry in kanjidic.items():
        if entry["meanings"] and all("radical" in m for m in entry["meanings"]):
            components.add(ch)  # all the dictionary says about it is that it's a radical
    for ch in set(equivalents.values()):
        if not is_real_character(ch):
            components.add(ch)  # Unicode has a radical code point for it, and it isn't a character otherwise
    for ch in unihan:
        if jis(ch) not in ("1", "2") and mentions_radical(ch) and not is_real_character(ch):
            components.add(ch)  # outside JIS X 0208 and described as a radical
    for ch in components:
        if not is_compatibility_ideograph(ch):
            category.setdefault(ch, "component")

    # 5. Rare: anything else with evidence of use in Japan.
    for ch in unihan:
        if jis(ch) or ch in japanese_extras:
            category.setdefault(ch, "rare")

    # 6. Chinese: in a modern Chinese standard list (the PRC's general list, Hong
    #    Kong's glyph list, or Big5 level 1, the frequently used part of Taiwan's Big5).
    for ch, fields in unihan.items():
        big5_level_1 = "A440" <= fields.get("kBigFive", "") <= "C67E"
        if "kTGH" in fields or "kHKGlyph" in fields or big5_level_1:
            category.setdefault(ch, "chinese")

    def label(ch):
        """Describe another character by its category, e.g. 'jōyō kanji 学'."""
        kind = category.get(ch, "obscure")
        return f"{kind} kanji {ch}" if kind in JAPANESE else f"{ch} ({kind})"

    # Pairs whose relationship is known: {(a, b): what b is to a}.
    relation = {}

    def relate(a, b, b_is, a_is):
        relation[a, b], relation[b, a] = b_is, a_is
        variants[a].add(b)
        variants[b].add(a)

    for old, new in old_forms.items():
        relate(new, old, "old form 旧字体", "new form 新字体")
    for simple, standard in hyogai_simplified.items():
        relate(standard, simple, "simplified everyday form 簡易慣用字体", "printed standard form 印刷標準字体")
    for ch, fields in unihan.items():
        for official in code_points(fields.get("kJoyoKanji")):
            relate(official, ch, "accepted alternative form 許容字体", "official jōyō form")
            # Wikipedia's table has only one of each official/alternative pair.
            joyo_years[ch] = joyo_years[official] = joyo_years.get(ch) or joyo_years[official]
    if missing := {ch for ch, kind in category.items() if kind == "jōyō"} ^ set(joyo_years):
        sys.exit(f"jōyō list: Unihan and Wikipedia disagree about {''.join(sorted(missing))}")
        for standard in code_points(fields.get("kJinmeiyoKanji")):
            variants[ch].add(standard)
            variants[standard].add(ch)

    def strokes(ch):
        if ch in kanjidic:
            return kanjidic[ch]["strokes"]
        return int(unihan[ch].get("kTotalStrokes", "0").split()[0])

    def variants_for(ch):
        """List the other forms of a kanji, saying what each is relative to it."""
        if category[ch] not in JAPANESE:
            return ""
        found = sorted((v for v in variants[ch] if category.get(v) in JAPANESE), key=lambda v: (JAPANESE.index(category[v]), ord(v)))
        items = []
        for v in found:
            what = relation.get((ch, v))
            if not what:
                mine, theirs = strokes(ch), strokes(v)
                what = "variant" if not mine or not theirs or mine == theirs else "simpler form" if theirs < mine else "more complex form"
            items.append(f"{v} ({category[v]}, {what})")
        return "; ".join(items)

    in_hyogai_table = hyogai_standard | set(hyogai_simplified)
    radical_ideograph = {n + 1: equivalents[chr(0x2F00 + n)] for n in range(214)}

    def note_for(ch):
        kind, fields, notes = category[ch], unihan[ch], []
        if kind == "jōyō":
            notes.append({
                "1946": "On the list since 1946, when it was the tōyō kanji list.",
                "1981": "Added to the list in 1981.",
                "2010": "Added to the list in 2010.",
            }[joyo_years[ch]])
            if code_points(fields["kJoyoKanji"]):
                notes.append("Not the official jōyō form, but the form most fonts and input methods produce.")
            elif any("official" in relation.get((v, ch), "") for v in variants[ch]):
                notes.append("Only in JIS X 0213, so most fonts and input methods produce the accepted alternative form instead.")
            grade = kanjidic.get(ch, {}).get("grade", "")
            if grade in list("123456"):
                notes.append(f"Taught in grade {grade}.")
            elif grade == "8":
                notes.append("Taught in secondary school.")
        elif kind == "jinmeiyō":
            if ch in DROPPED_IN_2010:
                notes.append("Former jōyō kanji: dropped from the list in 2010 and made a jinmeiyō kanji.")
        elif kind == "hyōgai":
            if ch in hyogai_standard:
                notes.append("Printed standard form (印刷標準字体) in the 表外漢字字体表.")
                typed = sorted(v for v in variants[ch] if jis(v) == "1" and v not in in_hyogai_table and category[v] == "hyōgai")
                if typed and jis(ch) not in ("1", "2"):
                    notes.append(f"Only in JIS X 0213, so often replaced by the JIS level 1 form {'、'.join(typed)}.")
            elif ch in hyogai_simplified:
                notes.append("Simplified everyday form (簡易慣用字体) in the 表外漢字字体表.")
            else:
                notes.append("JIS level 1 kanji that is not in the 表外漢字字体表.")
        elif kind == "rare":
            if ch in EXTRA_RARE:
                notes.append("In no Japanese character set standard, but in real use in Japanese names.")
            elif not jis(ch) and "kIBMJapan" in fields:
                notes.append("Not in JIS X 0208 or JIS X 0213, but in the IBM extensions to Shift_JIS (Windows-31J).")
            elif not jis(ch):
                notes.append("Not in JIS X 0208 or JIS X 0213, but in Unicode's core Japanese set (UnihanCore2020).")
        elif kind == "chinese":
            traditional = [c for c in code_points(fields.get("kTraditionalVariant")) if c != ch]
            if "kTGH" in fields and traditional:
                notes.append(f"Simplified Chinese form of {' and '.join(label(c) for c in traditional[:2])}.")
        elif kind == "component":
            radical = re.match(r"(\d+)'*\.(-?\d+)", fields.get("kRSUnicode", ""))
            if radical and radical.group(2) == "0":
                number = int(radical.group(1))
                if radical_ideograph[number] == ch:
                    notes.append(f"Kangxi radical {number}.")
                else:
                    notes.append(f"Form of Kangxi radical {number} ({radical_ideograph[number]}).")
            notes.append("Encoded as an ideograph, but in Japanese only a part of kanji.")
        return " ".join(notes)

    def meaning_for(ch):
        if ch in kanjidic and kanjidic[ch]["meanings"]:
            return "; ".join(kanjidic[ch]["meanings"])
        return unihan[ch].get("kDefinition", "")

    rows = []
    for ch, kind in category.items():
        entry = kanjidic.get(ch, {})
        rows.append((CATEGORIES.index(kind), ord(ch), [ch, cp(ch), kind, entry.get("jis", ""), entry.get("freq", ""), variants_for(ch), note_for(ch), meaning_for(ch)]))

    # Code points that exist only to show a radical or stroke: never kanji.
    blocks = [(0x2E80, 0x2EFF, "CJK radical"), (0x2F00, 0x2FDF, "Kangxi radical"), (0x31C0, 0x31EE, "CJK stroke")]
    for first, last, kind in blocks:
        for code in range(first, last + 1):
            ch = chr(code)
            name = unicodedata.name(ch, "")
            if not name and ch not in equivalents:
                continue  # unassigned, or too new for this Python's Unicode data
            note = f"{kind} code point, not a kanji."
            if ch in equivalents:
                target = equivalents[ch]
                note += f" The equivalent ideograph is {target} ({cp(target)}, {category.get(target, 'obscure')})."
            rows.append((CATEGORIES.index("component"), code, [ch, cp(ch), "component", "", "", "", note, name.capitalize().replace("Cjk", "CJK")]))

    rows.sort()
    with open(OUTPUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("char\tcodepoint\tcategory\tjis_level\tfreq_rank\tvariants\tnote\tmeaning\n")
        for _, _, fields in rows:
            f.write("\t".join(field.replace("\t", " ") for field in fields) + "\n")

    counts = collections.Counter(fields[2] for _, _, fields in rows)
    for kind in CATEGORIES:
        print(f"{kind:10} {counts[kind]:6,}")
    print(f"{'total':10} {len(rows):6,}  -> {OUTPUT.name}")


if __name__ == "__main__":
    main()
