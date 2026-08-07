#!/usr/bin/env python3
"""Two non-agent baselines that prove the eval discriminates.

    python3 baselines.py naive  > preds_naive.jsonl   # fuzzy, forced matching
    python3 baselines.py strict > preds_strict.jsonl  # normalize-only

`naive` is the matcher this project warns against: difflib similarity with a
threshold, always taking the best candidate. It posts high recall and MUST
fail the forced-match and wrong-title gates — if it ever passes, the golden
set has lost its teeth.

`strict` is the existing pipeline rule (uppercase + strip parentheticals +
collapse whitespace, exact only). It must pass every gate; its recall is the
floor the agent has to beat.
"""
import difflib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "..", "data", "raw")

with open(os.path.join(RAW, "k397_all_titles.json"), encoding="utf-8-sig") as fh:
    UNIVERSE = sorted({r.get("title_description") for r in json.load(fh)} - {None})


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"\([^)]*\)", "", s)).upper().strip()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "naive"
    cases = [json.loads(l) for l in open(os.path.join(HERE, "golden.jsonl"), encoding="utf-8")]
    exact = {norm(t): t for t in UNIVERSE}
    for c in cases:
        q = norm(c["exam_title"])
        if mode == "strict":
            if q in exact:
                out = {"id": c["id"], "action": "MATCH", "payroll_title": exact[q]}
            else:
                out = {"id": c["id"], "action": "NO_MATCH", "reason": "absent_title"}
        else:  # naive: force the best fuzzy candidate above a low bar
            best = difflib.get_close_matches(q, [norm(t) for t in UNIVERSE], n=1, cutoff=0.6)
            if best:
                # map back to an original-cased title
                t = next(t for t in UNIVERSE if norm(t) == best[0])
                out = {"id": c["id"], "action": "MATCH", "payroll_title": t}
            else:
                out = {"id": c["id"], "action": "NO_MATCH", "reason": "no_candidate"}
        print(json.dumps(out))


if __name__ == "__main__":
    main()
