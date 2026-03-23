#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILE_DIR="${1:-$ROOT_DIR/conformance/v0_1}"
OUT_FILE="${2:-$ROOT_DIR/out/conformance/v0_1/CONFORMANCE_REPORT.json}"

mkdir -p "$(dirname "$OUT_FILE")"
node "$ROOT_DIR/scripts/run_protocol_conformance_v0_1.js" "$PROFILE_DIR" --out "$OUT_FILE"
echo "Wrote conformance report: $OUT_FILE"
