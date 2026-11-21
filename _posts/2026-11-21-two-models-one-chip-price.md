---
layout: post
title: "My Two Models Disagreed by 16 GW on 2027. The Real Argument Was What One NVIDIA Chip Sells For"
date: 2026-11-21 10:52:00 +0800
lang: en
alt: /zh/writing/2026/11/two-models-one-chip-price/
permalink: /writing/2026/11/two-models-one-chip-price/
description: "This week I reconciled my model of how many chips ship against my model of how much capacity buyers can build. They agree on 2026 and miss by 16.3 GW on 2027. Most of the gap came from one unpinned number: NVIDIA's revenue per package. Rebuilding the 2027 unit count myself halved the gap, but the remaining 6.67 GW has no single cause, and I don't count the narrowing as validation."
---

<p class="lede">The thing I cared about most this week: I have two models estimating the same quantity, the gigawatts of AI compute added each year. For 2026 they differ by 10%. For 2027 they differ by 16.3 GW. One counts from the supply side, how many chips ship; the other counts from the demand side, how much buyers' capex and data center sites can absorb. After a week of digging, my conclusion is that most of the argument is about what one NVIDIA chip sells for, a number nobody has pinned down; their views on demand are closer than the headline gap suggests. Rebuilding NVIDIA's 2027 unit count myself cut the gap in half, but I don't think the problem is solved.</p>

<div class="keypoints" markdown="1">
**Key points**

- For 2026 the two models differ by 10%. Checked against NVIDIA's reported data center revenue, one side is 11.9% high and the other 12.0% low. I called it a tie.
- For 2027 they differ by 16.3 GW, or 14.7 GW after allowing for the lag between shipment and going live. I ruled out three common suspects and found one 0.4 GW double count.
- The main gap is NVIDIA's 2027 unit count: 9.12 million packages on the supply side, 4.38 million on the demand side. The same revenue divided by US$63,000 gives 9.12 million; divided by US$131,000 it gives 4.38 million.
- I rebuilt the count from five paths. My most likely figure is about 6.0 million, and the model now uses 6.13 million. The gap after timing fell from 37% of the baseline to 22%, still above my 15% tolerance.
- The remaining 6.67 GW splits into NVIDIA 3.16, non-NVIDIA 2.48 and conversion method 1.03. No single cause.
</div>

## 1. The models agree on 2026; for 2027 they can't both be right

The short version: my two models are usable for 2026, and from 2027 one of them has to be wrong.

First, what the two models are. The supply-side model works down from chip shipments: how many NVIDIA, AMD, Google TPU and other accelerators ship, how much power each draws, summed into new GW. The demand-side model works up from buyers: cloud capex, confirmed data center sites, and the cost per GW, giving how many GW buyers can actually install. As an analogy, one side counts air conditioners leaving the factory and the other counts how many units the new buildings can hold. The analogy has a limit: chips can sit in a warehouse until the building is ready, so some lag between the two is expected.

The trouble is that the 2027 gap is too big for lag to explain. I ran a stock account (shipped minus installed equals what is sitting in storage). If both sides were right, about 25 GW of chips would be shipped with nowhere to plug in by the end of 2027, and about 55 GW by the end of 2029, growing every year. A gap that keeps growing points to one side having the wrong level, which lag can't fix.

Here is the gap after timing and inventory, as a share of the supply-side baseline, before and after this week's changes:

{% include charts/2026-11-21/residual-en.svg %}
<p class="chart-note">Gray is where things stood at the start of the week (Nov 18); orange is after I rebuilt the unit count (Nov 19). Look at 2027-2029: down from the low-to-high 30s to 22%, but still above the red dashed line.</p>

Why do I accept 2026? I checked both sides against NVIDIA's reported data center revenue. Revenue implied by the supply side is 11.9% high and by the demand side 12.0% low, one over and one under, both inside ±15%. I ruled it a tie and kept 2026 at 23.40 GW of new capacity. Put simply, I can't tell which side is more accurate for 2026, but both are within a usable range. The real problem starts in 2027.

## 2. I ruled out three suspects and found one 0.4 GW double count

The short version: the usual definitional problems aren't the cause, and my own mistake accounts for about 3% of the gap.

I checked definitions first, because a definitional mismatch can close a gap without anyone changing their view:

| Suspect | What I found | Effect on the 2027 gap |
|---|---|---|
| One side counts dies, the other packages | Both count packages (one package can hold two dies) | 0 |
| Demand side excludes Blackwell in 2027 | True, but small | About 0.2-0.3 GW |
| Different ownership basis for non-NVIDIA sites | True, but it points the other way; fixing it widens the gap | Opposite direction |
| Rubin Ultra counted twice | **True, and my mistake** | 0.4 GW (about 3%) |

