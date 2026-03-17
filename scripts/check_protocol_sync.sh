#!/usr/bin/env bash
set -euo pipefail

TARGET_ROOT="${1:-}"

if [ -z "$TARGET_ROOT" ]; then
  echo "Usage: bash scripts/check_protocol_sync.sh <mirror-repo-root>" >&2
  exit 1
fi

if [ ! -d "$TARGET_ROOT" ]; then
  echo "ERROR: mirror repo root not found: $TARGET_ROOT" >&2
  exit 1
fi

PATHS=(
  "DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2.md"
  "DECIREPO_PROTOCOL_CONFORMANCE_V0_1.md"
  "DECIREPO_SEMANTICS_KERNEL_V0_1.md"
  "conformance/SEMANTICS_KERNEL_V0_1.json"
  "conformance/DOMAIN_PROFILE_V0_1.json"
  "conformance/CASE_CLASS_MATRIX_V0_1.json"
  "conformance/GAP_CLASSIFICATION_V0_1.json"
  "conformance/boundary_corpus_v0_1"
  "conformance/adversarial_corpus_v0_1"
  "conformance/generated_corpus_v0_1"
  "conformance/v0_1"
)

for rel in "${PATHS[@]}"; do
  local_path="$rel"
  mirror_path="$TARGET_ROOT/$rel"

  if [ ! -e "$local_path" ]; then
    echo "ERROR: missing local path: $local_path" >&2
    exit 1
  fi

  if [ ! -e "$mirror_path" ]; then
    echo "ERROR: missing mirror path: $mirror_path" >&2
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
