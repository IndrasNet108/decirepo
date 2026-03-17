#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from corpus_cases_v0_1 import (
    genesis_artifact,
    invalid_artifact_hash_artifact,
    missing_rebuild_source_artifact,
    rebuild_hash_mismatch_artifact,
    rebuild_source_invalid_artifact,
    scalar_transition_chain_artifact,
    schema_invalid_artifact,
    unknown_envelope_artifact,
)
from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
CORPUS_DIR = CONFORMANCE_DIR / "domain_guided_generated_corpus_v0_1"
ARTIFACTS_DIR = CORPUS_DIR / "artifacts"

DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"


def json_dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CASE_SPECS: List[Dict[str, Any]] = [
    {
        "case_id": "domain_verify_pass_minimal",
        "origin": "generated",
        "command": "verify",
        "expected_bucket": "in_domain_valid",
        "expected_class": None,
        "expected_verdict": "PASS",
        "expected_reason_codes": [],
        "artifact_factory": genesis_artifact,
        "notes": "Domain-guided valid verify path using only supported command and baseline-compatible identity surface.",
    },
    {
        "case_id": "domain_verify_unknown_envelope",
        "origin": "generated",
        "command": "verify",
        "expected_bucket": "in_domain_valid",
        "expected_class": None,
        "expected_verdict": "PASS",
        "expected_reason_codes": [],
        "artifact_factory": unknown_envelope_artifact,
        "notes": "Unknown top-level envelope field is tolerated while the rest of the verify surface remains valid.",
    },
    {
        "case_id": "domain_verify_schema_invalid",
        "origin": "generated",
        "command": "verify",
        "expected_bucket": "in_domain_invalid",
        "expected_class": None,
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["SCHEMA_VERSION_INVALID"],
        "artifact_factory": schema_invalid_artifact,
        "notes": "Supported command plus valid identity surface, but schema_version falls outside baseline.",
    },
    {
        "case_id": "domain_verify_hash_mismatch",
        "origin": "generated",
        "command": "verify",
        "expected_bucket": "in_domain_invalid",
        "expected_class": None,
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["REBUILD_HASH_EXPECTED_MISMATCH"],
        "artifact_factory": rebuild_hash_mismatch_artifact,
        "notes": "Supported verify path with deterministic identity mismatch.",
    },
    {
        "case_id": "domain_validate_scalar_transition_chain",
        "origin": "generated",
        "command": "validate",
        "expected_bucket": "in_domain_invalid",
        "expected_class": None,
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["TRANSITION_CHAIN_INVALID"],
        "artifact_factory": scalar_transition_chain_artifact,
        "notes": "Domain-guided invalid validate case using wrong transition_chain type without selecting a class a priori.",
    },
    {
        "case_id": "domain_rebuild_invalid_source",
        "origin": "generated",
        "command": "rebuild",
        "expected_bucket": "in_domain_invalid",
        "expected_class": None,
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["REBUILD_SOURCE_INVALID"],
        "artifact_factory": rebuild_source_invalid_artifact,
        "notes": "Supported rebuild command with parser-adjacent invalid rebuild_source.",
    },
    {
        "case_id": "domain_verify_missing_rebuild_source",
        "origin": "generated",
        "command": "verify",
        "expected_bucket": "out_of_scope",
        "expected_class": None,
        "expected_verdict": None,
        "expected_reason_codes": [],
        "artifact_factory": missing_rebuild_source_artifact,
        "notes": "Domain boundary case: verify command outside the baseline-compatible identity path.",
    },
    {
        "case_id": "domain_verify_invalid_artifact_hash",
        "origin": "generated",
        "command": "verify",
        "expected_bucket": "in_domain_gap",
        "expected_class": None,
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["ARTIFACT_HASH_INVALID"],
        "artifact_factory": invalid_artifact_hash_artifact,
        "notes": "Registry-only gap discovered from domain-valid shape plus invalid artifact_hash semantics.",
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
    bucket_counts: Dict[str, int] = {}
    for case in cases:
        bucket_counts[case["expected_bucket"]] = bucket_counts.get(case["expected_bucket"], 0) + 1
    return {
        "manifest_version": "0.1",
        "profile_id": "V0_1",
        "corpus_id": "domain_guided_generated_corpus_v0_1",
        "provenance_mode": "domain_guided",
        "generator": {
            "name": "gen_domain_guided_corpus_v0_1.py",
            "version": "0.1.0",
        },
        "inputs": {
            "domain_profile": "conformance/DOMAIN_PROFILE_V0_1.json",
            "semantics_kernel": "conformance/SEMANTICS_KERNEL_V0_1.json",
        },
        "generation_policy": {
            "mode": "deterministic",
            "seed_policy": "fixed",
            "seed": "V0_1-domain-guided",
            "emit_only_in_domain": False,
            "include_boundary_cases": True,
            "include_adversarial_cases": False,
            "class_matrix_guidance": "forbidden_during_sample_construction",
        },
        "coverage_summary": {
            "cases_total": len(cases),
            "cases_by_expected_bucket": bucket_counts,
            "cases_with_expected_class": sum(1 for case in cases if case["expected_class"] is not None),
            "cases_without_expected_class": sum(1 for case in cases if case["expected_class"] is None),
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
        if case["expected_class"] is not None and result["selected_class"] != case["expected_class"]:
            raise SystemExit(f"class drift for {case['case_id']}: {result['selected_class']} != {case['expected_class']}")
        if case["expected_verdict"] != result["verdict"]:
            raise SystemExit(f"verdict drift for {case['case_id']}: {result['verdict']} != {case['expected_verdict']}")
        if case["expected_reason_codes"] != result["reason_codes"]:
            raise SystemExit(f"reason code drift for {case['case_id']}: {result['reason_codes']} != {case['expected_reason_codes']}")

    json_dump(CORPUS_DIR / "manifest.json", build_manifest(cases))


if __name__ == "__main__":
    main()
