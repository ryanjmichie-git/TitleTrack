# TitleTrack

Maps NYC civil-service **payroll titles** → **DCAS exams** → **O*NET SOC codes**.

Everything below was verified against live API responses and the downloaded files,
not recalled. Raw evidence is in `data/raw/` (44 files, ~18 MB, all committed).
Figures are FY2025 unless stated.

---

## Data sources

| | dataset | rows | updated | attribution |
|---|---|---|---|---|
| Payroll | `k397-673e` | **6,775,830** (FY2014–FY2025) | 2026-04-16, **annually** | Office of Payroll Administration (OPA) |
| Exams | `4ptz-hmtc` | **2,901** | 2026-07-22, **annually** | Dept. of Citywide Administrative Services (DCAS) |
| Occupations | O*NET **30.3** | 1,016 occs / 57,543 job titles | — | see attribution below |

Latest fiscal year is **FY2025** (550,219 rows). Per-year counts sum exactly to the
total, so there are no null `fiscal_year` rows.

Both Socrata datasets update **annually**. Cache aggressively; there is no reason to
re-pull mid-session.

---

## Socrata API — hard-won gotchas

1. **Every value is a quoted string.** The `X-SODA2-Types` header says `number` for
   ten payroll fields. The JSON body still returns `"base_salary":"106346.00"`. Cast
   everything.
2. **Nulls are omitted, not null.** Absent fields don't appear as keys at all. Use
   `.get()`, never `[]` — a parser that works on a 5-row sample will crash at scale.
3. **Never paginate without `$order`.** Natural order is arbitrary: `$offset=6000000`
   returns FY2020 rows. Unordered paging silently skips and duplicates. Use
   `$order=:id`. Verified: 4 chunks × 100k with `:id` returned exactly 330,289 rows,
   matching the aggregate count.
4. **Unknown query params are a 400, not ignored.** `?burst=1` →
   `{"error":true,"message":"Unrecognized arguments [burst]"}`. Cache-busting breaks.
5. **Default page size is 1,000.** `$limit=100000` works and returns in ~2 s.
6. **No app token needed.** `$group`, `count(distinct …)`, `min/max/avg`, `$where …
   IS NOT NULL` all work unauthenticated. **600 requests** (200 sequential + 400
   concurrent) produced **zero throttling**. Socrata publishes no anonymous limit;
   throttling would surface as **HTTP 429**. An app token buys isolation from others
   sharing your IP, not a documented higher quota.

---

## Payroll (`k397-673e`) — data hazards

**`base_salary` is meaningless without `pay_basis`.** Four bases, different units in
the same column:

```
per Annum 4,060,360 | per Day 1,549,827 | per Hour 1,136,177 | Prorated Annual 29,466
```

FY2025 ranges show real contamination: `per Annum` min **$1.00**; `per Hour` max
**$190,941.71** — an annual salary misfiled as hourly. **Never blend bases, never
convert between them.** Scope to one basis and count what you excluded.

Other hazards (FY2025):
- **1,343** rows with negative `regular_gross_paid`; **136** with negative `ot_hours`
- **0** rows with `base_salary = 0`
- **1** title group with null `title_description` (164 rows)
- `work_location_borough` is the **agency's** location, not the employee's — 73%
  `MANHATTAN`, and includes `WESTCHESTER`, `ULSTER`, `DELAWARE`, `WASHINGTON DC`
- 2,025 distinct titles all-time; 1,557 in FY2025

---

## Exams (`4ptz-hmtc`) — data hazards

- **`title_code` is populated on 367 of 2,901 rows (12.7%).** It is the obvious join
  key and it is unusable. Do not build on it.
- `data_current_as_of` present on 2,472 (85%); `application_period_start` null on 256
- Application periods run 2019-06-27 → **2027-06-02** (future exams are in the file)
- **`open_competitive_promotion` conflates eligibility with schedule status** and has
  case-variant duplicates:
  `Open Competitive 1598 | Promotion 796 | Canceled 191 | CANCELED 33 | Postponed 55 |
  POSTPONED 23 | QIE 166 | Qualified Incumbent Exam 34 | (missing) 5`
  `QIE` == `Qualified Incumbent Exam`. Naive `GROUP BY` yields nine categories where
  there are five. Rows carrying only a *status* have no eligibility — treat as null.

---

## The join — this is the hard part of the project

There is **no shared key**. Payroll has `title_description` (UPPERCASE); exams have
`exam_title` (Mixed Case). Join on normalized text:

| stage | matched / 698 distinct exam titles |
|---|---|
| exact string | 268 (38.4%) |
| **uppercase + strip parentheticals** | **625 (89.5%)** |
| residual | 73 (10.5%) |

**The 10.5% residual is two different things — do not conflate them:**

1. **Correctly unmatched.** `(NYC H+H)`, `(Hospitals)`, `(Transit Authority)` are
   separate employers **absent from the citywide payroll file entirely**. Verified
   against the FY2025 `agency_name` list. These are true negatives; a fuzzy matcher
   tuned to maximize match rate will actively corrupt the data by forcing them.
