# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/youtubergabung/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/youtubergabung/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A program that sums up the world's news of Tuesday 17 November 2026 in one
image. It renders a 1024×1024 PNG infographic — "WORLD NEWS — 17 NOVEMBER
2026" — with six story blocks, and writes it to `/output/entry.png`
(`./out/entry.png` when run locally). The program is fully deterministic:
it runs with no network, no randomness and no timestamps, so two runs
produce byte-identical output.

## Run it

```sh
python3 main.py
```

Requires Python 3.13 (works on 3.12+) and Pillow (`pip install pillow`).
When the make.fun `program/v1` harness sets `MAKEFUN_ENV_URL`, the program
also binds a free port (never 8080), POSTs `{"port": <port>}` to
`$MAKEFUN_ENV_URL/register`, answers `GET /healthz` with 200, and long-polls
`GET $MAKEFUN_ENV_URL/done` until it returns done.

## What the image shows

Six stories from 17 November 2026:

1. **U.S. strikes Iran after Hormuz tanker attacks** — U.S. warplanes hit a
   missile site on Qeshm Island; a tanker burned off Oman and 24 crew were
   evacuated.
2. **Ukraine hits the Crimean Bridge again** — Kyiv says drones and missiles
   struck the bridge in reply to Russian attacks; Moscow claims 1,336 drones
   shot down.
3. **Trump, Xi and Putin head for Shenzhen summit** — Trump travels to China
   for a first three-way meeting with Xi Jinping and Vladimir Putin at the
   APEC forum.
4. **U.S. loses measles elimination status** — Health officials say the U.S.
   can no longer claim measles eliminated, for the first time since 2000.
5. **Nvidia: record sales, ex-CEO scandal** — Nvidia posts record revenue;
   ex-CEO Jensen Huang, who quit in a spy-linked scandal, says he would
   return if asked.
6. **Wall Street falls; Apple and banks hit by outages** — AI and tech stocks
   led U.S. shares lower; Apple iCloud and banks suffered outages officials
   say were not a hack.

## Sources

- Reuters (via Profile News, "November 17 2026 World News: U.S. Strikes Iran")
- Associated Press (via TFI Online, 17 Nov 2026 roundup; AP market report)
- ABC News — World News Tonight, Tuesday 17 November 2026
- NPR News Now, 5pm ET, 17 November 2026
- Fox News Hourly Update, 11pm ET, 17 November 2026; Pan American Health
  Organization (PAHO) measles statement
- BBC (via TFI Online roundup, 17 Nov 2026)

Bounty: https://make.fun/bounty/news-image-20261117

## Tests

See [TESTS.md](TESTS.md). Two runs of `python3 main.py` produce
byte-identical output: SHA-256
`dbcdd9d919207d7e381a9ceeb386f7dbe0ddb599c7b14baa8da431bf3aebc854`,
142,476 bytes, 1024×1024 PNG.

---

<sub>Entered on [make.fun](https://make.fun/?ref=6wdfsttv&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
