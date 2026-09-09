# The payroll-to-exam join

How payroll titles are joined to DCAS exam titles, the match rate at each stage, and why the residual must not be forced.

Referenced from CLAUDE.md.

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

The CUNY caveat in `data/raw/top40_titles.json` was **corrected 2026-08-07**:
both generators were edited together and the artifact regenerated, resetting
the `--check` baseline to 47,524 bytes. The corrected caveat states the
community-college finding above and flags senior-college exams as the ones to
treat as foreign.

196 of 2,901 exams carry a foreign-employer marker; **none** of them match a top-40
payroll title, which is consistent with the above.
