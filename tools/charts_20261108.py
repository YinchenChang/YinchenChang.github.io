"""Charts for the 2026-11-08 essay (Chinese and English versions).

Writes inline SVG files to _includes/charts/2026-11-08/<name>-<lang>.svg; the posts
include them with {% include charts/2026-11-08/<name>-<lang>.svg %}.
Each mark carries a <title>, so hovering shows its value.

Data sources (all public or in the essay):
  - price and target changes: _data/coverage.json now vs. the 2026-10-31 build
    (git show 9b8e20c:_data/coverage.json), non-Taiwan semiconductor names only
  - NVIDIA DCF bridge: company-models nvidia/README.md (v0.3 and v0.3.1–v0.3.4 tables)
  - TPU / Trainium3: Tokenomics report 20261104_v21.10 (NonNV H column)
  - Terra: Tokenomics report 20261105_v22.0, table 1

Run: python3 tools/charts_20261108.py <path to the 2026-10-31 coverage.json>
"""
import html, json, sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "_includes/charts/2026-11-08"

INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
# diverging (rating): strong short … strong buy, gray midpoint
DIV = ["#c43b3a", "#f0a09f", "#d6d5cf", "#86b6ef", "#1c5cab"]
FONT = 'font-family="system-ui,-apple-system,Segoe UI,sans-serif"'


def esc(s):
    return html.escape(str(s), quote=True)


def svg(w, h, body, label):
    return (f'<figure class="chart"><svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(label)}" '
            f'{FONT} style="max-width:{w}px;height:auto">{body}</svg></figure>\n')


def text(x, y, s, size=12, fill=INK2, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>'


def pct(v, d=0):
    return f"{v * 100:+.{d}f}%"


# ---------------------------------------------------------------- 1. scatter
def scatter(rows, L):
    W, H, l, r, t, b = 680, 470, 64, 20, 30, 56
    lo, hi = -0.65, 0.0
    sx = lambda v: l + (v - lo) / (hi - lo) * (W - l - r)
    sy = lambda v: t + (hi - v) / (hi - lo) * (H - t - b)
    o = []
    for g in [-0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0]:
        o.append(f'<line x1="{l}" x2="{W - r}" y1="{sy(g):.1f}" y2="{sy(g):.1f}" stroke="{GRID}"/>')
        o.append(f'<line y1="{t}" y2="{H - b}" x1="{sx(g):.1f}" x2="{sx(g):.1f}" stroke="{GRID}"/>')
        o.append(text(l - 6, sy(g) + 4, f"{g * 100:.0f}%", 11, MUTED, "end"))
        o.append(text(sx(g), H - b + 16, f"{g * 100:.0f}%", 11, MUTED, "middle"))
    # diagonal: target fell as much as price
    o.append(f'<line x1="{sx(lo):.1f}" y1="{sy(lo):.1f}" x2="{sx(hi):.1f}" y2="{sy(hi):.1f}" stroke="{AXIS}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    zh = L == "zh"
    o.append(text(sx(-0.62), sy(-0.05), "對角線以上：目標價跌得比股價少 → 變便宜" if zh else "Above the line: target fell less than price, so cheaper", 11.5, INK2))
    o.append(text(sx(-0.01), sy(-0.62), "對角線以下：目標價跌得比股價多 → 變貴" if zh else "Below the line: target fell more than price, so dearer", 11.5, INK2, "end"))
    o.append(text((l + W - r) / 2, H - 14, "股價變動（2026-10-23 → 11-05 收盤）" if zh else "Share price change (close, 23 Oct → 5 Nov 2026)", 12, INK2, "middle"))
    o.append(f'<text transform="translate(16 {(t + H - b) / 2}) rotate(-90)" font-size="12" fill="{INK2}" text-anchor="middle">'
             f'{"目標價變動（10-31 → 11-08 地圖）" if zh else "Target change (map, 31 Oct → 8 Nov)"}</text>')
    label = {"NVDA", "MRVL", "SNDK", "AMD", "000660", "AVGO", "TER", "300502", "SMCI"}
    for k, name, px, tg, *_ in rows:
        x, y = sx(px), sy(tg)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BLUE}" stroke="#fff" stroke-width="2">'
                 f'<title>{esc(name)}: {"股價" if zh else "price"} {pct(px, 1)}, {"目標價" if zh else "target"} {pct(tg, 1)}</title></circle>')
        if k in label:
            right = px > -0.08
            o.append(text(x - 8 if right else x + 8, y + (14 if k == "NVDA" else 4), name, 11, INK, "end" if right else "start"))
    return svg(W, H, "".join(o), "scatter of price change vs target change")


