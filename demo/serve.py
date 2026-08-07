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
    "classifications mean for one NYC civil-service job.\n\n"
    "FORMAT — output exactly these three sections, each header on its own line "
    "followed by a colon, and nothing else. No markdown, no bullets, no preamble:\n"
    "What AI can help with: 1-2 sentences naming the specific tasks.\n"
    "What stays with you: 1-2 sentences naming the specific tasks and why.\n"
    "Your move: 1 sentence on what makes this worker's judgment more valuable, "
    "not less.\n\n"
    "RULES: ground every claim in the task data provided; never give a percentage, "
    "score, or 'replaceable' framing; address the worker as 'you'; warm and direct. "
    "Where an anchor is given, respect the distinction it draws: a task anchored by "
    "capability stays human because it needs a body present, and that can change as "
    "technology improves; a task anchored by authority stays human because the law "
    "vests the act in a person, and no model release changes it. Never collapse the "
    "two, and never total them into an overall figure for the job. "
    "If the title is not an occupation at all, still use the three headers: say what "
    "the title actually is, why no honest answer exists for it, and what would have "
    "to happen first."
)


def live_explain(title):
    import anthropic  # imported lazily so the demo runs without the package
    t = BY_TITLE[title]
    if t.get("tasks"):
        facts = "\n".join(
            f"- [{x['class']}] {x['task']}"
            + (f"\n    anchor: {x['anchor']}" if x.get("anchor") else "")
            for x in t["tasks"])
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

    def end_headers(self):
        # the demo is edited live; never let the browser serve a stale build
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

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
