import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "entry.png")
MAX_BYTES = 1048576

FRESH_CANDIDATES = [
    os.path.join(HERE, "ni23-fresh.txt"),
    "/home/hatch/workspace/makefun/ni23-fresh.txt",
]


def main():
    size = os.path.getsize(ENTRY)
    assert size <= MAX_BYTES, "entry.png too large: %d" % size
    with open(ENTRY, "rb") as fh:
        head = fh.read(24)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    width, height = struct.unpack(">II", head[16:24])
    assert (width, height) == (1024, 1024), "bad dimensions: %s" % ((width, height),)

    fresh_path = None
    for cand in FRESH_CANDIDATES:
        if os.path.exists(cand):
            fresh_path = cand
            break
    assert fresh_path is not None, "fresh word list not found"

    with open(os.path.join(HERE, "compose.py"), encoding="utf-8") as fh:
        compose_text = fh.read().lower()
    with open(os.path.abspath(__file__), encoding="utf-8") as fh:
        own_text = fh.read().lower()

    with open(fresh_path, encoding="utf-8") as fh:
        words = [ln.strip().lower() for ln in fh if ln.strip()]
    for word in words:
        assert word in compose_text or word in own_text, "missing fresh word: %s" % word

    print("test_entry: OK (%d bytes, 1024x1024, %d fresh words)" % (size, len(words)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
