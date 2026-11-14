---
layout: post
title: "The Valuation Says Buy CoreWeave. The Cash Flow Says No, and I'm Going With the Cash"
date: 2026-11-14 10:52:00 +0800
lang: en
alt: /zh/writing/2026/11/valuation-says-buy-cash-says-no/
permalink: /writing/2026/11/valuation-says-buy-cash-says-no/
description: "I rebuilt CoreWeave on the Oracle funding template this week. The valuation just clears the buy line, but five-year free cash flow sums to −US$95.7bn, so I added a funding gate to my ratings. Plus Oracle's reverse DCF, Anthropic's prospectus, a 15.8% EPS error I made on Supermicro, and a lower Meta target."
---

<p class="lede">The thing I cared about most this week: a company's valuation can say "buy" while its next five years of cash can't pay for what it is building. That is where CoreWeave landed after the rebuild. Peer multiples push it over the buy line, but my model has base-case free cash flow summing to −US$95.7bn over five years. My view is that the rating should listen to the cash in that situation, so I added a gate. The other updates this week circle the same question: where does the money come from, and is it enough?</p>

<div class="keypoints" markdown="1">
**This week**

- CoreWeave's new weighted target is US$76.20, +25.4% upside, just 0.4 points above the buy threshold. The DCF half is zero; all the value comes from peer multiples.
- I added a funding gate: if base-case FY2026–FY2030 free cash flow sums to less than zero, no buy rating, however good the valuation. CoreWeave is now "underfunded".
- Oracle: to justify the US$115.16 share price, long contracts need US$13.99m of revenue per MW per year, above the top of my plausible range (US$12.72m).
- Anthropic's prospectus lifts my model's cash low point from US$40.2bn to US$142.2bn, but at the US$74 midpoint of the offer range my rating is only neutral.
- I had overstated Supermicro's EPS by 15.8%. Fixed this week.
</div>

## 1. CoreWeave's "buy" comes from peer multiples; the DCF half is zero

The short version: CoreWeave moved from short to a valuation buy because of the method and the peer multiples, not because its economics per MW got better.

This week I rebuilt CoreWeave on the "funding" template I first built for Oracle: revenue, capex, borrowing and equity raised year by year, then valued half by DCF and half by peer multiples. Here is how the old US$25.51 became the new US$76.20:

{% include charts/2026-11-14/crwv-bridge-en.svg %}
<p class="chart-note">CoreWeave target, v4.13 to v5.0, in five sequential steps (they sum to the total change of +50.69). Green raises the target, orange lowers it.</p>

Two things to take from this chart. First, the two biggest steps are the method (+41.68) and the peers (+18.44), together +60.12. Second, the only step that comes from the business itself, replacing my estimates with third-quarter actuals, is −11.33. The main reason is that the company reported Q3 borrowings of US$46.9bn and cash of US$4.1bn, so net debt was higher than I had estimated.

The DCF half (valuing future cash flows discounted back to today) is zero in all three scenarios, because enterprise value comes out negative. In my model, each extra gigawatt CoreWeave builds lowers DCF enterprise value: −US$37.4bn per GW between the base and bear cases. So US$76.20 is simply half of the peer-multiple value of US$152.41. The peer measure is enterprise value over next-twelve-month EBITDA (operating profit before depreciation). The median is 7.86x, which happens to be Oracle; at 7.84x the rating falls back to neutral.

I need to own a mistake here. Earlier rounds this week had the peer median at 7.16x. **I got it wrong because** I paired Nebius's net debt including convertibles with its basic share count, and used IREN's June net debt. **Now** both use their 30 September filings, the median is 7.86x, and the target rises from US$65.08 to US$76.20. When fixing one input moves the same company from neutral to buy, that tells you how fragile the buy is.

## 2. So I added a funding gate: negative five-year cash, no buy

The valuation rating is calculated as before, but the final recommendation has to pass one more check.

{% include charts/2026-11-14/gate-flow-en.svg %}
<p class="chart-note">How the funding gate works. It only blocks buy-or-better; it never changes a neutral or a short.</p>

CoreWeave fails it:

{% include charts/2026-11-14/crwv-fcf-en.svg %}
<p class="chart-note">Five-year free cash flow is negative in all three scenarios. The bull case is the most negative because the more it builds, the more it pays up front.</p>

