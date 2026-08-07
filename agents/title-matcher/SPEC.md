# title-matcher — agent spec

## Mission

Given a DCAS exam title, return the FY2014–FY2025 payroll `title_description` it
denotes — **the same civil-service title, as the exact string in
`data/raw/k397_all_titles.json`** — or `NO_MATCH` with a reason. The goal is to
recover the join residuals that normalization misses (currently 0/41 recoverable
cases) **without ever forcing a match**.

## Non-goals

- Maximizing match rate. A wrong match is silent data corruption; a miss is a
  visible gap. The eval encodes this asymmetry as hard gates.
- Fuzzy similarity scoring. `baselines.py naive` is the cautionary tale: 35/41
  recall, 12 forced matches, FAIL.
- Semantic/SOC matching. That is the crosswalk's job, not this agent's.

## Output contract

One JSON object per input line, written to a predictions file:

```json
{"id": "TM05", "action": "MATCH",    "payroll_title": "ADMINISTRATIVE PARKS & RECREATION MANAGER"}
{"id": "TM01", "action": "NO_MATCH", "reason": "foreign_employer"}
```

`payroll_title` must be byte-exact from the universe file. Reasons:
`foreign_employer` | `absent_title` | `not_a_title` | `ambiguous_employer`.

## Decision procedure

1. **Strip exam-file artifacts**: leading list bullets (`- `, `• `, and the
   mojibake form `â€¢ `), schedule suffixes `(Prom)/(Pro)/(PRO)`, trailing
   punctuation. These are formatting, never meaning.
2. **Read the remaining parenthetical — do not blindly strip it.** Three kinds:
   - **Foreign employer** (`NYC H+H`, `Hospitals`, `Transit Authority`): the
     employer is absent from the FY2025 agency list (`k397_agencies_2025.json`)
     → `NO_MATCH / foreign_employer`, full stop. The base string being a real
     payroll title (`CLERICAL ASSOCIATE (NYC H+H)`) does not change this.
   - **Domestic employer** (`HA`/`Housing Authority`, `Da`, `Fire`/`FDNY`,
     `CUNY` community colleges): drop the marker, keep matching.
   - **Content** (`Crane Operator (Any Motive Power Except Steam)` → payroll
     `CRANE OPERATOR AMPES`): the parenthetical may BE the match key,
     abbreviated. Check before discarding.
3. **Search the universe for legitimate variants** — transformations with a
   documented mechanism, not a similarity score:
   singular/plural (`PARKS/PARK`, `BUILDINGS/BUILDING`); `AND`/`&`; compound
   spacing (`IRON WORK`/`IRONWORK`); hyphen spacing (`- EMT`/`-EMT`);
   possessives (`Mason's`/`MASONS`); apostrophe placement (`WORKERS'`/`WORKER'S`);
   known abbreviations (`SUPT`, `SPVR`, `ASSOC`, `ADMIN/ADM`, `ENFRCMNT`,
   `SPEC`, `CONGREG`); payroll-side typos (`TECHNICAN`, `INPECTOR`); suffix
   noise (`- NON-SPVR`, `- AL 1 ONLY 40 HR`, trailing `#`).
4. **Never cross a rank boundary.** `Assistant`/`Associate`/`Senior`/
   `Supervising`/`Principal`/`Administrative` prefixes name *different titles*
   on the same ladder. If the ranked title is absent from the universe, the
   answer is `NO_MATCH / absent_title`, not the adjacent rank.
   (`SUPERVISOR`/`SUPERVISING` on the *same* rank is word-form drift and fine.)
5. **When two mechanisms disagree, prefer `NO_MATCH`.** The gray cases in the
   golden set accept either answer; everything else accepts exactly one.

## Verification loop

```
python3 agents/title-matcher/evaluate.py --emit-inputs inputs.jsonl
# ... produce predictions ...
python3 agents/title-matcher/evaluate.py --predictions preds.jsonl
```

Gates (all hard): no forced match on gated cases, no wrong-title match, no
fabricated title. Target: beat strict-baseline recall (0/41) with gates clean.
Iterate until `RESULT: PASS`, then report the scorecard verbatim.

## Golden set provenance

54 cases distilled from `data/raw/join_unmatched_after_normalization.txt` — the
actual join residuals — each label hand-verified against
`k397_all_titles.json`. Three labels (TM18, TM34, TM43) were corrected after
the naive baseline exposed abbreviated payroll variants the original labeling
grep missed; the notes on those cases preserve the history. The evaluator
re-validates every golden label against the raw universe on every run.
