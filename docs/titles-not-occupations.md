# Titles that are not occupations

The large payroll titles that are pay codes or hiring categories rather than jobs, and the euphemisms whose names do not describe the duties.

Referenced from CLAUDE.md.

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
