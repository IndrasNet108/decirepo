#!/usr/bin/env python3
from __future__ import annotations

import json
from copy import deepcopy
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from corpus_cases_v0_1 import genesis_artifact
from decirepo_oracle_v0_1 import applicable_rules, evaluate_corpus_entry, load_json_file

ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"
ANALYSIS_PATH = CONFORMANCE_DIR / "cc012_verify_distribution_v0_1.json"
DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"

MUTATION_ORDER: List[str] = [
    "schema_version_invalid",
    "rebuild_hash_expected_mismatch",
    "pass_requires_match",
    "artifact_hash_invalid",
    "validator_result_invalid",
    "rebuild_result_invalid",
]


def json_dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def top_level_reordered_artifact(artifact: Dict[str, Any]) -> Dict[str, Any]:
    ordered: Dict[str, Any] = {}
    for key in reversed(list(artifact.keys())):
        value = deepcopy(artifact[key])
        if key == "rebuild_source" and isinstance(value, dict):
            nested: Dict[str, Any] = {}
            for nested_key in reversed(list(value.keys())):
                nested[nested_key] = deepcopy(value[nested_key])
            value = nested
        ordered[key] = value
    return ordered


def rule_order_variants(kernel: Dict[str, Any]) -> List[List[str] | None]:
    rules = applicable_rules("verify", kernel, rule_statuses={"published", "registry_only_gap"})
    rule_ids = [rule["rule_id"] for rule in rules]
    variants: List[List[str] | None] = [None]
    if not rule_ids:
        return variants
    candidates: List[List[str]] = [
        list(reversed(rule_ids)),
        rule_ids[1:] + rule_ids[:1],
        sorted(rule_ids),
    ]
    seen: set[Tuple[str, ...] | None] = {None}
    for variant in candidates:
        key = tuple(variant)
        if key not in seen:
            seen.add(key)
            variants.append(variant)
    return variants


def build_artifact_for_mutations(mutations: Iterable[str]) -> Dict[str, Any]:
    mutation_set = set(mutations)
    artifact = genesis_artifact()

    if "schema_version_invalid" in mutation_set:
        artifact["schema_version"] = "dlx-artifact-v9.9"
    if "rebuild_hash_expected_mismatch" in mutation_set:
        artifact["rebuild_hash_expected"] = "0" * 64
    if "artifact_hash_invalid" in mutation_set:
        artifact["artifact_hash"] = "not-a-64-hex"

    if "validator_result_invalid" in mutation_set:
        artifact["validator_result"] = "UNKNOWN"
    elif "rebuild_result_invalid" in mutation_set:
        artifact["validator_result"] = "FAIL"
    else:
        artifact["validator_result"] = "PASS"

    if "rebuild_result_invalid" in mutation_set:
        artifact["rebuild_result"] = "UNKNOWN"
    elif "pass_requires_match" in mutation_set:
        artifact["rebuild_result"] = "MISMATCH"
    else:
        artifact["rebuild_result"] = "MATCH"

    return artifact


def pattern_key(values: List[str]) -> str:
    return "|".join(values)


def topology_family_for_reason_count(reason_count: int) -> str:
    if reason_count == 2:
        return "pairwise_reason_overlap"
    if reason_count == 3:
        return "triple_reason_overlap"
    return "higher_order_reason_overlap"


