#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "oracle"))

from decirepo_oracle_v0_1 import (  # noqa: E402
    DECLARED_CLASS_BUCKETS,
    SUPPORTED_STATE_REQUIREMENTS,
    SUPPORTED_COMPOSITION_OPERATORS,
    SUPPORTED_PREDICATE_OPERATORS,
)


def load_json(rel_path: str) -> dict:
    return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))


def collect_kernel_predicates(kernel: dict) -> list[dict]:
    predicates: list[dict] = []
    predicates.extend(kernel["domain"]["baseline_compatible_path"]["predicates"])
    for command_def in kernel["commands"].values():
        predicates.extend(command_def.get("entry_conditions", []))
    predicates.extend(rule["predicate"] for rule in kernel["rules"])
    return predicates


class KernelContractV01Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.kernel = load_json("conformance/SEMANTICS_KERNEL_V0_1.json")
        cls.domain = load_json("conformance/DOMAIN_PROFILE_V0_1.json")
        cls.matrix = load_json("conformance/CASE_CLASS_MATRIX_V0_1.json")

    def test_operator_registry_matches_oracle_capabilities(self) -> None:
        registry = set(self.kernel["predicate_language"]["operator_registry"].keys())
        self.assertEqual(registry, set(SUPPORTED_PREDICATE_OPERATORS))

    def test_composition_registry_matches_oracle_capabilities(self) -> None:
        registry = set(self.kernel["predicate_language"]["composition_registry"].keys())
        self.assertEqual(registry, set(SUPPORTED_COMPOSITION_OPERATORS))

    def test_all_used_kernel_operators_are_declared(self) -> None:
        declared = set(self.kernel["predicate_language"]["operator_registry"].keys())
        used = {predicate["operator"] for predicate in collect_kernel_predicates(self.kernel)}
        self.assertTrue(used)
        self.assertTrue(used.issubset(declared))

    def test_operator_contract_entries_are_complete(self) -> None:
        required_keys = {
            "arity",
            "required_keys",
            "evaluation",
            "false_semantics",
            "predicate_error_semantics",
        }
        for operator, contract in self.kernel["predicate_language"]["operator_registry"].items():
            self.assertTrue(required_keys.issubset(contract.keys()), operator)
            self.assertIsInstance(contract["required_keys"], list, operator)
            self.assertTrue(contract["required_keys"], operator)

    def test_classification_pipeline_is_explicit(self) -> None:
        pipeline = self.kernel["classification_pipeline"]
        self.assertTrue(pipeline["bucket_assignment_precedes_verdict_assignment"])
        self.assertEqual(
            [stage["stage_id"] for stage in pipeline["stages"]],
            ["bucket_assignment", "class_assignment", "verdict_derivation"],
        )
        self.assertEqual(pipeline["bucket_order"], self.matrix["class_buckets"])
        self.assertEqual(set(self.matrix["class_buckets"]), set(DECLARED_CLASS_BUCKETS))

    def test_case_matrix_predicate_refs_resolve(self) -> None:
        predicate_registry = {
            predicate["predicate_id"]: predicate for predicate in self.matrix["predicate_registry"]
        }
        self.assertTrue(predicate_registry)
        for cls in self.matrix["classes"]:
            self.assertIn(cls["predicate_ref"], predicate_registry, cls["class_id"])
            predicate = predicate_registry[cls["predicate_ref"]]
            self.assertEqual(cls["class_bucket"], predicate["class_bucket"], cls["class_id"])
            self.assertEqual(cls["command"], predicate["command"], cls["class_id"])
            self.assertIn(cls["class_bucket"], DECLARED_CLASS_BUCKETS, cls["class_id"])

    def test_case_matrix_predicate_registry_is_closed(self) -> None:
        composition_registry = set(self.kernel["predicate_language"]["composition_registry"].keys())
        state_registry = set(self.kernel["classification_pipeline"]["state_projection_registry"].keys())
        rule_ids = {rule["rule_id"] for rule in self.kernel["rules"]}
        for predicate in self.matrix["predicate_registry"]:
            self.assertIn(predicate["composition"], composition_registry, predicate["predicate_id"])
            rule_outcomes = predicate.get("rule_outcomes", [])
            state_requirements = predicate.get("state_requirements", {})
            self.assertTrue(rule_outcomes or state_requirements, predicate["predicate_id"])
            self.assertTrue(set(state_requirements).issubset(state_registry), predicate["predicate_id"])
            for rule_outcome in rule_outcomes:
                self.assertIn(rule_outcome["rule_id"], rule_ids, predicate["predicate_id"])
                self.assertIsInstance(rule_outcome["outcome"], bool, predicate["predicate_id"])

    def test_state_projection_registry_matches_oracle_capabilities(self) -> None:
        registry = set(self.kernel["classification_pipeline"]["state_projection_registry"].keys())
        self.assertEqual(registry, set(SUPPORTED_STATE_REQUIREMENTS))

    def test_precedence_ranks_are_unique_within_scope(self) -> None:
        seen: dict[tuple[str, str], set[int]] = defaultdict(set)
        for cls in self.matrix["classes"]:
            scope = (cls["command"], cls["class_bucket"])
            rank = cls["precedence_rank"]
            self.assertNotIn(rank, seen[scope], f"duplicate precedence_rank in scope={scope}")
            seen[scope].add(rank)

    def test_domain_reason_order_matches_kernel(self) -> None:
        self.assertEqual(
            self.domain["normalized_result"]["reason_code_ordering"],
            self.kernel["normalized_result"]["reason_code_ordering"],
        )
        self.assertEqual(
            self.domain["normalized_result"]["reason_code_normalization"],
            self.kernel["normalized_result"]["reason_code_normalization"],
        )


if __name__ == "__main__":
    unittest.main()
