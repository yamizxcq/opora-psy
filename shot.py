# -*- coding: utf-8 -*-
"""Снимок лендинга целиком через headless Edge + нарезка на куски.

Edge снимает окно, а не документ, поэтому окно делаем заведомо высоким,
после чего обрезаем пустой низ и режем полотно на экраны — так удобно
просматривать вёрстку постранично.

    PYTHONIOENCODING=utf-8 python shot.py              # десктоп 1440
    PYTHONIOENCODING=utf-8 python shot.py 420          # телефон
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TALL = 15000          # запас по высоте, лишнее обрежется
CHUNK = 1100          # высота одного куска при нарезке


MIN_WIN = 500     # уже этого Edge окно не делает: просит 420 — рисует 476
                  # и обрезает снимок справа, из-за чего вёрстка кажется битой


def shot(width, dest):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=%d,%d" % (width, TALL),
                        "--virtual-time-budget=6000",
                        "--screenshot=" + dest,
                        "file:///" + os.path.join(HERE, "index.html").replace("\\", "/"),
                        "--user-data-dir=" + os.path.join(tmp, "ud")],
                       capture_output=True, timeout=180)
    return os.path.exists(dest)


def trim(path):
    """Обрезать однотонный хвост внизу."""
    im = Image.open(path).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((im.width - 2, im.height - 2)))
    box = ImageChops.difference(im, bg).getbbox()
    if box:
        im = im.crop((0, 0, im.width, min(im.height, box[3] + 2)))
    im.save(path)
    return im


def main():
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
    if width < MIN_WIN:
        print("ширина поднята до %d — Edge не рисует окно уже" % MIN_WIN)
        width = MIN_WIN
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    full = os.path.join(OUT, "page-%d.png" % width)
    if not shot(width, full):
        print("не снялось")
        return
    im = trim(full)
    print("full", full, im.size)
    n = 0
    for top in range(0, im.height, CHUNK):
        n += 1
        part = os.path.join(OUT, "p%d-%02d.png" % (width, n))
        im.crop((0, top, im.width, min(im.height, top + CHUNK))).save(part)
    print("кусков:", n)


if __name__ == "__main__":
    main()
