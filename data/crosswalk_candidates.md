# Crosswalk candidates — NYC payroll title → O*NET SOC

Top 40 FY2025 payroll titles by headcount. Three SOC candidates each.
**Ordered worst-confidence first** — the ones that need your judgment are at the top,
the obvious ones are at the bottom. Stop whenever you get bored; you'll have covered
the hard ones.

Sources: `k397-673e` FY2025 (payroll), O*NET **30.3** `Occupation Data` +
`Job Titles` + `Sample of Reported Titles`. Every SOC code below was verified to
exist in `Occupation Data.txt` — none are from memory.

**Confidence means:** `high` = one obviously correct code. `medium` = right
occupational family, wrong-or-unknown sub-code. `low` = the payroll title is not
an occupation, or is too ambiguous to resolve without agency context.

`median` is per-Annum-only; `—` means the title has no salaried rows at all.

Fill in `DECISION:` with a SOC code, `SKIP`, or a note.

**Status 2026-08-07: the 13 `low` items are decided (L01–L13). The 27 `medium` and
`high` items are still open.** The verdict vocabulary and the two rules used are
defined at the head of the LOW section; apply the same ones to the remaining 27.

> **13 of 40 are `low`.** That is the real finding here. See the euphemism section
> immediately below — most low-confidence cases are not hard matching problems,
> they are titles that do not describe an occupation at all.
>
> That held up under review: of the 13, **five are not occupations** (`SKIP`,
> 124,911 rows) and **two more are real work that no single SOC code spans**
> (14,089 rows). Only one of the 13 turned out to be a genuine matching problem
> awaiting data (L09). Deciding them also surfaced a factual error in this file and
> in `CLAUDE.md` — see the correction on flag #8.

---

# ⚠️ Euphemism / misleading-name flags

Titles where the payroll name does not describe the actual duties. **Read this
before deciding anything below** — several of these will make you change your answer.

### 1. `TEACHER- PER SESSION` — not a job. A pay code.
The single largest "title" in the city at 78,618 rows. Per-session is the DOE
mechanism for paying *existing* teachers hourly for work beyond the school day —
after-school, coaching, summer, professional development. **These are overwhelmingly
the same people already counted under `TEACHER`.** Treating it as 78,618 workers
double-counts the teaching workforce. Its `median` is null precisely because no one
holds it as a salaried job.

### 2. `CARETAKER` — a janitor, not a caregiver.
NYCHA Caretaker cleans buildings, removes refuse, and does grounds work. The word
pulls matchers toward `31-1122 Personal Care Aides` and `39-2021 Animal Caretakers`.
Both are wrong. This is the clearest homonym trap in the set.

### 3. `PRINCIPAL ADMINISTRATIVE ASSOCIATE` — not a principal, not an associate.
"Principal" is a civil-service seniority grade, not a school leader. "Associate"
is not a partner. It is a senior clerical/administrative title, and this variant
is explicitly tagged `NON SUPVR`.

### 4. `ADMINISTRATIVE STAFF ANALYST` — a manager, not an analyst.
In NYC, the `Administrative ___` prefix marks a managerial (M-level) title. The
$128,296 median is the tell — that is manager pay, not analyst pay. Mapping it to
an analyst SOC understates the seniority.

### 5. `COMMUNITY COORDINATOR` / `COMMUNITY ASSOCIATE` — generic administrative ladder.
These are broadband titles used across dozens of agencies for wildly different
work: outreach in one agency, pure back-office admin in another. The word
"community" is frequently vestigial. No single SOC is honest for the whole group.

### 6. `JOB TRAINING PARTICIPANT` / `CITY SEASONAL AIDE` / `STUDENT AIDE` — hiring categories.
These describe *how someone was hired* (program enrollee, seasonal, student), not
what they do. Duties vary arbitrarily across incumbents. Note `JOB TRAINING
PARTICIPANT` has 18 salaried rows out of 4,021, and `CITY SEASONAL AIDE` 17 of 2,414.

### 7. `ELECTION WORKER` — a civic role, not an occupation.
36,517 rows, zero salaried. Poll workers serve a handful of days per year for a
stipend. O*NET has no corresponding occupation because it is not a career.

### 8. `COLLEGE ASSISTANT` — CUNY catch-all.
One hourly title covering tutors, lab techs, office staff, and IT help.

> **CORRECTED 2026-08-07.** This flag used to add "CUNY is barely present in the
> payroll file (217 rows citywide)." **That is wrong.** The 217 figure is
> `CUNY CENTRAL OFFICE` alone. CUNY's community colleges are in `k397_agencies_2025.json`
> under their own names and were missed because the check keyed on the string `CUNY`:
> `COMMUNITY COLLEGE (MANHATTAN)` 4,897 · `(LAGUARDIA)` 4,201 · `(KINGSBORO)` 3,232 ·
> `(QUEENSBORO)` 2,783 · `(BRONX)` 2,275 · `(HOSTOS)` 1,907 · `GUTTMAN COMMUNITY COLLEGE`
> 568 — **19,863 FY2025 rows**, 20,080 with Central Office.
>
> The real split is community vs senior: no senior college (Hunter, Baruch, City,
> Brooklyn, Queens, John Jay…) appears anywhere in the 158-agency list, consistent
> with community colleges being city-funded and senior colleges state-funded. So
> CUNY *community college* staff are well represented and CUNY *senior college*
> staff are absent entirely. "CUNY matches are low confidence" is not supportable
> as stated — it depends which CUNY.
>
> Affects L06 and L11 (both upgraded), the `caveats` string in `top40_titles.json`,
> and the employer-check bullet in `CLAUDE.md`.

