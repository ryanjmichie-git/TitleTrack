# The demo/ prototype

How the worker-facing prototype in demo/ is generated, gated, and served, and which raw evidence files are worth opening.

Referenced from CLAUDE.md.

## `demo/` — the worker-facing prototype

Run it: `python demo/serve.py` → `http://localhost:8765`. Five titles; pick one,
see verified facts, O*NET task statements labeled by rubric v0.1, and open DCAS
exams. `python demo/evaluate.py` is a **hard-fail gate written before any demo
data existed** — it re-derives every headcount, salary block, exam, SOC code, and
task statement from the committed sources and exits 1 on any mismatch. It also
bans occupation-level aggregate keys outright (`risk_score`, `ai_score`, …),
enforcing rubric ambiguity A1: statement-level classes must never be aggregated.

- `demo/demo_data.json` is **generated** — never hand-edit it; change
  `build_demo_data.py` or `task_classifications.json` and rebuild.
- `task_classifications.json` carries an `_anchors` block recording *why* each
  `human_anchored` task is anchored. `capability` (P0) erodes as models and
  robotics improve; `authority` (D0) does not move until a statute or rule
  changes. The front-end surfaces this distinction, and it is the demo's argument.
- The live explain panel needs `ANTHROPIC_API_KEY` and the `anthropic` package.
  Without either it silently serves `fallback_explanations.json` and labels the
  answer as precomputed on screen. **The fallback path is the tested one.**

`build_top40.py` reproduces the PowerShell output **byte for byte** — BOM, CRLF,
and PS 5.1's column-aligned `ConvertTo-Json` layout — so a Linux rebuild does not
churn the committed artifact. `python scripts/build_top40.py --check` is the
regression test; it currently passes at 47,524 bytes (was 47,331 before the
CUNY-caveat correction of 2026-08-07). Keep the two generators in
step: any change to one must be mirrored, or `--check` fails by design.

Useful raw files: `join_unmatched_after_normalization.txt` (the 73 residuals — read
before "fixing" the matcher), `k397_agencies_2025.json` (employer checks),
`onet_license_db.txt` (attribution source), `ratelimit_burst_log.json`.
