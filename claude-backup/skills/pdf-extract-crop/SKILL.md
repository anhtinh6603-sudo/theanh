---
name: pdf-extract-crop
description: Extract text, screenshots, page images, and targeted regions from PDF files. Use when reading PDF catalogs, pulling structured text from PDFs, cropping a specific table or model block, rendering PDF pages to images, or preparing PDF snippets for chat delivery.
---

# PDF Extract Crop

Work with PDF files in a practical way: text first, page images second, targeted crops third.

## Workflow

1. Read `references/usage.md` before first use.
2. Use `scripts/pdf_tools.py text` to extract readable text from a PDF.
3. Use `scripts/pdf_tools.py page-shot` to open the PDF in a browser viewer, jump to the requested page, and screenshot that page.
4. Use `scripts/pdf_tools.py page-crop` to crop a specific rectangle from a rendered page image.
5. Save outputs to `/tmp/pdf-extract-crop/` or a user-specified output path.

## Commands

Extract text:

```bash
python3 skills/pdf-extract-crop/scripts/pdf_tools.py text --pdf /path/file.pdf --out /tmp/out.txt
```

Render a page screenshot:

```bash
python3 skills/pdf-extract-crop/scripts/pdf_tools.py page-shot --pdf /path/file.pdf --page 1 --out /tmp/page1.png
```

Crop a region from a rendered page image:

```bash
python3 skills/pdf-extract-crop/scripts/pdf_tools.py page-crop --image /tmp/page1.png --x 100 --y 300 --w 1200 --h 400 --out /tmp/crop.png
```

## Notes

- If precise PDF parsing libraries are missing, the script falls back to browser-based rendering.
- For hard crops, first create a full page image, then crop from that image.
- Prefer a reproducible crop rectangle over manual guessing.
