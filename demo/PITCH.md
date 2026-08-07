# TitleTrack — 3-minute pitch

Run `python demo/serve.py` first. Open `http://localhost:8765`. Have the
landing screen up before you start talking.

---

## Open (20s) — the title that lies

"A title like CITY SEASONAL AIDE tells a New Yorker almost nothing about how AI
will affect their work. It can hide many different jobs — and a generic AI risk
score gets all of them wrong. TitleTrack makes the work visible before making a
recommendation."

## The problem (30s)

550,219 people were on the New York City payroll in FY2025. Skipping just the
five largest titles that turn out not to be occupations at all removes **124,911
rows — 30.1% of top-40 headcount**: per-session teachers, election workers,
student aides, job-training participants, seasonal aides. These are the people
the "future of work" conversation reaches last, and no tool connects their actual
title to what AI means for their actual tasks — because the city's titles connect
to nothing. There is **no shared key** between payroll, exams, and occupations,
and the titles lie: `CARETAKER` is a NYCHA janitor, not a caregiver;
`TEACHER- PER SESSION` — the largest title in the city, 78,618 rows — is a pay
code, not a job.

## Demo (90s) — one worker journey

1. **Landing** → pick **TRAFFIC ENFORCEMENT AGENT**. 2,508 people, $49,830
   median, per Annum, and we say what we excluded.
2. **Role view** → real O*NET task statements, verbatim, three labels, never a
   score. Point at the prototype banner: **honesty is the feature.**
3. **The line that wins the room** → scroll to *"Write warnings and citations for
   illegally parked vehicles."* It looks like the most automatable line on the
   page. It is labeled human-anchored — **by authority, not by capability.** A
   summons is an appealable record affirmed by the agent who observed the
   violation. A model can write it perfectly and still cannot issue it. Contrast
   with *"Patrol an assigned area"* two lines up: also human, but anchored by the
   body — that one erodes as technology improves. **One score cannot say both
   things.**
4. **Action plan** → **4 open DCAS exams** with real application windows.
5. **"Explain this for me"** → live Claude call, grounded only in the page's data.
   The system prompt forbids percentages and "replaceable"; if the network dies
   mid-demo it serves a precomputed answer and says so on screen.
6. **Back → CITY SEASONAL AIDE** → the SKIP panel. "Refusing to answer is the
   right answer here, and our eval enforces it."

**If you have 20 seconds spare:** open CARETAKER. Six of its eight tasks are
human-anchored — the "low-skill" title is among the *least* exposed in the set,
and the one automatable task is the office-shaped edge (requisitioning supplies).
The intuition most people walk in with is backwards. EMT is the same shape: six
of eight human-anchored, and the one item that could erode with technology is
driving the ambulance, not treating the patient.

## Why trust it (30s)

Every number traces to a committed city snapshot. Every SOC code is verified
against the O*NET occupation file before it is written down — never cited from
memory. `python demo/evaluate.py` is a hard-fail gate that was written **before**
any demo data existed and fails the build on a forced match, an invented number,
a task statement that isn't verbatim, or any job-level aggregate score. Two of
the four crosswalk decisions behind this demo carry a flagged caveat because the
employer is not verifiable from our own snapshots — we recorded that rather than
asserting it. Our naive-matcher baseline produced **12 corrupt matches**; that is
why the discipline exists.

## Close (10s)

"We are not building a replacement score. We are building an honest navigation
tool: where AI can reduce drudgery, where humans remain accountable, and what
NYC workers can do next."

---

## Likely questions

**"Why no overall score?"** — Because we cannot compute one honestly. O*NET
publishes no clause-level weights, so rolling statement labels up to an
occupation requires inventing a weighting scheme. Our rubric documents this as an
unresolved ambiguity (A1) and our eval bans the aggregate keys outright.

**"How accurate are the labels?"** — They are a prototype at v0.1 and the page
says so. The task text is published federal data shown verbatim; the label is our
judgment and needs worker validation. That is the next piece of work, and it needs
workers, not a bigger model.

**"Isn't this just Frey & Osborne?"** — The opposite. Occupation-level exposure
scores are what we are refusing to produce. We score two axes and never average
them: can a model produce this output, and can that output take effect without a
named human accountable for it. The second is a law-and-process question that no
model release moves.

**"What's next?"** — Fill the remaining 23 crosswalk decisions, validate labels
with DC 37 / PBA / UFT members, and add the promotion ladder so the exam screen
shows the next rung, not just the next test.

---

This page includes information from the O*NET 30.3 Database by the U.S. Department
of Labor, Employment and Training Administration (USDOL/ETA). Used under the
CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA.

TitleTrack has modified all or some of this information. USDOL/ETA has not
approved, endorsed, or tested these modifications.
