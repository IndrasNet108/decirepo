#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'oracle'))

from corpus_cases_v0_1 import (  # noqa: E402
    invalid_artifact_hash_artifact,
    invalid_rebuild_result_artifact,
    invalid_validator_result_artifact,
    rebuild_hash_mismatch_artifact,
)
from decirepo_oracle_v0_1 import applicable_rules, evaluate_corpus_entry, load_json_file  # noqa: E402
from gen_cc012_negative_verify_corpus_v0_1 import main as generate_negative_verify_corpus  # noqa: E402

CONFORMANCE_DIR = ROOT / 'conformance'
DOMAIN_PATH = CONFORMANCE_DIR / 'DOMAIN_PROFILE_V0_1.json'
KERNEL_PATH = CONFORMANCE_DIR / 'SEMANTICS_KERNEL_V0_1.json'
MATRIX_PATH = CONFORMANCE_DIR / 'CASE_CLASS_MATRIX_V0_1.json'
MANIFEST_PATH = CONFORMANCE_DIR / 'cc012_negative_verify_corpus_v0_1' / 'manifest.json'
PRECEDENCE_MANIFEST_PATH = CONFORMANCE_DIR / 'precedence_adversarial_corpus_v0_1' / 'manifest.json'


def rule_order_variants(command: str, kernel: dict) -> list[list[str] | None]:
    rules = applicable_rules(command, kernel, rule_statuses={'published', 'registry_only_gap'})
    rule_ids = [rule['rule_id'] for rule in rules]
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


