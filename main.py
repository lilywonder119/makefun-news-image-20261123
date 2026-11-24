"""THE FULL RECORD — NI23 G4 entry carrier for Final 7.

Stdlib-only, copy-only: main.py never draws anything. It carries the
finished entry.png (drawn locally by compose.py) into MAKEFUN_OUTPUT_DIR.
"""
import os
import shutil
import sys


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(target_dir, exist_ok=True)
    source = os.path.join(here, "entry.png")
    dest = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, dest)
    # Revision pass: the copy is the whole job — no transforms, ever.
    return 0


if __name__ == "__main__":
    sys.exit(run())
