# OPERATOR_ONBOARDING_CHECKLIST_V0_1.md

## Operator Setup Checklist

### 1. Infrastructure
- [ ] Deploy DeciRepo node endpoint.
- [ ] Configure artifact storage (persistent).
- [ ] Enable verification runtime (DLX compatible).

### 2. Protocol Implementation
- [ ] Implement `verify(decision_id)` according to `VERIFY_DECISION_SPEC_V0_1.md`.
- [ ] Enable artifact resolution.
- [ ] Enable evidence bundle validation.

### 3. Discovery & Identity
- [ ] Generate node public key.
- [ ] Publish `/.well-known/decirepo-node`.
- [ ] Ensure manifest is signed (if required by role).

### 4. Validation
- [ ] Pass full `dlx-ref` conformance suite.
- [ ] Run `bash scripts/validate_all.sh` locally.
- [ ] Submit conformance report to protocol steward.
