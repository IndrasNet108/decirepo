#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import evaluate_corpus_entry, load_json_file  # noqa: E402
from gen_adversarial_corpus_v0_1 import main as generate_adversarial_corpus  # noqa: E402
from gen_boundary_corpus_v0_1 import main as generate_boundary_corpus  # noqa: E402

CONFORMANCE_DIR = ROOT / "conformance"
DOMAIN_PATH = CONFORMANCE_DIR / "DOMAIN_PROFILE_V0_1.json"
KERNEL_PATH = CONFORMANCE_DIR / "SEMANTICS_KERNEL_V0_1.json"
MATRIX_PATH = CONFORMANCE_DIR / "CASE_CLASS_MATRIX_V0_1.json"
BOUNDARY_MANIFEST = CONFORMANCE_DIR / "boundary_corpus_v0_1" / "manifest.json"
ADVERSARIAL_MANIFEST = CONFORMANCE_DIR / "adversarial_corpus_v0_1" / "manifest.json"


def coarse_bucket_for_case(command: str, artifact: object, domain: dict) -> str:
    supported_commands = set(domain["verification_commands"])
    if command not in supported_commands:
        return "harness_only_gap"
    if not isinstance(artifact, dict):
        return "malformed"
    if command in {"verify", "validate"} and "rebuild_source" not in artifact:
        return "out_of_scope"
    return "in_domain"


class BoundaryAdversarialV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        generate_boundary_corpus()
        generate_adversarial_corpus()
        cls.domain = load_json_file(DOMAIN_PATH)
        cls.kernel = load_json_file(KERNEL_PATH)
        cls.matrix = load_json_file(MATRIX_PATH)
        cls.manifests = [
            load_json_file(BOUNDARY_MANIFEST),
            load_json_file(ADVERSARIAL_MANIFEST),
        ]

    def test_manifests_exist(self) -> None:
        corpus_ids = {manifest["corpus_id"] for manifest in self.manifests}
        self.assertEqual(corpus_ids, {"boundary_corpus_v0_1", "adversarial_corpus_v0_1"})
        modes = {manifest["corpus_id"]: manifest["provenance_mode"] for manifest in self.manifests}
        self.assertEqual(modes["boundary_corpus_v0_1"], "manual_boundary")
        self.assertEqual(modes["adversarial_corpus_v0_1"], "manual_adversarial")

    def test_bucket_sanity_and_determinism(self) -> None:
        for manifest in self.manifests:
            for case in manifest["cases"]:
                artifact = load_json_file(ROOT / case["artifact_path"])
                coarse_bucket = coarse_bucket_for_case(case["command"], artifact, self.domain)
                result1 = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)
                result2 = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)

                self.assertEqual(result1, result2, case["case_id"])
                self.assertFalse(result1["predicate_error"], case["case_id"])
                self.assertEqual(result1["class_bucket"], case["expected_bucket"], case["case_id"])

                if coarse_bucket == "in_domain":
                    self.assertTrue(result1["class_bucket"].startswith("in_domain_"), case["case_id"])
                else:
                    self.assertEqual(result1["class_bucket"], coarse_bucket, case["case_id"])

    def test_expected_class_verdict_and_reason_codes(self) -> None:
        for manifest in self.manifests:
            for case in manifest["cases"]:
                artifact = load_json_file(ROOT / case["artifact_path"])
                result = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)

                if case["expected_class"] is not None:
                    self.assertEqual(result["selected_class"], case["expected_class"], case["case_id"])
                self.assertEqual(result["verdict"], case["expected_verdict"], case["case_id"])
                self.assertEqual(result["reason_codes"], case["expected_reason_codes"], case["case_id"])

    def test_adversarial_cases_are_not_silently_valid(self) -> None:
        adversarial = next(manifest for manifest in self.manifests if manifest["corpus_id"] == "adversarial_corpus_v0_1")
        for case in adversarial["cases"]:
            artifact = load_json_file(ROOT / case["artifact_path"])
            result = evaluate_corpus_entry(case["command"], artifact, self.kernel, self.domain, self.matrix)
            self.assertNotEqual(result["class_bucket"], "in_domain_valid", case["case_id"])


if __name__ == "__main__":
    unittest.main()
