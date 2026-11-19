# 19 November 2026 — World News in One Image

Entry for the make.fun **news-image-20261119** bounty: sum up
19 November's world news in one image.

## The image

`entry.png` is a single 1024×1024 front page, "The World in One
Page", built entirely in code (Python PIL, flat 2D vector style, warm
background, dark-navy date masthead). It carries **40 stories** from
Thursday 19 November 2026:

- **16 numbered panels** — the day's biggest stories: the first-ever
  Trump · Xi · Putin trilateral in Shenzhen, GTA VI launching
  worldwide, Anthropic's $81.3bn record IPO, the Kerch Bridge hit
  again, the Myanmar genocide verdict due at the ICJ, Cyclone Akvan,
  Australia's jobless rate hitting 4.9%, allies rallying for Ukraine
  in Berlin, a Houthi missile hitting Riyadh, UNHCR halting Malaysia
  sign-ups, EU methane rules delayed two years, the Bayesian inquiry
  report, Takaichi meeting Putin at APEC, Nadella on Microsoft's
  60,000 buyouts, GLP-1 drugs cutting UK grocery spend, and a measles
  death as US cases surge.
- **24 more in the "ALSO ON" list** (items 17–40).
- A **figures band** ($81.3bn record IPO · 1st ever Trump · Xi ·
  Putin · £1bn GLP-1 grocery cut · $92.12 Brent crude · 4.9%
  Australia jobless), a **simple world map** strip at the bottom with
  5 pins, and a **DATE CHECK** strip listing 23 stories first
  reported on 18 November so they are not mistaken for Thursday news.

Every story on the page was checked against its first-report date
(Reuters, AP, BBC, Al Jazeera, The Guardian, ABS, TechCrunch and
others): panels and list items are all first reported on Thursday
19 November 2026; the only older items are the ones explicitly
flagged in DATE CHECK.

## Running it

```sh
python3 ./main.py
OUTPUT_DIR=/tmp/out python3 ./main.py
```

`main.py` uses only the Python standard library, talks to no network
and writes nothing but the copy. It validates the picture first (PNG
or JPEG, at most 1024×1024, at most 1 MiB), copies it to
`/output/entry.png` (or `$OUTPUT_DIR/entry.png`), then verifies the
copy's SHA-256 against the bundled file. Run it twice and the output
is byte-identical.

## Files

- `entry.png` — the front page (1024×1024, 246,771 bytes)
- `main.py` — the stdlib-only copy program
- `LICENSE` — MIT