# ---------------------------------------------------------------- 2. ratings
def ratings(old, new, L):
    zh = L == "zh"
    cats = ["強力放空", "放空", "中立", "買進", "強力買進"]
    en = {"強力放空": "Strong short", "放空": "Short", "中立": "Neutral", "買進": "Buy", "強力買進": "Strong buy"}
    W, H, l, r = 680, 170, 120, 20
    tot = sum(old.values())
    o = []
    for i, (lab, cnt) in enumerate([("10-31", old), ("11-08", new)]):
        y = 34 + i * 54
        o.append(text(l - 10, y + 21, (f"{lab} 地圖" if zh else f"Map, {lab}"), 12.5, INK, "end", 600))
        x = l
        for j, c in enumerate(cats):
            n = cnt.get(c, 0)
            if not n:
                continue
            w = n / tot * (W - l - r)
            nm = c if zh else en[c]
            o.append(f'<rect x="{x + 1:.1f}" y="{y}" width="{w - 2:.1f}" height="32" rx="3" fill="{DIV[j]}"><title>{esc(nm)}: {n}</title></rect>')
            fg = "#fff" if j in (0, 4) else INK
            o.append(text(x + w / 2, y + 21, str(n), 12.5, fg, "middle", 600))
            x += w
    lx = l
    for j, c in enumerate(cats):
        nm = c if zh else en[c]
        o.append(f'<rect x="{lx}" y="{H - 26}" width="12" height="12" rx="2" fill="{DIV[j]}"/>')
        o.append(text(lx + 17, H - 16, nm, 11.5, INK2))
        lx += 100 if zh else 108
    return svg(W, H, "".join(o), "rating distribution before and after")


# ---------------------------------------------------------------- 3. NVIDIA bridge
def bridge(L):
    zh = L == "zh"
    steps = [  # (zh, en, value, kind) kind: total / delta
        ("舊 DCF", "Old DCF", 235.05, "total"),
        ("現金流定義", "Cash-flow definition", -6.20, "delta"),
        ("折現率 10%→12.5%", "Discount rate 10%→12.5%", -59.96, "delta"),
        ("永續價值算法", "Terminal value method", -31.04, "delta"),
        ("扣股利", "Dividends", -1.00, "delta"),
        ("自算 β（WACC→14.4%）", "Own beta (WACC→14.4%)", -15.57, "delta"),
        ("其他（現金滾到評價日等）", "Other (cash rolled forward etc.)", 3.53, "delta"),
        ("新 DCF", "New DCF", 124.81, "total"),
    ]
    W, H, l, r, t = 680, 352, 200, 70, 14
    rowh = 36
    sx = lambda v: l + v / 250 * (W - l - r)
    o = []
    for g in [0, 50, 100, 150, 200, 250]:
        o.append(f'<line x1="{sx(g):.1f}" x2="{sx(g):.1f}" y1="{t}" y2="{t + rowh * len(steps)}" stroke="{GRID}"/>')
        o.append(text(sx(g), t + rowh * len(steps) + 16, f"{g}", 11, MUTED, "middle"))
    run = 0
    for i, (a, b_, v, kind) in enumerate(steps):
        y = t + i * rowh + 6
        nm = a if zh else b_
        o.append(text(l - 10, y + 17, nm, 12, INK if kind == "total" else INK2, "end", 600 if kind == "total" else 400))
        if kind == "total":
            x0, x1, col = 0, v, BLUE
            run = v
            lab = f"{v:.2f}"
        else:
            x0, x1 = sorted([run, run + v])
            col = ORANGE if v < 0 else AQUA
            run += v
            lab = f"{v:+.2f}"
        o.append(f'<rect x="{sx(x0):.1f}" y="{y}" width="{max(sx(x1) - sx(x0), 2):.1f}" height="24" rx="3" fill="{col}"><title>{esc(nm)}: {lab}</title></rect>')
        o.append(text(sx(x1) + 6, y + 17, lab, 12, INK, "start", 600 if kind == "total" else 400))
    o.append(text(l, H - 6, "美元／股（情境加權，推到 12 個月後）" if zh else "US$ per share (scenario-weighted, 12 months forward)", 11.5, MUTED))
    return svg(W, H, "".join(o), "NVIDIA DCF bridge")