### 9. `SERGEANT-` / `LIEUTENANT` — which uniformed service?
These map to *different* SOC codes (`33-1012` vs `33-1021`) and the payroll title
alone cannot tell you. The trailing hyphen on `SERGEANT-` is a data artifact, not
part of the name.

> **NARROWED 2026-08-07.** This flag treated both ranks as equally ambiguous. The
> DCAS exam file does not: across all 2,901 rows the only Sergeant exams are
> `Sergeant (Police) (Prom)` and `Sergeant (Police) (Pro)` — **zero** fire or
> correction Sergeant exams — while Lieutenant appears as *both*
> `Lieutenant (Police) (Prom)` and `Lieutenant (Fire) (Prom)`. Consistent with the
> FDNY ladder going Firefighter → Lieutenant with no Sergeant rank.
>
> So the ambiguity is real for `LIEUTENANT` and largely not real for `SERGEANT-`.
> Exam evidence is indirect — it shows which ranks DCAS tests, not who holds them —
> so it narrows L07 rather than closing it.

### 10. `P.O. DA DET GR3` — a detective-grade investigator, not a patrol officer.
Unreadable without decoding, and not a patrol officer despite the `P.O.` prefix.

> **GLOSS UNVERIFIED 2026-08-07.** This flag expanded `DA` as "District Attorney"
> with no source. The headcount makes that strained: the title has 3,330 FY2025
> rows and *all six* DA offices together have 6,993 rows, so the reading requires
> 48% of every DA-office employee to be a detective investigator, in offices
> staffed mainly by ADAs and support. The competing expansion — `D/A` = "Detailed
> As", i.e. a police officer detailed as Detective 3rd Grade, an NYPD payroll
> convention — fits both the headcount and the `GR3` grade notation better.
>
> **RESOLVED later the same day**, from inside `k397_all_titles.json` itself: the
> payroll universe contains `CAPTAIN D/A DEPUTY CHIEF`, `CAPTAIN D/A INSPECTOR`,
> etc. in parallel with fully spelled `CAPTAIN DETAILED AS ASSISTANT CHIEF`,
> `CAPTAIN DETAILED AS CHIEF OF DETECTIVES`, etc. — the same convention in both
> spellings. `D/A` = **"Detailed As"**. `P.O. DA DET GR3` is a Police Officer
> detailed as Detective Grade 3. The "District Attorney" gloss is dead; L08's
> `33-3021.00` stands, now on firmer ground.

### 11. `ED PARA` — paraprofessional, i.e. a teaching assistant.
`ANNUAL ED PARA` and `SUBSTITUTE ED PARA` are classroom paraprofessionals. The
abbreviation defeats exact matching entirely, and "PARA" reads as a prefix rather
than a noun.

---

# LOW confidence

**All 13 decided 2026-08-07.** Four verdicts are used, and the distinction between
the first two is the one that matters:

| verdict | meaning | effect |
|---|---|---|
| `SKIP` | the title is **not an occupation** — a pay code, hiring category, or civic role | dropping it **improves** the analysis |
| `NO SINGLE CODE` | real workers doing real jobs that split across SOC **major groups**, with no residual spanning them | dropping it **loses** people; keep the bucket visible |
| a SOC code | assigned, with the precision it actually supports | family-level unless stated |
| `BLOCKED` | one specific query resolves it; the query is given | do not guess in the meantime |

Two rules were applied consistently:

1. **Prefer the family residual (`… , All Other`) when the candidate codes disagree
   about the *nature* of the work; prefer a specific code when they agree on the
   work and differ only on detail.** Assigning a specific code asserts detail the
   payroll file does not carry.
2. **Never let a lexical match outrank an evidentiary one.** Several candidates
   below exist only because a scorer ranked them; they are marked.

Headcount outcome across the 13 (of 414,667 top-40 rows):
`SKIP` 124,911 (30.1%) · `NO SINGLE CODE` 14,089 (3.4%) · `BLOCKED` 3,076 (0.7%) ·
coded 23,021 (5.6%). The 13 low-confidence titles are **165,097 rows, 39.8%** of
top-40 headcount.

---

## L01 · TEACHER- PER SESSION
`low` · 78,618 staff · median — · 0 open exams

**1. `SKIP`** — do not code as an occupation
Per-session is an hourly pay mechanism for existing teachers, not a job. See flag #1.

**2. `25-3031.00`** Substitute Teachers, Short-Term
Only if you can confirm a subset is genuinely coverage work rather than extra duty.

**3. `25-2031.00`** Secondary School Teachers, Except Special and Career/Technical Education
Fallback if you decide to fold these rows into the parent teaching title.

*Why low:* the largest title in the city is a payroll artifact. Coding it at all
risks double-counting ~78k people already present under `TEACHER`.

DECISION: **`SKIP`** — pay code, not an occupation.
New corroboration: `k397_agencies_2025.json` carries a payroll *agency* literally
named `DEPT OF ED PER SESSION TEACHER` with **81,516** FY2025 rows, alongside
`DEPT OF ED PEDAGOGICAL` (107,754) and `DEPT OF ED PER DIEM TEACHERS` (16,358).
Per-session is an accounting bucket at the agency level, not a job — that plus the
null median settles it. Report the 78,618 as a documented exclusion, never as
headcount. Do **not** take candidate 3; folding these rows into a teaching SOC is
the double-count the flag warns about.

