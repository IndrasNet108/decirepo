# NEGATIVE_FEDERATION_TESTS_V0_1

Purpose: verify deterministic fail-closed behavior for federation boundary failures.

## Cases

- NEG-001 incompatible protocol version -> `deny_quarantine`
- NEG-002 missing node manifest -> `deny`
- NEG-003 invalid manifest signature -> `deny`
- NEG-004 repeated rebuild mismatch -> `suspend`
- NEG-005 undeclared policy profile drift -> `quarantine`

## Run

```bash
node /home/indrasnet/DeciRepo/scripts/run_negative_federation_tests.js
```

Expected result: all cases pass and no case resolves to permissive action.
