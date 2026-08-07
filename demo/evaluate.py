#!/usr/bin/env python3
"""Gated eval for the TitleTrack demo. Exits 1 on any failure.

Every number, SOC code, and task statement in demo_data.json must trace to a
committed source file. No occupation-level AI score may exist anywhere.
Run: python demo/evaluate.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo"
FAILURES = []


def check(cond, msg):
    if cond:
        print(f"  PASS  {msg}")
    else:
        print(f"  FAIL  {msg}")
        FAILURES.append(msg)


def load_json(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def load_tsv(p):
    lines = p.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, l.split("\t"))) for l in lines[1:]]


def main():
    # --- 1. demo_data.json exists and parses ---
    dd_path = DEMO / "demo_data.json"
    if not dd_path.exists():
        print("FAIL  demo/demo_data.json does not exist (run build_demo_data.py)")
        sys.exit(1)
    dd = load_json(dd_path)
    titles = dd["titles"]
    check(len(titles) >= 5, f"at least 5 demo titles present ({len(titles)})")

    # --- 2. every fact traces to top40_titles.json ---
    top40 = {t["title_description"]: t
             for t in load_json(ROOT / "data/raw/top40_titles.json")["titles"]}
    for t in titles:
        name = t["title_description"]
        src = top40.get(name)
        check(src is not None, f"{name}: exists in top40_titles.json")
        if src is None:
            continue
        check(t["headcount_fy2025"] == src["headcount_fy2025"],
              f"{name}: headcount matches source")
        check(t["salary"] == src["salary"],
              f"{name}: salary block matches source verbatim (basis+median+exclusions)")
        check(t["open_exams"] == src["open_exams"],
              f"{name}: open_exams match source verbatim")

    # --- 3. every SOC code exists in Occupation Data (repo convention) ---
    occ = {r["O*NET-SOC Code"]: r["Title"]
           for r in load_tsv(ROOT / "data/raw/onet_Occupation_Data.txt")}
    coded = [t for t in titles if t.get("soc_code")]
    check(len(coded) >= 3, f"at least 3 coded titles ({len(coded)})")
    for t in coded:
        check(t["soc_code"] in occ,
              f"{t['title_description']}: SOC {t['soc_code']} exists in Occupation Data")
        if t["soc_code"] in occ:
            check(t["occupation_title"] == occ[t["soc_code"]],
                  f"{t['title_description']}: occupation title matches Occupation Data")

    # --- 4. every task is verbatim from Task Statements for that SOC ---
    task_rows = load_tsv(ROOT / "data/raw/onet_Task_Statements.txt")
    tasks_by_soc = {}
    for r in task_rows:
        tasks_by_soc.setdefault(r["O*NET-SOC Code"], set()).add(r["Task"])
    for t in coded:
        legit = tasks_by_soc.get(t["soc_code"], set())
        for task in t.get("tasks", []):
            check(task["task"] in legit,
                  f"{t['title_description']}: task verbatim in Task Statements "
                  f"({task['task'][:50]}...)")

    # --- 5. classes valid; NO occupation-level aggregate anywhere ---
    VALID = {"automatable", "augmentable", "human_anchored"}
    for t in coded:
        check(len(t.get("tasks", [])) >= 4,
              f"{t['title_description']}: at least 4 tasks shown")
        for task in t.get("tasks", []):
            check(task.get("class") in VALID,
                  f"{t['title_description']}: task class valid ({task.get('class')})")
    banned = ("risk_score", "automation_score", "percent_automatable",
              "exposure_score", "ai_score")
    raw = dd_path.read_text(encoding="utf-8-sig").lower()
    for b in banned:
        check(b not in raw, f"no occupation-level aggregate key '{b}' anywhere "
                            "(rubric rule: statement classes never aggregate)")

    # --- 6. SKIP titles render the honest path, never tasks ---
    skips = [t for t in titles if t.get("verdict") == "SKIP"]
    check(len(skips) >= 1, "at least one SKIP title (the 'titles that lie' moment)")
    for t in skips:
        check(not t.get("soc_code") and not t.get("tasks"),
              f"{t['title_description']}: SKIP carries no SOC code and no tasks")
        check(bool(t.get("skip_reason")),
              f"{t['title_description']}: SKIP carries its reason")

    # --- 7. O*NET attribution, verbatim, in the page ---
    html_path = DEMO / "index.html"
    if html_path.exists():
        html = html_path.read_text(encoding="utf-8")
        for frag in ("O*NET 30.3 Database", "USDOL/ETA", "CC BY 4.0",
                     "O*NET&reg;", "has modified all or some of this information"):
            check(frag in html, f"index.html carries attribution fragment '{frag}'")
        check("prototype" in html.lower(),
              "index.html labels classifications as prototype/needs validation")
    else:
        check(False, "demo/index.html exists")

    # --- 8. fallback explanations cover every demo title ---
    fb_path = DEMO / "fallback_explanations.json"
    if fb_path.exists():
        fb = load_json(fb_path)
        for t in titles:
            check(t["title_description"] in fb,
                  f"fallback explanation exists for {t['title_description']}")
    else:
        check(False, "demo/fallback_explanations.json exists")

    print()
    if FAILURES:
        print(f"GATE FAILED — {len(FAILURES)} failure(s)")
        sys.exit(1)
    print("GATE PASSED")


if __name__ == "__main__":
    main()
