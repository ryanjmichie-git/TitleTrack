# Round 1 — five hand-classified task statements

Scored one at a time against [`rubric.md`](rubric.md) v0.1, no batching. Task text
is verbatim from `data/raw/onet_Task_Statements.txt`; every SOC code was checked
against `data/raw/onet_Occupation_Data.txt`.

The five were chosen to **stress** the rubric, not to exercise it. Each probes a
different failure mode: a compound statement, the pure authority case, an
evidentiary record that looks clerical, a near-identical verb phrase in a
different occupation, and a statement with no consequence on its face.

All five occupations are in the FY2025 top-40 crosswalk, so these are NYC titles
with real headcount, not hypotheticals.

---

## 1 · Task 9736 — Eligibility Interviewers, Government Programs (`43-4061.00`)

> Compile, record, and evaluate personal and financial data to verify completeness
> and accuracy, and to determine eligibility status.

*NYC title: `ELIGIBILITY SPECIALIST`, 2,275 staff (H14).*

Compound. Three clauses, two classes:

| clause | P | D | class |
|---|---|---|---|
| compile, record … data | 3 | 3 | `automatable` |
| evaluate … to verify completeness and accuracy | 3 | 2 | `automatable` |
| **…and to determine eligibility status** | **3** | **0** | **`human_anchored`** |

```yaml
task_id: 9736
soc: 43-4061.00
class: human_anchored
anchor: authority
P: 3
D: 0
d0_test: 1          # and 3 — determination is appealable via fair hearing
compound: true
context_dependent: false
evidence: >
  Eligibility determinations for public assistance are made by the agency under
  regulation and are appealable; the determination must have a reasoned basis and
  a responsible human at the hearing. The compile/verify clauses carry none of
  that.
confidence: high
```

**This is the rubric's central case and its central problem.** Two of three
clauses are `automatable` at P3, and the statement-level label is
`human_anchored`. The label is correct and it hides most of the work. See
ambiguity **A1**.

---

## 2 · Task 9735 — Eligibility Interviewers, Government Programs (`43-4061.00`)

> Initiate procedures to grant, modify, deny, or terminate assistance, or refer
> applicants to other agencies for assistance.

```yaml
task_id: 9735
soc: 43-4061.00
class: human_anchored
anchor: authority
P: 3
D: 0
d0_test: 3          # and 1
compound: true      # the "refer applicants" clause is D2 / augmentable
context_dependent: false
evidence: >
  Termination of assistance is the canonical due-process case: the recipient is
  entitled to notice and a hearing, and the agency must produce a reasoned basis
  and an accountable human. Producibility is not the binding constraint.
confidence: high
```

**P3 / D0 — the gap the rubric exists to show.** A model can write the
determination and the notice to a standard the agency would accept today. It
still cannot issue them. Nothing about model capability moves this; only a change
in statute or delegation rule does. This is the case that justifies scoring two
axes instead of one, and it classified cleanly and for the right reason.

---

## 3 · Task 23053 — Police and Sheriff's Patrol Officers (`33-3051.00`)

> Record facts to prepare reports that document incidents and activities.

*NYC title: `POLICE OFFICER`, 24,153 staff (H01).*

```yaml
task_id: 23053
soc: 33-3051.00
class: augmentable
anchor: n/a
P: 2
D: 1 (nominal)
d0_test: null       # see below — test 2 nearly fires
compound: false
context_dependent: false
evidence: >
  The incident report is discoverable and admissible and will be read as the
  officer's account. The officer signs it. But a routine incident report is
  signed, not sworn — the sworn artifact is the criminal court complaint derived
  from it — so D0 test 2 as written does not fire.
confidence: low
```

Chosen because it **looks** clerical. "Record facts to prepare reports" is
syntactically indistinguishable from filing. It is the evidentiary foundation of
a prosecution.

`D1 (nominal)` is flagged deliberately: drafting assistance on incident reports is
precisely where a signature degrades into a rubber stamp, and the artifact is
evidence. Under the rubric this does not change the class — but it is the single
highest-risk item in this set, and the class alone does not say so. Ambiguity
**A3**.

---

## 4 · Task 237 — Child, Family, and School Social Workers (`21-1021.00`)

> Maintain case history records and prepare reports.

*NYC titles: `CHILD PROTECTIVE SPECIALIST` 2,958 (H09) and `SCHOOL SOCIAL WORKER`
2,638 (H11).*

```yaml
task_id: 237
soc: 21-1021.00
class: augmentable
anchor: n/a
P: 2
D: 1
d0_test: null
compound: false
context_dependent: false
evidence: >
  The case record feeds custody and protective proceedings (see task 243, same
  occupation, "assisting with hearings and providing testimony"). Consequence
  falls on a child and is not cheaply reversible. Record maintenance is incidental
  to the reserved clinical act rather than being it, so D0 test 5 does not fire.
confidence: medium
```

Selected as a near-duplicate of #3 — *"prepare reports"* in both — to test whether
the rubric discriminates on context rather than syntax.

