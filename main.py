#!/usr/bin/env python3
"""make.fun bounty news-image-20261117: sum up 17 November 2026 world news
in one image.

Deterministic, no network at runtime (except the make.fun program/v1
harness handshake when MAKEFUN_ENV_URL is set), no randomness, no
timestamps. Renders a 1024x1024 PNG infographic with Pillow and writes it
to /output/entry.png (or ./out/entry.png when /output is unavailable).

Run:  python3 main.py
Requires: Pillow (pip install pillow)
"""

import json
import os
import socket
import sys
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    print("Pillow is required: pip install pillow", file=sys.stderr)
    raise

WIDTH, HEIGHT = 1024, 1024

# --- News content: reported for Tuesday 17 November 2026 -------------------
# Sources (see README.md): Reuters via Profile News, Associated Press,
# ABC News (World News Tonight), NPR News Now, Fox News / PAHO, BBC.
STORIES = [
    {
        "tag": "MIDDLE EAST",
        "color": (176, 42, 42),
        "headline": "U.S. strikes Iran after Hormuz tanker attacks",
        "summary": "U.S. warplanes hit a missile site on Qeshm Island; a tanker "
                   "burned off Oman and 24 crew were evacuated.",
    },
    {
        "tag": "UKRAINE",
        "color": (31, 93, 140),
        "headline": "Ukraine hits the Crimean Bridge again",
        "summary": "Kyiv says drones and missiles struck the bridge in reply to "
                   "Russian attacks; Moscow claims 1,336 drones shot down.",
    },
    {
        "tag": "ASIA SUMMIT",
        "color": (146, 96, 10),
        "headline": "Trump, Xi and Putin head for Shenzhen summit",
        "summary": "Trump travels to China for a first three-way meeting with "
                   "Xi Jinping and Vladimir Putin at the APEC forum.",
    },
    {
        "tag": "HEALTH",
        "color": (25, 122, 82),
        "headline": "U.S. loses measles elimination status",
        "summary": "Health officials say the U.S. can no longer claim measles "
                   "eliminated, for the first time since 2000.",
    },
    {
        "tag": "TECH",
        "color": (90, 55, 150),
        "headline": "Nvidia: record sales, ex-CEO scandal",
        "summary": "Nvidia posts record revenue; ex-CEO Jensen Huang, who quit "
                   "in a spy-linked scandal, says he would return if asked.",
    },
    {
        "tag": "MARKETS",
        "color": (180, 84, 20),
        "headline": "Wall Street falls; Apple and banks hit by outages",
        "summary": "AI and tech stocks led U.S. shares lower; Apple iCloud and "
                   "banks suffered outages officials say were not a hack.",
    },
]

NAVY = (10, 37, 64)
GOLD = (212, 175, 55)
BG = (244, 241, 234)
CARD = (255, 255, 255)
INK = (18, 24, 32)
MUTED = (84, 92, 102)


