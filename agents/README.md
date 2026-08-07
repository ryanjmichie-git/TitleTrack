# TitleTrack agents

Two custom agents, each with a spec, a hand-verified golden set, a deterministic
offline evaluator with hard gates, and adversarial baselines that prove the
evaluator discriminates. Agent definitions live in `.claude/agents/` and are
invocable as Claude Code subagents.

| agent | job | goldens | gates |
|---|---|---|---|
| `title-matcher` | exam title → exact payroll `title_description`, or `NO_MATCH` | 54 cases from the real join residuals | forced-match, wrong-title, invalid-title |
| `crosswalk-decider` | payroll title → `CODE / SKIP / NO_SINGLE_CODE / BLOCKED` | the 13 decided LOW crosswalk entries | forbidden-code, forbidden-verdict, fabricated-code |

## Design notes

**Goldens are byproducts of work done by hand, not invented test data.** The
matcher's cases are the actual residuals from
`data/raw/join_unmatched_after_normalization.txt`; the decider's are the 13
crosswalk decisions of 2026-08-07, each with its reasoning on record in
`data/crosswalk_candidates.md`.

**Gates encode the failure modes that matter, and they are hard.** This
project's central claim is that a wrong answer delivered confidently is worse
than a gap delivered honestly. Recall is reported; corruption fails the run.

**The evaluators validate their own golden sets on every run** — every payroll
title against `k397_all_titles.json`, every SOC against
`onet_Occupation_Data.txt`. A golden that drifts from the raw data refuses to
grade.

**Baselines prove the harness has teeth**, in both directions:

```
agents/title-matcher$ python3 baselines.py strict | ... evaluate.py
  recall 0/41, all gates PASS            # the current pipeline: safe, blind
agents/title-matcher$ python3 baselines.py naive | ... evaluate.py
  recall 35/41, forced-match FAIL (12)   # fuzzy matching: high recall, corrupt
```

The naive baseline matches `Dental Assistant (NYC H+H)` to
`STUDENT LEGAL ASSISTANT` and `ADDICTION COUNSELOR (NYC H+H)` to
`CORRECTIONAL COUNSELOR`. That is what a similarity threshold does to this data,
and it is why the gate exists. The agent's job is the space between the two
baselines: recall above 0 with gates clean.

```
agents/crosswalk-decider$ python3 baselines.py first_soc  | ...   # 3/13, 2 gates FAIL
agents/crosswalk-decider$ python3 baselines.py always_skip | ...  # 5/13, 1 gate FAIL
```

**The baselines already earned their keep once:** the naive matcher's first run
exposed three mislabeled goldens (TM18, TM34, TM43 — payroll abbreviates
`CONGREG`, one-words `IRONWORK`, and drops an S in
`PRINCIPAL POLICE COMMUNICATION TECHNICIAN`). The labels were corrected and the
case notes preserve the history. Run the adversary before trusting the oracle.

## Running

```
# grade a predictions file
python3 agents/title-matcher/evaluate.py --predictions preds.jsonl
python3 agents/crosswalk-decider/evaluate.py --predictions preds.jsonl

# get label-free inputs for an agent run
python3 agents/title-matcher/evaluate.py --emit-inputs inputs.jsonl

# regenerate baseline predictions
python3 agents/title-matcher/baselines.py naive > preds.jsonl
```

Everything is offline and deterministic: stdlib only, no network, exit code 0
iff all gates pass.

## Invoking the agents

From Claude Code in this repo: ask for the agent by name ("use the
title-matcher agent to …"). Each definition in `.claude/agents/` instructs the
agent to read its SPEC, work item by item, verify claims against the raw files
with Grep before emitting them, run its evaluator, and iterate until
`RESULT: PASS` — and forbids editing the golden set or evaluator to get there.
