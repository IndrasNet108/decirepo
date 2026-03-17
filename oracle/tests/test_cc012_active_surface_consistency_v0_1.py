#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import load_json_file  # noqa: E402

STATUS_PATH = ROOT / "conformance" / "BOUNDED_COMPLETENESS_STATUS_V0_1.json"
PROTOCOL_DOC_PATH = ROOT / "DECIREPO_PROTOCOL_CONFORMANCE_V0_1.md"
PACKAGE_JSON_PATH = ROOT / "package.json"
VALIDATE_ALL_PATH = ROOT / "scripts" / "validate_all.sh"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "protocol-ci.yml"
SYNC_GUARD_PATH = ROOT / "scripts" / "check_protocol_sync.sh"
ACTIVE_GENERATOR_PATHS = [
    ROOT / "oracle" / "gen_cc012_negative_verify_corpus_v0_1.py",
    ROOT / "oracle" / "gen_precedence_adversarial_corpus_v0_1.py",
    ROOT / "oracle" / "gen_cc012_verify_distribution_v0_1.py",
    ROOT / "oracle" / "corpus_cases_v0_1.py",
]


class CC012ActiveSurfaceConsistencyV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.status = load_json_file(STATUS_PATH)
        cls.protocol_doc = PROTOCOL_DOC_PATH.read_text(encoding="utf-8")
        cls.package_scripts = json.loads(PACKAGE_JSON_PATH.read_text(encoding="utf-8"))["scripts"]
        cls.validate_all = VALIDATE_ALL_PATH.read_text(encoding="utf-8")
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.sync_guard = SYNC_GUARD_PATH.read_text(encoding="utf-8")
        cls.active_generator_sources = {
            path.name: path.read_text(encoding="utf-8")
            for path in ACTIVE_GENERATOR_PATHS
        }

    def test_status_revision_and_registry_are_present(self) -> None:
        self.assertEqual(self.status["status_revision"]["revision_id"], "status-v0.1-r11")
        registry = self.status["cc012_surface_registry"]
        self.assertEqual(registry["active_negative_surface"]["artifact_id"], "conformance/cc012_negative_verify_corpus_v0_1/manifest.json")
        self.assertEqual(registry["active_positive_surface"]["artifact_id"], "conformance/precedence_adversarial_corpus_v0_1/manifest.json")
        self.assertEqual(registry["active_distribution_surface"]["artifact_id"], "conformance/cc012_verify_distribution_v0_1.json")
        self.assertEqual(registry["superseded_legacy_surface"]["artifact_id"], "conformance/cc012_negative_corpus_v0_1")
        self.assertTrue(registry["active_negative_surface"]["active"])
        self.assertTrue(registry["active_positive_surface"]["active"])
        self.assertTrue(registry["active_distribution_surface"]["active"])
        self.assertFalse(registry["superseded_legacy_surface"]["active"])
        self.assertTrue(registry["superseded_legacy_surface"]["excluded_from_claim_surface"])
        self.assertEqual(
            registry["active_negative_surface"]["claim_strict_description"],
            "verify-side non-overcapture boundary for currently representable non-CC012 verify-adjacent surfaces in V0_1",
        )
        self.assertEqual(
            registry["active_negative_surface"]["working_layer_name"],
            "verify-side CC012 negative boundary layer",
        )
        self.assertEqual(
            registry["active_distribution_surface"]["working_layer_name"],
            "CC012 verify distribution layer",
        )
        self.assertEqual(
            registry["active_distribution_surface"]["current_observation"],
            "CC012 behaves as a stable convergence class across all currently observed verify multi-reason outcomes within the V0_1 representable surface",
        )
        self.assertEqual(
            registry["active_distribution_surface"]["analysis_role"],
            "empirical_baseline_not_proof_or_invariant",
        )

    def test_active_evidence_layers_do_not_include_legacy_cc012_surface(self) -> None:
        layers = set(self.status["evidence_layers_present"])
        self.assertIn("precedence_adversarial_corpus", layers)
        self.assertIn("cc012_negative_verify_corpus", layers)
        self.assertIn("cc012_verify_distribution_analysis", layers)
        self.assertNotIn("cc012_negative_corpus", layers)
        self.assertNotIn("cc012_negative_capture_corpus", layers)

    def test_protocol_doc_uses_active_cc012_surface_and_marks_legacy_as_superseded(self) -> None:
        registry = self.status["cc012_surface_registry"]
        self.assertIn(registry["active_positive_surface"]["artifact_id"], self.protocol_doc)
        self.assertIn(registry["active_negative_surface"]["artifact_id"], self.protocol_doc)
        self.assertIn(registry["active_distribution_surface"]["artifact_id"], self.protocol_doc)
        self.assertIn(registry["active_negative_surface"]["claim_strict_description"], self.protocol_doc)
        self.assertIn(registry["active_negative_surface"]["working_layer_name"], self.protocol_doc)
        self.assertIn(registry["active_distribution_surface"]["current_observation"], self.protocol_doc)
        self.assertIn("supersedes the legacy exploratory `conformance/cc012_negative_corpus_v0_1/` layer", self.protocol_doc)
        self.assertIn("excluded from the active claim surface", self.protocol_doc)
        self.assertIn("neither a proof object nor an invariant", self.protocol_doc)
        self.assertIn("cluster existence alone is not a split signal", self.protocol_doc)

    def test_active_entrypoints_do_not_call_legacy_cc012_generator_or_tests(self) -> None:
        active_texts = [
            self.package_scripts["oracle:test:v0_1"],
            self.package_scripts["oracle:gen-cc012-negative:v0_1"],
            self.package_scripts["oracle:gen-cc012-distribution:v0_1"],
            self.validate_all,
            self.workflow,
            self.sync_guard,
        ]
        forbidden = [
            "gen_cc012_negative_corpus_v0_1.py",
            "test_cc012_negative_capture_v0_1.py",
            "conformance/cc012_negative_corpus_v0_1",
            "cc012_negative_capture_corpus",
        ]
        joined = "\n".join(active_texts)
        for token in forbidden:
            self.assertNotIn(token, joined, token)

    def test_active_generators_and_utilities_do_not_reference_superseded_cc012_surface(self) -> None:
        joined = "\n".join(self.active_generator_sources.values())
        forbidden = [
            "gen_cc012_negative_corpus_v0_1",
            "cc012_negative_corpus_v0_1",
            "test_cc012_negative_capture_v0_1",
            "cc012_negative_capture_corpus",
        ]
        for token in forbidden:
            self.assertNotIn(token, joined, token)

    def test_active_entrypoints_include_current_cc012_surface(self) -> None:
        registry = self.status["cc012_surface_registry"]
        joined = "\n".join(
            [
                self.package_scripts["oracle:test:v0_1"],
                self.package_scripts["oracle:gen-cc012-negative:v0_1"],
                self.package_scripts["oracle:gen-cc012-distribution:v0_1"],
                self.validate_all,
                self.workflow,
                self.sync_guard,
            ]
        )
        required = [
            "gen_precedence_adversarial_corpus_v0_1.py",
            "gen_cc012_negative_verify_corpus_v0_1.py",
            "gen_cc012_verify_distribution_v0_1.py",
            "test_cc012_negative_verify_capture_v0_1.py",
            "test_cc012_negative_verify_composition_v0_1.py",
            "test_cc012_verify_distribution_v0_1.py",
            registry["active_positive_surface"]["artifact_id"].replace("/manifest.json", ""),
            registry["active_negative_surface"]["artifact_id"].replace("/manifest.json", ""),
            registry["active_distribution_surface"]["artifact_id"],
        ]
        for token in required:
            self.assertIn(token, joined, token)


if __name__ == "__main__":
    unittest.main()
