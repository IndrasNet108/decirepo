#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import load_json_file  # noqa: E402

STATUS_PATH = ROOT / "conformance" / "BOUNDED_COMPLETENESS_STATUS_V0_1.json"
GAP_PATH = ROOT / "conformance" / "GAP_CLASSIFICATION_V0_1.json"


class BoundedCompletenessStatusV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.status = load_json_file(STATUS_PATH)
        cls.ledger = load_json_file(GAP_PATH)
        cls.ledger_by_id = {gap["gap_id"]: gap for gap in cls.ledger["gaps"]}
        cls.status_by_id = {gap["gap_id"]: gap for gap in cls.status["gap_status"]}

    def test_top_level_status_ceiling_is_explicit(self) -> None:
        self.assertEqual(self.status["profile_id"], "V0_1")
        self.assertEqual(self.status["protocol_specification"], "v0.2")
        self.assertEqual(self.status["protocol_semantics"], "v0.1")
        self.assertEqual(self.status["framework_status"], "bounded_conformance_framework_present")
        self.assertEqual(self.status["known_gap_boundary_status"], "sealed_known_gap_boundary")
        self.assertFalse(self.status["bounded_completeness_proven"])

    def test_status_revision_is_traceable(self) -> None:
        revision = self.status["status_revision"]
        self.assertTrue(revision["revision_id"])
        self.assertTrue(revision["change_reason"].strip())
        self.assertEqual(revision["revision_id"], "status-v0.1-r11")
        self.assertEqual(
            revision["recomputed_from"],
            [
                "conformance/GAP_CLASSIFICATION_V0_1.json",
                "conformance/SEMANTICS_KERNEL_V0_1.json",
                "conformance/DOMAIN_PROFILE_V0_1.json",
                "conformance/CASE_CLASS_MATRIX_V0_1.json",
            ],
        )

    def test_legacy_cc012_cross_command_corpus_is_superseded(self) -> None:
        superseded = self.status["superseded_artifacts"]
        self.assertEqual(len(superseded), 1)
        artifact = superseded[0]
        self.assertEqual(artifact["artifact_id"], "conformance/cc012_negative_corpus_v0_1")
        self.assertEqual(artifact["status"], "superseded")
        self.assertEqual(
            artifact["superseded_by"],
            "conformance/cc012_negative_verify_corpus_v0_1/manifest.json",
        )
        self.assertTrue(artifact["excluded_from_claim_surface"])
        self.assertTrue(artifact["reason"].strip())

    def test_blocker_set_stability_gate_prevents_premature_ceiling_raise(self) -> None:
        stability = self.status["blocker_set_stability"]
        self.assertEqual(stability["status"], "unstable_under_active_exploration")
        self.assertFalse(stability["claim_ceiling_raise_permitted"])
        self.assertLess(
            stability["iterations_without_new_claim_blockers"],
            stability["minimum_iterations_before_claim_ceiling_raise"],
        )
        self.assertEqual(
            stability["last_claim_blocker_set_change_discovered_by"],
            ["adversarial", "contract_test"],
        )
        self.assertEqual(
            stability["last_non_blocker_defect_discovered_by"],
            ["domain_guided"],
        )
        self.assertFalse(self.status["ceiling_raise_policy"]["claim_ceiling_raise_permitted"])
        self.assertEqual(
            self.status["ceiling_raise_policy"]["stability_conditions"],
            {
                "minimum_iterations_before_claim_ceiling_raise": stability["minimum_iterations_before_claim_ceiling_raise"],
                "iterations_without_new_claim_blockers": stability["iterations_without_new_claim_blockers"],
            },
        )

    def test_claim_ceiling_has_allowed_and_disallowed_claims(self) -> None:
        ceiling = self.status["claim_ceiling"]
        self.assertTrue(ceiling["allowed_claims"])
        self.assertTrue(ceiling["disallowed_claims"])
        self.assertIn("bounded_completeness_established", ceiling["disallowed_claims"])

    def test_registry_sets_are_closed(self) -> None:
        groups = set(self.status["group_registry"])
        discoveries = set(self.status["discovery_registry"])
        routes = set(self.status["resolution_route_registry"])
        self.assertTrue(groups)
        self.assertTrue(discoveries)
        self.assertTrue(routes)

        for gap in self.status["gap_status"]:
            self.assertIn(gap["group"], groups, gap["gap_id"])
            self.assertIn(gap["preferred_resolution_route"], routes, gap["gap_id"])
            self.assertTrue(gap["discovered_by"], gap["gap_id"])
            for item in gap["discovered_by"]:
                self.assertIn(item, discoveries, gap["gap_id"])

    def test_gap_status_covers_all_known_ledger_gaps_exactly_once(self) -> None:
        self.assertEqual(set(self.status_by_id), set(self.ledger_by_id))

    def test_next_target_resolves_to_existing_gap_and_has_traceability(self) -> None:
        target = self.status["next_target"]
        self.assertIn(target["target_id"], self.ledger_by_id)
        self.assertEqual(target["selected_from_group"], "claim_blocker")
        self.assertEqual(target["selected_from_gap_class"], self.ledger_by_id[target["target_id"]]["gap_class"])
        self.assertTrue(target["selection_reason"].strip())
        self.assertEqual(
            target["selection_basis"],
            [
                "gap_status=open",
                "selected_from_group=claim_blocker",
                "claim_ceiling_raise_permitted=false",
            ],
        )
        self.assertEqual(target["target_status"], "active")
        self.assertEqual(self.status_by_id[target["target_id"]]["group"], "claim_blocker")

    def test_target_transition_policy_is_present_and_traceability_oriented(self) -> None:
        policy = self.status["target_transition_policy"]
        self.assertEqual(
            policy["target_change_requires"],
            [
                "gap_classification_update_or_confirmation",
                "status_revision",
                "documented_change_reason",
            ],
        )
        self.assertEqual(
            policy["allowed_reselection_sources"],
            ["claim_blocker", "newly_discovered_claim_blocker"],
        )
        self.assertEqual(
            policy["forbidden_effects"],
            [
                "implicit_claim_ceiling_raise",
                "implicit_blocker_resolution",
                "implicit_gap_reclassification",
            ],
        )

    def test_ceiling_raise_policy_is_explicit(self) -> None:
        policy = self.status["ceiling_raise_policy"]
        self.assertFalse(policy["claim_ceiling_raise_permitted"])
        self.assertEqual(
            policy["requires"],
            [
                "claim_blockers_resolved_or_formally_excluded",
                "blocker_set_stability_satisfied",
                "status_recomputed",
                "gap_classification_recomputed",
                "all_contract_and_corpus_tests_pass",
            ],
        )
        self.assertEqual(
            policy["forbidden_shortcuts"],
            [
                "target_completion_implies_raise",
                "single_blocker_resolution_implies_raise",
                "manual_claim_wording_upgrade_without_status_update",
            ],
        )

    def test_claim_blockers_match_ledger_blocked_bounded_claims(self) -> None:
        grouped = {
            gap["gap_id"]
            for gap in self.status["gap_status"]
            if gap["group"] == "claim_blocker"
        }
        from_ledger = {
            gap_id
            for gap_id, gap in self.ledger_by_id.items()
            if gap["claim_impact"]["blocks_bounded_claim_v0_1"]
        }
        self.assertEqual(grouped, from_ledger)

    def test_future_scope_items_are_formally_excludable(self) -> None:
        for gap in self.status["gap_status"]:
            if gap["group"] == "future_scope":
                self.assertTrue(
                    self.ledger_by_id[gap["gap_id"]]["claim_impact"]["formally_excludable_in_v0_1"],
                    gap["gap_id"],
                )

    def test_framework_hygiene_items_do_not_block_bounded_claim(self) -> None:
        for gap in self.status["gap_status"]:
            if gap["group"] == "framework_hygiene":
                self.assertFalse(
                    self.ledger_by_id[gap["gap_id"]]["claim_impact"]["blocks_bounded_claim_v0_1"],
                    gap["gap_id"],
                )

    def test_non_blocking_gap_list_matches_non_claim_blockers(self) -> None:
        expected = {
            gap["gap_id"]
            for gap in self.status["gap_status"]
            if gap["group"] != "claim_blocker"
        }
        self.assertEqual(set(self.status["non_blocking_gaps"]), expected)

    def test_blocked_surface_references_known_gap_ids(self) -> None:
        all_gap_ids = set(self.ledger_by_id)
        blocked = set()
        for surface in self.status["blocked_surface"]:
            self.assertTrue(surface["blocker_ids"], surface["surface_id"])
            for gap_id in surface["blocker_ids"]:
                self.assertIn(gap_id, all_gap_ids, surface["surface_id"])
                blocked.add(gap_id)
        self.assertIn("GAP_MULTI_REASON_PRECEDENCE_CANONICALIZATION", blocked)

    def test_excluded_surface_points_only_to_formally_excludable_gaps(self) -> None:
        for item in self.status["excluded_surface"]:
            gap_id = item["gap_id"]
            self.assertIn(gap_id, self.ledger_by_id)
            self.assertTrue(
                self.ledger_by_id[gap_id]["claim_impact"]["formally_excludable_in_v0_1"],
                gap_id,
            )

    def test_evidence_layers_present_include_gap_ledger_and_domain_guided_layers(self) -> None:
        layers = set(self.status["evidence_layers_present"])
        self.assertIn("machine_readable_gap_ledger", layers)
        self.assertIn("executable_gap_ledger_contract", layers)
        self.assertIn("domain_guided_generated_corpus", layers)
        self.assertIn("cc012_negative_verify_corpus", layers)
        self.assertIn("cc012_verify_distribution_analysis", layers)
        self.assertIn("malformed_corpus", layers)

    def test_cc012_distribution_surface_is_observation_not_proof(self) -> None:
        distribution_surface = self.status["cc012_surface_registry"]["active_distribution_surface"]
        self.assertEqual(
            distribution_surface["current_observation"],
            "CC012 behaves as a stable convergence class across all currently observed verify multi-reason outcomes within the V0_1 representable surface",
        )
        self.assertEqual(
            distribution_surface["analysis_role"],
            "empirical_baseline_not_proof_or_invariant",
        )

    def test_open_claim_blockers_prevent_raise(self) -> None:
        open_claim_blockers = [
            gap_id
            for gap_id, gap in self.ledger_by_id.items()
            if gap["status"] == "open" and self.status_by_id[gap_id]["group"] == "claim_blocker"
        ]
        self.assertTrue(open_claim_blockers)
        self.assertFalse(self.status["ceiling_raise_policy"]["claim_ceiling_raise_permitted"])
        self.assertFalse(self.status["bounded_completeness_proven"])


if __name__ == "__main__":
    unittest.main()
