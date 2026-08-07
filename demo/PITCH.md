# TitleTrack — 3-minute pitch

Run `python demo/serve.py` first (with `$env:ANTHROPIC_API_KEY` set, for the live
panel). Open `http://localhost:8765`. Have the landing screen up before you talk.

**Target: the working product is on screen by 0:90.** Roughly 400 words at a
deliberate pace. Problem ~30s · demo ~90s · proof ~30s · ask ~25s.

---

## Open (20s) — one person, one problem

"Marisol is a School Safety Agent. She's 44, she's been in the title six years,
and she makes $56,508. Every headline she reads says AI is coming for her job.
Nobody has ever shown her *which parts* — and the one tool that could tell her,
the city's own data, doesn't connect to itself."

Then: "A title like CITY SEASONAL AIDE tells a New Yorker almost nothing about
their work. A generic AI risk score gets all of them wrong. TitleTrack makes the
work visible before it makes a recommendation."

## The problem (30s)

550,219 people were on the NYC payroll in FY2025. Their titles connect to
**nothing** — there is no shared key between payroll, exams, and occupations, and
the titles lie: `CARETAKER` is a NYCHA janitor, not a caregiver;
`TEACHER- PER SESSION`, the largest title in the city at 78,618 rows, is a pay
code, not a job. Skipping the five largest titles that aren't occupations removes
**124,911 rows — 30.1% of top-40 headcount.**

And the mobility system underneath is **pull, not push**: DCAS sends no notice
when you become eligible for a promotional exam. Filing windows run about three
weeks. Exam-to-hire is, by DCAS's own testimony, a best-case **14–15 months**,
with a **290-day median just to release scores**. If you're provisional — and the
provisional count *rose* from 11,337 to 13,359 between Aug 2024 and Nov 2025 —
you can't sit a promotional exam at all.

## Demo (90s) — Marisol's journey, one flow

1. **Landing** → click **SCHOOL SAFETY AGENT**. 4,017 people, $56,508 median, per
   Annum, and we say what we excluded.
2. **Role view** → real O*NET task statements, verbatim, three labels, never a
   score. Point at the prototype banner: **honesty is the feature.**
3. **The line that wins the room** → *"Warn persons of rule infractions… and
   apprehend or evict violators, using force when necessary."* Human-anchored **by
   authority** — coercive power over a person is vested in a human, and no model
   release changes that. Two lines up, *"Patrol industrial or commercial
   premises"* is also human — but anchored by **the body**, which technology can
   change. **One score cannot say both things.** And *"Answer telephone calls to
   take messages"* is the one task labeled automatable.
4. **The next rung** → Supervisor of School Security, Exam 2547, $74,344 against
   her $39,206 start. Note the dashed border and the amber box: this block is
   externally researched and **labeled as such**, because every other number on
   the page is re-derived from a committed city snapshot and this one isn't.
5. **"Explain this for me"** → live Claude call, grounded only in this page's
   data. The system prompt forbids percentages and "replaceable." If the network
   dies it serves a precomputed answer and says so on screen.
6. **Back → CITY SEASONAL AIDE** → the SKIP panel. "Refusing to answer is the
   right answer here, and our eval fails the build if we ever fill it in."

**If you have 20 seconds spare:** open CARETAKER. Six of its eight tasks are
human-anchored — the "low-skill" title is among the *least* exposed, and the one
automatable task is the office-shaped edge (requisitioning supplies). EMT is the
same shape: six of eight, and the one item that erodes with technology is driving
the ambulance, not treating the patient. **The intuition most people walk in with
is backwards.**

## Why trust it (30s)

Every number traces to a committed city snapshot. Every SOC code is verified
against the O*NET occupation file before it is written down — never cited from
memory. `python demo/evaluate.py` is a hard-fail gate **written before any demo
data existed**; it fails the build on a forced match, an invented number, a task
statement that isn't verbatim, or any job-level aggregate score. Two of our four
crosswalk decisions carry a flagged caveat because the employer isn't verifiable
from our own snapshots — we recorded that rather than asserting it. Our naive
matcher produced **12 corrupt matches**; that's why the discipline exists.

