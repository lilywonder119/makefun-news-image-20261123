#!/usr/bin/env python3
"""THE WORLD DISPATCH front page, delivered untouched.

compose.py rendered the Monday edition of THE WORLD DISPATCH and saved
the finished page next to this script as entry.png. My task here is
narrow on purpose: carry those exact bytes to wherever the harness
asks for them, and complain loudly if the page on disk is not the page
that was verified before commit.

Nothing in here draws, resizes or re-encodes. The only tools are the
Python standard library (hashlib for the fingerprint, os for paths,
sys for the exit channel), so the output of the first run and the
output of the fiftieth run are the same file, bit for bit. The page
covers the World Chess Championship crowds of Monday 23 November
2026, and it travels exactly as it was composed.
"""

import hashlib
import os
import sys

# Fingerprint of the checked-in page. Both numbers were taken from the
# verified entry.png at commit time; if either drifts, delivery stops.
EXPECTED_BYTES = 317402
EXPECTED_SHA256 = "669c11c95d6cd4c5a574577d8e065a43deb28c07cc65c2bee8208b78ef1507a4"

# The eight magic bytes every PNG starts with, and the square canvas
# the competition fixes for this edition.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CANVAS = (1024, 1024)


def load_page():
    """Read entry.png from the folder this script lives in."""
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, "entry.png"), "rb") as handle:
        return handle.read()


def verify(page):
    """Refuse to ship a page that fails any of the pinned checks."""
    if not page.startswith(PNG_SIGNATURE):
        sys.exit("entry.png: missing PNG signature")
    if len(page) < 24:
        sys.exit("entry.png: truncated before the IHDR fields")
    size = (int.from_bytes(page[16:20], "big"),
            int.from_bytes(page[20:24], "big"))
    if size != CANVAS:
        sys.exit("entry.png: canvas is %dx%d, want %dx%d"
                 % (size[0], size[1], CANVAS[0], CANVAS[1]))
    if len(page) != EXPECTED_BYTES:
        sys.exit("entry.png: %d bytes, want %d" % (len(page), EXPECTED_BYTES))
    digest = hashlib.sha256(page).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png: sha256 mismatch (%s)" % digest)
    return digest


def main():
    page = load_page()
    digest = verify(page)

    destination = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(destination, exist_ok=True)
    target = os.path.join(destination, "entry.png")
    with open(target, "wb") as handle:
        handle.write(page)

    sys.stderr.write("THE WORLD DISPATCH delivered: %s "
                     "(%d bytes, sha256 %s)\n"
                     % (target, len(page), digest))


if __name__ == "__main__":
    main()
