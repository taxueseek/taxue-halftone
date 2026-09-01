#!/usr/bin/env bash
# Full test suite for taxue-halftone. Exits non-zero on any failure.
set -euo pipefail

cd "$(dirname "$0")/.."
echo "== taxue-halftone test suite =="
pass=0

echo ""
echo "[1/3] design-system structure"
if python3 scripts/validate_design_system.py; then
  pass=$((pass+1)); echo "  OK"
else
  echo "  FAIL"; exit 1
fi

echo ""
echo "[2/3] styles six-axes completeness"
if python3 scripts/validate_styles.py; then
  pass=$((pass+1)); echo "  OK"
else
  echo "  FAIL"; exit 1
fi

echo ""
echo "[3/3] evals assertions"
if python3 scripts/validate_evals.py; then
  pass=$((pass+1)); echo "  OK"
else
  echo "  FAIL"; exit 1
fi

echo ""
echo "== all $pass/3 suites passed =="
