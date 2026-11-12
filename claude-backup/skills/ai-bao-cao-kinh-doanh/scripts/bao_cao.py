#!/usr/bin/env python3
"""Tổng hợp số liệu bán hàng/quảng cáo theo kênh thành báo cáo (Excel + Markdown + biểu đồ).

Cách dùng:
    python bao_cao.py --input du-lieu.csv --out-dir bao-cao
    python bao_cao.py --input du-lieu.xlsx --out-dir bao-cao --breakeven-roas 2.5 --target-cpa 120000

Cột dữ liệu (tên tiếng Việt hoặc tiếng Anh đều được, không phân biệt dấu):
    bắt buộc:  kenh (kênh), chi_phi (chi phí quảng cáo), doanh_thu
    nên có:    ngay, don_hang, lead (khách tiềm năng), click, hien_thi
    tùy chọn:  gia_von (tổng giá vốn), khach_moi
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

ALIASES = {
    "date": ["date", "ngay", "thoi_gian", "day"],
    "channel": ["channel", "kenh", "nguon", "source"],
    "spend": ["spend", "cost", "chi_phi", "chi_phi_quang_cao", "ngan_sach_da_tieu"],
    "impressions": ["impressions", "impr", "hien_thi", "luot_hien_thi"],
    "clicks": ["clicks", "click", "luot_click", "luot_nhap"],
    "leads": ["leads", "lead", "khach_tiem_nang", "tin_nhan", "so_dien_thoai"],
    "orders": ["orders", "order", "don_hang", "don", "so_don"],
    "revenue": ["revenue", "doanh_thu", "doanh_so", "sales"],
    "cogs": ["cogs", "gia_von", "chi_phi_gia_von"],
    "new_customers": ["new_customers", "khach_moi", "khach_hang_moi"],
}
NUMERIC = ["spend", "impressions", "clicks", "leads", "orders", "revenue", "cogs", "new_customers"]
VN_LABELS = {"date": "Ngày", "channel": "Kênh", "spend": "Chi phí", "impressions": "Hiển thị", "clicks": "Click",
             "leads": "Lead", "orders": "Đơn", "revenue": "Doanh thu", "cogs": "Giá vốn", "new_customers": "Khách mới"}


def norm(name):
    text = unicodedata.normalize("NFKD", str(name).replace("đ", "d").replace("Đ", "D"))
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).lower()
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def to_number(value):
    """Đọc số kiểu Việt/Anh: 1.500.000 | 1,500,000 | 1.500,5 | '1.500.000đ'."""
    if pd.isna(value):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    s = re.sub(r"[^\d,.\-]", "", str(value))
    if not s:
        return 0.0
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", s):
        s = s.replace(",", "")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def load(path):
    p = Path(path)
    df = pd.read_excel(p) if p.suffix.lower() in (".xlsx", ".xlsm", ".xls") else pd.read_csv(p, encoding="utf-8-sig", dtype=str)
    mapping = {}
    normalized = {norm(c): c for c in df.columns}
    for key, names in ALIASES.items():
        for n in names:
            if n in normalized:
                mapping[key] = normalized[n]
                break
    missing = [k for k in ("channel", "spend", "revenue") if k not in mapping]
    if missing:
        sys.exit("Thiếu cột bắt buộc: " + ", ".join(missing) +
                 f". Các cột đang có: {list(df.columns)}. Cần ít nhất: kênh, chi phí, doanh thu.")
    out = pd.DataFrame({k: df[v] for k, v in mapping.items()})
    for col in NUMERIC:
        out[col] = out[col].map(to_number) if col in out else 0.0
    if "date" in out:
        out["date"] = pd.to_datetime(out["date"], errors="coerce", dayfirst=True)
    out["channel"] = out["channel"].astype(str).str.strip()
    return out, set(mapping)


def kpis(g):
    """Tính các chỉ số từ các tổng; chia cho 0 thì để trống (None) thay vì bịa số."""
    def div(a, b):
        return None if not b else a / b
    return {
        "spend": g["spend"], "revenue": g["revenue"], "orders": g["orders"], "leads": g["leads"],
        "clicks": g["clicks"], "impressions": g["impressions"],
        "ctr": div(g["clicks"], g["impressions"]), "cpc": div(g["spend"], g["clicks"]) if g["spend"] else None,
        "cpl": div(g["spend"], g["leads"]) if g["spend"] else None, "cpa": div(g["spend"], g["orders"]) if g["spend"] else None,
        "roas": div(g["revenue"], g["spend"]), "aov": div(g["revenue"], g["orders"]),
        "close_rate": div(g["orders"], g["leads"]),
        "profit": (g["revenue"] - g["cogs"] - g["spend"]) if g["cogs"] else None,
    }


def money(x):
    return "-" if x is None else f"{x:,.0f}".replace(",", ".")


def pct(x):
    return "-" if x is None else f"{x * 100:.1f}%".replace(".", ",")


def roas_fmt(x):
    return "-" if x is None else f"{x:.2f}x".replace(".", ",")


def write_excel(df, has, channels, path, title):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter as L

    wb = Workbook()
    ws = wb.active
    ws.title = "Du_lieu"
    cols = ["date", "channel", "spend", "impressions", "clicks", "leads", "orders", "revenue", "cogs", "new_customers"]
    head_fill = PatternFill("solid", fgColor="1F3864")
    for i, c in enumerate(cols, 1):
        cell = ws.cell(1, i, VN_LABELS[c])
        cell.font, cell.fill = Font(name="Arial", bold=True, color="FFFFFF"), head_fill
    for r, (_, row) in enumerate(df.iterrows(), 2):
        for i, c in enumerate(cols, 1):
            v = row[c] if c in df else None
            if c == "date":
                v = None if pd.isna(v) else v.to_pydatetime()
            cell = ws.cell(r, i, v)
            cell.font = Font(name="Arial", color="0000FF")  # ô nhập liệu: chữ xanh
            if c == "date":
                cell.number_format = "dd/mm/yyyy"
            elif c not in ("channel",):
                cell.number_format = "#,##0"
    last = len(df) + 1
    for i, w in enumerate([12, 20, 14, 12, 10, 10, 10, 16, 14, 12], 1):
        ws.column_dimensions[L(i)].width = w
    ws.freeze_panes = "A2"

    def rng(col_letter):
        return f"Du_lieu!${col_letter}$2:${col_letter}${last}"

    S, K = wb.create_sheet("Tong_hop_kenh"), None
    ws2 = S
    ws2["A1"] = title
    ws2["A1"].font = Font(name="Arial", bold=True, size=14)
    headers = ["Kênh", "Chi phí", "Doanh thu", "Đơn", "Lead", "Click", "Hiển thị", "CTR", "CPC", "CPL",
               "CPA (chi phí/đơn)", "ROAS", "Giá trị đơn TB", "Tỷ lệ chốt (đơn/lead)"]
    with_profit = "cogs" in has
    if with_profit:
        headers.append("Lợi nhuận sau QC")
    for i, h in enumerate(headers, 1):
        cell = ws2.cell(3, i, h)
        cell.font, cell.fill = Font(name="Arial", bold=True, color="FFFFFF"), head_fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws2.row_dimensions[3].height = 32
    src = {"B": "C", "C": "H", "D": "G", "E": "F", "F": "E", "G": "D"}  # cột Tong_hop -> cột Du_lieu
    first = 4
    for r, ch in enumerate(channels, first):
        ws2.cell(r, 1, ch).font = Font(name="Arial")
        for tcol, scol in src.items():
            ws2[f"{tcol}{r}"] = f"=SUMIFS({rng(scol)},{rng('B')},$A{r})"
        ws2[f"H{r}"] = f"=IFERROR(F{r}/G{r},0)"
        ws2[f"I{r}"] = f"=IFERROR(B{r}/F{r},0)"
        ws2[f"J{r}"] = f"=IFERROR(B{r}/E{r},0)"
        ws2[f"K{r}"] = f"=IFERROR(B{r}/D{r},0)"
        ws2[f"L{r}"] = f"=IFERROR(C{r}/B{r},0)"
        ws2[f"M{r}"] = f"=IFERROR(C{r}/D{r},0)"
        ws2[f"N{r}"] = f"=IFERROR(D{r}/E{r},0)"
        if with_profit:
            ws2[f"O{r}"] = f"=C{r}-SUMIFS({rng('I')},{rng('B')},$A{r})-B{r}"
    tot = first + len(channels)
    ws2.cell(tot, 1, "TỔNG").font = Font(name="Arial", bold=True)
    for col in "BCDEFG":
        ws2[f"{col}{tot}"] = f"=SUM({col}{first}:{col}{tot - 1})"
    ws2[f"H{tot}"] = f"=IFERROR(F{tot}/G{tot},0)"
    ws2[f"I{tot}"] = f"=IFERROR(B{tot}/F{tot},0)"
    ws2[f"J{tot}"] = f"=IFERROR(B{tot}/E{tot},0)"
    ws2[f"K{tot}"] = f"=IFERROR(B{tot}/D{tot},0)"
    ws2[f"L{tot}"] = f"=IFERROR(C{tot}/B{tot},0)"
    ws2[f"M{tot}"] = f"=IFERROR(C{tot}/D{tot},0)"
    ws2[f"N{tot}"] = f"=IFERROR(D{tot}/E{tot},0)"
    if with_profit:
        ws2[f"O{tot}"] = f"=SUM(O{first}:O{tot - 1})"
    for r in range(first, tot + 1):
        for i in range(2, len(headers) + 1):
            c = ws2.cell(r, i)
            c.font = Font(name="Arial", bold=(r == tot))
            letter = L(i)
            c.number_format = "0.0%" if letter in ("H", "N") else ('0.00"x"' if letter == "L" else "#,##0")
    ws2.column_dimensions["A"].width = 22
    for i in range(2, len(headers) + 1):
        ws2.column_dimensions[L(i)].width = 15
    ws2.freeze_panes = "B4"

    notes = wb.create_sheet("Ghi_chu")
    lines = [
        "Cách đọc file này",
        "- Sheet Du_lieu: số liệu đầu vào (chữ xanh = ô nhập). Thêm/sửa dòng rồi cập nhật lại các công thức nếu thêm kênh mới.",
        "- Sheet Tong_hop_kenh: tính bằng công thức từ Du_lieu, đổi số liệu là tự tính lại.",
        "- ROAS = Doanh thu / Chi phí quảng cáo. CPA = Chi phí / Đơn. CPL = Chi phí / Lead. CTR = Click / Hiển thị.",
        "- Ô chia cho 0 hiển thị 0 (nghĩa là chưa có dữ liệu để chia), không phải kết quả thật bằng 0.",
        "- Lợi nhuận sau QC (nếu có) = Doanh thu - Giá vốn - Chi phí quảng cáo; chưa gồm lương, thuê mặt bằng, thuế, phí sàn.",
        "Lưu ý về dữ liệu",
        "- Mỗi nền tảng quảng cáo tự ghi nhận đơn của mình nên tổng đơn các kênh có thể trùng nhau; ưu tiên số đơn thật từ hệ thống bán hàng.",
        "- Kỳ báo cáo ngắn hoặc ít đơn thì các tỷ lệ dao động mạnh, đừng kết luận vội.",
    ]
    for i, t in enumerate(lines, 1):
        notes.cell(i, 1, t).font = Font(name="Arial", bold=t in ("Cách đọc file này", "Lưu ý về dữ liệu"))
    notes.column_dimensions["A"].width = 120
    wb.save(path)


def write_chart(agg, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = list(agg.index)
    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(names))
    ax.bar([i - 0.2 for i in x], agg["spend"] / 1e6, width=0.4, label="Chi phí (triệu đ)", color="#94A3B8")
    ax.bar([i + 0.2 for i in x], agg["revenue"] / 1e6, width=0.4, label="Doanh thu (triệu đ)", color="#2563EB")
    for i, n in enumerate(names):
        s, r = agg.loc[n, "spend"], agg.loc[n, "revenue"]
        ax.text(i + 0.2, r / 1e6, f"ROAS {r / s:.1f}x" if s else "", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(names)
    ax.set_ylabel("Triệu đồng")
    ax.set_title("Chi phí và doanh thu theo kênh")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description="Báo cáo hiệu quả kinh doanh theo kênh")
    ap.add_argument("--input", required=True)
    ap.add_argument("--out-dir", default="bao-cao")
    ap.add_argument("--title", default="Báo cáo hiệu quả theo kênh")
    ap.add_argument("--breakeven-roas", type=float, help="ROAS hòa vốn của bạn (để cảnh báo kênh lỗ)")
    ap.add_argument("--target-cpa", type=float, help="CPA mục tiêu (để cảnh báo kênh vượt)")
    ap.add_argument("--compare-days", type=int, default=7, help="So sánh N ngày gần nhất với N ngày trước đó")
    a = ap.parse_args()

    df, has = load(a.input)
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    agg = df.groupby("channel")[NUMERIC].sum().sort_values("revenue", ascending=False)
    total = agg.sum()
    rows = {ch: kpis(agg.loc[ch]) for ch in agg.index}
    tk = kpis(total)

    xlsx_path = out / "bao-cao-hieu-qua.xlsx"
    write_excel(df, has, list(agg.index), xlsx_path, a.title)
    chart_path = out / "bieu-do-theo-kenh.png"
    write_chart(agg, chart_path)

    md = [f"# {a.title}", ""]
    if "date" in has and df["date"].notna().any():
        md.append(f"Kỳ dữ liệu: {df['date'].min():%d/%m/%Y} - {df['date'].max():%d/%m/%Y}  ")
    md += [f"Số dòng dữ liệu: {len(df)}", "", "## Tổng quan", "",
           f"- Chi phí quảng cáo: **{money(tk['spend'])} đ**",
           f"- Doanh thu: **{money(tk['revenue'])} đ**",
           f"- ROAS chung: **{roas_fmt(tk['roas'])}**",
           f"- Đơn hàng: **{money(tk['orders'])}**" + (f" | CPA chung: **{money(tk['cpa'])} đ**" if tk['cpa'] else ""),
           f"- Lead: **{money(tk['leads'])}**" + (f" | CPL chung: **{money(tk['cpl'])} đ**" if tk['cpl'] else "")]
    if tk["profit"] is not None:
        md.append(f"- Lợi nhuận sau quảng cáo (doanh thu - giá vốn - chi phí QC): **{money(tk['profit'])} đ**")
    md += ["", "## Theo kênh (xếp theo doanh thu)", "",
           "| Kênh | Chi phí | Doanh thu | Đơn | CPA | ROAS | Tỷ lệ chốt |", "|---|---:|---:|---:|---:|---:|---:|"]
    for ch, k in rows.items():
        md.append(f"| {ch} | {money(k['spend'])} | {money(k['revenue'])} | {money(k['orders'])} | "
                  f"{money(k['cpa'])} | {roas_fmt(k['roas'])} | {pct(k['close_rate'])} |")

    flags = []
    for ch, k in rows.items():
        if k["spend"] > 0 and k["orders"] == 0 and k["revenue"] == 0:
            flags.append(f"**{ch}**: đã chi {money(k['spend'])} đ nhưng chưa ghi nhận đơn/doanh thu. Kiểm tra theo dõi chuyển đổi trước khi kết luận kênh kém.")
        if a.breakeven_roas and k["roas"] is not None and k["spend"] > 0 and k["roas"] < a.breakeven_roas:
            flags.append(f"**{ch}**: ROAS {roas_fmt(k['roas'])} thấp hơn ROAS hòa vốn {roas_fmt(a.breakeven_roas)}, đang lỗ trên chi phí quảng cáo.")
        if a.target_cpa and k["cpa"] is not None and k["cpa"] > a.target_cpa:
            flags.append(f"**{ch}**: CPA {money(k['cpa'])} đ cao hơn CPA mục tiêu {money(a.target_cpa)} đ.")
    md += ["", "## Điểm cần chú ý", ""] + ([f"- {f}" for f in flags] if flags else
          ["- Không có cảnh báo theo ngưỡng đã đặt" + ("" if (a.breakeven_roas or a.target_cpa) else
           " (bạn chưa đặt ROAS hòa vốn / CPA mục tiêu: hãy đặt để báo cáo cảnh báo chính xác hơn)") + "."])

    if "date" in has and df["date"].notna().any() and a.compare_days > 0:
        end = df["date"].max()
        cur = df[df["date"] > end - pd.Timedelta(days=a.compare_days)]
        prev = df[(df["date"] <= end - pd.Timedelta(days=a.compare_days)) &
                  (df["date"] > end - pd.Timedelta(days=2 * a.compare_days))]
        if len(prev):
            kc, kp = kpis(cur[NUMERIC].sum()), kpis(prev[NUMERIC].sum())
            def delta(c, p):
                return "-" if not p else f"{(c - p) / p * 100:+.0f}%".replace(".", ",")
            md += ["", f"## So sánh {a.compare_days} ngày gần nhất với {a.compare_days} ngày trước đó", "",
                   "| Chỉ số | Trước | Gần nhất | Thay đổi |", "|---|---:|---:|---:|",
                   f"| Chi phí | {money(kp['spend'])} | {money(kc['spend'])} | {delta(kc['spend'], kp['spend'])} |",
                   f"| Doanh thu | {money(kp['revenue'])} | {money(kc['revenue'])} | {delta(kc['revenue'], kp['revenue'])} |",
                   f"| ROAS | {roas_fmt(kp['roas'])} | {roas_fmt(kc['roas'])} | "
                   f"{delta(kc['roas'], kp['roas']) if kc['roas'] and kp['roas'] else '-'} |"]

    missing = [VN_LABELS[c] for c in ("orders", "leads", "clicks", "impressions", "cogs") if c not in has]
    md += ["", "## Lưu ý về dữ liệu", "",
           "- Mỗi nền tảng quảng cáo tự ghi nhận đơn nên tổng đơn các kênh có thể trùng nhau; hãy đối chiếu với số đơn thật của hệ thống bán hàng.",
           "- Số liệu kỳ ngắn hoặc ít đơn thì tỷ lệ dao động mạnh, chưa nên kết luận chắc chắn.",
           "- Báo cáo này chỉ phản ánh dữ liệu bạn cung cấp, không tự lấy số từ nền tảng quảng cáo."]
    if missing:
        md.append("- Chưa có cột: " + ", ".join(missing) + " nên các chỉ số liên quan bị bỏ trống.")
    (out / "tom-tat.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(json.dumps({"excel": str(xlsx_path), "tom_tat": str(out / "tom-tat.md"), "bieu_do": str(chart_path),
                      "kenh": list(agg.index), "roas_chung": tk["roas"], "canh_bao": len(flags)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
