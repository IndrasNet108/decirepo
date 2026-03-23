# VERIFICATION_GRAPH_SPEC_V0_1.md

## Status
Draft Protocol Specification

---

## 1. Purpose
The verification graph records **independent verification activity** within the DeciRepo network. It tracks which nodes verify which decision artifacts, enabling:
- independent rebuild validation
- verification density measurement
- cross-node verification tracking
- trust signal generation

The graph does **not** determine the correctness of decisions; it only records **verification activity**.

---

## 2. Graph Entities

### Node
Represents a DeciRepo network operator.
Attributes: `node_id`, `operator`, `node_type`, `software_version`, `public_key`.

### Decision Artifact
Represents a DLX decision artifact.
Attributes: `decision_id`, `artifact_hash`, `model_reference`, `timestamp`.

### Verification Event
Represents an attempt to verify a decision artifact.
Attributes: `verification_id`, `node_id`, `decision_id`, `verification_status`, `timestamp`.
Where: `verification_status ∈ { VERIFIED | INVALID | INCOMPLETE }`.

---

## 3. Graph Edges

### Verification Edge
Represents a node verifying a decision.
`node → verifies → decision`
Attributes: `verification_status`, `timestamp`.

### Trust Observation Edge
Represents a node observing verification results produced by another node.
`node_A → observes → node_B`
This edge allows the network to compute **verification independence**.

---

## 4. Graph Update Rules
The verification graph updates when `verify(decision_id)` is executed.
Update process:
1. Verification event created.
2. Verification edge added.
3. Verification result recorded.

If multiple nodes verify the same decision, multiple edges exist, increasing network confidence in the artifact’s reproducibility.

---

## 5. Graph Query Endpoints
Nodes may expose verification graph data via API endpoints:
- `/api/verification-graph`
- `/api/verification-events`
- `/api/decision-verification-history`

Example query response (`GET /api/decision-verification-history?decision_id=abc123`):
```json
{
  "decision_id": "abc123",
  "verifications": [
    { "node_id": "node_A", "status": "VERIFIED" },
    { "node_id": "node_B", "status": "VERIFIED" }
  ]
}
```

---

## 6. Trust Signal Derivation
Trust signals are derived from graph activity:
- `verification_success_rate(node)`
- `rebuild_match_rate(node)`
- `independent_verification_count(decision)`
- `node_availability`

These signals contribute to the DeciRepo **trust score** system.

---

## 7. Summary
The verification graph enables DeciRepo to track **independent verification activity** across nodes. This allows the network to evolve into a **federated verification system** where trust emerges from multiple independent rebuild confirmations.
