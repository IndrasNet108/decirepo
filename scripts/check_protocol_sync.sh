#!/usr/bin/env bash
set -euo pipefail

TARGET_ROOT="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -z "$TARGET_ROOT" ]; then
  echo "Usage: bash scripts/check_protocol_sync.sh <mirror-repo-root>" >&2
  exit 1
fi

if [ ! -d "$TARGET_ROOT" ]; then
  echo "ERROR: mirror repo root not found: $TARGET_ROOT" >&2
  exit 1
fi

TARGET_ROOT="$(cd "$TARGET_ROOT" && pwd)"

PATHS=(
  "DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2.md"
  "DECIREPO_PROTOCOL_CONFORMANCE_V0_1.md"
  "DECIREPO_SEMANTICS_KERNEL_V0_1.md"
  "conformance/SEMANTICS_KERNEL_V0_1.json"
  "conformance/DOMAIN_PROFILE_V0_1.json"
  "conformance/CASE_CLASS_MATRIX_V0_1.json"
  "conformance/GAP_CLASSIFICATION_V0_1.json"
  "conformance/BOUNDED_COMPLETENESS_STATUS_V0_1.json"
  "conformance/domain_guided_generated_corpus_v0_1"
  "conformance/boundary_corpus_v0_1"
  "conformance/adversarial_corpus_v0_1"
  "conformance/precedence_adversarial_corpus_v0_1"
  "conformance/cc012_negative_verify_corpus_v0_1"
  "conformance/cc012_verify_distribution_v0_1.json"
  "conformance/generated_corpus_v0_1"
  "conformance/malformed_corpus_v0_1"
  "conformance/v0_1"
)

emit_debug_context() {
  local missing_rel="$1"
  echo "DEBUG: repo_root=$REPO_ROOT" >&2
  echo "DEBUG: target_root=$TARGET_ROOT" >&2
  echo "DEBUG: pwd=$(pwd)" >&2
  git -C "$REPO_ROOT" rev-parse HEAD >&2 || true
  echo "DEBUG: tracked entry for $missing_rel" >&2
  git -C "$REPO_ROOT" ls-files -- "$missing_rel" >&2 || true
  echo "DEBUG: top-level repo root listing" >&2
  ls -la "$REPO_ROOT" >&2 || true
}

for rel in "${PATHS[@]}"; do
  local_path="$REPO_ROOT/$rel"
  mirror_path="$TARGET_ROOT/$rel"

  if [ ! -e "$local_path" ]; then
    echo "ERROR: missing local path: $local_path" >&2
    emit_debug_context "$rel"
    exit 1
  fi

  if [ ! -e "$mirror_path" ]; then
    echo "ERROR: missing mirror path: $mirror_path" >&2
    emit_debug_context "$rel"
    exit 1
  fi

  echo "Comparing $rel"
  if ! git diff --no-index --exit-code -- "$local_path" "$mirror_path" >/tmp/decirepo_protocol_sync.diff 2>&1; then
    echo "ERROR: protocol drift detected for $rel" >&2
    cat /tmp/decirepo_protocol_sync.diff >&2
    exit 1
  fi

done

echo "Protocol sync check passed."
