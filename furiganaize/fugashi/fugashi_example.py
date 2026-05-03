import argparse

from fugashi import Tagger

AUXILIARY_SYMBOL = "補助記号"


def analyze(text: str) -> None:
    tagger = Tagger()
    for word in tagger(text):
        # skip punctuation and symbols if you want
        if word.feature.pos1 == AUXILIARY_SYMBOL:
            continue
        print(f"{word.surface:4}  lemma={word.feature.lemma}  pos={word.pos}  unk={word.is_unk}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tokenize Japanese text with fugashi.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="path to a file containing the text to analyze")
    group.add_argument("-t", "--text", help="text to analyze")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            analyze(f.read())
    else:
        analyze(args.text)


if __name__ == "__main__":
    main()
