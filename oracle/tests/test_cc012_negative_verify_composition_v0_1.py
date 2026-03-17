#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import load_json_file  # noqa: E402
from gen_cc012_negative_verify_corpus_v0_1 import main as generate_negative_verify_corpus  # noqa: E402

MANIFEST_PATH = ROOT / "conformance" / "cc012_negative_verify_corpus_v0_1" / "manifest.json"
MATRIX_PATH = ROOT / "conformance" / "CASE_CLASS_MATRIX_V0_1.json"
PRECEDENCE_MANIFEST_PATH = ROOT / "conformance" / "precedence_adversarial_corpus_v0_1" / "manifest.json"


class CC012NegativeVerifyCompositionV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        generate_negative_verify_corpus()
        cls.manifest = load_json_file(MANIFEST_PATH)
        cls.matrix = load_json_file(MATRIX_PATH)
        cls.precedence_manifest = load_json_file(PRECEDENCE_MANIFEST_PATH)
        cls.class_ids = {cls_def["class_id"] for cls_def in cls.matrix["classes"]}

    def test_manifest_identity_is_fixed(self) -> None:
        self.assertEqual(self.manifest["profile_id"], "V0_1")
        self.assertEqual(self.manifest["corpus_id"], "cc012_negative_verify_corpus_v0_1")
        self.assertEqual(
            self.manifest["provenance_mode"],
            "manual_adversarial_negative_capture_verify_only",
        )
        self.assertEqual(len(self.manifest["cases"]), 8)

    def test_cases_are_verify_only_and_class_resolved(self) -> None:
        forbidden_tokens = {"PLACEHOLDER", "TODO", "EXPECTED_NEIGHBOR_CLASS"}
        case_ids: list[str] = []
        for case in self.manifest["cases"]:
            case_ids.append(case["case_id"])
            self.assertEqual(case["command"], "verify", case["case_id"])
            self.assertEqual(case["must_not_select_class"], "CC012_MULTI_REASON_PRECEDENCE", case["case_id"])
            self.assertIn(case["expected_selected_class"], self.class_ids, case["case_id"])
            self.assertTrue(case["cc012_negative_mode"].strip(), case["case_id"])
            self.assertTrue(case["input_shape_profile"].strip(), case["case_id"])
            joined = " ".join(
                [
                    case["case_id"],
                    case["expected_selected_class"],
                    case["must_not_select_class"],
                    case["cc012_negative_mode"],
                ]
            )
            for token in forbidden_tokens:
                self.assertNotIn(token, joined, case["case_id"])
        self.assertEqual(len(case_ids), len(set(case_ids)))

    def test_negative_capture_contract_distribution_is_satisfied(self) -> None:
        contract = self.manifest["negative_capture_contract"]
        bucket_counts: dict[str, int] = {}
        mode_counts: dict[str, int] = {}
        shape_counts: dict[str, int] = {}
        for case in self.manifest["cases"]:
            bucket_counts[case["expected_bucket"]] = bucket_counts.get(case["expected_bucket"], 0) + 1
            mode_counts[case["cc012_negative_mode"]] = mode_counts.get(case["cc012_negative_mode"], 0) + 1
            shape_counts[case["input_shape_profile"]] = shape_counts.get(case["input_shape_profile"], 0) + 1
        for bucket, minimum in contract["bucket_minima"].items():
            self.assertGreaterEqual(bucket_counts.get(bucket, 0), minimum, bucket)
        for mode, minimum in contract["mode_minima"].items():
            self.assertGreaterEqual(mode_counts.get(mode, 0), minimum, mode)
        for profile, minimum in contract["input_shape_profile_minima"].items():
            self.assertGreaterEqual(shape_counts.get(profile, 0), minimum, profile)

    def test_expected_multiple_reason_policy_is_explicit_and_honored(self) -> None:
        contract = self.manifest["negative_capture_contract"]["expected_multiple_reason_codes_policy"]
        self.assertTrue(contract["all_cases_must_be_false"])
        self.assertTrue(contract["reason"].strip())
        for case in self.manifest["cases"]:
            self.assertFalse(case["expected_multiple_reason_codes"], case["case_id"])

    def test_excluded_negative_modes_are_explicit(self) -> None:
        excluded = {
            entry["mode"]: entry["reason"]
            for entry in self.manifest["negative_capture_contract"]["excluded_negative_modes"]
        }
        self.assertIn("multi_reason_non_precedence", excluded)
        self.assertIn("same_reason_multipath", excluded)
        self.assertTrue(excluded["multi_reason_non_precedence"].strip())
        self.assertTrue(excluded["same_reason_multipath"].strip())

    def test_verify_only_negative_corpus_is_paired_with_positive_precedence_surface(self) -> None:
        self.assertEqual(
            self.manifest["negative_capture_contract"]["paired_positive_corpus_manifest"],
            "conformance/precedence_adversarial_corpus_v0_1/manifest.json",
        )
        positive_verify_cases = [
            case
            for case in self.precedence_manifest["cases"]
            if case["command"] == "verify"
            and case["expected_selected_class"] == "CC012_MULTI_REASON_PRECEDENCE"
        ]
        self.assertGreaterEqual(len(positive_verify_cases), 2)


if __name__ == "__main__":
    unittest.main()