---

## L02 · ELECTION WORKER
`low` · 36,517 staff · median — · 0 open exams

**1. `SKIP`** — civic stipend role, not an occupation
No O*NET occupation corresponds. See flag #7.

**2. `43-4199.00`** Information and Record Clerks, All Other
Residual bucket; matched via the alternate title "Election Clerk".

**3. `43-9061.00`** Office Clerks, General
Also carries "Election Clerk" as an alternate. Generic, but defensible.

*Why low:* both non-skip options are residual "All Other" codes. Third-largest
title in the city and O*NET simply has no home for it.

DECISION: **`SKIP`** — civic stipend role, not an occupation.
Corroborated the same way as L01: there is a dedicated payroll agency
`BOARD OF ELECTION POLL WORKERS` with **36,732** rows — within 215 of this title's
36,517 — kept separate from `BOARD OF ELECTION` (1,027), which is the actual
year-round staff. The city's own payroll structure treats poll workers as a
distinct non-staff population. Zero salaried rows. Both alternatives are "All
Other" residuals that would launder a stipend into an occupation.

---

## L03 · F/T SCHOOL AIDE
`low` · 9,217 staff · median — · 0 open exams

**1. `25-9042.00`** Teaching Assistants, Preschool, Elementary, Middle, and Secondary School, Except Special Education
Correct if the aide is classroom-assigned.

**2. `43-9061.00`** Office Clerks, General
Correct if school-office assigned — a large share of School Aides are.

**3. `35-9011.00`** Dining Room and Cafeteria Attendants and Bartender Helpers
Correct if cafeteria/lunchroom-assigned, also common.

*Why low:* one title, three genuinely different jobs, split by school assignment
that payroll does not record. Zero salaried rows.

DECISION: **`NO SINGLE CODE`** — retain as a visible unresolved bucket (9,217).
This is **not** a `SKIP`. These are real workers doing real jobs; the blocker is
that the three candidates sit in three different SOC *major groups* — 25
(education), 43 (office), 35 (food service) — so no "All Other" residual spans
them and rule 1 has nothing to fall back on. Any single pick misclassifies the
majority.
Resolver: DOE school-assignment data. It is **not** in `k397-673e` and no other
field proxies it, so this cannot be closed from the current sources — treat it as
a standing gap, not a to-do. Report the 9,217 separately from the L01/L02 skips;
the reasons are different and merging them misstates both.

---

## L04 · COMMUNITY COORDINATOR
`low` · 6,604 staff · median $74,363 · 0 open exams

**1. `11-9151.00`** Social and Community Service Managers
Best fit where the role is genuine community programming; alternate title
"Community Outreach Coordinator" matches directly.

**2. `21-1099.00`** Community and Social Service Specialists, All Other
Residual bucket for non-managerial incumbents.

**3. `43-6014.00`** Secretaries and Administrative Assistants, Except Legal, Medical, and Executive
Honest option for the substantial share doing pure back-office work.

*Why low:* broadband title, see flag #5. The $74k median spans very different jobs.

DECISION: **`21-1099.00`** Community and Social Service Specialists, All Other —
**family-level only**, not a sub-code claim.
Rule 1 applies: the three candidates disagree about the nature of the work
(manager / specialist / clerical), so the residual is the honest assignment.
Candidate 1 (`11-9151.00`, managers) is affirmatively argued against by this file's
own numbers: the $74,363 median sits far below the $128,296 median of
`ADMINISTRATIVE STAFF ANALYST` (M09), which flag #4 identifies as the M-level
manager benchmark. Most incumbents are not managers.
Known contamination: a material share do pure back-office work and belong in
43-xxxx. That share is not recoverable from `title_description`; a join on
`agency_name` would bound it. Record precision as family-level and do not report
this code without that caveat.

---

## L05 · COMMUNITY ASSOCIATE
`low` · 6,364 staff · median $54,272 · 0 open exams

**1. `21-1093.00`** Social and Human Service Assistants
Strongest lexical match ("Social and Human Services Assistant") and fits
client-facing incumbents.

**2. `43-9061.00`** Office Clerks, General
Fits the administrative share, which is large.

**3. `21-1094.00`** Community Health Workers
Only where the assignment is health outreach specifically.

*Why low:* same broadband problem as L04, one grade lower. See flag #5.

DECISION: **`21-1099.00`** Community and Social Service Specialists, All Other —
**family-level only**. Same verdict and same reasoning as L04.
Rule 1 again: the candidates disagree about the nature of the work (human-service
assistant / office clerk / community health worker), so the residual wins over
candidate 1 despite `21-1093.00` being the stronger *lexical* match — that is
exactly the trap rule 2 exists to block.
Note the grade difference from L04 ($54,272 vs $74,363) is a civil-service grade
distinction, and SOC does not encode grade. Two titles sharing one code here is
correct, not a collision to fix.

---

## L06 · COLLEGE ASSISTANT
`low` · 4,872 staff · median — · 0 open exams

**1. `25-9044.00`** Teaching Assistants, Postsecondary
Fits tutoring and instructional support.

**2. `43-9061.00`** Office Clerks, General
Fits clerical assignments, probably the plurality.

