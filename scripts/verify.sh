#!/bin/sh
# TitleTrack gate runner. One source of truth for CI and the local Stop hook.
#
# Exits 0 only if every gate lands on its EXPECTED verdict. Three of the four
# agent baselines MUST exit non-zero: an adversarial baseline that starts
# passing means the golden set lost its teeth, which is a regression, not a win.
set -u

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd) || exit 1
cd "$ROOT" || exit 1
PY=${PYTHON:-python3}
command -v "$PY" >/dev/null 2>&1 || PY=python
TMP=$(mktemp -d) || exit 1
trap 'rm -rf "$TMP"' EXIT INT TERM
FAILED=0

expect() { # expect <want-exit> <label> <cmd...>
  want=$1; label=$2; shift 2
  "$@" >"$TMP/out" 2>&1; got=$?
  if [ "$got" -eq "$want" ]; then
    printf 'PASS  %-46s exit %s\n' "$label" "$got"
  else
    printf 'FAIL  %-46s exit %s (expected %s)\n' "$label" "$got" "$want"
    sed 's/^/      | /' "$TMP/out"
    FAILED=$((FAILED + 1))
  fi
}

echo "== data gates (both must pass) =="
expect 0 "build_top40.py --check" "$PY" scripts/build_top40.py --check
expect 0 "demo/evaluate.py" "$PY" demo/evaluate.py

echo
echo "== generate baseline predictions =="
gen() { # gen <agent> <mode>
  if ! "$PY" "agents/$1/baselines.py" "$2" >"$TMP/$1.$2.jsonl" 2>"$TMP/err"; then
    printf 'FAIL  baselines.py %s %s did not run\n' "$1" "$2"
    sed 's/^/      | /' "$TMP/err"; FAILED=$((FAILED + 1)); return
  fi
  if [ ! -s "$TMP/$1.$2.jsonl" ]; then
    printf 'FAIL  baselines.py %s %s produced nothing\n' "$1" "$2"
    FAILED=$((FAILED + 1)); return
  fi
  printf 'PASS  %-46s %s lines\n' "baselines.py $1 $2" \
    "$(wc -l <"$TMP/$1.$2.jsonl" | tr -d ' ')"
}
gen title-matcher     naive
gen title-matcher     strict
gen crosswalk-decider first_soc
gen crosswalk-decider always_skip

echo
echo "== mode names are actually honoured =="
# An unrecognised mode SILENTLY falls through to the default instead of erroring,
# and the mode names differ per agent. Identical output therefore means a mode
# name was ignored, not that two baselines agree.
distinct() {
  if cmp -s "$TMP/$1.$2.jsonl" "$TMP/$1.$3.jsonl"; then
    printf 'FAIL  %s: %s and %s byte-identical (mode name ignored?)\n' "$1" "$2" "$3"
    FAILED=$((FAILED + 1))
  else
    printf 'PASS  %-46s\n' "$1: $2 differs from $3"
  fi
}
distinct title-matcher     naive     strict
distinct crosswalk-decider first_soc always_skip

echo
echo "== agent evals: 1 must PASS, 3 must FAIL =="
expect 1 "title-matcher naive           MUST FAIL" \
  "$PY" agents/title-matcher/evaluate.py     --predictions "$TMP/title-matcher.naive.jsonl"
expect 0 "title-matcher strict          MUST PASS" \
  "$PY" agents/title-matcher/evaluate.py     --predictions "$TMP/title-matcher.strict.jsonl"
expect 1 "crosswalk-decider first_soc   MUST FAIL" \
  "$PY" agents/crosswalk-decider/evaluate.py --predictions "$TMP/crosswalk-decider.first_soc.jsonl"
expect 1 "crosswalk-decider always_skip MUST FAIL" \
  "$PY" agents/crosswalk-decider/evaluate.py --predictions "$TMP/crosswalk-decider.always_skip.jsonl"

echo
echo "== evidence files survived checkout verbatim =="
bom=$(head -c 3 data/raw/top40_titles.json | od -An -tx1 | tr -d ' \n')
if [ "$bom" = "efbbbf" ]; then
  printf 'PASS  top40_titles.json keeps its UTF-8 BOM\n'
else
  printf 'FAIL  top40_titles.json BOM is %s, expected efbbbf\n' "$bom"
  FAILED=$((FAILED + 1))
fi
if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
  case "$(git check-attr text -- data/raw/top40_titles.json)" in
    *"text: unset") printf 'PASS  data/raw/** is still -text\n' ;;
    *) printf 'FAIL  data/raw/** lost its -text attribute\n'; FAILED=$((FAILED + 1)) ;;
  esac
fi

echo
if [ "$FAILED" -ne 0 ]; then
  echo "VERIFY FAILED -- $FAILED gate(s) off their expected verdict"
  exit 1
fi
echo "VERIFY PASSED -- 2 data gates, 4 baselines, 4 evals, 2 evidence checks"
