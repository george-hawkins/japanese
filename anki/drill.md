# Drilling Anki Cards Without Wrecking Your Schedule

How to zip through a set of cards *n* times to drum them into your head — before
you commit to a real "know / don't know" — without using the "Again" button as a
makeshift drill loop.

## Methods that don't touch the SRS

### Filtered Deck ("Cram Mode")

A filtered deck is a temporary sandbox: you can see the cards as many times as
you like without affecting their real due dates or scheduling progress.

**Set it up:**

1. Open the Browser — press `B`.
2. Select the new cards you want to drill.
3. **Edit → Create Filtered Deck** (or `Ctrl + G`).
4. Configure:
   - **Search** — auto-fills from your selection.
   - **Limit** — set to the number of cards you want to see.
   - **Reschedule cards based on my answers** — **UNCHECK THIS.** This is the
     key step. With it off, your `1/2/3/4` clicks don't count toward the card's
     permanent history.
5. Click **Build**. A temporary deck appears on your home screen.

**Drill *n* times:** when you finish, the cards just sit there. Click the
filtered deck → **Rebuild** (bottom of screen) → zip through them again.

**When done:** delete the filtered deck. The cards return safely to their
original home deck, exactly as they were before.

### Browser Preview (the quickest way)

If you don't even want to click answer buttons and just want to flip through:

1. Go to the **Browser**.
2. Select the cards.
3. Click **Preview** (top right, or `Ctrl + Shift + P`).
4. Use the **arrow keys** to flip rapidly through fronts and backs.

### At a glance

| Feature         | Filtered Deck (Cram)            | Browser Preview            |
| --------------- | ------------------------------- | -------------------------- |
| Active recall?  | Yes — shows front, then back    | Optional — you see what you want |
| Affects SRS?    | No (if Reschedule is off)       | No                         |
| Repeatability   | Easy "Rebuild" button           | Just scroll back up        |
| Best for        | A 15-minute "pre-study" session | A 2-minute sanity check    |

> **A small warning:** the "magic" of Anki happens when you *struggle* a little
> to remember. Don't drill so many times that you're just memorizing the *order*
> of the cards rather than the content.

## The first time you see a card

That initial "click of shame" on a card you've literally never laid eyes on
feels less like studying and more like being interrogated for a crime you didn't
commit. There are a few ways to handle it.

### 1. Education first — learn it *before* Anki

Common power-user advice: never learn something for the first time *inside* Anki.
Anki is a tool for **memory**, not understanding. Seeing cards with zero context
forces your brain to memorize "shapes" and "strings of text" rather than
concepts.

**The fix:** before studying a batch of 10–20 cards, open the Browser, select
them, and read through them — front and back, Googling a term if it's confusing.
Now when you study, you're seeing each card for the *second* time, and the answer
buttons actually mean something.

### 2. Tweak your Learning Steps

If you'd rather learn inside the app, soften the sting of "failing" a new card:

- **Deck Options** (gear icon) → **Learning Steps**.
- Default is often `1m 10m`. Change it to something like `1m 5m 15m`.

You see the card → `Again` (1m) → it returns almost immediately → `Good` (5m) →
and by the time you clear the 15m step you've genuinely *learned* it this
session. It feels like "staging" a card rather than failing it.

### 3. The mindset shift — the "Seed" button

If you don't want to change any settings, change your relationship with the
`Again` button. The first time you see a new card is the **Seed Phase**:

- `Again` does **not** mean "I forgot this."
- `Again` means "I am planting this seed."

### Recommended warm-up flow

Especially for someone else's imported deck — where you lack the connection the
card's creator had — a 3-step warm-up works well:

1. **Browse** — select the 10–20 cards you plan to release today.
2. **Preview** — flip through them (~60 seconds).
3. **Study** — start your session.

This removes the "what on earth is this?" factor and lets you use your brain for
recall instead of first-time reading.

## Is hitting "Again" on a new card actually harmful?

**No.** You are *not* punished for hitting `Again` on **New** or **Learning**
cards:

- **Ease factor** — hitting `Again` here does not lower the card's ease (the
  variable controlling how fast intervals grow).
- **Leech status** — Anki only counts *lapses* on cards you've already graduated.
  Failures while still learning a card for the first time don't count.

You could hit `Again` 50 times on a brand-new card today and the algorithm won't
think you're "bad" at it tomorrow.

The penalties only kick in once a card has **Graduated** — passed its learning
steps and been pushed a few days out, becoming a **Review** card (green numbers):

- **Ease factor** — `Again` here *does* lower the ease (typically by 20%).
- **Leech status** — each `Again` counts as a lapse; after a threshold (usually
  8), Anki tags the card a **leech** and may auto-suspend it.

So drilling new cards with `Again` is safe — it just isn't the *best* tool.
Filtered Deck or Browser Preview keep your "learning" headspace separate from
your "testing" headspace. Using `Again` to drill a new card is like using a
sledgehammer to tap in a thumbtack: it works and won't break the wall, but it's
not the right tool for the job.
