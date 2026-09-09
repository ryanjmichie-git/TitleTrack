# O*NET 30.3 and required attribution

O*NET 30.3 file layout, match rates against NYC titles, and the verbatim attribution and trademark rules required in any output.

Referenced from CLAUDE.md.

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
