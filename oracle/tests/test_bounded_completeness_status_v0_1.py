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
        self.assertIn("malformed_corpus", layers)


if __name__ == "__main__":
    unittest.main()
