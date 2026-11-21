"""Charts for the 2026-11-21 extra essay on the 20 November proof claims (zh and en).

Writes inline SVG files to _includes/charts/2026-11-21/<name>-<lang>.svg.
Unlike the weekly essays, the figures here come from public reporting, not from the models:
  - Timeline, 10,000 agents / 88 hours, Codex and authorship dispute: lilting.ch timeline of
    the September Navier-Stokes dispute (Buckmaster's and OpenAI's statements)
  - Alpöge note (Oct 6 start, Nov 15 key steps, 14-part Lean archive, >250,000 pages unpublished),
    Clay prize rules, "hundreds" of conditional results: DataCamp, 2026-11-20
  - Compile confirmed (Sutherland and others), Masullo 12 years: TechCrunch, 2026-11-20
  - Statement is GRH (Glazer): OfficeChai, 2026-11-20
  - Share of zeta zeros proven on the critical line 41.6% -> 67.2% (Anthropic, August):
    as recounted by Nacionale / Superpower Daily
  - Navier-Stokes papers (79 pages; ~2,270 Lean files, 600,000 lines; certificate unreleased): OfficeChai
  - Anthropic first trading day 2026-11-19: Anthropic pricing announcement
Derived here: Oct 6 -> Nov 15 = 40 days; 88 hours = 3.7 days; 12 years = 4,383 days;
2 years = 730 days; 1859 -> 2026 = 167 years = 60,997 days.

Run: python3 tools/charts_20261121.py
"""
import math
from pathlib import Path

from charts_20261114 import (AQUA, AXIS, BLUE, GRID, INK, INK2, MUTED, ORANGE, YELLOW,
                             esc, flow, hbars, svg, text)

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "_includes/charts/2026-11-21"
GREY = "#a9a79f"


def timeline(rows, legend, label):
    """rows: (date, color, line1, line2)."""
    W, rowh, top = 680, 44, 40
    H = top + rowh * len(rows) + 6
    o = []
    x = 20
    for name, col in legend:
        o.append(f'<circle cx="{x + 6}" cy="14" r="6" fill="{col}"/>')
        o.append(text(x + 18, 18, name, 12, INK2))
        x += 30 + len(name) * (12.5 if ord(name[0]) > 255 else 6.8)
    o.append(f'<line x1="104" x2="104" y1="{top}" y2="{H - 26}" stroke="{AXIS}" stroke-width="2"/>')
    for i, (d, col, a, b) in enumerate(rows):
        y = top + i * rowh + 10
        o.append(text(88, y + 4, d, 12, INK, "end", 600))
        o.append(f'<circle cx="104" cy="{y}" r="6.5" fill="{col}" stroke="#fff" stroke-width="2"><title>{esc(d)} {esc(a)}</title></circle>')
        o.append(text(122, y + 4, a, 12.5, INK, "start", 600))
        if b:
            o.append(text(122, y + 20, b, 11.5, MUTED))
    return svg(W, H, "".join(o), label)


def logbars(rows, ticks, unit, label, l=250):
    """rows: (name, days, color, value label). ticks: (days, caption)."""
    W, r, t, rowh = 680, 96, 14, 38
    H = t + rowh * len(rows) + 50
    lo, hi = math.log10(1), math.log10(100000)
    sx = lambda v: l + (math.log10(v) - lo) / (hi - lo) * (W - l - r)
    o = []
    for g, cap in ticks:
        o.append(f'<line x1="{sx(g):.1f}" x2="{sx(g):.1f}" y1="{t}" y2="{t + rowh * len(rows)}" stroke="{GRID}"/>')
        o.append(text(sx(g), t + rowh * len(rows) + 16, cap, 11, MUTED, "middle"))
    for i, (name, v, col, lab) in enumerate(rows):
        y = t + 7 + i * rowh
        o.append(text(l - 10, y + 17, name, 12, INK2, "end"))
        o.append(f'<rect x="{sx(1):.1f}" y="{y}" width="{max(sx(v) - sx(1), 2):.1f}" height="24" rx="3" fill="{col}"><title>{esc(name)}: {esc(lab)}</title></rect>')
        o.append(text(sx(v) + 6, y + 17, lab, 12, INK, "start", 600))
    o.append(text(l, H - 8, unit, 11.5, MUTED))
    return svg(W, H, "".join(o), label)


