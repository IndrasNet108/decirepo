#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import run_profile  # noqa: E402


class OracleVectorsV01Test(unittest.TestCase):
    def test_oracle_reproduces_published_vectors(self) -> None:
        report = run_profile(
            ROOT / "conformance" / "v0_1",
            ROOT / "conformance" / "SEMANTICS_KERNEL_V0_1.json",
            ROOT / "conformance" / "DOMAIN_PROFILE_V0_1.json",
        )
        self.assertEqual(report["overall_verdict"], "PASS")
        self.assertEqual(report["vectors_total"], 7)
        self.assertEqual(report["vectors_passed"], 7)
        self.assertEqual(report["vectors_failed"], 0)
        for row in report["results"]:
            self.assertEqual(row["verdict"], "PASS", row["vector_id"])
            self.assertTrue(row["identity_check"], row["vector_id"])
            self.assertTrue(row["verification_check"], row["vector_id"])
            self.assertTrue(row["result_bytes_check"], row["vector_id"])

    def test_report_shape_matches_published_validator_contract(self) -> None:
        report = run_profile(
            ROOT / "conformance" / "v0_1",
            ROOT / "conformance" / "SEMANTICS_KERNEL_V0_1.json",
            ROOT / "conformance" / "DOMAIN_PROFILE_V0_1.json",
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
            Path(tmp.name).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            tmp_path = Path(tmp.name)
        try:
            validator = ROOT / ".." / "decirepo_second_impl_dry_run_v0_1" / "src" / "validate_report_shape.py"
            # Fallback to local contract assertions if the external helper is absent.
            if validator.exists():
                import subprocess
                subprocess.run([sys.executable, str(validator), str(tmp_path)], check=True)
            else:
                self.assertEqual(report["report_schema"], "decirepo-conformance-report-v0.1")
                self.assertEqual(report["conformance_profile"], "V0_1")
                self.assertEqual(report["protocol_specification"], "v0.2")
                self.assertEqual(report["protocol_semantics"], "v0.1")
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
