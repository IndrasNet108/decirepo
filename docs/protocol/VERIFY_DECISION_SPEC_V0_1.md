# VERIFY_DECISION_SPEC_V0_1.md

## Status
Active Protocol Specification

## Scope
This document defines the protocol primitive:
`verify(decision_id)`

The primitive allows any party to independently verify that a decision artifact:
1. exists
2. is structurally valid
3. is reproducible
4. matches its canonical identity
5. references a valid evidence chain

The verification procedure does **not** determine whether a decision is correct, fair, or legally valid. It only determines whether the decision artifact is **consistent, reproducible, and verifiable**.

---

## 1. Definitions

### Decision Artifact
A deterministic record representing the execution of a decision model.
A decision artifact contains:
- `decision_id`
- `model_reference`
- `input_set`
- `policy_reference`
- `execution_trace`
- `result`
- `identity_hash`

### Evidence Artifact
An auxiliary artifact used to explain, compare, or investigate the decision.
Examples: `precedent-search-report`, `decision-explanation`, `decision-divergence`, `divergence-investigation-report`, `audit-package`.

### Evidence Bundle
A deterministic package that references all artifacts required to investigate a decision.

### Identity Hash
A cryptographic hash representing the canonical serialization of the decision artifact.

### Rebuild
The deterministic recomputation of a decision artifact using the same inputs and model reference.

---

## 2. Verification Goals
The verification process answers the following questions:
1. Does the decision artifact exist?
2. Is the artifact structurally valid?
3. Can the artifact be deterministically rebuilt?
4. Does the rebuilt artifact match the recorded identity hash?
5. Are referenced evidence artifacts available and consistent?

---

## 3. Verification Primitive
The verification primitive is defined as:
`verify(decision_id)`

### Expected Output
A verification report containing:
- `decision_id`
- `artifact_presence`
- `structure_valid`
- `rebuild_status`
- `identity_match`
- `evidence_chain_status`
- `verification_status`

Where:
`verification_status ∈ { VERIFIED | INVALID | INCOMPLETE }`

---

## 4. Verification Procedure

### Stage 1 — Artifact Resolution
Resolve the decision artifact: `resolve(decision_id)`.
Possible results: `FOUND`, `NOT_FOUND`.

### Stage 2 — Structural Validation
Validate artifact structure against the decision artifact schema.
Check: required fields, types, serialization rules, schema version compatibility.

### Stage 3 — Canonical Identity Validation
Recompute the canonical serialization and compare:
`computed_hash == identity_hash`.

### Stage 4 — Deterministic Rebuild
Rebuild the decision artifact: `rebuild(model_reference, input_set)`.
Expected result: `rebuild_result == recorded_result`.

### Stage 5 — Evidence Reference Validation
Resolve references to evidence artifacts. Each reference must be resolvable, structurally valid, and linked to `decision_id`.

### Stage 6 — Verification Result
- If all checks PASS: `VERIFIED`
- If identity or rebuild mismatch: `INVALID`
- If artifact valid but evidence incomplete: `INCOMPLETE`

---

## 5. Verification Report Format (JSON)
```json
{
  "decision_id": "...",
  "artifact_presence": "FOUND",
  "structure_valid": true,
  "identity_match": true,
  "rebuild_status": "MATCH",
  "evidence_chain_status": "VALID",
  "verification_status": "VERIFIED"
}
```

---

## 6. Determinism Requirement
The rebuild procedure MUST be deterministic. Given identical model reference, input set, policy reference, and environment constraints, the rebuild MUST produce identical result and identity hash.

---

## 7. Non-Goals
The verification protocol explicitly does **not**:
- determine whether the decision was correct
- determine whether the policy is valid
- determine legal compliance
- provide recommendations

---

## 8. Summary
The verification primitive ensures that a decision artifact is present, structured, reproducible, identity-consistent, and evidence-linked. This allows independent parties to verify the integrity of a decision without trusting the system that produced it.
