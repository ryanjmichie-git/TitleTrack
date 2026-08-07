#!/usr/bin/env python3
"""Builds docs/TitleTrack-pitch.pdf — the 5-slide hackathon deck.

Deterministic: same input, byte-comparable output. Run:
    python docs/make_pitch_deck.py
"""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent / "TitleTrack-pitch.pdf"
W, H = landscape((7.5 * inch, 13.333 * inch))  # 16:9

BG     = HexColor("#FBFBFD")
INK    = HexColor("#1D1D1F")
INK2   = HexColor("#6E6E73")
INK3   = HexColor("#A1A1A6")
LINE   = HexColor("#E3E3E8")
ACCENT = HexColor("#0071E3")
AUTO   = HexColor("#B35309")
AUG    = HexColor("#00734A")
HUMAN  = HexColor("#0053C2")

M = 0.95 * inch          # margin
BOLD, REG = "Helvetica-Bold", "Helvetica"


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(c, text, x, y, width, font=REG, size=13, leading=None, color=INK2):
    leading = leading or size * 1.45
    c.setFont(font, size)
    c.setFillColor(color)
    for ln in wrap(text, font, size, width):
        c.drawString(x, y, ln)
        y -= leading
    return y


def page(c, kicker=None):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    if kicker:
        c.setFont(BOLD, 11)
        c.setFillColor(ACCENT)
        c.drawString(M, H - M + 0.05 * inch, kicker.upper())
        c.setStrokeColor(LINE)
        c.setLineWidth(1)
        c.line(M, H - M - 0.12 * inch, W - M, H - M - 0.12 * inch)


def foot(c, txt, color=INK3):
    size = 8.5
    c.setFont(REG, size)
    c.setFillColor(color)
    lines = wrap(txt, REG, size, W - 2 * M)
    y = 0.52 * inch + (len(lines) - 1) * size * 1.35
    for ln in lines:
        c.drawString(M, y, ln)
        y -= size * 1.35


def bullets(c, items, x, y, width, size=13.5, gap=0.30 * inch):
    """items: list of (bold_lead, rest). bold_lead may be ''."""
    for lead, rest in items:
        c.setFillColor(ACCENT)
        c.circle(x + 3.2, y + 4.6, 3.2, stroke=0, fill=1)
        tx = x + 16
        w = width - 16
        if lead:
            c.setFont(BOLD, size)
            c.setFillColor(INK)
            lead_w = stringWidth(lead + " ", BOLD, size)
            if lead_w < w * 0.9:
                c.drawString(tx, y, lead)
                # fill line 1 beside the bold lead, then re-wrap the rest at FULL
                # width — wrapping everything at the narrow width leaves a ragged
                # short-line column all the way down the slide.
                words, line1, i = rest.split(), "", 0
                while i < len(words):
                    trial = f"{line1} {words[i]}".strip()
                    if stringWidth(trial, REG, size) <= w - lead_w:
                        line1, i = trial, i + 1
                    else:
                        break
                c.setFont(REG, size)
                c.setFillColor(INK2)
                c.drawString(tx + lead_w, y, line1)
                y -= size * 1.42
                for ln in wrap(" ".join(words[i:]), REG, size, w):
                    c.drawString(tx, y, ln)
                    y -= size * 1.42
            else:
                y = para(c, lead + " " + rest, tx, y, w, REG, size)
        else:
            y = para(c, rest, tx, y, w, REG, size)
        y -= gap - size * 0.4
    return y


def chip(c, x, y, label, color, bg):
    pad, size = 7, 9.5
    tw = stringWidth(label, BOLD, size)
    c.setFillColor(bg)
    c.roundRect(x, y - 4, tw + pad * 2, 19, 9.5, stroke=0, fill=1)
    c.setFont(BOLD, size)
    c.setFillColor(color)
    c.drawString(x + pad, y + 1.5, label)
    return x + tw + pad * 2 + 8


# ─────────────────────────────────────────────────────────── slides