class CC012NegativeVerifyCaptureV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        generate_negative_verify_corpus()
        cls.domain = load_json_file(DOMAIN_PATH)
        cls.kernel = load_json_file(KERNEL_PATH)
        cls.matrix = load_json_file(MATRIX_PATH)
        cls.manifest = load_json_file(MANIFEST_PATH)
        cls.precedence_manifest = load_json_file(PRECEDENCE_MANIFEST_PATH)
        cls.case_by_id = {case['case_id']: case for case in cls.manifest['cases']}
        cls.class_ids = {cls_def['class_id'] for cls_def in cls.matrix['classes']}

    def test_manifest_identity_and_verify_only_distribution(self) -> None:
        self.assertEqual(self.manifest['corpus_id'], 'cc012_negative_verify_corpus_v0_1')
        self.assertEqual(self.manifest['provenance_mode'], 'manual_adversarial_negative_capture_verify_only')
        self.assertEqual(len(self.manifest['cases']), 8)
        contract = self.manifest['negative_capture_contract']
        self.assertTrue(contract['verify_only'])
        self.assertEqual(contract['must_not_select_class'], 'CC012_MULTI_REASON_PRECEDENCE')
        self.assertEqual(
            contract['paired_positive_corpus_manifest'],
            'conformance/precedence_adversarial_corpus_v0_1/manifest.json',
        )
        bucket_counts: dict[str, int] = {}
        mode_counts: dict[str, int] = {}
        shape_counts: dict[str, int] = {}
        for case in self.manifest['cases']:
            self.assertEqual(case['command'], 'verify', case['case_id'])
            self.assertIn(case['expected_selected_class'], self.class_ids, case['case_id'])
            self.assertEqual(case['must_not_select_class'], 'CC012_MULTI_REASON_PRECEDENCE', case['case_id'])
            self.assertTrue(case['cc012_negative_mode'].strip(), case['case_id'])
            self.assertTrue(case['input_shape_profile'].strip(), case['case_id'])
            self.assertFalse(case['expected_multiple_reason_codes'], case['case_id'])
            bucket_counts[case['expected_bucket']] = bucket_counts.get(case['expected_bucket'], 0) + 1
            mode_counts[case['cc012_negative_mode']] = mode_counts.get(case['cc012_negative_mode'], 0) + 1
            shape_counts[case['input_shape_profile']] = shape_counts.get(case['input_shape_profile'], 0) + 1
        for bucket, minimum in contract['bucket_minima'].items():
            self.assertGreaterEqual(bucket_counts.get(bucket, 0), minimum, bucket)
        for mode, minimum in contract['mode_minima'].items():
            self.assertGreaterEqual(mode_counts.get(mode, 0), minimum, mode)
        for profile, minimum in contract['input_shape_profile_minima'].items():
            self.assertGreaterEqual(shape_counts.get(profile, 0), minimum, profile)

    def test_manifest_declares_model_constraints_and_positive_pairing(self) -> None:
        contract = self.manifest['negative_capture_contract']
        self.assertTrue(contract['expected_multiple_reason_codes_policy']['all_cases_must_be_false'])
        excluded = {row['mode']: row['reason'] for row in contract['excluded_negative_modes']}
        self.assertIn('multi_reason_non_precedence', excluded)
        self.assertIn('same_reason_multipath', excluded)
        self.assertTrue(excluded['multi_reason_non_precedence'].strip())
        self.assertTrue(excluded['same_reason_multipath'].strip())
        paired_cases = [
            case for case in self.precedence_manifest['cases']
            if case['command'] == 'verify' and case['expected_selected_class'] == 'CC012_MULTI_REASON_PRECEDENCE'
        ]
        self.assertGreaterEqual(len(paired_cases), 2)

    def test_verify_only_negative_cases_do_not_select_cc012(self) -> None:
        for case in self.manifest['cases']:
            artifact = load_json_file(ROOT / case['artifact_path'])
            result = evaluate_corpus_entry('verify', artifact, self.kernel, self.domain, self.matrix)
            self.assertEqual(result['class_bucket'], case['expected_bucket'], case['case_id'])
            self.assertEqual(result['selected_class'], case['expected_selected_class'], case['case_id'])
            self.assertNotEqual(result['selected_class'], 'CC012_MULTI_REASON_PRECEDENCE', case['case_id'])
            self.assertEqual(result['multiple_reason_codes'], case['expected_multiple_reason_codes'], case['case_id'])
            self.assertGreaterEqual(result['triggered_rule_count'], case['expected_triggered_rule_count_min'], case['case_id'])
            self.assertEqual(result['normalized_reason_codes'], case['expected_normalized_reason_codes'], case['case_id'])

    def test_verify_only_negative_cases_are_perturbation_safe(self) -> None:
        for case in self.manifest['cases']:
            artifact = load_json_file(ROOT / case['artifact_path'])
            baseline = evaluate_corpus_entry('verify', artifact, self.kernel, self.domain, self.matrix)
            for variant in rule_order_variants('verify', self.kernel):
                perturbed = evaluate_corpus_entry(
                    'verify',
                    artifact,
                    self.kernel,
                    self.domain,
                    self.matrix,
                    rule_id_order_override=variant,
                )
                self.assertEqual(perturbed['selected_class'], baseline['selected_class'], case['case_id'])
                self.assertNotEqual(perturbed['selected_class'], 'CC012_MULTI_REASON_PRECEDENCE', case['case_id'])
                self.assertEqual(perturbed['matched_classes'], baseline['matched_classes'], case['case_id'])
                self.assertEqual(perturbed['normalized_reason_codes'], baseline['normalized_reason_codes'], case['case_id'])
                self.assertEqual(perturbed['canonical_result_hex'], baseline['canonical_result_hex'], case['case_id'])

    def test_verify_multi_reason_cases_map_to_positive_precedence_surface(self) -> None:
        positive_cases = [
            invalid_artifact_hash_artifact() | {'validator_result': 'UNKNOWN'},
            rebuild_hash_mismatch_artifact() | {'schema_version': 'dlx-artifact-v9.9'},
        ]
        for artifact in positive_cases:
            result = evaluate_corpus_entry('verify', artifact, self.kernel, self.domain, self.matrix)
            self.assertTrue(result['multiple_reason_codes'])
            self.assertEqual(result['selected_class'], 'CC012_MULTI_REASON_PRECEDENCE')

    def test_layout_negative_equivalence_is_stable(self) -> None:
        for case in self.manifest['cases']:
            counterpart_id = case.get('must_match_selected_class_with')
            if not counterpart_id:
                continue
            counterpart_case = self.case_by_id[counterpart_id]
            artifact = load_json_file(ROOT / case['artifact_path'])
            counterpart_artifact = load_json_file(ROOT / counterpart_case['artifact_path'])
            result = evaluate_corpus_entry('verify', artifact, self.kernel, self.domain, self.matrix)
            counterpart = evaluate_corpus_entry('verify', counterpart_artifact, self.kernel, self.domain, self.matrix)
            self.assertEqual(result['selected_class'], counterpart['selected_class'], case['case_id'])
            self.assertNotEqual(result['selected_class'], 'CC012_MULTI_REASON_PRECEDENCE', case['case_id'])
            self.assertEqual(result['normalized_reason_codes'], counterpart['normalized_reason_codes'], case['case_id'])
            self.assertEqual(result['canonical_result_hex'], counterpart['canonical_result_hex'], case['case_id'])

    def test_neighbor_verify_classes_non_regression_outside_manifest(self) -> None:
        neighbor_cases = [
            ('CC003_VERIFY_REBUILD_HASH_EXPECTED_MISMATCH', rebuild_hash_mismatch_artifact()),
            ('CC009_VERIFY_ARTIFACT_HASH_INVALID', invalid_artifact_hash_artifact()),
            ('CC010_VERIFY_VALIDATOR_RESULT_INVALID', invalid_validator_result_artifact()),
            ('CC011_VERIFY_REBUILD_RESULT_INVALID', invalid_rebuild_result_artifact()),
        ]
        for expected_class, artifact in neighbor_cases:
            baseline = evaluate_corpus_entry('verify', artifact, self.kernel, self.domain, self.matrix)
            self.assertEqual(baseline['selected_class'], expected_class)
            self.assertNotEqual(baseline['selected_class'], 'CC012_MULTI_REASON_PRECEDENCE')
            self.assertFalse(baseline['multiple_reason_codes'])
            for variant in rule_order_variants('verify', self.kernel):
                perturbed = evaluate_corpus_entry(
                    'verify',
                    artifact,
                    self.kernel,
                    self.domain,
                    self.matrix,
                    rule_id_order_override=variant,
                )
                self.assertEqual(perturbed['selected_class'], expected_class)
                self.assertNotEqual(perturbed['selected_class'], 'CC012_MULTI_REASON_PRECEDENCE')
                self.assertEqual(perturbed['normalized_reason_codes'], baseline['normalized_reason_codes'])
                self.assertEqual(perturbed['canonical_result_hex'], baseline['canonical_result_hex'])


if __name__ == '__main__':
    unittest.main()
