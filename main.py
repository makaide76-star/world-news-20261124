#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261124 bounty.

Copies the front-page image for Tuesday 24 November 2026
(assets/entry.png, drawn by tools/make_image.py) to the output
directory named by MAKEFUN_OUTPUT_DIR.

Stdlib only, no network, deterministic: the source image is resolved
relative to this file, never relative to the cwd, and nothing is ever
written into the repository itself. Every run writes identical bytes.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    size = os.path.getsize(dst)
    print("Wrote %s (%d bytes)" % (dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
