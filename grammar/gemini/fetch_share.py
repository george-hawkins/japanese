#!/usr/bin/env python3
"""Fetch a Gemini share URL and emit GitHub-flavored Markdown.

Usage:
    fetch_share.py <share-url> [-o output] [--no-markdown] [--no-preprocess]

The chat content on a Gemini share page is rendered client-side after the
initial document loads, so `curl` returns a shell with no conversation. This
script drives a headless Chromium via Playwright to wait for the conversation
to render, then:

  1. Extracts the <div class="chat-history"> subtree (pass --full to keep the
     entire document instead).
  2. Strips inline <svg> blocks (Lottie loading-icon sources that would otherwise
     become huge data: URIs in the markdown) and rewrites <user-query> elements
     as <blockquote>, so user turns render as quoted blocks. Disable with
     --no-preprocess.
  3. Converts to GitHub-flavored Markdown via pandoc. Disable with --no-markdown
     to leave the output as HTML.

Run once after installing:
    pip install playwright pypandoc beautifulsoup4
    playwright install chromium
    # ensure `pandoc` is on PATH (brew install pandoc)
"""

from __future__ import annotations

import argparse
import sys
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


CHAT_HISTORY_SELECTOR = "share-viewer div.chat-history"


class LayoutChangedError(RuntimeError):
    """Raised when the expected DOM element isn't present after rendering."""


def fetch(share_url: str, full: bool, timeout_ms: int, verbose: bool) -> str:
    t0 = time.perf_counter()
    last = t0
    requests = 0
    responses = 0
    bytes_in = 0

    def step(label: str) -> None:
        nonlocal last
        now = time.perf_counter()
        if verbose:
            sys.stderr.write(
                f"[{now - t0:6.2f}s] +{now - last:5.2f}s  {label}\n"
            )
        last = now

    with sync_playwright() as p:
        step("playwright started")
        browser = p.chromium.launch(headless=True)
        step("chromium launched")
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/127.0.0.0 Safari/537.36"
            ),
            locale="en-US",
        )
        page = context.new_page()

        def on_request(_req):
            nonlocal requests
            requests += 1

        def on_response(resp):
            nonlocal responses, bytes_in
            responses += 1
            try:
                cl = resp.headers.get("content-length")
                if cl:
                    bytes_in += int(cl)
            except Exception:
                pass

        page.on("request", on_request)
        page.on("response", on_response)
        step("context + page ready")

        page.goto(share_url, wait_until="domcontentloaded", timeout=timeout_ms)
        step(f"goto domcontentloaded  ({requests} req, {responses} resp, {bytes_in / 1024:.0f} KiB)")

        # In some regions (e.g. EU/Switzerland) Google redirects to a
        # consent.google.com interstitial; click through it. The click triggers
        # a navigation that can race; we just fire it and let the next
        # wait_for_selector below wait for the destination page to render.
        if "consent.google.com" in page.url:
            reject = page.locator('button[aria-label="Reject all"]').first
            reject.wait_for(state="visible", timeout=timeout_ms)
            reject.click(no_wait_after=True)
            step("dismissed consent")

        try:
            page.wait_for_selector(
                CHAT_HISTORY_SELECTOR, state="attached", timeout=timeout_ms
            )
        except PlaywrightTimeoutError as e:
            raise LayoutChangedError(
                f"Timed out waiting for '{CHAT_HISTORY_SELECTOR}' on {page.url}. "
                "Gemini's share-page layout may have changed; the script's "
                "selector needs updating."
            ) from e
        step(f"<div.chat-history> attached  ({requests} req, {responses} resp, {bytes_in / 1024:.0f} KiB)")

        # `networkidle` never fires on Gemini — it polls forever. Instead, wait
        # until the last <message-content> inside chat-history has rendered text.
        try:
            page.wait_for_function(
                """(sel) => {
                    const root = document.querySelector(sel);
                    if (!root) return false;
                    const nodes = root.querySelectorAll('message-content');
                    if (nodes.length === 0) return false;
                    const last = nodes[nodes.length - 1];
                    return (last.innerText || '').trim().length > 0;
                }""",
                arg=CHAT_HISTORY_SELECTOR,
                timeout=timeout_ms,
            )
        except PlaywrightTimeoutError as e:
            raise LayoutChangedError(
                f"Timed out waiting for rendered <message-content> inside "
                f"'{CHAT_HISTORY_SELECTOR}'. Gemini's share-page layout may "
                "have changed; the script's selector needs updating."
            ) from e
        step(f"last response has text       ({requests} req, {responses} resp, {bytes_in / 1024:.0f} KiB)")

        if full:
            html = page.content()
        else:
            html = page.eval_on_selector(
                CHAT_HISTORY_SELECTOR, "el => el.outerHTML"
            )
            if not html:
                raise LayoutChangedError(
                    f"'{CHAT_HISTORY_SELECTOR}' matched an element with empty "
                    "outerHTML. Gemini's share-page layout may have changed."
                )
        step("got HTML")
        browser.close()
        step("browser closed")

    return html


def preprocess(html: str) -> str:
    """Strip inline <svg> blocks and rewrite <user-query> as <blockquote>."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for svg in soup.find_all("svg"):
        svg.decompose()
    for uq in soup.find_all("user-query"):
        uq.name = "blockquote"
    return str(soup)


def to_markdown(html: str) -> str:
    """Convert HTML to GitHub-flavored Markdown via pandoc."""
    import pypandoc

    return pypandoc.convert_text(
        html,
        to="gfm-raw_html",
        format="html",
        extra_args=["--wrap=none", "--strip-comments"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url", help="e.g. https://gemini.google.com/share/XXXX")
    parser.add_argument(
        "-o", "--output", default="-", help="output file (default: stdout)"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="write the whole document instead of just the chat-history subtree",
    )
    parser.add_argument(
        "--preprocess",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="drop inline <svg> blocks and turn <user-query> into <blockquote> "
        "(on by default; --no-preprocess disables)",
    )
    parser.add_argument(
        "--markdown",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="convert to GitHub-flavored Markdown via pandoc (on by default; "
        "--no-markdown leaves output as HTML)",
    )
    parser.add_argument(
        "--timeout", type=int, default=30000, help="per-step timeout in ms (default 30000)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print per-step timing to stderr"
    )
    args = parser.parse_args()

    try:
        html = fetch(
            args.url, full=args.full, timeout_ms=args.timeout, verbose=args.verbose
        )
    except LayoutChangedError as e:
        sys.stderr.write(f"error: {e}\n")
        return 2

    def report(label: str, t_start: float) -> None:
        if args.verbose:
            sys.stderr.write(f"           +{time.perf_counter() - t_start:5.2f}s  {label}\n")

    if args.preprocess or args.markdown:
        t = time.perf_counter()
        html = preprocess(html)
        report("preprocessed (svg stripped, user-query→blockquote)", t)

    if args.markdown:
        t = time.perf_counter()
        output = to_markdown(html)
        report("pandoc → gfm", t)
    else:
        output = html

    if args.output == "-":
        sys.stdout.write(output)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