2. **Genuine misses.** `Park and Recreation` vs `Parks and Recreation`. Singular/plural
   and abbreviation drift.

**Employer checks (data-driven, not assumed):**
- `NYC HOUSING AUTHORITY` **IS** in payroll (14,297 rows) → NYCHA exams are same-employer
- **CUNY: community colleges are in payroll (19,863 rows), senior colleges are not.**
  Do not use `CUNY CENTRAL OFFICE` (217 rows) as the CUNY check — that was the
  error. The colleges appear under their own agency names and a substring search
  for `CUNY` misses all of them: `COMMUNITY COLLEGE (MANHATTAN)` 4,897,
  `(LAGUARDIA)` 4,201, `(KINGSBORO)` 3,232, `(QUEENSBORO)` 2,783, `(BRONX)` 2,275,
  `(HOSTOS)` 1,907, `GUTTMAN COMMUNITY COLLEGE` 568. No senior college (Hunter,
  Baruch, City, Brooklyn, Queens, John Jay…) appears in the 158-agency list —
  consistent with community colleges being city-funded and senior colleges
  state-funded. So `COLLEGE ASSISTANT` and `ADJUNCT LECTURER` are well represented,
  not marginal.
- No agency matches `HOSPITAL`, `H+H`, or `TRANSIT` → those are foreign employers

⚠️ `data/raw/top40_titles.json` still carries the **superseded** CUNY caveat
("CUNY college staff are largely absent"). It is left in place deliberately so the
artifact stays byte-identical to what the generator produces; fixing it means
editing the caveat in both generators and regenerating. See known gaps.

196 of 2,901 exams carry a foreign-employer marker; **none** of them match a top-40
payroll title, which is consistent with the above.

---

## O*NET 30.3

Bulk text files live at `https://www.onetcenter.org/dl_files/database/db_30_3_text/<Name>.txt`.
The download page only advertises `.xlsx`; the `_text/` path is parallel and
undocumented there. **Tab-delimited UTF-8 with a header row — not CSV.** Task text
contains commas freely; a comma parser shreds it.

**`Alternate Titles` no longer exists — it is `Job Titles` in 30.3.**
`db_30_3_text/Alternate%20Titles.txt` returns a hard **404**. Code written against
the old name breaks silently on this release.

**`Job Titles` is a supplement, not a superset.** It contains only colloquial
variants: **1,013 of the 1,016 canonical O*NET titles are absent from it.**
`Occupational Therapist` appears **zero** times. Always consult `Occupation Data`
as well.

**Canonical titles are plural** (`Occupational Therapists`), so exact matching
against `Occupation Data` scores **0 / 40**. Depluralize before comparing.

Match rate, 40 largest payroll titles, exact case-insensitive:

| source | /40 |
|---|---|
| Job Titles (alternate) | **14 (35%)** |
| Sample of Reported Titles | 9 — strict subset, adds 0 |
| Occupation Data as published | 0 |
| union + depluralization | 15 |

Headcount-weighted this is only **32.3%** (133,898 of 414,667). The five biggest
misses are 189,177 people, failing on NYC formatting (`- PER SESSION`, `ED PARA`,
`TEACHER-GENERAL ED`), not on missing occupations.

⚠️ Bare `TEACHER` exact-matches to `25-1011.00 Business Teachers, Postsecondary`.
That is **wrong**. Exact-match precision ≠ correctness.

### Required attribution — verbatim, non-negotiable

> This page includes information from the O*NET 30.3 Database by the U.S. Department
> of Labor, Employment and Training Administration (USDOL/ETA). Used under the
> CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA.

Because this project **modifies** the data (joining it), also append:

> [Your name or company] has modified all or some of this information. USDOL/ETA has
> not approved, endorsed, or tested these modifications.

Enforced trademark rules: the ® must be displayed; use "O*NET" **as an adjective
only** ("includes information from the O*NET database", never "includes O*NET");
never possessive or plural; and **the version number is mandatory** — "O*NET 30.3
Database", not "O*NET Database". Pin `db_30_3` in URLs so the data and the
attribution string stay in sync.

---

## Decisions already made

- **Salary is scoped to a single `pay_basis`, never blended.** `top40_titles.json`
  carries `{basis: "per Annum", median, n_included, n_excluded}`. Non-annual rows are
  excluded and counted, never converted.
- **A null median is a fact, not missing data.** 10 of the top 40 titles have *zero*
  `per Annum` rows. Do not "fix" them.
- **`data/raw/*` is gitignored, with `!data/raw/top40_titles.json` as an exception.**
  The glob must be `data/raw/*`, not `data/raw/`: excluding the *directory* stops git
  descending into it and makes the negation a silent no-op. Raw snapshots were
  force-added deliberately.
- **`.gitattributes` sets `data/raw/** -text`** so snapshots round-trip byte-identical;
  `core.autocrlf` would otherwise rewrite LF→CRLF and a fresh clone would no longer
  match what the APIs returned.

