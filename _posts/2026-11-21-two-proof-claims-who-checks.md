---
layout: post
title: "Two Million-Dollar Math Problems Were Claimed Solved in One Day. I Care About Who Checks, and How Long It Takes"
date: 2026-11-21 08:28:00 +0800
lang: en
alt: /zh/writing/2026/11/two-proof-claims-who-checks/
permalink: /writing/2026/11/two-proof-claims-who-checks/
description: "On November 20 the Riemann hypothesis got two claimed proofs and Navier-Stokes got an unforced blowup claim; two of the three were made with AI. All three are still claims. I separate what has been checked from what has not, then look at the short, medium and long-term effects on mathematics and AI technology: writing a proof has gone from years to weeks, while checking and understanding it has not."
---

<p class="lede">This is an extra piece outside my weekly essay. The thing I care about most: on November 20, in a single day, the Riemann hypothesis got two claimed proofs and the Navier-Stokes equations got a claimed "unforced" proof, and two of the three were made by a person working with AI. My view is that all three are still claims; none has been confirmed by mathematicians. One thing is already visible, though. AI has cut the time to write a proof from years to weeks, and the time to check and understand one has not shrunk with it. I think most of what changes in mathematics and in AI technology over the next few years will follow from that gap.</p>

<div class="keypoints" markdown="1">
**Key points**

- Three claims, none confirmed. The AI-assisted Riemann proof was released only as Lean code (Lean is a language that lets a computer check a proof step by step), with no paper. The human-readable version ran past 250,000 pages and the author chose not to publish it.
- Two things have been checked by others: the code compiles, and the statement it proves is the generalized Riemann hypothesis. What has not been checked is whether anyone can explain why it works.
- The Navier-Stokes result closes the "forcing" loophole that OpenAI's September proof was criticized for, but its key numerical certificate has not been released.
- The speed gap: OpenAI's September proof took 88 hours and the Riemann work took 40 days at most. The Clay Mathematics Institute's prize rules require at least two more years after publication.
- For AI technology, my reading is that fields whose output a machine can check will benefit first. Mathematics happens to be the science that is cheapest to verify. Other fields do not have that.
</div>

## 1. Separate fact from claim first: three proofs, none confirmed

The short version: as I write this (the morning of November 21, Taipei time), all three proofs are at the stage where the authors say they have done it.

Here is what happened over the past few months:

{% include charts/2026-11-21/timeline-en.svg %}
<p class="chart-note">Timeline, July to November 2026. What to look at is the pace: a little over two months separate the September dispute from November 20.</p>

What each proof consists of, and how far the checking has gone:

| Claim | Who | What was released | Checked by others | Not yet checked |
|---|---|---|---|---|
| Riemann hypothesis (the author says it covers the generalized version) | Levent Alpöge, a mathematician at Anthropic, with Claude | A four-page note plus Lean code in a 14-part archive; no paper | Several mathematicians report a successful build; the statement has been confirmed as the generalized Riemann hypothesis | A full audit of axioms and dependencies; a version people can read |
| Generalized Riemann hypothesis | Alessandro Masullo (Stanford PhD), posted by Ravi Vakil, president of the American Mathematical Society | A human-written draft, stated to use no AI; the author says it took 12 years | Stanford's Brian Conrad has been vetting it privately for months; Vakil says it looks good so far | Public review has only just begun, and some mathematicians are already skeptical |
| Unforced Navier-Stokes blowup | Alpöge and Tristan Buckmaster of New York University | A 79-page paper plus a Lean 4 formalization of about 2,270 files and 600,000 lines | The authors state it uses only standard axioms | The numerical certificate is not public; the numerical verification is not formalized; no peer review |

A few things circulating online need correcting after I checked them.

First, the "250,000 pages" are not a published result. That is the length of the Lean proof once Alpöge converted it into natural language. He judged the quality too poor and chose not to release it. Only the code is public.

Second, "the Lean code compiles" does not mean "it is proved." A successful build says the computer accepted every step. Section 3 covers the gates that remain.

Third, some headlines already say "solved," while the body of the same coverage says the work is unverified. The headlines are ahead of the evidence.

So everything I say below about effects carries one condition: if the verification holds. I can't judge that myself. I can only watch how far the checking has gone.

