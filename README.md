# TitleTrack

**Pick your city job title, see what AI actually means for your work task-by-task —
no fake risk scores — and see the exam that's your next move up.**

A worker-facing prototype built on New York City's own payroll, civil-service exam,
and federal occupation data. It maps **NYC payroll titles → DCAS exams → O\*NET SOC
codes**, labels each published task as `automatable` / `augmentable` /
`human_anchored`, and points at the promotional exam that is the actual mechanism for
moving up in civil service.

It deliberately produces **no occupation-level risk score.** Holding the method
constant and changing only the unit of analysis moves US "high-risk" employment from
38% to 9% (Arntz, Gregory & Zierahn 2017) — the scary number is an artifact of
aggregation, not a property of the technology. A hard-fail gate in this repo bans
job-level aggregate keys outright.

## The finding

New York City's titles do not describe jobs.

- **`CARETAKER`** is a NYCHA janitor, not a caregiver.
- **`TEACHER- PER SESSION`** — 78,618 people, the largest title in the city — is a
  pay code for teachers working after-school hours, not a job.
- **`LIEUTENANT`** is two different occupations depending on whether it is NYPD or
  FDNY (1,581 / 1,495), so it is never coded as one.
- Five of the forty largest titles are not occupations at all. Excluding them removes
  **124,911 rows — 30.1% of top-40 headcount.** That exclusion is the finding, not a
  gap to fill.

Nothing joins these datasets. There is no shared key: `4ptz-hmtc.title_code` is
populated on 367 of 2,901 rows (12.7%) and is unusable. The join has to be rebuilt
from title text, without forcing matches.

## Run the demo

```bash
python demo/serve.py          # then open http://localhost:8765
```

13 titles, task categories, DCAS exam links, and a promotional next rung. The
"Explain" panel calls Claude live if `ANTHROPIC_API_KEY` is set and the `anthropic`
package is installed; otherwise it serves a precomputed answer and says so on screen.
Everything else is offline.

## How to verify it

There is no pytest suite — these gates are the tests. All are stdlib-only, offline,
and finish in a few seconds. Python 3.9+ — CI tests 3.9 and 3.13 on every
push and pull request, so that floor is measured rather than asserted.
`sh scripts/verify.sh` runs every gate at once and is what both CI and the
local pre-stop hook execute.

| Command | Asserts | Expected |
|---|---|---|
| `python scripts/build_top40.py --check` | a fresh rebuild is byte-identical to the committed artifact, BOM and CRLF included | exit **0**, `OK byte-identical … (47524 bytes)` |
| `python demo/evaluate.py` | all 248 facts in the demo trace to committed sources; no job-level aggregate keys exist | exit **0**, `GATE PASSED` |
| `agents/title-matcher/baselines.py strict \| … evaluate.py --predictions /dev/stdin` | an over-conservative matcher passes the gates | exit **0** |
| same with `naive` | a fuzzy matcher is **caught** forcing matches | exit **1** |
| `agents/crosswalk-decider/baselines.py first_soc` / `always_skip` | reflexive coding and reflexive skipping are both **caught** | exit **1** each |

The three inverted expectations are the point: an adversarial baseline that starts
passing means the golden set lost its teeth. CI asserts the expected exit code rather
than success. Note the baseline mode names differ per agent, and an unrecognised mode
**silently falls through to the default** rather than erroring.

## Layout

```
data/raw/            committed API snapshots - evidence, and the gates' fixtures
data/crosswalk_candidates.md   40 titles x 3 SOC candidates + the DECISION lines
scripts/             build_top40.{py,ps1} - kept byte-identical by --check
demo/                the prototype, its builder, and its gate
agents/              two subagents: spec + golden set + gate each
scoring/             the task-classification rubric and its round-1 findings
docs/                data hazards, attribution rules, the join, the pitch deck
```

## The two subagents

- **`title-matcher`** — joins DCAS exam titles to payroll titles. Its gate hard-fails
  a forced match, because the naive baseline produced 12 corrupt ones while scoring
  35/41 on recall. Some residuals are true negatives: foreign employers absent from
  the citywide payroll file. A matcher tuned to maximise match rate corrupts the data.
- **`crosswalk-decider`** — maps a payroll title to an occupation code from repo
  evidence, using the verdict vocabulary `CODE` / `SKIP` / `NO_SINGLE_CODE` /
  `BLOCKED`. It is golden-tested against 13 hand-decided titles and returns `BLOCKED`
  rather than guessing. **18 of 40 decisions are filled; 22 are open.**

## Data sources

| Source | ID | Rows | Vintage |
|---|---|---|---|
| NYC Citywide Payroll | Socrata `k397-673e` | 6,775,830 (FY2014–FY2025) | updated 2026-04-16, **annually** |
| DCAS Annual Examination Schedule | Socrata `4ptz-hmtc` | 2,901 | updated 2026-07-22, **annually** |
| O\*NET Database | 30.3 | 1,016 occupations | — |

Hazards worth reading before touching any of it: `docs/data-sources-and-hazards.md`.
`base_salary` is meaningless without `pay_basis` (FY2025 has a `per Annum` minimum of
$1.00 and a `per Hour` maximum of $190,941.71), and Socrata paging without
`$order=:id` silently skips and duplicates rows.

## Attribution

This product includes information from the O\*NET 30.3 Database by the U.S. Department
of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0
license. O\*NET® is a trademark of USDOL/ETA.

TitleTrack has modified all or some of this information. USDOL/ETA has not approved,
endorsed, or tested these modifications.

## Licence

MIT for the code and documentation. **`data/raw/` is not covered** — and it does not
hold one licence but three:

- O\*NET 30.3 under **CC BY 4.0** (attribution mandatory and verbatim)
- NYC Open Data under the **City's terms of use**
- `socrata_app_tokens.*` under **CC BY-NC-SA 3.0** — NonCommercial and ShareAlike,
  which is *not* MIT-compatible and is carved out explicitly

See [LICENSE](LICENSE) for the full scope and
[docs/onet-attribution.md](docs/onet-attribution.md) for the mandatory attribution
rules. Reusing anything from `data/raw/` means complying with that file's upstream
terms, not this repository's MIT grant.

## Status

A prototype. The task classifications are rubric v0.1 with two documented unresolved
ambiguities, and the page says so; they need validation by the workers in those
titles, not a bigger model. `HANDOFF.md` records what is built, what is decided, what
is verified, and what is not.
