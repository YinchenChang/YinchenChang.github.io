---
layout: post
title: "The Neocloud Ledger: Contract Prices Don't Cover the GPU, Only the Funder Differs"
date: 2026-10-24 16:00:00 +0800
lang: en
alt: /zh/writing/2026/10/neocloud-economics/
---

Neocloud discussions usually start with backlog: how big the contracts are, who the customers are, how long the terms run. Over the past several weeks I built a funding-and-valuation model for each of four companies: CoreWeave, Nebius, Oracle's OCI and WhiteFiber. All four sit on the same per-gigawatt cost model. The conclusion they share is more useful than any one of them alone:

**At the only long-term contract price that can be verified, rental revenue per MW does not recover the capital cost of the GPUs. The four companies differ not in unit economics but in who funds the gap.**

## One ruler

All four models use the same inputs, deliberately.

- **Cost** comes from my Tokenomics model (racks, data hall, power, maintenance and depreciation per GW). For GB300, IT capex is about US$32.2m per MW of IT power, and about US$37.6m for VR200. At a 10% cost of capital and six-year depreciation, a GB300 megawatt needs about US$10.9m a year in rent to break even.
- **Price** uses only long-term contracts whose economics can be computed from disclosed terms. So far there is one: IREN's five-year GB300 contract with Microsoft, about US$9.7m per MW per year.
- Divide one by the other and you get a **pricing multiple k ≈ 0.89**. The long-term price is about 89% of break-even rent.

**What is k?** Think of it as rent divided by mortgage. Break-even rent is the mortgage: the cost of the GPUs and equipment, six years of depreciation, a 10% cost of capital, power and maintenance, all spread into one annual amount per MW. k is the rent actually received divided by that amount.

- **k = 1**: rent covers every cost and delivers a 10% return.
- **k > 1**: the megawatt makes money; the higher k, the more.
- **k < 1**: every megawatt built loses money, and building more loses more.

The advantage of k is that it survives changes in chip generation and cost. If GPUs get cheaper, break-even rent falls with them, so k always compares price with cost.

New capacity at all four companies is priced at that multiple. No company's k is backed out of its own revenue or backlog. That is the strongest and the most fragile assumption in the analysis, and I come back to it below.

## Why backlog is not cash

k < 1 means each additional megawatt generates enough operating cash to pay for power, rent and overhead, but not for the GPUs. Take CoreWeave (model v4.12, base case):

- EBITDA is about US$4–5m per MW per year, close to reported results (the model's 2H26 is US$4.86m; Q2 actual was US$4.83m).
- Each MW first requires more than US$30m of GPUs and IT equipment, depreciated over six years.
- After depreciation and interest, every MW is still loss-making before tax.

So remaining performance obligations become revenue only after capacity is built, and the more is built, the more outside funding is needed. In my model CoreWeave's five-year funding gap is roughly US$32bn, US$79bn and US$152bn in the conservative, base and aggressive expansion cases. The counterintuitive result: **the faster it expands, the lower the equity value**, because each extra MW has negative net present value, masked by revenue growth.

## Four companies, four ways to fill the gap

| Company | Who funds the gap | What the model says |
|---|---|---|
| CoreWeave | Asset-backed debt, convertibles, equity | Negative unit economics; the gap scales with expansion. Backlog is not cash |
| Nebius | Customer prepayments | Prepayments are real cash (about US$4.55bn in 1H26) but cover only about 36% of capex, leaving a base-case gap of about US$76bn |
| Oracle (OCI) | Legacy software cash flow, investment-grade debt, customer prepayments | Funding holds: no new equity over five years, adjusted leverage peaks near 4.2x against a 4.5x ceiling. What holds is the balance sheet, not the return |
| WhiteFiber | Ten-year colocation leases (low price, capital-heavy) | Colocation is a financeable base; cloud expansion by itself creates no value |

The point of the table: **funding structure decides who survives, but it does not change whether a megawatt makes money.** Oracle has the strongest balance sheet, so it can scale a k < 1 business without dilution. CoreWeave does not, so the same unit economics depend on capital markets continuing to buy. Nebius's prepayments are closer to cash than CoreWeave's backlog, but there are not enough of them.

## The biggest uncertainty: k

The whole conclusion rests on one number with one data point behind it.

- **Only one verified long-term contract.** Two other contracts (IREN–NVIDIA, and an unverified Oracle–OpenAI reading) price similar or slightly higher, but neither can be fully computed from disclosed terms. Spot prices run about 1.8 times break-even, but neoclouds mostly sign long-term contracts before they build.
- **Oracle is the best counter-example.** Backing k out of Oracle's own OpenAI contract terms gives roughly 1.22–1.47 (unverified; it depends on whether the 4.5 GW is IT or facility power). If that price holds, Oracle's conclusion flips. Oracle's question is not capacity but **whether the price it signed will stick**.
- **Market prices imply a k well above the evidence.** Solving a reverse DCF, Oracle's share price needs k of about 1.27, and Nebius's needs revenue per MW of about 2.5 times break-even rent. Either the market expects neocloud contract prices far above the only verified one, or it expects GPUs to earn well beyond six years.

## What to watch

Any of these would force a recalculation:

1. **A second verifiable long-term contract price**, especially for VR200, with disclosed MW or GPU count and term.
2. **Renewal pricing.** The discount at which the first five-year contracts renew sets the GPU's economic life directly.
3. **Oracle disclosing OCI megawatts and its OpenAI contract terms.** This is the one evidence source that could push k above 1.
4. **Third-quarter results in November.** CoreWeave's actual capex per MW (about US$24.8m in 1H26, about 19% below my model) would shrink the gap if it stays low. It is currently the largest gap between the model and reported results.

## Conclusion

The neocloud question is not demand. Demand is real, and so is backlog. The question is that at the prices that can be verified today, rent per megawatt does not pay for its capital, and the gap grows with scale. Whoever has the lowest cost of capital and the strongest counterparty lasts longest. Lasting and earning a return are different things.

All four models are public and let you change k, expansion pace and cost scenario: [CoreWeave](/models/coreweave.html), [Nebius](/models/nebius.html), [Oracle](/models/oracle.html), [WhiteFiber](/models/whitefiber.html) (model pages are in Chinese).

*All figures come from my own models (as of 22 October 2026, Tokenomics v18.0–v19.0). They are internal research, not an independent source. Company figures are from filings and earnings calls, tagged and sourced on each model page. Not investment advice.*
