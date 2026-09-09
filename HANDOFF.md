# TitleTrack — handoff

Project state, not rules. Rules live in `CLAUDE.md`.
Last updated **2026-09-08**. Previous update 2026-09-06 ("moved out of CLAUDE.md:
this is project state, not a rule").

---

## Built

- **Crosswalk data layer.** NYC payroll titles → DCAS exams → O*NET SOC codes, from
  committed API snapshots in `data/raw/`. Artifact is `data/raw/top40_titles.json`
  (47,524 bytes), regression-tested by `scripts/build_top40.py --check`.
- **Two subagents**, each with a spec, a golden set, and its own hard-fail gate:
  `agents/title-matcher/` (exam title → payroll title, refuses forced matches) and
  `agents/crosswalk-decider/` (payroll title → SOC code, golden-tested against the
  13 hand-decided `low` titles, returns `BLOCKED` rather than guessing).
- **`demo/` — worker-facing prototype, 13 titles.** Search box, tasks grouped into
  three collapsible categories, a counts-only summary line, per-task anchor
  explanation, DCAS exam links, an externally-researched promotional "next rung",
  two illustrative partner cards, and a live Claude "Explain" panel with a
  precomputed fallback. Served by `python demo/serve.py` on `:8765`.
- **Pitch materials.** `demo/PITCH.md` (3-minute script + Q&A), `demo/WALKTHROUGH.md`
  (spoken narrative, beat by beat), `docs/TitleTrack-pitch.pdf` (5 slides, generated
  by `docs/make_pitch_deck.py`, not hand-built).
- **Docs restructure, 2026-09-06/07 — UNCOMMITTED.** `CLAUDE.md` cut from 412 lines
  to ~93 (319 deletions, 93 insertions); the detail moved into five new files:
  `docs/data-sources-and-hazards.md`, `docs/demo-prototype.md`,
  `docs/onet-attribution.md`, `docs/title-exam-onet-join.md`,
  `docs/titles-not-occupations.md`. Plus `HANDOFF.md` itself. **None of it is on the
  remote** — see Risks #1.

## Decisions

- **`data/crosswalk_candidates.md`: 18 of 40 `DECISION:` lines filled, 22 open**
  (counted 2026-09-08; the 2026-09-06 handoff said 17/23 and was stale by one).
  Filled = the `low` set L01–L13, plus M08 `CARETAKER` → `37-2011.00`, M10
  `SCHOOL SAFETY AGENT` → `33-9032.00`, M11 `TRAFFIC ENFORCEMENT AGENT` →
  `33-3041.00`, H10 `EMERGENCY MEDICAL SPECIALIST-EMT` → `29-2042.00`, H08
  `SCHOOL SECRETARY` → `43-6014.00`. Every code verified against
  `onet_Occupation_Data.txt` before writing. Verdict vocabulary and its two rules
  are at the head of that file's LOW section.
- **Two decisions carry a flagged caveat, deliberately not asserted.** The employer
  is *unverifiable in-repo* for M10 and M11 — the per-Annum CSVs carry no
  `agency_name`, and both plausible employers map to the same code. Recorded as
  unverified; the resolver named is the L09-style `agency_name` group-by.
- **L09 `LIEUTENANT` is never a single code.** NYPD 1,581 / FDNY 1,495 (51/49), so it
  decomposes to `33-1012.00` + `33-1021.00` by `agency_name`. L07 `SERGEANT-`
  confirmed 100% NYPD. Raw responses in
  `data/raw/k397_{lieutenant,sergeant,po_da_det_gr3}_agencies_2025.json`.
- **Statement-level classes are never aggregated to an occupation score.** No clause
  weights exist in O*NET (rubric ambiguity A1). `demo/evaluate.py` bans the aggregate
  keys outright and fails the run if one appears.
- **The demo's summary line is counts, not a rate.** "5 of 8 tasks shown", never a
  percentage, with a caveat naming how many statements O*NET actually publishes.
  Computed in the page rather than stored in `demo_data.json`, so the eval's
  banned-key check keeps its meaning.
- **External data is quarantined and the seam is enforced.** The promotional next-rung
  data is not re-derivable from the snapshots, so it lives in its own file
  (`demo/next_rung.json`, with `_provenance` and `_caveat` headers), renders in its
  own UI block, and has its own eval check group that fails the build if the
  disclosure is missing, a source is absent, or a closed exam cycle is presented as
  an open filing window. Every cycle recorded there has already closed.
- **`COMMUNITY COORDINATOR` and `ADJUNCT LECTURER` are decided but excluded from the
  demo.** O*NET publishes **zero** task statements for "All Other" residual codes
  (`21-1099.00`, `25-1199.00`), so there is no task-level analysis to show. Having a
  code is not the same as having data.
- **Partner cards are labelled mock in the UI.** The Indeed and Coursera links are
  badged "illustrative partnership" with a caption saying a real version would pass
  the title and SOC code through. Unlabelled they would be the one thing that
  discredits a provenance-first project.
- **Rubric v0.1 stands with its ambiguities open.** A3's widened attestation test was
  *considered and not adopted*; SSA task 2134 stays `augmentable` and that call is
  flagged in the `_anchors` block of `demo/task_classifications.json` rather than
  silently made.

## Artifacts

| Path | What it is |
|---|---|
| `data/raw/top40_titles.json` | The committed artifact. Regression baseline 47,524 bytes. |
| `data/crosswalk_candidates.md` | 40 titles, 3 SOC candidates each, and the `DECISION:` lines. |
| `demo/demo_data.json` | **Generated.** Never hand-edit; change the builder or the classifications and rebuild. |
| `demo/task_classifications.json` | Rubric labels plus the `_anchors` block recording *why* each task is human-anchored. |
| `demo/next_rung.json` | External promotional-ladder research, quarantined. |
| `demo/index.html`, `serve.py`, `evaluate.py`, `build_demo_data.py` | The prototype and its gate. |
| `demo/PITCH.md`, `demo/WALKTHROUGH.md` | Pitch script and spoken narrative. |
| `docs/TitleTrack-pitch.pdf` | 5-slide deck. Regenerate with `python docs/make_pitch_deck.py`. |
| `docs/*.md` (5 files) | Reference detail split out of CLAUDE.md. **Uncommitted.** |

## Acceptance status

Run **2026-09-08 in this session**, output shown:

- `python demo/evaluate.py` → `GATE PASSED`, exit 0. **248 checks passed, 0 failed.**
- `python scripts/build_top40.py --check` → `OK  byte-identical … (47524 bytes)`, exit 0.

**Agent gates — verified 2026-09-09 against their adversarial baselines.** No real
agent-prediction file is committed, so what is proven here is that *the gates
discriminate*, not that a live agent run passes them:

| agent | baseline | exit | result | detail |
|---|---|---|---|---|
| `title-matcher` | `naive` | 1 | **FAIL** | `recall(matchable) 35/41`, **12 forced matches**, 19 wrong titles |
| `title-matcher` | `strict` | 0 | PASS | passes all three gates but collapses recall (`word_form` 0/18, `suffix` 0/4) |
| `crosswalk-decider` | `first_soc` | 1 | **FAIL** | `correct 3/13`; 3 forbidden codes, 1 forbidden verdict (L09 as a single `CODE`) |
| `crosswalk-decider` | `always_skip` | 1 | **FAIL** | `correct 5/13` |

The **35/41 recall and 12 corrupt matches are now confirmed**, not remembered (an
earlier note said 37/41). `strict` passing is the designed outcome: the gates catch
corruption, not low recall — which is exactly why a fuzzy matcher tuned for match
rate is the wrong lever.

**Bug found and fixed in CLAUDE.md while doing this:** the command reference said
`baselines.py naive|strict` for *both* agents. `crosswalk-decider`'s modes are
actually `first_soc|always_skip`, and an unrecognised mode **silently falls through
to the default rather than erroring** — so `strict` re-ran `first_soc` and produced a
byte-identical "second baseline". Corrected in `CLAUDE.md`.

Not verified:

- **The live Claude "Explain" path has never run end-to-end.** No `ANTHROPIC_API_KEY`
  is set in this environment. The `anthropic` SDK is installed (0.121.0) and the
  fallback path is verified for all 13 titles (`live=false`, correct text). The key
  drops in via env var with no code change — but the live branch is untested.
- **No agent gate has been run against a real agent's output** — only baselines. Doing
  that means dispatching each subagent over its golden inputs (41 items for
  `title-matcher`, 13 for `crosswalk-decider`) via `--emit-inputs`, which is a
  deliberate job, not a side effect of a session.
- **`demo/index.html` has had no human visual review** since the 2026-08-07 restyle to
  the system-font treatment. Structure and JS syntax are checked; layout is not.
- **No `.claude/verify` script exists** in this repo, though the global Stop hook
  refers to one.

## Risks and what's next

1. **HIGHEST: six files are uncommitted and unpushed.** `CLAUDE.md` (modified) plus
   `HANDOFF.md` and the five `docs/*.md`. The remote's last push was 2026-08-07.
   This is not only a backup gap — the working-tree `CLAUDE.md` instructs readers to
   read `docs/onet-attribution.md` before shipping O*NET data, and **that file does
   not exist on the remote**, so a fresh clone points at nothing. Commit and push.
2. **`data/raw/` is fully tracked despite the gitignore rule.** 47 files, including
   all four payroll CSV chunks and the O*NET database files, were force-added, and
   `data/raw/*` has no effect on already-tracked paths. Checked 2026-09-08: the repo
   is **private**; the payroll CSVs carry only `title_description` and `base_salary`
   (no PII); no credentials appear in any tracked file (`socrata_app_tokens.txt` is a
   scraped documentation page, not a token); O*NET redistribution is permitted under
   CC BY 4.0 per `onet_license_db.txt`. **If this repo is ever made public that data
   goes with it, and `git rm --cached` would not remove it from history.**
3. **22 open `DECISION:` lines** — the `crosswalk-decider` agent's job. Budget roughly
   one agent run plus 8 task classifications per title.
4. **`SCHOOL SECRETARY` needs worker validation most.** It is the most exposed title
   in the demo (5 of 8 shown tasks `automatable`) and three of those five are
   context-free statements classified by fiat under unresolved ambiguity **A2**.
5. **Rubric v0.1 ambiguities A1 and A2 are unresolved** and both distort scoring at
   volume. Read `scoring/classifications_round1.md` before scoring in bulk.
6. **No O*NET→NYC mapping is committed.** Exact matching tops out at 32.3% by
   headcount. The next lever is suffix stripping and abbreviation expansion — *not* a
   fuzzy-similarity threshold, which would force the 73 true-negative residuals in
   `data/raw/join_unmatched_after_normalization.txt`.
7. **Grade level is unrecoverable** for `TEACHER` / `TEACHER-GENERAL ED` /
   `TEACHER SPECIAL EDUCATION` (101,630 people). O*NET has no grade-agnostic K-12 code.
8. **If the demo is ever hosted** (HF Spaces was discussed): `serve.py` is stdlib
   `HTTPServer` and will not run there as-is — either a static-only Space, or
   Gradio/Docker with the key in Space secrets. Log counts only, never session
   identity: this tool tells identifiable municipal workers their job may be
   automated, and title plus borough narrows to very few people.