def slide_title(c):
    page(c)
    c.setFillColor(ACCENT)
    c.setFont(BOLD, 12)
    c.drawString(M, H - M - 0.1 * inch, "CLAUDE IMPACT LAB  ·  THE FUTURE OF WORK")

    c.setFillColor(INK)
    c.setFont(BOLD, 78)
    c.drawString(M, H / 2 + 0.85 * inch, "TitleTrack")

    y = para(c, "Pick your city job title, see what AI actually means for your work "
                "task-by-task — no fake risk scores — and see the exam "
                "that’s your next move up.",
             M, H / 2 + 0.1 * inch, W - 2 * M - 2.6 * inch, REG, 19, 27, INK2)

    c.setStrokeColor(LINE)
    c.line(M, y - 0.35 * inch, M + 2.2 * inch, y - 0.35 * inch)
    c.setFont(BOLD, 15)
    c.setFillColor(INK)
    c.drawString(M, y - 0.75 * inch, "Ryan Michie")
    c.setFont(REG, 12)
    c.setFillColor(INK2)
    c.drawString(M, y - 1.05 * inch, "Built on NYC’s own payroll, exam, and occupation data")
    c.showPage()


def slide_problem(c):
    page(c, "The problem")
    y = H - M - 0.75 * inch

    c.setFont(BOLD, 27)
    c.setFillColor(INK)
    for ln in wrap("“How do we make sure AI lifts workers instead of leaving "
                   "them behind?”", BOLD, 27, W - 2 * M):
        c.drawString(M, y, ln)
        y -= 36
    c.setFont(REG, 12)
    c.setFillColor(INK3)
    c.drawString(M, y - 4, "— the question this event asked")
    y -= 0.62 * inch

    y = para(c, "For 550,219 people on New York City’s payroll, that question is "
                "currently answered by headlines and generic “40% of jobs at risk” "
                "scores. Those scores are wrong, because they treat a job title as if it "
                "were one thing. The city’s own data proves it isn’t:",
             M, y, W - 2 * M - 0.4 * inch, REG, 14, 21, INK2)
    y -= 0.28 * inch

    bullets(c, [
        ("CARETAKER", "is a NYCHA janitor, not a caregiver."),
        ("TEACHER- PER SESSION", "— 78,618 people, the largest title in the city "
                                 "— isn’t a job at all. It’s a pay code."),
        ("LIEUTENANT", "is two different jobs, NYPD or FDNY, mapping to two different "
                       "occupation codes."),
        ("And nothing connects.", "Payroll, exams, and occupations share no key. "
                                  "The join has to be rebuilt from text."),
    ], M, y, W - 2 * M - 0.4 * inch, 13.5)

    foot(c, "Sources: NYC Citywide Payroll k397-673e (FY2025) · DCAS Annual Examination "
            "Schedule 4ptz-hmtc · O*NET 30.3")
    c.showPage()


def slide_solution(c):
    page(c, "The solution")
    y = H - M - 0.8 * inch

    c.setFont(BOLD, 30)
    c.setFillColor(INK)
    c.drawString(M, y, "Answer it one task at a time. Never score the job.")
    y -= 0.55 * inch

    y = para(c, "A worker picks their real payroll title and sees the real tasks that job "
                "involves — published federal task statements, shown verbatim. Every "
                "statement gets one of three labels:",
             M, y, W - 2 * M - 0.6 * inch, REG, 14, 21, INK2)
    y -= 0.34 * inch

    x = chip(c, M, y, "AUTOMATABLE", AUTO, HexColor("#FDF3E9"))
    x = chip(c, x, y, "AUGMENTABLE", AUG, HexColor("#E9F5EF"))
    chip(c, x, y, "HUMAN ANCHORED", HUMAN, HexColor("#EAF1FD"))
    y -= 0.62 * inch

    bullets(c, [
        ("No overall risk score — on purpose.", "Holding method constant and changing "
         "only the unit of analysis moves US “high-risk” employment from 38% to 9% "
         "(Arntz et al. 2017). The scary number is an artifact of aggregation."),
        ("Two kinds of human, and they are opposites.", "A task can stay human because it "
         "needs a body present — which erodes as technology improves — or because "
         "the law vests the act in a person, which no model release changes. "
         "A technology roadmap and a policy roadmap. One score erases the difference."),
        ("It knows when to refuse.", "Ask it about CITY SEASONAL AIDE and it declines: "
         "a hiring category, 17 salaried rows out of 2,414. A gated eval fails the build "
         "if that refusal is ever replaced with a guess."),
        ("Then it gives them a move.", "Open DCAS exams for their title, plus their real "
         "promotional next rung — the actual civil-service mechanism for moving up."),
    ], M, y, W - 2 * M - 0.4 * inch, 13)
    c.showPage()