def _font(name, size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % name,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = lambda s: _font("-Bold", s)
FONT_BODY = lambda s: _font("", s)


def wrap(draw, text, font, max_width):
    """Wrap text to fit max_width pixels; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def render():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)

    # --- Header -----------------------------------------------------------
    d.rectangle([0, 0, WIDTH, 168], fill=NAVY)
    d.rectangle([0, 168, WIDTH, 174], fill=GOLD)
    f_eyebrow = FONT_TITLE(22)
    f_title = FONT_TITLE(76)
    f_date = FONT_TITLE(40)
    d.text((36, 22), "TUESDAY  •  WORLD NEWS", font=f_eyebrow, fill=GOLD)
    d.text((34, 52), "WORLD NEWS", font=f_title, fill=(255, 255, 255))
    d.text((36, 128), "17 NOVEMBER 2026", font=f_date, fill=GOLD)
    # Right-hand header note
    f_note = FONT_BODY(20)
    for i, line in enumerate(["Six stories that", "defined the day"]):
        d.text((800, 46 + i * 26), line, font=f_note, fill=(200, 210, 220))
    d.text((800, 108), "17 NOV 2026", font=FONT_TITLE(20), fill=(255, 255, 255))

    # --- Subtitle strip ----------------------------------------------------
    f_sub = FONT_BODY(21)
    d.text((36, 188),
           "From the Strait of Hormuz to Shenzhen: the day in six stories.",
           font=f_sub, fill=MUTED)

    # --- Story cards: 2 columns x 3 rows ----------------------------------
    margin, gap = 28, 16
    card_w = (WIDTH - 2 * margin - gap) // 2
    card_h = 228
    top = 226
    f_tag = FONT_TITLE(19)
    f_head = FONT_TITLE(27)
    f_sum = FONT_BODY(20)
    f_num = FONT_TITLE(30)

    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (card_w + gap)
        y0 = top + row * (card_h + gap)
        x1, y1 = x0 + card_w, y0 + card_h
        rounded_rect(d, [x0, y0, x1, y1], radius=14, fill=CARD)
        d.rectangle([x0, y0 + 14, x0 + 9, y1 - 14], fill=s["color"])
        d.text((x1 - 52, y0 + 14), "%02d" % (i + 1), font=f_num,
               fill=(220, 224, 230))
        d.text((x0 + 26, y0 + 16), s["tag"], font=f_tag, fill=s["color"])
        head_lines = wrap(d, s["headline"], f_head, card_w - 52)
        y = y0 + 48
        for line in head_lines[:2]:
            d.text((x0 + 26, y), line, font=f_head, fill=INK)
            y += 34
        y += 6
        for line in wrap(d, s["summary"], f_sum, card_w - 52)[:3]:
            d.text((x0 + 26, y), line, font=f_sum, fill=MUTED)
            y += 27

    # --- Footer ------------------------------------------------------------
    fy = 950
    d.rectangle([0, fy, WIDTH, HEIGHT], fill=NAVY)
    d.text((36, fy + 18), "Summary of 17 Nov 2026 world news",
           font=FONT_TITLE(22), fill=(255, 255, 255))
    d.text((36, fy + 46), "Sources: Reuters, Associated Press, ABC News, NPR, PAHO",
           font=FONT_BODY(17), fill=(180, 192, 204))
    return img


def choose_output_path():
    """Primary: /output/entry.png if /output exists or can be created,
    else ./out/entry.png."""
    try:
        os.makedirs("/output", exist_ok=True)
        return "/output/entry.png"
    except OSError:
        os.makedirs("out", exist_ok=True)
        return os.path.join("out", "entry.png")


def write_image(path):
    img = render()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    img.save(path, format="PNG")
    return path


# --- program/v1 harness ----------------------------------------------------
class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            body = b'{"status":"ok"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


def run_harness(env_url, timeout_s=1800):
    """Register with the make.fun harness and wait until it says done."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    port = server.server_address[1]
    assert port != 8080, "harness must never use port 8080"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = env_url.rstrip("/")
    req = urllib.request.Request(
        base + "/register",
        data=json.dumps({"port": port}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    last_err = None
    for _ in range(10):
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                resp.read()
            last_err = None
            break
        except Exception as exc:  # retry briefly; harness may not be ready
            last_err = exc
            time.sleep(1)
    if last_err is not None:
        print("register failed: %s" % last_err, file=sys.stderr)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base + "/done", timeout=5) as resp:
                body = resp.read().decode("utf-8", "replace").strip().lower()
            if "done" in body or '"done":true' in body.replace(" ", ""):
                break
        except Exception:
            pass
        time.sleep(2)
    server.shutdown()


def main():
    path = choose_output_path()
    write_image(path)
    print("wrote %s" % path)
    # Also keep a local copy for inspection when running outside the harness.
    if os.environ.get("MAKEFUN_ENV_URL") is None and path != os.path.join("out", "entry.png"):
        local = os.path.join("out", "entry.png")
        write_image(local)
        print("wrote %s" % local)
    env_url = os.environ.get("MAKEFUN_ENV_URL")
    if env_url:
        run_harness(env_url)


if __name__ == "__main__":
    main()