**It did not.** Both landed `augmentable / P2 / D1`. I expected the child-welfare
record to anchor harder than the police report and it does not, because both reach
D1 by the same route (evidentiary use, irreversible consequence) and the rubric has
no rung above D1 short of D0. That is a real limitation, not a tidy result.
Ambiguity **A4**.

---

## 5 · Task 2805 — Secretaries and Administrative Assistants (`43-6014.00`)

> Conduct searches to find needed information, using such sources as the Internet.

*NYC titles: `PRINCIPAL ADMINISTRATIVE ASSOCIATE - NON SUPVR` 4,242 (M06),
`SCHOOL SECRETARY` 3,305 (H08).*

```yaml
task_id: 2805
soc: 43-6014.00
class: automatable
anchor: n/a
P: 3
D: 3
d0_test: null
compound: false
context_dependent: true
evidence: >
  The statement names no consequence and no consumer of the output. Under the
  context-inheritance rule it is classified at the lowest-consequence plausible
  use — locating a form, a vendor, a phone number — which is D3.
confidence: low
```

The only `automatable` in the set, and it is the one I trust least. "Needed
information" is undefined: the identical task supporting an eligibility
determination inherits that determination's anchoring. The rubric's under-anchor
rule produced this answer by fiat, not by evidence. Ambiguity **A2**.

---

# Where the rubric was ambiguous

Four places. **A1 and A2 are unresolved and will distort any scoring run.**

### A1 · Compound statements make the statement-level class misleading — unresolved

O\*NET task statements bundle clauses of different classes. Task 9736 is two
`automatable` clauses and one `human_anchored` clause; the rubric's max-anchor
rule labels the statement `human_anchored`, which is correct and deeply
misleading.

The damage appears on aggregation. Roll statement-level classes up to the
occupation and `ELIGIBILITY SPECIALIST` reads as largely un-automatable, when the
majority of the actual *work* — compiling, verifying, drafting the notice — is
`automatable` and only the determination is not.

**Why it is unresolved:** correcting it needs clause-level weights, and O\*NET
publishes none. `Incumbents Responding` is per statement, not per clause. Any
weighting would be invented. Until that is settled, **statement-level classes must
not be aggregated to occupation level** — the clause table is the real output.

### A2 · Context inheritance is decided by fiat — unresolved

Task 2805 has no consequence on its face. The rubric says classify at the
lowest-consequence plausible use, which yields `automatable`. In an agency where
that research feeds determinations, that is wrong.

The rule picks a side with no justification beyond a preference for
under-anchoring. Three defensible options, and v0.1 does not argue for the one it
chose:

1. under-anchor (current) — risks calling anchored work automatable;
2. over-anchor — risks the opposite and makes the whole rubric conservative;
3. refuse to classify context-free statements, and require an agency process map.

I lean to (3): it is the honest answer, and it forces the process mapping the
product needs anyway. It also means a meaningful share of O\*NET statements are
**not classifiable from the task file alone** — worth knowing before promising
coverage.

### A3 · The attestation test is binary and the world is not — resolvable

D0 test 2 says "sworn". A routine police incident report is *signed and
evidentiary* but not sworn, so it falls to D1 and #3 came out `augmentable`. Its
practical accountability is much closer to D0.

**Proposed fix:** widen test 2 to *"sworn, **or** admissible as the agency's
evidentiary record of the event."* That would move task 23053 to
`human_anchored / authority`. I did **not** apply it — it would reclassify a large
family of tasks and should be a deliberate decision, not a mid-scoring
adjustment.

### A4 · Low resolution in the "records and reports" family — needs a sub-axis

Tasks 23053 and 237 are different occupations with very different stakes and
identical scores. Essentially every "maintain records / prepare reports" statement
will land on `augmentable / D1`, because D1's triggers are broad and there is no
rung between D1 and D0.

Records-and-reports statements are a large share of public-agency task text, so
the rubric's most frequent output is also its least informative. Fixing A3 splits
this family properly; a sub-axis on *who reads the record and what it can do to a
person* would split it better.

---

## What worked

The P/D separation earned itself on task 9735: `P3 / D0`, `human_anchored`,
authority-anchored. A single-axis "can AI do this" score returns *yes* and is
useless to the agency. Recording the **anchor** is what makes the output
actionable — the authority-anchored set is a policy roadmap that no model release
will shrink, and it is the part a capability benchmark cannot produce.

## Suggested v0.2 changes

1. Adopt A3's widened attestation test — deliberately, as its own change.
2. Decide A2 explicitly. My recommendation is option (3), refuse-and-flag.
3. Add the A4 sub-axis for evidentiary records.
4. State in the rubric that statement-level classes must not be aggregated to
   occupations until A1 has a weighting scheme.

---

This page includes information from the O\*NET 30.3 Database by the U.S. Department
of Labor, Employment and Training Administration (USDOL/ETA). Used under the
CC BY 4.0 license. O\*NET® is a trademark of USDOL/ETA.

TitleTrack has modified all or some of this information. USDOL/ETA has not
approved, endorsed, or tested these modifications.
