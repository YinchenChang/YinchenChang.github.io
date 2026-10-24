---
layout: post
title: "Nine Days In: What an AI Mandate Does When Nothing Clears the Bar"
date: 2026-10-24 12:00:00 +0800
lang: en
alt: /zh/writing/2026/10/aim-nine-days-in/
---

*Follow-up to [When Governance Ate the Research](/writing/2026/10/when-governance-ate-the-research/).*

The last post ended with a successor system going live on 15 October: a US$20,000 mandate in which AI roles do the research, the auditing and the position sizing, and I only fund it and place the orders. This is the first report on it. It is early, and the main result is a number that looks like nothing happened.

## What the mandate is

The Autonomous Investment Mandate (AIM) has one objective, one admission test and one pool of capital.

- **Objective.** Maximise ten-year expected log growth of the committed capital, from 15 October 2026 to 15 October 2036.
- **Pre-registered test.** Over those ten years the pool must beat (a) a 70/30 US broad-market / bitcoin ETF mix, rebalanced quarterly, and (b) the S&P 500 total return. (a) is the primary test. Excess return over (b) is split into [(a) − (b)] plus [pool − (a)], and only the second part counts as research.
- **Admission.** A thesis can become a position only if its lower-bound wealth multiple at repricing is at least 5x, its repricing window is at least 12 months, and (for shorts) upside/downside asymmetry is at least 3.
- **Default holding.** Capital not in an active position holds benchmark (a). Not trading is not a defect; it is the baseline.

Four roles run on an hourly schedule: a scout generates candidates, an analyst tests them, an auditor from a different model family can only veto or uphold, and a portfolio manager sizes positions at quarter-Kelly with a 25% single-position cap. The research roles never see the ledger or any position.

## Nine days of output

Every number below comes from the mandate's public research repository, counted on 24 October.

| Stage | Count |
|---|---|
| Candidate cells in the funnel at start (15 Oct) | 65 |
| Cells tested 15–24 Oct | 50 |
| Total cells tested | 115 |
| — failed first test | 89 |
| — partially passed | 16 |
| — passed first test, but too small or not separable to write up | 6 |
| — thesis written, not loaded (all before the start) | 4 |
| Frozen load cards (the only thing that can be sized) | **0** |

The scheduler logged 318 runs from 15 to 24 October: 50 analyst runs, 50 scout generations, 55 trigger re-scans, 120 idle runs where the queue was empty, and two portfolio-manager sessions.

So nine days and 50 tests produced no position. By the mandate's own rules the pool must then sit entirely in the default holding, and it does.

## Where the allocation actually stands

The orders were executed on 15 October. US$20,000 went in once and bought 37 shares of VTI at $375.45 and 129 shares of IBIT at $45.36. Whole-share rounding put the split at about 70.4/29.6 against the 70/30 target, with $257 left as settlement cash (1.3% of the pool; the cap is 5%).

| As of 23 Oct close (6 trading days) | Value |
|---|---|
| Active positions | 0 |
| Pool NAV | US$19,987 |
| Pool, time-weighted from 15 Oct close | −1.39% |
| Benchmark (a), 70/30 VTI/IBIT | −1.41% |
| Benchmark (b), S&P 500 total return | −1.55% |
| Max drawdown since start (daily) | 2.3% |
| NAV vs. capital committed | −0.07% |

Two notes on reading these figures. First, the three time-weighted returns all start at the 15 October close, so they compare directly. The fills were earlier that day, and the intraday gain from fill to close (about +1.35%) is outside the −1.39%. That is why NAV is almost exactly the capital committed. Second, six trading days say nothing about skill. The pool is 0.02 percentage points ahead of (a) only because 1.3% of it was cash in a falling week.

The figures do not change the structural point. With zero frozen cards, the portfolio manager has nothing it is allowed to size. The pool is benchmark (a), minus trading costs. Every basis point of difference from (a) until the first card freezes is cost, not skill.

## Why nothing cleared

The first post argued that the bottleneck was expressibility and separability, not research depth. The new system was supposed to fix the order of work. Nine days later the kill reasons say the same thing more precisely.

I tallied the reason words in the analyst's first-test files. The leading cause is **separability**: the mechanism is real, but no listed company's filings let you attribute the outcome to it. Next are **already priced** and **already disclosed**: the gap exists, but named sell-side analysts or the company have already quantified it. A smaller group failed on **magnitude**, where the gap is real and observable but too small to reach 5x.

A typical example from 24 October: a candidate argued that the market was extrapolating chip counts directly from CoWoS wafer counts, ignoring that larger packages fit fewer chips per wafer. The geometry checked out. But the analyst found JPMorgan, Morgan Stanley and a Rapidus executive had all published chips-per-wafer figures. The "consensus error" had no named holder. Killed: already disclosed.

That is the system working as designed. A 5x lower bound is meant to be rare. On 15 October I decided to keep the bar at 5x rather than lower it, and recorded the decision: few positions are a feature of this mandate, to be watched, not fixed mid-quarter.

## What would change my mind

The design makes two failure modes visible in advance, so here they are.

1. **The bar is right but the generator is wrong.** If the funnel keeps dying on separability and prior disclosure, the scout is producing ideas where the market already looks. That is a generation problem, and the remedy is to generate from the instrument map backwards. The first post recommended exactly that.
2. **The bar is simply unreachable.** If no cell reaches a frozen card within several quarters, AIM becomes an expensive way to hold (a). The pre-registered review fires only on calibration (two consecutive quarters of Brier above 0.25, with a minimum sample), not on drawdown or underperformance. So this case has to be read from the quarterly scorecard, not from a trigger.

The first scorecard is due on 15 January 2027. I will publish it.

## The lesson so far

The old system failed by doing too much: 1.2 MB of rules, no research. The new one is producing research, 50 documented tests in nine days, each with sources and a stated reason. It has a hard gate and declines to act. That is a better failure mode if it is a failure at all, because it costs the benchmark rather than the capital, and it is measurable.

Whether the gate is filtering out bad ideas or the generator is not yet producing good ones is the question for the next quarter.

*Not investment advice. The mandate is a personal experiment with capital I can afford to lose.*
