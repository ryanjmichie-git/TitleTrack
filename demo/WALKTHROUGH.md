# TitleTrack — the narrative

*The spoken version. Keep this open next to the laptop.*

---

## The one-sentence pitch

**"Pick your city job title, see what AI actually means for your work task-by-task —
no fake risk scores — and see the exam that's your next move up."**

---

## Why this exists

Right now, if you're a New York City worker and you wonder *"is AI coming for my
job?"*, your options are headlines and generic "40% of jobs at risk" scores. Those
scores are usually wrong, because they treat a job title like it's one thing. The
city's own data proves it isn't: **`CARETAKER` is a NYCHA janitor, not a caregiver.
`TEACHER- PER SESSION` — 78,618 people, the largest title in the city — isn't a job
at all, it's a pay code. `LIEUTENANT` is two completely different jobs depending on
whether you're NYPD or FDNY, and they map to different occupation codes.**

TitleTrack answers the question honestly, one task at a time, using the city's own
data — and then points to a concrete next step instead of just a verdict.

## Who it's for

The **550,219 people** on NYC's payroll — and specifically the ones the organizers
asked us to think about, not the office 9-to-5ers. The titles in this demo are a
traffic enforcement agent, a school safety agent, an EMT, a NYCHA caretaker, an
NYPD sergeant. Hourly, frontline, uniformed. The people generic career tools ignore.

## Why it helps them

1. **It's about their actual job.** They pick their real payroll title and see the
   real tasks that job involves — published federal task statements shown verbatim —
   not a national average for some vaguely similar occupation.
2. **It doesn't scare or lie.** Each task gets one of three labels: *AI could do much
   of this / AI assists but a person decides / this stays with people.* There is
   deliberately **no overall risk score**, because our own methodology shows no
   honest one exists.
3. **It says *why* the work stays human — and this is the part nobody else has.**
   Two tasks can both be labeled "stays with people" for opposite reasons. One stays
   human because it **needs a body present** — that erodes as technology improves.
   The other stays human because **the law vests the act in a person** — no model
   release ever touches that. One is a technology roadmap. The other is a policy
   roadmap. A single risk score erases the difference.
4. **It gives them a move to make.** The last screens show open DCAS exams for their
   title *and* their real promotional next rung — which in civil service is literally
   the mechanism for getting promoted or changing jobs. That's the "AI lifts workers"
   part of the brief.

---

# The walkthrough

**Before you start:** `$env:ANTHROPIC_API_KEY = "..."` then `python demo/serve.py`.
Open `http://localhost:8765`. Landing screen up before you talk.

### Screen 1 — Landing (15s)

> "How might AI change *your* work? Twelve of the forty largest titles in New York
> City. Not the ones you'd expect."

Type **`safety`** in the search box. One tile.

### Screen 2 — School Safety Agent (45s)

> "Marisol. 4,017 people hold this title, median $56,508. She's read every headline
> about AI. Nobody has ever shown her *which parts* of her job."

Point at the three collapsible categories.

> "Her actual work — published federal task data, shown word for word. We sorted it
> into three buckets so she isn't reading a wall of text."

Open **"AI could do much of this."** One task: answering off-hours phone calls.
Open **"Stays with people."**

> "And here's the one that decides the whole argument."

Point at *"Warn persons of rule infractions… and apprehend or evict violators, using
force when necessary."*

> "Read the line underneath: **stays human because the law vests it in a person.**
> Coercive power over another person is vested by statute. A model could write the
> report perfectly and still not be allowed to do this. Now look two rows up —
> *patrol the premises* — **stays human because of the body.** Also human, but that
> one erodes as technology improves. **Same label. Opposite futures. One score cannot
> say both things.**"

### Screen 3 — Her next move (25s)

> "Three open exams, linked straight to the DCAS application page. And below that,
> her real next rung: Supervisor of School Security. $74,344 against the $39,206 she
> started at."

Point at the grey line.

> "Note what that says — *most recent cycles, not open filing windows.* Promotional
> exams run on irregular cycles, windows are about three weeks, and DCAS sends you no
> notice when you become eligible. That gap is half the problem."

*(The Indeed and Coursera cards are badged **illustrative partnership** — mention only
if asked: "mock handoff, a real version passes her title and SOC code through.")*

### The live call (20s)

Hit **Explain**.

> "That's Claude, writing live, grounded only in the verified data on this page. The
> system prompt forbids percentages, forbids the word replaceable. If the network
> dies it serves a precomputed answer and says so on screen — the demo never depends
> on the wifi."

### The killer moment (30s)

Back → search **`seasonal`** → **CITY SEASONAL AIDE**.

> "And here's where it refuses."

> "This title isn't a job. It's a hiring category — 17 salaried rows out of 2,414,
> covering a lifeguard, a parks crew member, and an office temp. Any score here is
> wrong for every single one of them. **Every other demo today will answer every
> question you ask it. Ours knows when the honest answer is 'that's the wrong
> question' — and our eval fails the build if we ever fill this in with a guess.**"

If you have 10 more seconds, search **`teacher`**:

> "Same refusal on the largest title in the entire city. 78,618 people. It's a pay
> code for teachers working after-school hours — the same people already counted
> somewhere else. Skipping the five titles like this removes 30% of top-40 headcount.
> That's a finding, not a gap."

### The inversion, if time allows (20s)

Search **`sergeant`**, then **`caretaker`** or **`EMT`**.

> "The sergeant's human-anchored work is *all* authority-anchored — none of it moves,
> ever. The caretaker's and the EMT's is *all* capability-anchored — six of eight
> tasks each, and the one thing on the EMT's list that technology might actually
> change is driving the ambulance, not treating the patient. **The 'low-skill' titles
> are the least exposed in our whole dataset. The intuition everyone walks in with is
> backwards.**"

### Close (15s)

> "We are not building a replacement score. We're building an honest navigation tool:
> where AI can reduce drudgery, where humans stay accountable, and what a New Yorker
> can do next. Pick your title, see your tasks, find your exam."

---

## The three things to say if you only get one minute

1. **"No risk score, on purpose."** Arntz et al. held the method constant and changed
   only the unit of analysis — US "high-risk" employment moved from **38% to 9%**.
   The scary number is an artifact of aggregation, not of technology.
2. **"Two kinds of human."** Capability-anchored erodes; authority-anchored doesn't.
   That distinction is the product.
3. **"It knows when to refuse."** And a gated eval enforces the refusal.

---

## Demo-failure drill

| If | Say |
|---|---|
| Explain falls back | "That's the precomputed answer — the fallback is by design." |
| Wifi dies entirely | Everything but Explain is local. Keep going. |
| Anything else | `python demo/evaluate.py` in a spare terminal. `GATE PASSED` on screen is a good ten seconds. |
