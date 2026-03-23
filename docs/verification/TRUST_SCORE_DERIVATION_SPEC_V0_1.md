# TRUST_SCORE_DERIVATION_SPEC_V0_1.md

## Status
Draft Protocol Specification

---

## 1. Purpose
This document defines how DeciRepo derives **trust-relevant signals** from observable network behavior. The trust score system provides a machine-readable summary of node reliability based on verification activity, reproducibility, and protocol conformance.

Trust score is an **network-operational signal**. It does NOT determine decision correctness, policy validity, or moral legitimacy.

---

## 2. Trust Model
Trust in DeciRepo is derived from **observable protocol behavior**, not reputation claims. It is downstream of:
- verification events and results
- verification graph structure
- conformance status
- availability observations

---

## 3. Trust Signal Categories

### 3.1 Verification Success Rate
`verification_success_rate(node) = VERIFIED results / total verification attempts`

### 3.2 Rebuild Match Rate
`rebuild_match_rate(node) = MATCH rebuilds / total rebuild attempts`

### 3.3 Artifact Availability Rate
`artifact_availability_rate(node) = successful artifact resolutions / total resolution requests`

### 3.4 Evidence Completeness Rate
`evidence_completeness_rate(node) = VALID evidence chains / total evidence checks`

### 3.5 Protocol Conformance Status
Represents whether the node passes `dlx-ref` conformance checks. Possible values: `PASS`, `FAIL`, `PENDING`.

---

## 4. Trust Inputs
Trust score derivation MUST only use inputs observable through protocol mechanisms:
- `verification_result` objects
- verification graph edges
- conformance reports
- artifact resolution outcomes

---

## 5. Derivation Rules
A trust score MUST be derived from a weighted combination of signals. 
Example JSON structure:
```json
{
  "node_id": "node_A",
  "trust_score": 0.94,
  "signals": {
    "verification_success_rate": 0.98,
    "rebuild_match_rate": 0.99,
    "artifact_availability_rate": 0.97,
    "evidence_completeness_rate": 0.95,
    "conformance_status": "PASS"
  }
}
```

---

## 6. Penalties and Downgrades
Trust score MUST support negative adjustments for:
- repeated rebuild mismatches (Identity Drift)
- repeated artifact unavailability
- conformance failures (Protocol Drift)
- malformed verification result publication

---

## 7. Summary
The DeciRepo trust score system converts observable verification behavior into structured signals. This allows the network to estimate node reliability without confusing operational trust with decision correctness.
