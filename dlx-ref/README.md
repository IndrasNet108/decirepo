# dlx-ref

Neutral reference engine skeleton for DLX protocol semantics (`v0.1`).

Scope is defined in:

- `../DLX_REFERENCE_ENGINE_SCOPE_V0_1.md`

## Commands

```bash
node dlx-ref/cli.js verify dlx-ref/test-vectors/artifacts/valid_governance_artifact.json
node dlx-ref/cli.js rebuild dlx-ref/test-vectors/artifacts/valid_governance_artifact.json
node dlx-ref/cli.js validate dlx-ref/test-vectors/artifacts/transition_valid_artifact.json
node dlx-ref/cli.js conformance dlx-ref/tests/conformance_v0_1.json
```

## CLI contract

- `verify <artifact.json>`: schema and semantic checks for artifact envelope.
- `rebuild <artifact.json>`: deterministic rebuild hash from `rebuild_source`.
- `validate <artifact.json>`: transition chain validation.
- `conformance <suite.json | suite_dir>`: run pass/fail conformance profile.

## Notes

- Determinism-first implementation.
- Fail-closed on malformed input.
- No production runtime optimizations.

