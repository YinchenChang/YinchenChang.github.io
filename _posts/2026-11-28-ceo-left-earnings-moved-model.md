---
layout: post
title: "Jensen Huang Resigned and Q3 Was Strong. I Let Only the Earnings Move My NVIDIA Model"
date: 2026-11-28 10:55:00 +0800
lang: en
alt: /zh/writing/2026/11/ceo-left-earnings-moved-model/
permalink: /writing/2026/11/ceo-left-earnings-moved-model/
description: "NVIDIA gave me two things this month: founder Jensen Huang stepped down as CEO, and Q3 results went into my model. I let the results lift my target from $300.62 to $316.02 and kept the CEO change in sensitivity only; even with three discounts at once, the target is $240.66. Separately, the sector fell 16% in a week while my targets fell 10%, and 11 overseas ratings drifted toward neutral."
---

<p class="lede">The thing I cared about most this week: within one month NVIDIA handed me a hard number and a soft event. The hard number is the third-quarter report. The soft event is founder Jensen Huang resigning as president, CEO and director on November 11. My rule was to let only evidence move the base case. The results went in, and my target rose from $300.62 to $316.02. For the CEO change I have no reliable parameters, so it lives in sensitivity analysis and the base case stays put. This post explains why I split it that way, what it costs, and a few related fixes from the week.</p>

<div class="keypoints" markdown="1">
**Key points**

- NVIDIA reported Q3 revenue of $115.8bn, data center $107.6bn. After rolling it in, my model's FY2027 EPS rose from 9.06 to 9.50 and the weighted target from $300.62 to $316.02.
- The CEO change sits in sensitivity only. With a 25%-retained premium, WACC +1pt and more conservative scenario weights all at once, the target is $240.66 (−23.8%), still close to twice the $125.53 close on Nov 20.
- Last week I said I'd keep Q3 as an out-of-sample test. This week it went into the model first. I've recorded what the test showed: with Q3, the gap between actuals and my industry-layer value sits somewhere between −9.7% and −23.9%, and the two readings can't say where.
- After moving to Nov 20 closes, the median share price across 51 overseas names fell 16.3% while my median target fell 9.8%. Eleven ratings changed, mostly from short toward neutral.
- Two small fixes: peer net debt no longer scales with share price, and Coherent's interest assumption now uses actuals. Microsoft is 1.8% away from flipping from Short to Neutral.
</div>

## 1. Q3 results pulled my NVIDIA target back up to $316.02

The results were good, and rolling them in recovered part of the value my target lost when peers fell.

First, what the company reported. These are NVIDIA's November figures, which I checked against the company press release on Nov 24:

| Item ($bn, except EPS) | Company-reported FY2027 Q3 |
|---|---|
| Revenue | 115.8 |
| Data center revenue | 107.6 (Q1 75.2, Q2 89.0) |
| Operating income | 77.5 |
| Net income | 65.3 |
| EPS (GAAP / non-GAAP, $) | 2.70 / 2.68 |
| Q4 revenue guidance | 130.0 ±3% |

After the roll-in, my model's FY2027 EPS goes from 9.06 to 9.50, the DCF target from $130.32 to $136.48, and the weighted target from $300.62 to $316.02. But the week's path was down first, then up:

{% include charts/2026-11-28/nvda-path-en.svg %}
<p class="chart-note">Two steps in NVIDIA's weighted target. The point is that the first step is bigger: lower peer prices took away $32.89, and the results put back $15.40.</p>

The first step was moving every model's share price and peer quotes to the Nov 20 close (section 4). Peers fell, so my comparables leg fell. The second step was the results. Put simply, NVIDIA's own numbers got better this week, but the market priced the whole group lower, and that mattered more. That's the thread through this post: what moved the base case, and why.

## 2. Jensen Huang resigned. I left the base case alone and priced three discounts

The CEO change is real, but I can't produce evidence for its effect on value, so it stays in sensitivity. Even with all three discounts at once, the rating is still Strong buy.

The event itself, per NVIDIA's 8-K and the Nov 12 press release: on Nov 11 the board accepted Jensen Huang's resignation as president, CEO and director, effective immediately. CFO Colette Kress is interim CEO while the board searches for a permanent one, and Harvey C. Jones becomes the company's first board chair.

The hard part is putting it into a model. I can think of three channels: the valuation premium the market gives NVIDIA shrinks, the discount rate (WACC, the rate that brings future cash flows back to today) goes up, or the odds of the optimistic scenario go down. None of the three has evidence behind it. There's no historical sample that tells me how much premium survives a founder leaving. So every parameter is labeled an assumption, and I look only at the range of outcomes:

{% include charts/2026-11-28/ceo-en.svg %}
<p class="chart-note">NVIDIA's weighted target under each case. The premium cases (orange) matter most, and even all three together (red) sit near twice the share price (grey).</p>

The 15/55/30 weights are the probabilities on the optimistic, base and conservative scenarios. "All three at once" means a 50%-retained premium, WACC +1pt and 15/55/30 weights; recalculating the whole model gives $240.66, 23.8% below base.

Two approaches are defensible here: pick a discount and put it in the base case, or leave the base case and show the range. I chose the second. A number with no evidence behind it, once in the base case, flows into the map, the rating and other models, and starts to look calculated. The cost is that my base case may be too high, and I accept that. My weakest assumption is that the valuation premium doesn't depend on who runs the company. If guidance weakens or senior people start leaving, I'll move the discount into the base case. Same thread as above: only evidence changes the base case.

## 3. I said I'd keep Q3 as a test. It went into the model first

My mistake was in process, not numbers. The test is used up, and I've kept the result from just before it was.

Last week I wrote that I was deliberately keeping NVIDIA's Q3 actuals out of every model so I could use them to test my industry-layer model. **Where I went wrong:** when Q3 was rolled into the stock model on Nov 24, nobody checked it against the holdout list. **Why:** the release-date field on that list was blank, so the update process didn't stop it. I caught it on Nov 25, formally released the holdout, and recorded the test result at that moment. **What changes:** Q3 is no longer out of sample, and I need a new test.

The test itself is simple. Take NVIDIA's reported data center revenue and compare it with what my industry-layer model implies for NVIDIA data center revenue in 2026: $476.4bn, a value set before I saw Q3 and left untouched. There are two readings:

{% include charts/2026-11-28/oos-en.svg %}
<p class="chart-note">How far actuals fall below my layer value. With Q3 added, one reading is past the threshold and one is inside it, and they are 14 points apart.</p>

- **Main reading:** cumulative actuals for three quarters, $271.8bn, against the layer value pro-rated by month, $357.3bn: 23.9% low.
- **Second reading:** latest quarter × 4 = $430.4bn against the full-year $476.4bn: 9.7% low, inside the ±15% threshold.

The verdict changed from "under reconciliation" to "timing boundary (reference)." I don't read that as good news. Part of the improvement in the second reading is a timing effect: in a year of quarter-on-quarter growth, the latest quarter times four will run above the annual average, while straight-line pro-rating in the main reading is biased the other way. These two readings can't tell me where between −9.7% and −23.9% the true gap is. Also, my industry-layer model hasn't taken in Q3 yet, so right now my two models give different verdicts on the same check. They'll line up only after I update the layer.

## 4. The sector fell 16% in a week and my targets fell 10%, so ratings drifted toward neutral

This week's rating changes came mostly from share prices, not fundamentals. Prices fell more than my targets, so a lot of shorts became neutral.

On Nov 21 I moved all 78 models to Nov 20 closes for both the stock and its peers. Consensus EPS, rates and operating assumptions stayed the same. Here's what happened:

{% include charts/2026-11-28/scatter-en.svg %}
<p class="chart-note">51 overseas names: one-week share price change across, my target change up. Most points sit above the diagonal, meaning targets fell less than prices.</p>

The median price fell 16.3% and the median target fell 9.8%. Why did targets fall at all? Part of each target comes from peer comparisons, and when peers fall, that part falls with them. The DCF part depends mainly on cash flows, and share price barely touches it. It's like valuing a house half on its own rental yield and half on what the house next door just sold for. If the neighbor's price drops 20%, the valuation drops about 10%. The analogy is loose in one way: a house has fixed halves, while the weights differ across my models, so each stock moves by a different amount.

The exceptions are Nebius and CoreWeave, whose targets fell 52.7% and 47.0%, more than their prices. My guess is that high net debt amplifies the change in peer multiples into equity value, but I haven't broken it down yet, so I'm not drawing a conclusion.

The 11 overseas names whose rating changed (Taiwan-listed stocks show no ratings or targets on this site):

