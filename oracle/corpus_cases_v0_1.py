#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

from decirepo_oracle_v0_1 import load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
VECTORS_DIR = CONFORMANCE_DIR / "v0_1"


def load_vector_artifact(vector_id: str) -> Dict[str, Any]:
    return load_json_file(VECTORS_DIR / vector_id / "artifact.json")


def genesis_artifact() -> Dict[str, Any]:
    return deepcopy(load_vector_artifact("vector_001_genesis"))


def transition_invalid_artifact() -> Dict[str, Any]:
    return deepcopy(load_vector_artifact("vector_005_transition_chain_invalid"))


def rebuild_source_invalid_artifact() -> Dict[str, Any]:
    return deepcopy(load_vector_artifact("vector_006_rebuild_source_invalid"))


def unknown_envelope_artifact() -> Dict[str, Any]:
    return deepcopy(load_vector_artifact("vector_007_unknown_envelope_field"))


def schema_invalid_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    return artifact


def rebuild_hash_mismatch_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["rebuild_hash_expected"] = "0" * 64
    return artifact


def pass_requires_match_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["rebuild_result"] = "MISMATCH"
    return artifact


def missing_rebuild_source_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact.pop("rebuild_source", None)
    return artifact


def invalid_artifact_hash_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["artifact_hash"] = "not-a-64-hex"
    return artifact


def invalid_validator_result_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["validator_result"] = "UNKNOWN"
    return artifact


def invalid_rebuild_result_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["validator_result"] = "FAIL"
    artifact["rebuild_result"] = "UNKNOWN"
    return artifact


def multi_reason_precedence_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    artifact["rebuild_hash_expected"] = "0" * 64
    artifact["validator_result"] = "FAIL"
    artifact["rebuild_result"] = "MATCH"
    return artifact


def unknown_envelope_plus_schema_invalid_artifact() -> Dict[str, Any]:
    artifact = unknown_envelope_artifact()
    artifact["schema_version"] = "dlx-artifact-v9.9"
    return artifact


def invalid_artifact_hash_and_validator_result_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact["artifact_hash"] = "not-a-64-hex"
    artifact["validator_result"] = "UNKNOWN"
    return artifact


def malformed_root_array_artifact() -> list[Any]:
    return []


def malformed_root_string_artifact() -> str:
    return "not-a-json-object"


def malformed_root_number_artifact() -> int:
    return 17


def missing_schema_version_artifact() -> Dict[str, Any]:
    artifact = genesis_artifact()
    artifact.pop("schema_version", None)
    return artifact


def scalar_transition_chain_artifact() -> Dict[str, Any]:
    artifact = transition_invalid_artifact()
    artifact["transition_chain"] = "not-an-array"
    return artifact
