#!/usr/bin/env python3
"""Grade title-matcher predictions against golden.jsonl. Deterministic, offline.

    python3 evaluate.py --predictions preds.jsonl        # grade
    python3 evaluate.py --emit-inputs inputs.jsonl       # write label-free inputs

Prediction format, one JSON object per line:
    {"id": "TM05", "action": "MATCH",    "payroll_title": "<exact payroll string>"}
    {"id": "TM01", "action": "NO_MATCH", "reason": "foreign_employer"}

Exit code 0 only if every gate passes. Gates are hard by design:

  G1 forced-match  — any MATCH on a gated NO_MATCH case (foreign employer,
                     umbrella artifact, rank absent from payroll). This is the
                     project thesis: a matcher tuned for match rate corrupts
                     the data. One violation fails the run.
  G2 wrong-title   — a MATCH whose payroll_title is not an accepted answer for
                     that case. A wrong match is silent corruption; a miss is a
                     visible gap. Zero tolerance.
  G3 invalid-title — a MATCH naming a string that is not in the payroll
                     universe at all (fabrication).

Recall is reported, not gated: the strict baseline shows ~0 recall with clean
gates, and the point of the agent is to raise recall while keeping them clean.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "..", "data", "raw")


def load_universe():
    with open(os.path.join(RAW, "k397_all_titles.json"), encoding="utf-8-sig") as fh:
        return {r.get("title_description") for r in json.load(fh)} - {None}


def load_golden():
    cases = []
    with open(os.path.join(HERE, "golden.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            cases.append(json.loads(line))
    return cases


def validate_golden(cases, universe):
    """The golden set is itself under test: every referenced payroll title must
    exist in the raw universe, or the eval refuses to run."""
    for c in cases:
        for a in c["accept"]:
            if a["action"] == "MATCH" and a["payroll_title"] not in universe:
                sys.exit(f"GOLDEN INVALID: {c['id']} references unknown payroll "
                         f"title {a['payroll_title']!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions")
    ap.add_argument("--emit-inputs")
    args = ap.parse_args()

    universe = load_universe()
    cases = load_golden()
    validate_golden(cases, universe)

    if args.emit_inputs:
        with open(args.emit_inputs, "w") as fh:
            for c in cases:
                fh.write(json.dumps({"id": c["id"], "exam_title": c["exam_title"]}) + "\n")
        print(f"wrote {len(cases)} inputs to {args.emit_inputs}")
        return 0
    if not args.predictions:
        ap.error("--predictions or --emit-inputs required")

    preds = {}
    # utf-8-sig: PS 5.1's `Out-File -Encoding utf8` prepends a BOM, and a BOM
    # crash exits 1 exactly like a legitimate gate failure. Tolerate it here;
    # repo-internal files stay strict utf-8.
    with open(args.predictions, encoding="utf-8-sig") as fh:
        for line in fh:
            if line.strip():
                p = json.loads(line)
                preds[p["id"]] = p

    g1 = []; g2 = []; g3 = []
    correct = 0; matchable = 0; recovered = 0; missing = []
    by_class = {}
    for c in cases:
        cid = c["id"]
        accepted_titles = {a["payroll_title"] for a in c["accept"] if a["action"] == "MATCH"}
        nomatch_ok = any(a["action"] == "NO_MATCH" for a in c["accept"])
        if accepted_titles:
            matchable += 1
        p = preds.get(cid)
        if p is None:
            missing.append(cid)
            continue
        act = p.get("action")
        ok = False
        if act == "MATCH":
            t = p.get("payroll_title")
            if t not in universe:
                g3.append((cid, t))
            if c.get("gate") and not accepted_titles:
                g1.append((cid, t))          # forced match on a gated NO_MATCH case
            if t in accepted_titles:
                ok = True; recovered += 1
            elif t in universe:
                g2.append((cid, t))          # real title, wrong one
        elif act == "NO_MATCH":
            ok = nomatch_ok
        if ok:
            correct += 1
        cls = c.get("class", "?")
        s = by_class.setdefault(cls, [0, 0]); s[1] += 1; s[0] += int(ok)

    print(f"cases {len(cases)}  scored {len(cases)-len(missing)}  missing {len(missing)}")
    print(f"correct            {correct}/{len(cases)-len(missing)}")
    print(f"recall(matchable)  {recovered}/{matchable}")
    for cls in sorted(by_class):
        s = by_class[cls]
        print(f"  {cls:12s} {s[0]}/{s[1]}")
    def gate(name, viol):
        print(f"GATE {name:14s} {'PASS' if not viol else 'FAIL ' + str(viol)}")
        return not viol
    ok = all([gate("forced-match", g1), gate("wrong-title", g2), gate("invalid-title", g3)])
    if missing:
        print(f"NOTE: {len(missing)} unanswered case(s) count against accuracy, not gates: {missing}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
