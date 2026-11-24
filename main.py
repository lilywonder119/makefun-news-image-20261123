#!/usr/bin/env python3
"""THE WORLD DISPATCH — entry program for news-image-20261123 (Final 7).

The newspaper front page drawn by compose.py is stored beside this file
as entry.png. This program's only job is to deliver that page, byte for
byte, into the output directory the harness points at MAKEFUN_OUTPUT_DIR
(or /output when the variable is absent).

It is deliberately boring: standard library only (hashlib, os, sys), no
image processing at all, and it refuses to ship anything whose size or
digest differs from the page that was checked in with it. Two runs always
produce identical output because the input file never changes.
"""

import hashlib
import os
import sys

EXPECTED_BYTES = 317402
EXPECTED_SHA256 = "669c11c95d6cd4c5a574577d8e065a43deb28c07cc65c2bee8208b78ef1507a4"
HARD_LIMIT = 1048576  # the competition's 1 MiB ceiling
PNG_HEADER = b"\x89PNG\r\n\x1a\n"


def read_page():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png"), "rb") as fh:
        return fh.read()


def check_dimensions(page):
    """Second, independent guard: the IHDR chunk of a PNG carries the
    canvas size at bytes 16..24, and this entry must be exactly the
    1024 x 1024 square the competition demands. Reading it by hand keeps
    the program free of any imaging library."""
    if len(page) < 24:
        sys.exit("entry.png is too short to hold an IHDR chunk")
    width = int.from_bytes(page[16:20], "big")
    height = int.from_bytes(page[20:24], "big")
    if (width, height) != (1024, 1024):
        sys.exit("entry.png canvas is %dx%d, expected 1024x1024" % (width, height))


def main():
    page = read_page()

    if not page.startswith(PNG_HEADER):
        sys.exit("entry.png is not a PNG file")
    check_dimensions(page)
    if len(page) > HARD_LIMIT:
        sys.exit("entry.png exceeds the 1 MiB limit: %d bytes" % len(page))
    if len(page) != EXPECTED_BYTES:
        sys.exit("entry.png size drifted: %d != %d" % (len(page), EXPECTED_BYTES))
    digest = hashlib.sha256(page).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 drifted: %s" % digest)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(page)

    sys.stderr.write("delivered %s (%d bytes, sha256 %s)\n" % (target, len(page), digest))


if __name__ == "__main__":
    main()
