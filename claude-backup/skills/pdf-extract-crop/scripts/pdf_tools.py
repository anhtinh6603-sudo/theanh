#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
import textwrap
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = SCRIPT_DIR.parents[2]
TMP_DIR = Path('/tmp/pdf-extract-crop')
TMP_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or 'Command failed')
    return result.stdout.strip()


def write_file(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding='utf-8')


def extract_text(pdf, out):
    # Browser/PDF parsing libraries are not guaranteed in this environment.
    # This command stores a clear explanation for the operator and leaves a hook for future upgrades.
    msg = textwrap.dedent(f"""
    PDF text extraction placeholder.
    Source PDF: {pdf}

    Suggested next step:
    - If pypdf/pdfplumber is installed later, extend this script to parse text directly.
    - If the PDF is visual only, use page-shot + OCR workflow externally.
    """).strip() + "\n"
    write_file(out, msg)
    print(out)


def render_page_shot(pdf, page, out):
    # Render the requested PDF page to PNG via pdfjs + canvas instead of browser PDF viewer.
    js = f"""
const fs = require('fs');
const path = require('path');
const pdfjsLib = require('pdfjs-dist/legacy/build/pdf.mjs');
const {{ createCanvas }} = require('@napi-rs/canvas');

(async () => {{
  const data = new Uint8Array(fs.readFileSync(path.resolve({pdf!r})));
  const loadingTask = pdfjsLib.getDocument({{ data, useSystemFonts: true }});
  const pdf = await loadingTask.promise;
  const page = await pdf.getPage({page});
  const viewport = page.getViewport({{ scale: 2.0 }});
  const canvas = createCanvas(Math.ceil(viewport.width), Math.ceil(viewport.height));
  const context = canvas.getContext('2d');
  await page.render({{ canvasContext: context, viewport }}).promise;
  fs.writeFileSync(path.resolve({out!r}), canvas.toBuffer('image/png'));
  console.log(path.resolve({out!r}));
}})().catch(err => {{ console.error(err.stack || err.message); process.exit(1); }});
"""
    run(['bash', '-lc', f"node - <<'NODE'\n{js}\nNODE"])
    print(out)


def crop_image(image, x, y, w, h, out):
    # Use a small Node helper through Playwright's image-free path via sharp if installed is not guaranteed.
    # Instead rely on Python Pillow only if available; otherwise emit a clear failure.
    try:
        from PIL import Image
    except Exception:
        raise RuntimeError('Pillow is not installed. Install pillow or crop externally after rendering the page image.')
    img = Image.open(image)
    cropped = img.crop((x, y, x + w, y + h))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    cropped.save(out)
    print(out)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd', required=True)

    p1 = sub.add_parser('text')
    p1.add_argument('--pdf', required=True)
    p1.add_argument('--out', required=True)

    p2 = sub.add_parser('page-shot')
    p2.add_argument('--pdf', required=True)
    p2.add_argument('--page', type=int, default=1)
    p2.add_argument('--out', required=True)

    p3 = sub.add_parser('page-crop')
    p3.add_argument('--image', required=True)
    p3.add_argument('--x', type=int, required=True)
    p3.add_argument('--y', type=int, required=True)
    p3.add_argument('--w', type=int, required=True)
    p3.add_argument('--h', type=int, required=True)
    p3.add_argument('--out', required=True)

    args = parser.parse_args()

    if args.cmd == 'text':
        extract_text(args.pdf, args.out)
    elif args.cmd == 'page-shot':
        render_page_shot(args.pdf, args.page, args.out)
    elif args.cmd == 'page-crop':
        crop_image(args.image, args.x, args.y, args.w, args.h, args.out)


if __name__ == '__main__':
    main()