## 2. Navier-Stokes: this one closes the forcing loophole, but the key certificate is not out

My view: if the November result holds, it carries more weight than OpenAI's September one, because it answers the harder version. What it lacks today is a piece that other people can recompute.

The Navier-Stokes equations describe how fluids move. The million-dollar question is whether a fluid that starts out perfectly smooth can, in finite time, develop a point where the rate of change of velocity becomes infinite. Mathematicians call that a blowup.

Here is one way to think about forced versus unforced. Forced is like someone stirring the glass of water with a spoon the whole time, which makes a violent swirl easier to produce. Unforced is leaving the glass alone and asking whether it can whip itself into an infinitely fast swirl. This is only an analogy. In the mathematics the forcing still has to be smooth, so the September result was not easy either.

| | OpenAI (September) | Alpöge and Buckmaster (November) |
|---|---|---|
| External force | Yes, a smooth one | None |
| Part of the Clay statement | (C), with (D) as a corollary | The authors say it disproves (A) and (B) |
| How it was produced | About 10,000 agents running for 88 hours | The authors say they used Claude and Codex throughout; Anthropic's models wrote the first force-free proof, which the two then rewrote |
| What is missing | Still a preprint; Clay has not ruled | Only a hash of the numerical certificate is public; the numerics are not formalized; no peer review |

On the September dispute I will stick to what each side says, because the accounts do not match. Buckmaster's account is that OpenAI started only after hearing of their progress, and that on a September 6 call the other side wanted Alpöge left off the author list. OpenAI's account is that it never saw the pair's results and reached its proof independently, and that it did not ask for Alpöge to be removed from the pair's own paper; the discussion was about Buckmaster rewriting OpenAI's proof. Separately, the pair had kept nearly a year of drafts in OpenAI Codex sessions. On September 10 OpenAI said those sessions could not have influenced its result, without publishing the records behind that conclusion.

I can't tell who is right. What it means for the AI industry is in section 6. Back to the main line: this proof took a little over two months to write, and outsiders still can't check its most important piece.

## 3. Riemann: the computer has signed off on part of it; people have not understood it yet

The short version: this proof has gone further down the machine-checking road than most people expected, and has barely started down the human-understanding road.

The Riemann hypothesis dates from 1859 and is about how prime numbers are distributed. It says that all the important zeros of a function called zeta lie on a single straight line, known as the critical line. Computers have checked the first ten trillion zeros and every one is on the line, but checking many is not proving all.

Claude had a first run at this in August:

{% include charts/2026-11-21/zeros-en.svg %}
<p class="chart-note">Share of zeros proven to lie on the critical line. August's 67.2% was Lean-checked; November's 100% is a claim. The August figures were published by Anthropic at the time; I am reading them from secondary coverage.</p>

Back in August, Oxford number theorist James Maynard told the press he saw no route from those techniques to a full proof. Coverage also notes that Terence Tao said only weeks ago that AI might reach the Riemann hypothesis sometime before the 2050s. Three months after August, a claim exists. What I take from this: even the people who know the most can be far off on timing here, so my own estimate of how long verification takes needs a wide range too.

The gates verification has to pass, and where things stand:

{% include charts/2026-11-21/gates-en.svg %}
<p class="chart-note">Green: reported as passed. Yellow: in progress. Grey: not started. Passing the first two gates does not mean the last two will be passed.</p>

Gate 1, the code compiles. TechCrunch reports that several mathematicians in the Lean community's chat confirmed a successful build, including Andrew Sutherland of MIT.

Gate 2, the sentence being proved really is the Riemann hypothesis. This gate is easier than it sounds, because Mathlib, Lean's standard mathematics library, already contains a definition of the Riemann hypothesis. The proof targets the library's own definition, so nobody has to trust a statement the author wrote. The statement in this release has been confirmed as the generalized Riemann hypothesis.

Gate 3 is the hard one: a full audit of which axioms the proof depends on and whether any unfinished steps are hiding in it, and then someone has to understand it. Alpöge says in his own note that he does not yet fully command one area of mathematics the proof relies on. Tao's comment is that digesting it will take some time.

Put simply, the current state is "the computer says every step is right, and nobody can explain why the whole thing is right." That leads straight to the main line of this piece.

## 4. The gap between writing a proof and understanding it is the real story

