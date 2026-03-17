#!/usr/bin/env python3
"""Executable bounded semantics oracle for DeciRepo baseline V0_1."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_DIR = ROOT / "conformance" / "v0_1"
DEFAULT_KERNEL_PATH = ROOT / "conformance" / "SEMANTICS_KERNEL_V0_1.json"
DEFAULT_DOMAIN_PATH = ROOT / "conformance" / "DOMAIN_PROFILE_V0_1.json"
SUPPORTED_PREDICATE_OPERATORS = frozenset(
    {
        "input_is_json_object",
        "supported_command",
        "field_present",
        "equals",
        "optional_equals_artifact_id",
        "if_field_equals_then_field_equals",
        "non_empty_array",
        "each_step_has_keys",
        "allowed_local_transitions",
        "continuous_chain",
        "present",
        "is_object",
        "is_64_hex",
        "enum",
    }
)
SUPPORTED_COMPOSITION_OPERATORS = frozenset({"all_of", "any_of", "not"})
DECLARED_CLASS_BUCKETS = frozenset(
    {
        "malformed",
        "out_of_scope",
        "in_domain_valid",
        "in_domain_invalid",
        "in_domain_gap",
        "harness_only_gap",
    }
)


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_json_file(path: str | Path) -> Dict[str, Any]:
    return read_json(Path(path))


def stable_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable_json_hex(value: Any) -> str:
    return stable_json_bytes(value).hex()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def get_field(artifact: Dict[str, Any], field: str) -> Any:
    return artifact.get(field)


def is_object(value: Any) -> bool:
    return isinstance(value, dict)


def resolve_identity_surface(artifact: Dict[str, Any], kernel: Dict[str, Any]) -> Any:
    identity_surface = kernel["domain"]["identity_surface"]
    surface = identity_surface["path"]
    if surface != "artifact.rebuild_source":
        raise ValueError(f"unsupported identity surface: {surface}")
    if "rebuild_source" not in artifact:
        raise ValueError("identity surface artifact.rebuild_source is unresolved")
    return artifact["rebuild_source"]


def compute_artifact_identity(artifact: Dict[str, Any], kernel: Dict[str, Any]) -> Tuple[str, str]:
    identity_surface = resolve_identity_surface(artifact, kernel)
    canonical_bytes = stable_json_bytes(identity_surface)
    return canonical_bytes.hex(), sha256_hex(canonical_bytes)


def check_transition_chain_non_empty_array(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def check_transition_chain_step_shape(value: Any, required_keys: Iterable[str]) -> bool:
    if not isinstance(value, list):
        return False
    required = set(required_keys)
    return all(isinstance(step, dict) and required.issubset(step.keys()) for step in value)


def check_transition_chain_allowed(value: Any, allowed: Iterable[str]) -> bool:
    if not isinstance(value, list):
        return False
    allowed_set = set(allowed)
    for step in value:
        if not isinstance(step, dict):
            return False
        transition = f"{step.get('from')}->{step.get('to')}"
        if transition not in allowed_set:
            return False
    return True


def check_transition_chain_continuity(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    prev_to = None
    for step in value:
        if not isinstance(step, dict):
            return False
        if prev_to is not None and prev_to != step.get("from"):
            return False
        prev_to = step.get("to")
    return True


def evaluate_predicate(predicate: Dict[str, Any], artifact: Dict[str, Any], artifact_id: str | None, command: str, kernel: Dict[str, Any]) -> bool:
    operator = predicate["operator"]
    if operator not in SUPPORTED_PREDICATE_OPERATORS:
        raise ValueError(f"unsupported predicate operator: {operator}")

    if operator == "input_is_json_object":
        return is_object(artifact)
    if operator == "supported_command":
        return command in kernel["domain"]["supported_commands"]

    field = predicate.get("field")
    value = get_field(artifact, field) if field is not None else None

    if operator == "field_present":
        return field in artifact
    if operator == "equals":
        return value == predicate["value"]
    if operator == "optional_equals_artifact_id":
        return value is None or value == artifact_id
    if operator == "if_field_equals_then_field_equals":
        if get_field(artifact, predicate["if_field"]) != predicate["if_value"]:
            return True
        return get_field(artifact, predicate["then_field"]) == predicate["then_value"]
    if operator == "non_empty_array":
        return check_transition_chain_non_empty_array(value)
    if operator == "each_step_has_keys":
        return check_transition_chain_step_shape(value, predicate["required_keys"])
    if operator == "allowed_local_transitions":
        return check_transition_chain_allowed(value, predicate["allowed"])
    if operator == "continuous_chain":
        return check_transition_chain_continuity(value)
    if operator == "present":
        return field in artifact
    if operator == "is_object":
        return is_object(value)
    if operator == "is_64_hex":
        return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{64}", value))
    if operator == "enum":
        return value in predicate["allowed"]

    raise ValueError(f"unhandled supported predicate operator: {operator}")


def order_reason_codes(reason_codes: List[str], kernel: Dict[str, Any]) -> List[str]:
    order = kernel["normalized_result"]["reason_code_ordering"]["ordered_codes"]
    index = {code: pos for pos, code in enumerate(order)}
    ordered = sorted(reason_codes, key=lambda code: (index.get(code, len(order)), code))
    deduped: List[str] = []
    for code in ordered:
        if code not in deduped:
            deduped.append(code)
    return deduped


def get_bucket_order(kernel: Dict[str, Any], matrix: Dict[str, Any] | None = None) -> List[str]:
    if matrix is not None and "class_buckets" in matrix:
        return matrix["class_buckets"]
    return kernel["classification_pipeline"]["bucket_order"]


def get_known_top_level_fields(domain: Dict[str, Any]) -> set[str]:
    return set(domain["artifact_domain"].get("known_top_level_fields", []))


def applicable_rules(command: str, kernel: Dict[str, Any], rule_statuses: Iterable[str] | None = None) -> List[Dict[str, Any]]:
    allowed_statuses = set(rule_statuses or {"published"})
    return [
        rule
        for rule in kernel["rules"]
        if command in rule.get("applies_to", []) and rule["status"] in allowed_statuses
    ]


def evaluate_rule_outcomes(
    command: str,
    artifact: Dict[str, Any],
    artifact_id: str | None,
    kernel: Dict[str, Any],
    rule_statuses: Iterable[str] | None = None,
) -> Dict[str, bool]:
    outcomes: Dict[str, bool] = {}
    for rule in applicable_rules(command, kernel, rule_statuses):
        outcomes[rule["rule_id"]] = evaluate_predicate(rule["predicate"], artifact, artifact_id, command, kernel)
    return outcomes


def compute_pipeline_state(
    command: str,
    artifact: Dict[str, Any],
    kernel: Dict[str, Any],
    domain: Dict[str, Any],
    rule_statuses: Iterable[str] | None = None,
) -> Dict[str, Any]:
    state: Dict[str, Any] = {
        "command": command,
        "artifact_is_json_object": is_object(artifact),
        "command_supported": command in kernel["domain"]["supported_commands"],
        "identity_surface_resolved": False,
        "artifact_id": None,
        "canonical_identity_hex": None,
        "unknown_top_level_fields": [],
        "unknown_top_level_fields_outside_identity_surface": False,
        "rule_outcomes": {},
    }
    if not state["artifact_is_json_object"]:
        return state

    known_fields = get_known_top_level_fields(domain)
    unknown_fields = sorted(field for field in artifact.keys() if field not in known_fields)
    state["unknown_top_level_fields"] = unknown_fields
    state["unknown_top_level_fields_outside_identity_surface"] = bool(unknown_fields)

    try:
        identity_hex, artifact_id = compute_artifact_identity(artifact, kernel)
        state["identity_surface_resolved"] = True
        state["canonical_identity_hex"] = identity_hex
        state["artifact_id"] = artifact_id
    except Exception:
        state["identity_surface_resolved"] = False

    if state["command_supported"] and (state["identity_surface_resolved"] or command == "rebuild"):
        state["rule_outcomes"] = evaluate_rule_outcomes(
            command,
            artifact,
            state["artifact_id"],
            kernel,
            rule_statuses=rule_statuses,
        )

    return state


def compose_match_results(composition: str, results: List[bool]) -> bool:
    if composition == "all_of":
        return all(results)
    if composition == "any_of":
        return any(results)
    if composition == "not":
        if len(results) != 1:
            raise ValueError("not composition requires exactly one child result")
        return not results[0]
    raise ValueError(f"unsupported composition operator: {composition}")


def matches_state_requirements(requirements: Dict[str, Any], state: Dict[str, Any]) -> bool:
    for key, expected in requirements.items():
        if state.get(key) != expected:
            return False
    return True


def evaluate_matrix_predicate(predicate_entry: Dict[str, Any], state: Dict[str, Any]) -> bool:
    predicate_command = predicate_entry["command"]
    if predicate_command == "harness":
        if state["command_supported"]:
            return False
    elif predicate_command == "mixed":
        pass
    elif predicate_command != state["command"]:
        return False

    if not matches_state_requirements(predicate_entry.get("state_requirements", {}), state):
        return False

    comparisons: List[bool] = []
    for requirement in predicate_entry.get("rule_outcomes", []):
        comparisons.append(state["rule_outcomes"].get(requirement["rule_id"]) == requirement["outcome"])

    if not comparisons:
        return True
    return compose_match_results(predicate_entry["composition"], comparisons)


def select_class(matches: List[Dict[str, Any]], kernel: Dict[str, Any], matrix: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    if not matches:
        raise ValueError("unclassified_input")
    if len(matches) == 1:
        return matches[0], matches[0]["partition_mode"]

    if any(match["partition_mode"] != "ordered_precedence_chain" for match in matches):
        raise ValueError("ambiguous_input_without_declared_precedence")

    bucket_index = {bucket: idx for idx, bucket in enumerate(get_bucket_order(kernel, matrix))}
    selected = sorted(matches, key=lambda row: (bucket_index.get(row["class_bucket"], 999), row["precedence_rank"], row["class_id"]))[0]
    return selected, "ordered_precedence_chain"


def classify_artifact(
    command: str,
    artifact: Dict[str, Any],
    kernel: Dict[str, Any],
    domain: Dict[str, Any],
    matrix: Dict[str, Any],
    rule_statuses: Iterable[str] | None = None,
) -> Dict[str, Any]:
    state = compute_pipeline_state(command, artifact, kernel, domain, rule_statuses=rule_statuses)
    predicates = {predicate["predicate_id"]: predicate for predicate in matrix["predicate_registry"]}
    matches: List[Dict[str, Any]] = []

    for cls in matrix["classes"]:
        predicate = predicates[cls["predicate_ref"]]
        if evaluate_matrix_predicate(predicate, state):
            matches.append(cls)

    selected, partition_mode = select_class(matches, kernel, matrix)
    return {
        "state": state,
        "matched_classes": [cls["class_id"] for cls in matches],
        "selected_class": selected["class_id"],
        "selected_bucket": selected["class_bucket"],
        "partition_mode": partition_mode,
        "selected_class_def": selected,
    }


def evaluate_entry_conditions(command: str, artifact: Dict[str, Any], kernel: Dict[str, Any]) -> None:
    command_def = kernel["commands"][command]
    for predicate in command_def.get("entry_conditions", []):
        if not evaluate_predicate(predicate, artifact, None, command, kernel):
            if predicate["operator"] == "field_present" and predicate.get("field") == "rebuild_source":
                raise ValueError("identity surface artifact.rebuild_source is unresolved")
            raise ValueError(f"entry condition failed for command={command}: {predicate['operator']}")


def evaluate_command(
    command: str,
    artifact: Dict[str, Any],
    artifact_id: str,
    kernel: Dict[str, Any],
    rule_statuses: Iterable[str] | None = None,
    use_declared_rule_order_only: bool = True,
) -> Dict[str, Any]:
    if command not in kernel["commands"]:
        raise ValueError(f"unsupported verification_command: {command}")

    evaluate_entry_conditions(command, artifact, kernel)

    rules = applicable_rules(command, kernel, rule_statuses=rule_statuses)
    rules_by_id = {rule["rule_id"]: rule for rule in rules}
    rule_outcomes = evaluate_rule_outcomes(command, artifact, artifact_id, kernel, rule_statuses=rule_statuses)
    reason_codes: List[str] = []
    errors: List[str] = []

    if use_declared_rule_order_only:
        ordered_rule_ids = kernel["commands"][command]["rule_order"]
    else:
        ordered_rule_ids = [rule["rule_id"] for rule in rules]

    for rule_id in ordered_rule_ids:
        ok = rule_outcomes[rule_id]
        if ok:
            continue
        rule = rules_by_id[rule_id]
        reason_codes.append(rule["on_false_emit"])
        errors.append(rule_id)

    reason_codes = order_reason_codes(reason_codes, kernel)
    status = "FAIL" if reason_codes else "PASS"
    return {
        "command": command,
        "status": status,
        "errors": errors,
        "warnings": [],
        "derived": {
            "computed_rebuild_hash": artifact_id,
        },
        "reason_codes": reason_codes,
    }


def build_normalized_result(raw_result: Dict[str, Any], artifact_id: str, kernel: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": raw_result["status"],
        "artifact_id": artifact_id,
        "reason_codes": raw_result["reason_codes"],
        "protocol_version": kernel["normalized_result"]["protocol_version"],
        "verifier_result_schema": kernel["normalized_result"]["schema"],
    }


def evaluate_vector(vector_dir: Path, kernel: Dict[str, Any], domain: Dict[str, Any]) -> Dict[str, Any]:
    del domain
    vector_id = vector_dir.name
    manifest = read_json(vector_dir / "vector_manifest.json")
    artifact = read_json(vector_dir / "artifact.json")
    expected_artifact_id = (vector_dir / "expected_artifact_id.txt").read_text(encoding="utf-8").strip()
    expected_identity_hex = (vector_dir / "canonical_bytes.hex").read_text(encoding="utf-8").strip()
    expected_result = read_json(vector_dir / "expected_verification_result.json")
    expected_result_hex = (vector_dir / "expected_verification_result.canonical.hex").read_text(encoding="utf-8").strip()
    command = manifest["verification_command"]

    try:
        actual_identity_hex, actual_artifact_id = compute_artifact_identity(artifact, kernel)
        raw_result = evaluate_command(command, artifact, actual_artifact_id, kernel)
        normalized_result = build_normalized_result(raw_result, actual_artifact_id, kernel)
        actual_result_hex = stable_json_hex(normalized_result)

        checks = {
            "vector_consistency_ok": sha256_hex(bytes.fromhex(expected_identity_hex)) == expected_artifact_id,
            "canonical_identity_bytes_match": actual_identity_hex == expected_identity_hex,
            "artifact_id_match": actual_artifact_id == expected_artifact_id,
            "normalized_result_match": normalized_result == expected_result,
            "result_bytes_match": actual_result_hex == expected_result_hex,
            "unmapped_errors_empty": True,
        }
        failure_keys = [name for name, ok in checks.items() if not ok]
        verdict = "PASS" if not failure_keys else "FAIL"
        return {
            "vector_id": vector_id,
            "verdict": verdict,
            "identity_check": checks["canonical_identity_bytes_match"] and checks["artifact_id_match"],
            "verification_check": checks["normalized_result_match"],
            "result_bytes_check": checks["result_bytes_match"],
            "diagnostics": {
                "command": command,
                "reason_text": "matched_expected_outputs" if verdict == "PASS" else ",".join(failure_keys),
                "failure_keys": failure_keys,
                "checks": checks,
                "manifest": manifest,
                "raw_result": raw_result,
                "expected_normalized_result": expected_result,
                "actual_normalized_result": normalized_result,
                "unmapped_errors": [],
            },
        }
    except Exception as exc:
        return {
            "vector_id": vector_id,
            "verdict": "CONFORMANCE_ERROR",
            "identity_check": False,
            "verification_check": False,
            "result_bytes_check": False,
            "diagnostics": {
                "command": command,
                "reason_text": "runner_error",
                "failure_keys": ["runner_error"],
                "checks": {
                    "runner_ok": False
                },
                "error": str(exc),
            },
        }


def evaluate_corpus_entry(
    command: str,
    artifact: Dict[str, Any],
    kernel: Dict[str, Any],
    domain: Dict[str, Any],
    matrix: Dict[str, Any],
) -> Dict[str, Any]:
    classification = classify_artifact(
        command,
        artifact,
        kernel,
        domain,
        matrix,
        rule_statuses={"published", "registry_only_gap"},
    )
    state = classification["state"]
    selected_class_def = classification["selected_class_def"]
    class_bucket = selected_class_def["class_bucket"]

    result: Dict[str, Any] = {
        "in_domain": class_bucket in {"in_domain_valid", "in_domain_invalid", "in_domain_gap"},
        "matched_classes": classification["matched_classes"],
        "selected_class": classification["selected_class"],
        "partition_mode": classification["partition_mode"],
        "class_bucket": class_bucket,
        "predicate_error": False,
        "artifact_id": state["artifact_id"],
        "canonical_identity_hex": state["canonical_identity_hex"],
        "normalized_result": None,
        "canonical_result_hex": None,
        "verdict": selected_class_def["expected_verdict"],
        "reason_codes": list(selected_class_def.get("expected_reason_codes") or []),
    }

    if class_bucket in {"malformed", "out_of_scope", "harness_only_gap"}:
        return result

    if state["artifact_id"] is None:
        raise ValueError("in-domain corpus entry did not resolve artifact_id")

    raw_result = evaluate_command(
        command,
        artifact,
        state["artifact_id"],
        kernel,
        rule_statuses={"published", "registry_only_gap"},
        use_declared_rule_order_only=False,
    )
    normalized_result = build_normalized_result(raw_result, state["artifact_id"], kernel)
    result["normalized_result"] = normalized_result
    result["canonical_result_hex"] = stable_json_hex(normalized_result)
    result["verdict"] = raw_result["status"]
    result["reason_codes"] = raw_result["reason_codes"]
    return result


def build_report(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    failed = sum(1 for row in results if row["verdict"] != "PASS")
    has_conformance_error = any(row["verdict"] == "CONFORMANCE_ERROR" for row in results)
    overall_verdict = "CONFORMANCE_ERROR" if has_conformance_error else ("PASS" if failed == 0 else "FAIL")
    return {
        "report_schema": "decirepo-conformance-report-v0.1",
        "implementation_name": "decirepo-oracle-v0_1",
        "implementation_version": "0.1.0-oracle",
        "conformance_profile": "V0_1",
        "protocol_specification": "v0.2",
        "protocol_semantics": "v0.1",
        "vectors_total": len(results),
        "vectors_passed": len(results) - failed,
        "vectors_failed": failed,
        "overall_verdict": overall_verdict,
        "results": results,
    }


def run_profile(profile_dir: Path, kernel_path: Path, domain_path: Path) -> Dict[str, Any]:
    kernel = read_json(kernel_path)
    domain = read_json(domain_path)
    vector_dirs = sorted(p for p in profile_dir.iterdir() if p.is_dir() and p.name.startswith("vector_"))
    results = [evaluate_vector(vector_dir, kernel, domain) for vector_dir in vector_dirs]
    return build_report(results)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-dir", default=str(DEFAULT_PROFILE_DIR))
    parser.add_argument("--kernel", default=str(DEFAULT_KERNEL_PATH))
    parser.add_argument("--domain", default=str(DEFAULT_DOMAIN_PATH))
    parser.add_argument("--report-out", default=None)
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    report = run_profile(Path(args.profile_dir), Path(args.kernel), Path(args.domain))
    if args.report_out:
        out_path = Path(args.report_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["overall_verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