**3. `SKIP`** — CUNY catch-all
See flag #8. Also note CUNY is barely in this payroll file at all.

*Why low:* one hourly title spanning unrelated work, at an employer only
partially represented in the dataset.

DECISION: **`NO SINGLE CODE`** — retain as a visible unresolved bucket (4,872).
**Candidate 3 (`SKIP`) is withdrawn.** Its stated reason — CUNY is barely in the
payroll file — is wrong; see the correction on flag #8. CUNY community colleges
contribute 19,863 FY2025 rows, so these 4,872 people are genuinely in the dataset
and dropping them would lose real workers.
What remains is the L03 problem: tutors, lab techs, office staff and IT help span
SOC major groups 25, 43 and 15, and no residual spans them.
Resolver: a CUNY assignment/department field. Not present in `k397-673e`. Until
then this is a standing gap. Do **not** merge it into the L01/L02 skip total.

---

## L07 · SERGEANT-
`low` · 4,025 staff · median $118,056 · 0 open exams

**1. `33-1012.00`** First-Line Supervisors of Police and Detectives
Most likely by volume — NYPD is the largest employer of the rank.

**2. `33-1021.00`** First-Line Supervisors of Firefighting and Prevention Workers
FDNY also uses the rank.

**3. `33-1011.00`** First-Line Supervisors of Correctional Officers
DOC also uses it.

*Why low:* the service is not recoverable from the title. See flag #9.
`agency_name` would resolve this — worth joining before deciding.

DECISION: **`33-1012.00`** First-Line Supervisors of Police and Detectives.
Evidence, not assumption: across all 2,901 DCAS exam rows the only Sergeant exams
are `Sergeant (Police) (Prom)` and `Sergeant (Police) (Pro)`. There is **no** fire
or correction Sergeant exam anywhere in the file, consistent with the FDNY ladder
running Firefighter → Lieutenant with no Sergeant rank. Candidates 2 and 3 have no
support in this repo's data. See the narrowing note on flag #9.
Confidence: medium, upgraded from low. The evidence is indirect — the exam file
shows which ranks DCAS *tests*, not who holds them — and DOC in particular could
carry incumbents without a current exam. The `agency_name` join in L09 answers
this title at the same time; run it and confirm before publishing.

---

## L08 · P.O. DA DET GR3
`low` · 3,330 staff · median $119,980 · 0 open exams

**1. `33-3021.00`** Detectives and Criminal Investigators
Detective-grade investigative work is the actual duty. See flag #10.

**2. `33-3051.00`** Police and Sheriff's Patrol Officers
Only if you treat the `P.O.` civil-service line as controlling over actual duties.

**3. `33-3021.02`** Police Identification and Records Officers
Narrower investigative variant; pick only with DA-office specifics.

*Why low:* the title is an unreadable code, and candidates 1 and 2 disagree on
whether to classify by civil-service line or by real duties.

