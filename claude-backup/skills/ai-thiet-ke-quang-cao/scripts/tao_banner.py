#!/usr/bin/env python3
"""Tạo ảnh banner/poster/thumbnail có chữ tiếng Việt từ một file mô tả JSON (dùng Pillow).

Cách dùng:
    python tao_banner.py --spec mo-ta.json
    python tao_banner.py --spec mo-ta.json --out anh.png

Xem assets/mau-mo-ta.json để biết các trường. Chỉ trường "preset" và "title" là bắt buộc.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# Kích thước (rộng, cao) và vùng an toàn phía trên/dưới (tỷ lệ chiều cao) để tránh bị giao diện che.
PRESETS = {
    "fb_post":      {"size": (1080, 1080), "safe_top": 0.06, "safe_bottom": 0.06},
    "fb_post_4x5":  {"size": (1080, 1350), "safe_top": 0.06, "safe_bottom": 0.06},
    "fb_story":     {"size": (1080, 1920), "safe_top": 0.13, "safe_bottom": 0.20},
    "yt_thumbnail": {"size": (1280, 720),  "safe_top": 0.06, "safe_bottom": 0.10, "title_scale": 1.5},
    "fb_cover":     {"size": (1640, 624),  "safe_top": 0.10, "safe_bottom": 0.10},
    "banner_web":   {"size": (1920, 600),  "safe_top": 0.08, "safe_bottom": 0.08},
    "poster_a4":    {"size": (2480, 3508), "safe_top": 0.05, "safe_bottom": 0.05},
}

FONT_BOLD_CANDIDATES = [
    "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_REGULAR_CANDIDATES = [
    "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
VI_TEST = "Ưu đãi Hà Nội Đà Nẵng ắằẳẵặ ếềểễệ ốồổỗộ ớờởỡợ ứừửữự"


def find_font(explicit, candidates):
    for path in ([explicit] if explicit else []) + candidates:
        if path and os.path.exists(path):
            return path
    sys.exit("Không tìm thấy font hỗ trợ tiếng Việt. Hãy đặt đường dẫn file .ttf vào trường "
             '"font" / "font_bold" trong file mô tả (ví dụ Arial, Be Vietnam Pro, Noto Sans).')


def hex_to_rgb(value):
    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Màu không hợp lệ: #{value} (cần dạng #RRGGBB)")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast_ratio(rgb1, rgb2):
    l1, l2 = luminance(rgb1), luminance(rgb2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def make_background(spec_bg, size):
    w, h = size
    bg = spec_bg or {}
    if bg.get("image"):
        img = Image.open(bg["image"]).convert("RGB")
        scale = max(w / img.width, h / img.height)  # phủ kín khung, không kéo méo
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
        left, top = (img.width - w) // 2, (img.height - h) // 2
        img = img.crop((left, top, left + w, top + h))
    else:
        c1 = hex_to_rgb(bg.get("color", "#0F172A"))
        c2 = hex_to_rgb(bg.get("gradient_to", bg.get("color", "#0F172A")))
        img = Image.new("RGB", size, c1)
        if c1 != c2:
            px = Image.new("RGB", (1, h))
            for y in range(h):
                t = y / max(h - 1, 1)
                px.putpixel((0, y), tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
            img = px.resize((w, h))
    overlay = float(bg.get("overlay", 0.45 if bg.get("image") else 0.0))
    if overlay > 0:
        black = Image.new("RGB", size, (0, 0, 0))
        img = Image.blend(img, black, min(max(overlay, 0), 0.9))
    return img


def wrap(draw, text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        words, line = paragraph.split(), ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=font) <= max_width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def balance(draw, text, font, max_width):
    """Chia chữ thành cùng số dòng nhưng đều nhau hơn, tránh dòng cuối chỉ có một từ."""
    lines = wrap(draw, text, font, max_width)
    n = len(lines)
    if n < 2 or "\n" in text:
        return lines
    lo, hi, best = max(int(draw.textlength(w, font=font)) for w in text.split()), int(max_width), lines
    while lo <= hi:
        mid = (lo + hi) // 2
        trial = wrap(draw, text, font, mid)
        if len(trial) <= n:
            best, hi = trial, mid - 1
        else:
            lo = mid + 1
    return best


def fit_text(draw, text, font_path, max_width, max_height, max_size, min_size, max_lines):
    size = max_size
    while size >= min_size:
        font = ImageFont.truetype(font_path, size)
        lines = balance(draw, text, font, max_width)
        line_h = round(size * 1.22)
        widest = max(draw.textlength(l, font=font) for l in lines)
        if len(lines) <= max_lines and len(lines) * line_h <= max_height and widest <= max_width:
            return font, lines, line_h, False
        size -= 4
    font = ImageFont.truetype(font_path, min_size)
    lines = wrap(draw, text, font, max_width)[:max_lines]
    return font, lines, round(min_size * 1.22), True


def pill(draw, xy, fill, radius=None):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius or (y1 - y0) // 2, fill=fill)


def build(spec, out_path):
    preset = PRESETS.get(spec.get("preset", ""))
    if not preset:
        sys.exit(f'Preset không có: {spec.get("preset")}. Chọn một trong: {", ".join(PRESETS)}')
    if not spec.get("title"):
        sys.exit('Thiếu trường "title".')
    size = preset["size"]
    w, h = size
    warnings = []

    colors = {"text": "#FFFFFF", "accent": "#FACC15", "accent_text": "#111827",
              "cta_bg": "#EF4444", "cta_text": "#FFFFFF"}
    colors.update(spec.get("colors", {}))
    c = {k: hex_to_rgb(v) for k, v in colors.items()}

    font_bold = find_font(spec.get("font_bold"), FONT_BOLD_CANDIDATES)
    font_reg = find_font(spec.get("font"), FONT_REGULAR_CANDIDATES)
    for path in (font_bold, font_reg):  # kiểm tra font vẽ được chữ Việt (không ra ô vuông)
        f = ImageFont.truetype(path, 40)
        if f.getmask("ệ").getbbox() is None or f.getmask("Ư").getbbox() is None:
            warnings.append(f"Font {os.path.basename(path)} có thể thiếu ký tự tiếng Việt")

    img = make_background(spec.get("background"), size)
    draw = ImageDraw.Draw(img)

    margin = round(min(w, h) * 0.08)
    top = round(h * preset["safe_top"]) + (margin // 2)
    bottom = h - round(h * preset["safe_bottom"]) - (margin // 2)
    align = spec.get("align", "left")
    box_w = w - 2 * margin
    base = min(w, h)

    # --- chuẩn bị từng khối (khối cố định trước, chữ dài chia phần chỗ còn lại) ---
    gap = round(base * 0.035)
    badge = cta = footer_font = None
    if spec.get("badge"):
        bf = ImageFont.truetype(font_bold, round(base * 0.045))
        pad_x, pad_y = round(base * 0.03), round(base * 0.016)
        badge = ("badge", spec["badge"], bf, draw.textlength(spec["badge"], font=bf) + 2 * pad_x,
                 round(base * 0.045) + 2 * pad_y, pad_x, pad_y)
    if spec.get("cta"):
        cf = ImageFont.truetype(font_bold, round(base * 0.048))
        pad_x, pad_y = round(base * 0.05), round(base * 0.024)
        cta = ("cta", spec["cta"], cf, draw.textlength(spec["cta"], font=cf) + 2 * pad_x,
               round(base * 0.048) + 2 * pad_y, pad_x, pad_y)
    footer_h = 0
    if spec.get("footer"):
        footer_font = ImageFont.truetype(font_reg, round(base * 0.032))
        footer_h = round(base * 0.032) + gap

    n_blocks = 1 + (1 if spec.get("subtitle") else 0) + (1 if badge else 0) + (1 if cta else 0)
    fixed = sum(b[4] for b in (badge, cta) if b) + gap * (n_blocks - 1)
    remaining = (bottom - footer_h - top) - fixed
    if remaining < round(base * 0.12):
        warnings.append("Quá nhiều thành phần cho khung này: hãy bớt badge/phụ đề/nút hoặc chọn khung lớn hơn")
        remaining = max(remaining, round(base * 0.12))

    title_budget = round(remaining * (0.66 if spec.get("subtitle") else 1.0))
    tfont, tlines, tlh, tshrunk = fit_text(draw, spec["title"], font_bold, box_w, title_budget,
                                           round(base * 0.10 * preset.get("title_scale", 1.0)), round(base * 0.045), 3)
    if tshrunk:
        warnings.append("Tiêu đề quá dài, đã thu về cỡ chữ nhỏ nhất và bị cắt bớt: hãy rút gọn tiêu đề")
    title_block = ("title", tlines, tfont, box_w, len(tlines) * tlh, tlh)

    sub_block = None
    if spec.get("subtitle"):
        sub_budget = remaining - title_block[4]
        sfont, slines, slh, sshrunk = fit_text(draw, spec["subtitle"], font_reg, box_w, max(sub_budget, 1),
                                               round(base * 0.052), round(base * 0.03), 3)
        if sshrunk:
            warnings.append("Phụ đề quá dài, đã bị cắt bớt: hãy rút gọn")
        sub_block = ("subtitle", slines, sfont, box_w, len(slines) * slh, slh)

    blocks = [b for b in (badge, title_block, sub_block, cta) if b]
    total_h = sum(b[4] for b in blocks) + gap * (len(blocks) - 1)
    avail_bottom = bottom - footer_h
    y = top + max(0, (avail_bottom - top - total_h) // 2)

    # Đo độ tương phản nền tại vùng chữ (lấy trước khi vẽ chữ)
    region = img.crop((margin, max(y, 0), w - margin, min(max(y + total_h, y + 1), h))).resize((1, 1), Image.BOX)
    bg_avg = region.getpixel((0, 0))
    ratio = contrast_ratio(c["text"], bg_avg)
    if ratio < 4.5:
        warnings.append(f"Độ tương phản chữ/nền thấp ({ratio:.1f}:1, nên từ 4.5:1): tăng overlay hoặc đổi màu chữ")

    # --- vẽ ---
    def x_for(width):
        return margin if align == "left" else (w - width) // 2

    for block in blocks:
        kind = block[0]
        if kind == "badge":
            _, text, font, bw, bh, px, py = block
            x = x_for(bw)
            pill(draw, (x, y, x + bw, y + bh), c["accent"])
            draw.text((x + px, y + py - round(bh * 0.04)), text, font=font, fill=c["accent_text"])
        elif kind in ("title", "subtitle"):
            _, lines, font, bw, bh, lh = block
            fill = c["text"]
            for i, line in enumerate(lines):
                lw = draw.textlength(line, font=font)
                lx = margin if align == "left" else (w - lw) // 2
                draw.text((lx, y + i * lh), line, font=font, fill=fill)
        elif kind == "cta":
            _, text, font, bw, bh, px, py = block
            x = x_for(bw)
            pill(draw, (x, y, x + bw, y + bh), c["cta_bg"])
            draw.text((x + px, y + py - round(bh * 0.04)), text, font=font, fill=c["cta_text"])
        y += block[4] + gap

    if spec.get("footer"):
        fw = draw.textlength(spec["footer"], font=footer_font)
        fx = margin if align == "left" else (w - fw) // 2
        draw.text((fx, bottom - round(base * 0.032)), spec["footer"], font=footer_font, fill=c["text"])

    if spec.get("logo"):
        logo = Image.open(spec["logo"]).convert("RGBA")
        lw = round(w * float(spec.get("logo_width", 0.14)))
        logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
        pos_right = spec.get("logo_pos", "top_left") == "top_right"
        lx = w - margin - logo.width if pos_right else margin
        ly = round(h * preset["safe_top"]) + margin // 3
        img.paste(logo, (lx, ly), logo)

    out_path = out_path or spec.get("out", "banner.png")
    save_kwargs = {"quality": 95} if out_path.lower().endswith((".jpg", ".jpeg")) else {}
    img.save(out_path, **save_kwargs)
    return {"file": os.path.abspath(out_path), "size": f"{w}x{h}", "preset": spec["preset"],
            "font_bold": os.path.basename(font_bold), "font_regular": os.path.basename(font_reg),
            "contrast_ratio": round(ratio, 1), "warnings": warnings}


def main():
    p = argparse.ArgumentParser(description="Tạo banner/poster/thumbnail có chữ tiếng Việt")
    p.add_argument("--spec", required=True, help="File JSON mô tả (xem assets/mau-mo-ta.json)")
    p.add_argument("--out", help="Đường dẫn ảnh đầu ra (mặc định lấy trong JSON hoặc banner.png)")
    args = p.parse_args()
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    result = build(spec, args.out)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
