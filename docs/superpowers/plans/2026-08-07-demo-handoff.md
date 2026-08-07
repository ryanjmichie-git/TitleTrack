# Handoff prompt — paste into a fresh session after compaction

---

We're at the Claude Impact Lab hackathon ("Future of Work — make sure AI lifts workers instead of leaving them behind"). Presentations are imminent; judged on problem/solution clarity, logic, and front-end quality. $200 API credits available for live demo calls.

Execute the plan at `docs/superpowers/plans/2026-08-07-titletrack-demo.md` using the superpowers:executing-plans skill (or subagent-driven-development). Read `CLAUDE.md` first — it is accurate and hard-won; follow its conventions exactly (never blend pay bases, never cite SOC codes from memory, null medians are facts, `data/raw/*` needs `git add -f`).

Context you need:
- The plan builds a 3-screen laptop demo (`demo/`) — pick an NYC title → see rubric-labeled O*NET tasks → open DCAS exams — gated by `demo/evaluate.py` (hard-fail, written first).
- Task 2 dispatches the existing `crosswalk-decider` agent (4 parallel runs) to fill the `DECISION: ___` lines for M08 CARETAKER, M10 SCHOOL SAFETY AGENT, M11 TRAFFIC ENFORCEMENT AGENT, H10 EMERGENCY MEDICAL SPECIALIST-EMT in `data/crosswalk_candidates.md`. Dispatch those FIRST (background), then do Task 1 while they run.
- CITY SEASONAL AIDE is already decided (SKIP) and is deliberately in the demo as the "titles that lie" moment.
- The live "explain" panel goes through `demo/serve.py` → anthropic SDK → `claude-opus-5`, with `demo/fallback_explanations.json` as the always-works fallback. If no `ANTHROPIC_API_KEY` is set, build fallback-first and say so; the venue key drops in via env var.
- Commit after every green step; push at the end (Task 8). `python demo/evaluate.py` is the target to iterate against; `python scripts/build_top40.py --check` must still pass (47,524 bytes) before pushing.
- Work autonomously; only stop for decisions the plan explicitly leaves to me (classification sanity-check is a flag-in-summary, not a blocker).

Start now with Task 2 dispatch + Task 1.

---

# Claude Research prompts (run on claude.ai in parallel with the build)

1. **Audience reality check:** "How do NYC civil-service workers — especially hourly and frontline titles like traffic enforcement agents, school safety agents, EMTs, and NYCHA caretakers — currently learn about DCAS civil-service exams, promotions, and career mobility? What are the documented pain points (application windows, exam fees, list delays), and what do unions (DC 37, PBA, UFT) and worker advocates say workers most need? Cite NYC-specific sources."

2. **Defending the no-score stance:** "Summarize the academic debate on occupation-level vs task-level AI/automation exposure measures: Frey & Osborne (2013) and its critiques, Arntz/Gregory/Zierahn (OECD), Autor's task framework, and recent LLM-exposure papers (e.g. Eloundou et al. 2023). What are the strongest documented arguments that occupation-level 'automation risk scores' mislead, and that task-level analysis without aggregation is more defensible? I need citable ammunition for a judged Q&A."

3. **Demo craft:** "What distinguishes winning 3-minute hackathon demos for civic-tech and data tools? Find concrete structures used by winners of NYC BigApps, Code for America, and recent AI-for-good hackathons: how they balance one user's story vs methodology, how they handle live-demo failure risk, and what judges say they reward. Give me a beat-by-beat template."

4. **Trustworthy civic UI:** "Collect design principles and exemplary references for data tools that need to feel trustworthy and government-adjacent without being drab: NYC.gov / USDS / gov.uk design systems, plus standout civic-data sites (city dashboards, WNYC/THE CITY data projects). What typography, color, and labeling choices signal 'verified public data' — and what accessibility requirements (WCAG) matter most for a demo shown on one laptop?"

5. **The mobility layer (stretch):** "For NYC civil-service titles like Traffic Enforcement Agent, School Safety Agent, and EMT, what are the documented promotion ladders and lateral pathways (e.g. TEA → Associate TEA; SSA → NYPD; EMT → Paramedic → FDNY)? Which require promotional vs open-competitive DCAS exams? Cite NYC DCAS, NYPD, FDNY sources — I want to show one real 'next rung' per title."
