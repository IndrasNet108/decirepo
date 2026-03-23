# FIRST_EXTERNAL_OPERATOR_PROGRAM_V0_1.md

## Status
Draft Network Program

---

## 1. Purpose
This document defines the process for onboarding independent DeciRepo operators.
The objective is to establish the first **multi-node verification network** capable of:
- cross-node verification
- artifact mirroring
- independent rebuild validation
- trust scoring

External operators extend the verification capacity of the network without altering the DLX execution model.

---

## 2. Node Types

### Reference Node
Maintained by the protocol steward.
Responsibilities: protocol reference implementation, canonical documentation, conformance test suite, registry reference data.

### Mirror Verifier Node
Independent operator that verifies decisions but does not necessarily publish new artifacts.
Responsibilities: `verify(decision_id)`, artifact rebuild, evidence bundle validation, participation in verification graph.
**Recommended first external role.**

### Registry Node
Operator capable of both publishing decision artifacts and verifying them. Registry nodes expand the decision network.

---

## 3. Operator Requirements
An external operator must provide:
- **Infrastructure:** Public DeciRepo node endpoint, artifact storage, verification runtime.
- **Protocol Support:** `verify(decision_id)`, artifact resolution, identity validation, evidence bundle resolution.
- **Conformance:** Node MUST pass the `dlx-ref` conformance suite.

---

## 4. Node Discovery
Operators must expose a discovery file at `/.well-known/decirepo-node`.
Example:
```json
{
  "node_id": "example-node",
  "operator": "Example Organization",
  "node_type": "mirror_verifier",
  "software_version": "decirepo-node-v0.1",
  "verification_endpoint": "https://node.example.org/api/verify",
  "conformance_status": "PASS",
  "public_key": "..."
}
```

---

## 5. Trust Integration
External operators become part of the DeciRepo trust layer. Trust signals include:
- `verification_success_rate`
- `rebuild_match_rate`
- `node_availability`
- `protocol_conformance`

---

## 6. Pilot Phase Requirements
Initial external operators participate in a pilot program with minimum thresholds:
- ≥ 30 days uptime
- ≥ 100 verification requests
- ≥ 10 verified decision artifacts

---

## 7. Network Objective
The goal is to establish a network where decisions are produced by DLX, registered by DeciRepo, and verified independently. This ensures that no single operator controls the verification process.
