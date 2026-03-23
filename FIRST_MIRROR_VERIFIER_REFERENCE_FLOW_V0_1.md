# FIRST_MIRROR_VERIFIER_REFERENCE_FLOW_V0_1.md

## Status
Operational Reference Scenario

---

# 1. Purpose
This document defines the **reference deployment scenario** for the first external mirror verifier node in the DeciRepo network.
The goal is to demonstrate a complete cross-node verification cycle.
The scenario establishes the first **independent verification path** in the network.

---

# 2. Actors

### Reference Node
Maintained by the protocol steward.
Responsibilities:
- publish decision artifacts
- serve artifact resolution endpoints
- maintain registry state

---

### Mirror Verifier Node
Independent external operator.
Responsibilities:
- resolve decision artifacts
- execute `verify(decision_id)`
- produce independent verification results
- publish verification events

---

# 3. Preconditions
Before the scenario begins:
- Both nodes must expose: `/.well-known/decirepo-node`
- Both nodes must support: `verify(decision_id)`, artifact resolution, verification event recording
- The decision artifact must be resolvable by `decision_id`.

---

# 4. Reference Verification Flow

### Step 1 — Node Discovery
Mirror node resolves reference node manifest: `GET /.well-known/decirepo-node`.
Manifest contains: `node_id`, `verification_endpoint`, `software_version`, `public_key`.

### Step 2 — Artifact Resolution
Mirror node retrieves decision artifact: `GET /api/decision?id={decision_id}`.
Artifact includes: decision artifact, `identity_hash`, `model_reference`, evidence references.

### Step 3 — Evidence Resolution
Mirror node resolves evidence bundle: `GET /api/evidence-bundle-manifest?id={decision_id}`.
Bundle references: `precedent-search-report`, `decision-explanation`, `decision-divergence`, `divergence-investigation-report`, `audit-package`.

### Step 4 — Independent Verification
Mirror node executes: `verify(decision_id)`.
Verification performs: artifact validation, identity hash validation, deterministic rebuild, evidence chain validation.

### Step 5 — Verification Result Generation
Mirror node generates verification report.
Example:
```json
{
  "verification_id": "verif-001",
  "decision_id": "decision_X",
  "origin_node": "reference_node",
  "verifier_node": "mirror_node",
  "verification_status": "VERIFIED",
  "identity_match": true,
  "rebuild_status": "MATCH",
  "evidence_chain_status": "VALID",
  "timestamp": "2026-03-07T12:00:00Z"
}
```

### Step 6 — Verification Event Publication
Mirror node exposes verification result via API: `GET /api/verification-result?id={verification_id}`.

### Step 7 — Verification Graph Update
The following edge is added: `mirror_node ──verifies──> decision_X`.

---

# 5. Trust Signal Emission
Verification events contribute to trust metrics:
- `independent_verification_count(decision)`
- `verification_success_rate(node)`
- `rebuild_match_rate(node)`
- `artifact_availability_rate(origin_node)`

---

# 6. Minimal Pilot Metrics
- ≥ 10 cross-node verifications
- ≥ 1 external mirror node
- ≥ 1 independent rebuild confirmation
- ≥ 30 days operational uptime

---

# 7. Summary
The first mirror verifier deployment demonstrates that DeciRepo decisions can be verified independently by external nodes. This confirms that trust in the system emerges from **independent verification**, not from authority of a single node.
