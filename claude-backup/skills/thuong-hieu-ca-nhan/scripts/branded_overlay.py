#!/usr/bin/env python3
"""Create a 4:5 social image with a headline and optional brand badge."""
import argparse
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CANVAS = (1080, 1350)

def get_font(size):
    choices = [Path(__file__).parents[1] / "assets/fonts/Lato-Black.ttf", Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")]
    for path in choices:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()

def cover(image):
    scale = max(CANVAS[0] / image.width, CANVAS[1] / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left, top = (image.width - CANVAS[0]) // 2, (image.height - CANVAS[1]) // 2
    return image.crop((left, top, left + CANVAS[0], top + CANVAS[1])).convert("RGBA")

def parse(value):
    pieces = re.split(r"(\*\*.*?\*\*)", value)
    marked = [p for p in pieces if p.startswith("**") and p.endswith("**")]
    if len(marked) > 1:
        raise ValueError("Headline may contain only one **highlighted phrase**")
    return [(p[2:-2], True) if p.startswith("**") and p.endswith("**") else (p, False) for p in pieces if p]

def wrap(draw, parts, face, max_width):
    tokens = [(t, mark) for text, mark in parts for t in re.findall(r"\S+\s*", text)]
    lines, line, width = [], [], 0
    for token, mark in tokens:
        token_width = draw.textlength(token, font=face)
        if line and width + token_width > max_width:
            lines.append(line); line, width = [], 0
        line.append((token, mark)); width += token_width
    if line: lines.append(line)
    return lines

def render(photo, headline, output, badge, accent):
    base = cover(Image.open(photo).convert("RGB"))
    shade = Image.new("RGBA", CANVAS, (0, 0, 0, 0)); px = shade.load()
    for y in range(650, CANVAS[1]):
        alpha = int(210 * ((y - 650) / 700) ** 1.25)
        for x in range(CANVAS[0]): px[x, y] = (0, 0, 0, alpha)
    base = Image.alpha_composite(base, shade); draw = ImageDraw.Draw(base)
    parts, size = parse(headline), 86
    while size >= 54:
        face = get_font(size); lines = wrap(draw, parts, face, 920)
        if len(lines) <= 3: break
        size -= 4
    line_height = int(size * 1.18); bottom = 1180 if badge else 1260; y = bottom - len(lines) * line_height
    for line in lines:
        total = sum(draw.textlength(t, font=face) for t, _ in line); x = (CANVAS[0] - total) / 2
        for text, marked in line:
            draw.text((x + 2, y + 3), text, font=face, fill=(0, 0, 0, 150)); draw.text((x, y), text, font=face, fill=accent if marked else "white"); x += draw.textlength(text, font=face)
        y += line_height
    if badge:
        badge_face = get_font(34); bbox = draw.textbbox((0, 0), badge, font=badge_face); w, h = bbox[2] - bbox[0] + 54, bbox[3] - bbox[1] + 30
        x, y = CANVAS[0] - w - 46, CANVAS[1] - h - 42
        draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill="white"); draw.text((x + 27, y + 12 - bbox[1]), badge, font=badge_face, fill="#171717")
    destination = Path(output); destination.parent.mkdir(parents=True, exist_ok=True); base.convert("RGB").save(destination, quality=95, subsampling=0)

def main():
    p = argparse.ArgumentParser(); p.add_argument("--photo", required=True); p.add_argument("--headline", required=True); p.add_argument("--output", required=True); p.add_argument("--badge"); p.add_argument("--accent", default="#FF5C8A"); a = p.parse_args()
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", a.accent): p.error("--accent must be a six-digit hex color such as #FF5C8A")
    render(a.photo, a.headline, a.output, a.badge, a.accent)

if __name__ == "__main__": main()
