#!/usr/bin/env python3
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

from corpus_cases_v0_1 import (
    malformed_root_string_artifact,
    missing_rebuild_source_artifact,
    pass_requires_match_artifact,
    schema_invalid_artifact,
    unknown_envelope_plus_schema_invalid_artifact,
)
from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
CORPUS_DIR = CONFORMANCE_DIR / "cc012_negative_verify_corpus_v0_1"
ARTIFACTS_DIR = CORPUS_DIR / "artifacts"

DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"


def json_dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reorder_artifact(artifact: Dict[str, Any], top_level_order: List[str]) -> Dict[str, Any]:
    ordered: Dict[str, Any] = {}
    for key in top_level_order:
        if key in artifact:
            ordered[key] = deepcopy(artifact[key])
    for key, value in artifact.items():
        if key not in ordered:
            ordered[key] = deepcopy(value)
    return ordered


def out_of_scope_schema_noise_artifact() -> Dict[str, Any]:
    artifact = missing_rebuild_source_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    return artifact


def out_of_scope_registry_noise_artifact() -> Dict[str, Any]:
    artifact = missing_rebuild_source_artifact()
    artifact["artifact_hash"] = "not-a-64-hex"
    artifact["validator_result"] = "UNKNOWN"
    return artifact


def malformed_root_array_noise_artifact() -> list[Any]:
    return [
        {
            "schema_version": "dlx-artifact-v9.9",
            "artifact_hash": "not-a-64-hex",
            "validator_result": "UNKNOWN",
        }
    ]


def layout_negative_schema_noise_artifact() -> Dict[str, Any]:
    return unknown_envelope_plus_schema_invalid_artifact()


def layout_negative_schema_noise_variant_artifact() -> Dict[str, Any]:
    artifact = unknown_envelope_plus_schema_invalid_artifact()
    return reorder_artifact(
        artifact,
        [
            "unknown_boundary_field",
            "schema_version",
            "validator_result",
            "rebuild_result",
            "rebuild_hash_expected",
            "rebuild_source",
            "decision_id",
            "publisher",
            "policy_version",
        ],
    )


def harness_contamination_pass_requires_match_artifact() -> Dict[str, Any]:
    artifact = pass_requires_match_artifact()
    artifact["harness_trace"] = {
        "runner": "cc012-negative-verify",
        "attempts": [
            1,
            {
                "phase": "negative-capture",
                "notes": ["verify", "noise", "must_not_escape_public_surface"],
            },
        ],
    }
    return artifact


