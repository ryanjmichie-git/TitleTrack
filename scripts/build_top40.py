#!/usr/bin/env python3
"""Builds data/raw/top40_titles.json from files already in data/raw/.

Fully offline - no network calls. Re-run after refreshing data/raw/.

Python port of build_top40.ps1, which assumed Windows. This runs anywhere and
reproduces the PowerShell output BYTE FOR BYTE, so a rebuild on Linux does not
churn the committed artifact. That is also the port's test:

    python3 scripts/build_top40.py --check

writes nothing and diffs against the committed file.

Byte-equality means matching three Windows PowerShell 5.1 quirks that have
nothing to do with the data - see ps_json() below.
"""

import argparse
import csv
import datetime as dt
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
AS_OF = dt.datetime(2026, 8, 7)

# --- Employers that run civil-service exams but do NOT appear in the citywide
# --- payroll file (k397-673e). Derived from k397_agencies_2025.json: no agency
# --- matching HOSPITAL / H+H / TRANSIT exists in FY2025 payroll.
# --- NOTE: HOUSING AUTHORITY *is* present (NYC HOUSING AUTHORITY, 14,297 rows),
# --- so it is deliberately NOT in this list.
FOREIGN_EMPLOYER = ("NYC H+H", "H+H", "HOSPITALS", "TRANSIT AUTHORITY")

# open_competitive_promotion conflates ELIGIBILITY with STATUS. Map only the
# eligibility values; statuses (Canceled/Postponed) yield a null eligibility.
ELIGIBILITY = {
    "OPEN COMPETITIVE": "Open Competitive",
    "PROMOTION": "Promotion",
    "QIE": "Qualified Incumbent Exam",
    "QUALIFIED INCUMBENT EXAM": "Qualified Incumbent Exam",
}

_PARENS = re.compile(r"\([^)]*\)")
_WS = re.compile(r"\s+")


def norm(s):
    """Uppercase + strip parentheticals. Mirrors Norm() in the .ps1 exactly,
    including the operation order: parens, then whitespace, then case, then trim."""
    if not s:
        return ""
    return _WS.sub(" ", _PARENS.sub("", s)).upper().strip()


def median(values):
    """None for an empty set - a null median is a fact, not missing data."""
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[(n - 1) // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2


# ---------------------------------------------------------------------------
# PowerShell 5.1 ConvertTo-Json emulation
# ---------------------------------------------------------------------------
# Three quirks, none of them standard JSON style:
#   1. Indentation is COLUMN-ALIGNED, not fixed-depth. A nested value's children
#      are indented to (column where the value's bracket sits) + 4, and its
#      closing bracket sits at that column. So depth alone does not tell you the
#      indent - the length of the parent key does.
#   2. Two spaces after every colon.
#   3. The underlying JavaScriptSerializer escapes ' < > & as \uXXXX.
# An empty collection renders as "[\n\n<indent>]" - which falls out of the same
# rule, since joining zero elements leaves the two newlines adjacent.

_ESCAPES = {
    '"': '\\"',
    "\\": "\\\\",
    "\b": "\\b",
    "\f": "\\f",
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
    "'": "\\u0027",
    "<": "\\u003c",
    ">": "\\u003e",
    "&": "\\u0026",
}


def _ps_str(s):
    out = ['"']
    for ch in s:
        esc = _ESCAPES.get(ch)
        if esc is not None:
            out.append(esc)
        elif ch < " ":
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def ps_json(value, col=0):
    """Render `value` as PowerShell 5.1 would, with its first character at
    column `col`."""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return _ps_str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, dict):
        pad = " " * (col + 4)
        parts = []
        for k, v in value.items():
            key = _ps_str(k)
            parts.append(pad + key + ":  " + ps_json(v, col + 4 + len(key) + 3))
        return "{\n" + ",\n".join(parts) + "\n" + " " * col + "}"
    if isinstance(value, list):
        pad = " " * (col + 4)
        parts = [pad + ps_json(v, col + 4) for v in value]
        return "[\n" + ",\n".join(parts) + "\n" + " " * col + "]"
    raise TypeError("unserializable: %r" % (value,))


# ---------------------------------------------------------------------------


def read_json(name):
    """data/raw snapshots carry a UTF-8 BOM; utf-8-sig or every key breaks."""
    with open(os.path.join(RAW, name), encoding="utf-8-sig") as fh:
        return json.load(fh)


def parse_dt(s):
    """Socrata timestamps look like 2019-06-27T00:00:00.000."""
    if not s:
        return None
    return dt.datetime.fromisoformat(s)


