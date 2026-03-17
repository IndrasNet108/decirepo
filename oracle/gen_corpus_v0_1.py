#!/usr/bin/env python3
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
VECTORS_DIR = CONFORMANCE_DIR / "v0_1"
CORPUS_DIR = CONFORMANCE_DIR / "generated_corpus_v0_1"
ARTIFACTS_DIR = CORPUS_DIR / "artifacts"

DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"


def json_dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_vector_artifact(vector_id: str) -> Dict[str, Any]:
    return load_json_file(VECTORS_DIR / vector_id / "artifact.json")


def representative_artifact(class_id: str) -> Dict[str, Any]:
    artifact = load_vector_artifact("vector_001_genesis")

    if class_id == "CC014_MALFORMED_NON_OBJECT_ARTIFACT":
        return []
    if class_id == "CC001_VERIFY_BASELINE_PASS":
        return artifact
    if class_id == "CC002_VERIFY_SCHEMA_VERSION_INVALID":
        artifact["schema_version"] = "dlx-artifact-v9.9"
        return artifact
    if class_id == "CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH":
        artifact["rebuild_hash_expected"] = "0" * 64
        return artifact
    if class_id == "CC004_VERIFY_PASS_REQUIRES_MATCH":
        artifact["rebuild_result"] = "MISMATCH"
        return artifact
    if class_id == "CC005_VALIDATE_TRANSITION_CHAIN_INVALID":
        return load_vector_artifact("vector_005_transition_chain_invalid")
    if class_id == "CC006_REBUILD_REBUILD_SOURCE_INVALID":
        return load_vector_artifact("vector_006_rebuild_source_invalid")
    if class_id == "CC007_VERIFY_UNKNOWN_TOP_LEVEL_ENVELOPE_FIELD_TOLERATED":
        return load_vector_artifact("vector_007_unknown_envelope_field")
    if class_id == "CC008_VERIFY_REBUILD_SOURCE_ABSENT":
        artifact.pop("rebuild_source", None)
        return artifact
    if class_id == "CC009_VERIFY_ARTIFACT_HASH_INVALID":
        artifact["artifact_hash"] = "not-a-64-hex"
        return artifact
    if class_id == "CC010_VERIFY_VALIDATOR_RESULT_INVALID":
        artifact["validator_result"] = "UNKNOWN"
        return artifact
    if class_id == "CC011_VERIFY_REBUILD_RESULT_INVALID":
        artifact["validator_result"] = "FAIL"
        artifact["rebuild_result"] = "UNKNOWN"
        return artifact
    if class_id == "CC012_MULTI_REASON_PRECEDENCE":
        artifact["schema_version"] = "dlx-artifact-v9.9"
        artifact["rebuild_hash_expected"] = "0" * 64
        artifact["validator_result"] = "FAIL"
        artifact["rebuild_result"] = "MATCH"
        return artifact
    if class_id == "CC013_CONFORMANCE_ERROR_HARNESS_FAILURE":
        return artifact
    raise KeyError(f"no representative artifact for class_id={class_id}")