| Company | Rating | Map target |
|---|---|---|
| Broadcom | Strong short → Short | $152.59 |
| Marvell | Strong short → Short | $62.08 |
| Astera Labs | Strong short → Short | $90.33 |
| Micron | Short → Neutral | $493.83 |
| Lumentum | Short → Neutral | $347.65 |
| Applied Materials | Short → Neutral | $227.84 |
| Lam Research | Short → Neutral | $142.13 |
| Dell | Short → Neutral | $217.02 |
| Advantest | Short → Neutral | ¥19,667.72 |
| ABB | Short → Neutral | CHF 49.52 |
| Victory Giant | Buy → Strong buy | CNY 166.41 |

What worries me: peer comparison assumes the peers are priced sensibly. If the whole group is overvalued or undervalued together, that half of every target is off, and nothing inside my models would show it. So I read these 11 changes as "prices moved first," not "the companies got better." Back to the thread: there's no new fundamental evidence behind these rating changes, and I won't dress them up as if there were.

## 5. Two small fixes: net debt shouldn't track the share price, and interest shouldn't be a guess

Both were errors in my models. The numbers barely moved, but Microsoft is now closer to a rating boundary.

The first is how I reprice peers. When updating a peer's EV/EBITDA (enterprise value over earnings before interest, taxes, depreciation and amortization) to a new quote, I used to scale the whole EV by the price change. But EV is equity value plus net debt. When the share price falls 10%, only the equity part falls; net debt doesn't change. **Where I went wrong:** I scaled net debt too. **What changes:** I now separate net debt and reprice only the equity.

The second is Coherent's interest. I had assumed $0.08bn a year of net interest and other expense. That was an assumption with no actuals behind it. The company's reported FY2027 Q1 figure was $0.033bn, or $0.132bn annualized, and the FY2026 full-year figure was $0.118bn, both above my assumption. **What changes:** I now use Q1 actuals times four.

| Company | What changed | Weighted target (before → after) | Upside | Rating |
|---|---|---|---|---|
| Microsoft | Peer repricing separates net debt | $354.14 → $357.02 | −26.3% | Short, unchanged |
| Oracle | Same | $62.94 → $63.28 | −37.5% | Short, unchanged |
| SpaceX | Same | $32.84 → $32.81 | −74.3% | Strong short, unchanged |
| Coherent | Interest uses annualized Q1 actuals | $195.59 → $193.30 | +3.2% | Neutral, unchanged |

Microsoft deserves a note. The line between Short and Neutral is −25%. It's at −26.3%, so a target about $6.40 (around 1.8%) higher would make it Neutral. At that distance a small fix can flip the rating, so I don't put much weight on the Short rating.

## 6. After Anthropic listed, I switched to the market price, and upside went from +11.8% to −5.7%

My view of the company barely changed. The price I compare it to did.

Anthropic listed on Nov 19 under the ticker ANT. I had been using $74 as the price, the midpoint of the preliminary prospectus range of $70–78. Now I use the Nov 20 close of $88.91. The peer median EV/forward revenue moved from 26.32x to 26.93x, my weighted target from $82.71 to $83.84, and upside from +11.8% to −5.7%. The rating stays Neutral.

I made a mistake here too. At first I changed the "offering price" directly to the $88.91 close, which pushed net proceeds in the model to $91.8bn, as if the company had raised money at the closing price. I then split the model's price into two inputs, market price and offering price, and net proceeds went back to $80.8bn. The actual $83 IPO price and the upsized offering aren't in the model yet; they wait for the final prospectus.

## What I'm watching next

- **NVIDIA's CEO search and Q4 results (expected late February 2027).** I'll check whether Q4 revenue lands inside the company's $130.0bn ±3% guidance, who becomes permanent CEO, and whether the core team stays. If revenue comes in below the low end of guidance or senior people start leaving, I'll change my view and move the premium discount into the base case.
- **The industry-layer model taking in Q3.** Right now my two models disagree on the same check. If, after the update, the main reading is still below −15%, I'll change my view and cut the layer's 2026 NVIDIA revenue.
- **Anthropic's final prospectus.** I'll roll in the $83 pricing and the upsized offering. If the change in net proceeds moves the target by more than 5%, I'll recheck the rating rather than keep Neutral by default.

Data and models for every company are on the [AI compute map]({{ '/map/' | relative_url }}).

*Figures come from my own models (versions dated November 21-25, 2026: NVIDIA v0.3.14-v0.3.16, Coherent v0.4.8, Microsoft v0.3.11, Oracle v0.5.5, SpaceX v0.2.12, Anthropic v0.2.4, with other stock models rebuilt on Nov 20 closes; AI compute map v0.6.57-v0.6.60). This is internal research, not an independent source. Company figures are from filings, earnings calls, 8-Ks and prospectuses. Research notes, not investment advice.*
