# crosswalk-decider — agent spec

## Mission

Given a payroll title from `data/crosswalk_candidates.md`, return a crosswalk
verdict using the vocabulary defined at the head of that file's LOW section:

| verdict | meaning |
|---|---|
| `CODE` + SOC | one code, at the precision the data supports (family residuals are complete answers, not placeholders) |
| `SKIP` | the title is not an occupation — pay code, hiring category, civic role |
| `NO_SINGLE_CODE` | real work spanning SOC **major groups**, with no residual spanning them |
| `BLOCKED` | a specific, named piece of evidence would decide it and is not in the repo |

The agent is graded on the 13 decided LOW items; its purpose is the 27 open
MEDIUM/HIGH lines.

## Non-goals

- Lexical matching. The strongest lexical match in the whole sheet
  (`JOB TRAINING PARTICIPANT` → `13-1151.00 Training and Development
  Specialists`) is exactly backwards — trainee coded as trainer.
- Guessing under ambiguity. `BLOCKED` with a named resolver query beats a
  plausible code. The eval hard-fails a confident answer on `LIEUTENANT`.
- Filling every line. Ten titles legitimately end in `SKIP` or
  `NO_SINGLE_CODE`; that is the finding, not a failure.

## Output contract

```json
{"id": "L04", "verdict": "CODE", "soc": "21-1099.00", "rationale": "one sentence citing evidence"}
{"id": "L09", "verdict": "BLOCKED", "soc": null, "rationale": "resolver: agency_name group-by, denied in sandbox"}
```

## Decision procedure

1. **Read the euphemism flags first** (`data/crosswalk_candidates.md`, top
   section, including its dated corrections). Several titles' names are lies:
   `CARETAKER` is a janitor, `Administrative ___` is a manager, `Principal` is
   a seniority grade.
2. **Check whether the title names work at all.** A pay mechanism, hiring
   category, or civic role (`- PER SESSION`, `SEASONAL`, `STUDENT`,
   `PARTICIPANT`, `ELECTION WORKER`) → `SKIP`. Corroborate in the data:
   dedicated payroll agencies (`DEPT OF ED PER SESSION TEACHER`,
   `BOARD OF ELECTION POLL WORKERS`) and null/near-null salaried-row counts in
   `data/raw/top40_titles.json` are the tells.
3. **Verify every candidate SOC exists** in `data/raw/onet_Occupation_Data.txt`
   before citing it. Never from memory.
4. **Weigh evidence in this order**: payroll-internal facts (agency names,
   medians, salaried-row counts) > DCAS exam-file structure
   (`4ptz-hmtc_full.json` — which ranks/services have exams) > O*NET title
   evidence > lexical similarity (never decisive alone).
5. **Apply the two sheet rules**: prefer the family residual when candidates
   disagree about the *nature* of the work; prefer specificity only when they
   agree on the work. Never let a lexical match outrank an evidentiary one.
6. **Candidates spanning SOC major groups** with no spanning residual →
   `NO_SINGLE_CODE`. **A named missing fact** (e.g. the agency split of a
   uniformed rank) → `BLOCKED`, and state the exact query.
7. **Distrust stale premises.** One golden exists solely because a documented
   claim ("CUNY is barely in the payroll file") was false. If a decision rests
   on a checkable claim, check it.

## Verification loop

```
python3 agents/crosswalk-decider/evaluate.py --emit-inputs inputs.jsonl
# ... decide each item, one at a time, no batching ...
python3 agents/crosswalk-decider/evaluate.py --predictions preds.jsonl
```

Gates (hard): no forbidden code, no forbidden verdict (SKIP where corrected
evidence forbids it; any confident verdict on BLOCKED items), no fabricated
SOC. Iterate until `RESULT: PASS`, then report the scorecard verbatim.

## Golden set provenance

The 13 LOW decisions of 2026-08-07, recorded with their reasoning in
`data/crosswalk_candidates.md`. Gates encode the four failure modes that
review surfaced: double-counting (L01), inverted lexical match (L12), stale
premise (L06/L11), and overconfidence on missing evidence (L09).