ENTRY_SPECS: List[Dict[str, Any]] = [
    {
        "entry_id": "GEN_CC014_MALFORMED_NON_OBJECT_ARTIFACT",
        "class_id": "CC014_MALFORMED_NON_OBJECT_ARTIFACT",
        "command": "verify",
        "matched_classes": ["CC014_MALFORMED_NON_OBJECT_ARTIFACT"],
        "selected_class": "CC014_MALFORMED_NON_OBJECT_ARTIFACT",
    },
    {
        "entry_id": "GEN_CC001_VERIFY_BASELINE_PASS",
        "class_id": "CC001_VERIFY_BASELINE_PASS",
        "command": "verify",
        "matched_classes": ["CC001_VERIFY_BASELINE_PASS"],
        "selected_class": "CC001_VERIFY_BASELINE_PASS",
    },
    {
        "entry_id": "GEN_CC002_VERIFY_SCHEMA_VERSION_INVALID",
        "class_id": "CC002_VERIFY_SCHEMA_VERSION_INVALID",
        "command": "verify",
        "matched_classes": ["CC002_VERIFY_SCHEMA_VERSION_INVALID"],
        "selected_class": "CC002_VERIFY_SCHEMA_VERSION_INVALID",
    },
    {
        "entry_id": "GEN_CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH",
        "class_id": "CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH",
        "command": "verify",
        "matched_classes": ["CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH"],
        "selected_class": "CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH",
    },
    {
        "entry_id": "GEN_CC004_VERIFY_PASS_REQUIRES_MATCH",
        "class_id": "CC004_VERIFY_PASS_REQUIRES_MATCH",
        "command": "verify",
        "matched_classes": ["CC004_VERIFY_PASS_REQUIRES_MATCH"],
        "selected_class": "CC004_VERIFY_PASS_REQUIRES_MATCH",
    },
    {
        "entry_id": "GEN_CC005_VALIDATE_TRANSITION_CHAIN_INVALID",
        "class_id": "CC005_VALIDATE_TRANSITION_CHAIN_INVALID",
        "command": "validate",
        "matched_classes": ["CC005_VALIDATE_TRANSITION_CHAIN_INVALID"],
        "selected_class": "CC005_VALIDATE_TRANSITION_CHAIN_INVALID",
    },
    {
        "entry_id": "GEN_CC006_REBUILD_REBUILD_SOURCE_INVALID",
        "class_id": "CC006_REBUILD_REBUILD_SOURCE_INVALID",
        "command": "rebuild",
        "matched_classes": ["CC006_REBUILD_REBUILD_SOURCE_INVALID"],
        "selected_class": "CC006_REBUILD_REBUILD_SOURCE_INVALID",
    },
    {
        "entry_id": "GEN_CC007_VERIFY_UNKNOWN_TOP_LEVEL_ENVELOPE_FIELD_TOLERATED",
        "class_id": "CC007_VERIFY_UNKNOWN_TOP_LEVEL_ENVELOPE_FIELD_TOLERATED",
        "command": "verify",
        "matched_classes": ["CC007_VERIFY_UNKNOWN_TOP_LEVEL_ENVELOPE_FIELD_TOLERATED"],
        "selected_class": "CC007_VERIFY_UNKNOWN_TOP_LEVEL_ENVELOPE_FIELD_TOLERATED",
    },
    {
        "entry_id": "GEN_CC008_VERIFY_REBUILD_SOURCE_ABSENT",
        "class_id": "CC008_VERIFY_REBUILD_SOURCE_ABSENT",
        "command": "verify",
        "matched_classes": ["CC008_VERIFY_REBUILD_SOURCE_ABSENT"],
        "selected_class": "CC008_VERIFY_REBUILD_SOURCE_ABSENT",
    },
    {
        "entry_id": "GEN_CC009_VERIFY_ARTIFACT_HASH_INVALID",
        "class_id": "CC009_VERIFY_ARTIFACT_HASH_INVALID",
        "command": "verify",
        "matched_classes": ["CC009_VERIFY_ARTIFACT_HASH_INVALID"],
        "selected_class": "CC009_VERIFY_ARTIFACT_HASH_INVALID",
    },
    {
        "entry_id": "GEN_CC010_VERIFY_VALIDATOR_RESULT_INVALID",
        "class_id": "CC010_VERIFY_VALIDATOR_RESULT_INVALID",
        "command": "verify",
        "matched_classes": ["CC010_VERIFY_VALIDATOR_RESULT_INVALID"],
        "selected_class": "CC010_VERIFY_VALIDATOR_RESULT_INVALID",
    },
    {
        "entry_id": "GEN_CC011_VERIFY_REBUILD_RESULT_INVALID",
        "class_id": "CC011_VERIFY_REBUILD_RESULT_INVALID",
        "command": "verify",
        "matched_classes": ["CC011_VERIFY_REBUILD_RESULT_INVALID"],
        "selected_class": "CC011_VERIFY_REBUILD_RESULT_INVALID",
    },
    {
        "entry_id": "GEN_CC012_MULTI_REASON_PRECEDENCE",
        "class_id": "CC012_MULTI_REASON_PRECEDENCE",
        "command": "verify",
        "matched_classes": [
            "CC002_VERIFY_SCHEMA_VERSION_INVALID",
            "CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH",
            "CC012_MULTI_REASON_PRECEDENCE",
        ],
        "selected_class": "CC012_MULTI_REASON_PRECEDENCE",
    },
    {
        "entry_id": "GEN_CC013_CONFORMANCE_ERROR_HARNESS_FAILURE",
        "class_id": "CC013_CONFORMANCE_ERROR_HARNESS_FAILURE",
        "command": "verify_unsupported",
        "matched_classes": ["CC013_CONFORMANCE_ERROR_HARNESS_FAILURE"],
        "selected_class": "CC013_CONFORMANCE_ERROR_HARNESS_FAILURE",
    },
]


def build_entries(kernel: Dict[str, Any], domain: Dict[str, Any], matrix: Dict[str, Any]) -> List[Dict[str, Any]]:
    classes = {cls["class_id"]: cls for cls in matrix["classes"]}
    entries: List[Dict[str, Any]] = []

    for spec in ENTRY_SPECS:
        class_def = classes[spec["class_id"]]
        artifact = representative_artifact(spec["class_id"])
        artifact_path = ARTIFACTS_DIR / f"{spec['entry_id']}.json"
        json_dump(artifact_path, artifact)

        in_domain = class_def["class_bucket"] in {"in_domain_valid", "in_domain_invalid", "in_domain_gap"}
        oracle_expectation = {
            "artifact_id_required": in_domain,
            "normalized_result_required": in_domain,
            "canonical_result_hex_required": in_domain,
        }

        entries.append(
            {
                "entry_id": spec["entry_id"],
                "source_class_id": spec["class_id"],
                "source_bucket": class_def["class_bucket"],
                "command": spec["command"],
                "generation_kind": "representative",
                "artifact_path": str(artifact_path.relative_to(ROOT)),
                "expected": {
                    "in_domain": in_domain,
                    "matched_classes": spec["matched_classes"],
                    "selected_class": spec["selected_class"],
                    "partition_mode": class_def["partition_mode"],
                    "expected_verdict": class_def["expected_verdict"],
                    "expected_reason_codes": deepcopy(class_def.get("expected_reason_codes") or []),
                },
                "trace_expectation": {
                    "bucket_assignment": class_def["class_bucket"],
                    "predicate_ref": class_def["predicate_ref"],
                    "precedence_rank": class_def["precedence_rank"],
                },
                "oracle_expectation": oracle_expectation,
            }
        )

    return entries


