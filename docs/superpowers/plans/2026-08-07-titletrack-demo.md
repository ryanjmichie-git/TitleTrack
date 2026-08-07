# TitleTrack Demo ("What AI Means for Your City Job") Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A 3-screen laptop demo where an NYC frontline worker picks their payroll title and sees (1) verified facts about their job, (2) O*NET tasks labeled automatable / augmentable / human-anchored, (3) open DCAS exams as concrete next steps — plus a live Claude "explain this for me" panel — all gated by a hard-fail eval in the repo's existing style.

**Architecture:** Everything derives from committed files (`data/raw/top40_titles.json`, `data/raw/onet_Task_Statements.txt`, `data/raw/onet_Occupation_Data.txt`, DECISION lines in `data/crosswalk_candidates.md`). A deterministic build script produces `demo/demo_data.json`; a gated eval (`demo/evaluate.py`) verifies every number, SOC code, and task against source files and enforces the no-occupation-score rule; a static single-page front-end reads the JSON; a tiny Python server serves the page and proxies one Claude API call with a precomputed fallback.

**Tech Stack:** Python 3.11 stdlib (+ `anthropic` SDK for the live panel only), vanilla HTML/CSS/JS. No build tools, no frameworks, no network dependency except the optional live Claude call.

**Design principles (per Boris Cherny / Andrej Karpathy):** evals before features — the gate exists and fails before any demo data does; every step small and independently verifiable; the model gets a target to iterate against (`python demo/evaluate.py`); deterministic code does the data work, Claude only explains and personalizes; commit after every green step; no fuzzy matching, no invented numbers — the eval hard-fails anything not traceable to a committed source file.

**Time budget note:** Tasks 1 and 2 are independent — dispatch Task 2's decider agents first (they run in the background), then do Task 1 while waiting.

---

## File map

| Path | Role |
|---|---|
| `demo/evaluate.py` | Create — hard-fail gated eval (the target everything iterates against) |
| `demo/build_demo_data.py` | Create — deterministic builder: sources → `demo/demo_data.json` |
| `demo/task_classifications.json` | Create — per-task rubric labels (prototype, Claude-drafted, human-skimmed) |
| `demo/demo_data.json` | Generated — the only file the front-end reads |
| `demo/fallback_explanations.json` | Create — canned "explain" output per title (offline fallback) |
| `demo/index.html` | Create — the 3-screen page (single file, inline CSS/JS) |
| `demo/serve.py` | Create — static server + `POST /api/explain` (live Claude or fallback) |
| `demo/PITCH.md` | Create — 3-minute pitch script |
| `data/crosswalk_candidates.md` | Modify — fill 4 `DECISION: ___` lines (M08, M10, M11, H10) |

---

### Task 1: The gated eval (write it first; it must fail first)

**Files:**
- Create: `demo/evaluate.py`

- [ ] **Step 1: Write the eval**

```python
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
```

- [ ] **Step 2: Run it and confirm it fails for the right reason**

Run: `python demo/evaluate.py`
Expected: exit 1 with `FAIL demo/demo_data.json does not exist`

- [ ] **Step 3: Commit**

```bash
git add demo/evaluate.py
git commit -m "Add gated eval for demo data integrity (fails until demo exists)"
```

---

### Task 2: Decide the 4 demo titles (crosswalk-decider agents)

**Files:**
- Modify: `data/crosswalk_candidates.md` (the `DECISION: ___` lines for M08 · CARETAKER, M10 · SCHOOL SAFETY AGENT, M11 · TRAFFIC ENFORCEMENT AGENT, H10 · EMERGENCY MEDICAL SPECIALIST-EMT)

- [ ] **Step 1: Dispatch four `crosswalk-decider` agents in parallel** (Agent tool, `subagent_type: "crosswalk-decider"`), one per title. Prompt each with exactly: *"Decide the DECISION line for [entry ID · TITLE] in data/crosswalk_candidates.md using the verdict vocabulary and the two rules at the head of the LOW section. Return the full replacement DECISION line plus a 2-sentence justification. Do not edit any file."*

- [ ] **Step 2: Verify each returned SOC code** against `data/raw/onet_Occupation_Data.txt` (repo convention — never cite codes from memory):

Run: `python -c "print([l.split('\t')[:2] for l in open('data/raw/onet_Occupation_Data.txt',encoding='utf-8') if l.startswith('<CODE>')])"` for each code.
Expected: one row per code, occupation title printed.