My view: the most important message of the week is that production and verification now differ by orders of magnitude in speed. Whether the Riemann hypothesis has actually been proved is something we will only know later.

{% include charts/2026-11-21/speed-en.svg %}
<p class="chart-note">The horizontal axis is logarithmic; each step is 10 times the last. The two AI-assisted efforts sit in the range of days. The human route and the verification rules sit in the range of years.</p>

Put the numbers side by side. OpenAI's September proof used about 10,000 agents for 88 hours. Multiplied out, that is 880,000 agent-hours, or one agent running nonstop for roughly 100 years. That conversion is mine, and it assumes every agent ran the full 88 hours. Alpöge's current round of work with Claude began on October 6, and his note dates the key steps to November 15, so the Riemann part took 40 days at most. On the other side, Masullo says his draft took 12 years, and Clay's rules say a proof must be formally published, wait at least two years, and be generally accepted by mathematicians before the prize is considered.

Think of a factory. The production line suddenly runs a hundred times faster, but quality control is the same few people using the same methods. The faster the line, the more finished-but-unchecked goods pile up in the warehouse. This is only an analogy. Mathematics does have automated quality control in Lean, which can check whether each step is wrong. It cannot check what the proof teaches us.

Tao splits mathematical work into three parts: generating a proof, verifying it, and digesting it. His argument this year is that mathematics is moving from proofs being scarce to proofs being abundant, and the field's institutions have not adapted. The 250,000 pages are the most direct example. The content may be correct, and nobody is going to read it.

What I'm unsure about is whether AI closes this gap itself. If the next generation of models can compress 250,000 pages into a 50-page paper people can follow, then digestion is not the bottleneck and I will have to rewrite the main line of this piece.

## 5. For mathematics: verification in the short term, rules in the medium term, the job itself in the long term

{% include charts/2026-11-21/impact-math-en.svg %}
<p class="chart-note">Effects on mathematics over three horizons. The medium-term "if it holds" items are conditional; the "either way" item is, in my view, already happening.</p>

**Short term (the next three months): one thing only, verification.** I will watch three results: the independent rebuild and axiom audit of the Lean proof, the release and recomputation of the Navier-Stokes certificate, and the open review of Masullo's draft. I can't judge whether the proofs are right, so I am not giving probabilities. There is one unusual feature this time: the generalized Riemann hypothesis has both a machine-checked proof and a human-written draft, and the two routes are independent. If both hold, mathematics gets "certainly true" and "we know why" at once. If only the machine one holds, we get a very awkward theorem.

**Medium term (three months to two years): the rules change.** If the proof holds, coverage says hundreds of results that were proved only under the assumption that the Riemann hypothesis is true become unconditional at once. Whether or not it holds, I think two things are already under way. First, Lean becomes the standard for delivering a proof: two of the three releases came with Lean, and the one that did not will take longer to earn trust. Second, the rules for credit and priority get rewritten. In September, 25 Fields medalists published a declaration saying that AI companies' use of famous problems as a scoreboard is severely misaligned with the goals of mathematics; coverage says more than 7,400 researchers endorsed it within days. That declaration is about exactly these questions: who was first, who counts as an author, and whether a proof nobody understands is a contribution.

**Long term (beyond two years): what mathematicians do will shift.** My inference is that the value of proving something first goes down, and the value of choosing which problems matter, understanding a proof, and explaining it to others goes up. The risk sits here as well. If theorems nobody can read keep piling up, the people who come later have to build on them without knowing why the foundation holds. In the preface to his draft, Masullo tells his colleagues "we are still here." My reading is that the human route's value lies in being readable. On speed it has already lost.

The weakest assumption in this section is the medium-term "if it holds." If the Lean audit finds a problem, the medium-term effects are pushed back wholesale, but the speed gap that runs through this piece stays.

## 6. For AI technology: fields whose output a machine can check benefit first

{% include charts/2026-11-21/impact-ai-en.svg %}
<p class="chart-note">Effects on AI technology over three horizons. The first medium-term item is my inference and has no data behind it yet.</p>

