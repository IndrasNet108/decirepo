#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import applicable_rules, evaluate_corpus_entry, load_json_file  # noqa: E402
from gen_precedence_adversarial_corpus_v0_1 import main as generate_precedence_corpus  # noqa: E402

CONFORMANCE_DIR = ROOT / "conformance"
DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"
MANIFEST_PATH = CONFORMANCE_DIR / "precedence_adversarial_corpus_v0_1" / "manifest.json"


def rule_order_variants(command: str, kernel: dict) -> list[list[str] | None]:
    rules = applicable_rules(command, kernel, rule_statuses={"published", "registry_only_gap"})
    rule_ids = [rule["rule_id"] for rule in rules]
    if not rule_ids:
        return [None]
    variants: list[list[str] | None] = [None, list(reversed(rule_ids))]
    if len(rule_ids) > 1:
        variants.append(rule_ids[1:] + rule_ids[:1])
    variants.append(sorted(rule_ids))
    deduped: list[list[str] | None] = []
    seen: set[tuple[str, ...] | None] = set()
    for variant in variants:
        key = None if variant is None else tuple(variant)
        if key not in seen:
            seen.add(key)
            deduped.append(variant)
    return deduped


class CC012PrecedenceV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        generate_precedence_corpus()
        cls.domain = load_json_file(DOMAIN_PATH)
        cls.kernel = load_json_file(KERNEL_PATH)
        cls.matrix = load_json_file(MATRIX_PATH)
        cls.manifest = load_json_file(MANIFEST_PATH)
        cls.class_by_id = {item["class_id"]: item for item in cls.matrix["classes"]}
        cls.case_by_id = {case["case_id"]: case for case in cls.manifest["cases"]}

    def test_manifest_identity(self) -> None:
        self.assertEqual(self.manifest["corpus_id"], "precedence_adversarial_corpus_v0_1")
        self.assertEqual(self.manifest["provenance_mode"], "manual_adversarial_precedence")
        self.assertEqual(len(self.manifest["cases"]), 12)

    def test_expected_surface_matches_default_execution(self) -> None:
        for case in self.manifest["cases"]:
            artifact = load_json_file(ROOT / case["artifact_path"])
            result = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)
            self.assertEqual(result["class_bucket"], case["expected_bucket"], case["case_id"])
            self.assertEqual(result["selected_class"], case["expected_selected_class"], case["case_id"])
            self.assertEqual(result["matched_classes"], case["expected_matched_classes"], case["case_id"])
            self.assertEqual(result["reason_codes"], case["expected_reason_codes"], case["case_id"])
            self.assertEqual(result["triggered_rule_ids"], case["expected_triggered_rule_ids"], case["case_id"])

    def test_selected_class_and_matched_classes_are_stable_under_rule_order_perturbation(self) -> None:
        for case in self.manifest["cases"]:
            artifact = load_json_file(ROOT / case["artifact_path"])
            baseline = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)
            for variant in rule_order_variants(case["command"], self.kernel):
                perturbed = evaluate_corpus_entry(
                    case["command"],
                    artifact,
                    self.kernel,
                    self.domain,
                    self.matrix,
                    rule_id_order_override=variant,
                )
                self.assertEqual(perturbed["selected_class"], baseline["selected_class"], case["case_id"])
                self.assertEqual(perturbed["matched_classes"], baseline["matched_classes"], case["case_id"])

    def test_reason_codes_and_canonical_result_are_stable_under_rule_order_perturbation(self) -> None:
        for case in self.manifest["cases"]:
            artifact = load_json_file(ROOT / case["artifact_path"])
            baseline = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)
            for variant in rule_order_variants(case["command"], self.kernel):
                perturbed = evaluate_corpus_entry(
                    case["command"],
                    artifact,
                    self.kernel,
                    self.domain,
                    self.matrix,
                    rule_id_order_override=variant,
                )
                self.assertEqual(perturbed["reason_codes"], baseline["reason_codes"], case["case_id"])
                self.assertEqual(perturbed["canonical_result_hex"], baseline["canonical_result_hex"], case["case_id"])
                self.assertEqual(perturbed["normalized_result"], baseline["normalized_result"], case["case_id"])
                self.assertEqual(perturbed["triggered_rule_ids"], baseline["triggered_rule_ids"], case["case_id"])

    def test_precedence_dominance_uses_highest_ranked_candidate(self) -> None:
        bucket_order = {
            bucket: index for index, bucket in enumerate(self.matrix["class_buckets"])
        }
        for case in self.manifest["cases"]:
            artifact = load_json_file(ROOT / case["artifact_path"])
            result = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)
            matched_defs = [self.class_by_id[class_id] for class_id in result["matched_classes"]]
            selected = self.class_by_id[result["selected_class"]]
            selected_rank = selected["precedence_rank"]
            selected_bucket = selected["class_bucket"]
            selected_bucket_index = bucket_order[selected_bucket]
            for defn in matched_defs:
                self.assertLessEqual(selected_bucket_index, bucket_order[defn["class_bucket"]], case["case_id"])
                if defn["class_bucket"] == selected_bucket:
                    self.assertLessEqual(selected_rank, defn["precedence_rank"], case["case_id"])

    def test_semantic_equivalence_layout_variants_match_selected_class_and_canonical_result(self) -> None:
        for case in self.manifest["cases"]:
            counterpart_id = case.get("must_match_selected_class_with")
            if not counterpart_id:
                continue
            counterpart_case = self.case_by_id[counterpart_id]
            artifact = load_json_file(ROOT / case["artifact_path"])
            counterpart_artifact = load_json_file(ROOT / counterpart_case["artifact_path"])
            result = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)
            counterpart = evaluate_corpus_entry(
                counterpart_case["command"],
                counterpart_artifact,
                self.kernel,
                self.domain,
                self.matrix,
            )
            self.assertEqual(result["selected_class"], counterpart["selected_class"], case["case_id"])
            self.assertEqual(result["canonical_result_hex"], counterpart["canonical_result_hex"], case["case_id"])
            self.assertEqual(result["reason_codes"], counterpart["reason_codes"], case["case_id"])

    def test_harness_contamination_probe_stays_out_of_normative_reason_surface(self) -> None:
        case = self.case_by_id["cc012_harness_contamination_probe"]
        artifact = load_json_file(ROOT / case["artifact_path"])
        result = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)
        self.assertEqual(result["class_bucket"], "harness_only_gap")
        self.assertEqual(result["selected_class"], "CC013_CONFORMANCE_ERROR_HARNESS_FAILURE")
        self.assertEqual(result["reason_codes"], [])
        self.assertIsNone(result["canonical_result_hex"])
        self.assertEqual(result["matched_classes"], ["CC013_CONFORMANCE_ERROR_HARNESS_FAILURE"])


if __name__ == "__main__":
    unittest.main()