# ---------------------------------------------------------------- 4. TPU / Trainium
def chips(L):
    zh = L == "zh"
    rows = [("Google TPU v7", 2.000, 1.061), ("AWS Trainium3", 4.357, 2.179)]
    W, H, l, r, t = 680, 230, 130, 60, 40
    sx = lambda v: l + v / 4.6 * (W - l - r)
    o = []
    for g in [0, 1, 2, 3, 4]:
        o.append(f'<line x1="{sx(g):.1f}" x2="{sx(g):.1f}" y1="{t - 8}" y2="{t + 2 * 66}" stroke="{GRID}"/>')
        o.append(text(sx(g), t + 2 * 66 + 16, f"{g}×", 11, MUTED, "middle"))
    o.append(f'<line x1="{sx(1):.1f}" x2="{sx(1):.1f}" y1="{t - 14}" y2="{t + 2 * 66}" stroke="{INK2}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    o.append(text(sx(1) + 4, t - 18, "＝ NVIDIA VR200" if zh else "= NVIDIA VR200", 11.5, INK2))
    ser = [("各用自己最高原生精度（v21.9）" if zh else "Each chip's own best precision (v21.9)", ORANGE, 1),
           ("同用 FP8 比較（v21.10 基準）" if zh else "Both compared at FP8 (v21.10 base)", BLUE, 2)]
    for i, row in enumerate(rows):
        y = t + i * 66
        o.append(text(l - 10, y + 30, row[0], 12.5, INK, "end", 600))
        for j, (nm, col, idx) in enumerate(ser):
            yy = y + 4 + j * 26
            v = row[idx]
            o.append(f'<rect x="{sx(0):.1f}" y="{yy}" width="{sx(v) - sx(0):.1f}" height="22" rx="3" fill="{col}"><title>{esc(row[0])}, {esc(nm)}: {v:.2f}×</title></rect>')
            o.append(text(sx(v) + 6, yy + 16, f"{v:.2f}×", 12, INK))
    lx = l
    for nm, col, _ in ser:
        o.append(f'<rect x="{lx}" y="{H - 22}" width="12" height="12" rx="2" fill="{col}"/>')
        o.append(text(lx + 17, H - 12, nm, 11.5, INK2))
        lx += 250
    return svg(W, H, "".join(o), "cost per token relative to VR200")


# ---------------------------------------------------------------- 5. Terra mix + effects
def terra(L):
    zh = L == "zh"
    tiers = [("Luna", AQUA), ("Sol", BLUE), ("Astra", ORANGE), ("Terra", YELLOW)]
    mixes = [("v21.12", [0.40, 0.45, 0.15, 0.0]), ("v22.0", [0.40, 0.30, 0.15, 0.15])]
    W, H, l, r = 680, 400, 110, 20
    o = [text(l, 18, "2026 付費 token 組合" if zh else "2026 paid-token mix", 12.5, INK, "start", 600)]
    for i, (lab, m) in enumerate(mixes):
        y = 30 + i * 44
        o.append(text(l - 10, y + 20, lab, 12.5, INK, "end", 600))
        x = l
        for (nm, col), v in zip(tiers, m):
            if not v:
                continue
            w = v * (W - l - r)
            o.append(f'<rect x="{x + 1:.1f}" y="{y}" width="{w - 2:.1f}" height="30" rx="3" fill="{col}"><title>{nm}: {v:.0%}</title></rect>')
            o.append(text(x + w / 2, y + 20, f"{nm} {v:.0%}", 12, INK if col == YELLOW else "#fff", "middle", 600))
            x += w
    # effects
    t2 = 150
    o.append(text(l, t2, "對每 GW 數字的影響（VR200 基準）" if zh else "Effect on per-GW figures (VR200 base)", 12.5, INK, "start", 600))
    eff = [("平均有效單價 P" if zh else "Average effective price P", -0.0605, ""),
           ("每 GW 付費產能 Q" if zh else "Paid capacity per GW Q", 0.0476, ""),
           ("每 GW 營收 P×Q" if zh else "Revenue per GW, P×Q", 0.0452, "49.51 → 51.75"),
           ("變現率 m（機械性）" if zh else "Monetisation m (mechanical)", 0.0644, "1.355 → 1.443")]
    lo, hi = -0.08, 0.08
    l2 = 200
    sx = lambda v: l2 + (v - lo) / (hi - lo) * (W - l2 - 140)
    y0 = t2 + 14
    for g in [-0.08, -0.04, 0, 0.04, 0.08]:
        o.append(f'<line x1="{sx(g):.1f}" x2="{sx(g):.1f}" y1="{y0}" y2="{y0 + 4 * 40}" stroke="{GRID if g else AXIS}"/>')
        o.append(text(sx(g), y0 + 4 * 40 + 16, f"{g * 100:+.0f}%" if g else "0", 11, MUTED, "middle"))
    for i, (nm, v, note) in enumerate(eff):
        y = y0 + i * 40 + 8
        o.append(text(l2 - 10, y + 16, nm, 12, INK, "end"))
        x0, x1 = sorted([sx(0), sx(v)])
        col = ORANGE if v < 0 else BLUE
        extra = ' fill-opacity="0.45" stroke="%s" stroke-dasharray="3 2"' % BLUE if i == 3 else ""
        o.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" height="22" rx="3" fill="{col}"{extra}><title>{esc(nm)}: {pct(v, 2)}</title></rect>')
        o.append(text(max(x1, sx(0)) + 6, y + 16, pct(v, 1) + (f"（{note}）" if note and zh else (f" ({note})" if note else "")), 12, INK))
    o.append(text(l2, H - 6, "營收單位：十億美元／GW／年。m 上升只因分母（有效牌價）變便宜，不是變現改善。" if zh else
                  "Revenue in US$bn per GW per year. m rises only because its denominator got cheaper.", 11, MUTED))
    return svg(W, H, "".join(o), "Terra paid mix and per-GW effects")


# ---------------------------------------------------------------- 6. P x Q flow
def flow(L):
    zh = L == "zh"
    W, H = 680, 250
    box = lambda x, y, w, h, s, fill="#f0efec", fg=INK: (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{AXIS}"/>'
        + "".join(text(x + w / 2, y + h / 2 + 5 - 8 * (len(s) - 1) + 16 * k, line, 12.5, fg, "middle", 600 if k == 0 else 400) for k, line in enumerate(s)))
    arrow = lambda x1, y1, x2, y2: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK2}" stroke-width="1.5" marker-end="url(#ah)"/>'
    o = [f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker></defs>']
    if zh:
        q = ["數量 Q", "1 GW 產能 × 利用率", "× 付費占比 × 產出折減"]
        p = ["單價 P", "表列牌價 × (1 − 折扣)", "× 變現率 m × 層級組合"]
        rv = ["每 GW 營收", "＝ P × Q"]
        c = ["Terra 換掉一部分 Sol", "Terra 半價、每 GW 能跑", "的 token 比 Sol 多"]
    else:
        q = ["Quantity Q", "1 GW capacity × utilisation", "× paid share × derate"]
        p = ["Price P", "list price × (1 − discount)", "× monetisation m × tier mix"]
        rv = ["Revenue/GW", "= P × Q"]
        c = ["Terra replaces part of Sol", "half the price, more tokens", "per GW than Sol"]
    o.append(box(20, 20, 210, 70, c, "#fff4d6"))
    o.append(box(300, 20, 230, 74, p, "#e4effc"))
    o.append(box(300, 150, 230, 74, q, "#e4effc"))
    o.append(box(570, 85, 100, 70, rv, BLUE, "#fff"))
    o.append(arrow(230, 50, 298, 50))
    o.append(text(264, 42, "P ↓", 12, ORANGE, "middle", 700))
    o.append(arrow(200, 90, 298, 175))
    o.append(text(240, 150, "Q ↑", 12, BLUE, "middle", 700))
    o.append(arrow(530, 57, 568, 108))
    o.append(arrow(530, 187, 568, 135))
    return svg(W, H, "".join(o), "price times quantity flow")


def main(old_path):
    OUT.mkdir(parents=True, exist_ok=True)
    o = {x["tk"]: x for x in json.load(open(old_path, encoding="utf-8"))["items"]}
    n = {x["tk"]: x for x in json.load(open(SITE / "_data/coverage.json", encoding="utf-8"))["items"]}
    rows, old_r, new_r = [], {}, {}
    names_en = {"000660": "SK hynix", "005930": "Samsung", "300308": "Innolight", "300502": "Eoptolink",
                "300476": "Victory Giant", "MU": "Micron", "6857": "Advantest", "6146": "Disco",
                "6315": "TOWA", "7729": "Accretech", "4062": "Ibiden", "042700": "Hanmi", "285A": "Kioxia"}
    for k, x in n.items():
        y = o.get(k)
        if x["tw"] or not y or x["layer"] not in ("L3 IT 設備", "L2 半導體製造與設備"):
            continue
        if not (x["target"] and y["target"] and x["price"] and y["price"]):
            continue
        assert not x["tw"]
        rows.append((k, x["name"], x["price"] / y["price"] - 1, x["target"] / y["target"] - 1))
        old_r[y["rating"]] = old_r.get(y["rating"], 0) + 1
        new_r[x["rating"]] = new_r.get(x["rating"], 0) + 1
    for L in ("zh", "en"):
        rr = rows if L == "zh" else [(k, names_en.get(k, nm), a, b) for k, nm, a, b in rows]
        files = {"scatter": scatter(rr, L), "ratings": ratings(old_r, new_r, L), "nvda-dcf": bridge(L),
                 "tpu": chips(L), "terra": terra(L), "pq-flow": flow(L)}
        for name, s in files.items():
            (OUT / f"{name}-{L}.svg").write_text(s, encoding="utf-8")
    print(len(rows), "names;", old_r, new_r)


if __name__ == "__main__":
    main(sys.argv[1])
