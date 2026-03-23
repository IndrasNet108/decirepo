#!/usr/bin/env bash
set -euo pipefail

TARGET_ROOT="${1:-}"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}

trap cleanup EXIT

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
  "conformance/v0_1"
  "conformance/SEMANTICS_KERNEL_V0_1.json"
  "conformance/DOMAIN_PROFILE_V0_1.json"
  "conformance/CASE_CLASS_MATRIX_V0_1.json"
  "conformance/GAP_CLASSIFICATION_V0_1.json"
  "conformance/BOUNDED_COMPLETENESS_STATUS_V0_1.json"
  "conformance/generated_corpus_v0_1/manifest.json"
  "conformance/domain_guided_generated_corpus_v0_1/manifest.json"
  "conformance/boundary_corpus_v0_1/manifest.json"
  "conformance/adversarial_corpus_v0_1/manifest.json"
  "conformance/precedence_adversarial_corpus_v0_1/manifest.json"
  "conformance/cc012_negative_verify_corpus_v0_1/manifest.json"
  "conformance/cc012_verify_distribution_v0_1.json"
  "conformance/malformed_corpus_v0_1/manifest.json"
)

normalize_for_sync() {
  local rel="$1"
  local src="$2"
  local dst="$3"

  if [ -d "$src" ]; then
    cp -R "$src" "$dst"
    return
  fi

  cp "$src" "$dst"

  if [ "$rel" = "DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2.md" ]; then
    # Allow public/spec sync across repos while keeping the internal bootstrap
    # note path out of the sanitized public repository.
    perl -0pi -e 's@Network bootstrap is operationally described separately in:\n\n- `DECIREPO_NETWORK_BOOTSTRAP_NOTE_V0_1\.md`@Network bootstrap is operationally described separately in operator documentation outside the public repository.@g' "$dst"
  fi
}

for rel in "${PATHS[@]}"; do
  local_path="$rel"
  mirror_path="$TARGET_ROOT/$rel"
  local_cmp="$TMP_DIR/local_${rel//\//__}"
  mirror_cmp="$TMP_DIR/mirror_${rel//\//__}"

  if [ ! -e "$local_path" ]; then
    echo "ERROR: missing local path: $local_path" >&2
    exit 1
  fi

  if [ ! -e "$mirror_path" ]; then
    echo "ERROR: missing mirror path: $mirror_path" >&2
    exit 1
  fi

  echo "Comparing $rel"
  normalize_for_sync "$rel" "$local_path" "$local_cmp"
  normalize_for_sync "$rel" "$mirror_path" "$mirror_cmp"

  if ! git diff --no-index --exit-code -- "$local_cmp" "$mirror_cmp" >/tmp/decirepo_protocol_sync.diff 2>&1; then
    echo "ERROR: protocol drift detected for $rel" >&2
    cat /tmp/decirepo_protocol_sync.diff >&2
    exit 1
  fi

done

echo "Protocol sync check passed."