**I was wrong to** count Rubin Ultra (NVIDIA's higher-end part for the second half of 2027) both inside the Rubin count and on its own line. **The reason** was that my two sources defined Rubin differently, one including Ultra and one not, and I didn't reconcile them first. **I've now changed** Rubin from 7.0 million packages to 6.7 million, which takes the 2027 supply side from 39.16 to 38.74 GW. The fix was needed, but it can't explain a 14.7 GW gap. Once definitions are cleared, what's left is a difference in views.

## 3. The real problem: nobody has pinned down NVIDIA's revenue per package

The short version: most of the distance between 9.12 million and 4.38 million comes from the assumed price per package.

This week I rebuilt NVIDIA's 2027 package count myself, without any broker or research-firm figures, using five paths built on primary sources: NVIDIA's revenue guidance divided by price per package, NVIDIA's statements about orders, big-four cloud capex, TSMC's AI accelerator revenue, and HBM (high-bandwidth memory, the memory stacked next to the GPU) bit supply. The results:

{% include charts/2026-11-21/nv-units-en.svg %}
<p class="chart-note">NVIDIA packages in 2027, low to high for each path. Look at the red line: 9.12 million touches only the top end of the two widest paths (TSMC and HBM). The blue line at 4.38 million falls inside all five, but below the middle of each.</p>

My view is 4.0 to 8.8 million packages in 2027, most likely around 6.0 million, with medium-low confidence. The range is wide; even the narrowest path spans 2.2 times from low to high. That's as far as primary evidence goes today, and I didn't force the paths to converge.

Price is the crux. NVIDIA reports revenue, not units; it has never published unit counts. So every unit count is revenue divided by price. It's like knowing a restaurant's monthly sales and trying to guess how many customers came in: you have to guess the average bill first, and if that's off by a factor of two, so is the head count. The same revenue at an average of US$63,000 per package gives 9.12 million; at US$131,000 it gives 4.38 million. My base is US$103,000.

What evidence is there on price?

{% include charts/2026-11-21/rubin-price-en.svg %}
<p class="chart-note">NVIDIA revenue per package, US$ thousands. Both dots fall outside the Rubin evidence band (light orange): 9.12 million needs Rubin priced close to Blackwell, and 4.38 million needs Rubin priced above the highest evidence.</p>

- **What the company said:** On its August 26, 2026 earnings call, NVIDIA put its revenue opportunity per GW at US$25 billion for Blackwell and US$40 billion for Vera Rubin. It also guided revenue growth of about 70% for the next fiscal year (FY2028) and said supply would stay constrained through the end of FY2028.
- **What a buyer disclosed:** Nscale's prospectus filed with the SEC includes purchase estimates that imply US$96,000-139,000 per Rubin package, right in the middle of the range I derive from NVIDIA's own statements. It doesn't rely on NVIDIA's word, so I give it more weight.
- **My estimates:** Rubin at US$96,000 / 114,000 / 139,000 per package (low / base / high), Blackwell at US$43,000 / 50,000 / 55,000.

So for 9.12 million to hold, a Rubin package would have to sell for about US$67,000, only 1.3 times Blackwell. That conflicts with NVIDIA's own "US$25 billion to US$40 billion per GW". The alternative is NVIDIA data center revenue in 2027 at 1.6 times what its guidance implies. For 4.38 million to hold, NVIDIA's revenue would have to fall about 22% short of guidance, or Rubin would have to sell for about US$157,000, above every piece of evidence I have. Both sides need one implausible assumption; the one behind 9.12 million is the less plausible.

## 4. Switching to my own count halved the gap, but I don't call that validation

The short version: I moved the model to 6.13 million packages and the 2027 gap shrank a lot, but part of that shrinkage is circular.

After the change, the 2027 supply-side baseline fell from 39.16 to 30.45 GW, and the residual after timing fell from 14.68 to 6.67 GW. 2028 and 2029 also roughly halved (those two years also had a unit coefficient changed from 0.80 / 0.71 to 0.69 / 0.61; that coefficient is my assumption, not something with outside evidence behind it).

One number looks great and needs a caveat. After the change, the supply side's implied 2027 NVIDIA revenue matches the figure derived from company guidance to within 0.2%. That match is circular: I derived the unit count from revenue guidance using the same prices, so of course it matches. The real test needs actual results. That's also why I deliberately kept NVIDIA's third-quarter results, reported in November, out of every model and parameter. I'm holding them back as an exam for later.

Changing the unit count flows through every hardware stock model. In the November 18 version, 56 of the 66 companies with models had their target prices change, by −10.6% to +16.4%, median −4.1%. The direction is intuitive: lower industry shipments mean lower values for most suppliers. NVIDIA is the exception, because I raised the price per package at the same time, and its target went from US$283.30 to US$329.77. After the map was recalculated, rating changes for non-Taiwan stocks were:

| Company | Rating | Map target | What changed |
|---|---|---|---|
| NVIDIA | Strong buy | US$333.51 | Fewer packages, higher price per package; net up |
| Broadcom | Short → Strong short | US$166.10 | Valuation moved after the industry-level recalculation |
| Astera Labs | Short → Strong short | US$106.42 | Same |
| Ibiden | Neutral → Short | ¥4,407.92 | Same |
| Advantest | Neutral → Short | ¥22,196.40 | Same |
| Disco | Short → Neutral | ¥36,416.30 | Valuation moved after the industry-level recalculation |
| Intel | New: Strong short | US$16.00 | New model |
| GlobalFoundries | New: Short | US$30.49 | New model |
| Tokyo Electron | New: Short | ¥6,716.32 | New model |
| Vertiv | New: Short | US$141.57 | New model, placed in the map's power and cooling segment |
| ABB | New: Short | CHF52.11 | New model, placed in the map's power and cooling segment |

Per this site's rules, ratings and targets are not shown for Taiwan stocks. The point of the table: one industry-level parameter runs through the unit count into dozens of valuations, which is why I'd rather spend a week getting it straight.

## 5. The remaining 6.67 GW isn't concentrated anywhere

The short version: what's left is a roughly 22% difference in overall level, shared between NVIDIA and everyone else, with no single cause.

{% include charts/2026-11-21/residual-split-en.svg %}
<p class="chart-note">The 2027 residual between the two sides, in GW. All three pieces are material: removing any one of them doesn't make the sides agree.</p>

Broken down: for NVIDIA, the supply side has 6.13 million packages against 4.44 million implied on the demand side, a 1.38x gap. Outside NVIDIA the two sides differ by about 1.22x. The remaining 1.03 GW comes from converting the demand side's payment-year figures to shipment years, a method difference rather than either side's view. In dollar terms, about US$250 billion of 2027 AI IT capex has no buyer on the demand side.

I also checked a parameter people often reach for to close gaps like this: what share of cloud capex is AI. No company discloses it directly. Microsoft and Alphabet split servers from buildings but don't separate CPUs from GPUs. The market data I could find is IDC's count of US$122.6 billion of global server revenue in the first quarter of 2026, with GPU-accelerated servers at 56.2%. That doesn't support raising the 0.85 in my model; if anything it points to a wider gap. So I'm keeping 0.85, and this lever can't close the gap.

## 6. The two sides are now so close that near-term data can't tell them apart

The short version: a side effect of the narrower gap is that early-2027 results will probably only produce a "tie", so I'll have to wait longer.

I wrote down the 2027 checkpoints in advance, such as assembler revenue and NVIDIA's first-half revenue. Recomputed with current figures, the two sides differ on those measures by only 1.11x and 1.20x, while my rule needs at least 1.35x to say which side is right. In other words, the February 28, 2027 re-ruling (after NVIDIA's fourth quarter) is almost certain to be a tie. The thresholds are as strict as before; the two sides are simply already within tolerance on what can be observed.

