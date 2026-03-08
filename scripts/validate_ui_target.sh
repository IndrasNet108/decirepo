#!/bin/bash
set -euo pipefail

echo "Checking syntax of assets/data.js..."
node --check assets/data.js

echo "Running full validation..."
bash scripts/validate_all.sh

echo "UI TARGET VALIDATION PASSED"
