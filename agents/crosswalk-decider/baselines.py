#!/usr/bin/env python3
"""Two non-agent baselines proving the decider eval discriminates.

    python3 baselines.py first_soc  > preds_first.jsonl  # always code something
    python3 baselines.py always_skip > preds_skip.jsonl  # never code anything

`first_soc` models a matcher that refuses to say anything but a code: it takes
the first SOC listed among each entry's candidates in data/crosswalk_candidates.md.
It must trip the forbidden-code gate on L01 (teaching code -> double count) and
the forbidden-verdict gate on L09 (confident answer where the evidence is not in
the repo).

`always_skip` models reflexive exclusion. It scores on the five real skips and
must trip the forbidden-verdict gate on L06/L11 — titles whose SKIP option died
with the CUNY correction.

Candidate SOCs are parsed from crosswalk_candidates.md so the baselines stay in
sync with the sheet.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHEET = os.path.join(HERE, "..", "..", "data", "crosswalk_candidates.md")


def candidates_by_item():
    text = open(SHEET, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^## (L\d{2}) ·", text, re.M):
        lid = m.group(1)
        block = text[m.end():m.end() + 1200]
        out[lid] = re.findall(r"`(\d{2}-\d{4}\.\d{2})`", block)
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "first_soc"
    cases = [json.loads(l) for l in open(os.path.join(HERE, "golden.jsonl"), encoding="utf-8")]
    cands = candidates_by_item()
    for c in cases:
        if mode == "always_skip":
            out = {"id": c["id"], "verdict": "SKIP", "soc": None}
        else:
            socs = cands.get(c["id"], [])
            out = {"id": c["id"], "verdict": "CODE" if socs else "SKIP",
                   "soc": socs[0] if socs else None}
        print(json.dumps(out))


if __name__ == "__main__":
    main()
