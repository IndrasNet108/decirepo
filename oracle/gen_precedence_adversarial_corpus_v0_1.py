#!/usr/bin/env python3
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

from corpus_cases_v0_1 import (
    genesis_artifact,
    scalar_transition_chain_artifact,
)
from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
CORPUS_DIR = CONFORMANCE_DIR / "precedence_adversarial_corpus_v0_1"
ARTIFACTS_DIR = CORPUS_DIR / "artifacts"

DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"


def json_dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reorder_artifact(
    artifact: Dict[str, Any],
    top_level_order: List[str],
    rebuild_source_order: List[str] | None = None,
) -> Dict[str, Any]:
    ordered: Dict[str, Any] = {}
    rebuild_source_order = rebuild_source_order or []

    for key in top_level_order:
        if key not in artifact:
            continue
        value = deepcopy(artifact[key])
        if key == "rebuild_source" and isinstance(value, dict):
            nested: Dict[str, Any] = {}
            for nested_key in rebuild_source_order:
                if nested_key in value:
                    nested[nested_key] = deepcopy(value[nested_key])
            for nested_key, nested_value in value.items():
                if nested_key not in nested:
                    nested[nested_key] = deepcopy(nested_value)
            value = nested
        ordered[key] = value

    for key, value in artifact.items():
        if key not in ordered:
            ordered[key] = deepcopy(value)
    return ordered


def pair_schema_hash_mismatch_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    artifact["rebuild_hash_expected"] = "0" * 64
    return artifact


def pair_schema_hash_mismatch_layout_variant() -> Dict[str, Any]:
    artifact = pair_schema_hash_mismatch_artifact()
    return reorder_artifact(
        artifact,
        [
            "rebuild_hash_expected",
            "validator_result",
            "rebuild_result",
            "rebuild_source",
            "schema_version",
            "decision_id",
            "publisher",
            "policy_version",
        ],
        rebuild_source_order=["specification_version", "target", "source"],
    )


def pair_artifact_hash_and_validator_invalid_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["artifact_hash"] = "not-a-64-hex"
    artifact["validator_result"] = "UNKNOWN"
    return artifact


def pair_rebuild_hash_and_pass_requires_match_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["rebuild_hash_expected"] = "0" * 64
    artifact["rebuild_result"] = "MISMATCH"
    return artifact


def pair_schema_and_pass_requires_match_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    artifact["rebuild_result"] = "MISMATCH"
    return artifact


def triple_schema_hash_pass_requires_match_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    artifact["rebuild_hash_expected"] = "0" * 64
    artifact["rebuild_result"] = "MISMATCH"
    return artifact


def triple_artifact_validator_rebuild_invalid_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["artifact_hash"] = "not-a-64-hex"
    artifact["validator_result"] = "UNKNOWN"
    artifact["rebuild_result"] = "UNKNOWN"
    return artifact


def triple_artifact_validator_rebuild_invalid_layout_variant() -> Dict[str, Any]:
    artifact = triple_artifact_validator_rebuild_invalid_artifact()
    return reorder_artifact(
        artifact,
        [
            "rebuild_result",
            "artifact_hash",
            "rebuild_source",
            "validator_result",
            "schema_version",
            "decision_id",
            "publisher",
            "policy_version",
        ],
        rebuild_source_order=["target", "source", "specification_version"],
    )


def triple_schema_artifact_validator_invalid_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    artifact["artifact_hash"] = "not-a-64-hex"
    artifact["validator_result"] = "UNKNOWN"
    return artifact


def validate_multi_path_transition_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["transition_chain"] = [
        {"from": "DRAFT", "to": "BROKEN"},
        {"from": "WRONG", "to": "PUBLISHED"},
    ]
    return artifact


def harness_contamination_probe_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    artifact["rebuild_hash_expected"] = "0" * 64
    artifact["rebuild_result"] = "MISMATCH"
    artifact["artifact_hash"] = "not-a-64-hex"
    return artifact