This is what worries me most: I only have two independent historical points to test against, which isn't enough to say which side is more accurate. I also looked at how others handle this. Epoch AI, SemiAnalysis, LBNL and the IEA all give scenario ranges for 2027-2029; none publicly reconciles supply and demand to a single point year by year. Epoch AI estimates its own site database covers about 44% of deployed compute worldwide. My 2027 sites show only 7.50 GW, 41% of the 18.16 GW capex path, a similar order. So my view is that an open gap here is normal for the field; what I add is putting it in writing. Where two readings are both defensible, I take the more conservative path: the baseline doesn't move until new evidence arrives, I don't average toward the middle (the midpoint estimate is display-only), and when I use the supply-side baseline for hardware stocks I also look at the result under the demand-side reading.

## What I'm watching next

- **NVIDIA's fourth-quarter results (expected at the end of February 2027).** I'll check whether data center revenue tracks guidance. If it comes in about 20% below what guidance implies, I'll change my view and move the unit count toward 4.38 million.
- **Evidence on Rubin's price.** NVIDIA doesn't publish units, so I'll keep looking for buyer disclosures like Nscale's filing, and add Dell and Supermicro AI server revenue as a fifth independent path. If more buyer disclosures put Rubin above US$139,000 per package, I'll cut the unit count.
- **Interim results from May 2027.** I've frozen every version of the forecast so I can check them one by one. If actual results land systematically on the demand side, I'll change the baseline rather than keep it on the supply side.

Data and models for every company are on the [AI compute map]({{ '/map/' | relative_url }}).

*Figures come from my own models (versions dated November 14-20, 2026: Siliconomics v0.20-v0.22, Wattonomics v0.3.7-v0.3.9, with hardware stock models rebuilt accordingly; AI compute map v0.6.56). This is internal research, not an independent source. Company figures are from filings, earnings calls and prospectuses; Epoch AI and IDC figures are from their public material. Research notes, not investment advice.*
