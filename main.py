"""Deliver the 19 November 2026 front page to the bounty output.

This is the entry program for the make.fun news-image-20261119
bounty, "Sum up 19 November's world news in one image". The front
page itself lives next to this file as entry.png; this program's whole
job is to place an exact duplicate of that picture at
/output/entry.png, where the bounty harness expects it.

Design notes, kept deliberately boring:

- Only the Python standard library is used. No network, no random
  numbers, no wall-clock reads, no environment other than OUTPUT_DIR.
- The picture is checked before it is written: it must be a readable
  PNG or JPEG, no wider or taller than 1024 pixels, and no heavier
  than one mebibyte. Anything else stops the run with a nonzero exit.
- After copying, the program fingerprints both the bundled picture
  and the copy and refuses to report success unless the two hashes
  match, so a truncated write cannot pass silently.
- Running the program twice produces the same bytes twice.

Usage:
    python3 ./main.py
    OUTPUT_DIR=/tmp/out python3 ./main.py
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1_048_576
MAX_EDGE = 1024


def read_png_size(blob):
    """Return (width, height) for a PNG blob, else None."""
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if blob[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def read_jpeg_size(blob):
    """Return (width, height) for a JPEG blob, else None."""
    pos = 2
    while pos + 9 < len(blob):
        if blob[pos] != 0xFF:
            return None
        marker = blob[pos + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", blob[pos + 5:pos + 9])
            return width, height
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
        else:
            (length,) = struct.unpack(">H", blob[pos + 2:pos + 4])
            pos += 2 + length
    return None


def measure(blob):
    """Return (width, height) for a PNG or JPEG blob, else None."""
    size = read_png_size(blob)
    if size is not None:
        return size
    return read_jpeg_size(blob)


def die(message):
    """Print an error to stderr and exit nonzero."""
    print(f"main.py: {message}", file=sys.stderr)
    return 1


def main():
    """Copy the bundled front page to the output directory."""
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return die(f"cannot create output directory {out_dir}: {exc}")
    target = out_dir / "entry.png"

    try:
        blob = SOURCE.read_bytes()
    except OSError as exc:
        return die(f"cannot read the bundled picture {SOURCE}: {exc}")
    size = measure(blob)
    if size is None:
        return die("entry.png is not a readable PNG or JPEG")
    width, height = size
    if width > MAX_EDGE or height > MAX_EDGE:
        return die(
            f"entry.png is {width}x{height}, larger than "
            f"{MAX_EDGE}x{MAX_EDGE}"
        )
    if len(blob) > MAX_BYTES:
        return die(
            f"entry.png is {len(blob)} bytes, over the "
            f"{MAX_BYTES} byte limit"
        )

    shutil.copyfile(SOURCE, target)
    digest = hashlib.sha256(blob).hexdigest()
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        return die("the written copy does not match the bundled picture")

    print(
        f"wrote {target}: {len(blob)} bytes, {width}x{height}, "
        f"sha256={digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
