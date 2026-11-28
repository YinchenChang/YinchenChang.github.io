"""Charts for the 2026-11-28 weekly essay (zh and en).

Writes inline SVG files to _includes/charts/2026-11-28/<name>-<lang>.svg.
Data sources (company-models main, 2026-11-21 to 11-25):
  - NVIDIA target path 333.51 -> 300.62 -> 316.02, CEO cases, price 125.53:
    docs/reports/20261124_外部稽核優化_第三波_會改值對照.md; markets/invest_map/README.md v0.6.57;
    site _data/coverage.json (map v0.6.56 at HEAD~ vs v0.6.60)
  - C0 readings: docs/reports/20261125_NVIDIA_C0判定納入第三季.md
  - Price vs target change: _data/coverage.json v0.6.56 (git HEAD before this build) vs v0.6.60,
    non-Taiwan names, Anthropic and SanDisk (split) excluded
Run: python3 tools/charts_20261128.py <path to previous coverage.json>
"""
import json, sys
from pathlib import Path

from charts_20261114 import (AQUA, AXIS, BLUE, GRID, INK, INK2, MUTED, ORANGE, YELLOW,
                             esc, hbars, svg, text, waterfall)

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "_includes/charts/2026-11-28"
RED = "#c43b3a"
GREY = "#b9b7af"


def oos(L):
    zh = L == "zh"
    W, H, l, r, t, b = 680, 300, 60, 20, 30, 70
    lo, hi = -0.35, 0.0
    sy = lambda v: t + (hi - v) / (hi - lo) * (H - t - b)
    o = []
    for g in [0, -0.1, -0.2, -0.3]:
        o.append(f'<line x1="{l}" x2="{W - r}" y1="{sy(g):.1f}" y2="{sy(g):.1f}" stroke="{GRID}"/>')
        o.append(text(l - 6, sy(g) + 4, f"{g * 100:.0f}%", 11, MUTED, "end"))
    o.append(f'<line x1="{l}" x2="{W - r}" y1="{sy(-0.15):.1f}" y2="{sy(-0.15):.1f}" stroke="{RED}" stroke-dasharray="5 4"/>')
    o.append(text(W - r - 4, sy(-0.15) - 5, "門檻 −15%" if zh else "Threshold −15%", 11, RED, "end"))
    groups = [("主讀數：累計實績 vs 層級" if zh else "Main: cumulative actuals vs layer", -0.311, -0.239),
              ("第二讀數：最近一季×4 vs 層級" if zh else "Second: latest quarter ×4 vs layer", -0.253, -0.097)]
    gw = (W - l - r) / 2
    for i, (name, a, c) in enumerate(groups):
        x = l + i * gw + gw * 0.25
        for j, (v, col) in enumerate([(a, GREY), (c, ORANGE)]):
            xx = x + j * 62
            o.append(f'<rect x="{xx:.1f}" y="{sy(0):.1f}" width="54" height="{sy(v) - sy(0):.1f}" rx="3" fill="{col}"><title>{esc(name)}: {v * 100:.1f}%</title></rect>')
            o.append(text(xx + 27, sy(v) + 15, f"{v * 100:.1f}%", 12, INK, "middle", 600))
        o.append(text(x + 58, H - b + 20, name, 12, INK2, "middle"))
    o.append(f'<rect x="{l}" y="{H - 28}" width="12" height="12" fill="{GREY}"/>')
    o.append(text(l + 18, H - 18, "只有 Q1、Q2" if zh else "Q1-Q2 only", 11.5, INK2))
    o.append(f'<rect x="{l + 140}" y="{H - 28}" width="12" height="12" fill="{ORANGE}"/>')
    o.append(text(l + 158, H - 18, "加入 Q3" if zh else "Q3 added", 11.5, INK2))
    o.append(text(l + 270, H - 18, "NVIDIA 資料中心營收實績 vs 我的層級值 476.4（十億美元）" if zh else "NVIDIA data center revenue vs my layer value of 476.4 ($bn)", 11, MUTED))
    return svg(W, H, "".join(o), "out-of-sample check")


