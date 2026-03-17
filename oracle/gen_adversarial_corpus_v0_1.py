#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from corpus_cases_v0_1 import (
    genesis_artifact,
    invalid_artifact_hash_and_validator_result_artifact,
    invalid_artifact_hash_artifact,
    invalid_rebuild_result_artifact,
    invalid_validator_result_artifact,
    multi_reason_precedence_artifact,
    unknown_envelope_plus_schema_invalid_artifact,
)
from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
CORPUS_DIR = CONFORMANCE_DIR / "adversarial_corpus_v0_1"
ARTIFACTS_DIR = CORPUS_DIR / "artifacts"

DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"


def json_dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CASE_SPECS: List[Dict[str, Any]] = [
    {
        "case_id": "adversarial_invalid_artifact_hash",
        "origin": "adversarial",
        "command": "verify",
        "expected_bucket": "in_domain_gap",
        "expected_class": "CC009_VERIFY_ARTIFACT_HASH_INVALID",
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["ARTIFACT_HASH_INVALID"],
        "artifact_factory": invalid_artifact_hash_artifact,
        "notes": "Attacks the registry-only artifact_hash rule without changing the rest of the valid surface.",
    },
    {
        "case_id": "adversarial_invalid_validator_result",
        "origin": "adversarial",
        "command": "verify",
        "expected_bucket": "in_domain_gap",
        "expected_class": "CC010_VERIFY_VALIDATOR_RESULT_INVALID",
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["VALIDATOR_RESULT_INVALID"],
        "artifact_factory": invalid_validator_result_artifact,
        "notes": "Forces validator_result outside the bounded enum.",
    },
    {
        "case_id": "adversarial_invalid_rebuild_result",
        "origin": "adversarial",
        "command": "verify",
        "expected_bucket": "in_domain_gap",
        "expected_class": "CC011_VERIFY_REBUILD_RESULT_INVALID",
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["REBUILD_RESULT_INVALID"],
        "artifact_factory": invalid_rebuild_result_artifact,
        "notes": "Forces rebuild_result outside the bounded enum while staying inside the verify path.",
    },
    {
        "case_id": "adversarial_multi_reason_precedence",
        "origin": "adversarial",
        "command": "verify",
        "expected_bucket": "in_domain_invalid",
        "expected_class": "CC012_MULTI_REASON_PRECEDENCE",
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["REBUILD_HASH_EXPECTED_MISMATCH", "SCHEMA_VERSION_INVALID"],
        "artifact_factory": multi_reason_precedence_artifact,
        "notes": "Forces overlapping failure classes and requires ordered precedence resolution.",
    },
    {
        "case_id": "adversarial_unsupported_command",
        "origin": "adversarial",
        "command": "verify_unsupported",
        "expected_bucket": "harness_only_gap",
        "expected_class": "CC013_CONFORMANCE_ERROR_HARNESS_FAILURE",
        "expected_verdict": "CONFORMANCE_ERROR",
        "expected_reason_codes": [],
        "artifact_factory": genesis_artifact,
        "notes": "Attacks the harness boundary directly with an unsupported command.",
    },
    {
        "case_id": "adversarial_unknown_envelope_plus_schema_invalid",
        "origin": "adversarial",
        "command": "verify",
        "expected_bucket": "in_domain_invalid",
        "expected_class": "CC002_VERIFY_SCHEMA_VERSION_INVALID",
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["SCHEMA_VERSION_INVALID"],
        "artifact_factory": unknown_envelope_plus_schema_invalid_artifact,
        "notes": "Unknown envelope tolerance must not mask a real verify failure.",
    },
    {
        "case_id": "adversarial_invalid_hash_and_validator_result",
        "origin": "adversarial",
        "command": "verify",
        "expected_bucket": "in_domain_gap",
        "expected_class": "CC009_VERIFY_ARTIFACT_HASH_INVALID",
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["ARTIFACT_HASH_INVALID", "VALIDATOR_RESULT_INVALID"],
        "artifact_factory": invalid_artifact_hash_and_validator_result_artifact,
        "notes": "Conflicting registry-only gaps must not collapse to a silent PASS; precedence should pick artifact_hash_invalid while reason ordering stays stable.",
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
                "origin": spec["origin"],
                "command": spec["command"],
                "artifact_path": str(artifact_path.relative_to(ROOT)),
                "expected_bucket": spec["expected_bucket"],
                "expected_class": spec["expected_class"],
                "expected_verdict": spec["expected_verdict"],
                "expected_reason_codes": spec["expected_reason_codes"],
                "notes": spec["notes"],
            }
        )
    return cases


def build_manifest(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "manifest_version": "0.1",
        "profile_id": "V0_1",
        "corpus_id": "adversarial_corpus_v0_1",
        "provenance_mode": "manual_adversarial",
        "generator": {
            "name": "gen_adversarial_corpus_v0_1.py",
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
            "seed": "V0_1-adversarial",
            "emit_only_in_domain": False,
            "include_boundary_cases": False,
            "include_adversarial_cases": True,
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
        if case["expected_class"] and result["selected_class"] != case["expected_class"]:
            raise SystemExit(f"class drift for {case['case_id']}: {result['selected_class']} != {case['expected_class']}")
        if case["expected_verdict"] != result["verdict"]:
            raise SystemExit(f"verdict drift for {case['case_id']}: {result['verdict']} != {case['expected_verdict']}")
        if case["expected_reason_codes"] != result["reason_codes"]:
            raise SystemExit(f"reason code drift for {case['case_id']}: {result['reason_codes']} != {case['expected_reason_codes']}")

    json_dump(CORPUS_DIR / "manifest.json", build_manifest(cases))


if __name__ == "__main__":
    main()