To cover the US$75.7bn base-case gap, my model raises US$62.7bn of investment-grade debt, US$8.9bn of new equity and US$4.1bn of high-yield debt, for 29.0% cumulative dilution by end-2030 and net debt peaking at 4.58x EBITDA. As an analogy, think of a restaurant chain where every branch is full, but each new branch costs more up front than it earns back for years, so the faster it expands the shorter of cash it gets. The analogy breaks in one place: CoreWeave has long contracts, so its revenue is far more certain than a restaurant's. The real issue is price per MW against cost per MW.

Why let cash override the valuation? Both readings make sense. Peer multiples say the market will pay 7–9x EBITDA for this kind of company; cash flow says it needs outside money to get through the next five years. I take the more conservative side because the peer multiple ignores the capex needed to replace GPUs, which is exactly CoreWeave's biggest bill. The cost: if credit markets stay easy, I will miss part of a rally.

My weakest assumption is new contract pricing. On its earnings call the company said new 4–5 year contracts earn US$20–25m per MW per year; my base case is US$10.28m (FY2027). I have not seen that claim in a filing, so it is not in the base case. If all new capacity were priced at the midpoint of the company's claim, the weighted target would be US$360.57. Put simply, the valuation rests almost entirely on whether those new contract prices are real.

The map still shows this week's third-round figure of US$65.08, neutral. Once the next map build picks up v5.0.1, it will show "underfunded".

## 3. Oracle's share price needs contract prices above what I can accept

The funding template CoreWeave now uses was built on Oracle first this week, and Oracle also got a reverse DCF: instead of asking what it is worth, ask what the current price assumes. My conclusion: no single assumption within my plausible ranges supports US$115.16.

{% include charts/2026-11-14/orcl-plong-en.svg %}
<p class="chart-note">Oracle long-contract revenue per MW per year: my base case, the level needed for a neutral rating, the top of my plausible range, and what the current price implies. The yellow band is my sensitivity range.</p>

The closest driver is the long-contract price: the share price implies US$13.99m per MW per year, 10% above the US$12.72m top of my range. The others are further away: WACC would need to fall another 5.4 points, or non-AI margins rise 20.5 points; even cutting operating costs to zero only gets the target to US$96.0.

On funding, Oracle is in much better shape than CoreWeave. The company completed an equity and debt raise in early November worth about US$19.9bn net, and my base case needs only US$5.0bn more. But that depends on construction staying on time:

{% include charts/2026-11-14/orcl-stress-en.svg %}
<p class="chart-note">Longer delays and less customer funding mean more outside money. From a nine-month delay, the leverage cap uses up the investment-grade room, and the rest has to come from new equity and high-yield debt.</p>

What I am unsure about: the company does not split its roughly US$664bn of remaining performance obligations (RPO, contracted revenue not yet delivered) by business, so public data can neither confirm nor rule out a delivery bottleneck. Weighted target US$70.38, still short. As with CoreWeave, the question is whether price per MW covers the cost.

## 4. Anthropic's prospectus fixed the cash problem, not the valuation problem

The preliminary prospectus of 10 November gives an offer range of US$70–78 and net proceeds of about US$84.6bn from the IPO and a concurrent private placement (US$26.0bn, including US$10bn each from Google and NVIDIA). The company also reports run-rate revenue of about US$81bn as of 31 October.

With that in my model, the cash picture improves a lot: the low point of cash using only money already in hand rises from US$40.2bn to US$142.2bn, operating free cash flow turns positive in 2029 instead of 2030, and five-year outside funding need is zero. On funding, Anthropic is the opposite of CoreWeave.

The valuation is less comfortable:

{% include charts/2026-11-14/ant-val-en.svg %}
<p class="chart-note">Three valuation methods against the offer range. My weighted target is only 11.8% above the midpoint.</p>

The usual market approach, the unadjusted peer revenue multiple, gives US$153.44. But the peer median free-cash-flow margin is 29.8%, while I estimate Anthropic at 23.8% by 2030, so I scale the multiple by 0.799 to get US$111.06. The DCF is only US$54.37, and in the base case 91.5% of its value is terminal value after 2033; free cash flow is negative in 2027–2029. Half and half gives US$82.71, +11.8% against the US$74 midpoint: neutral.

What I am unsure about is the terminal value. It depends on a 2033 operating margin of about 21.9% holding up, and that figure is my estimate, not company guidance. For a company with no funding problem, the whole valuation question becomes how much it earns in the end.

## 5. I had overstated Supermicro's EPS by 15.8%

