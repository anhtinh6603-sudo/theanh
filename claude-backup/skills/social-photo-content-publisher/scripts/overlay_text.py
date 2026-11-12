from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def load_font(path: str | None, size: int) -> ImageFont.FreeTypeFont:
    candidates = [path, r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    raise FileNotFoundError("Truyền --font với đường dẫn font TTF hỗ trợ tiếng Việt.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chèn text lên ảnh thật mà không tái tạo ảnh bằng AI.")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--line", action="append", required=True)
    parser.add_argument("--subline")
    parser.add_argument("--font")
    parser.add_argument("--top", type=float, default=0.065)
    parser.add_argument("--size", type=float, default=0.029)
    parser.add_argument("--color", default="#262626")
    parser.add_argument("--arrows", action="store_true")
    args = parser.parse_args()

    source = Image.open(args.input).convert("RGBA")
    layer = Image.new("RGBA", source.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    width, height = source.size
    main_font = load_font(args.font, max(14, int(width * args.size)))
    sub_font = load_font(args.font, max(12, int(width * args.size * 0.72)))
    y = int(height * args.top)

    for line in args.line:
        box = draw.textbbox((0, 0), line, font=main_font)
        draw.text(((width - (box[2] - box[0])) / 2, y), line, font=main_font, fill=args.color)
        y += (box[3] - box[1]) + int(width * 0.012)

    if args.subline:
        box = draw.textbbox((0, 0), args.subline, font=sub_font)
        draw.text(((width - (box[2] - box[0])) / 2, y), args.subline, font=sub_font, fill=args.color)
        y += (box[3] - box[1]) + int(width * 0.015)

    if args.arrows:
        arrows = "↓   ↓   ↓"
        box = draw.textbbox((0, 0), arrows, font=main_font)
        draw.text(((width - (box[2] - box[0])) / 2, y), arrows, font=main_font, fill="#528EBE")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    Image.alpha_composite(source, layer).convert("RGB").save(output, quality=96)
    print(output)


if __name__ == "__main__":
    main()