DECISION: **`33-3021.00`** Detectives and Criminal Investigators.
The decision was made robust to the then-unresolved abbreviation (flag #10):
whether `DA` meant "District Attorney" or "Detailed As", the duty is
detective-grade investigation and the SOC is the same. The gloss has since been
resolved to "Detailed As" from the payroll universe itself (see flag #10),
which removes the residual doubt.
Candidate 2 rejected: classifying by the `P.O.` civil-service line over actual
duties would put 3,330 investigators into patrol, and this file's own convention
(flags #2, #3, #4) is that duties govern over title wording. Candidate 3
(`33-3021.02`) asserts an identification/records specialty nothing supports —
rule 1, do not claim unsupported detail.

---

## L09 · LIEUTENANT
`low` · 3,076 staff · median $141,684 · 1 open exam

**1. `33-1012.00`** First-Line Supervisors of Police and Detectives
Matched via alternate title "Police Lieutenant".

**2. `33-1021.00`** First-Line Supervisors of Firefighting and Prevention Workers
Matched equally well via "Fire Lieutenant" — a genuine tie on the evidence.

**3. `33-1011.00`** First-Line Supervisors of Correctional Officers
DOC variant.

*Why low:* exact 0.571 tie between the police and fire codes. See flag #9.

DECISION: **`BLOCKED`** — split between `33-1012.00` and `33-1021.00`, pending one
query. Do not assign a single code.
Unlike L07, the exam file **confirms** the ambiguity rather than resolving it:
both `Lieutenant (Police) (Prom)` and `Lieutenant (Fire) (Prom)` exist. NYPD
(55,424) and FDNY (19,333) are both large enough that either could hold a
substantial share of 3,076 incumbents, and agency headcount does not decompose to
ranks.

⚠️ Do **not** use this title's one open exam as a tiebreak. It is
`Lieutenant (Police) (Prom)`, application window 2027-05-05 → 2027-05-25 — a fact
about a future promotional schedule, not about who holds the title today.

The query that closes it (blocked in this sandbox: the network policy denies
`data.cityofnewyork.us`, gateway 403 on CONNECT):

```
https://data.cityofnewyork.us/resource/k397-673e.json
  ?$select=agency_name,count(1)
  &$where=fiscal_year=2025 AND title_description='LIEUTENANT'
  &$group=agency_name&$order=count_1 DESC
```

Run the same query for `SERGEANT-` (L07) and `P.O. DA DET GR3` (L08) while you are
there — one round trip confirms all three. If a single code is unavoidable before
then, use `33-1012.00` **marked provisional**, and state that the FDNY share is
unmeasured rather than zero.

---

## L10 · STUDENT AIDE
`low` · 3,341 staff · median — · 0 open exams

**1. `SKIP`** — employment category, not an occupation
See flag #6.

**2. `43-9061.00`** Office Clerks, General
Most common actual assignment.

**3. `25-9049.00`** Teaching Assistants, All Other
Where the placement is instructional.

*Why low:* describes who the worker is (a student), not what they do.

DECISION: **`SKIP`** — employment category, not an occupation.
Candidates 2 and 3 sit in different SOC major groups (43 and 25), which is the
L03/L06 signature. The difference is that L03 and L06 name *work* ambiguously
while this title names a *worker attribute* — being a student — and never names
work at all. A title that describes who was hired rather than what they do cannot
take a SOC code at any confidence.
Zero salaried rows, consistent with the reading. Report 3,341 as a documented
exclusion.

---

## L11 · ADJUNCT LECTURER
`low` · 2,698 staff · median — · 0 open exams

**1. `25-1199.00`** Postsecondary Teachers, All Other
The only honest code — every other postsecondary SOC is discipline-specific and
payroll records no discipline.

**2. `25-1194.00`** Career/Technical Education Teachers, Postsecondary
Only if the CUNY assignment is CTE.

**3. `SKIP`** — pending discipline data
Defer until a department field is available.

*Why low:* O*NET splits postsecondary teaching into ~35 discipline codes. Without
a subject you are forced into a residual bucket.

DECISION: **`25-1199.00`** Postsecondary Teachers, All Other.
The textbook case for rule 1: the occupation is certain, only the discipline is
missing, and O*NET publishes a purpose-built residual for exactly that. A forced
discipline pick would be fabrication.
Candidate 3 (`SKIP`) is withdrawn for the same reason as L06 — it rested on CUNY
being absent from the payroll file, which the flag #8 correction disproves. These
2,698 adjuncts sit in the community colleges, which carry 19,863 FY2025 rows.
Confidence: medium, upgraded from low. Note this is a *complete* answer at the
precision the data supports, not a placeholder — do not "improve" it later with a
discipline guess.

---

## L12 · JOB TRAINING PARTICIPANT
`low` · 4,021 staff · median $39,926 (**only 18 salaried rows**) · 0 open exams

**1. `SKIP`** — program enrollment, not an occupation
See flag #6.

**2. `13-1151.00`** Training and Development Specialists
**Almost certainly wrong** — this is the person who *delivers* training. The
payroll title is the person receiving it. Listed only to warn you off it.

**3. `53-7062.00`** Laborers and Freight, Stock, and Material Movers, Hand
Rough proxy if placements are known to be manual.

*Why low:* not an occupation, and the obvious lexical match inverts the
relationship. The median rests on 18 of 4,021 rows — treat it as noise.

DECISION: **`SKIP`** — program enrollment, not an occupation.

⚠️ **Never take candidate 2.** `13-1151.00` is the person who *delivers* training;
this title is the person *receiving* it. It is the highest-scoring lexical match in
the entire top 40 and it is exactly backwards — the single best argument in this
file against a fuzzy-similarity matcher. If any automated pass proposes it,
that pass is broken.
Candidate 3 rests on placements being manual, which nothing here establishes.
The $39,926 median rests on 18 of 4,021 rows (0.4%); do not report it.

---

## L13 · CITY SEASONAL AIDE
`low` · 2,414 staff · median $41,527 (**only 17 salaried rows**) · 0 open exams

**1. `SKIP`** — hiring category, not an occupation
See flag #6.

**2. `37-3011.00`** Landscaping and Groundskeeping Workers
Parks summer work is the most common placement.

**3. `53-7062.00`** Laborers and Freight, Stock, and Material Movers, Hand
Generic manual fallback.

*Why low:* "seasonal" is a hiring mechanism. Median rests on 17 of 2,414 rows.

DECISION: **`SKIP`** — hiring category, not an occupation.
Same reasoning as L10: "seasonal" describes the terms of hire, not the work.
Candidate 2 (`37-3011.00`) is plausible for Parks summer placements but nothing in
`k397-673e` establishes the placement mix, and `CITY SEASONAL AIDE` is used beyond
Parks — assigning it would assert a distribution never measured.
The $41,527 median rests on 17 of 2,414 rows (0.7%); do not report it.

---

# MEDIUM confidence

---

## M01 · TEACHER
`medium` · 56,041 staff · median $110,848 · 0 open exams

**1. `25-2021.00`** Elementary School Teachers, Except Special Education
**2. `25-2031.00`** Secondary School Teachers, Except Special and Career/Technical Education
**3. `25-2022.00`** Middle School Teachers, Except Special and Career/Technical Education

*Why medium:* the family is certain, the grade level is not — and O*NET has no
grade-agnostic K-12 teacher code. Any single pick misclassifies most of 56,041
people. Consider splitting by agency or accepting a deliberate roll-up.

> Note: bare `TEACHER` exact-matches O*NET alternate title data to
> `25-1011.00 Business Teachers, Postsecondary`. That match is **wrong** and is a
> good example of exact-match precision not meaning correctness.

DECISION: ___

---

## M02 · TEACHER SPECIAL EDUCATION
`medium` · 30,058 staff · median $105,520 · 0 open exams

**1. `25-2056.00`** Special Education Teachers, Elementary School
**2. `25-2058.00`** Special Education Teachers, Secondary School
**3. `25-2059.00`** Special Education Teachers, All Other

*Why medium:* special-education family is unambiguous; grade level again missing.
Option 3 is the honest roll-up if you will not split.

DECISION: ___

---

## M03 · ANNUAL ED PARA
`medium` · 28,453 staff · median $45,212 · 0 open exams

**1. `25-9043.00`** Teaching Assistants, Special Education
Most NYC paraprofessionals support special-education students.

**2. `25-9042.00`** Teaching Assistants, Preschool, Elementary, Middle, and Secondary School, Except Special Education
General-education classroom assignments.

**3. `25-9049.00`** Teaching Assistants, All Other
Roll-up if the special/general split is unavailable.

*Why medium:* occupation is clear once "PARA" is decoded (flag #11); only the
special-vs-general split is uncertain.

DECISION: ___

---

## M04 · SUBSTITUTE ED PARA
`medium` · 14,166 staff · median — · 0 open exams

**1. `25-9043.00`** Teaching Assistants, Special Education
**2. `25-9042.00`** Teaching Assistants, Preschool, Elementary, Middle, and Secondary School, Except Special Education
**3. `25-3031.00`** Substitute Teachers, Short-Term
Only if you weight "substitute" over "paraprofessional" — note this code is for
substitute *teachers*, not substitute aides.

*Why medium:* same as M03, plus a real question about whether the substitute
status or the paraprofessional role governs.

DECISION: ___

---

## M05 · TEACHER-GENERAL ED
`medium` · 15,531 staff · median — · 0 open exams

**1. `25-2021.00`** Elementary School Teachers, Except Special Education
**2. `25-2031.00`** Secondary School Teachers, Except Special and Career/Technical Education
**3. `25-2022.00`** Middle School Teachers, Except Special and Career/Technical Education

*Why medium:* identical to M01 but with "general ed" made explicit, which at least
rules out the special-education codes. Should almost certainly get the same
DECISION as M01.

DECISION: ___

---

## M06 · PRINCIPAL ADMINISTRATIVE ASSOCIATE -  NON SUPVR
`medium` · 4,242 staff · median $68,765 · 0 open exams

**1. `43-6014.00`** Secretaries and Administrative Assistants, Except Legal, Medical, and Executive
**2. `43-9061.00`** Office Clerks, General
**3. `43-6011.00`** Executive Secretaries and Executive Administrative Assistants
Fits the senior grade, but `NON SUPVR` argues against the executive tier.

*Why medium:* clearly administrative support; only the seniority tier is in
question. See flag #3 — do not let "Principal" pull this toward education admin.

DECISION: ___

---

## M07 · CLERICAL ASSOCIATE MOST MAYORAL AG
`medium` · 2,941 staff · median $51,227 · 0 open exams

**1. `43-9061.00`** Office Clerks, General
**2. `43-6014.00`** Secretaries and Administrative Assistants, Except Legal, Medical, and Executive
**3. `43-4171.00`** Receptionists and Information Clerks

*Why medium:* occupation is clear. `MOST MAYORAL AG` is agency-scope noise in the
title, not job content — strip it before any string matching.

DECISION: ___

---

## M08 · CARETAKER
`medium` · 4,011 staff · median $52,086 · 0 open exams

**1. `37-2011.00`** Janitors and Cleaners, Except Maids and Housekeeping Cleaners
NYCHA Caretakers clean buildings and remove refuse. Matched via "Building Custodian".

**2. `37-3011.00`** Landscaping and Groundskeeping Workers
Grounds portion of the duties.

**3. `39-2021.00`** Animal Caretakers
**Wrong — listed as a warning.** Exact lexical match on "Caretaker", completely
wrong job. See flag #2.

*Why medium:* confident once the euphemism is decoded, but this title will
mis-map under any automated matcher.

DECISION: ___

---

## M09 · ADMINISTRATIVE STAFF ANALYST
`medium` · 2,151 staff · median $128,296 · 2 open exams

**1. `11-3012.00`** Administrative Services Managers
Fits the managerial reality and the $128k median. See flag #4.

**2. `13-1111.00`** Management Analysts
Fits the literal title; understates seniority.

**3. `13-2031.00`** Budget Analysts
Only for incumbents in budget offices specifically.

*Why medium:* the split between 1 and 2 is exactly the euphemism question — is
this a manager or an analyst? The salary says manager.

DECISION: ___

---

## M10 · SCHOOL SAFETY AGENT
`medium` · 4,017 staff · median $56,508 · 3 open exams

**1. `33-9032.00`** Security Guards
Closest by duties; matched via "Safety and Security Officer".

**2. `33-9099.00`** Protective Service Workers, All Other
Residual that better reflects their NYPD-employed peace-officer status.

**3. `33-3012.00`** Correctional Officers and Jailers
Custodial-authority analogue; a stretch.

*Why medium:* real occupation, but SSAs are NYPD-employed peace officers with
arrest powers, which `Security Guards` understates.

DECISION: ___

---

## M11 · TRAFFIC ENFORCEMENT AGENT
`medium` · 2,508 staff · median $49,830 · 4 open exams

**1. `33-3041.00`** Parking Enforcement Workers
Standard mapping; matched via "Parking Enforcement Officer".

**2. `43-9199.00`** Office and Administrative Support Workers, All Other
Matched via "Traffic Agent"; weaker.

**3. `33-9099.00`** Protective Service Workers, All Other
For higher-level TEAs who direct traffic rather than issue summonses.

*Why medium:* option 1 is right for most incumbents, but senior TEA levels direct
traffic in the roadway, which `Parking Enforcement` does not capture.

DECISION: ___

---

## M12 · F/T SCHOOL LUNCH HELPER
`medium` · 3,801 staff · median — · 0 open exams

**1. `35-9011.00`** Dining Room and Cafeteria Attendants and Bartender Helpers
**2. `35-2021.00`** Food Preparation Workers
**3. `35-2012.00`** Cooks, Institution and Cafeteria
Only if incumbents actually cook rather than serve.

*Why medium:* food-service family is certain; serve-vs-prep-vs-cook is not.
Strip the `F/T` prefix before matching.

DECISION: ___

---

## M13 · F/T SR. SCHOOL LUNCH HELPER
`medium` · 2,744 staff · median — · 0 open exams

**1. `35-9011.00`** Dining Room and Cafeteria Attendants and Bartender Helpers
**2. `35-2012.00`** Cooks, Institution and Cafeteria
The `SR.` grade may imply cooking or lead duties.

**3. `35-1012.00`** First-Line Supervisors of Food Preparation and Serving Workers
If `SR.` denotes supervision — check before choosing.

*Why medium:* same as M12 plus an unresolved question about what `SR.` confers.
Should probably track M12's DECISION unless `SR.` means supervisory.

DECISION: ___

---

# HIGH confidence

---

## H01 · POLICE OFFICER
`high` · 24,153 staff · median $109,352 · 13 open exams

**1. `33-3051.00`** Police and Sheriff's Patrol Officers
**2. `33-3021.00`** Detectives and Criminal Investigators
**3. `33-1012.00`** First-Line Supervisors of Police and Detectives

*Why high:* candidate 1 is the canonical mapping. 2 and 3 listed only for
promoted incumbents who retain the base title.

> Note: exact matching sends this to `33-3021.02 Police Identification and Records
> Officers`, a narrow specialty. Prefer `33-3051.00`.

DECISION: ___

---

## H02 · FIREFIGHTER
`high` · 9,187 staff · median $109,352 · 0 open exams

**1. `33-2011.00`** Firefighters
**2. `33-1021.00`** First-Line Supervisors of Firefighting and Prevention Workers
**3. `33-2021.00`** Fire Inspectors and Investigators

*Why high:* direct match via alternate title "Fire Fighter". Unambiguous.

DECISION: ___

---

## H03 · CORRECTION OFFICER
`high` · 8,082 staff · median $105,146 · 3 open exams

**1. `33-3012.00`** Correctional Officers and Jailers
**2. `33-1011.00`** First-Line Supervisors of Correctional Officers
**3. `21-1092.00`** Probation Officers and Correctional Treatment Specialists
Scored equal to candidate 1 but is a **different job** — treatment, not custody.

*Why high:* candidate 1 matches the exact alternate title "Correction Officer".
Candidate 3 is a scorer artifact; do not pick it.

DECISION: ___

---

## H04 · SANITATION WORKER
`high` · 7,263 staff · median $92,093 · 0 open exams

**1. `53-7081.00`** Refuse and Recyclable Material Collectors
**2. `37-2011.00`** Janitors and Cleaners, Except Maids and Housekeeping Cleaners
**3. `53-7062.04`** Recycling and Reclamation Workers

*Why high:* DSNY workers collect refuse; candidate 1 is exact. Note the O*NET
alternate title "Sanitation Worker" also hangs off janitorial codes — a trap.

DECISION: ___

---

## H05 · ASSISTANT PRINCIPAL
`high` · 3,892 staff · median $153,562 · 0 open exams

**1. `11-9032.00`** Education Administrators, Kindergarten through Secondary
**2. `11-9033.00`** Education Administrators, Postsecondary
Only if CUNY-assigned.
**3. `25-2031.00`** Secondary School Teachers, Except Special and Career/Technical Education
Only for incumbents still primarily teaching.

*Why high:* candidate 1 is the standard mapping and the $153k median is
consistent with school leadership.

DECISION: ___

---

## H06 · GUIDANCE COUNSELOR
`high` · 3,722 staff · median $118,317 · 0 open exams

**1. `21-1012.00`** Educational, Guidance, and Career Counselors and Advisors
**2. `21-1021.00`** Child, Family, and School Social Workers
**3. `21-1011.00`** Substance Abuse and Behavioral Disorder Counselors

*Why high:* exact match via "Career Guidance Counselor". Candidate 1 is the
purpose-built code.

DECISION: ___

---

## H07 · OCCUPATIONAL THERAPIST
`high` · 3,494 staff · median $88,216 · 2 open exams

**1. `29-1122.00`** Occupational Therapists
**2. `31-2011.00`** Occupational Therapy Assistants
**3. `31-2012.00`** Occupational Therapy Aides

*Why high:* candidate 1 is exact. Candidates 2 and 3 are **lower-credential
different occupations** — listed only because the scorer ranks them highly.

> Note: this title matches **zero** entries in `Job Titles`. It resolves only
> against `Occupation Data`, and only after depluralizing "Occupational Therapists".

DECISION: ___

---

## H08 · SCHOOL SECRETARY
`high` · 3,305 staff · median $70,784 · 0 open exams

**1. `43-6014.00`** Secretaries and Administrative Assistants, Except Legal, Medical, and Executive
**2. `43-9061.00`** Office Clerks, General
**3. `43-6011.00`** Executive Secretaries and Executive Administrative Assistants

*Why high:* candidate 1 is the natural home. The scorer's top hits
(`43-4161`, `43-3051`) are HR/payroll codes and are wrong.

DECISION: ___

---

## H09 · CHILD PROTECTIVE SPECIALIST
`high` · 2,958 staff · median $68,309 · 1 open exam

**1. `21-1021.00`** Child, Family, and School Social Workers
**2. `21-1029.00`** Social Workers, All Other
**3. `21-1093.00`** Social and Human Service Assistants

*Why high:* strongest evidence in the whole set — O*NET carries the alternate
title "Child Protective Services Social Worker" verbatim under candidate 1.

DECISION: ___

---

## H10 · EMERGENCY MEDICAL SPECIALIST-EMT
`high` · 2,953 staff · median $49,047 · 0 open exams

**1. `29-2042.00`** Emergency Medical Technicians
**2. `29-2043.00`** Paramedics
The `-EMT` suffix argues for candidate 1; FDNY EMS employs both.
**3. `29-2099.00`** Health Technologists and Technicians, All Other

*Why high:* the family is certain and the suffix resolves the EMT/paramedic split.
Note O*NET split these into two codes; NYC has a separate Paramedic title.

DECISION: ___

---

## H11 · SCHOOL SOCIAL WORKER
`high` · 2,638 staff · median $115,195 · 0 open exams

**1. `21-1021.00`** Child, Family, and School Social Workers
**2. `21-1022.00`** Healthcare Social Workers
**3. `21-1029.00`** Social Workers, All Other

*Why high:* candidate 1 names school social workers explicitly. Should share a
DECISION with H09.

DECISION: ___

---

## H12 · SCHOOL CROSSING GUARD
`high` · 2,575 staff · median $44,533 (only 82 salaried rows) · 0 open exams

**1. `33-9091.00`** Crossing Guards and Flaggers
**2. `33-9032.00`** Security Guards
**3. `33-9099.00`** Protective Service Workers, All Other

*Why high:* O*NET carries "School Crossing Guard" verbatim under candidate 1.

> Caveat: the median rests on 82 of 2,575 rows — the title is overwhelmingly
> hourly. Trust the SOC mapping, not the salary.

DECISION: ___

---

## H13 · ASSISTANT DISTRICT ATTORNEY
`high` · 2,409 staff · median $120,000 · 0 open exams

**1. `23-1011.00`** Lawyers
**2. `23-1012.00`** Judicial Law Clerks
**3. `23-2011.00`** Paralegals and Legal Assistants
**Wrong** — listed because "Assistant" drags the scorer toward assistant codes.

*Why high:* ADAs are prosecuting attorneys. O*NET carries "District Attorney" as
an alternate title under `23-1011.00`. The exact $120,000 median reflects a
fixed salary schedule.

DECISION: ___

---

## H14 · ELIGIBILITY SPECIALIST
`high` · 2,275 staff · median $50,446 · 1 open exam

**1. `43-4061.00`** Eligibility Interviewers, Government Programs
**2. `21-1093.00`** Social and Human Service Assistants
**3. `13-1141.00`** Compensation, Benefits, and Job Analysis Specialists

*Why high:* candidate 1 is purpose-built for government benefit eligibility
determination, which is exactly this job.

DECISION: ___

---

## Coverage note

These 40 titles are 414,667 of 550,219 FY2025 payroll rows (75.4%).

With the 13 low-confidence decisions applied (2026-08-07):

| outcome | titles | rows | % of top-40 |
|---|---|---|---|
| `SKIP` — not an occupation | L01, L02, L10, L12, L13 | 124,911 | 30.1% |
| `NO SINGLE CODE` — real work, no code spans it | L03, L06 | 14,089 | 3.4% |
| `BLOCKED` — one query resolves it | L09 | 3,076 | 0.7% |
| coded (family-level or better) | L04, L05, L07, L08, L11 | 23,021 | 5.6% |
| **all 13 low-confidence** | | **165,097** | **39.8%** |

**Report those first three rows separately — they are not the same claim.** The
124,911 `SKIP` rows are a finding: the crosswalk is *more* accurate without them.
The 14,089 `NO SINGLE CODE` rows are a real gap: those are people doing real jobs
that O*NET cannot resolve at the granularity `k397-673e` records, and folding them
into the skip total would overstate the finding by 11% and hide the gap. The 3,076
blocked rows are neither — they are one API call away.

**Coded today: 23,021 rows, 5.6%** — the 13 low-confidence titles only. The 27
medium/high `DECISION:` lines are still open, so the crosswalk is not yet usable
end to end. If those 27 close on their candidate 1, coded coverage reaches 272,591
of 414,667 (**65.7%**), or 275,667 (**66.5%**) once L09 resolves. The remaining
138,999 rows (33.5%) split 124,911 deliberately excluded + 14,089 standing gap and
never become codeable.

Do not quote a coverage figure without its denominator caveat. The honest form is
**"65.7% of top-40 headcount coded, 30.1% deliberately excluded as
not-an-occupation, 3.4% a standing gap"** — the bare percentage invites the reader
to treat the exclusions as failure, which inverts the finding.
