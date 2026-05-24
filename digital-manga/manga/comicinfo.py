"""Build a ComicInfo.xml for a manga volume using the AniList GraphQL API.

Usage:
    ./comicinfo.py "Witch Hat Atelier" 1
    ./comicinfo.py "Witch Hat Atelier" 1 -o vol01/ComicInfo.xml
    ./comicinfo.py "Witch Hat Atelier" 1 --language en --count 14
    ./comicinfo.py "Witch Hat Atelier" 1 --publisher "Kodansha" --imprint "Kodansha Comics"
    ./comicinfo.py "Witch Hat Atelier" 1 --title "Witch Hat Atelier, Vol. 1"
    ./comicinfo.py "Witch Hat Atelier" 1 -o -    # write to stdout
"""

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

ANILIST_URL = "https://graphql.anilist.co"

QUERY = """
query ($search: String) {
  Media(search: $search, type: MANGA) {
    id
    title { romaji english native }
    description(asHtml: false)
    startDate { year month day }
    endDate { year }
    chapters
    volumes
    status
    genres
    tags { name }
    staff { edges { role node { name { full } } } }
    siteUrl
    countryOfOrigin
  }
}
"""


def fetch(series):
    body = json.dumps({"query": QUERY, "variables": {"search": series}}).encode()
    req = urllib.request.Request(
        ANILIST_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "comicinfo.py/1.0 (+https://github.com/)",
        },
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if data.get("errors"):
        sys.exit(f"AniList error: {data['errors']}")
    media = data["data"]["Media"]
    if not media:
        sys.exit(f"No manga found for: {series}")
    return media


def strip_html(s):
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def staff_by_role(media, *wanted_roles):
    """Return names whose role matches one of the given roles exactly (case-insensitive)."""
    wanted = {r.lower() for r in wanted_roles}
    out = []
    for edge in media.get("staff", {}).get("edges", []) or []:
        role = (edge.get("role") or "").strip().lower()
        if role in wanted:
            name = (edge.get("node") or {}).get("name", {}).get("full")
            if name and name not in out:
                out.append(name)
    return out


def build_xml(media, volume, count_override=None, language="ja",
              title_override=None, publisher=None, imprint=None):
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

    title = media["title"] or {}
    series_name = title.get("english") or title.get("romaji") or title.get("native")
    # Per-issue Title — readers like OpenComic fall back to the filename without this.
    issue_title = title_override or f"{series_name}, Vol. {volume}"
    add("Title", issue_title)
    add("Series", series_name)
    add("LocalizedSeries", title.get("native"))
    add("Number", volume)
    add("Volume", volume)
    add("Count", count_override if count_override is not None else media.get("volumes"))
    add("Summary", strip_html(media.get("description")))

    start = media.get("startDate") or {}
    add("Year", start.get("year"))
    add("Month", start.get("month"))
    add("Day", start.get("day"))

    # Most manga credit a single creator as "Story & Art"; otherwise the roles are split.
    both = staff_by_role(media, "story & art")
    if both:
        writers = both
        artists = both
    else:
        writers = staff_by_role(media, "story", "original creator", "original story")
        artists = staff_by_role(media, "art", "illustration", "illustrator")

    add("Writer", ", ".join(writers))
    if artists:
        joined = ", ".join(artists)
        add("Penciller", joined)
        add("Inker", joined)
        add("Letterer", joined)
        add("CoverArtist", joined)

    add("Publisher", publisher)
    add("Imprint", imprint)
    add("Genre", ", ".join(media.get("genres") or []))
    add("Tags", ", ".join(t["name"] for t in (media.get("tags") or []) if t.get("name")))
    add("Web", media.get("siteUrl"))
    add("LanguageISO", language)
    # Most manga read right-to-left; flip to "Yes" if the volume is mirrored.
    add("Manga", "YesAndRightToLeft")

    return root


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("series", help='Search string, e.g. "Witch Hat Atelier"')
    p.add_argument("volume", help="Volume number, e.g. 1")
    p.add_argument("-o", "--output", default="ComicInfo.xml", help='Output path, or "-" for stdout')
    p.add_argument("--language", default="ja", help="LanguageISO (default: ja)")
    p.add_argument("--count", type=int, help="Override total volume count")
    p.add_argument("--title", help='Per-issue title (default: "<Series>, Vol. <N>")')
    p.add_argument("--publisher", help="Publisher (e.g. Kodansha) — AniList does not expose this")
    p.add_argument("--imprint", help='Imprint (e.g. "Kodansha Comics")')
    args = p.parse_args()

    media = fetch(args.series)
    root = build_xml(media, args.volume, args.count, args.language,
                     args.title, args.publisher, args.imprint)
    ET.indent(root, space="  ")
    xml_bytes = b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding="utf-8")

    if args.output == "-":
        sys.stdout.buffer.write(xml_bytes)
        sys.stdout.buffer.write(b"\n")
    else:
        with open(args.output, "wb") as f:
            f.write(xml_bytes)
        title = media["title"]
        resolved = title.get("english") or title.get("romaji") or title.get("native")
        print(f"Wrote {args.output} for: {resolved} vol. {args.volume}", file=sys.stderr)


if __name__ == "__main__":
    main()