def slide_how(c):
    page(c, "How I built it")
    y = H - M - 0.8 * inch

    c.setFont(BOLD, 30)
    c.setFillColor(INK)
    c.drawString(M, y, "Evals before features. Agents for the judgment calls.")
    y -= 0.72 * inch

    bullets(c, [
        ("Wrote the gate first, and made it fail.", "A hard-fail eval re-derives every "
         "headcount, salary, exam, occupation code, and task statement from committed "
         "city snapshots. It exits non-zero on a forced match, an invented number, or any "
         "job-level aggregate. It existed before the demo did."),
        ("Agent 1 — title-matcher.", "Joins DCAS exam titles to payroll titles without "
         "forcing matches. Its own eval hard-fails a forced match, because the naive "
         "baseline produced 12 corrupt ones."),
        ("Agent 2 — crosswalk-decider.", "Maps a payroll title to an occupation code "
         "from repo evidence, golden-tested against 13 hand-decided titles. It returns "
         "BLOCKED rather than guessing, and it overruled my own assumptions twice."),
        ("A two-axis rubric, never averaged.", "Can a model produce this output? And can "
         "that output take effect without a named human accountable for it? The second is "
         "law and process, not capability — so it is a ceiling, not a factor."),
        ("Claude on the page, deterministic code underneath.", "Python does all the data "
         "work; Claude only explains it in plain language, grounded in the verified page "
         "— with a precomputed fallback so the demo never depends on the network."),
    ], M, y, W - 2 * M - 0.3 * inch, 12.5, gap=0.24 * inch)
    c.showPage()


def slide_forward(c):
    page(c, "What this gives New York")
    y = H - M - 0.8 * inch

    c.setFont(BOLD, 30)
    c.setFillColor(INK)
    c.drawString(M, y, "AI lifting workers, in the four ways the brief asked for.")
    y -= 0.7 * inch

    bullets(c, [
        ("Navigate what AI means for their jobs.", "Not a verdict — a task-level, "
         "title-specific answer for the frontline workers generic career tools ignore: "
         "traffic and school safety agents, EMTs, NYCHA caretakers, sergeants."),
        ("Find new opportunities.", "Civil service already has the ladder. The gap is "
         "that it is pull, not push: DCAS sends no notice when you become eligible, "
         "filing windows are three weeks, and exam-to-hire runs 14–15 months. "
         "Wiring the exam feed to a notification closes that."),
        ("Reskill and upskill where it actually pays.", "Target the augmentable tasks. "
         "The authority-anchored ones are a policy question, and no training changes them."),
        ("Augment the work people already do.", "The result is not the intuitive one: "
         "the “low-skill” titles are the least exposed in this dataset, and the "
         "office-shaped edges are the exposed part."),
        ("Next: validate with the people in the titles.", "Finish the remaining 23 "
         "crosswalk decisions, test the labels with DC 37 and Local 237 members, and "
         "pilot the eligibility notice with DCAS."),
    ], M, y, W - 2 * M - 0.3 * inch, 12.5, gap=0.22 * inch)

    foot(c, "This page includes information from the O*NET 30.3 Database by the U.S. Department of Labor, "
            "Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. "
            "O*NET® is a trademark of USDOL/ETA. TitleTrack has modified all or some of this "
            "information. USDOL/ETA has not approved, endorsed, or tested these modifications.")
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=(W, H))
    c.setTitle("TitleTrack — Claude Impact Lab")
    c.setAuthor("Ryan Michie")
    for fn in (slide_title, slide_problem, slide_solution, slide_how, slide_forward):
        fn(c)
    c.save()
    print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, 5 slides)")


if __name__ == "__main__":
    main()