def matrix(cols, label):
    """cols: (heading, sub, fill, [lines]). Three stacked-text columns."""
    W, gap, top = 680, 10, 8
    cw = (W - 2 * gap) / 3
    n = max(len(c[3]) for c in cols)
    H = top + 54 + n * 19 + 16
    o = []
    for i, (head, sub, fill, lines) in enumerate(cols):
        x = i * (cw + gap)
        o.append(f'<rect x="{x:.1f}" y="{top}" width="{cw:.1f}" height="{H - top - 4}" rx="6" fill="{fill}" stroke="{AXIS}"/>')
        o.append(text(x + 12, top + 22, head, 13.5, INK, "start", 700))
        o.append(text(x + 12, top + 39, sub, 11, MUTED))
        for k, s in enumerate(lines):
            bold = s.startswith("*")
            o.append(text(x + 12, top + 64 + k * 19, s.lstrip("*"), 12, INK if bold else INK2, "start", 600 if bold else 400))
    return svg(W, H, "".join(o), label)


T = {
 "zh": dict(
  tl_legend=[("Alpöge／Anthropic", BLUE), ("OpenAI", ORANGE), ("學界", AQUA), ("市場", YELLOW)],
  tl=[("7/19", BLUE, "Alpöge 用 Claude 提出 Jacobian 猜想的反例", ""),
      ("8 月", BLUE, "Claude 把「已證明在臨界線上的零點比例」從 41.6% 推到 67.2%", "當時 Anthropic 自己說這不是黎曼猜想的證明"),
      ("8/15", BLUE, "Buckmaster 與 Alpöge 得到有外力的 Euler 等爆破結果", "依 Buckmaster 的聲明；尚未公開"),
      ("9/5", ORANGE, "OpenAI 約 1 萬個 agent 跑 88 小時，得到有外力的納維-斯托克斯證明", ""),
      ("9/7", BLUE, "Buckmaster 與 Alpöge 公開三篇有外力結果，並發表聲明", ""),
      ("9/8", ORANGE, "OpenAI 對外公布；雙方對「誰先、誰看過誰的草稿」說法不一", ""),
      ("9/11", AQUA, "25 位菲爾茲獎得主聲明：AI 公司與數學界的目標嚴重錯位", ""),
      ("10/6", BLUE, "Alpöge 開始這一輪與 Claude 的合作", ""),
      ("11/15", BLUE, "他的說明把幾個關鍵步驟標在這一天", ""),
      ("11/19", YELLOW, "Anthropic 在那斯達克掛牌", ""),
      ("11/20", BLUE, "同一天：黎曼猜想（Lean）與無外力納維-斯托克斯兩份宣稱", ""),
      ("11/20", AQUA, "幾小時後：Masullo 的純人類廣義黎曼猜想草稿公開", "")],
  tl_label="2026 年 7 月到 11 月的事件時間線",
  gate=[["第一關", "程式碼編得過", "多位數學家回報通過"],
        ["第二關", "命題就是黎曼猜想", "有人確認是廣義版"],
        ["第三關", "公理稽核、人能讀懂", "進行中"],
        ["克雷認定", "發表後至少兩年", "尚未開始計時"]],
  gate_cap=["", "", ""],
  gate_label="黎曼猜想 Lean 證明的驗證關卡",
  spd=[("OpenAI 有外力版：約 1 萬個 agent", 88 / 24, ORANGE, "88 小時"),
       ("Alpöge × Claude：10/6 到 11/15", 40, BLUE, "最多約 40 天"),
       ("克雷獎規則：發表後的最短等待", 730, GREY, "至少 2 年"),
       ("Masullo 的純人類草稿", 4383, AQUA, "12 年"),
       ("黎曼猜想提出至今", 60997, GREY, "167 年")],
  spd_ticks=[(1, "1 天"), (10, "10 天"), (100, "100 天"), (1000, "約 3 年"), (10000, "約 27 年"), (100000, "約 274 年")],
  spd_unit="時間（對數刻度，每一格是 10 倍）；天數為我依報導日期換算",
  spd_label="產出證明與驗證所需時間的比較",
  zero=[("8 月以前的紀錄", 41.6, GREY), ("8 月：Claude（Lean 驗證）", 67.2, BLUE), ("11/20 的宣稱（未確認）", 100.0, YELLOW)],
  zero_unit="%；已證明落在臨界線上的 ζ 函數零點比例",
  zero_label="已證明在臨界線上的零點比例",
  m_math=[("短期", "未來三個月", "#e4effc",
           ["*驗證三件事", "Lean 獨立重建與公理稽核", "納維-斯托克斯數值憑證公開", "Masullo 草稿的公開審查", "", "*我會怎麼讀", "三份都當「宣稱」處理"]),
          ("中期", "三個月到兩年", "#fff4d6",
           ["*若成立", "數百個條件式定理轉為無條件", "Lean 變成交付證明的標準", "", "*不論成立與否", "署名與優先權的規則要重寫", "克雷的兩年等待開始計時"]),
          ("長期", "兩年以上", "#eef0ec",
           ["*工作內容移動", "從搶先證出來", "移到挑問題、讀懂、講清楚", "", "*風險", "沒有人讀得懂的定理越積越多", "後人難以在上面繼續蓋"])],
  m_math_label="對數學的短中長期影響",
  m_ai=[("短期", "未來三個月", "#e4effc",
         ["*展示競賽升溫", "各家拿難題當模型的廣告", "公告都是利害關係方的說法", "", "*算力", "長時間、多 agent 的推論", "token 用量未揭露，無法換算"]),
        ("中期", "三個月到兩年", "#fff4d6",
         ["*生成加形式驗證往外擴", "軟體正確性、晶片設計驗證", "（我的推論，尚無數據）", "", "*資料治理", "未公開的研究有沒有進訓練", "會變成企業合約的條款"]),
        ("長期", "兩年以上", "#eef0ec",
         ["*AI 成為研究的產出者", "但數學的驗證成本最低", "藥物、材料仍卡在實驗", "", "*資安", "不會因此破解 RSA", "真正的威脅仍是量子電腦"])],
  m_ai_label="對 AI 科技的短中長期影響",
 ),
 "en": dict(
  tl_legend=[("Alpöge / Anthropic", BLUE), ("OpenAI", ORANGE), ("Academia", AQUA), ("Market", YELLOW)],
  tl=[("Jul 19", BLUE, "Alpöge presents a Jacobian conjecture counterexample found with Claude", ""),
      ("Aug", BLUE, "Claude lifts the proven share of zeros on the critical line, 41.6% to 67.2%", "Anthropic said then that this was not a proof of the hypothesis"),
      ("Aug 15", BLUE, "Buckmaster and Alpöge obtain forced blowup results (Euler and others)", "Per Buckmaster's statement; unpublished at the time"),
      ("Sep 5", ORANGE, "About 10,000 OpenAI agents reach a forced Navier-Stokes proof in 88 hours", ""),
      ("Sep 7", BLUE, "Buckmaster and Alpöge post three forced results and a statement", ""),
      ("Sep 8", ORANGE, "OpenAI announces; the two sides dispute who knew what, and when", ""),
      ("Sep 11", AQUA, "25 Fields medalists: AI labs and mathematics are severely misaligned", ""),
      ("Oct 6", BLUE, "Alpöge starts this round of work with Claude", ""),
      ("Nov 15", BLUE, "His note dates several key steps to this day", ""),
      ("Nov 19", YELLOW, "Anthropic starts trading on Nasdaq", ""),
      ("Nov 20", BLUE, "Same day: Riemann (Lean) and unforced Navier-Stokes claims", ""),
      ("Nov 20", AQUA, "Hours later: Masullo's all-human GRH draft goes public", "")],
  tl_label="Timeline, July to November 2026",
  gate=[["Gate 1", "The code compiles", "Reported by several"],
        ["Gate 2", "Statement is RH", "Confirmed as GRH"],
        ["Gate 3", "Axioms; human reading", "In progress"],
        ["Clay", "2+ years after print", "Clock not started"]],
  gate_label="Verification gates for the Lean proof of the Riemann hypothesis",
  spd=[("OpenAI forced proof: ~10,000 agents", 88 / 24, ORANGE, "88 hours"),
       ("Alpöge × Claude: Oct 6 to Nov 15", 40, BLUE, "40 days at most"),
       ("Clay rules: minimum wait after publication", 730, GREY, "2 years or more"),
       ("Masullo's all-human draft", 4383, AQUA, "12 years"),
       ("Since Riemann posed it", 60997, GREY, "167 years")],
  spd_ticks=[(1, "1 day"), (10, "10 days"), (100, "100 days"), (1000, "~3 yrs"), (10000, "~27 yrs"), (100000, "~274 yrs")],
  spd_unit="Log scale (each step is 10x); my day counts from reported dates",
  spd_label="Time to produce a proof versus time to verify it",
  zero=[("Record before August", 41.6, GREY), ("August: Claude (Lean-checked)", 67.2, BLUE), ("Nov 20 claim (unconfirmed)", 100.0, YELLOW)],
  zero_unit="%; share of zeta zeros proven to lie on the critical line",
  zero_label="Share of zeros proven on the critical line",
  m_math=[("Short term", "Next three months", "#e4effc",
           ["*Three checks", "Independent Lean rebuild, axioms", "Navier-Stokes certificate out", "Open review of Masullo's draft", "", "*How I read it", "All three remain claims"]),
          ("Medium term", "Three months to two years", "#fff4d6",
           ["*If it holds", "Hundreds of conditional results", "become unconditional", "Lean becomes the delivery norm", "", "*Either way", "Credit and priority rules change"]),
          ("Long term", "Beyond two years", "#eef0ec",
           ["*The work moves", "From proving it first", "to choosing, digesting, explaining", "", "*The risk", "Theorems nobody can read pile up", "and are hard to build on"])],
  m_math_label="Short, medium and long-term effects on mathematics",
  m_ai=[("Short term", "Next three months", "#e4effc",
         ["*The showcase race heats up", "Hard problems as model adverts", "Read announcements as interested", "", "*Compute", "Long multi-agent inference runs", "Token use undisclosed"]),
        ("Medium term", "Three months to two years", "#fff4d6",
         ["*Generate, then formally verify", "Software and chip verification", "(my inference, no data yet)", "", "*Data governance", "Did unpublished work reach", "training? A contract term now"]),
        ("Long term", "Beyond two years", "#eef0ec",
         ["*AI as a producer of research", "But math is cheapest to verify", "Drugs, materials still need labs", "", "*Security", "This does not break RSA", "Quantum remains the threat"])],
  m_ai_label="Short, medium and long-term effects on AI technology",
 ),
}


