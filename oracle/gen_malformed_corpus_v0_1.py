#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from corpus_cases_v0_1 import (
    malformed_root_array_artifact,
    malformed_root_number_artifact,
    malformed_root_string_artifact,
    missing_rebuild_source_artifact,
    missing_schema_version_artifact,
    rebuild_source_invalid_artifact,
    scalar_transition_chain_artifact,
)
from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
CORPUS_DIR = CONFORMANCE_DIR / "malformed_corpus_v0_1"
ARTIFACTS_DIR = CORPUS_DIR / "artifacts"

DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"


def json_dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CASE_SPECS: List[Dict[str, Any]] = [
    {
        "case_id": "malformed_root_array_verify",
        "origin": "malformed",
        "command": "verify",
        "expected_bucket": "malformed",
        "expected_class": "CC014_MALFORMED_NON_OBJECT_ARTIFACT",
        "expected_verdict": None,
        "expected_reason_codes": [],
        "artifact_factory": malformed_root_array_artifact,
        "notes": "Top-level JSON array should be classified as malformed rather than drifting into a protocol bucket.",
    },
    {
        "case_id": "malformed_root_string_validate",
        "origin": "malformed",
        "command": "validate",
        "expected_bucket": "malformed",
        "expected_class": "CC014_MALFORMED_NON_OBJECT_ARTIFACT",
        "expected_verdict": None,
        "expected_reason_codes": [],
        "artifact_factory": malformed_root_string_artifact,
        "notes": "Top-level JSON string stays in the malformed layer across command variants.",
    },
    {
        "case_id": "malformed_root_number_rebuild",
        "origin": "malformed",
        "command": "rebuild",
        "expected_bucket": "malformed",
        "expected_class": "CC014_MALFORMED_NON_OBJECT_ARTIFACT",
        "expected_verdict": None,
        "expected_reason_codes": [],
        "artifact_factory": malformed_root_number_artifact,
        "notes": "Top-level scalar input must never silently enter the rebuild path.",
    },
    {
        "case_id": "malformed_missing_schema_version_verify",
        "origin": "malformed",
        "command": "verify",
        "expected_bucket": "in_domain_invalid",
        "expected_class": None,
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["SCHEMA_VERSION_INVALID"],
        "artifact_factory": missing_schema_version_artifact,
        "notes": "Parser-adjacent malformed object with missing schema_version must still classify deterministically.",
    },
    {
        "case_id": "malformed_scalar_transition_chain_validate",
        "origin": "malformed",
        "command": "validate",
        "expected_bucket": "in_domain_invalid",
        "expected_class": None,
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["TRANSITION_CHAIN_INVALID"],
        "artifact_factory": scalar_transition_chain_artifact,
        "notes": "Wrong transition_chain type should remain deterministic and not escape as out_of_scope.",
    },
    {
        "case_id": "malformed_missing_rebuild_source_verify",
        "origin": "malformed",
        "command": "verify",
        "expected_bucket": "out_of_scope",
        "expected_class": "CC008_VERIFY_REBUILD_SOURCE_ABSENT",
        "expected_verdict": None,
        "expected_reason_codes": [],
        "artifact_factory": missing_rebuild_source_artifact,
        "notes": "Missing required identity surface field stays on the scope boundary instead of the malformed root bucket.",
    },
    {
        "case_id": "malformed_rebuild_source_scalar_rebuild",
        "origin": "malformed",
        "command": "rebuild",
        "expected_bucket": "in_domain_invalid",
        "expected_class": None,
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["REBUILD_SOURCE_INVALID"],
        "artifact_factory": rebuild_source_invalid_artifact,
        "notes": "Invalid canonicalization input under rebuild remains an in-domain invalid, not an unhandled parser failure.",
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
        "corpus_id": "malformed_corpus_v0_1",
        "provenance_mode": "malformed_manual",
        "generator": {
            "name": "gen_malformed_corpus_v0_1.py",
            "version": "0.1.0",
        },
        "inputs": {
            "domain_profile": "conformance/DOMAIN_PROFILE_V0_1.json",
            "semantics_kernel": "conformance/SEMANTICS_KERNEL_V0_1.json",
        },
        "generation_policy": {
            "mode": "deterministic",
            "seed_policy": "fixed",
            "seed": "V0_1-malformed",
            "emit_only_in_domain": False,
            "include_boundary_cases": True,
            "include_adversarial_cases": False,
        },
        "coverage_summary": {
            "cases_total": len(cases),
            "cases_by_expected_bucket": bucket_counts,
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