CASE_SPECS: List[Dict[str, Any]] = [
    {
        "case_id": "cc012_pair_schema_hash_layout_a",
        "command": "verify",
        "artifact_factory": pair_schema_hash_mismatch_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": [
            "CC002_VERIFY_SCHEMA_VERSION_INVALID",
            "CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH",
            "CC012_MULTI_REASON_PRECEDENCE",
        ],
        "expected_reason_codes": ["REBUILD_HASH_EXPECTED_MISMATCH", "SCHEMA_VERSION_INVALID"],
        "expected_triggered_rule_ids": [
            "RULE_REBUILD_HASH_EXPECTED_MATCHES_ARTIFACT_ID",
            "RULE_SCHEMA_VERSION_EQUALS_DLX_ARTIFACT_V0_1",
        ],
        "semantic_equivalence_group": "schema_hash_pair",
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_pair_schema_hash_layout_b",
        "command": "verify",
        "artifact_factory": pair_schema_hash_mismatch_layout_variant,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": [
            "CC002_VERIFY_SCHEMA_VERSION_INVALID",
            "CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH",
            "CC012_MULTI_REASON_PRECEDENCE",
        ],
        "expected_reason_codes": ["REBUILD_HASH_EXPECTED_MISMATCH", "SCHEMA_VERSION_INVALID"],
        "expected_triggered_rule_ids": [
            "RULE_REBUILD_HASH_EXPECTED_MATCHES_ARTIFACT_ID",
            "RULE_SCHEMA_VERSION_EQUALS_DLX_ARTIFACT_V0_1",
        ],
        "semantic_equivalence_group": "schema_hash_pair",
        "layout_variant_of": "cc012_pair_schema_hash_layout_a",
        "must_match_selected_class_with": "cc012_pair_schema_hash_layout_a",
        "must_match_canonical_result_with": "cc012_pair_schema_hash_layout_a",
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_pair_artifact_hash_validator",
        "command": "verify",
        "artifact_factory": pair_artifact_hash_and_validator_invalid_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": [
            "CC009_VERIFY_ARTIFACT_HASH_INVALID",
            "CC010_VERIFY_VALIDATOR_RESULT_INVALID",
            "CC012_MULTI_REASON_PRECEDENCE",
        ],
        "expected_reason_codes": ["ARTIFACT_HASH_INVALID", "VALIDATOR_RESULT_INVALID"],
        "expected_triggered_rule_ids": [
            "RULE_ARTIFACT_HASH_64_HEX",
            "RULE_VALIDATOR_RESULT_ENUM",
        ],
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_pair_hash_mismatch_pass_requires_match",
        "command": "verify",
        "artifact_factory": pair_rebuild_hash_and_pass_requires_match_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": [
            "CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH",
            "CC012_MULTI_REASON_PRECEDENCE",
        ],
        "expected_reason_codes": ["PASS_REQUIRES_MATCH", "REBUILD_HASH_EXPECTED_MISMATCH"],
        "expected_triggered_rule_ids": [
            "RULE_PASS_REQUIRES_MATCH_REBUILD_RESULT",
            "RULE_REBUILD_HASH_EXPECTED_MATCHES_ARTIFACT_ID",
        ],
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_pair_schema_pass_requires_match",
        "command": "verify",
        "artifact_factory": pair_schema_and_pass_requires_match_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": [
            "CC002_VERIFY_SCHEMA_VERSION_INVALID",
            "CC012_MULTI_REASON_PRECEDENCE",
        ],
        "expected_reason_codes": ["PASS_REQUIRES_MATCH", "SCHEMA_VERSION_INVALID"],
        "expected_triggered_rule_ids": [
            "RULE_PASS_REQUIRES_MATCH_REBUILD_RESULT",
            "RULE_SCHEMA_VERSION_EQUALS_DLX_ARTIFACT_V0_1",
        ],
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_triple_schema_hash_pass_requires_match",
        "command": "verify",
        "artifact_factory": triple_schema_hash_pass_requires_match_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": [
            "CC002_VERIFY_SCHEMA_VERSION_INVALID",
            "CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH",
            "CC012_MULTI_REASON_PRECEDENCE",
        ],
        "expected_reason_codes": [
            "PASS_REQUIRES_MATCH",
            "REBUILD_HASH_EXPECTED_MISMATCH",
            "SCHEMA_VERSION_INVALID",
        ],
        "expected_triggered_rule_ids": [
            "RULE_PASS_REQUIRES_MATCH_REBUILD_RESULT",
            "RULE_REBUILD_HASH_EXPECTED_MATCHES_ARTIFACT_ID",
            "RULE_SCHEMA_VERSION_EQUALS_DLX_ARTIFACT_V0_1",
        ],
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_triple_artifact_validator_rebuild_layout_a",
        "command": "verify",
        "artifact_factory": triple_artifact_validator_rebuild_invalid_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": ["CC012_MULTI_REASON_PRECEDENCE"],
        "expected_reason_codes": [
            "ARTIFACT_HASH_INVALID",
            "REBUILD_RESULT_INVALID",
            "VALIDATOR_RESULT_INVALID",
        ],
        "expected_triggered_rule_ids": [
            "RULE_ARTIFACT_HASH_64_HEX",
            "RULE_REBUILD_RESULT_ENUM",
            "RULE_VALIDATOR_RESULT_ENUM",
        ],
        "semantic_equivalence_group": "artifact_validator_rebuild_triple",
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_triple_artifact_validator_rebuild_layout_b",
        "command": "verify",
        "artifact_factory": triple_artifact_validator_rebuild_invalid_layout_variant,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": ["CC012_MULTI_REASON_PRECEDENCE"],
        "expected_reason_codes": [
            "ARTIFACT_HASH_INVALID",
            "REBUILD_RESULT_INVALID",
            "VALIDATOR_RESULT_INVALID",
        ],
        "expected_triggered_rule_ids": [
            "RULE_ARTIFACT_HASH_64_HEX",
            "RULE_REBUILD_RESULT_ENUM",
            "RULE_VALIDATOR_RESULT_ENUM",
        ],
        "semantic_equivalence_group": "artifact_validator_rebuild_triple",
        "layout_variant_of": "cc012_triple_artifact_validator_rebuild_layout_a",
        "must_match_selected_class_with": "cc012_triple_artifact_validator_rebuild_layout_a",
        "must_match_canonical_result_with": "cc012_triple_artifact_validator_rebuild_layout_a",
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_same_reason_validate_scalar_chain",
        "command": "validate",
        "artifact_factory": scalar_transition_chain_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC005_VALIDATE_TRANSITION_CHAIN_INVALID",
        "expected_matched_classes": ["CC005_VALIDATE_TRANSITION_CHAIN_INVALID"],
        "expected_reason_codes": ["TRANSITION_CHAIN_INVALID"],
        "expected_triggered_rule_ids": [
            "RULE_TRANSITION_CHAIN_ALLOWED_LOCAL_TRANSITIONS",
            "RULE_TRANSITION_CHAIN_CONTINUITY",
            "RULE_TRANSITION_CHAIN_NON_EMPTY_ARRAY",
            "RULE_TRANSITION_CHAIN_STEP_SHAPE",
        ],
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_same_reason_validate_multi_path",
        "command": "validate",
        "artifact_factory": validate_multi_path_transition_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC005_VALIDATE_TRANSITION_CHAIN_INVALID",
        "expected_matched_classes": ["CC005_VALIDATE_TRANSITION_CHAIN_INVALID"],
        "expected_reason_codes": ["TRANSITION_CHAIN_INVALID"],
        "expected_triggered_rule_ids": [
            "RULE_TRANSITION_CHAIN_ALLOWED_LOCAL_TRANSITIONS",
            "RULE_TRANSITION_CHAIN_CONTINUITY",
            "RULE_TRANSITION_CHAIN_STEP_SHAPE",
        ],
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_triple_schema_artifact_validator",
        "command": "verify",
        "artifact_factory": triple_schema_artifact_validator_invalid_artifact,
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_matched_classes": ["CC012_MULTI_REASON_PRECEDENCE"],
        "expected_reason_codes": [
            "ARTIFACT_HASH_INVALID",
            "SCHEMA_VERSION_INVALID",
            "VALIDATOR_RESULT_INVALID",
        ],
        "expected_triggered_rule_ids": [
            "RULE_ARTIFACT_HASH_64_HEX",
            "RULE_SCHEMA_VERSION_EQUALS_DLX_ARTIFACT_V0_1",
            "RULE_VALIDATOR_RESULT_ENUM",
        ],
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
    {
        "case_id": "cc012_harness_contamination_probe",
        "command": "verify_unsupported",
        "artifact_factory": harness_contamination_probe_artifact,
        "expected_bucket": "harness_only_gap",
        "expected_selected_class": "CC013_CONFORMANCE_ERROR_HARNESS_FAILURE",
        "expected_matched_classes": ["CC013_CONFORMANCE_ERROR_HARNESS_FAILURE"],
        "expected_reason_codes": [],
        "expected_triggered_rule_ids": [],
        "expected_precedence_invariant": "stable",
        "expected_reason_normalization": "fixed_total_order_then_deduplicate",
    },
]


