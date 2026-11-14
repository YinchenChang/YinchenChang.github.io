"""Charts for the 2026-11-14 essay (Chinese and English versions).

Writes inline SVG files to _includes/charts/2026-11-14/<name>-<lang>.svg; the posts
include them with {% include charts/2026-11-14/<name>-<lang>.svg %}.
Each mark carries a <title>, so hovering shows its value. Overseas names only.

Data sources (company-models main, 2026-11-08 to 2026-11-14):
  - CoreWeave: coreweave/docs/reports/20261112_coreweave_v5.0_Oracle樣板重建與Q3.md
    (five-step target bridge; FY2026-FY2030 free cash flow by scenario) and README v5.0.1
  - Oracle: oracle/docs/reports/20261110_oracle_v0.5.0_收支模組.md (reverse DCF, stress table)
  - Anthropic: anthropic/docs/reports/20261111_v0.2.0.md (valuation page) and
    20261111_Prospectus原文摘錄.md (price range)
  - Supermicro: smci/docs/reports/20261110_smci_v0.3.6_稀釋股數.md
  - Meta: meta/docs/reports/20261111_meta_v0.2.0_驗收採用.md (section 2 bridge)

Run: python3 tools/charts_20261114.py
"""
import html
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "_includes/charts/2026-11-14"

INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#c43b3a"
FONT = 'font-family="system-ui,-apple-system,Segoe UI,sans-serif"'


def esc(s):
    return html.escape(str(s), quote=True)


def svg(w, h, body, label):
    return (f'<figure class="chart"><svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(label)}" '
            f'{FONT} style="max-width:{w}px;height:auto">{body}</svg></figure>\n')


