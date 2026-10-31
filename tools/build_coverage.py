"""Weekly coverage update for the public site, built from the AI Investment Map.

Source: a local clone of YinchenChang/company-models, file
markets/invest_map/dist/data.json (the map's published data; the map is the authority).

Writes:
  _data/coverage.json         public, sanitized coverage list (used by pages and the NEW badges)
  _data/coverage_state.json   last week's snapshot, used to find what changed (sanitized too)
  _data/map_extra.json        covered companies not yet placed in _data/map.yml, by layer
  stocks/<ticker>/index.html  one company page (Chinese profile)
  models/<folder>.html        mirror of each non-Taiwan model page

Rules (Andy 2026-10-31):
  * Taiwan-listed stocks (currency TWD): no target price. Nothing that reveals it either:
    target, upside, pessimistic-case price, the model page itself (its valuation tab
    has the target), and profile lines that quote any target price. Rating shown only if
    SHOW_TW_RATING is True (default False until Andy decides).
  * Other markets: published as the map shows them.
  * Models the map marks private (meta.private_models) are not mirrored.
A guard scans every generated file before anything is written; one hit stops the build.

Run:  python3 tools/build_coverage.py /path/to/company-models [--date YYYY-MM-DD]
"""
import argparse, datetime as dt, html, json, re, shutil, sys
from pathlib import Path

SHOW_TW_RATING = False  # Andy's call; default hides Taiwan ratings (see WP1.24)
NEW_DAYS = 7

SITE = Path(__file__).resolve().parent.parent
TPE = dt.timezone(dt.timedelta(hours=8))

# Words that, on a Taiwan page, mean a target price (or something that back-solves it) is present.
TW_FORBIDDEN = ["目標價", "隱含價", "合理價", "中心價", "上檔空間", "下檔空間", "悲觀情境", "情境 DCF",
                "情境DCF", "情境加權價", "規則值", "估值 v2", "加權目標", "Val!", "target price",
                "upside", "Target", "Upside"]

RATING_EN = {"強力買進": "Strong buy", "買進": "Buy", "中立": "Neutral", "放空": "Short",
             "強力放空": "Strong short", "收支不足": "Funding shortfall", "未估值": "Not valued",
             "未上市": "Private"}
LAYER_EN = {"L5 模型商": "Model labs", "L4 算力平台": "Compute platforms",
            "L3 IT 設備": "IT equipment", "L2 半導體製造與設備": "Semiconductor manufacturing and equipment"}
LAYER_ORDER = ["L5 模型商", "L4 算力平台", "L3 IT 設備", "L2 半導體製造與設備"]


def is_tw(v):
    return v.get("ccy") == "TWD"


def slug(tk):
    return re.sub(r"[^a-z0-9]+", "-", tk.lower()).strip("-")


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or ""))


def hits(text):
    return [w for w in TW_FORBIDDEN if w in text]


def sanitize_tw(fragment):
    """Drop every list item / table row / paragraph that mentions a target price."""
    if not fragment:
        return fragment
    for tag in ("li", "tr", "p"):
        fragment = re.sub(rf"<{tag}\b[^>]*>.*?</{tag}>",
                          lambda m: "" if hits(m.group(0)) else m.group(0), fragment, flags=re.S)
    return fragment


def hover(fragment):
    # the map shows sources on hover via its own script; here a plain title attribute does it
    return re.sub(r'data-src="([^"]*)"', r'title="\1" data-src="\1"', fragment or "")


def fmt_px(x, ccy):
    if x is None:
        return "—"
    return f"{ccy} {x:,.0f}" if x >= 1000 else f"{ccy} {x:,.2f}"


def fmt_pct(x):
    return "—" if x is None else f"{x*100:+.1f}%"


def latest_event(sections):
    """First dated item of 近期重大事件: (date, text)."""
    sec = sections.get("近期重大事件", "")
    m = re.search(r"<(li|tr)\b[^>]*>(.*?)</\1>", sec, flags=re.S)
    if not m:
        return None, None
    t = " ".join(strip_tags(re.sub(r"</t[dh]>", "｜", m.group(2))).split()).strip("｜ ")
    d = re.match(r"(\d{4}-\d{2}-\d{2})", t)
    return (d.group(1) if d else None), t


