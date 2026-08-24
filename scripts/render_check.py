#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader


def main():
    parser = argparse.ArgumentParser(description="Validate page count and render a resume PDF for visual QA.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--render-dir", type=Path, default=Path("tmp/rendered"))
    args = parser.parse_args()

    if not args.pdf.exists():
        parser.error(f"File not found: {args.pdf}")
    pages = len(PdfReader(str(args.pdf)).pages)
    if pages != 1:
        raise SystemExit(f"FAIL: expected exactly 1 page, got {pages}")

    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise SystemExit("FAIL: pdftoppm is required for render validation")
    args.render_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.render_dir / args.pdf.stem
    subprocess.run([renderer, "-f", "1", "-singlefile", "-png", "-r", "150", str(args.pdf), str(prefix)], check=True)
    print(f"PASS: 1-page A4 PDF; preview: {prefix}.png")


if __name__ == "__main__":
    main()
