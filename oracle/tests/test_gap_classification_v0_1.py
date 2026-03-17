#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import load_json_file  # noqa: E402

GAP_PATH = ROOT / "conformance" / "GAP_CLASSIFICATION_V0_1.json"
MATRIX_PATH = ROOT / "conformance" / "CASE_CLASS_MATRIX_V0_1.json"
DOMAIN_PATH = ROOT / "conformance" / "DOMAIN_PROFILE_V0_1.json"


class GapClassificationV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = load_json_file(GAP_PATH)
        cls.matrix = load_json_file(MATRIX_PATH)
        cls.domain = load_json_file(DOMAIN_PATH)
        cls.classes = {item["class_id"]: item for item in cls.matrix["classes"]}
        cls.gaps = cls.ledger["gaps"]
        cls.gaps_by_id = {item["gap_id"]: item for item in cls.gaps}

    def test_top_level_metadata_is_pinned(self) -> None:
        self.assertEqual(self.ledger["profile_id"], "V0_1")
        self.assertEqual(self.ledger["protocol_specification"], "v0.2")
        self.assertEqual(self.ledger["protocol_semantics"], "v0.1")
        self.assertIn(self.ledger["status"], {"draft", "sealed"})

    def test_gap_class_and_block_type_registries_are_closed(self) -> None:
        declared_gap_classes = set(self.ledger["gap_classes"])
        declared_block_types = set(self.ledger["block_types"])
        self.assertTrue(declared_gap_classes)
        self.assertTrue(declared_block_types)

        for gap in self.gaps:
            self.assertIn(gap["gap_class"], declared_gap_classes, gap["gap_id"])
            self.assertIsInstance(gap["blocks"], list, gap["gap_id"])
            self.assertTrue(gap["blocks"], gap["gap_id"])
            self.assertIsInstance(gap["related_class_ids"], list, gap["gap_id"])
            self.assertIn(gap["status"], {"open", "resolved", "excluded"}, gap["gap_id"])
            for block in gap["blocks"]:
                self.assertIn(block, declared_block_types, gap["gap_id"])

    def test_every_matrix_gap_class_is_mapped(self) -> None:
        expected_gap_classes = {
            item["class_id"]
            for item in self.matrix["classes"]
            if item["proof_status"] in {"prose_only_gap", "registry_only_gap", "open_gap"}
        }
        mapped_gap_classes = {
            class_id for gap in self.gaps for class_id in gap["related_class_ids"]
        }
        self.assertEqual(mapped_gap_classes, expected_gap_classes)

    def test_related_class_ids_resolve_to_known_gap_classes(self) -> None:
        for gap in self.gaps:
            for class_id in gap["related_class_ids"]:
                self.assertIn(class_id, self.classes, gap["gap_id"])
                self.assertIn(
                    self.classes[class_id]["proof_status"],
                    {"prose_only_gap", "registry_only_gap", "open_gap"},
                    gap["gap_id"],
                )

    def test_gap_class_matches_matrix_gap_nature(self) -> None:
        expected_by_proof_status = {
            "prose_only_gap": "scope_boundary_gap",
            "registry_only_gap": "registry_hygiene_gap",
        }
        for gap in self.gaps:
            for class_id in gap["related_class_ids"]:
                proof_status = self.classes[class_id]["proof_status"]
                expected = expected_by_proof_status.get(proof_status)
                if expected is not None:
                    self.assertEqual(gap["gap_class"], expected, gap["gap_id"])

    def test_harness_only_gap_maps_to_harness_boundary(self) -> None:
        for gap in self.gaps:
            related = [self.classes[class_id] for class_id in gap["related_class_ids"]]
            if any(item["class_bucket"] == "harness_only_gap" for item in related):
                self.assertEqual(gap["gap_class"], "harness_boundary_gap", gap["gap_id"])

    def test_registry_hygiene_gaps_do_not_block_bounded_completeness(self) -> None:
        for gap in self.gaps:
            if gap["gap_class"] == "registry_hygiene_gap":
                self.assertNotIn("bounded_completeness", gap["blocks"], gap["gap_id"])

    def test_multi_reason_precedence_gap_blocks_bounded_completeness(self) -> None:
        gap = self.gaps_by_id["GAP_MULTI_REASON_PRECEDENCE_CANONICALIZATION"]
        self.assertIn("CC012_MULTI_REASON_PRECEDENCE", gap["related_class_ids"])
        self.assertEqual(gap["gap_class"], "semantic_blocker")
        self.assertIn("bounded_completeness", gap["blocks"])

    def test_evidence_method_gaps_are_classless(self) -> None:
        for gap in self.gaps:
            if gap["gap_class"] == "evidence_method_gap":
                self.assertEqual(gap["related_class_ids"], [], gap["gap_id"])

    def test_domain_open_gaps_are_covered_by_gap_ledger(self) -> None:
        gap_ids = set(self.gaps_by_id)
        self.assertIn("GAP_CONFORMANCE_ERROR_BOUNDARY", gap_ids)
        self.assertIn("GAP_VERIFY_WITHOUT_REBUILD_SOURCE_SCOPE", gap_ids)
        self.assertIn("GAP_MULTI_REASON_PRECEDENCE_CANONICALIZATION", gap_ids)
        self.assertIn("GAP_ARTIFACT_HASH_INVALID_ANCHOR", gap_ids)
        self.assertIn("GAP_VALIDATOR_RESULT_INVALID_ANCHOR", gap_ids)
        self.assertIn("GAP_REBUILD_RESULT_INVALID_ANCHOR", gap_ids)
        self.assertEqual(len(self.domain["open_gaps"]), 4)


if __name__ == "__main__":
    unittest.main()
