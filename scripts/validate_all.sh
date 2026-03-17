#!/bin/bash

# Exit on any failure
set -e

echo "Running Registry Sanity Check..."
node scripts/sanity_check_registry.js

echo "Running Negative Federation Tests..."
node scripts/run_negative_federation_tests.js

echo "Running Conformance Suite..."
node dlx-ref/cli.js conformance dlx-ref/tests/conformance_v0_1.json

echo "Running Protocol Conformance Baseline..."
node scripts/run_protocol_conformance_v0_1.js

echo "Running Oracle Vector Tests..."
python3 oracle/tests/test_vectors_v0_1.py
python3 oracle/tests/test_kernel_contract_v0_1.py
python3 oracle/tests/test_gap_classification_v0_1.py
python3 oracle/gen_corpus_v0_1.py
python3 oracle/gen_boundary_corpus_v0_1.py
python3 oracle/gen_adversarial_corpus_v0_1.py
python3 oracle/tests/test_partition_v0_1.py
python3 oracle/tests/test_boundary_adversarial_v0_1.py

echo "ALL VALIDATIONS PASSED"