def gates(g, label):
    fills = [("#d9f2e6", INK), ("#d9f2e6", INK), ("#fff4d6", INK), ("#eef0ec", INK)]
    w, gap, y, h = 152, 24, 30, 84
    boxes, arrows = [], []
    for i, lines in enumerate(g):
        x = i * (w + gap)
        boxes.append((x, y, w, h, fills[i][0], fills[i][1], lines))
        if i:
            arrows.append((x - gap + 2, y + h / 2, x - 2, y + h / 2, ""))
    return flow(boxes, arrows, label, W=680, H=140)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for lang, t in T.items():
        files = {
            "timeline": timeline(t["tl"], t["tl_legend"], t["tl_label"]),
            "gates": gates(t["gate"], t["gate_label"]),
            "speed": logbars(t["spd"], t["spd_ticks"], t["spd_unit"], t["spd_label"], l=250 if lang == "zh" else 262),
            "zeros": hbars(t["zero"], 0, 100, [0, 25, 50, 75, 100], t["zero_unit"], t["zero_label"], l=190, fmt="{:.1f}"),
            "impact-math": matrix(t["m_math"], t["m_math_label"]),
            "impact-ai": matrix(t["m_ai"], t["m_ai_label"]),
        }
        for name, body in files.items():
            (OUT / f"{name}-{lang}.svg").write_text(body, encoding="utf-8")
            n += 1
    print(n, "charts")


if __name__ == "__main__":
    build()