**Short term (the next three months): the showcase race heats up, and announcements should be read as statements from interested parties.** The Jacobian conjecture counterexample in July, the zeros-on-the-critical-line result in August, Navier-Stokes in September, Riemann in November: each one doubled as an advertisement for a model maker. The timing this time is especially sensitive. Anthropic began trading on Nasdaq on November 19, priced at US$83 and closing its first day at US$97.17. The proof was announced the next day, and the stock fell about 9% in early trading that same day, which coverage put down to profit-taking. Alpöge himself calls the timing horrible and denies any link to the share price. My approach is not to guess at motives and to count only third-party verification.

On compute, this kind of work is long-running, multi-agent inference; 880,000 agent-hours is one example. But neither lab has disclosed how many tokens (the unit in which a model's text processing is measured) each agent used per hour, so I can't convert it into compute or dollars. That is the one missing input. Until I have it, I won't put "AI doing mathematics" into any estimate of compute demand.

**Medium term (three months to two years): two things.** First, the pairing of "AI generates, a machine verifies" spreads beyond mathematics. Software correctness, chip design verification and cryptographic protocols are like mathematics in that a machine can check whether the answer is right. This is my inference, with no data yet, and I am treating it as a hypothesis to test. Second, data governance. In the September dispute, researchers worked on unpublished drafts inside an AI tool and afterward could not confirm whether that material had been used for training. OpenAI's final position was that it could not have had an effect, but the basis was not published. Enterprise customers will ask the same question, so I expect "does customer data enter training" to become a harder clause in model makers' enterprise contracts.

**Long term (beyond two years): AI goes from tool to producer of research, with one limit I would add.** Mathematics is the science that is cheapest to verify: a computer can check whether a proof is right. Drugs, materials and physics need experiments, and however many hypotheses AI proposes, the bottleneck stays in the lab. So I won't extrapolate "AI proved the Riemann hypothesis" into "AI will soon solve every scientific problem." The more conservative reading is that AI moves fastest wherever verification is cheapest.

One more point that comes up often: proving the Riemann hypothesis does not break internet encryption. RSA and similar schemes rely on large numbers being hard to factor, and the Riemann hypothesis does not make that easier. The real threat is still a quantum computer.

## What I'm watching next

- **The independent rebuild and axiom audit of the Lean proof.** I will follow the Lean community's reports. If someone shows the proof relies on extra axioms or contains unfinished steps, I will change my view and withdraw "the computer has signed off on part of it."
- **The Navier-Stokes numerical certificate.** The authors say it will be released soon. If it is still not public in a month, or others can't reproduce it, I will mark this one back down to unfinished.
- **Who first turns the proof into something people can read.** If a person or a model writes the Riemann proof up as a paper mathematicians can follow within a few months, I will change my view: digestion is not the bottleneck and the speed gap is smaller than I thought. If instead the Lean proof stands and nobody can explain it a year from now, the judgment in this piece gets firmer.

Data on model makers and the compute supply chain is on the [AI Compute Investment Map]({{ '/map/' | relative_url }}).

<div class="sources" markdown="1">
**Sources**
- TechCrunch (2026-11-20): "AI claimed a solution to the 167-year-old Riemann hypothesis — and a human did, too." Build confirmation; Masullo's draft.
- DataCamp (2026-11-20): "Two Proofs of the Riemann Hypothesis Dropped on the Same Day. One Used AI." Contents and dates of Alpöge's note; Clay rules; RSA.
- OfficeChai (2026-11-20): contents and gaps of the two Navier-Stokes papers; mathematicians' reactions to the Riemann claim.
- lilting.ch: "OpenAI Navier–Stokes: Proof Dispute." Timeline of the September dispute and both sides' accounts.
- Scientific American (2026-11-20): headlines and summaries of three related reports.
- Nacionale (2026-11-20): verification steps; the August zero share (recounting Superpower Daily); Tao's blog.
- Terence Tao: slides of the ICM 2026 public lecture and the summary of his views on AI on his website.
- Anthropic pricing announcement (2026-11-18); Forbes and Yahoo Finance (2026-11-19 and 11-20): listing and share price.
- Wikipedia: Levent Alpöge (the July Jacobian conjecture counterexample).
</div>

*The figures in this piece come from public reporting and the statements of those involved (as of the morning of 2026-11-21, Taipei time), not from my models; the day counts and agent-hours are my own conversions. None of the three proofs has been confirmed and any of them may yet fall, and I am not able to verify these proofs myself. Research notes, not investment advice.*
