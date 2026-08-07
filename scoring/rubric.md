# Task classification rubric — v0.1

Classify **one O\*NET task statement at a time** as `automatable`, `augmentable`,
or `human_anchored`, in the context of **a public agency**.

Round-1 findings against this rubric, including the four places it was ambiguous,
are in [`classifications_round1.md`](classifications_round1.md). Read them before
scoring anything at volume — two of them are unresolved.

---

## The distinction this rubric exists to protect

> **"A model can produce this output" and "a model can be trusted with this output
> unsupervised" are different questions.** In a private firm they mostly move
> together. In a public agency they routinely do not — authority is vested by
> statute in a named officer, outputs are appealable, and the cost of error falls
> on a member of the public rather than on the agency.

That divergence is the entire point. So the rubric scores **two independent axes**
and never averages them:

| axis | question | what moves it |
|---|---|---|
| **P — Producibility** | Can a model produce an acceptable output, from inputs that actually exist? | model capability |
| **D — Delegability** | Can that output take effect without a named human accepting responsibility for it? | law, rule, and process design |

**D is a ceiling, not a factor.** A P3 output under D0 is `human_anchored`. High
capability must never raise the class. Any scorer that averages P and D, or that
lets a "wow, a model could totally do that" reaction move the answer, has
destroyed the thing being measured.

---

## Axis P — Producibility

| | |
|---|---|
| **P0** | Not producible. Requires physical presence, real-time embodied action, or a bodily act on a person or object. |
| **P1** | Partial. A model produces some of it; a material portion still requires a human to generate, not merely to approve. |
| **P2** | Draft. A model produces a complete output that a knowledgeable human would **edit**, not rewrite. |
| **P3** | At standard. Model output meets or exceeds what the agency currently accepts, with no edit. |

Score P against **inputs the agency actually holds**, not inputs it could
theoretically collect. A task that would be P3 given a clean structured record is
P1 if the record is a scanned fax and a phone call.

## Axis D — Delegability

| | |
|---|---|
| **D0** | Never. A person or office is legally vested; delegation is void **regardless of output quality**. |
| **D1** | Signature. Output takes effect only when a named human adopts it and becomes accountable for it. |
| **D2** | Sampled. Output takes effect on its own; errors are caught by audit or downstream review. |
| **D3** | Free. Output takes effect unreviewed. Errors are cheap and reversible. |

### D0 tests — any one is sufficient

1. **Statutory or regulatory vesting.** A named officer or title must make the
   finding ("the commissioner shall determine…"). Delegation to a non-person is
   not authorized.
2. **Attestation.** A sworn statement, affidavit, or certification, where the
   value of the artifact is that *a person can be prosecuted for its falsity*.
3. **Due-process record.** The output is appealable and the agency must produce
   both a reasoned basis and a responsible human at a hearing.
4. **Custodial or coercive power over a person.** Arrest, detention, removal of a
   child, use of force, involuntary transport.
5. **Reserved professional act.** The act is restricted by license — practice of
   law, medicine, clinical social work.

### D1 triggers — any one is sufficient (absent a D0 test)

- The consequence falls on a member of the public and is not cheaply reversible.
- The error is not detectable before the output takes effect.
- The output is discoverable, FOIL-able, or admissible, and will be read as the
  agency's position.

---

## Decision procedure

Run in order. Stop at the first hit.

1. **P0?** → `human_anchored`, anchor = **capability**.
2. **Any D0 test?** → `human_anchored`, anchor = **authority**.
3. **D1?** → `augmentable`.
4. **D2 or D3, and P3?** → `automatable`.
5. **D2 or D3, and P1–P2?** → `augmentable`.

## Always record the anchor

`human_anchored` has two causes that behave in opposite ways over time, and
collapsing them makes the output useless for planning:

- **capability-anchored (P0)** — erodes as models and robotics improve. A
  technology roadmap.
- **authority-anchored (D0)** — does not move until a statute, rule, or contract
  changes. A **policy** roadmap. No amount of model progress touches it.

An agency's authority-anchored set is the honest answer to "what can't we
automate", and it is the deliverable a vendor cannot produce by benchmarking
models.

---

## Signals that do **not** count

Scoring on any of these produces a plausible, wrong answer:

- **The verb.** "Prepare reports" appears in both clerical and sworn-evidentiary
  tasks and classifies differently in each. Never score from the statement's
  syntax.
- **Difficulty, prestige, credential, or salary** of the occupation.
- **"A model can't really understand / be creative / show empathy."** Not a rubric
  axis. If it matters, it shows up as a D1 trigger or a D0 test, or it does not
  matter.
- **Headcount.** How many people do the task is a weighting question, not a
  classification question.
- **Whether the agency currently uses software for it.** Existing automation
  reflects past procurement, not delegability.

---

## Edge rules

**Compound statements.** O\*NET task statements routinely bundle clauses of
different classes ("compile, record, and evaluate … *and determine eligibility
status*"). Split into clauses, classify each, and take the **most-anchored clause
as the statement's class**. Set `compound: true` and keep the per-clause scores —
the statement-level class systematically understates the automatable share, and
the clause table is the only place that shows it.

**Context inheritance.** A statement that names no consequence ("conduct searches
to find needed information") inherits its class from whatever it feeds. Classify
at the **lowest-consequence plausible use**, set `context_dependent: true`, and do
not imagine the worst case. This is a deliberate choice to under-anchor rather
than over-anchor; see round-1 ambiguity #2, which argues it may be wrong.

**Nominal review.** Where a D1 signature is in practice a rubber stamp, record
`D1 (nominal)`. Do **not** reclassify to D2 — the accountability is real even when
the review is not. The nominal flag is where the actual deployment risk lives, and
it should drive the review-design work, not the class.

---

## Output format

```yaml
task_id: 9735                  # O*NET Task ID, verbatim
soc: 43-4061.00                # verified against onet_Occupation_Data.txt
class: human_anchored
anchor: authority              # authority | capability | n/a
P: 3
D: 0
d0_test: 1                     # which test fired, if any
compound: false
context_dependent: false
evidence: >
  One sentence, pointing at the statute, the process, or the file. Not a vibe.
confidence: high               # high | medium | low
```

`confidence` is about the **classification**, not about the model's ability. Low
confidence means the rubric did not cleanly decide — log it as an ambiguity rather
than picking and moving on.

---

## Scope limits

- The unit is one task statement. It is **not** an occupation-level score. Rolling
  clauses up to occupations requires a weighting scheme this rubric does not
  define.
- Public agencies only. D0 tests 1, 3, and 4 mostly do not exist in private firms,
  which is why private-sector automation scores do not transfer.
- The rubric classifies **the task as the agency performs it today**. Redesigning
  the process can move D. That is a finding, not a score.

---

This page includes information from the O\*NET 30.3 Database by the U.S. Department
of Labor, Employment and Training Administration (USDOL/ETA). Used under the
CC BY 4.0 license. O\*NET® is a trademark of USDOL/ETA.

TitleTrack has modified all or some of this information. USDOL/ETA has not
approved, endorsed, or tested these modifications.
