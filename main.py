#!/usr/bin/env python3
"""Publish the prepared front page for the 24 November 2026 edition.

The artwork for this entry was rendered ahead of time and is stored in
the repository as ``assets/entry.png``.  Nothing is drawn at run time:
this program simply delivers that finished page by copying it into the
output directory the harness points at.

Only modules from the Python standard library are imported, so the
script works in a bare interpreter with nothing extra installed.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

PAGE_FILENAME = "entry.png"
OUTPUT_ENV_VARS = ("MAKEFUN_OUTPUT_DIR", "ENTRY_OUTPUT_DIR")


def stored_page() -> Path:
    """Locate the front-page image that ships with this repository."""
    here = Path(__file__).resolve().parent
    return here / "assets" / PAGE_FILENAME


def pick_output_folder() -> Path:
    """Choose where the page goes.

    The harness names the destination through an environment variable;
    when neither variable is set, the page is left in the assets folder
    it already lives in.
    """
    for var in OUTPUT_ENV_VARS:
        value = os.environ.get(var)
        if value:
            return Path(value)
    return stored_page().parent


def deliver_page() -> Path:
    """Copy the stored page into the output folder and report its path."""
    source = stored_page()
    folder = pick_output_folder()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / PAGE_FILENAME
    if target.resolve() != source.resolve():
        shutil.copyfile(source, target)
    return target


def main() -> int:
    result = deliver_page()
    print(f"Delivered the 24 November 2026 front page to {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
