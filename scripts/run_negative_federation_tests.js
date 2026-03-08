#!/usr/bin/env node
/**
 * DeciRepo Negative Federation Tests
 * Lead Architect & Creator: Oleg Surkov
 */

const fs = require('fs');
const path = require('path');

const suitePath = path.resolve(__dirname, '..', 'NEGATIVE_FEDERATION_TESTS_V0_1.json');
const suite = JSON.parse(fs.readFileSync(suitePath, 'utf8'));

function evaluate(input) {
  if (!input.protocol_compatible) return 'deny_quarantine';
  if (!input.node_manifest_present) return 'deny';
  if (!input.manifest_signature_valid) return 'deny';
  if (input.rebuild_mismatch_repeated) return 'suspend';
  if (input.undeclared_profile_drift) return 'quarantine';
  return 'allow';
}

let failed = 0;
const rows = [];

for (const testCase of suite.cases || []) {
  const actual = evaluate(testCase.input || {});
  const expected = testCase.expected_action;
  const ok = actual === expected;
  if (!ok) failed += 1;
  rows.push({
    id: testCase.id,
    name: testCase.name,
    expected,
    actual,
    ok
  });
}

for (const row of rows) {
  const status = row.ok ? 'PASS' : 'FAIL';
  console.log(`${status} ${row.id} ${row.name} expected=${row.expected} actual=${row.actual}`);
}

if (failed > 0) {
  console.error(`\nNegative federation suite FAILED: ${failed} case(s).`);
  process.exit(1);
}

console.log(`\nNegative federation suite PASSED: ${rows.length} case(s).`);
