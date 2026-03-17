#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import load_json_file  # noqa: E402
from gen_cc012_verify_distribution_v0_1 import MUTATION_ORDER, main as generate_distribution  # noqa: E402

ANALYSIS_PATH = ROOT / "conformance" / "cc012_verify_distribution_v0_1.json"


class CC012VerifyDistributionV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        generate_distribution()
        cls.analysis = load_json_file(ANALYSIS_PATH)
        cls.summary = cls.analysis["summary"]
        cls.cases = cls.analysis["cases"]

    def test_analysis_identity_and_scope(self) -> None:
        self.assertEqual(self.analysis["profile_id"], "V0_1")
        self.assertEqual(self.analysis["analysis_id"], "cc012_verify_distribution_v0_1")
        self.assertEqual(
            self.analysis["analysis_scope"],
            "representable_verify_multi_reason_combinations_under_current_v0_1_rule_surface",
        )
        self.assertEqual(self.analysis["mutation_registry"], MUTATION_ORDER)

    def test_summary_is_self_consistent(self) -> None:
        self.assertEqual(self.summary["evaluated_combinations_total"], (2 ** len(MUTATION_ORDER)) - 1)
        self.assertEqual(self.summary["multi_reason_cases_total"], len(self.cases))
        self.assertTrue(self.cases)
        self.assertEqual(
            self.summary["population_views"],
            {
                "verify_multiple_reason_surface": len(self.cases),
                "verify_selected_cc012_surface": len(self.cases),
            },
        )
        self.assertEqual(
            self.summary["selected_class_distribution"],
            {"CC012_MULTI_REASON_PRECEDENCE": len(self.cases)},
        )

    def test_all_cases_are_stable_cc012_surfaces(self) -> None:
        for case in self.cases:
            self.assertEqual(case["selected_class"], "CC012_MULTI_REASON_PRECEDENCE", case["case_id"])
            self.assertGreaterEqual(len(case["normalized_reason_codes"]), 2, case["case_id"])
            self.assertTrue(case["conflict_topology"]["cluster_id"], case["case_id"])
            self.assertTrue(case["stability"]["selected_class_under_rule_order_perturbation"], case["case_id"])
            self.assertTrue(case["stability"]["matched_classes_under_rule_order_perturbation"], case["case_id"])
            self.assertTrue(case["stability"]["normalized_reason_codes_under_rule_order_perturbation"], case["case_id"])
            self.assertTrue(case["stability"]["canonical_result_under_rule_order_perturbation"], case["case_id"])
            self.assertTrue(case["stability"]["layout_selected_class_stable"], case["case_id"])
            self.assertTrue(case["stability"]["layout_reason_codes_stable"], case["case_id"])
            self.assertTrue(case["stability"]["layout_canonical_result_stable"], case["case_id"])

    def test_distribution_has_real_internal_variety_without_selected_class_divergence(self) -> None:
        self.assertGreater(len(self.summary["triggered_rule_pattern_distribution"]), 1)
        self.assertGreater(len(self.summary["normalized_reason_pattern_distribution"]), 1)
        self.assertGreater(self.summary["canonical_result_profile_count"], 1)
        topology = self.summary["conflict_topology_diversity"]
        self.assertIn("pairwise_reason_overlap", topology["topology_family_distribution"])
        self.assertIn("triple_reason_overlap", topology["topology_family_distribution"])
        self.assertIn("higher_order_reason_overlap", topology["topology_family_distribution"])
        self.assertIn("conflict geometry", topology["topology_axis_note"])
        excluded = {row["family"]: row["reason"] for row in topology["excluded_topology_families"]}
        self.assertIn("same_reason_multipath", excluded)
        self.assertIn("non_cc012_multi_reason_verify_surface", excluded)
        policy = topology["cluster_split_relevance_policy"]
        self.assertTrue(policy["cluster_existence_alone_is_not_split_signal"])
        self.assertEqual(
            policy["split_relevant_only_if_cluster_induces_distinct_behavior_in"],
            [
                "precedence_resolution",
                "reason_code_normalization_behavior",
                "canonicalization_behavior",
            ],
        )
        self.assertIn("no currently observed cluster", policy["current_surface_result"])
        clusters = topology["conflict_topology_clusters"]
        self.assertGreater(len(clusters), 1)
        cluster_ids = {cluster["cluster_id"] for cluster in clusters}
        self.assertEqual(len(cluster_ids), len(clusters))
        self.assertTrue(
            all(cluster["selected_class_distribution"] == {"CC012_MULTI_REASON_PRECEDENCE": cluster["case_count"]} for cluster in clusters)
        )
        self.assertTrue(all(not cluster["split_relevant"] for cluster in clusters))
        self.assertTrue(
            all(
                cluster["behavior_signature"]["reason_code_normalization_behavior"]
                == "stable_fixed_total_order_then_deduplicate"
                for cluster in clusters
            )
        )
        self.assertTrue(
            all(
                cluster["behavior_signature"]["canonicalization_behavior"]
                == "stable_under_rule_order_and_layout_perturbation"
                for cluster in clusters
            )
        )
        self.assertFalse(self.summary["family_split_signal"])
        self.assertIn(
            "all representable verify multi-reason combinations currently select CC012_MULTI_REASON_PRECEDENCE",
            self.summary["family_split_signal_reason"],
        )

    def test_interpretation_keeps_claim_ceiling_unchanged(self) -> None:
        interpretation = self.analysis["interpretation"]
        self.assertEqual(interpretation["claim_ceiling_effect"], "none")
        self.assertEqual(interpretation["analysis_role"], "empirical_baseline_not_proof_or_invariant")
        self.assertEqual(
            interpretation["current_observation"],
            "CC012 behaves as a stable convergence class across all currently observed verify multi-reason outcomes within the V0_1 representable surface",
        )
        self.assertIn("keep CC012 as a single family-class", interpretation["recommended_action"])
        self.assertEqual(interpretation["primary_population_for_family_analysis"], "verify_selected_cc012_surface")
        self.assertEqual(interpretation["secondary_population_for_family_analysis"], "verify_multiple_reason_surface")
        self.assertIn("not a completeness proof", interpretation["caveat"])


if __name__ == "__main__":
    unittest.main()
