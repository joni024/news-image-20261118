#!/usr/bin/env python3
"""Entrypoint for make.fun competition news-image-20261118.

The infographic for Wednesday 18 November 2026 is stored in this
repository as base64 text (image_b64.txt), so the entry contains no
binary file. This program decodes it, checks that the bytes are a PNG
of at most 1 MiB, and writes entry.png into the output directory.

Standard library only, no network, deterministic: every run writes
the same bytes to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
"""
import base64
import os
import struct
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024

IMAGE_B64 = Path(__file__).resolve().parent / "image_b64.txt"


def png_dimensions(raw: bytes) -> tuple[int, int]:
    """Read width and height from the PNG IHDR chunk (bytes 16..24)."""
    width, height = struct.unpack(">II", raw[16:24])
    return width, height


def load_image() -> bytes:
    raw = base64.b64decode(IMAGE_B64.read_text(encoding="ascii").strip())
    if not raw.startswith(PNG_MAGIC):
        raise ValueError("image_b64.txt does not decode to a PNG image")
    if len(raw) > MAX_BYTES:
        raise ValueError(f"decoded image is {len(raw)} bytes, over the "
                         f"{MAX_BYTES} byte limit")
    width, height = png_dimensions(raw)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"decoded image is {width}x{height}, over the "
                         f"{MAX_SIDE}x{MAX_SIDE} limit")
    return raw


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(load_image())


if __name__ == "__main__":
    main()