def build_cases() -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []
    for spec in CASE_SPECS:
        artifact = spec["artifact_factory"]()
        artifact_path = ARTIFACTS_DIR / f"{spec['case_id']}.json"
        json_dump(artifact_path, artifact)
        cases.append(
            {
                "case_id": spec["case_id"],
                "provenance_mode": "manual_adversarial_precedence",
                "command": spec["command"],
                "artifact_path": str(artifact_path.relative_to(ROOT)),
                "expected_bucket": spec["expected_bucket"],
                "expected_selected_class": spec["expected_selected_class"],
                "expected_matched_classes": spec["expected_matched_classes"],
                "expected_reason_codes": spec["expected_reason_codes"],
                "expected_triggered_rule_ids": spec["expected_triggered_rule_ids"],
                "expected_precedence_invariant": spec["expected_precedence_invariant"],
                "expected_reason_normalization": spec["expected_reason_normalization"],
                "semantic_equivalence_group": spec.get("semantic_equivalence_group"),
                "layout_variant_of": spec.get("layout_variant_of"),
                "must_match_selected_class_with": spec.get("must_match_selected_class_with"),
                "must_match_canonical_result_with": spec.get("must_match_canonical_result_with"),
            }
        )
    return cases


def build_manifest(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "manifest_version": "0.1",
        "profile_id": "V0_1",
        "corpus_id": "precedence_adversarial_corpus_v0_1",
        "provenance_mode": "manual_adversarial_precedence",
        "generator": {
            "name": "gen_precedence_adversarial_corpus_v0_1.py",
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
            "seed": "V0_1-precedence-adversarial",
            "emit_only_in_domain": False,
            "include_boundary_cases": False,
            "include_adversarial_cases": True,
            "include_precedence_stress_cases": True,
        },
        "cases": cases,
    }