def text(x, y, s, size=12, fill=INK2, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>'


def axis(o, sx, ticks, top, bottom, fmt=lambda v: f"{v:g}"):
    for g in ticks:
        o.append(f'<line x1="{sx(g):.1f}" x2="{sx(g):.1f}" y1="{top}" y2="{bottom}" stroke="{GRID}"/>')
        o.append(text(sx(g), bottom + 16, fmt(g), 11, MUTED, "middle"))


def waterfall(rows, lo, hi, ticks, unit, label, l=210, fmt="{:.2f}"):
    """rows: (name, value, kind) kind in start|delta|end."""
    W, r, t, rowh = 680, 70, 14, 36
    H = t + rowh * len(rows) + 50
    sx = lambda v: l + (v - lo) / (hi - lo) * (W - l - r)
    o = []
    axis(o, sx, ticks, t, t + rowh * len(rows))
    run = 0.0
    for i, (name, v, kind) in enumerate(rows):
        y = t + 6 + i * rowh
        if kind in ("start", "end"):
            a, b, col, w8 = max(lo, 0), v, BLUE, 600
            run = v
            lab = fmt.format(v)
        else:
            a, b = run, run + v
            col = AQUA if v >= 0 else ORANGE
            run += v
            w8 = 400
            lab = ("+" if v >= 0 else "−") + fmt.format(abs(v))
        x0, x1 = sorted((sx(a), sx(b)))
        o.append(text(l - 10, y + 17, name, 12, INK if kind != "delta" else INK2, "end", w8))
        o.append(f'<rect x="{x0:.1f}" y="{y}" width="{max(x1 - x0, 2):.1f}" height="24" rx="3" fill="{col}"><title>{esc(name)}: {esc(lab)}</title></rect>')
        o.append(text(x1 + 6, y + 17, lab, 12, INK, "start", w8))
    o.append(text(l, H - 8, unit, 11.5, MUTED))
    return svg(W, H, "".join(o), label)


def hbars(rows, lo, hi, ticks, unit, label, band=None, l=210, fmt="{:.2f}", zero=0):
    """rows: (name, value, color). band: (a, b, caption) shaded range."""
    W, r, t, rowh = 680, 70, 22 if band else 14, 36
    H = t + rowh * len(rows) + 50
    sx = lambda v: l + (v - lo) / (hi - lo) * (W - l - r)
    o = []
    axis(o, sx, ticks, t, t + rowh * len(rows))
    if band:
        a, b, cap = band
        o.append(f'<rect x="{sx(a):.1f}" y="{t}" width="{sx(b) - sx(a):.1f}" height="{rowh * len(rows)}" fill="{YELLOW}" opacity="0.18"/>')
        o.append(text((sx(a) + sx(b)) / 2, t - 6, cap, 11, INK2, "middle", 600))
    for i, (name, v, col) in enumerate(rows):
        y = t + 6 + i * rowh
        x0, x1 = sorted((sx(zero), sx(v)))
        o.append(text(l - 10, y + 17, name, 12, INK2, "end"))
        o.append(f'<rect x="{x0:.1f}" y="{y}" width="{max(x1 - x0, 2):.1f}" height="24" rx="3" fill="{col}"><title>{esc(name)}: {fmt.format(v)}</title></rect>')
        if v >= zero:
            o.append(text(x1 + 6, y + 17, fmt.format(v), 12, INK, "start", 600))
        else:
            o.append(text(x0 - 6, y + 17, fmt.format(v), 12, INK, "end", 600))
    o.append(text(l, H - 8, unit, 11.5, MUTED))
    return svg(W, H, "".join(o), label)


def grouped(cats, series, hi, ticks, unit, label, l=60):
    """Vertical grouped bars. series: (name, color, values)."""
    W, H, r, t, b = 680, 330, 20, 40, 60
    sy = lambda v: t + (hi - v) / hi * (H - t - b)
    o = []
    for g in ticks:
        o.append(f'<line x1="{l}" x2="{W - r}" y1="{sy(g):.1f}" y2="{sy(g):.1f}" stroke="{GRID}"/>')
        o.append(text(l - 6, sy(g) + 4, f"{g:g}", 11, MUTED, "end"))
    gw = (W - l - r) / len(cats)
    bw = gw * 0.7 / len(series)
    for j, (sn, col, vals) in enumerate(series):
        o.append(f'<rect x="{l + j * 190}" y="8" width="12" height="12" rx="2" fill="{col}"/>')
        o.append(text(l + j * 190 + 18, 18, sn, 12, INK2))
        for i, v in enumerate(vals):
            x = l + i * gw + gw * 0.15 + j * bw
            o.append(f'<rect x="{x:.1f}" y="{sy(v):.1f}" width="{bw - 3:.1f}" height="{max(sy(0) - sy(v), 1.5):.1f}" rx="2" fill="{col}"><title>{esc(cats[i])} {esc(sn)}: {v:.1f}</title></rect>')
            o.append(text(x + (bw - 3) / 2, sy(v) - 5, f"{v:.1f}", 11, INK, "middle"))
    for i, c in enumerate(cats):
        o.append(text(l + i * gw + gw / 2, H - b + 18, c, 12, INK2, "middle"))
    o.append(text(l, H - 10, unit, 11.5, MUTED))
    return svg(W, H, "".join(o), label)


def flow(boxes, arrows, label, W=680, H=240):
    """boxes: (x, y, w, h, fill, txtcolor, [lines]) first line bold. arrows: (x1,y1,x2,y2,caption)."""
    o = ['<defs><marker id="ah14" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker></defs>']
    for x, y, w, h, fill, tc, lines in boxes:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{AXIS}"/>')
        y0 = y + h / 2 - (len(lines) - 1) * 8 + 4
        for k, s in enumerate(lines):
            o.append(text(x + w / 2, y0 + k * 16, s, 12.5, tc, "middle", 600 if k == 0 else 400))
    for x1, y1, x2, y2, cap in arrows:
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK2}" stroke-width="1.5" marker-end="url(#ah14)"/>')
        if cap:
            o.append(text((x1 + x2) / 2 + 4, (y1 + y2) / 2 - 6, cap, 11.5, INK2, "middle", 600))
    return svg(W, H, "".join(o), label)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {}
    for L in ("zh", "en"):
        z = L == "zh"
        # 1. CoreWeave target bridge v4.13 -> v5.0 (USD per share)
        files[f"crwv-bridge-{L}"] = waterfall([
            ("v4.13 目標價" if z else "v4.13 target", 25.51, "start"),
            ("① 改用收支型估值方法" if z else "① New method (funding template)", 41.68, "delta"),
            ("② Q3 實績取代推估" if z else "② Q3 actuals replace estimates", -11.33, "delta"),
            ("③ Tokenomics 更新" if z else "③ Tokenomics update", 0.00, "delta"),
            ("④ 現價 43.66→60.77" if z else "④ Price 43.66→60.77", 1.91, "delta"),
            ("⑤ 同業與無風險利率" if z else "⑤ Peers and risk-free rate", 18.44, "delta"),
            ("v5.0 目標價" if z else "v5.0 target", 76.20, "end"),
        ], 0, 90, [0, 20, 40, 60, 80],
            "美元／股；DCF 為 0，目標價全部來自同業倍數那一半" if z else "USD per share; the DCF half is zero, so the whole target comes from the peer-multiple half",
            "CoreWeave target bridge", l=220)
        # 2. CoreWeave five-year FCF by scenario (USD bn)
        files[f"crwv-fcf-{L}"] = hbars([
            ("情境 A（樂觀）" if z else "Scenario A (bull)", -175.2, RED),
            ("情境 B（基準）" if z else "Scenario B (base)", -95.7, ORANGE),
            ("情境 C（保守）" if z else "Scenario C (bear)", -56.9, ORANGE),
        ], -200, 0, [-200, -150, -100, -50, 0],
            "十億美元；FY2026–FY2030 自由現金流合計，我的模型推估" if z else "USD bn; FY2026–FY2030 free cash flow summed, my model's estimate",
            "CoreWeave five-year free cash flow", fmt="{:.1f}", l=170)
        # 3. Gate flow
        if z:
            boxes = [(20, 30, 190, 74, "#e4effc", INK, ["估值評等", "只看上檔空間", "（DCF＋同業倍數）"]),
                     (20, 140, 190, 74, "#fff4d6", INK, ["收支關卡", "情境 B 五年自由現金流", "合計 ≥ 0？"]),
                     (290, 85, 160, 74, "#eef0ec", INK, ["估值評等是", "買進以上", "且關卡不通過？"]),
                     (520, 30, 140, 64, RED, "#fff", ["是：收支不足", "不給買進"]),
                     (520, 150, 140, 64, BLUE, "#fff", ["否：照估值評等", ""])]
            arrows = [(210, 67, 288, 105, ""), (210, 177, 288, 140, ""), (450, 105, 518, 70, "是"), (450, 140, 518, 175, "否")]
        else:
            boxes = [(20, 30, 190, 74, "#e4effc", INK, ["Valuation rating", "upside only", "(DCF + peer multiples)"]),
                     (20, 140, 190, 74, "#fff4d6", INK, ["Funding gate", "base-case 5-yr free", "cash flow ≥ 0?"]),
                     (290, 85, 160, 74, "#eef0ec", INK, ["Rated buy or", "better, and the", "gate fails?"]),
                     (520, 30, 140, 64, RED, "#fff", ["Yes: underfunded", "no buy"]),
                     (520, 150, 140, 64, BLUE, "#fff", ["No: keep the", "valuation rating"])]
            arrows = [(210, 67, 288, 105, ""), (210, 177, 288, 140, ""), (450, 105, 518, 70, "yes"), (450, 140, 518, 175, "no")]
        files[f"gate-flow-{L}"] = flow(boxes, arrows, "funding gate", H=240)
        # 4. Oracle reverse DCF: long-contract price
        files[f"orcl-plong-{L}"] = hbars([
            ("我的基準" if z else "My base case", 9.70, BLUE),
            ("評等升到中立所需" if z else "Needed for a neutral rating", 11.25, AXIS),
            ("我設的合理區間上緣" if z else "Top of my plausible range", 12.72, AXIS),
            ("現價 115.16 隱含" if z else "Implied by price of 115.16", 13.99, ORANGE),
        ], 0, 16, [0, 4, 8, 12, 16],
            "百萬美元／MW／年（長約每 MW 年收入），我的模型反解" if z else "USD m per MW per year (long-contract revenue), solved from my model",
            "Oracle implied contract price", band=(8.91, 12.72, "合理區間 8.91–12.72" if z else "plausible range 8.91–12.72"), l=200)
        # 5. Oracle stress: extra external funding by delay
        files[f"orcl-stress-{L}"] = grouped(
            ["0", "3", "6", "9", "12"] if not z else ["延誤 0 月", "3 月", "6 月", "9 月", "12 月"],
            [("客戶出資 24.3%（基準）" if z else "Customers fund 24.3% (base)", BLUE, [0, 5.0, 12.3, 19.6, 27.0]),
             ("客戶完全不出資" if z else "Customers fund nothing", ORANGE, [29.9, 37.2, 44.5, 51.9, 59.2])],
            70, [0, 20, 40, 60], "十億美元；情境 B，FY27 Q2–FY2031 另需外部融資，我的模型推估" if z else
            "USD bn; base case, extra external funding FY27 Q2–FY2031 by months of build delay; my model's estimate",
            "Oracle stress table")
        # 6. Anthropic valuation vs IPO range
        files[f"ant-val-{L}"] = hbars([
            ("DCF" if z else "DCF", 54.37, ORANGE),
            ("加權目標價（各半）" if z else "Weighted target (50/50)", 82.71, BLUE),
            ("同業倍數（我調整後）" if z else "Peer multiple (my adjustment)", 111.06, AQUA),
            ("同業倍數（未調整）" if z else "Peer multiple (unadjusted)", 153.44, AXIS),
        ], 0, 170, [0, 40, 80, 120, 160],
            "美元／股；黃色帶為公司公布的發行價區間" if z else "USD per share; yellow band is the company's offer price range",
            "Anthropic valuation versus IPO range", band=(70, 78, "發行價區間 70–78" if z else "offer range 70–78"), l=200)
        # 7. Supermicro EPS
        files[f"smci-eps-{L}"] = hbars([
            ("我舊模型的算法" if z else "My old method", 2.03, ORANGE),
            ("公司公布（10-Q）" if z else "Company reported (10-Q)", 1.75, INK2),
            ("我修正後的算法" if z else "My corrected method", 1.75, BLUE),
        ], 0, 2.4, [0, 0.5, 1.0, 1.5, 2.0],
            "美元；1Q FY27 稀釋每股盈餘" if z else "USD; diluted EPS for 1Q FY27",
            "Supermicro diluted EPS", l=200)
        # 8. Meta bridge
        files[f"meta-bridge-{L}"] = waterfall([
            ("v0.1.6 目標價" if z else "v0.1.6 target", 844.10, "start"),
            ("目標時點改 12 個月後" if z else "Target date: 12 months out", 1.79, "delta"),
            ("在建工程分 4 季轉入" if z else "Construction in 4 quarters", -0.83, "delta"),
            ("股數加計未歸屬 RSU" if z else "Add unvested RSUs to shares", -34.61, "delta"),
            ("在建工程折舊時點" if z else "Timing of construction depreciation", 0.07, "delta"),
            ("容量改讀實際上線時程" if z else "Capacity from go-live schedule", -30.64, "delta"),
            ("既有機隊世代固定" if z else "Freeze existing fleet mix", -1.44, "delta"),
            ("v0.2.0 目標價" if z else "v0.2.0 target", 778.44, "end"),
        ], 600, 870, [600, 650, 700, 750, 800, 850],
            "美元／股；橫軸從 600 起，放大變動" if z else "USD per share; axis starts at 600 to show the steps",
            "Meta target bridge", l=230)
    for k, v in files.items():
        (OUT / f"{k}.svg").write_text(v, encoding="utf-8")
    print(len(files), "charts")


if __name__ == "__main__":
    build()