def scatter(rows, L):
    zh = L == "zh"
    W, H, l, r, t, b = 680, 470, 64, 20, 30, 56
    lo, hi = -0.55, 0.1
    sx = lambda v: l + (v - lo) / (hi - lo) * (W - l - r)
    sy = lambda v: t + (hi - v) / (hi - lo) * (H - t - b)
    o = []
    for g in [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1]:
        o.append(f'<line x1="{l}" x2="{W - r}" y1="{sy(g):.1f}" y2="{sy(g):.1f}" stroke="{GRID}"/>')
        o.append(f'<line y1="{t}" y2="{H - b}" x1="{sx(g):.1f}" x2="{sx(g):.1f}" stroke="{GRID}"/>')
        o.append(text(l - 6, sy(g) + 4, f"{g * 100:.0f}%", 11, MUTED, "end"))
        o.append(text(sx(g), H - b + 16, f"{g * 100:.0f}%", 11, MUTED, "middle"))
    o.append(f'<line x1="{sx(lo):.1f}" y1="{sy(lo):.1f}" x2="{sx(hi):.1f}" y2="{sy(hi):.1f}" stroke="{AXIS}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    o.append(text(sx(-0.53), sy(0.05), "對角線以上：目標價跌得比股價少 → 變便宜" if zh else "Above the line: target fell less than price, so cheaper", 11.5, INK2))
    o.append(text(sx(0.08), sy(-0.52), "對角線以下：目標價跌得比股價多 → 變貴" if zh else "Below the line: target fell more than price, so dearer", 11.5, INK2, "end"))
    o.append(text((l + W - r) / 2, H - 14, "股價變動（2026-11-13 → 11-20 收盤）" if zh else "Share price change (close, 13 Nov → 20 Nov 2026)", 12, INK2, "middle"))
    o.append(f'<text transform="translate(16 {(t + H - b) / 2}) rotate(-90)" font-size="12" fill="{INK2}" text-anchor="middle">'
             f'{"我的目標價變動（地圖 v0.6.56 → v0.6.60）" if zh else "My target change (map v0.6.56 → v0.6.60)"}</text>')
    show = {"nvda", "nbis", "crwv", "mu", "msft"}
    for slug, name, px, tg in rows:
        x, y = sx(px), sy(tg)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BLUE}" stroke="#fff" stroke-width="2">'
                 f'<title>{esc(name)}: {"股價" if zh else "price"} {px * 100:+.1f}%, {"目標價" if zh else "target"} {tg * 100:+.1f}%</title></circle>')
        if slug in show:
            o.append(text(x + 8, y + 4, name, 11, INK))
    return svg(W, H, "".join(o), "scatter of price change vs target change")


def build(prev):
    old = {x["slug"]: x for x in json.load(open(prev))["items"]}
    new = json.load(open(SITE / "_data/coverage.json"))["items"]
    rows = []
    for x in new:
        y = old.get(x["slug"])
        if not y or x["ccy"] == "TWD" or x["slug"] in ("anthropic", "sndk"):
            continue
        if not (x["price"] and y["price"] and x["target"] and y["target"]):
            continue
        rows.append((x["slug"], x["tk"], x["price"] / y["price"] - 1, x["target"] / y["target"] - 1))
    OUT.mkdir(parents=True, exist_ok=True)
    for L in ("zh", "en"):
        zh = L == "zh"
        files = {
            "nvda-path": waterfall([
                ("地圖 v0.6.56（11-21 前）" if zh else "Map v0.6.56 (before 21 Nov)", 333.51, "start"),
                ("同業報價換 11-20 收盤" if zh else "Peer prices moved to 20 Nov close", 300.62 - 333.51, "delta"),
                ("第三季財報滾入" if zh else "Q3 results rolled in", 316.02 - 300.62, "delta"),
                ("現在（v0.3.16）" if zh else "Now (v0.3.16)", 316.02, "end")],
                0, 360, [0, 100, 200, 300], "NVIDIA 加權目標價（美元）；我的模型" if zh else "NVIDIA weighted target (US$); my model",
                "NVIDIA target path", l=230),
            "ceo": hbars([
                ("基準（不採執行長異動）" if zh else "Base (CEO change not applied)", 316.02, BLUE),
                ("WACC +0.5 個百分點" if zh else "WACC +0.5pt", 313.85, AQUA),
                ("WACC +1 個百分點" if zh else "WACC +1pt", 311.81, AQUA),
                ("WACC +2 個百分點" if zh else "WACC +2pt", 308.13, AQUA),
                ("情境權重 15／55／30" if zh else "Scenario weights 15/55/30", 295.07, AQUA),
                ("溢價保留 50%" if zh else "Premium kept at 50%", 262.32, ORANGE),
                ("溢價保留 25%" if zh else "Premium kept at 25%", 235.47, ORANGE),
                ("三案同時成立" if zh else "All three at once", 240.66, RED),
                ("11-20 收盤股價" if zh else "Share price, 20 Nov close", 125.53, GREY)],
                0, 350, [0, 100, 200, 300], "美元；參數全部是假設，無實證；我的模型" if zh else "US$; all parameters assumed, no evidence; my model",
                "NVIDIA CEO change cases", l=230),
            "oos": oos(L),
            "scatter": scatter(rows, L),
        }
        for k, v in files.items():
            (OUT / f"{k}-{L}.svg").write_text(v, encoding="utf-8")
    return rows


if __name__ == "__main__":
    rows = build(sys.argv[1])
    print(len(rows), "points")