def build_manifest(entries: List[Dict[str, Any]], matrix: Dict[str, Any]) -> Dict[str, Any]:
    in_domain_total = sum(1 for entry in entries if entry["expected"]["in_domain"])
    out_of_domain_total = len(entries) - in_domain_total
    precedence_total = sum(1 for entry in entries if entry["expected"]["partition_mode"] == "ordered_precedence_chain")
    return {
        "manifest_version": "0.1",
        "profile_id": "V0_1",
        "corpus_id": "generated_corpus_v0_1",
        "provenance_mode": "class_guided",
        "generator": {
            "name": "gen_corpus_v0_1.py",
            "version": "0.1.0",
        },
        "inputs": {
            "domain_profile": "conformance/DOMAIN_PROFILE_V0_1.json",
            "semantics_kernel": "conformance/SEMANTICS_KERNEL_V0_1.json",
            "case_class_matrix": "conformance/CASE_CLASS_MATRIX_V0_1.json",
        },
        "generation_policy": {
            "mode": "deterministic",
            "seed_policy": "fixed",
            "seed": "V0_1",
            "emit_only_in_domain": False,
            "include_boundary_cases": False,
            "include_adversarial_cases": False,
        },
        "classification_contract": {
            "classification_pipeline": [
                "bucket_assignment",
                "predicate_resolution",
                "class_selection",
                "verdict_derivation",
                "reason_code_normalization",
                "normalized_result_construction",
            ],
            "partition_expectation": "every_generated_input_must_resolve_to_exactly_one_class_or_declared_precedence_chain",
            "ambiguity_policy": "allowed_only_if_partition_mode_is_ordered_precedence_chain",
            "reason_code_ordering": "fixed_total_order",
        },
        "coverage_summary": {
            "declared_classes_total": len(matrix["classes"]),
            "declared_classes_covered": len({entry["source_class_id"] for entry in entries}),
            "generated_inputs_total": len(entries),
            "generated_inputs_in_domain": in_domain_total,
            "generated_inputs_out_of_domain": out_of_domain_total,
            "generated_inputs_ambiguous": 0,
            "generated_inputs_with_declared_precedence_chain": precedence_total,
            "generated_inputs_unclassified": 0,
        },
        "entries": entries,
    }


def main() -> None:
    kernel = load_json_file(KERNEL_PATH)
    domain = load_json_file(DOMAIN_PATH)
    matrix = load_json_file(MATRIX_PATH)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    entries = build_entries(kernel, domain, matrix)

    # Fail fast if the explicit manifest table and the current oracle drift.
    for entry in entries:
        artifact = load_json_file(ROOT / entry["artifact_path"])
        evaluated = evaluate_corpus_entry(entry["command"], artifact, kernel, domain, matrix)
        if evaluated["matched_classes"] != entry["expected"]["matched_classes"]:
            raise SystemExit(f"matched_classes drift for {entry['entry_id']}: {evaluated['matched_classes']} != {entry['expected']['matched_classes']}")
        if evaluated["selected_class"] != entry["expected"]["selected_class"]:
            raise SystemExit(f"selected_class drift for {entry['entry_id']}: {evaluated['selected_class']} != {entry['expected']['selected_class']}")
        if evaluated["partition_mode"] != entry["expected"]["partition_mode"]:
            raise SystemExit(f"partition_mode drift for {entry['entry_id']}: {evaluated['partition_mode']} != {entry['expected']['partition_mode']}")
        if evaluated["verdict"] != entry["expected"]["expected_verdict"]:
            raise SystemExit(f"verdict drift for {entry['entry_id']}: {evaluated['verdict']} != {entry['expected']['expected_verdict']}")
        if evaluated["reason_codes"] != entry["expected"]["expected_reason_codes"]:
            raise SystemExit(f"reason_codes drift for {entry['entry_id']}: {evaluated['reason_codes']} != {entry['expected']['expected_reason_codes']}")

    manifest = build_manifest(entries, matrix)
    json_dump(CORPUS_DIR / "manifest.json", manifest)


if __name__ == "__main__":
    main()
