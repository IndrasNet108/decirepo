# NODE_TO_NODE_VERIFICATION_PROTOCOL_V0_1.md

## Status
Draft Protocol Specification

---

## 1. Purpose
This document defines the protocol for **cross-node verification** in the DeciRepo network. It allows one node to request independent verification of a decision artifact from another node, enabling independent rebuild confirmation, verification graph updates, and trust signal generation.

---

## 2. Roles

### Origin Node
The node that publishes or serves the decision artifact being verified.

### Verifier Node
The node that independently resolves and verifies the artifact.

### Observer Node
Any node that consumes or records verification events for graph and trust purposes.

---

## 3. Preconditions
- Both nodes must expose discoverable manifests via `/.well-known/decirepo-node`.
- The decision artifact must be resolvable by `decision_id`.
- The verifier node must support the `verify(decision_id)` primitive.

---

## 4. Verification Exchange Model
1. Discover origin node.
2. Resolve artifact reference.
3. Request verification.
4. Execute local verification on verifier node.
5. Produce and return structured verification result.
6. Update verification graph and emit trust events.

---

## 5. Minimal API Surface

### 5.1 Node discovery
`GET /.well-known/decirepo-node` -> Returns node manifest.

### 5.2 Artifact resolution
`GET /api/decision?id={decision_id}` -> Returns decision artifact.

### 5.3 Verification request
`POST /api/verify-request`
Request body: `{"decision_id": "...", "origin_node": "...", "requesting_node": "..."}`

### 5.4 Verification result
`GET /api/verification-result?id={verification_id}` -> Returns result per `VERIFY_DECISION_SPEC_V0_1.md`.

---

## 6. Verification Semantics
The verifier node MUST return a structured result containing:
- `verification_id`, `decision_id`, `origin_node`, `verifier_node`
- `verification_status` (VERIFIED | INVALID | INCOMPLETE)
- `identity_match`, `rebuild_status`, `evidence_chain_status`
- `timestamp`

---

## 7. Graph Update Rules
A successful exchange MUST create a verification event in the graph:
`verifier_node ──verifies──> decision_id`

---

## 8. Failure Modes
- **Discovery failure:** Origin node manifest not resolvable.
- **Resolution failure:** Artifact cannot be fetched.
- **Verification failure:** Local runtime errors or missing dependencies.
- **Identity mismatch:** Hash mismatch during rebuild/canonicalization.
- **Evidence incompleteness:** Required references missing.

---

## 9. Summary
The node-to-node verification protocol transforms DeciRepo from a single-node registry into a proto-federated verification network where trust emerges from independent verification activity across multiple nodes.
