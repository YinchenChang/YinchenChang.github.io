---
layout: page
title: 技術週讀
permalink: /tech-weekly/
lang: zh
description: 我每週挑三篇長期最可能改變 AI 經濟學的論文或技術報告，寫成白話預讀版，逐段標出原文位置，方便對照原文讀。
---
{%- assign issues = site.pages | where_exp: "p", "p.path contains 'tech-weekly/issues/'" | sort: "date" | reverse -%}

<p class="lede">我每週六上午從一週的 AI 論文、技術報告和系統文件裡，挑出長期最可能改變 AI 經濟學的三篇，寫成白話的預讀版。每一段都標出對應的原文章節或圖表，讀完預讀版，再回原文對照。</p>

{% if issues.size > 0 %}{% assign latest = issues | first %}
<div class="section-label">最新一期</div>
<div class="cards" style="grid-template-columns:1fr">
  <a class="card" href="{{ latest.url | relative_url }}"><b>{{ latest.title | escape }}</b><span>{{ latest.date | date: "%Y-%m-%d" }}｜{{ latest.description | escape }}</span></a>
</div>
{% else %}
<div class="site-notice"><b>即將出刊</b>第一期 2026-11-28（六）上午上線。</div>
{% endif %}

## 我為什麼每週讀這些

我認為要比市場更早看出 AI 投資的變化，前提是自己讀得懂技術。模型能不能更便宜地推論、一顆晶片能多產出多少 token，最後都會變成每 GW 的成本與營收；這些數字我不想只聽公司或賣方怎麼說。所以我把讀論文變成固定的功課，每週一次，一次大約一個小時。

## 每期怎麼讀

<div class="keypoints" markdown="1">
**每期的結構**

- **本週主線：** 三篇之間的關聯，或這週最值得記住的一件事。
- **精讀一篇，先猜再讀：** 開頭一兩題「讀前先猜」，答案摺疊；接著講背景、方法、結果、限制，關鍵數字附原文表或圖的編號。
- **對產業的含義：** 影響需求、成本、硬體組成，還是誰拿到價值；只講方向與量級區間，不給個股建議。
- **速讀兩篇：** 一句話、方法三句、關鍵數字、含義兩三句。
- **原文對照與名詞小抄：** 固定版本的原文連結與逐段位置；開放授權的論文才並列原文段落。
</div>

## 我怎麼選題

我不追熱度。每篇候選依四項各給 0–3 分，再乘上新穎度、除以閱讀成本排序，取前三名。說白了，就是挑「最可能改變結論、又讀得完」的那幾篇。

| 評分項目 | 看什麼 |
|---|---|
| 算力需求與每 token 成本 | 訓練或推論效率、模型規模、記憶體與頻寬需求 |
| 能力前緣 | 推理、代理、長脈絡、多模態、機器人能做到什麼 |
| 硬體組成與價值分配 | HBM、網通、ASIC 與 GPU、電力 |
| 證據強度 | 有沒有開源、復現、獨立評測；只有作者自述的會標明 |

我最擔心的是選題偏誤：我挑的往往是符合自己既有看法的論文。所以每期會列出「其他候選」與沒選的理由，事後可以回頭檢查。

## 歷期

{% if issues.size > 0 %}
<ul class="post-index">
{%- for p in issues %}
  <li><time>{{ p.date | date: "%Y-%m-%d" }}</time><div><a href="{{ p.url | relative_url }}">{{ p.title | escape }}</a><p>{{ p.description | escape }}</p></div></li>
{%- endfor %}
</ul>
{% else %}
<p>第一期出刊後列在這裡。</p>
{% endif %}

*內容是我的技術閱讀整理，數字以原文為準；整理由 AI 代理協助完成並經另一個代理對照原文核對。不是投資建議。*