**Where I went wrong:** I took Supermicro's net income less preferred dividends and divided by diluted shares, getting first-quarter EPS of US$2.03. **Why:** I missed its mandatory convertible preferred. Those shares already share in earnings now (the two-class method) rather than only after conversion, which adds 130.7 million shares to the denominator; and after-tax interest on the convertible notes has to be added back to the numerator. **Now** I use the company's 10-Q method:

{% include charts/2026-11-14/smci-eps-en.svg %}
<p class="chart-note">Supermicro diluted EPS for 1Q FY27. Applied to first-quarter actuals, the corrected method matches the company's reported US$1.75.</p>

The valuation share count now also includes unvested RSUs and options. The map target falls from US$70.50 to US$67.01 against a price of US$27.08; the rating stays strong buy. The error doesn't change the conclusion, but it belongs to this week's theme: share counts and cash are unglamorous, and when you get them wrong the whole valuation drifts.

## 6. Other updates: Meta down US$66, Cerebras joins the map

Meta was rebuilt to the new standard this week, and its target falls from US$844.10 to US$778.44:

{% include charts/2026-11-14/meta-bridge-en.svg %}
<p class="chart-note">Meta target, step by step (full recalculation, added in order). Both big steps are about counting more honestly: shares and capacity actually in service.</p>

The two main cuts: adding 134.5 million unvested RSUs to the share count (−34.61), and reading Meta's own AI capacity from the data-center go-live schedule tracked in another of my models rather than inferring it from capex (−30.64). Capacity comes online more slowly than the money is spent, so the same capex delivers less benefit within the valuation window. At US$605.08 the upside is +28.7%, still buy, but only 3.7 points from the buy/neutral boundary.

Changes to overseas names on the map this week:

| Company | Rating | Map target (USD) | Price (USD) | What changed |
|---|---|---|---|---|
| CoreWeave | Short → Neutral | 25.51 → 65.08 | 60.77 | Funding template; v5.0.1 is 76.20 and underfunded, in the next map build |
| Astera Labs | Strong short → Short | 87.65 → 103.66 | 179.47 | High/low share paths for new products in scenarios; share count |
| Anthropic | New: Neutral | 82.71 | 74 (range midpoint) | Prospectus rolled in; first valuation |
| Cerebras | New: Neutral | 80.56 | 81.71 | New model; chip companies only as peers |
| NVIDIA | Buy (unchanged) | 267.15 → 254.26 | 181.60 | Fiscal and calendar years weighted by month |
| Meta | Buy (unchanged) | 844.10 → 778.44 | 605.08 | See above |
| Oracle | Short (unchanged) | 75.31 → 70.38 | 115.16 | New-debt rate and working capital |
| AMD | Short (unchanged) | 261.79 → 273.32 | 404.40 | Customer warrants vest with GW shipped |
| Supermicro | Strong buy (unchanged) | 70.50 → 67.01 | 27.08 | See section 5 |
| SpaceX | Strong short (unchanged) | 34.79 → 32.73 | 135.92 | Peers on one valuation date; RSUs and options in share count |

Under this site's rules, Taiwan-listed stocks show no rating or target.

## What to watch

- **CoreWeave's new contract prices.** The Q3 10-Q has been filed, and my model has not yet read in the debt-by-instrument detail, period-end share count or construction in progress. I will look for evidence of new contract pricing in the filing; if it shows revenue per MW per year really above US$20m, I will change my mind and put the company's figure in the base case.
- **Anthropic's pricing and first day of trading.** Media report trading from around 19 November; the final price has not been set. I will watch where it prices; if the market trades well above US$111, it is using the unadjusted peer multiple and I need to rethink my 0.799 haircut.
- **Oracle's construction schedule.** If the company discloses a delay of six months or more at its main sites, my stress table puts outside funding needs at US$12.3bn or more, and I will move the delay into the base case.

Data and models for every company are on the [AI Compute Investment Map]({{ '/map/' | relative_url }}).

<div class="sources" markdown="1">
**Market data sources**
- Anthropic expected trading date: FinanceFeeds, "Anthropic IPO Date: $70-$78 Price Range Set, Trading Reported From 19 November".
- CoreWeave Q3 10-Q: SEC EDGAR (crwv-20260930).
</div>

*All figures come from my own models (versions dated 8–14 November 2026: CoreWeave v5.0–v5.0.1, Oracle v0.5.0–v0.5.1, Anthropic v0.2.0, Meta v0.2.0, Supermicro v0.3.6; AI Investment Map v0.6.40). They are internal research, not an independent source; company figures are from filings, the prospectus and earnings calls, tagged and sourced on each model page. Research notes, not investment advice.*
