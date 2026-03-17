#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from corpus_cases_v0_1 import (
    missing_rebuild_source_artifact,
    transition_invalid_artifact,
    unknown_envelope_artifact,
)
from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
CORPUS_DIR = CONFORMANCE_DIR / "boundary_corpus_v0_1"
ARTIFACTS_DIR = CORPUS_DIR / "artifacts"

DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"


def json_dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CASE_SPECS: List[Dict[str, Any]] = [
    {
        "case_id": "boundary_unknown_envelope_tolerated",
        "origin": "boundary",
        "command": "verify",
        "expected_bucket": "in_domain_valid",
        "expected_class": "CC007_VERIFY_UNKNOWN_TOP_LEVEL_ENVELOPE_FIELD_TOLERATED",
        "expected_verdict": "PASS",
        "expected_reason_codes": [],
        "artifact_factory": unknown_envelope_artifact,
        "notes": "Single unknown top-level envelope field remains non-semantic at the bounded verify surface.",
    },
    {
        "case_id": "boundary_missing_rebuild_source",
        "origin": "boundary",
        "command": "verify",
        "expected_bucket": "out_of_scope",
        "expected_class": "CC008_VERIFY_REBUILD_SOURCE_ABSENT",
        "expected_verdict": None,
        "expected_reason_codes": [],
        "artifact_factory": missing_rebuild_source_artifact,
        "notes": "Boundary between published baseline path and verify inputs outside the identity-surface-compatible path.",
    },
    {
        "case_id": "boundary_empty_transition_chain",
        "origin": "boundary",
        "command": "validate",
        "expected_bucket": "in_domain_invalid",
        "expected_class": "CC005_VALIDATE_TRANSITION_CHAIN_INVALID",
        "expected_verdict": "FAIL",
        "expected_reason_codes": ["TRANSITION_CHAIN_INVALID"],
        "artifact_factory": lambda: {**transition_invalid_artifact(), "transition_chain": []},
        "notes": "Minimal invalid edge for validate: empty chain rather than illegal local transition.",
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
        "corpus_id": "boundary_corpus_v0_1",
        "provenance_mode": "manual_boundary",
        "generator": {
            "name": "gen_boundary_corpus_v0_1.py",
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
            "seed": "V0_1-boundary",
            "emit_only_in_domain": False,
            "include_boundary_cases": True,
            "include_adversarial_cases": False,
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
