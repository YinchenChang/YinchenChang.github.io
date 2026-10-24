---
layout: post
title: "When Governance Ate the Research: A Post-Mortem of a Multi-Agent AI Investment System"
date: 2026-10-24
---

## Seven weeks, one position, 1.2 MB of rules

From late July to 13 September 2026, I ran a multi-agent AI system built to do investment research and position sizing with the human kept out of the research loop. In about seven weeks it deployed one position. Over three of those weeks, its governance documents grew to 1.2 MB while its research output was zero. I retired it on 13 September.

There is no performance to report. The one position is unresolved, and this post does not discuss it. What I can report is how a carefully designed system failed, measured in its own files.

I think the failure modes are worth writing down because they were not exotic. They are the ones I expect investment teams to meet as they move from "an analyst uses a chatbot" to "agents run a research process." Every component of my system was defensible. The sum was not.

## The design

The system split work the way a small fund would, with one hard wall in the middle. I designed the architecture and made the calls; the agents wrote most of the rules, research files and audits.

| Role | Job | What it could see |
| --- | --- | --- |
| Hub (capital agent) | Sizing, allocation, resolving conflicts, commissioning research | Everything, including positions |
| Research agents (AI infrastructure; crypto) | Generate candidates, test mechanisms, write milestone tables | No amounts, positions, P&L or thresholds |
| Me | Open sessions, move files, check option chains at the broker, final filter | Everything |

The wall was the point. A researcher who knows the size of a position, or whether it is underwater, starts reasoning toward it. Human funds handle this with culture. Agents can be given a harder rule: the position file never leaves the Hub, and no handoff file may enter the shared drive unless it carries a line stating it contains no amounts and no positions.

Three other design choices still seem right to me.

- **Candidates from three kinds of first principles.** Physical conservation (energy, bandwidth, time), accounting identities (revenue = price × quantity, balance-sheet constraints), and incentives or information. Running only the physics kind is a narrowing, not rigor.
- **Frozen milestones with probabilities.** Each thesis carried dated milestones, a named data source and a prior probability, frozen before the outcome. Scoring them with a Brier score makes the research itself auditable, not just the P&L.
- **A hit-rate budget.** A concentrated book produces perhaps seven resolvable positions over its life, far too few to test skill. The same theses produce about 45 milestones. Testing at the milestone layer turns an untestable claim into a testable one.

The transport layer was a shared Google Drive used as a message bus: one inbox folder per agent, one state file capped at 6,000 bytes and written only by the Hub, handoffs capped at 8 KB. From 11 September the Hub and the AI research agent each ran on two platforms, Claude and Grok, under a handoff protocol with signatures, idempotent processing order and fork detection when both platforms picked up the same file.

## Failure 1: the governance ratchet

Between 5 and 26 August, the governance corpus grew to 1.2 MB and the research output was zero.

It happened one reasonable step at a time. An agent made an error; a rule was added so the error could not recur. The shared constitution went from version 17 to version 21 in five days and reached 228 KB. The lessons ledger reached 45 entries and 82 KB. Each rule had a valid incident behind it.

The cost was not visible at any single step. Every session had to load more rules before doing any work. Every new rule created edge cases that needed further rules. Agents spent their context, and I spent my own time, on compliance with the process rather than on the questions.

The lesson I wrote down afterward: **a process in which every step is correct but the total is harmful will not be caught by checking steps.** Language models make this worse, because writing a rule costs them nothing.

The fix was quotas, not better rules:

- 20 rules maximum, replacing the 228 KB constitution
- 25 lessons maximum; the 45 were compressed to 24, keeping only those that change a research action
- the state file capped at 6,000 bytes
- at most one governance round in any rolling seven days
- later, in the successor system: to add a rule, delete one first

## Failure 2: candidates died after the mechanism held

Thirteen positionable candidates entered validation. One died because its mechanism was falsified. Twelve died after the mechanism had been shown to hold.

Five of those twelve died on separability: the technology gap was real, but no listed company's financial statements would let you attribute results to it. The rest died at other gates downstream of the mechanism. The same pattern showed up in the September screen: a consumer-AI thesis was rejected because its dominant monetizer was private, leaving no clean public expression. At retirement, two rankable candidates were left, and the system itself flagged that ranking them was not discriminating.

This is the result I find most useful. **The bottleneck was not research depth. It was expressibility and separability.** AI makes depth cheap. It does not create instruments that isolate a view.