def build(cm: Path, today: dt.date):
    data = json.loads((cm / "markets/invest_map/dist/data.json").read_text(encoding="utf-8"))
    meta, models, profiles = data["meta"], data["models"], data["profiles"]
    private = set(meta.get("private_models", {}))
    state_path = SITE / "_data/coverage_state.json"
    prev = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    prev_items = prev.get("items", {})

    rows, state, pages, mirrors = [], {}, {}, {}
    for v in data["valuation"]:
        tk, tw = v["tk"], is_tw(v)
        m = models.get(tk) or {}
        prof = profiles.get(tk)
        model_date = m.get("date") or v.get("model_date")
        ev_date, ev_text = latest_event(prof["sections"]) if prof else (None, None)
        if tw and ev_text and hits(ev_text):
            ev_text = None
        show_val = not tw
        row = {
            "tk": tk, "slug": slug(tk), "name": v["name"], "tw": tw,
            "layer": v.get("layer"), "layer_en": LAYER_EN.get(v.get("layer"), v.get("layer")),
            "seg": v.get("seg"), "ccy": v.get("ccy"),
            "rating": v.get("tier") if (show_val or SHOW_TW_RATING) else None,
            "price": v.get("price") if show_val else None,
            "price_date": v.get("price_date") if show_val else None,
            "target": v.get("center") if show_val else None,
            "upside": v.get("cu") if show_val else None,
            "bear": v.get("bear") if show_val else None,
            "bear_ret": v.get("bu") if show_val else None,
            "gate": v.get("gate"),
            "model_ver": m.get("ver"), "model_date": model_date,
            "model_url": None, "has_profile": bool(prof),
            "event_date": ev_date, "event": ev_text,
        }
        row["rating_en"] = RATING_EN.get(row["rating"], row["rating"]) if row["rating"] else None
        # mirror the model page for non-Taiwan, non-private companies
        if not tw and m and m.get("folder") not in private:
            src = cm / m["folder"] / "dist" / m["file"]
            if src.exists():
                mirrors[m["folder"]] = src
                row["model_url"] = f"/models/{m['folder']}.html"
        old = prev_items.get(tk, {})
        row["first_seen"] = old.get("first_seen") or today.isoformat()
        # "new" date: newest of first appearance, model build, latest event
        cand = [model_date, ev_date] + ([row["first_seen"]] if (prev_items and not old) else [])
        row["new_date"] = max([x for x in cand if x], default=None)
        rows.append(row)
        st = {"first_seen": row["first_seen"], "model_ver": row["model_ver"], "event": ev_text}
        if row["rating"]:
            st["rating"] = row["rating"]
        if show_val:
            st["target"] = row["target"]
        state[tk] = st
        if prof:
            pages[tk] = page_html(row, prof, tw)

    rows.sort(key=lambda r: (LAYER_ORDER.index(r["layer"]) if r["layer"] in LAYER_ORDER else 9, r["seg"] or "", r["name"]))
    by_folder = {models[r["tk"]]["folder"]: f'/stocks/{r["slug"]}/' for r in rows if r["has_profile"] and r["tk"] in models}
    cov = {"by_folder": by_folder, "updated": today.isoformat(), "map_version": meta.get("version"),
           "price_note": meta.get("price_date"), "show_tw_rating": SHOW_TW_RATING, "items": rows}
    changes = diff(rows, prev_items, today)
    # every covered company should sit in one map segment (_data/map.yml tks); new ones go to their layer's
    # "newly added" line until classified by hand
    import yaml
    mp = yaml.safe_load((SITE / "_data/map.yml").read_text(encoding="utf-8"))
    placed = [str(t) for L in mp for sg in L.get("segs", []) for t in sg.get("tks", [])]
    dup = sorted({t for t in placed if placed.count(t) > 1})
    unknown = sorted(set(placed) - {r["tk"] for r in rows})
    default_layer = {"AI 模型商": 0, "AI 雲端平台": 1, "Neocloud（GPU 租賃）": 1, "運算": 4, "記憶體": 5, "網通": 6,
                     "伺服器組裝": 7, "電源與散熱": 7, "代工與封測": 8, "載板與 PCB": 8, "設備與材料": 9}
    extra = {}
    for r in rows:
        if r["tk"] not in placed:
            extra.setdefault(str(default_layer.get(r["seg"], 9)), []).append(r["tk"])
    if dup or unknown or extra:
        print(f"map placement: duplicates {dup}, not covered {unknown}, unplaced {extra}")
    posts = {}  # weekly essays are written separately (Andy 2026-10-31: no list-style weekly post)

    out = {
        "_data/coverage.json": json.dumps(cov, ensure_ascii=False, indent=1),
        "_data/map_extra.json": json.dumps(extra, ensure_ascii=False, indent=1),
        "_data/coverage_state.json": json.dumps({"updated": today.isoformat(), "items": state}, ensure_ascii=False, indent=1),
    }
    for tk, body in pages.items():
        out[f"stocks/{slug(tk)}/index.html"] = body
    for name, body in posts.items():
        out[f"_posts/{name}"] = body

    # ---- guard: no Taiwan target price anywhere ----
    tw_rows = [r for r in rows if r["tw"]]
    problems = []
    for r in tw_rows:
        for k in ("price", "target", "upside", "bear", "bear_ret", "model_url"):
            if r[k] is not None:
                problems.append(f"{r['tk']}: field {k} set")
        if not SHOW_TW_RATING and r["rating"]:
            problems.append(f"{r['tk']}: rating shown")
        body = out.get(f"stocks/{slug(r['tk'])}/index.html", "")
        if hits(body):
            problems.append(f"{r['tk']} page: {hits(body)}")
        if r["event"] and hits(r["event"]):
            problems.append(f"{r['tk']} event: {hits(r['event'])}")
        if r["tk"] in state and ("target" in state[r["tk"]] or (not SHOW_TW_RATING and "rating" in state[r["tk"]])):
            problems.append(f"{r['tk']}: state leaks valuation")
    tw_folders = {models[r["tk"]]["folder"] for r in tw_rows if r["tk"] in models}
    for f in tw_folders:
        if f in mirrors:
            problems.append(f"model mirror for Taiwan folder {f}")
    for name, body in posts.items():
        for r in tw_rows:
            for line in body.splitlines():
                if r["name"] in line and hits(line):
                    problems.append(f"post {name}: {r['name']} line {hits(line)}")
    if problems:
        sys.exit("STOP — Taiwan target-price guard failed:\n  " + "\n  ".join(problems))

    # ---- write ----
    shutil.rmtree(SITE / "stocks", ignore_errors=True)
    for rel, body in out.items():
        p = SITE / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    mdir = SITE / "models"
    for old in mdir.glob("*.html"):
        old.unlink()
    for folder, src in mirrors.items():
        shutil.copyfile(src, mdir / f"{folder}.html")
    (mdir / "manifest.json").write_text(json.dumps({f: str(s.relative_to(cm)) for f, s in mirrors.items()},
                                                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"coverage {len(rows)} (Taiwan {len(tw_rows)}), pages {len(pages)}, models mirrored {len(mirrors)}, "
          f"posts {list(posts)}, changes: " + ", ".join(f"{k} {len(v)}" for k, v in changes.items()))


def diff(rows, prev, today):
    ch = {"new": [], "rating": [], "target": [], "model": [], "event": []}
    if not prev:
        return ch
    since = (today - dt.timedelta(days=NEW_DAYS)).isoformat()
    for r in rows:
        o = prev.get(r["tk"])
        if o is None:
            ch["new"].append(r); continue
        if r["rating"] and o.get("rating") and r["rating"] != o["rating"]:
            ch["rating"].append((r, o["rating"]))
        if r["target"] and o.get("target") and abs(r["target"] / o["target"] - 1) >= 0.03:
            ch["target"].append((r, o["target"]))
        if r["model_ver"] and r["model_ver"] != o.get("model_ver"):
            ch["model"].append((r, o.get("model_ver")))
        if r["event"] and r["event"] != o.get("event") and (r["event_date"] or "") >= since:
            ch["event"].append(r)
    return ch


# ---------------- pages ----------------

CSS = """<style>
.cov-table{font-size:14px;width:100%} .cov-table td,.cov-table th{padding:6px 8px;vertical-align:top}
.cov-layer{margin-top:28px} .cov-note{font-size:14px;color:#828282}
.sv{border-bottom:1px dotted #999;cursor:help} .sm{font-size:9px;color:#999;cursor:help;vertical-align:super;line-height:0}
.ptbl{overflow-x:auto} .ptbl table{font-size:13px}
.kpi{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 20px} .kpi div{border:1px solid #e8e8e8;border-radius:4px;padding:8px 12px;min-width:120px}
.kpi b{display:block;font-size:18px} .kpi span{font-size:12px;color:#828282}
</style>"""


def front(title, permalink, lang, alt):
    return f"---\nlayout: page\ntitle: \"{title}\"\npermalink: {permalink}\nlang: {lang}\nalt: {alt}\n---\n"


def table_page(cov, lang):
    zh = lang == "zh"
    head = front("個股" if zh else "Coverage", "/zh/coverage/" if zh else "/coverage/", lang,
                 "/coverage/" if zh else "/zh/coverage/")
    intro = ("本頁列出 AI 算力投資地圖涵蓋的個股，每週更新一次，數字取自各公司的個股模型。台股只列公司資料，不列目標價與評等。"
             if zh else
             "Companies covered by the AI Compute Investment Map, refreshed weekly from each company's model. "
             "Taiwan-listed companies show company information only, without target price or rating. Company pages are in Chinese.")
    if cov["show_tw_rating"]:
        intro = intro.replace("不列目標價與評等", "不列目標價").replace("without target price or rating", "without target price")
    out = [head, CSS, f"<p>{intro}</p>",
           f'<p class="cov-note">{"更新" if zh else "Updated"} {cov["updated"]} · '
           f'{"地圖版本" if zh else "Map version"} {cov["map_version"]} · {"價格日" if zh else "Prices"}: {html.escape(cov["price_note"] or "")}</p>']
    by = {}
    for r in cov["items"]:
        by.setdefault(r["layer"], []).append(r)
    cols = (["公司", "次產業", "評等", "現價", "目標價", "上檔空間", "悲觀情境價", "收支關卡", "模型"] if zh else
            ["Company", "Segment", "Rating", "Price", "Target", "Upside", "Pessimistic case", "Funding check", "Model"])
    for layer in sorted(by, key=lambda l: LAYER_ORDER.index(l) if l in LAYER_ORDER else 9):
        out.append(f'<h2 class="cov-layer">{html.escape(layer if zh else LAYER_EN.get(layer, layer))}</h2>')
        out.append('<div class="ptbl"><table class="cov-table"><thead><tr>' + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead><tbody>")
        for r in by[layer]:
            name = html.escape(r["name"])
            link = f'<a href="{{{{ \'/stocks/{r["slug"]}/\' | relative_url }}}}">{name}</a>' if r["has_profile"] else name
            badge = f' <span data-new="{r["new_date"]}"></span>' if r["new_date"] else ""
            rating = (r["rating"] if zh else r["rating_en"]) if r["rating"] else ("台股不列" if (zh and r["tw"]) else "—")
            mlink = (f'<a href="{{{{ \'{r["model_url"]}\' | relative_url }}}}">{r["model_ver"] or ""}</a>' if r["model_url"]
                     else (r["model_ver"] or "—") + ("" if not r["tw"] else (" (不公開)" if zh else " (not public)")))
            cells = [link + badge, html.escape(r["seg"] or ""), rating,
                     fmt_px(r["price"], r["ccy"]), fmt_px(r["target"], r["ccy"]), fmt_pct(r["upside"]),
                     fmt_px(r["bear"], r["ccy"]), html.escape(r["gate"] or "—"), mlink]
            out.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
        out.append("</tbody></table></div>")
    out.append('<p class="cov-note">' + ("研究整理，非投資建議。目標價為個股模型加權目標價（約 12 個月）；悲觀情境價為悲觀情境 DCF。"
                                         if zh else
                                         "Research notes, not investment advice. Target is the model's weighted target (about 12 months); "
                                         "pessimistic case is the downside-scenario DCF.") + "</p>")
    return "\n".join(out) + "\n"


def page_html(r, prof, tw):
    pm = prof["meta"]
    head = front(f'{r["name"]}（{r["tk"]}）', f'/stocks/{r["slug"]}/', "zh", "/map/")
    out = [head, CSS]
    if r["new_date"]:
        out.append(f'<p class="cov-note">更新 {r["new_date"]} <span data-new="{r["new_date"]}"></span></p>')
    out.append(f'<p>{hover(sanitize_tw(prof["oneliner"]) if tw else prof["oneliner"])}</p>')
    facts = [("上市", pm.get("listing")), ("總部", pm.get("hq")), ("層級", r["layer"]), ("次產業", r["seg"]),
             ("模型版本", f'{r["model_ver"]}（{r["model_date"]}）' if r["model_ver"] else None)]
    out.append("<p>" + "<br>".join(f"<b>{k}</b>：{hover(v)}" for k, v in facts if v) + "</p>")
    if not tw:
        out.append('<div class="kpi">' + "".join(
            f"<div><span>{k}</span><b>{v}</b></div>" for k, v in [
                ("評等", r["rating"] or "—"), ("現價", fmt_px(r["price"], r["ccy"])),
                ("目標價", fmt_px(r["target"], r["ccy"])), ("上檔空間", fmt_pct(r["upside"])),
                ("悲觀情境價", fmt_px(r["bear"], r["ccy"])), ("收支關卡", r["gate"] or "—")]) + "</div>")
        if r["model_url"]:
            out.append(f'<p><a href="{{{{ \'{r["model_url"]}\' | relative_url }}}}">開啟完整個股模型</a></p>')
    else:
        if r["rating"]:
            out.append(f'<p><b>評等</b>：{r["rating"]}</p>')
        out.append('<p class="cov-note">台股只列公司資料。</p>')
    for sec, frag in prof["sections"].items():
        if sec == "來源":
            continue
        frag = sanitize_tw(frag) if tw else frag
        if not strip_tags(frag).strip():
            continue
        out.append(f"<h2>{html.escape(sec)}</h2>\n{hover(frag)}")
    out.append(f'<p class="cov-note">資料日 {pm.get("asof", "")}。數字出處：滑鼠停在虛線底數字或 ⓘ 上即顯示。'
               f'研究整理，非投資建議。<a href="{{{{ \'/zh/map/\' | relative_url }}}}">回 AI 算力投資地圖</a></p>')
    return "\n".join(out) + "\n"


# ---------------- weekly note ----------------

def weekly_posts(cov, ch, today, first):
    now = dt.datetime.now(TPE) - dt.timedelta(minutes=5)
    stamp = f"{today.isoformat()} {now.strftime('%H:%M:%S') if now.date() == today else '09:00:00'} +0800"
    rows = cov["items"]
    url_zh = f"/zh/writing/{today:%Y/%m}/coverage-weekly/"
    url_en = f"/writing/{today:%Y/%m}/coverage-weekly/"

    def link(r, zh):
        return f'[{r["name"]}]({{{{ \'/stocks/{r["slug"]}/\' | relative_url }}}})' if r["has_profile"] else r["name"]

    def tline(r, zh):
        if r["tw"]:
            return f"- {link(r, zh)}（台股）" if zh else f"- {link(r, zh)} (Taiwan-listed)"
        rt = r["rating"] if zh else r["rating_en"]
        return (f"- {link(r, zh)}：{rt or '—'}，目標價 {fmt_px(r['target'], r['ccy'])}（{fmt_pct(r['upside'])}）" if zh else
                f"- {link(r, zh)}: {rt or '—'}, target {fmt_px(r['target'], r['ccy'])} ({fmt_pct(r['upside'])})")

    posts = {}
    for zh in (True, False):
        L = []
        n_tw = sum(r["tw"] for r in rows)
        if zh:
            title = f"個股週報 {today:%Y-%m-%d}"
            L.append(f"本週個股總表涵蓋 {len(rows)} 家公司（其中台股 {n_tw} 家），資料取自 AI 算力投資地圖 {cov['map_version']}。"
                     f"完整清單見[個股總表]({{{{ '/zh/coverage/' | relative_url }}}})。台股只列公司資料，不列目標價。")
        else:
            title = f"Coverage weekly, {today:%Y-%m-%d}"
            L.append(f"This week's coverage list has {len(rows)} companies ({n_tw} Taiwan-listed), taken from the AI Compute "
                     f"Investment Map {cov['map_version']}. Full list: [Coverage]({{{{ '/coverage/' | relative_url }}}}). "
                     "Taiwan-listed companies show company information only, without target price. Company pages are in Chinese.")
        if first:
            L.append("\n## " + ("首次上線：評等分布" if zh else "First edition: rating distribution"))
            dist = {}
            for r in rows:
                if r["rating"]:
                    k = r["rating"] if zh else r["rating_en"]
                    dist[k] = dist.get(k, 0) + 1
            L.append("\n".join(f"- {k}：{v} 家" if zh else f"- {k}: {v}" for k, v in dist.items()))
            hi = sorted([r for r in rows if r["upside"] is not None], key=lambda r: -r["upside"])
            L.append("\n## " + ("海外個股上檔空間最大五家" if zh else "Largest upside, non-Taiwan"))
            L.append("\n".join(tline(r, zh) for r in hi[:5]))
            L.append("\n## " + ("海外個股上檔空間最小五家" if zh else "Smallest upside, non-Taiwan"))
            L.append("\n".join(tline(r, zh) for r in hi[-5:][::-1]))
        else:
            sec = [("新增個股" if zh else "Added", [tline(r, zh) for r in ch["new"]]),
                   ("評等變動" if zh else "Rating changes",
                    [f"- {link(r, zh)}：{o} → {r['rating']}" if zh else f"- {link(r, zh)}: {RATING_EN.get(o, o)} → {r['rating_en']}"
                     for r, o in ch["rating"]]),
                   ("目標價變動 3% 以上（海外）" if zh else "Target changes of 3% or more (non-Taiwan)",
                    [f"- {link(r, zh)}：{fmt_px(o, r['ccy'])} → {fmt_px(r['target'], r['ccy'])}" for r, o in ch["target"]]),
                   ("模型更新" if zh else "Model updates",
                    [f"- {link(r, zh)}：{o or '—'} → {r['model_ver']}" for r, o in ch["model"]]),
                   ("近期重大事件" if zh else "Recent events (in Chinese)",
                    [f"- {link(r, zh)}：{r['event']}" for r in ch["event"]])]
            any_ = False
            for h, items in sec:
                if items:
                    any_ = True
                    L.append(f"\n## {h}\n" + "\n".join(items))
            if not any_:
                L.append("\n" + ("本週個股資料沒有變動。" if zh else "No changes in company data this week."))
        L.append("\n" + ("研究整理，非投資建議。" if zh else "Research notes, not investment advice."))
        fm = (f"---\nlayout: post\ntitle: \"{title}\"\ndate: {stamp}\nlang: {'zh' if zh else 'en'}\n"
              f"alt: {url_en if zh else url_zh}\npermalink: {url_zh if zh else url_en}\n---\n\n")
        posts[f"{today.isoformat()}-coverage-weekly{'-zh' if zh else ''}.md"] = fm + "\n".join(L) + "\n"
    return posts


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("company_models", type=Path)
    ap.add_argument("--date", help="run date YYYY-MM-DD (Asia/Taipei); default today")
    a = ap.parse_args()
    day = dt.date.fromisoformat(a.date) if a.date else dt.datetime.now(TPE).date()
    build(a.company_models, day)