def main() -> None:
    kernel = load_json_file(KERNEL_PATH)
    domain = load_json_file(DOMAIN_PATH)
    matrix = load_json_file(MATRIX_PATH)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    cases = build_cases()

    for case in cases:
        artifact = load_json_file(ROOT / case["artifact_path"])
        result = evaluate_corpus_entry(case["command"], artifact, kernel, domain, matrix)
        if result["class_bucket"] != case["expected_bucket"]:
            raise SystemExit(f"bucket drift for {case['case_id']}: {result['class_bucket']} != {case['expected_bucket']}")
        if result["selected_class"] != case["expected_selected_class"]:
            raise SystemExit(f"class drift for {case['case_id']}: {result['selected_class']} != {case['expected_selected_class']}")
        if result["matched_classes"] != case["expected_matched_classes"]:
            raise SystemExit(f"matched_classes drift for {case['case_id']}: {result['matched_classes']} != {case['expected_matched_classes']}")
        if result["reason_codes"] != case["expected_reason_codes"]:
            raise SystemExit(f"reason code drift for {case['case_id']}: {result['reason_codes']} != {case['expected_reason_codes']}")
        if result["triggered_rule_ids"] != case["expected_triggered_rule_ids"]:
            raise SystemExit(f"triggered_rule_ids drift for {case['case_id']}: {result['triggered_rule_ids']} != {case['expected_triggered_rule_ids']}")

    json_dump(CORPUS_DIR / "manifest.json", build_manifest(cases))


if __name__ == "__main__":
    main()