## The ask (25s)

"We want a pilot with **DCAS and one union education fund — Local 237 covers both
School Safety Agents and NYCHA caretakers.** Two things we need: worker validation
sessions to test whether these labels match the actual job, and permission to wire
the eligibility feed so a worker gets told when their window opens instead of
finding out after it closed. With that, Marisol learns which parts of her job are
changing — and files on day one of a three-week window instead of missing it."

---

## Likely questions

**"Why no overall score?"** — Because no honest one exists, and this is the
best-documented finding in the field. Arntz, Gregory & Zierahn (2017, *Economics
Letters*) hold the method constant and vary **only** the unit of analysis: US
"high-risk" employment drops **from 38% to 9%**. The scary number is an artifact
of aggregation, not a property of the technology. Brynjolfsson, Mitchell & Rock
(2018) measured the within-occupation standard deviation of task machine-learning
suitability at **0.596** and concluded "few occupations are fully automatable."
Concretely for us: O*NET publishes no clause-level weights, so rolling statement
labels up to an occupation would require inventing a weighting scheme. Our rubric
logs that as unresolved ambiguity A1, and our eval bans the aggregate keys.

**"Isn't this just Frey & Osborne?"** — The opposite; that's the thing we're
refusing to build. Their 47% figure came from a Gaussian process classifier
trained on ~70 hand-labeled occupations and assumed *whole occupations* are
automated. Tested against actual 2013–2018 US employment change, Coelli & Borland
(2019) found it "does not add value for forecasting." Every credible post-2016
measure — OECD, Eloundou et al., Brynjolfsson–Mitchell–Rock, Felten et al.,
Acemoglu 2024, the Anthropic Economic Index — is built from **tasks**. Task-level
is the mainstream, not the outlier.

**"Doesn't exposure mean displacement?"** — No, and the authors say so. Eloundou
et al. (2024, *Science*): "technical feasibility does not guarantee labor
productivity or automation outcomes." Svanberg et al. (MIT, 2024) found only
**~23%** of wages paid for vision tasks are currently cost-effective to automate.
And Autor (2015) and Acemoglu & Restrepo (2019) show partial task automation can
*raise* demand for an occupation — meaning an occupation-level risk score can have
the wrong sign. Hinton said in 2016 to stop training radiologists; Mayo's
radiology staff grew 55%.

**"Aren't occupation scores more useful for policy?"** — They're more
*communicable*, which is exactly why "47%" got repeated as "47% of jobs will be
lost," which the paper never claimed. Task scores can be aggregated when a
question needs it and disaggregated back to the driving tasks. An occupation score
can't — information is destroyed at the point of aggregation.

**"How accurate are your labels?"** — They're a prototype at v0.1 and the page
says so. Task text is published federal data shown verbatim; the label is our
judgment. Validating it needs workers, not a bigger model — which is the ask.

**"Why does that block look different?"** — Deliberately. The next-rung data is
externally researched and not re-derivable from our snapshots, so it gets a dashed
border and a labeled disclaimer. If a derived value renders identically to a
verified fact, you've used civic design language to launder a derivation.

**"What's next?"** — Fill the remaining 23 crosswalk decisions; validate labels
with DC 37 / Local 237 / Local 2507 members; wire the DCAS schedule feed
(Socrata `4ptz-hmtc`, refreshed monthly) to push a notice ~30 days before a
worker's window opens.

---

## Demo-failure drill

- **Live Claude call fails** → it already fell back and labeled itself. Say:
  "that's the precomputed answer — the fallback is by design, the demo never
  depends on the network."
- **Wifi dies entirely** → everything except the Explain button is local. Keep going.
- **Anything else** → `python demo/evaluate.py` in a spare terminal. `GATE PASSED`
  on screen is itself a good 10 seconds.

---

This page includes information from the O*NET 30.3 Database by the U.S. Department
of Labor, Employment and Training Administration (USDOL/ETA). Used under the
CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA.

TitleTrack has modified all or some of this information. USDOL/ETA has not
approved, endorsed, or tested these modifications.
