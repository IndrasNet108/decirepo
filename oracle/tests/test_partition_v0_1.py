#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file  # noqa: E402
from gen_corpus_v0_1 import main as generate_corpus  # noqa: E402

CONFORMANCE_DIR = ROOT / "conformance"
MANIFEST_PATH = CONFORMANCE_DIR / "generated_corpus_v0_1" / "manifest.json"
DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"


class PartitionV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        generate_corpus()
        cls.manifest = load_json_file(MANIFEST_PATH)
        cls.domain = load_json_file(DOMAIN_PATH)
        cls.kernel = load_json_file(KERNEL_PATH)
        cls.matrix = load_json_file(MATRIX_PATH)
        cls.classes = {item["class_id"]: item for item in cls.matrix["classes"]}

    def test_manifest_exists_and_is_v0_1(self) -> None:
        self.assertEqual(self.manifest["manifest_version"], "0.1")
        self.assertEqual(self.manifest["profile_id"], "V0_1")
        self.assertEqual(self.manifest["corpus_id"], "generated_corpus_v0_1")
        self.assertEqual(self.manifest["provenance_mode"], "class_guided")

    def test_every_declared_class_is_covered(self) -> None:
        declared = {item["class_id"] for item in self.matrix["classes"]}
        covered = {entry["source_class_id"] for entry in self.manifest["entries"]}
        self.assertEqual(covered, declared)

    def test_entry_ids_and_artifact_paths_are_unique(self) -> None:
        ids = [entry["entry_id"] for entry in self.manifest["entries"]]
        paths = [entry["artifact_path"] for entry in self.manifest["entries"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(paths), len(set(paths)))

    def test_selected_class_is_member_of_match_set(self) -> None:
        for entry in self.manifest["entries"]:
            self.assertIn(entry["expected"]["selected_class"], entry["expected"]["matched_classes"])

    def test_partition_mode_is_respected(self) -> None:
        for entry in self.manifest["entries"]:
            matched_classes = entry["expected"]["matched_classes"]
            partition_mode = entry["expected"]["partition_mode"]
            if partition_mode == "exclusive":
                self.assertEqual(len(matched_classes), 1, entry["entry_id"])
            elif partition_mode == "ordered_precedence_chain":
                self.assertGreaterEqual(len(matched_classes), 1, entry["entry_id"])
            else:
                self.fail(f"unexpected partition_mode for {entry['entry_id']}: {partition_mode}")

    def test_source_bucket_matches_class_matrix(self) -> None:
        for entry in self.manifest["entries"]:
            class_def = self.classes[entry["source_class_id"]]
            self.assertEqual(entry["source_bucket"], class_def["class_bucket"])

    def test_oracle_agrees_with_manifest(self) -> None:
        for entry in self.manifest["entries"]:
            artifact = load_json_file(ROOT / entry["artifact_path"])
            result = evaluate_corpus_entry(entry["command"], artifact, self.kernel, self.domain, self.matrix)

            self.assertEqual(result["in_domain"], entry["expected"]["in_domain"], entry["entry_id"])
            self.assertEqual(result["matched_classes"], entry["expected"]["matched_classes"], entry["entry_id"])
            self.assertEqual(result["selected_class"], entry["expected"]["selected_class"], entry["entry_id"])
            self.assertEqual(result["partition_mode"], entry["expected"]["partition_mode"], entry["entry_id"])
            self.assertEqual(result["verdict"], entry["expected"]["expected_verdict"], entry["entry_id"])
            self.assertEqual(result["reason_codes"], entry["expected"]["expected_reason_codes"], entry["entry_id"])

            oracle_expectation = entry["oracle_expectation"]
            if oracle_expectation["artifact_id_required"]:
                self.assertIsInstance(result["artifact_id"], str, entry["entry_id"])
                self.assertEqual(len(result["artifact_id"]), 64, entry["entry_id"])

            if oracle_expectation["normalized_result_required"]:
                self.assertIsInstance(result["normalized_result"], dict, entry["entry_id"])
            else:
                self.assertIsNone(result["normalized_result"], entry["entry_id"])

            if oracle_expectation["canonical_result_hex_required"]:
                self.assertIsInstance(result["canonical_result_hex"], str, entry["entry_id"])
                self.assertGreater(len(result["canonical_result_hex"]), 0, entry["entry_id"])
            else:
                self.assertIsNone(result["canonical_result_hex"], entry["entry_id"])

    def test_reason_codes_follow_declared_total_order(self) -> None:
        ordered_codes = self.domain["normalized_result"]["reason_code_ordering"]["ordered_codes"]
        positions = {code: idx for idx, code in enumerate(ordered_codes)}
        for entry in self.manifest["entries"]:
            artifact = load_json_file(ROOT / entry["artifact_path"])
            result = evaluate_corpus_entry(entry["command"], artifact, self.kernel, self.domain, self.matrix)
            codes = result["reason_codes"]
            self.assertEqual(codes, sorted(codes, key=lambda code: positions[code]), entry["entry_id"])

    def test_coverage_summary_matches_entries(self) -> None:
        entries = self.manifest["entries"]
        summary = self.manifest["coverage_summary"]
        in_domain_total = sum(1 for entry in entries if entry["expected"]["in_domain"])
        out_of_domain_total = len(entries) - in_domain_total
        precedence_total = sum(1 for entry in entries if entry["expected"]["partition_mode"] == "ordered_precedence_chain")

        self.assertEqual(summary["declared_classes_total"], len(self.matrix["classes"]))
        self.assertEqual(summary["declared_classes_covered"], len({entry["source_class_id"] for entry in entries}))
        self.assertEqual(summary["generated_inputs_total"], len(entries))
        self.assertEqual(summary["generated_inputs_in_domain"], in_domain_total)
        self.assertEqual(summary["generated_inputs_out_of_domain"], out_of_domain_total)
        self.assertEqual(summary["generated_inputs_with_declared_precedence_chain"], precedence_total)
        self.assertEqual(summary["generated_inputs_ambiguous"], 0)
        self.assertEqual(summary["generated_inputs_unclassified"], 0)


if __name__ == "__main__":
    unittest.main()
