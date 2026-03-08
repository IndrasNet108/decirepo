# VERIFICATION_RESULT_API_SPEC_V0_1.md

## Status
Draft Protocol Specification

---

## 1. Purpose
This document defines the **canonical API representation of verification results** produced by DeciRepo nodes. Standardizing these outcomes ensures interoperability across the verification graph, trust scoring systems, and independent audit trails.

---

## 2. Verification Result Object
All DeciRepo nodes MUST produce verification results using the following JSON structure:

```json
{
  "verification_id": "string",
  "decision_id": "string",
  "origin_node": "string",
  "verifier_node": "string",
  "verification_status": "VERIFIED | INVALID | INCOMPLETE",
  "identity_match": true,
  "rebuild_status": "MATCH | MISMATCH | FAILED",
  "evidence_chain_status": "VALID | PARTIAL | MISSING",
  "verification_timestamp": "ISO-8601 timestamp",
  "software_version": "string"
}
```

---

## 3. API Endpoints
Nodes SHOULD expose the following standardized endpoints:

### 3.1 Retrieve verification result
`GET /api/verification-result?id={verification_id}`

### 3.2 Retrieve decision verification history
`GET /api/decision-verification-history?decision_id={decision_id}`

### 3.3 Retrieve node verification history
`GET /api/node-verification-history?node_id={node_id}`

---

## 4. Error Handling
Nodes MUST return structured errors for failed operations.
Example:
```json
{
  "error": "ARTIFACT_NOT_FOUND",
  "decision_id": "decision_X"
}
```
Common error codes: `ARTIFACT_NOT_FOUND`, `REBUILD_FAILED`, `EVIDENCE_UNAVAILABLE`, `NODE_TIMEOUT`, `INVALID_REQUEST`.

---

## 5. Compatibility Rules
Nodes participating in the DeciRepo network MUST:
- support the canonical verification result schema.
- use ISO-8601 timestamps.
- ensure verification results are immutable once published.

---

## 6. Summary
The Verification Result API ensures that verification outcomes are interoperable across the network, enabling reliable aggregation of activity into the verification graph and trust signal systems.
