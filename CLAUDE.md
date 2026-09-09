# TitleTrack

Maps NYC civil-service **payroll titles** → **DCAS exams** → **O*NET SOC codes**.

Every figure in this repo and its docs was verified against live API responses and the
downloaded files in `data/raw/`, not recalled. Figures are FY2025 unless stated.

## Non-negotiables

- **The O*NET attribution block is verbatim and mandatory** in any output using O*NET
  data — including the "has modified" sentence, the ®, and the version number. Before
  shipping anything containing O*NET data, read `docs/onet-attribution.md`.
- **Never code a pay code or hiring category as an occupation.** Five of the top 40
  payroll titles are not jobs; skipping them is the finding, not a gap to fill. Before
  assigning any SOC code, read `docs/titles-not-occupations.md`.
- **Socrata:** never paginate without `$order=:id` — unordered paging silently skips and
  duplicates rows. Cast every value; the JSON body returns numbers as quoted strings
  regardless of `X-SODA2-Types`. Treat an absent key as null: use `.get()`, never `[]`.

## Commands

Run from the repo root. All are offline, stdlib-only, and exit non-zero on failure.

- `python scripts/build_top40.py --check` — artifact regression test. Writes nothing;
  diffs a fresh rebuild against the committed artifact. Passing prints
  `OK  byte-identical … (47524 bytes)`. Verified 2026-09-06.
- `python demo/evaluate.py` — hard-fail gate. Re-derives every headcount, salary, exam,
  SOC code, and task statement in `demo/demo_data.json` from committed sources, and bans
  occupation-level aggregate keys. Passing ends `GATE PASSED`. Verified 2026-09-06.
- `python agents/title-matcher/evaluate.py --predictions <preds.jsonl>` — grades agent
  output against the golden set; same for `agents/crosswalk-decider/`. Passing ends
  `RESULT: PASS`. `--emit-inputs <file>` gets label-free inputs; `baselines.py`
  regenerates adversarial predictions — **the mode names differ per agent**:
  `naive|strict` for `title-matcher`, `first_soc|always_skip` for
  `crosswalk-decider`. An unrecognised mode silently falls through to the default
  instead of erroring, so passing `strict` to `crosswalk-decider` re-runs
  `first_soc` and looks like a second baseline. Verified 2026-09-09.
- `python demo/serve.py` → `http://localhost:8765` serves the demo (unverified here:
  long-running server, not started).

No pytest suite — the gates above are the tests. For any new API pull the check is row
reconciliation: paged rows with `$order=:id` must sum **exactly** to the `count(*)`
aggregate (verified once at 330,289 rows over 4 chunks). See
`docs/data-sources-and-hazards.md`.

## Decisions already made

- Salary is scoped to a single `pay_basis`, never blended and never converted. Excluded
  rows are counted in `n_excluded`, not dropped silently.
- A null median is a fact, not missing data. 10 of the top 40 titles have zero
  `per Annum` rows. Do not "fix" them.
- `data/raw/*` is gitignored with `!data/raw/top40_titles.json` as the exception. The
  glob must be `data/raw/*`, not `data/raw/` — excluding the *directory* stops git
  descending into it and makes the negation a silent no-op. Snapshots were force-added
  deliberately; use `-f` deliberately too, never casually.
- `.gitattributes` sets `data/raw/** -text` so snapshots round-trip byte-identical.
  `core.autocrlf` would rewrite LF→CRLF and a fresh clone would stop matching what the
  APIs actually returned.

## Gotchas

- `base_salary` is meaningless without `pay_basis` — four bases share the column in
  different units. FY2025 has a `per Annum` min of **$1.00** and a `per Hour` max of
  **$190,941.71**. Real contamination; scope to one basis and count what you excluded.
- `4ptz-hmtc.title_code` is populated on **367 of 2,901 rows (12.7%)**. It is the obvious
  join key and it is unusable. Do not build on it.
- `open_competitive_promotion` conflates eligibility with schedule status and carries
  case-variant duplicates. A naive `GROUP BY` yields nine categories where there are five.
- `work_location_borough` is the **agency's** location, not the employee's.
- Unknown Socrata query params return a **400**, not a silent ignore — cache-busting breaks.
- O*NET `Alternate Titles` no longer exists; it is `Job Titles` in 30.3, and that file is
  a supplement, not a superset — 1,013 of the 1,016 canonical titles are absent from it.
  Always consult `Occupation Data` as well.
- Canonical O*NET titles are plural, so exact matching against `Occupation Data` scores
  **0 / 40** until you depluralize.
- ⚠️ Bare `TEACHER` exact-matches `25-1011.00 Business Teachers, Postsecondary`. That is
  wrong. Exact-match precision ≠ correctness.

## Where to look

- Before pulling from Socrata or citing any row count, read
  `docs/data-sources-and-hazards.md`. Both datasets update **annually** — cache
  aggressively; there is no reason to re-pull mid-session.
- Before touching the matcher, read `docs/title-exam-onet-join.md` and
  `data/raw/join_unmatched_after_normalization.txt` (the 73 residuals). Some are true
  negatives — foreign employers absent from the citywide payroll file. A fuzzy matcher
  tuned to maximize match rate will corrupt the data by forcing them.
- Before editing anything under `demo/`, read `docs/demo-prototype.md`.
  `demo/demo_data.json` is **generated** — change `build_demo_data.py` or
  `task_classifications.json` and rebuild.
- Before scoring tasks in bulk, read `scoring/classifications_round1.md`. Rubric v0.1 has
  two unresolved ambiguities; statement-level classes must never be aggregated to an
  occupation-level score, and `demo/evaluate.py` fails the run if they are.
- `data/crosswalk_candidates.md` holds the 40 titles × 3 SOC candidates and the
  `DECISION:` lines; the head of its LOW section defines the verdict vocabulary and its
  two rules. `HANDOFF.md` says which decisions are still open.
- `scripts/build_top40.ps1` and `build_top40.py` must be edited together — `--check`
  fails by design if they drift. Neither is authoritative over the other.
- Verify every SOC code against `data/raw/onet_Occupation_Data.txt` before use; never
  cite a code from memory. Report what was excluded alongside every median or rate.
- `agents/README.md` explains the two subagents, their golden sets, and their gates.

## Keep this file useful

When Claude gets something wrong twice, add one line here. Every line costs context.