---

## ⚠️ Titles that are not occupations

Several large payroll "titles" describe a pay mechanism or hiring category. Coding
them as jobs corrupts any workforce analysis. Full detail in
`data/crosswalk_candidates.md`.

- **`TEACHER- PER SESSION` (78,618 — the largest title in the city) is a pay code.**
  It is how DOE pays *existing* teachers hourly for after-school/summer work. These
  are overwhelmingly the same people already counted under `TEACHER`. Its null median
  is the tell.
- `ELECTION WORKER` (36,517) — civic stipend role, zero salaried rows
- `STUDENT AIDE`, `JOB TRAINING PARTICIPANT`, `CITY SEASONAL AIDE` — hiring
  categories. The latter two have 18 and 17 salaried rows out of 4,021 and 2,414.
- Skipping these five removes **124,911 rows, 30.1% of top-40 headcount**. That is a
  finding to report, not a gap to fill.

**Euphemisms** (name ≠ duties): `CARETAKER` is a NYCHA janitor, not a caregiver;
`ADMINISTRATIVE STAFF ANALYST` is a manager (M-level), not an analyst;
`PRINCIPAL ADMINISTRATIVE ASSOCIATE` is neither; `SERGEANT-`/`LIEUTENANT` don't say
which uniformed service and map to *different* SOC codes (`33-1012` vs `33-1021`) —
join `agency_name` to resolve.

---

## Repo map

```
CLAUDE.md                        this file
data/crosswalk_candidates.md     40 titles × 3 SOC candidates, confidence, DECISION lines
data/raw/top40_titles.json       derived artifact: headcount, per-Annum median, open exams
data/raw/*                       44 raw API/O*NET snapshots (byte-exact, ~18 MB)
scripts/build_top40.ps1          rebuilds top40_titles.json offline (Windows only)
scripts/build_top40.py           same, portable. `--check` diffs instead of writing
scoring/rubric.md                automatable / augmentable / human_anchored, v0.1
scoring/classifications_round1.md  5 hand-scored tasks + 4 rubric ambiguities
```

`build_top40.py` reproduces the PowerShell output **byte for byte** — BOM, CRLF,
and PS 5.1's column-aligned `ConvertTo-Json` layout — so a Linux rebuild does not
churn the committed artifact. `python3 scripts/build_top40.py --check` is the
regression test; it currently passes at 47,331 bytes. Keep the two generators in
step: any change to one must be mirrored, or `--check` fails by design.

Useful raw files: `join_unmatched_after_normalization.txt` (the 73 residuals — read
before "fixing" the matcher), `k397_agencies_2025.json` (employer checks),
`onet_license_db.txt` (attribution source), `ratelimit_burst_log.json`.

---

## Conventions

- Never commit raw dumps casually — `data/raw/*` is ignored by design; use `-f`
  deliberately.
- Every SOC code must be verified against `onet_Occupation_Data.txt` before use.
  Do not cite codes from memory.
- When reporting a median or rate, report what was excluded alongside it.

## Known gaps / next steps

- ~~`build_top40.ps1` is PowerShell and assumes Windows.~~ **Done** —
  `scripts/build_top40.py` is byte-identical and portable. The `.ps1` is kept as
  the reference implementation; neither is authoritative over the other.
- `data/crosswalk_candidates.md`: **13 of 40 `DECISION:` lines are filled** (the
  `low` set, L01–L13). The 27 `medium`/`high` lines are still open. Use the verdict
  vocabulary and the two rules defined at the head of that file's LOW section.
- **One API call closes three decisions.** L09 (`LIEUTENANT`) is `BLOCKED` and
  L07/L08 are decided but unconfirmed, all on the same `agency_name` group-by. It
  is blocked in the cloud sandbox — the network policy denies
  `data.cityofnewyork.us` with a gateway 403 on CONNECT. Run it from a machine
  with access; the exact query is in the L09 entry.
- **Superseded caveat in `top40_titles.json`.** The `caveats` array says CUNY
  college staff are largely absent; that is wrong (see employer checks). Fixing it
  means editing the string in *both* `build_top40.ps1` and `build_top40.py` and
  regenerating — which resets the byte-identity baseline `--check` compares
  against. Deliberately not done as a drive-by.
- `scoring/rubric.md` is v0.1. Two of the four ambiguities found in round 1 are
  unresolved and both distort scoring at volume: statement-level classes must not
  be aggregated to occupations (no clause weights exist in O*NET), and context-free
  task statements are currently classified by fiat. See
  `scoring/classifications_round1.md` before scoring anything in bulk.
- No O*NET→NYC mapping is committed yet; exact matching tops out at 32.3% by
  headcount. Suffix stripping and abbreviation expansion are the next lever — not a
  fuzzy-similarity threshold, which would force the true negatives above.
- Grade level is unrecoverable for `TEACHER` / `TEACHER-GENERAL ED` /
  `TEACHER SPECIAL EDUCATION` (101,630 people). O*NET has no grade-agnostic K-12 code.
