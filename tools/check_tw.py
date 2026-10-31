"""Stop publishing if any page or post shows a target price for a Taiwan-listed stock.

Rule (Andy 2026-10-31): Taiwan stocks never show a target price, nor anything that
reveals it (upside, pessimistic-case price, model page, quoted target prices).

Checks every row (list item, table row, paragraph or line) of _posts/, stocks/, coverage pages and index pages. A line fails when it
names a Taiwan company (name or ticker, from the AI Investment Map) and also
  (a) contains a target-price word, or
  (b) contains that company's model target or pessimistic price (rounded) as a number.
Exit code 1 lists the failing lines; 0 means clean.

Run:  python3 tools/check_tw.py /path/to/company-models [files...]
"""
import json, re, sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
WORDS = ["目標價", "隱含價", "合理價", "中心價", "上檔空間", "悲觀情境", "情境加權價", "Val!",
         "target price", "price target", "upside", "Target", "Upside", "fair value", "implied price"]


def nums(x):
    if not x:
        return set()
    return {f"{x:,.0f}", f"{x:.0f}", f"{x:,.1f}", f"{x:.1f}"}


def main(cm, files):
    d = json.loads((Path(cm) / "markets/invest_map/dist/data.json").read_text(encoding="utf-8"))
    tw = [v for v in d["valuation"] if v.get("ccy") == "TWD"]
    if not files:
        files = [p for g in ("_posts/*.md", "stocks/*/index.html", "coverage/index.html",
                             "zh/coverage/index.html", "*.md", "zh/**/*.md") for p in SITE.glob(g)]
    bad = []
    for f in files:
        f = Path(f)
        # unit = one list item / table row / paragraph / text line, so one company's row is judged alone
        units = re.split(r"</li>|</tr>|</p>|\n", f.read_text(encoding="utf-8"))
        for i, line in enumerate(units, 1):
            for v in tw:
                names = {v["name"], v["tk"]}
                if not any(re.search(rf"(?<![0-9A-Za-z]){re.escape(n)}(?![0-9A-Za-z])", line) for n in names):
                    continue
                w = [x for x in WORDS if x in line]
                n = [x for x in nums(v.get("center")) | nums(v.get("bear"))
                     if len(x.replace(",", "")) >= 3 and re.search(rf"(?<![\d.,]){re.escape(x)}(?![\d]|[.,]\d)", line)]
                if w or n:
                    bad.append(f"{f}:{i} {v['name']} {w + n}")
    if bad:
        print("STOP — Taiwan target price found:\n  " + "\n  ".join(bad))
        sys.exit(1)
    print(f"Taiwan check OK ({len(files)} files, {len(tw)} Taiwan stocks)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
