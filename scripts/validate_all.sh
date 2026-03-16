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

echo "ALL VALIDATIONS PASSED"