CASE_SPECS: List[Dict[str, Any]] = [
    {
        "case_id": "cc012_verify_neg_001_schema_invalid_neighbor",
        "cc012_negative_mode": "neighbor_class_non_regression",
        "command": "verify",
        "artifact_factory": schema_invalid_artifact,
        "input_shape_profile": "minimal_valid_envelope_shape",
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC002_VERIFY_SCHEMA_VERSION_INVALID",
        "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_multiple_reason_codes": False,
        "expected_triggered_rule_count_min": 1,
        "expected_normalized_reason_codes": ["SCHEMA_VERSION_INVALID"],
    },
    {
        "case_id": "cc012_verify_neg_002_harness_trace_pass_requires_match",
        "cc012_negative_mode": "harness_contamination_negative",
        "command": "verify",
        "artifact_factory": harness_contamination_pass_requires_match_artifact,
        "input_shape_profile": "deep_nested_unknown_envelope_shape",
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC004_VERIFY_PASS_REQUIRES_MATCH",
        "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_multiple_reason_codes": False,
        "expected_triggered_rule_count_min": 1,
        "expected_normalized_reason_codes": ["PASS_REQUIRES_MATCH"],
    },
    {
        "case_id": "cc012_verify_neg_003_layout_negative_schema_noise_a",
        "cc012_negative_mode": "layout_equivalence_negative",
        "command": "verify",
        "artifact_factory": layout_negative_schema_noise_artifact,
        "input_shape_profile": "unknown_field_layout_variant_shape",
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC002_VERIFY_SCHEMA_VERSION_INVALID",
        "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_multiple_reason_codes": False,
        "expected_triggered_rule_count_min": 1,
        "expected_normalized_reason_codes": ["SCHEMA_VERSION_INVALID"],
        "semantic_equivalence_group": "layout_negative_schema_noise",
        "must_match_selected_class_with": "cc012_verify_neg_004_layout_negative_schema_noise_b",
        "must_match_canonical_result_with": "cc012_verify_neg_004_layout_negative_schema_noise_b",
    },
    {
        "case_id": "cc012_verify_neg_004_layout_negative_schema_noise_b",
        "cc012_negative_mode": "layout_equivalence_negative",
        "command": "verify",
        "artifact_factory": layout_negative_schema_noise_variant_artifact,
        "input_shape_profile": "unknown_field_layout_variant_shape",
        "expected_bucket": "in_domain_invalid",
        "expected_selected_class": "CC002_VERIFY_SCHEMA_VERSION_INVALID",
        "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_multiple_reason_codes": False,
        "expected_triggered_rule_count_min": 1,
        "expected_normalized_reason_codes": ["SCHEMA_VERSION_INVALID"],
        "semantic_equivalence_group": "layout_negative_schema_noise",
        "layout_variant_of": "cc012_verify_neg_003_layout_negative_schema_noise_a",
        "must_match_selected_class_with": "cc012_verify_neg_003_layout_negative_schema_noise_a",
        "must_match_canonical_result_with": "cc012_verify_neg_003_layout_negative_schema_noise_a",
    },
    {
        "case_id": "cc012_verify_neg_005_out_of_scope_schema_noise",
        "cc012_negative_mode": "boundary_out_of_scope",
        "command": "verify",
        "artifact_factory": out_of_scope_schema_noise_artifact,
        "input_shape_profile": "near_boundary_missing_identity_surface_shape",
        "expected_bucket": "out_of_scope",
        "expected_selected_class": "CC008_VERIFY_REBUILD_SOURCE_ABSENT",
        "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_multiple_reason_codes": False,
        "expected_triggered_rule_count_min": 0,
        "expected_normalized_reason_codes": [],
    },
    {
        "case_id": "cc012_verify_neg_006_out_of_scope_registry_noise",
        "cc012_negative_mode": "future_scope_exclusion",
        "command": "verify",
        "artifact_factory": out_of_scope_registry_noise_artifact,
        "input_shape_profile": "near_boundary_missing_identity_surface_shape",
        "expected_bucket": "out_of_scope",
        "expected_selected_class": "CC008_VERIFY_REBUILD_SOURCE_ABSENT",
        "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_multiple_reason_codes": False,
        "expected_triggered_rule_count_min": 0,
        "expected_normalized_reason_codes": [],
    },
    {
        "case_id": "cc012_verify_neg_007_malformed_root_array",
        "cc012_negative_mode": "malformed_short_circuit",
        "command": "verify",
        "artifact_factory": malformed_root_array_noise_artifact,
        "input_shape_profile": "malformed_non_object_root_shape",
        "expected_bucket": "malformed",
        "expected_selected_class": "CC014_MALFORMED_NON_OBJECT_ARTIFACT",
        "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_multiple_reason_codes": False,
        "expected_triggered_rule_count_min": 0,
        "expected_normalized_reason_codes": [],
    },
    {
        "case_id": "cc012_verify_neg_008_malformed_root_string",
        "cc012_negative_mode": "malformed_short_circuit",
        "command": "verify",
        "artifact_factory": malformed_root_string_artifact,
        "input_shape_profile": "malformed_non_object_root_shape",
        "expected_bucket": "malformed",
        "expected_selected_class": "CC014_MALFORMED_NON_OBJECT_ARTIFACT",
        "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_multiple_reason_codes": False,
        "expected_triggered_rule_count_min": 0,
        "expected_normalized_reason_codes": [],
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
                "cc012_negative_mode": spec["cc012_negative_mode"],
                "command": spec["command"],
                "artifact_path": str(artifact_path.relative_to(ROOT)),
                "input_shape_profile": spec["input_shape_profile"],
                "expected_bucket": spec["expected_bucket"],
                "expected_selected_class": spec["expected_selected_class"],
                "must_not_select_class": spec["must_not_select_class"],
                "expected_multiple_reason_codes": spec["expected_multiple_reason_codes"],
                "expected_triggered_rule_count_min": spec["expected_triggered_rule_count_min"],
                "expected_normalized_reason_codes": spec["expected_normalized_reason_codes"],
                "assertions": [
                    "stable_selected_class",
                    "stable_matched_classes",
                    "stable_normalized_reason_codes",
                    "stable_canonical_result_hex",
                ],
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
        "corpus_id": "cc012_negative_verify_corpus_v0_1",
        "provenance_mode": "manual_adversarial_negative_capture_verify_only",
        "generator": {
            "name": "gen_cc012_negative_verify_corpus_v0_1.py",
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
            "seed": "V0_1-cc012-negative-verify",
            "emit_only_in_domain": False,
            "include_boundary_cases": True,
            "include_adversarial_cases": True,
            "include_negative_capture_cases": True,
            "verify_only": True,
        },
        "negative_capture_contract": {
            "verify_only": True,
            "must_not_select_class": "CC012_MULTI_REASON_PRECEDENCE",
            "paired_positive_corpus_manifest": "conformance/precedence_adversarial_corpus_v0_1/manifest.json",
            "mode_minima": {
                "neighbor_class_non_regression": 1,
                "harness_contamination_negative": 1,
                "layout_equivalence_negative": 2,
                "boundary_out_of_scope": 1,
                "future_scope_exclusion": 1,
                "malformed_short_circuit": 2,
            },
            "bucket_minima": {
                "in_domain_invalid": 4,
                "out_of_scope": 2,
                "malformed": 2,
            },
            "input_shape_profile_minima": {
                "minimal_valid_envelope_shape": 1,
                "deep_nested_unknown_envelope_shape": 1,
                "unknown_field_layout_variant_shape": 2,
                "near_boundary_missing_identity_surface_shape": 2,
                "malformed_non_object_root_shape": 2,
            },
            "expected_multiple_reason_codes_policy": {
                "all_cases_must_be_false": True,
                "reason": "under CASE_CLASS_MATRIX_V0_1, any in-domain verify artifact with multiple_reason_codes=true is selected as CC012_MULTI_REASON_PRECEDENCE; out_of_scope and malformed buckets short-circuit before reason normalization",
            },
            "excluded_negative_modes": [
                {
                    "mode": "multi_reason_non_precedence",
                    "reason": "not representable in verify under current V0_1 matrix because multiple_reason_codes=true implies CC012 selection for in-domain verify artifacts",
                },
                {
                    "mode": "same_reason_multipath",
                    "reason": "not representable in verify under current V0_1 kernel because verify rules emit distinct reason codes",
                },
            ],
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
        if result["selected_class"] == case["must_not_select_class"]:
            raise SystemExit(f"overcapture for {case['case_id']}: selected {result['selected_class']}")
        if result["multiple_reason_codes"] != case["expected_multiple_reason_codes"]:
            raise SystemExit(f"multiple_reason_codes drift for {case['case_id']}: {result['multiple_reason_codes']} != {case['expected_multiple_reason_codes']}")
        if result["triggered_rule_count"] < case["expected_triggered_rule_count_min"]:
            raise SystemExit(f"triggered_rule_count drift for {case['case_id']}: {result['triggered_rule_count']} < {case['expected_triggered_rule_count_min']}")
        if result["normalized_reason_codes"] != case["expected_normalized_reason_codes"]:
            raise SystemExit(f"normalized_reason_codes drift for {case['case_id']}: {result['normalized_reason_codes']} != {case['expected_normalized_reason_codes']}")

    json_dump(CORPUS_DIR / "manifest.json", build_manifest(cases))


if __name__ == "__main__":
    main()
