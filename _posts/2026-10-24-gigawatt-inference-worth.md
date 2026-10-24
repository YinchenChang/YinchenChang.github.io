---
layout: post
title: "What Is a Gigawatt of AI Inference Worth?"
date: 2026-10-24 15:00:00 +0800
lang: en
alt: /zh/writing/2026/10/gigawatt-inference-worth/
---

## The short answer

One gigawatt of current-generation capacity (VR200 NVL72), run the way a frontier lab runs its fleet, earns about **US$50 billion a year** in paid token revenue in my base case, within a range of **US$36–79 billion** depending on utilization. Owning and running that gigawatt costs about **US$12 billion a year**. Revenue is therefore about **4x** the holding cost, within a range of 3–6x.

Two caveats come before the number, not after it.

- **This rests on assumptions.** Utilization and production efficiency are not disclosed by any operator; both are assumed and shown as ranges.
- **The token ledger does not close yet.** The model's paid-token output is about 3x what demand-side data supports. If the whole gap sits on the capacity side, first-year revenue is closer to US$16 billion and the ratio closer to 1.3x. The 4x headline is the upper reading of that unresolved gap.

## The identity

Everything below comes from one accounting identity, revenue = price × quantity:

> **Revenue per GW** = tokens the GW can serve at the speed floor × utilization × production yield × paid share of the fleet × effective price per token

- **Capacity at the speed floor** is how many tokens 1 GW of IT power can serve while meeting a per-user speed floor. Memory bandwidth, compute and interconnect set it.
- **Utilization** is the share of the year that capacity is actually busy. Base case 41%.
- **Production yield** is the gap between benchmark throughput and real traffic: uneven request lengths, routing imbalance, failures. The base-case input is 0.85, which works out to about 0.81 of benchmark output once the model re-solves its latency constraints.
- **Paid share** is how much of the fleet sells tokens at all (next section).
- **Effective price** is list price after discounts and cached-input pricing. I calibrate it to reported revenue with a realization factor, m = 1.34. That factor exceeds 1 because of the unclosed token ledger above.

The first term is physics. The others are where the disagreement lives.

## From one tier to a fleet

A gigawatt serving only the mid tier all year at 60% utilization would earn about US$308 billion. A realistic fleet earns a fraction of that, because most of the gigawatt never sells a token.

| VR200, 60% utilization, before production losses | Revenue (US$B/yr) |
| --- | --- |
| 1 GW serving only the low tier (GPT-6 Luna) | 59.3 |
| 1 GW serving only the mid tier (GPT-6.1 Sol) | 307.6 |
| 1 GW serving only the top tier (GPT-6 Astra) | 335.7 |
| 1 GW reference fleet, paid tokens only (ideal ceiling) | 67.0 |

The reference fleet allocation is calibrated to OpenAI's reported spending, so treat it as an interested-party anchor:

- **59% training and research.** Training runs and experiments earn nothing directly.
- **41% external serving (range 30–60%), of which 46% is free.** Free users consume tokens and pay nothing, so only about 22% of the gigawatt sells. The 41% split rests on a reported inference figure; the training figure behind it could not be traced to a primary source, hence the wide range.
- **Paid tokens are 40% low tier, 45% mid tier, 15% top tier.** The top tier earns about 61% of paid revenue on 15% of paid tokens.

Blended, that is about US$1.96 per million paid tokens, or US$0.47 per million tokens served once free tokens are counted. The question "what is a gigawatt worth" is mostly a question about this allocation, not about chips.

The ideal ceiling of US$67 billion assumes 60% utilization, no production losses and list-price realization. Moving to the base case (41% utilization, 0.81 yield, m 1.34) gives the headline US$49.5 billion. The two reconcile exactly: 66.95 × (0.41 ÷ 0.60) × 0.806 × 1.343 = 49.51.

## How wide the range is

Utilization and production yield are the two least observable inputs. VR200 reference fleet, paid revenue in US$B/yr, with revenue ÷ annual holding cost (US$12.23B) in brackets:

| Production-yield input | 40% utilization | 60% utilization | 80% utilization |
| --- | --- | --- | --- |
| 0.8 | 44.4 (3.6x) | 66.6 (5.4x) | 88.8 (7.3x) |
| 0.9 | 52.2 (4.3x) | 78.3 (6.4x) | 104.4 (8.5x) |
| 1.0 | 59.9 (4.9x) | 89.9 (7.4x) | 119.9 (9.8x) |

The base case (41%, 0.85) is US$49.5 billion. Revenue scales one-for-one with utilization. It does not scale one-for-one with the yield input, because the model re-solves its latency limits: inputs of 0.80, 0.85, 0.90 and 1.00 give actual output of 0.74, 0.81, 0.87 and 1.00.

On the base cost case, the paid fleet covers its holding cost at about 10% utilization. With high-cost hardware and a 0.8 yield input, break-even rises to about 18%. Holding cost itself spans US$9.5–19.8 billion across cost cases.

