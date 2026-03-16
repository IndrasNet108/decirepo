#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLI="$ROOT_DIR/dlx-ref/cli.js"
ARTIFACT="$ROOT_DIR/genesis_artifact.json"
MODE="${1:-all}"

run_verify() {
  node "$CLI" verify "$ARTIFACT"
}

run_rebuild() {
  node "$CLI" rebuild "$ARTIFACT"
}

run_validate() {
  node "$CLI" validate "$ARTIFACT"
}

case "$MODE" in
  verify)
    run_verify
    ;;
  rebuild)
    run_rebuild
    ;;
  validate)
    run_validate
    ;;
  all)
    printf '# verify\n'
    run_verify
    printf '\n# rebuild\n'
    run_rebuild
    printf '\n# validate\n'
    run_validate
    ;;
  *)
    echo "Usage: bash scripts/run_genesis_verification.sh [verify|rebuild|validate|all]" >&2
    exit 1
    ;;
esac
