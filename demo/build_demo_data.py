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
    # NOTE: COMMUNITY COORDINATOR (21-1099.00) and ADJUNCT LECTURER (25-1199.00) are
    # decided in crosswalk_candidates.md but are deliberately NOT in this demo: O*NET
    # publishes zero task statements for "All Other" residual codes, so there is no
    # task-level analysis to show. Having a code is not the same as having data.
    "SERGEANT-":                          {"verdict": "CODE", "soc": "33-1012.00", "skip_reason": None},
    "CITY SEASONAL AIDE": {
        "verdict": "SKIP", "soc": None,
        "skip_reason": ("Hiring category, not an occupation — 17 salaried rows "
                        "out of 2,414. Coding it as a job would corrupt the "
                        "analysis. (L13, data/crosswalk_candidates.md)"),
    },
    "TEACHER- PER SESSION": {
        "verdict": "SKIP", "soc": None,
        "skip_reason": ("A pay code, not a job — and the largest title in the city. "
                        "It is how DOE pays existing teachers hourly for after-school "
                        "and summer work, so these are overwhelmingly the same people "
                        "already counted under TEACHER. The payroll file even carries a "
                        "separate agency named DEPT OF ED PER SESSION TEACHER (81,516 "
                        "rows). The null median is the tell. (L01)"),
    },
    "ELECTION WORKER": {
        "verdict": "SKIP", "soc": None,
        "skip_reason": ("A civic stipend role, not an occupation. Zero salaried rows, "
                        "and the city keeps BOARD OF ELECTION POLL WORKERS (36,732 rows) "
                        "separate from its actual year-round staff (1,027). Coding it "
                        "would launder a stipend into a job. (L02)"),
    },
    "STUDENT AIDE": {
        "verdict": "SKIP", "soc": None,
        "skip_reason": ("A hiring category, not an occupation — students placed across "
                        "many different agencies doing many different things. There is "
                        "no single job here to describe. (L10)"),
    },
    "JOB TRAINING PARTICIPANT": {
        "verdict": "SKIP", "soc": None,
        "skip_reason": ("A hiring category, not an occupation — 18 salaried rows out of "
                        "4,021. The title names the program someone is enrolled in, not "
                        "the work they do. (L12)"),
    },
    "F/T SCHOOL AIDE": {
        "verdict": "NO_SINGLE_CODE", "soc": None,
        "skip_reason": ("These are 9,217 real workers doing real jobs — this is NOT a "
                        "skip. The blocker is that the plausible occupations sit in "
                        "three different SOC major groups: education (25), office (43), "
                        "and food service (35). No residual code spans them, so any "
                        "single pick misclassifies the majority. Resolving it needs DOE "
                        "school-assignment data, which is not in the payroll file. (L03)"),
    },
    "COLLEGE ASSISTANT": {
        "verdict": "NO_SINGLE_CODE", "soc": None,
        "skip_reason": ("Real work, but the title spans clerical, tutoring, lab, and "
                        "library assignments across CUNY's community colleges — "
                        "different occupations under one payroll label. Picking one "
                        "would be a guess dressed as a finding. (L06)"),
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
