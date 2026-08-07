#!/usr/bin/env python3
"""Builds demo/demo_data.json from committed sources. Deterministic, offline.

SOC codes below are copied verbatim from the DECISION lines in
data/crosswalk_candidates.md (Task 2). evaluate.py cross-checks every code
against onet_Occupation_Data.txt, so a typo fails the gate, not the demo.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# EXECUTOR: replace each "DECIDE" with the verdict/code from the DECISION
# lines written in Task 2. A SKIP/NO_SINGLE_CODE verdict gets soc=None and a
# one-line reason quoted from the entry.
DECISIONS = {
    "TRAFFIC ENFORCEMENT AGENT":          {"verdict": "CODE", "soc": "33-3041.00", "skip_reason": None},
    "SCHOOL SAFETY AGENT":                {"verdict": "CODE", "soc": "33-9032.00", "skip_reason": None},
    "EMERGENCY MEDICAL SPECIALIST-EMT":   {"verdict": "CODE", "soc": "29-2042.00", "skip_reason": None},
    "CARETAKER":                          {"verdict": "CODE", "soc": "37-2011.00", "skip_reason": None},
    "CITY SEASONAL AIDE": {
        "verdict": "SKIP", "soc": None,
        "skip_reason": ("Hiring category, not an occupation — 17 salaried rows "
                        "out of 2,414. Coding it as a job would corrupt the "
                        "analysis. (L13, data/crosswalk_candidates.md)"),
    },
}
MAX_TASKS = 8


def load_tsv(p):
    lines = p.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, l.split("\t"))) for l in lines[1:]]


def main():
    for name, d in DECISIONS.items():
        if "DECIDE" in (d["verdict"], d["soc"]):
            sys.exit(f"ERROR: DECISIONS['{name}'] not filled in from crosswalk_candidates.md")

    top40 = {t["title_description"]: t for t in json.loads(
        (ROOT / "data/raw/top40_titles.json").read_text(encoding="utf-8-sig"))["titles"]}
    occ = {r["O*NET-SOC Code"]: (r["Title"], r["Description"])
           for r in load_tsv(ROOT / "data/raw/onet_Occupation_Data.txt")}
    task_rows = load_tsv(ROOT / "data/raw/onet_Task_Statements.txt")
    cls_path = ROOT / "demo/task_classifications.json"
    cls = json.loads(cls_path.read_text(encoding="utf-8")) if cls_path.exists() else {}
    # Anchors are why a task is human_anchored: "capability" (P0) erodes as models
    # and robotics improve; "authority" (D0) does not move until a rule changes.
    anchors = cls.get("_anchors", {})
    # EXTERNAL research, deliberately kept in its own file and its own UI block.
    # Everything else on the page is re-derived from data/raw/ by evaluate.py;
    # this is not, and the seam must stay visible from across the room.
    rungs = json.loads((ROOT / "demo/next_rung.json").read_text(encoding="utf-8"))

    titles = []
    for name, d in DECISIONS.items():
        src = top40[name]  # KeyError here = wrong title string; fix here, never fuzz
        entry = {
            "title_description": name,
            "headcount_fy2025": src["headcount_fy2025"],
            "salary": src["salary"],
            "open_exams": src["open_exams"],
            "verdict": d["verdict"],
            "soc_code": d["soc"],
            "skip_reason": d["skip_reason"],
            "next_rung": rungs.get(name),
        }
        if d["soc"]:
            occ_title, occ_desc = occ[d["soc"]]
            entry["occupation_title"] = occ_title
            entry["occupation_description"] = occ_desc
            rows = [r for r in task_rows if r["O*NET-SOC Code"] == d["soc"]]
            rows.sort(key=lambda r: (r.get("Task Type") != "Core", int(r["Task ID"])))
            entry["tasks"] = [
                {"task_id": r["Task ID"], "task": r["Task"],
                 "task_type": r.get("Task Type", ""),
                 "class": cls.get(d["soc"], {}).get(r["Task ID"], "unclassified"),
                 "anchor": anchors.get(d["soc"], {}).get(r["Task ID"], "")}
                for r in rows[:MAX_TASKS]
            ]
        titles.append(entry)

    out = {
        "generated_from": ["data/raw/top40_titles.json",
                           "data/raw/onet_Task_Statements.txt",
                           "data/raw/onet_Occupation_Data.txt",
                           "data/crosswalk_candidates.md DECISION lines",
                           "demo/task_classifications.json"],
        "external_sources": {
            "next_rung": "demo/next_rung.json — DCAS Notices of Examination and union "
                         "publications, compiled 2026-08-07. NOT re-derived from the "
                         "committed API snapshots the way every other figure here is.",
        },
        "classification_status": "prototype — rubric v0.1, needs worker validation",
        "titles": titles,
    }
    (ROOT / "demo/demo_data.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote demo/demo_data.json ({len(titles)} titles)")


if __name__ == "__main__":
    main()