def build_conflict_topology_clusters(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    clusters_by_key: Dict[Tuple[Tuple[str, ...], Tuple[str, ...]], Dict[str, Any]] = {}

    for case in cases:
        triggered_pattern = tuple(case["triggered_rule_ids"])
        normalized_pattern = tuple(case["normalized_reason_codes"])
        cluster_key = (triggered_pattern, normalized_pattern)
        cluster = clusters_by_key.get(cluster_key)
        if cluster is None:
            cluster = {
                "triggered_rule_pattern": list(triggered_pattern),
                "normalized_reason_pattern": list(normalized_pattern),
                "topology_family": topology_family_for_reason_count(len(normalized_pattern)),
                "case_ids": [],
                "selected_class_distribution": {},
                "canonical_result_profiles": set(),
                "all_selected_class_stable": True,
                "all_reason_ordering_stable": True,
                "all_canonicalization_stable": True,
            }
            clusters_by_key[cluster_key] = cluster

        cluster["case_ids"].append(case["case_id"])
        cluster["selected_class_distribution"][case["selected_class"]] = (
            cluster["selected_class_distribution"].get(case["selected_class"], 0) + 1
        )
        cluster["canonical_result_profiles"].add(case["canonical_result_hex"])
        cluster["all_selected_class_stable"] &= case["stability"]["selected_class_under_rule_order_perturbation"]
        cluster["all_reason_ordering_stable"] &= (
            case["stability"]["normalized_reason_codes_under_rule_order_perturbation"]
            and case["stability"]["layout_reason_codes_stable"]
        )
        cluster["all_canonicalization_stable"] &= (
            case["stability"]["canonical_result_under_rule_order_perturbation"]
            and case["stability"]["layout_canonical_result_stable"]
        )

    ordered_keys = sorted(
        clusters_by_key,
        key=lambda item: (
            len(item[1]),
            item[1],
            len(item[0]),
            item[0],
        ),
    )
    clusters: List[Dict[str, Any]] = []
    case_to_cluster: Dict[str, str] = {}

    for index, cluster_key in enumerate(ordered_keys, start=1):
        cluster = clusters_by_key[cluster_key]
        cluster_id = f"CC012_TOPOLOGY_{index:03d}"
        case_count = len(cluster["case_ids"])
        split_relevant = not (
            len(cluster["selected_class_distribution"]) == 1
            and cluster["all_selected_class_stable"]
            and cluster["all_reason_ordering_stable"]
            and cluster["all_canonicalization_stable"]
        )
        for case_id in cluster["case_ids"]:
            case_to_cluster[case_id] = cluster_id
        clusters.append(
            {
                "cluster_id": cluster_id,
                "triggered_rule_pattern": cluster["triggered_rule_pattern"],
                "normalized_reason_pattern": cluster["normalized_reason_pattern"],
                "topology_family": cluster["topology_family"],
                "case_count": case_count,
                "selected_class_distribution": cluster["selected_class_distribution"],
                "behavior_signature": {
                    "precedence_resolution_outcomes": sorted(cluster["selected_class_distribution"]),
                    "reason_code_normalization_behavior": (
                        "stable_fixed_total_order_then_deduplicate"
                        if cluster["all_reason_ordering_stable"]
                        else "divergent_under_perturbation"
                    ),
                    "canonicalization_behavior": (
                        "stable_under_rule_order_and_layout_perturbation"
                        if cluster["all_canonicalization_stable"]
                        else "divergent_under_perturbation"
                    ),
                },
                "split_relevant": split_relevant,
                "split_relevance_reason": (
                    "cluster existence alone is not split-relevant under the current surface because precedence resolution, reason-code normalization, and canonicalization behavior remain stable"
                    if not split_relevant
                    else "cluster exhibits distinguishable behavior in precedence resolution, normalization ordering, or canonicalization behavior"
                ),
            }
        )

    return clusters, case_to_cluster


def enumerate_multi_reason_cases(
    kernel: Dict[str, Any],
    domain: Dict[str, Any],
    matrix: Dict[str, Any],
) -> Dict[str, Any]:
    variants = rule_order_variants(kernel)
    cases: List[Dict[str, Any]] = []
    evaluated_total = 0

    for size in range(1, len(MUTATION_ORDER) + 1):
        for mutation_combo in combinations(MUTATION_ORDER, size):
            evaluated_total += 1
            artifact = build_artifact_for_mutations(mutation_combo)
            baseline = evaluate_corpus_entry("verify", artifact, kernel, domain, matrix)
            if not baseline["multiple_reason_codes"]:
                continue

            layout_variant = top_level_reordered_artifact(artifact)
            layout_result = evaluate_corpus_entry("verify", layout_variant, kernel, domain, matrix)

            perturbation_results = []
            stable_selected_class = True
            stable_matched_classes = True
            stable_reason_codes = True
            stable_canonical_result = True
            stable_triggered_rule_ids = True
            for variant in variants:
                perturbed = evaluate_corpus_entry(
                    "verify",
                    artifact,
                    kernel,
                    domain,
                    matrix,
                    rule_id_order_override=variant,
                )
                perturbation_results.append(
                    {
                        "rule_order_override": variant,
                        "selected_class": perturbed["selected_class"],
                        "matched_classes": perturbed["matched_classes"],
                        "normalized_reason_codes": perturbed["normalized_reason_codes"],
                        "canonical_result_hex": perturbed["canonical_result_hex"],
                        "triggered_rule_ids": perturbed["triggered_rule_ids"],
                    }
                )
                stable_selected_class &= perturbed["selected_class"] == baseline["selected_class"]
                stable_matched_classes &= perturbed["matched_classes"] == baseline["matched_classes"]
                stable_reason_codes &= perturbed["normalized_reason_codes"] == baseline["normalized_reason_codes"]
                stable_canonical_result &= perturbed["canonical_result_hex"] == baseline["canonical_result_hex"]
                stable_triggered_rule_ids &= perturbed["triggered_rule_ids"] == baseline["triggered_rule_ids"]

            cases.append(
                {
                    "case_id": "verify_multi_reason_" + "__".join(mutation_combo),
                    "requested_mutations": list(mutation_combo),
                    "selected_class": baseline["selected_class"],
                    "class_bucket": baseline["class_bucket"],
                    "matched_classes": baseline["matched_classes"],
                    "triggered_rule_ids": baseline["triggered_rule_ids"],
                    "normalized_reason_codes": baseline["normalized_reason_codes"],
                    "canonical_result_hex": baseline["canonical_result_hex"],
                    "artifact_id": baseline["artifact_id"],
                    "stability": {
                        "selected_class_under_rule_order_perturbation": stable_selected_class,
                        "matched_classes_under_rule_order_perturbation": stable_matched_classes,
                        "normalized_reason_codes_under_rule_order_perturbation": stable_reason_codes,
                        "canonical_result_under_rule_order_perturbation": stable_canonical_result,
                        "triggered_rule_ids_under_rule_order_perturbation": stable_triggered_rule_ids,
                        "layout_selected_class_stable": layout_result["selected_class"] == baseline["selected_class"],
                        "layout_reason_codes_stable": layout_result["normalized_reason_codes"] == baseline["normalized_reason_codes"],
                        "layout_canonical_result_stable": layout_result["canonical_result_hex"] == baseline["canonical_result_hex"],
                    },
                    "layout_variant": {
                        "selected_class": layout_result["selected_class"],
                        "normalized_reason_codes": layout_result["normalized_reason_codes"],
                        "canonical_result_hex": layout_result["canonical_result_hex"],
                    },
                    "perturbation_samples": perturbation_results,
                }
            )

    conflict_topology_clusters, case_to_cluster = build_conflict_topology_clusters(cases)
    for case in cases:
        case["conflict_topology"] = {
            "cluster_id": case_to_cluster[case["case_id"]],
            "topology_family": topology_family_for_reason_count(len(case["normalized_reason_codes"])),
            "triggered_rule_cardinality": len(case["triggered_rule_ids"]),
            "normalized_reason_cardinality": len(case["normalized_reason_codes"]),
        }

    selected_class_distribution: Dict[str, int] = {}
    triggered_rule_pattern_distribution: Dict[str, int] = {}
    normalized_reason_pattern_distribution: Dict[str, int] = {}
    canonical_result_distribution: Dict[str, int] = {}
    triggered_rule_cardinality_distribution: Dict[str, int] = {}
    normalized_reason_cardinality_distribution: Dict[str, int] = {}
    topology_family_distribution: Dict[str, int] = {}

    for case in cases:
        selected_class_distribution[case["selected_class"]] = selected_class_distribution.get(case["selected_class"], 0) + 1
        triggered_key = pattern_key(case["triggered_rule_ids"])
        reason_key = pattern_key(case["normalized_reason_codes"])
        canonical_key = case["canonical_result_hex"]
        triggered_cardinality = str(len(case["triggered_rule_ids"]))
        reason_cardinality = str(len(case["normalized_reason_codes"]))
        topology_family = topology_family_for_reason_count(len(case["normalized_reason_codes"]))
        triggered_rule_pattern_distribution[triggered_key] = triggered_rule_pattern_distribution.get(triggered_key, 0) + 1
        normalized_reason_pattern_distribution[reason_key] = normalized_reason_pattern_distribution.get(reason_key, 0) + 1
        canonical_result_distribution[canonical_key] = canonical_result_distribution.get(canonical_key, 0) + 1
        triggered_rule_cardinality_distribution[triggered_cardinality] = triggered_rule_cardinality_distribution.get(triggered_cardinality, 0) + 1
        normalized_reason_cardinality_distribution[reason_cardinality] = normalized_reason_cardinality_distribution.get(reason_cardinality, 0) + 1
        topology_family_distribution[topology_family] = topology_family_distribution.get(topology_family, 0) + 1

    all_stable = all(
        case["stability"]["selected_class_under_rule_order_perturbation"]
        and case["stability"]["matched_classes_under_rule_order_perturbation"]
        and case["stability"]["normalized_reason_codes_under_rule_order_perturbation"]
        and case["stability"]["canonical_result_under_rule_order_perturbation"]
        and case["stability"]["layout_selected_class_stable"]
        and case["stability"]["layout_reason_codes_stable"]
        and case["stability"]["layout_canonical_result_stable"]
        for case in cases
    )
    singleton_selected_class = set(selected_class_distribution) == {"CC012_MULTI_REASON_PRECEDENCE"}

    return {
        "evaluated_combinations_total": evaluated_total,
        "multi_reason_cases_total": len(cases),
        "population_views": {
            "verify_multiple_reason_surface": len(cases),
            "verify_selected_cc012_surface": sum(
                1 for case in cases if case["selected_class"] == "CC012_MULTI_REASON_PRECEDENCE"
            ),
        },
        "selected_class_distribution": selected_class_distribution,
        "triggered_rule_pattern_distribution": triggered_rule_pattern_distribution,
        "normalized_reason_pattern_distribution": normalized_reason_pattern_distribution,
        "canonical_result_profile_count": len(canonical_result_distribution),
        "conflict_topology_diversity": {
            "triggered_rule_cardinality_distribution": triggered_rule_cardinality_distribution,
            "normalized_reason_cardinality_distribution": normalized_reason_cardinality_distribution,
            "topology_family_distribution": topology_family_distribution,
            "conflict_topology_clusters": conflict_topology_clusters,
            "topology_axis_note": "captures conflict geometry among representable CC012-reachable verify overlaps; distinct from input_shape_diversity and broader semantic/domain diversity",
            "cluster_split_relevance_policy": {
                "cluster_existence_alone_is_not_split_signal": True,
                "split_relevant_only_if_cluster_induces_distinct_behavior_in": [
                    "precedence_resolution",
                    "reason_code_normalization_behavior",
                    "canonicalization_behavior",
                ],
                "current_surface_result": "no currently observed cluster induces distinguishable split-relevant behavior",
            },
            "excluded_topology_families": [
                {
                    "family": "same_reason_multipath",
                    "reason": "not representable in verify under the current V0_1 rule surface because verify rules emit distinct reason codes",
                },
                {
                    "family": "non_cc012_multi_reason_verify_surface",
                    "reason": "not representable in verify under the current V0_1 matrix because in-domain verify with multiple_reason_codes=true selects CC012_MULTI_REASON_PRECEDENCE",
                },
            ],
        },
        "family_split_signal": not (singleton_selected_class and all_stable),
        "family_split_signal_reason": (
            "all representable verify multi-reason combinations currently select CC012_MULTI_REASON_PRECEDENCE and remain stable under rule-order and layout perturbation"
            if singleton_selected_class and all_stable
            else "representable verify multi-reason combinations diverge by selected class or stability invariants"
        ),
        "cases": cases,
    }


def build_analysis() -> Dict[str, Any]:
    kernel = load_json_file(KERNEL_PATH)
    domain = load_json_file(DOMAIN_PATH)
    matrix = load_json_file(MATRIX_PATH)
    summary = enumerate_multi_reason_cases(kernel, domain, matrix)
    return {
        "analysis_version": "0.1",
        "profile_id": "V0_1",
        "analysis_id": "cc012_verify_distribution_v0_1",
        "analysis_scope": "representable_verify_multi_reason_combinations_under_current_v0_1_rule_surface",
        "inputs": {
            "domain_profile": "conformance/DOMAIN_PROFILE_V0_1.json",
            "semantics_kernel": "conformance/SEMANTICS_KERNEL_V0_1.json",
            "case_class_matrix": "conformance/CASE_CLASS_MATRIX_V0_1.json",
            "paired_positive_corpus": "conformance/precedence_adversarial_corpus_v0_1/manifest.json",
            "paired_negative_corpus": "conformance/cc012_negative_verify_corpus_v0_1/manifest.json",
        },
        "verify_rule_surface": {
            "published_rule_order": kernel["commands"]["verify"]["rule_order"],
            "registry_only_gap_rules": [
                "RULE_ARTIFACT_HASH_64_HEX",
                "RULE_VALIDATOR_RESULT_ENUM",
                "RULE_REBUILD_RESULT_ENUM",
            ],
        },
        "mutation_registry": MUTATION_ORDER,
        "summary": {k: v for k, v in summary.items() if k != "cases"},
        "cases": summary["cases"],
        "interpretation": {
            "claim_ceiling_effect": "none",
            "analysis_role": "empirical_baseline_not_proof_or_invariant",
            "current_observation": "CC012 behaves as a stable convergence class across all currently observed verify multi-reason outcomes within the V0_1 representable surface",
            "recommended_action": (
                "keep CC012 as a single family-class under the current ceiling unless future evidence shows selected-class divergence or stability failures"
                if not summary["family_split_signal"]
                else "inspect candidate subfamilies before considering a claim-relevant family split"
            ),
            "primary_population_for_family_analysis": "verify_selected_cc012_surface",
            "secondary_population_for_family_analysis": "verify_multiple_reason_surface",
            "caveat": "empirical over the enumerated representable verify mutation combinations under the current V0_1 kernel and matrix; not a completeness proof",
        },
    }


def main() -> None:
    json_dump(ANALYSIS_PATH, build_analysis())


if __name__ == "__main__":
    main()
