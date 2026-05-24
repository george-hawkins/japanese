"""Build a ComicInfo.xml for a book (novel etc.) using its ISBN-13.

Usage:
    ./bookinfo.py 978-4863898608
    ./bookinfo.py 978-4863898608 -o ComicInfo.xml
    ./bookinfo.py 978-4863898608 --series "Harry Potter" --volume 1
    ./bookinfo.py 978-4863898608 -o -    # write to stdout

Looks up metadata via openBD (Japanese ISBNs, prefix 978-4) and falls back to
Google Books. Books rarely carry the same shape of metadata as manga, so this
populates a minimal subset of ComicInfo: Title, Series, Number/Volume, Writer,
Publisher, Imprint, dates, Summary, LanguageISO, GTIN.
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

OPENBD_URL = "https://api.openbd.jp/v1/get"
GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
USER_AGENT = "bookinfo.py/1.0 (+https://github.com/)"


def http_get_json(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def _as_list(v):
    """ONIX fields are sometimes a single object, sometimes a list."""
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def fetch_openbd(isbn):
    data = http_get_json(f"{OPENBD_URL}?isbn={urllib.parse.quote(isbn)}")
    if not data or not data[0]:
        return None
    record = data[0]
    summary = record.get("summary") or {}
    onix = record.get("onix") or {}
    descriptive = onix.get("DescriptiveDetail") or {}
    publishing = onix.get("PublishingDetail") or {}
    collateral = onix.get("CollateralDetail") or {}

    # Prefer the structured ONIX Contributor list — summary.author is a single
    # space-joined string where each name itself contains a comma.
    authors = []
    for c in _as_list(descriptive.get("Contributor")):
        name = ((c.get("PersonName") or {}).get("content") or "").strip()
        if name and name not in authors:
            authors.append(name)
    if not authors and summary.get("author"):
        authors = summary["author"].split()

    # The "Collection" block names a bunko/series line (e.g. 静山社ペガサス文庫).
    # It's closer to an imprint than the work's own series, so treat it as such.
    collection = ""
    for el in _as_list(((descriptive.get("Collection") or {}).get("TitleDetail") or {}).get("TitleElement")):
        text = (el.get("TitleText") or {}).get("content")
        if text:
            collection = text
            break
    if not collection:
        collection = summary.get("series") or ""

    imprint = ((publishing.get("Imprint") or {}).get("ImprintName") or "").strip()
    publisher = summary.get("publisher") or ""
    # Avoid duplicating the publisher name as the imprint.
    if imprint and imprint == publisher:
        imprint = ""
    # The collection line is more specific than the bare publisher imprint.
    imprint = collection or imprint

    # TextContent[].TextType: 02=short description, 03=description, 04=table of
    # contents. Prefer the longest description-shaped entry.
    description = ""
    candidates = []
    for tc in _as_list(collateral.get("TextContent")):
        if (tc.get("TextType") or "") in ("02", "03"):
            text = tc.get("Text") or ""
            if text:
                candidates.append(text)
    if candidates:
        description = max(candidates, key=len)

    pubdate = ""
    for d in _as_list(publishing.get("PublishingDate")):
        # Role 01 = publication date.
        if (d.get("PublishingDateRole") or "") == "01":
            pubdate = d.get("Date") or ""
            break
    if not pubdate:
        pubdate = summary.get("pubdate") or ""

    return {
        "title": summary.get("title") or "",
        "authors": authors,
        "publisher": publisher,
        "imprint": imprint,
        "series": "",          # openBD doesn't carry a work-series name; user supplies
        "volume": summary.get("volume") or "",
        "year": pubdate[:4] if len(pubdate) >= 4 else "",
        "month": pubdate[4:6] if len(pubdate) >= 6 else "",
        "day": pubdate[6:8] if len(pubdate) >= 8 else "",
        "description": description,
        "language": "ja",
        "isbn": isbn,
        "source": "openBD",
    }


def fetch_google_books(isbn):
    data = http_get_json(f"{GOOGLE_BOOKS_URL}?q=isbn:{urllib.parse.quote(isbn)}")
    items = data.get("items") or []
    if not items:
        return None
    v = items[0].get("volumeInfo") or {}

    parts = (v.get("publishedDate") or "").split("-")
    year = parts[0] if len(parts) > 0 and parts[0] else ""
    month = parts[1] if len(parts) > 1 else ""
    day = parts[2] if len(parts) > 2 else ""

    title = v.get("title") or ""
    subtitle = v.get("subtitle") or ""
    if subtitle:
        title = f"{title}: {subtitle}"

    return {
        "title": title,
        "authors": list(v.get("authors") or []),
        "publisher": v.get("publisher") or "",
        "imprint": "",
        "series": (v.get("seriesInfo") or {}).get("title") or "",
        "volume": "",
        "year": year,
        "month": month,
        "day": day,
        "description": v.get("description") or "",
        "language": v.get("language") or "",
        "isbn": isbn,
        "source": "Google Books",
    }


def fetch(isbn):
    digits = re.sub(r"[^0-9Xx]", "", isbn)
    sources = []
    if digits.startswith("9784"):
        sources = [fetch_openbd, fetch_google_books]
    else:
        sources = [fetch_google_books, fetch_openbd]
    last_error = None
    for source in sources:
        try:
            info = source(digits)
        except urllib.error.HTTPError as e:
            last_error = f"{source.__name__}: HTTP {e.code} {e.reason}"
            continue
        except urllib.error.URLError as e:
            last_error = f"{source.__name__}: {e.reason}"
            continue
        if info:
            return info
    sys.exit(f"No book found for ISBN: {isbn}" + (f" ({last_error})" if last_error else ""))


def strip_html(s):
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def build_xml(info, volume=None, series=None, count=None, language=None,
              title=None, publisher=None, imprint=None):
    root = ET.Element(
        "ComicInfo",
        {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        },
    )

    def add(tag, value):
        if value not in (None, "", []):
            ET.SubElement(root, tag).text = str(value)

    resolved_title = title or info["title"]
    # ComicInfo readers expect a Series; if the caller didn't supply one, fall
    # back to the title so the field isn't empty.
    resolved_series = series or info.get("series") or info["title"]
    resolved_volume = volume if volume is not None else (info.get("volume") or None)

    add("Title", resolved_title)
    add("Series", resolved_series)
    add("Number", resolved_volume)
    add("Volume", resolved_volume)
    add("Count", count)
    add("Summary", strip_html(info.get("description")))

    add("Year", info.get("year"))
    add("Month", info.get("month"))
    add("Day", info.get("day"))

    add("Writer", ", ".join(info.get("authors") or []))
    add("Publisher", publisher or info.get("publisher"))
    add("Imprint", imprint or info.get("imprint"))
    resolved_language = language or info.get("language") or "ja"
    add("LanguageISO", resolved_language)
    add("GTIN", info.get("isbn"))
    if resolved_language.lower() in ("ja", "jp"):
        add("Manga", "YesAndRightToLeft")

    return root


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("isbn", help='ISBN-13, e.g. "978-4863898608"')
    p.add_argument("-o", "--output", default="ComicInfo.xml", help='Output path, or "-" for stdout')
    p.add_argument("--language", help="LanguageISO override (default: from lookup, else ja)")
    p.add_argument("--series", help="Series name override (e.g. Harry Potter)")
    p.add_argument("--volume", help="Volume number override")
    p.add_argument("--count", type=int, help="Total volume count in the series")
    p.add_argument("--title", help="Per-issue Title override")
    p.add_argument("--publisher", help="Publisher override")
    p.add_argument("--imprint", help="Imprint override (e.g. bunko line)")
    args = p.parse_args()

    info = fetch(args.isbn)
    root = build_xml(info, args.volume, args.series, args.count, args.language,
                     args.title, args.publisher, args.imprint)
    ET.indent(root, space="  ")
    xml_bytes = b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding="utf-8")

    if args.output == "-":
        sys.stdout.buffer.write(xml_bytes)
        sys.stdout.buffer.write(b"\n")
    else:
        with open(args.output, "wb") as f:
            f.write(xml_bytes)
        print(f"Wrote {args.output} for: {info['title']} (via {info['source']})", file=sys.stderr)


if __name__ == "__main__":
    main()
