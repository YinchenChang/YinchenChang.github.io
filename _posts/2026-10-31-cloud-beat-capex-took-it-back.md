---
layout: post
title: "Cloud Beat My Models This Quarter; Capex Took the Gain Back"
date: 2026-10-31 12:10:00 +0800
lang: en
alt: /zh/writing/2026/10/cloud-beat-capex-took-it-back/
permalink: /writing/2026/10/cloud-beat-capex-took-it-back/
---

This was hyperscaler earnings week. Cloud at Microsoft, Alphabet and Amazon all came in ahead of my models, some by a lot. Yet none of the three target prices moved much: the good news was offset by higher capital spending in the same report, or by custom chips that turned out more expensive to own. I also caught two errors in my own models. Short notes below.

## Azure grew faster than guided, and free cash flow nearly vanished

Azure grew 48% year on year against guidance of 44–45%. After rolling the quarter in, Microsoft's model target went from US$385.56 to US$384.10, effectively unchanged. The reason is cash. This quarter the company gave only a calendar-2026 figure of about US$170bn and said spending will accelerate in the second half of its fiscal year; from that I estimate FY2027 capex (July 2026 to June 2027, including finance leases) at about US$204bn, which leaves only about US$11bn of free cash flow that year. The base case needs about US$8bn of new debt, and buybacks shrink by about US$44bn over two years. Management itself said FY27 free cash flow will be "positive" and that it will raise additional funding "when appropriate". The line that is growing fastest is the line that eats the most cash.

## Google Cloud doubled; five-year cash after dividends fell from +US$180bn to about zero

Google Cloud revenue was US$30.7bn, up 103%, 17.8% above the model's value for the quarter, at a 36.2% operating margin. Search was weaker than modeled: US$63.4bn, up 12%, 4.1% below. The two roughly cancel, and the target moved from US$258.70 to US$258.21.

What changed is funding. Management said 2027 capex will "increase significantly". Re-solving the AI build pace from guidance raises it by about half, and the model's FY2027 and FY2028 capex become US$290bn and US$317bn (consensus US$308bn and US$352bn). Five-year (FY2026–2030) free cash flow after dividends in the base case drops from +US$180bn to −US$0.6bn. Take the top or bottom of the 2026 capex guidance range and the sign flips.

## AWS beat too, but Trainium costs more to own than assumed

Amazon's third-quarter operating income was US$28.1bn, 19.9% above the model; AWS revenue was US$46.0bn, up 39%. Those two add US$7.39 to the target. In the same week my Tokenomics model set Trainium's holding cost per unit of compute at 0.61 times NVIDIA's VR200, which lowers revenue per MW and takes US$10.77 off. Net, the target went from US$215.58 to US$217.65.

On the bright side, Amazon's funding improved the most of the three: base-case five-year free cash flow after dividends rose from +US$19bn to +US$90bn, with no new debt needed in any scenario.

## Meta: newly modeled, cheapest on valuation, and the only one that needs to borrow

I built a Meta model for the first time this week. The weighted target is US$844.10, 37.8% above the 28 October close of US$612.49, the only Buy among the four. The funding check, however, shows new debt in two of three scenarios, including the base case, which adds about US$11.6bn in FY2028. A cheap valuation and a cash-flow gap are both true at once; I will track them together.

## My error, part one: treating contract prices as selling prices

For NAND in the fourth quarter, my model was 9.6% above SanDisk's revenue guidance and 21.5% above Kioxia's. The error was in the market layer. I grew the market with TrendForce's contract-price increase (+15% in the third quarter), but SK hynix and Kioxia both reported realized prices up in the mid-20s percent. The market was understated, so each company's share (actual revenue ÷ market) was overstated by about 8%, and multiplying the fourth quarter by the contract increase again counted the same price rise twice. Lesson: a research firm's contract price is a quote, not what the company actually collects.

## My error, part two: calendar years versus fiscal years

For Advantest's SoC testers, the model's FY2026 was ¥177bn below company guidance. Three causes: a stale market size (US$11.0bn; the company now says about US$11.5bn), 21% of the gap; a two-year-old self-estimated share of 66% where this year's actuals imply 71.4%, 39%; and the remaining 40% from treating a fiscal year as three quarters of a calendar year. FY2026 starts in April and skips the weakest quarter, January–March, so it is really 81% of the calendar year. After the three fixes the model is 2–4% above guidance, and the method itself stands.

## Anthropic's S-1: signed compute commitments are 40% larger than modeled

Anthropic's public S-1 (filed 26 October) lists compute commitments totaling about US$832bn. My model counts only about US$598bn of signed contracts, 28% less; contracts signed after June alone add US$245bn. The model's conclusion holds (revenue per GW below cost in 2026–2028, turning positive in 2029), but compute costs after 2027 are understated. Whether to add the new contracts to the base case is still open.

## What I am watching next

- Formal 2027 capex numbers, which neither company has given yet. Alphabet says details come on its fourth-quarter call (early 2027), and its five-year funding sits right at zero; Microsoft has given only about US$170bn for calendar 2026, with no full-year FY2027 figure.
- Fourth-quarter realized NAND prices, to test the corrected market layer.
- Whether adding Anthropic's new contracts pushes the break-even year per GW later.

Each company's page and model is on the [AI Compute Investment Map]({{ '/map/' | relative_url }}).

*All figures come from my own models (versions of 27–31 October 2026). They are internal research, not an independent source. Company figures are from filings and earnings calls, tagged and sourced on each model page. Not investment advice.*
