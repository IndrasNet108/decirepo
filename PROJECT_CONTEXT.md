Project: DeciRepo

Architecture layers:
1. DLX — deterministic decision execution engine
2. DeciRepo — decision registry
3. Precedent Search — retrieval layer
4. Policy Drift Detection — governance monitoring

Protocol:
DeciRepo Protocol v0.1

Reference engine:
dlx-ref

Mandatory validation steps after any code change:
1. node scripts/sanity_check_registry.js
2. node scripts/run_negative_federation_tests.js
3. node dlx-ref/cli.js conformance dlx-ref/tests/conformance_v0_1.json

Rules:
- Never infer protocol behavior
- Never modify artifacts format
- Never change endpoints without updating protocol.json
- Always run validation before claiming success