- [ ] **Step 3: Write the DECISION lines into `data/crosswalk_candidates.md`** replacing `DECISION: ___` for the four entries, keeping each entry's existing prose intact. If the decider returns `SKIP` or `NO SINGLE CODE` for any title, record that verdict honestly — the demo renders those via the SKIP path (Task 3), and that *is* the pitch.

- [ ] **Step 4: Commit**

```bash
git add data/crosswalk_candidates.md
git commit -m "Decide M08/M10/M11/H10 for demo (crosswalk-decider, codes verified vs Occupation Data)"
```

---

### Task 3: Deterministic data builder

**Files:**
- Create: `demo/build_demo_data.py`
- Generated: `demo/demo_data.json`

- [ ] **Step 1: Write the builder**

```python
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
    "TRAFFIC ENFORCEMENT AGENT":          {"verdict": "DECIDE", "soc": "DECIDE", "skip_reason": None},
    "SCHOOL SAFETY AGENT":                {"verdict": "DECIDE", "soc": "DECIDE", "skip_reason": None},
    "EMERGENCY MEDICAL SPECIALIST-EMT":   {"verdict": "DECIDE", "soc": "DECIDE", "skip_reason": None},
    "CARETAKER":                          {"verdict": "DECIDE", "soc": "DECIDE", "skip_reason": None},
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
                 "class": cls.get(d["soc"], {}).get(r["Task ID"], "unclassified")}
                for r in rows[:MAX_TASKS]
            ]
        titles.append(entry)

    out = {
        "generated_from": ["data/raw/top40_titles.json",
                           "data/raw/onet_Task_Statements.txt",
                           "data/raw/onet_Occupation_Data.txt",
                           "data/crosswalk_candidates.md DECISION lines",
                           "demo/task_classifications.json"],
        "classification_status": "prototype — rubric v0.1, needs worker validation",
        "titles": titles,
    }
    (ROOT / "demo/demo_data.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote demo/demo_data.json ({len(titles)} titles)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Fill `DECISIONS` from Task 2's committed DECISION lines**, run the builder

Run: `python demo/build_demo_data.py`
Expected: `wrote demo/demo_data.json (5 titles)`

- [ ] **Step 3: Run the gate; confirm partial progress**

Run: `python demo/evaluate.py`
Expected: FAIL only on (a) task classes = `unclassified` (Task 4), (b) `index.html` (Task 5), (c) fallback file (Task 6). All source-tracing checks PASS. Any SOC/task/number failure means the builder or a DECISION is wrong — fix before proceeding.

- [ ] **Step 4: Commit**

```bash
git add demo/build_demo_data.py demo/demo_data.json
git commit -m "Add deterministic demo data builder (all facts trace to committed sources)"
```

---

### Task 4: Classify the tasks (rubric v0.1, prototype-labeled)

**Files:**
- Create: `demo/task_classifications.json`
- Regenerate: `demo/demo_data.json`

- [ ] **Step 1: Read the rubric and its known limits**: `scoring/rubric.md` and `scoring/classifications_round1.md`. Two constraints bind: statement-level classes must NEVER be aggregated to an occupation, and context-free statements are classified by fiat — hence the "prototype" label everywhere.

- [ ] **Step 2: Classify each task shown in `demo_data.json`** (the executor — Claude — does this directly; it is exactly the rubric's automatable/augmentable/human_anchored call, ~24-32 statements). Write:

```json
{
  "<soc_code>": {
    "<task_id>": "automatable | augmentable | human_anchored"
  }
}
```

One entry per `(soc_code, task_id)` pair appearing in `demo_data.json`. When genuinely torn between two classes, choose `augmentable` — the middle class overstates neither direction, matching the rubric's conservatism.

- [ ] **Step 3: Human skim** — print a table for the user to eyeball (they know these jobs):

Run: `python -c "import json; dd=json.load(open('demo/demo_data.json',encoding='utf-8-sig')); [print(t['title_description'],'\n  ' + '\n  '.join(f\"[{x['class'][:5]}] {x['task'][:80]}\" for x in t.get('tasks',[]))) for t in dd['titles']]"`
Expected: table prints; flag anything absurd in the summary to the user rather than blocking.

- [ ] **Step 4: Rebuild and re-gate**

Run: `python demo/build_demo_data.py && python demo/evaluate.py`
Expected: all task-class checks PASS; remaining failures only index.html + fallback.

- [ ] **Step 5: Commit**

```bash
git add demo/task_classifications.json demo/demo_data.json
git commit -m "Add prototype task classifications (rubric v0.1, statement-level only)"
```

---

### Task 5: The front-end (3 screens, single file)

**Files:**
- Create: `demo/index.html`

- [ ] **Step 1: Invoke the `frontend-design` skill** before writing, then write `index.html`. The complete working baseline below is the floor, not the ceiling — improve the visual design (typography, color, spacing, motion) per the skill, but keep every `id`, `class` hook, data binding, and the attribution text byte-identical so the eval and `serve.py` still hold.

```html
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TitleTrack — What AI means for your city job</title>
<style>
  :root{--ink:#16211c;--paper:#f7f5ef;--card:#ffffff;--accent:#0f6b4f;--accent2:#b45309;
        --auto:#b45309;--aug:#0f6b4f;--human:#1d4ed8;--muted:#5b6660;--line:#e2ded2}
  *{box-sizing:border-box;margin:0}
  body{font:16px/1.55 Georgia,'Times New Roman',serif;background:var(--paper);color:var(--ink);padding:2rem 1rem}
  .wrap{max-width:880px;margin:0 auto}
  h1{font-size:2rem;letter-spacing:-.01em} h1 em{color:var(--accent);font-style:italic}
  .sub{color:var(--muted);margin:.4rem 0 1.6rem}
  .tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:.8rem}
  .tile{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:1rem;
        cursor:pointer;text-align:left;font:inherit;transition:transform .08s}
  .tile:hover{transform:translateY(-2px);border-color:var(--accent)}
  .tile b{display:block;font-size:1.02rem} .tile span{color:var(--muted);font-size:.85rem}
  .back{background:none;border:none;color:var(--accent);cursor:pointer;font:inherit;padding:0;margin-bottom:1rem}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1.3rem;margin-bottom:1rem}
  .facts{display:flex;gap:2rem;flex-wrap:wrap} .facts div b{font-size:1.4rem;display:block}
  .facts div span{color:var(--muted);font-size:.85rem}
  .task{display:flex;gap:.7rem;padding:.55rem 0;border-top:1px solid var(--line);align-items:baseline}
  .pill{flex:none;font:700 .68rem/1.6 system-ui;letter-spacing:.04em;text-transform:uppercase;
        padding:0 .55rem;border-radius:99px;color:#fff}
  .pill.automatable{background:var(--auto)} .pill.augmentable{background:var(--aug)}
  .pill.human_anchored{background:var(--human)}
  .legend{color:var(--muted);font-size:.85rem;margin:.5rem 0 0}
  .exam{border-top:1px solid var(--line);padding:.6rem 0}
  .exam b{color:var(--accent)} .exam span{color:var(--muted);font-size:.9rem}
  .note{background:#fdf6ec;border:1px solid #ecd9b7;border-radius:8px;padding:.8rem 1rem;
        font-size:.9rem;color:#7a5410;margin-bottom:1rem}
  .skipbox{border-left:4px solid var(--accent2);padding-left:1rem}
  #explain-out{white-space:pre-wrap;font-size:.95rem;min-height:1.5rem}
  .btn{background:var(--accent);color:#fff;border:none;border-radius:8px;padding:.6rem 1.1rem;
       font:inherit;cursor:pointer} .btn:disabled{opacity:.5}
  footer{color:var(--muted);font-size:.78rem;margin-top:2.5rem;border-top:1px solid var(--line);padding-top:1rem}
  .hide{display:none}
</style></head><body><div class="wrap">

<section id="screen-landing">
  <h1>How might AI change <em>your</em> work?</h1>
  <p class="sub">For the people who run New York City — not just the 9-to-5ers.
     Built on the city's own payroll and exam data, task by task. No scores, no guesses.</p>
  <div class="tiles" id="tiles"></div>
</section>

<section id="screen-role" class="hide">
  <button class="back" onclick="show('landing')">&larr; All titles</button>
  <div class="card">
    <h1 id="r-title"></h1>
    <p class="sub" id="r-occ"></p>
    <div class="facts">
      <div><b id="r-head"></b><span>people in FY2025</span></div>
      <div><b id="r-pay"></b><span id="r-paynote"></span></div>
    </div>
  </div>
  <div class="note">Task labels are a <b>prototype</b> classification (rubric v0.1) —
    they describe how AI could touch each task, and they need worker validation.
    They are never rolled up into a job-level score, because no honest one exists.</div>
  <div class="card" id="r-tasks-card">
    <h2>The actual work, task by task</h2>
    <div id="r-tasks"></div>
    <p class="legend"><span class="pill automatable">automatable</span> AI could do much of this
      &nbsp;<span class="pill augmentable">augmentable</span> AI assists, a person decides
      &nbsp;<span class="pill human_anchored">human anchored</span> stays with people</p>
  </div>
  <div class="card skipbox hide" id="r-skip">
    <h2>This title isn't a job — and that matters</h2>
    <p id="r-skipreason"></p>
    <p class="legend">A generic "AI risk score" for this title would be wrong for every
       person under it. Making the work visible has to come first.</p>
  </div>
  <div class="card" id="r-exams-card">
    <h2>Your next move: open civil-service exams</h2>
    <div id="r-exams"></div>
  </div>
  <div class="card">
    <h2>Explain this for me</h2>
    <p class="sub">A plain-language read of what the labels above mean for someone in this job —
       written live by Claude, grounded only in the verified data on this page.</p>
    <button class="btn" id="explain-btn" onclick="explain()">Explain</button>
    <p id="explain-out"></p>
  </div>
</section>

<footer>
  This page includes information from the O*NET 30.3 Database by the U.S. Department of Labor,
  Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license.
  O*NET&reg; is a trademark of USDOL/ETA.<br>
  TitleTrack has modified all or some of this information. USDOL/ETA has not approved, endorsed,
  or tested these modifications.<br>
  Payroll: NYC Office of Payroll Administration (k397-673e), FY2025. Exams: DCAS (4ptz-hmtc).
</footer>
</div>
<script>
let DATA=null, CURRENT=null;
const $=id=>document.getElementById(id);
const money=n=>n==null?"—":"$"+Math.round(n).toLocaleString();

fetch("demo_data.json").then(r=>r.json()).then(d=>{DATA=d;renderTiles();});

function renderTiles(){
  $("tiles").innerHTML=DATA.titles.map((t,i)=>
    `<button class="tile" onclick="openRole(${i})"><b>${t.title_description}</b>
     <span>${t.headcount_fy2025.toLocaleString()} New Yorkers</span></button>`).join("");
}
function show(name){ $("screen-landing").classList.toggle("hide",name!=="landing");
  $("screen-role").classList.toggle("hide",name!=="role"); window.scrollTo(0,0); }
function openRole(i){
  const t=CURRENT=DATA.titles[i];
  $("r-title").textContent=t.title_description;
  $("r-head").textContent=t.headcount_fy2025.toLocaleString();
  $("r-pay").textContent=money(t.salary.median);
  $("r-paynote").textContent=t.salary.median==null
    ? "no annual-salary rows — a fact, not a gap"
    : `median, ${t.salary.basis} (${t.salary.n_excluded.toLocaleString()} non-annual rows excluded)`;
  const coded=!!t.soc_code;
  $("r-occ").textContent=coded?`O*NET occupation: ${t.occupation_title} (${t.soc_code})`:"";
  $("r-tasks-card").classList.toggle("hide",!coded);
  $("r-skip").classList.toggle("hide",coded);
  if(coded){$("r-tasks").innerHTML=t.tasks.map(x=>
    `<div class="task"><span class="pill ${x.class}">${x.class.replace("_"," ")}</span>
     <span>${x.task}</span></div>`).join("");}
  else{$("r-skipreason").textContent=t.skip_reason;}
  $("r-exams").innerHTML=t.open_exams.length?t.open_exams.map(e=>
    `<div class="exam"><b>${e.exam_title}</b> — exam #${e.exam_number}<br>
     <span>Apply ${e.application_period_start} to ${e.application_period_end} · ${e.eligibility||"—"}</span></div>`).join("")
    :`<div class="exam"><span>No open DCAS exams for this title right now.</span></div>`;
  $("explain-out").textContent=""; show("role");
}
async function explain(){
  const btn=$("explain-btn"); btn.disabled=true;
  $("explain-out").textContent="Thinking…";
  try{
    const r=await fetch("/api/explain",{method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({title:CURRENT.title_description})});
    const j=await r.json();
    $("explain-out").textContent=j.explanation+(j.live?"":"\n\n(precomputed — live API unavailable)");
  }catch(e){$("explain-out").textContent="Could not reach the local server — run demo/serve.py.";}
  btn.disabled=false;
}
</script></body></html>
```

- [ ] **Step 2: Smoke-test rendering** (server needed for `fetch`; fallback file doesn't exist yet, so only test page + data)

Run: `python -m http.server 8765 --directory demo` (background), then open `http://localhost:8765`
Expected: tiles render with real headcounts; clicking a coded title shows labeled tasks and exams; clicking CITY SEASONAL AIDE shows the honest SKIP panel. Kill the server after.

- [ ] **Step 3: Run the gate**

Run: `python demo/evaluate.py`
Expected: attribution + prototype checks PASS; only the fallback-file check still FAILs.

- [ ] **Step 4: Commit**

```bash
git add demo/index.html
git commit -m "Add 3-screen demo front-end (landing / role view / action plan)"
```

---

### Task 6: Local server + live Claude "explain" with fallback

**Files:**
- Create: `demo/serve.py`
- Create: `demo/fallback_explanations.json`

- [ ] **Step 1: Write the fallback file** — the executor (Claude) writes one 4-6 sentence explanation per demo title, in this exact voice (non-alarmist, task-grounded, ends on leverage). Shape:

```json
{
  "TRAFFIC ENFORCEMENT AGENT": "AI may help draft incident summaries and flag records for a traffic enforcement agent, but it should not independently decide penalties or take enforcement action. ...",
  "SCHOOL SAFETY AGENT": "...",
  "EMERGENCY MEDICAL SPECIALIST-EMT": "...",
  "CARETAKER": "...",
  "CITY SEASONAL AIDE": "..."
}
```

Every key must exactly match a `title_description` in `demo_data.json` (the eval enforces this). No percentages, no "X% of this job", no "replaceable".

- [ ] **Step 2: Write the server**

```python
#!/usr/bin/env python3
"""Serves the demo and one API endpoint. Run: python demo/serve.py [port]

POST /api/explain {"title": "..."} ->
  {"explanation": "...", "live": true|false}
Live path uses the anthropic SDK (claude-opus-5); any failure — no key, no
network, refusal — falls back to fallback_explanations.json. The demo never
breaks on stage.
"""
import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

HERE = Path(__file__).resolve().parent
FALLBACK = json.loads((HERE / "fallback_explanations.json").read_text(encoding="utf-8"))
DATA = json.loads((HERE / "demo_data.json").read_text(encoding="utf-8-sig"))
BY_TITLE = {t["title_description"]: t for t in DATA["titles"]}

SYSTEM = (
    "You explain, in plain language for the worker themself, what task-level AI "
    "classifications mean for one NYC civil-service job. Rules: ground every claim "
    "in the task data provided; never give a percentage, score, or 'replaceable' "
    "framing; name which tasks AI may assist and which stay human-accountable; end "
    "with one sentence on what makes this worker's judgment more valuable, not less. "
    "4-6 sentences, warm and direct, no headers."
)


def live_explain(title):
    import anthropic  # imported lazily so the demo runs without the package
    t = BY_TITLE[title]
    if t.get("tasks"):
        facts = "\n".join(f"- [{x['class']}] {x['task']}" for x in t["tasks"])
    else:
        facts = f"This title is not an occupation: {t['skip_reason']}"
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content":
                   f"Job title: {title}\nHeadcount FY2025: {t['headcount_fy2025']}\n"
                   f"Task classifications (prototype, rubric v0.1):\n{facts}"}],
    )
    if resp.stop_reason == "refusal":
        raise RuntimeError("refusal")
    return next(b.text for b in resp.content if b.type == "text")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(HERE), **kw)

    def do_POST(self):
        if self.path != "/api/explain":
            self.send_error(404)
            return
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        title = body.get("title", "")
        try:
            out = {"explanation": live_explain(title), "live": True}
        except Exception as e:
            print(f"live call failed ({e!r}); serving fallback", file=sys.stderr)
            out = {"explanation": FALLBACK.get(title, "No explanation available."),
                   "live": False}
        payload = json.dumps(out).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"TitleTrack demo -> http://localhost:{port}")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
```

- [ ] **Step 3: Test the fallback path** (no key set)

Run: `python demo/serve.py` (background), then
`curl -s -X POST http://localhost:8765/api/explain -H "Content-Type: application/json" -d "{\"title\": \"TRAFFIC ENFORCEMENT AGENT\"}"`
Expected: JSON with `"live": false` and the fallback text.

- [ ] **Step 4: Test the live path** (only if `ANTHROPIC_API_KEY` is set or `ant auth status` shows a profile; `pip install anthropic` if missing). Same curl.
Expected: `"live": true` with fresh text and no percentages. If no key is available now, note it in the summary — the venue key slots in via env var with zero code changes.

- [ ] **Step 5: Run the full gate**

Run: `python demo/evaluate.py`
Expected: **GATE PASSED**.

- [ ] **Step 6: Commit**

```bash
git add demo/serve.py demo/fallback_explanations.json
git commit -m "Add demo server: live Claude explain panel with precomputed fallback"
```

---

### Task 7: Pitch script

**Files:**
- Create: `demo/PITCH.md`

- [ ] **Step 1: Write `demo/PITCH.md`** with exactly this structure (fill the [bracketed] beats from the live data):

```markdown
# TitleTrack — 3-minute pitch

## Open (20s) — the title that lies
"A title like CITY SEASONAL AIDE tells a New Yorker almost nothing about how AI
will affect their work. It can hide many different jobs — and a generic AI risk
score gets all of them wrong. TitleTrack makes the work visible before making a
recommendation."

## The problem (30s)
550,000 people work for NYC. [X]% of the largest titles aren't standard salaried
9-to-5 roles — per-session teachers, seasonal aides, hourly caretakers. No tool
connects their actual title to what AI means for their actual tasks, because the
city's titles connect to nothing: no shared keys, and titles lie (CARETAKER is a
NYCHA janitor; TEACHER- PER SESSION isn't even a job).

## Demo (90s) — one worker journey
1. Landing → pick TRAFFIC ENFORCEMENT AGENT (2,508 people, $49,830 median).
2. Role view → real O*NET tasks, three labels, never a score. Point at the
   prototype banner: honesty is the feature.
3. Action plan → [N] open DCAS exams with real application windows.
4. "Explain this for me" → live Claude call, grounded only in the page's data.
5. Back → CITY SEASONAL AIDE → the SKIP panel. "Refusing to answer is the
   right answer here, and our eval enforces it."

## Why trust it (30s)
Every number traces to a committed city snapshot; every SOC code is verified
against the O*NET occupation file; a gated eval fails the build on any forced
match, any invented number, any job-level score. Our naive-matcher baseline
produced 12 corrupt matches — that's why the discipline exists.

## Close (10s)
"We are not building a replacement score. We are building an honest navigation
tool: where AI can reduce drudgery, where humans remain accountable, and what
NYC workers can do next."
```

- [ ] **Step 2: Fill the bracketed numbers** from `demo_data.json` / `CLAUDE.md` (30.1% of top-40 headcount for the not-a-job finding; exam count from the data). Commit:

```bash
git add demo/PITCH.md
git commit -m "Add 3-minute pitch script"
```

---

### Task 8: Final verification and push

- [ ] **Step 1: Full gate + regression**

Run: `python demo/evaluate.py && python scripts/build_top40.py --check`
Expected: `GATE PASSED` and `OK byte-identical ... (47524 bytes)`.

- [ ] **Step 2: End-to-end dry run** — `python demo/serve.py`, click through all 5 titles and the explain button once. Verify no console errors.

- [ ] **Step 3: Push**

```bash
git push
```

---

## Self-review notes

- **Spec coverage:** worker-first 3 screens (T5), evals (T1, run in T3-T6, T8), decisions for demo titles (T2), rubric-conformant classification with no aggregation (T4 + eval check 5), $200-credit live call with offline fallback (T6), pitch (T7), attribution (T5 + eval check 7).
- **Known judgment points left to the executor:** visual polish beyond the baseline (frontend-design skill, T5 step 1); the classification calls themselves (T4); fallback prose (T6 step 1). Everything else is specified.
- **If time runs out:** the demo is usable after Task 5 (unclassified pills will show — ugly but honest) and fully safe after Task 6. Task 7 can be improvised from CLAUDE.md. Never skip Task 8 step 1.
