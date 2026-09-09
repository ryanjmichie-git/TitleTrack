# Data sources and hazards

Row counts, update cadence, Socrata API behavior, and the payroll and exams data hazards behind every figure in this project.

The O*NET attribution referred to in the table below now lives in `docs/onet-attribution.md`.

Referenced from CLAUDE.md.

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

## What is committed under `data/raw/`, and one deliberate decision

The snapshots in `data/raw/` are tracked on purpose. Six of them are the fixtures
every gate reads, so they are load-bearing test data, not stray dumps —
`.gitignore` carries explicit negations saying so.

**`k397-673e_limit5.json` retains five named individuals.** It is the original
five-row schema probe against the payroll API, and it carries the full record:
`first_name`, `last_name`, `mid_init`, `agency_name`, `agency_start_date`,
`work_location_borough`, `title_description`, `base_salary`, `regular_gross_paid`,
`total_ot_paid` and the rest of the seventeen fields. Four of the five work for
`ADMIN FOR CHILDREN'S SVCS`.

This was reviewed before the repository was made public and **kept deliberately**.
The reasoning: NYC publishes `k397-673e` with employee names — that is the
dataset, not a leak of it — so republishing a five-row sample discloses nothing
the city has not already published itself. No gate reads this file; it exists as
the evidence of what the API actually returns, which is the same reason every
other snapshot here is committed.

Recorded so it reads as a decision rather than an oversight. If that call is ever
revisited, the file is referenced by no code and can be dropped or redacted
without touching any gate; removing it from history would need a rewrite, since
it was introduced in a single commit (`2e1358f`).