def build():
    # ---- 1. top 40 titles by FY2025 headcount (all pay bases) ----
    top = read_json("k397_top40_headcount_2025.json")

    # ---- 2. per Annum salaries, bucketed by title ----
    by_title = {}
    chunks = sorted(glob.glob(os.path.join(RAW, "k397_perannum_2025_chunk*.csv")))
    if not chunks:
        sys.exit("no k397_perannum_2025_chunk*.csv in %s" % RAW)
    for path in chunks:
        with open(path, encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                title = row.get("title_description")
                if not title:
                    continue
                by_title.setdefault(title, []).append(float(row["base_salary"]))

    # ---- 3. exams, normalized and indexed by normalized title ----
    exam_idx = {}
    for e in read_json("4ptz-hmtc_full.json"):
        # Nulls are omitted from Socrata JSON entirely - .get(), never [].
        if not e.get("exam_title"):
            continue
        exam_idx.setdefault(norm(e["exam_title"]), []).append(e)

    def open_exams(title_desc):
        result = []
        for e in exam_idx.get(norm(title_desc), []):
            raw_val = e.get("open_competitive_promotion")
            up = raw_val.upper().strip() if raw_val else ""
            if up == "CANCELED":  # cancelled exams are not open
                continue

            start = parse_dt(e.get("application_period_start"))
            end = parse_dt(e.get("application_period_end_date"))
            # "open" = window still open, or window entirely in the future
            is_open = (end is not None and end >= AS_OF) or (
                end is None and start is not None and start > AS_OF
            )
            if not is_open:
                continue

            up_title = e["exam_title"].upper()
            same = not any("(%s)" % m in up_title for m in FOREIGN_EMPLOYER)

            result.append(
                {
                    "exam_number": e.get("exam_number"),
                    "exam_title": e["exam_title"],
                    "application_period_start": start.strftime("%Y-%m-%d") if start else None,
                    "application_period_end": end.strftime("%Y-%m-%d") if end else None,
                    "eligibility": ELIGIBILITY.get(up),
                    "eligibility_source_value": raw_val,
                    "same_employer": same,
                }
            )
        return result

    # ---- 4. assemble ----
    titles = []
    for rank, t in enumerate(top, start=1):
        name = t["title_description"]
        head = int(t["count_1"])  # every Socrata value is a quoted string
        vals = by_title.get(name, [])
        med = median(vals)
        titles.append(
            {
                "rank": rank,
                "title_description": name,
                "headcount_fy2025": head,
                "salary": {
                    "basis": "per Annum",
                    "median": None if med is None else int(round(med)),
                    "n_included": len(vals),
                    "n_excluded": head - len(vals),
                },
                "open_exams": open_exams(name),
            }
        )

    return {
        "generated_as_of": AS_OF.strftime("%Y-%m-%d"),
        "sources": {
            "payroll": {
                "dataset": "k397-673e",
                "name": "Citywide Payroll Data (Fiscal Year)",
                "attribution": "Office of Payroll Administration (OPA)",
                "fiscal_year": 2025,
                "rows_updated_at": "2026-04-16",
            },
            "exams": {
                "dataset": "4ptz-hmtc",
                "name": "Annual Examination Schedule of Each Fiscal Year",
                "attribution": "Department of Citywide Administrative Services (DCAS)",
                "rows_updated_at": "2026-07-22",
            },
        },
        "definitions": {
            "headcount_fy2025": "FY2025 payroll rows for this title_description, ALL pay bases. One row = one person-year per agency; a person in two agencies appears twice.",
            "salary_median": "Median base_salary over FY2025 rows with pay_basis='per Annum' and non-null base_salary. per Day / per Hour / Prorated Annual rows are EXCLUDED, not converted - base_salary means a different unit in each basis and the per Hour column is known to contain misfiled annual figures (FY2025 max 190941.71).",
            "n_included": "per Annum rows contributing to the median.",
            "n_excluded": "headcount_fy2025 minus n_included: rows dropped for non-annual pay basis or null base_salary.",
            "open_exams": "Exams from 4ptz-hmtc whose title matches this payroll title after uppercasing and stripping parentheticals, that are not Canceled, and whose application window is still open or entirely in the future as of generated_as_of.",
            "eligibility": "Normalized from open_competitive_promotion. That column conflates eligibility with schedule status, so rows carrying only a status (Postponed) yield null. Raw value kept in eligibility_source_value.",
            "same_employer": "False when the exam is for an employer absent from the citywide payroll file (NYC H+H, Hospitals, Transit Authority) - those hires can never appear in k397-673e. Verified against FY2025 agency_name list; NYC Housing Authority IS in payroll and is therefore true.",
        },
        # NOTE: the CUNY caveat below is SUPERSEDED and knowingly left as-is.
        # CUNY community colleges ARE in the payroll file (19,863 FY2025 rows)
        # under COMMUNITY COLLEGE (...) agency names; only the senior colleges are
        # absent. The "217 rows" check keyed on the string CUNY and missed them.
        # Correcting the text here means correcting it in build_top40.ps1 too and
        # regenerating, which resets the byte-identity baseline --check compares
        # against. Do both together or neither. See CLAUDE.md known gaps.
        "caveats": [
            "A null salary.median means the title has zero per Annum rows - it is paid per Day, per Hour, or per Session. It is not missing data.",
            "Title matching is text-based: 4ptz-hmtc title_code is populated on only 367 of 2901 rows (12.7%), so it is unusable as a join key.",
            "CUNY exams are marked same_employer=true because CUNY CENTRAL OFFICE appears in payroll, but only 217 FY2025 rows do - CUNY college staff are largely absent. Treat CUNY matches as low confidence.",
            "work_location_borough is the agency location, not the employee location.",
        ],
        "titles": titles,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--check",
        action="store_true",
        help="compare against the existing file instead of writing it",
    )
    ap.add_argument("--out", default=os.path.join(RAW, "top40_titles.json"))
    args = ap.parse_args()

    # utf-8-sig + CRLF: Out-File -Encoding utf8 on Windows PowerShell 5.1 emits a
    # BOM and CRLF, and .gitattributes pins data/raw/** as -text, so anything
    # else would rewrite the committed artifact.
    payload = (ps_json(build()) + "\n").encode("utf-8").replace(b"\n", b"\r\n")
    payload = b"\xef\xbb\xbf" + payload

    if args.check:
        with open(args.out, "rb") as fh:
            existing = fh.read()
        if existing == payload:
            print("OK  byte-identical to %s (%d bytes)" % (args.out, len(payload)))
            return 0
        print(
            "DIFF  rebuilt %d bytes vs %d on disk" % (len(payload), len(existing)),
            file=sys.stderr,
        )
        return 1

    with open(args.out, "wb") as fh:
        fh.write(payload)
    print("WROTE %s (%d bytes)" % (args.out, len(payload)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