The ordering error is visible in the dates. The framework was built on 23 July. The file listing tradable instruments was created on 2 September, six weeks later. In hindsight, the instrument map should come first, and candidate generation should be steered by what can actually be expressed.

## Failure 3: the human became the transport layer

The design removed me from research. In practice it made me the courier.

Platform limits did this, not bad intent (as of September 2026). Files could not be overwritten in place. One platform had no tool to move files. Each platform's projects had to be synced by hand. So I opened sessions, uploaded files, moved processed files to the archive folder, and resolved collisions. Adding a second platform on 11 September roughly doubled that work, because every handoff now had two possible readers.

When the second platform went live, the system ran probe files to measure each platform's actual tool capabilities, for example how much of a file one platform could see in a single read. That was the right instinct. What it did not measure was the number of human actions per unit of research output. That is the metric I would track from day one now.

## Failures 4 and 5: filled-in parameters and anchoring drift

Two failures came from the models' default behavior rather than from the architecture.

**The model filled in facts about me.** Several times, without asking, an agent set parameters about my existing situation: which accounts were in scope, what records existed, what household spending looked like. Every one of them was load-bearing for downstream conclusions. My reading is that a model fills gaps because a complete-looking answer is what it tends to produce. For any parameter about the principal's own assets, records or constraints, the rule has to be: unknown until asked.

**Ambiguity drifted toward the latest input.** When a term or instruction could be read two ways, the agents tended to resolve it in the direction of whatever I had stressed most recently. The error was directional, not random noise, so it compounded across sessions. The countermeasure is mechanical: quote the principal's exact words beside each derived parameter, list the readings instead of choosing one, and count which way the resolutions went.

The sizing of the one deployed position shows why this matters. A Kelly calculation needs a probability, and validation showed this one could not actually be computed. The position was therefore sized from a hedge budget instead, at 1.94% of my total personal portfolio, a separate and much larger base than the mandate described below. A filled-in probability would have produced a larger position with the appearance of rigor.

## What survived, and what replaced it

I retired the system on 13 September 2026. Four pieces carried over: the wall between research and capital, frozen milestones with prior probabilities, the taxonomy of candidate deaths (falsified, inseparable, inexpressible), and a 24-item lessons list kept only where a lesson changes a research action.

The replacement inverts the question. The old system asked whether AI could recommend while a human governed the process. The new one, which I call an Autonomous Investment Mandate, commits US$20,000, a sum I can afford to lose entirely, and lets the AI roles decide end to end. It is judged on results, not on process compliance.

Its main design choices follow directly from the failures above:

- **Pre-registered test.** Ten-year log growth from 15 October 2026, against two named benchmarks, with the hypothesis fixed before the start.
- **Writer and auditor on different platforms.** The auditor may only veto or uphold, never rewrite.
- **Review triggered by calibration, not drawdown.** Two consecutive quarters of Brier above 0.25, with a minimum sample, trigger a review.
- **Hard budgets.** Fixed context load of 30 KB or less, at most 12 load-bearing rules, and a new rule requires deleting an old one.
- **Default to the benchmark.** Capital not placed in an active position holds the benchmark, so declining to act is not treated as a defect.

Before the start date, its candidate funnel has processed 17 cells and promoted none. That can be read as discipline, or as a funnel that has not yet produced an investable idea. Only data after the start can tell those apart.

## Six things I would tell a team building agentic research

1. **Cap governance with quotas, and track governance per unit of output.** Rules are free for a model to write. Size limits, rule counts and a governance cadence are what stop the ratchet.
2. **Map the instruments before generating candidates.** Most of my candidates died because a true mechanism could not be isolated in a listed security, not because the research was shallow.
3. **Build an information wall between research and capital.** It is easier to enforce on agents than on people, so enforce it.
4. **Freeze forecasts with dates, sources and probabilities.** Then score the agents on calibration. Position-level results are too few to tell skill from luck.
5. **Count human handoffs.** If the human is moving files, the system is not autonomous, whatever the diagram says.
6. **Never let the model fill in the principal's parameters.** Unknown until asked, with the principal's own words quoted beside every derived number.

The models were capable throughout. What failed was the system around them: each part was justified locally, and nothing measured the whole. The successor starts on 15 October. Whether it does better is a question only its results can answer.
