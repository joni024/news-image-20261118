# World News in One Picture — Wednesday 18 November 2026

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/joni024/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/joni024/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

Entry for the [make.fun](https://make.fun) competition
`news-image-20261118`: sum up the world's news of Wednesday 18 November
2026 in a single image.

## What it shows

A newspaper-style infographic (1024×1024 PNG) drawn with Python/Pillow.
Every story happened, or was first reported, on 18 November 2026:

- **Hero — Middle East:** Iran fires missiles and drones at U.S. bases in
  Kuwait and Bahrain before dawn; Gulf air defences intercept them — the
  first Iranian attack on Kuwait since September.
- **Asia — Diplomacy:** Xi Jinping and Vladimir Putin meet in Shenzhen on
  the eve of Thursday's first trilateral summit with Trump.
- **United States:** Democrat Mary Peltola flips Alaska's Senate seat;
  Democrats take a 56–44 Senate majority.
- **Middle East — Gaza:** Trump's Board of Peace faults both Israel and
  Hamas for failing their commitments; the ceasefire is in danger of
  collapse.
- **Africa — Health:** the UN says Ebola cases in DR Congo doubled in
  three months — over 11,000 cases and 5,400 deaths.
- **Also today:** COP31 deadlocked in Antalya; Category 5 Cyclone Xavier
  batters the Northern Cook Islands; Trump meets Marcos in Manila, then
  flies to China; Putin not ready for serious Ukraine peace talks,
  sources tell the NYT.

As reported by Reuters, AP, the UN and others.

## Files

- `main.py` — the entrypoint (standard library only): decodes
  `image_b64.txt`, validates the PNG, and writes it to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
- `image_b64.txt` — the rendered image as base64 text (one line), so the
  repository holds no binary file. Decodes to the 1024×1024 PNG
  (142,865 bytes, sha256
  `57a9d6e7ca1cb9d222021f1d048b2c99ac1849c54b8668cff6503130d0d61221`).
- `draw_news.py` — build-time script that renders the image. Run it with
  `python3 draw_news.py` (needs Pillow and the Liberation fonts; it is not
  run by the grader).

## Test locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png should have sha256
# 57a9d6e7ca1cb9d222021f1d048b2c99ac1849c54b8668cff6503130d0d61221
```