The other levers, each moved alone from the base case:

| Lever | Low | High | Effect on fleet revenue |
| --- | --- | --- | --- |
| Share of fleet serving external users | 30% | 60% | ×0.73 / ×1.46 |
| Free share of served tokens | 35% | 60% | ×1.20 / ×0.74 |
| Cached-input hit rate | 30% | 75% | ×0.93 / ×1.07 |
| Effective discount | 10% | 30% | ×1.00 / ×1.00 |

Two rows need a note. Because revenue is calibrated to what is actually reported, a deeper discount is offset one-for-one by the calibration, so realized revenue does not move. Cache hits are partly offset the same way. At list prices, before calibration, a 10–30% discount would move revenue ×1.13 / ×0.88.

The fleet-allocation levers matter as much as utilization. A lab that shifts compute from research to paid serving raises its revenue more than one that runs its servers harder.

## Across hardware generations

Pricing every generation at today's list prices, the question becomes: what would this hardware earn serving today's models?

| Generation | Paid tokens per GW (VR200 = 1) | Holding cost (US$B/yr) | Revenue ÷ holding cost |
| --- | --- | --- | --- |
| H100 | 0.10 | 9.70 | 0.5x |
| GB200 | 0.50 | 8.83 | 2.8x |
| GB300 | 0.61 | 10.89 | 2.7x |
| VR200 | 1.00 | 12.23 | 4.0x |
| Rubin Ultra | 1.39 | 15.35 | 4.5x |

An H100 gigawatt cannot pay for itself serving today's models: at the same speed floors it serves about one-tenth of VR200's tokens. The step from GB300 to VR200 raises the ratio by about half while holding cost rises about 12%. The gain comes from more tokens per gigawatt, not from cheaper hardware.

Only the VR200 ratio is a named model output; the other generations are converted on the same basis.

## What this number is not

It is not a revenue forecast. Four things sit outside it by construction:

1. **Demand.** The calculation assumes paid demand fills the paid capacity. The unclosed token ledger is a warning that it may not.
2. **Price.** List prices are a snapshot. If capability per dollar keeps rising, prices per token fall and revenue falls with them, even on the same hardware.
3. **Subscriptions and ads.** Consumer subscriptions are priced per seat, not per token, so they are only partly captured through the revenue calibration.
4. **Training amortization.** The holding cost covers owning and running the gigawatt. The cost of the models it serves is a separate charge, and it is large.

The useful reading is the reverse one. If a lab's reported revenue per gigawatt sits far below this number, the gap is utilization, allocation or pricing, and each of those is observable over time. If reported revenue ever sits above the ideal ceiling, one of the inputs here is wrong.

**What would change this view:** an operator disclosing utilization or the paid share of its fleet; a sustained cut in list prices per capability tier; measured production yield well below benchmark; or the token ledger closing on the demand side rather than the capacity side.

## Method and inputs

All figures come from my open, first-principles AI data center model ([github.com/YinchenChang/Tokenomics](https://github.com/YinchenChang/Tokenomics)), version 21.2 (model commit 45ce1ca). GW means IT-critical power; facility power adds PUE on top. Figures were extracted and independently recomputed (140 values) before publication. A minor update (v21.3, a lower low-end rack price and one cached-input price) is in progress; it leaves the base holding cost unchanged.

| Input | Base value | Range used | Basis |
| --- | --- | --- | --- |
| Speed floors per tier (decode tok/s per user) | 120 / 65 / 55 | — | Measured, third-party market observation |
| List prices (input / output, per M tokens) | three tiers | — | OpenAI GPT-6 Luna / GPT-6.1 Sol / GPT-6 Astra official price pages |
| Effective discount | 20% | 10–30% | Assumed |
| Cached-input hit rate | 55% | 30–75% | Assumed |
| Utilization | 41% | 30–65% (headline range) | Assumed |
| Production-yield input | 0.85 | 0.8–1.0 | Assumed |
| Revenue realization factor m | 1.343 | — | Derived; token ledger not closed |
| Fleet share serving external users | 41% | 30–60% | OpenAI 2025 inference spend share (interested party; training spend not traced to a primary source) |
| Free share of served tokens | 46% | 35–60% | OpenAI 2025 non-paying inference ÷ total inference, as reported by The Information, Feb 2026, via secondary summaries (interested party) |
| Capex per GW (VR200) | US$50.3B | model cost cases | Rack prices plus facility build-out; public estimates range from about US$40B to US$49B and have recently been revised down |
| Holding cost per GW per year | US$12.23B | US$9.5–19.8B | Capital recovery at 10% WACC, 6-year IT life, plus operating costs |

The headline rests mainly on assumed and derived values. Read it as "under these assumptions", not as a measurement.

*Not investment advice.*
