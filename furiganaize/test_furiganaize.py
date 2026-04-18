"""
Unit tests for furiganaize(text: str) -> list[Ruby | Plain].

Return-format contract
----------------------
- Ruby(text, reading, jukujikun=False): one kanji (or a jukujikun group of
  kanji) paired with its hiragana reading. jukujikun=True means the reading
  belongs to the group as a whole and cannot be split per kanji.
- Plain(text): any run without a reading — kana, punctuation, digits, ASCII,
  or whitespace. Adjacent plain runs are merged into one Plain segment.
- Per-kanji splits are represented as adjacent Ruby segments, so
  `学生` -> [Ruby("学","がく"), Ruby("生","せい")] is distinguishable from
  `今日` -> [Ruby("今日","きょう", jukujikun=True)].
"""

from dataclasses import dataclass

import pytest

# Replace with the real import when wiring up an implementation.
from furiganaize import furiganaize


@dataclass(frozen=True)
class Ruby:
    text: str
    reading: str
    jukujikun: bool = False


@dataclass(frozen=True)
class Plain:
    text: str


class TestBasics:
    def test_empty_string(self):
        assert furiganaize("") == []

    def test_plain_kana_only(self):
        assert furiganaize("こんにちは") == [Plain("こんにちは")]

    def test_single_kanji(self):
        assert furiganaize("山") == [Ruby("山", "やま")]

    def test_simple_compound_splits_per_kanji(self):
        # Headline case: the whole reason we're not using group-ruby output.
        assert furiganaize("学生") == [
            Ruby("学", "がく"),
            Ruby("生", "せい"),
        ]

    def test_ascii_passthrough(self):
        assert furiganaize("Hello, world!") == [Plain("Hello, world!")]

    def test_digits_passthrough_with_kanji(self):
        assert furiganaize("2024年") == [Plain("2024"), Ruby("年", "ねん")]

    def test_whitespace_is_preserved_in_plain(self):
        assert furiganaize("学生 学生") == [
            Ruby("学", "がく"),
            Ruby("生", "せい"),
            Plain(" "),
            Ruby("学", "がく"),
            Ruby("生", "せい"),
        ]


class TestOkurigana:
    """Verb/adjective stems keep the kana tail in Plain, not in Ruby."""

    def test_taberu(self):
        assert furiganaize("食べる") == [Ruby("食", "た"), Plain("べる")]

    def test_hashirimawaru(self):
        # Two verb stems joined, each with its own okurigana tail.
        assert furiganaize("走り回る") == [
            Ruby("走", "はし"),
            Plain("り"),
            Ruby("回", "まわ"),
            Plain("る"),
        ]

    def test_ochitsuku(self):
        assert furiganaize("落ち着く") == [
            Ruby("落", "お"),
            Plain("ち"),
            Ruby("着", "つ"),
            Plain("く"),
        ]

    def test_conjugated_verb(self):
        # Conjugation must not drag kana into the Ruby segment.
        assert furiganaize("食べました") == [
            Ruby("食", "た"),
            Plain("べました"),
        ]

    def test_honorific_prefix(self):
        # The お prefix is plain kana, not part of any ruby.
        assert furiganaize("お寿司") == [
            Plain("お"),
            Ruby("寿", "す"),
            Ruby("司", "し"),
        ]


class TestJukujikun:
    """Compounds whose reading is not decomposable — must be group-ruby."""

    @pytest.mark.parametrize(
        "surface, reading",
        [
            ("今日", "きょう"),
            ("大人", "おとな"),
            ("明日", "あした"),
            ("昨日", "きのう"),
            ("田舎", "いなか"),
            ("眼鏡", "めがね"),
        ],
    )
    def test_classic_jukujikun(self, surface, reading):
        assert furiganaize(surface) == [Ruby(surface, reading, jukujikun=True)]

    def test_jukujikun_in_sentence(self):
        # Jukujikun span stays intact when embedded in a sentence.
        assert furiganaize("今日は") == [
            Ruby("今日", "きょう", jukujikun=True),
            Plain("は"),
        ]


class TestNames:
    """Family names — a common failure mode when the tokenizer lacks JMnedict."""

    def test_tanaka(self):
        assert furiganaize("田中") == [Ruby("田", "た"), Ruby("中", "なか")]

    def test_sato(self):
        assert furiganaize("佐藤") == [Ruby("佐", "さ"), Ruby("藤", "とう")]


class TestContextSensitiveReadings:
    """Same kanji, different readings depending on surrounding context."""

    def test_iku_as_verb(self):
        assert furiganaize("行く") == [Ruby("行", "い"), Plain("く")]

    def test_ginkou(self):
        assert furiganaize("銀行") == [
            Ruby("銀", "ぎん"),
            Ruby("行", "こう"),
        ]

    def test_same_kanji_two_readings_in_one_sentence(self):
        # 行 appears twice: こう in 銀行, い in 行く.
        assert furiganaize("銀行に行く") == [
            Ruby("銀", "ぎん"),
            Ruby("行", "こう"),
            Plain("に"),
            Ruby("行", "い"),
            Plain("く"),
        ]


class TestFullSentences:
    """Integration cases that mix several features at once."""

    def test_sentence_mixing_features(self):
        assert furiganaize("お寿司を食べる") == [
            Plain("お"),
            Ruby("寿", "す"),
            Ruby("司", "し"),
            Plain("を"),
            Ruby("食", "た"),
            Plain("べる"),
        ]

    def test_sentence_with_jukujikun_and_splittable(self):
        assert furiganaize("今日は学生です") == [
            Ruby("今日", "きょう", jukujikun=True),
            Plain("は"),
            Ruby("学", "がく"),
            Ruby("生", "せい"),
            Plain("です"),
        ]

    def test_japanese_punctuation_merged_into_plain(self):
        # 、 and 。 merge with adjacent kana into a single Plain segment.
        assert furiganaize("学生、こんにちは。") == [
            Ruby("学", "がく"),
            Ruby("生", "せい"),
            Plain("、こんにちは。"),
        ]


class TestRoundTrip:
    """Structural invariants that should hold for any input."""

    @pytest.mark.parametrize(
        "text",
        [
            "",
            "こんにちは",
            "学生",
            "今日は学生です",
            "銀行に行く",
            "お寿司を食べる",
            "2024年4月16日",
            "Hello, 学生!",
        ],
    )
    def test_concatenated_surfaces_equal_input(self, text):
        # Whatever the segmentation, joining every segment's surface text
        # must reproduce the original input exactly.
        segments = furiganaize(text)
        rebuilt = "".join(seg.text for seg in segments)
        assert rebuilt == text

    def test_no_empty_segments(self):
        for seg in furiganaize("今日は学生です"):
            assert seg.text != ""

    def test_adjacent_plain_segments_are_merged(self):
        segments = furiganaize("学生、こんにちは。")
        for a, b in zip(segments, segments[1:]):
            assert not (isinstance(a, Plain) and isinstance(b, Plain)), (
                f"adjacent Plain segments should be merged: {a!r}, {b!r}"
            )
