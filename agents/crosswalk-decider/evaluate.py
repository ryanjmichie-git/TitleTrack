#!/usr/bin/env python3
"""Grade crosswalk-decider predictions against golden.jsonl. Deterministic, offline.

    python3 evaluate.py --predictions preds.jsonl
    python3 evaluate.py --emit-inputs inputs.jsonl

Prediction format, one JSON object per line:
    {"id": "L04", "verdict": "CODE",   "soc": "21-1099.00", "rationale": "..."}
    {"id": "L01", "verdict": "SKIP",   "soc": null, ...}
    {"id": "L09", "verdict": "BLOCKED", "soc": null, ...}

Verdicts: CODE | SKIP | NO_SINGLE_CODE | BLOCKED  (the vocabulary defined at the
head of the LOW section in data/crosswalk_candidates.md).

Gates — each encodes a failure mode this project documented the hard way:

  G1 forbidden-code   — citing a code the golden marks forbidden (e.g.
                        13-1151.00 for JOB TRAINING PARTICIPANT: the strongest
                        lexical match in the set, and exactly backwards).
  G2 forbidden-verdict— a verdict the correction history rules out (e.g. SKIP
                        for COLLEGE ASSISTANT after the CUNY correction; any
                        confident answer for LIEUTENANT, which is BLOCKED on
                        evidence the repo does not contain).
  G3 fabricated-code  — any cited SOC absent from onet_Occupation_Data.txt.

Accuracy is reported per verdict; gates are hard.
"""
import argparse, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "..", "data", "raw")
VERDICTS = {"CODE", "SKIP", "NO_SINGLE_CODE", "BLOCKED"}


def load_soc():
    codes = set()
    with open(os.path.join(RAW, "onet_Occupation_Data.txt"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            codes.add(r["O*NET-SOC Code"])
    return codes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions")
    ap.add_argument("--emit-inputs")
    args = ap.parse_args()

    soc_universe = load_soc()
    cases = [json.loads(l) for l in open(os.path.join(HERE, "golden.jsonl"), encoding="utf-8")]
    for c in cases:  # golden self-check
        e = c["expected"]
        for code in e["accept_soc"] + e["forbid_soc"]:
            if code not in soc_universe:
                sys.exit(f"GOLDEN INVALID: {c['id']} cites unknown SOC {code}")

    if args.emit_inputs:
        with open(args.emit_inputs, "w") as fh:
            for c in cases:
                fh.write(json.dumps({"id": c["id"], "title": c["title"]}) + "\n")
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
    correct = 0; rows = []
    for c in cases:
        cid = c["id"]; e = c["expected"]
        p = preds.get(cid)
        if p is None:
            rows.append((cid, "-", "MISSING")); continue
        v = p.get("verdict"); code = p.get("soc")
        if v not in VERDICTS:
            rows.append((cid, str(v), "INVALID VERDICT")); continue
        if code and code not in soc_universe:
            g3.append((cid, code))
        if code and code in e["forbid_soc"]:
            g1.append((cid, code))
        if v in e["must_not_verdict"] or (v == "CODE" and "CODE" in e["must_not_verdict"]):
            g2.append((cid, v))
        ok = (v == e["verdict"]) and (v != "CODE" or code in e["accept_soc"])
        correct += int(ok)
        rows.append((cid, f"{v}{' ' + code if code else ''}",
                     "ok" if ok else f"want {e['verdict']}{' ' + e['soc'] if e['soc'] else ''}"))

    for r in rows:
        print(f"  {r[0]}  {r[1]:24s} {r[2]}")
    print(f"correct {correct}/{len(cases)}")
    def gate(name, viol):
        print(f"GATE {name:17s} {'PASS' if not viol else 'FAIL ' + str(viol)}")
        return not viol
    ok = all([gate("forbidden-code", g1), gate("forbidden-verdict", g2), gate("fabricated-code", g3)])
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
