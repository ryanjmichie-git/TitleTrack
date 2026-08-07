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

> **13 of 40 are `low`.** That is the real finding here. See the euphemism section
> immediately below — most low-confidence cases are not hard matching problems,
> they are titles that do not describe an occupation at all.

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
One hourly title covering tutors, lab techs, office staff, and IT help. Also note
this is CUNY, which is barely present in the payroll file (217 rows citywide).

### 9. `SERGEANT-` / `LIEUTENANT` — which uniformed service?
Both ranks exist in NYPD, FDNY, and DOC, and they map to *different* SOC codes
(`33-1012` vs `33-1021`). The payroll title alone cannot tell you. The trailing
hyphen on `SERGEANT-` is a data artifact, not part of the name.

### 10. `P.O. DA DET GR3` — Police Officer / District Attorney / Detective Grade 3.
A detective-grade investigator assigned to a District Attorney's office. Unreadable
without decoding, and not a patrol officer despite the `P.O.` prefix.

### 11. `ED PARA` — paraprofessional, i.e. a teaching assistant.
`ANNUAL ED PARA` and `SUBSTITUTE ED PARA` are classroom paraprofessionals. The
abbreviation defeats exact matching entirely, and "PARA" reads as a prefix rather
than a noun.

---

# LOW confidence

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

DECISION: ___

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

These 40 titles are 414,667 of 550,219 FY2025 payroll rows (75.4%). If you accept
the `SKIP` recommendations for L01, L02, L10, L12, and L13, you remove 124,911 rows
(30% of the top-40 headcount) from the crosswalk as not-an-occupation — which is a
finding to report, not a gap to fill.
