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

    c.setFont(BOLD, 32)
    c.setFillColor(INK)
    c.drawString(M, y, "I built the test first, then let it fail.")
    y -= 0.82 * inch

    bullets(c, [
        ("Wrote the test before the app.", "It rebuilds every number on the page from "
         "the city's own files. If anything doesn't match, the build fails."),
        ("Agent 1 — title-matcher.", "Matches exam names to payroll names. It is not "
         "allowed to force a match. Guessing produced 12 wrong ones."),
        ("Agent 2 — crosswalk-decider.", "Picks the job code for a title using evidence "
         "in the files. It says BLOCKED instead of guessing. It corrected me twice."),
        ("Two questions, never mixed.", "Can AI do this task? And is a person legally "
         "required to be the one who does it? The second is about law, not technology."),
        ("Claude explains; code does the math.", "Python handles the data. Claude only "
         "puts it in plain English — with a saved answer ready if the internet drops."),
    ], M, y, W - 2 * M - 0.3 * inch, 15.5, gap=0.30 * inch)
    c.showPage()


def slide_forward(c):
    page(c, "What this gives New York")
    y = H - M - 0.8 * inch

    c.setFont(BOLD, 32)
    c.setFillColor(INK)
    c.drawString(M, y, "Helping AI lift workers, not leave them behind.")
    y -= 0.82 * inch

    bullets(c, [
        ("Workers can see what AI means for their job.", "Task by task, for their real "
         "title — traffic agents, school safety agents, EMTs, caretakers."),
        ("They get a real next step.", "The city already has a promotion ladder. But "
         "nobody tells you when your exam opens, and the window is only three weeks."),
        ("Training goes where it pays off.", "Learn the tasks AI will help with. Skip "
         "the ones the law says only a person can do."),
        ("The results surprise people.", "The so-called low-skill jobs are the least "
         "exposed. A school secretary is more exposed than a NYCHA caretaker."),
        ("Next: ask the workers if we got it right.", "Test the labels with union "
         "members, and pilot exam alerts with the city."),
    ], M, y, W - 2 * M - 0.3 * inch, 15.5, gap=0.30 * inch)

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
