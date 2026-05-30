# Controlling new-card release in an imported Anki deck

**Goal:** explicitly decide when new cards become available — e.g. release 10 today, and have *zero* new cards appear tomorrow unless I act again.

By default Anki releases new cards every day up to the deck's "New cards/day" limit. Two ways to take manual control:

## Method 1 — Zero-limit

1. Deck gear icon → **Options** → **Daily Limits** → set **New cards/day** to `0`.
2. On a day you want to learn, click the deck → **Custom Study** (bottom of screen).
3. Choose **Increase today's new card limit** and enter `10`.

Anki releases those 10 immediately. Tomorrow the limit resets to `0`, so nothing new appears unless you repeat Custom Study.

- Effort: very low.
- Control: random cards from the top of the deck.
- Best for: small, simple decks.

## Method 2 — Suspend (recommended for large decks)

1. **Suspend everything:** open **Browse**, select the deck, click a card, `Cmd/Ctrl+A` to select all, right-click → **Suspend** (`Ctrl+J`). Suspended cards turn yellow.
2. Set the deck's **New cards/day** high (e.g. `999`).
3. **Release** when ready: in the Browser, select the specific 10 cards (or topics) you want and **Unsuspend** them.

Unsuspending makes those cards available for study; with a high limit they show up instantly, and nothing else appears until you unsuspend more.

- Effort: slightly higher (requires browsing).
- Control: you pick exactly which cards/topics.
- Best for: large decks (medical, language, etc.).
- Bonus: avoids being "spoiled" by cards you haven't reviewed in the browser yet.

## Which to use

| | Zero-limit | Suspend |
|---|---|---|
| Effort | Very low | Slightly higher |
| Control | Random from top | Pick exact cards/topics |
| Best for | Small/simple decks | Large decks |

For an imported pre-made deck, the Suspend method is usually superior.
