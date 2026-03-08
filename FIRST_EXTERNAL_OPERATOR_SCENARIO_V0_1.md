# First External Operator Scenario v0.1

**Status:** Draft Operational Scenario  
**Objective:** Network Genesis (Transition to 2-node state)

---

## 1. Network Genesis

The network begins when the first independent verification path is established:
1. **Reference Node (Node A)** publishes a decision artifact (e.g., `DR-GOV-0001`).
2. **External Operator (Node B)** deploys a Mirror Verifier using the Deployment Guide.
3. **Discovery:** Node B resolves the manifest of Node A.
4. **Verification:** Node B executes `verify(DR-GOV-0001)` via independent rebuild.
5. **Result:** Node B publishes a "VERIFIED" result.
6. **Persistence:** The event is recorded, creating the first multi-node edge in the Verification Graph.

---

## 2. First Independent Trust Signal

Prior to this scenario, trust in artifacts was based on the authority of the Reference Node. After the first independent verification:
- **Reproducibility Proof:** Trust emerges from the fact that an independent environment produced an identical artifact hash.
- **Signal:** `independent_rebuild_match_count` for the artifact becomes `1`.
- **Impact:** The `trust_score` of Node A increases due to external confirmation of its artifacts.

---

## 3. Verification Graph Emergence

The graph transitions from a single-point registry to a relational structure:
- **Edge A → B:** Node B verifies Node A.
- **Visibility:** The edge becomes visible via `/api/verification-graph`.
- **Topology:** The network now has a verifiable path of independent validation.

---

## 4. Operator Roles in Genesis Phase

- **Reference Node:** Serves as the "anchor of truth" and source of initial artifacts.
- **Mirror Verifier:** Acts as the "independent witness," providing external validation capacity.
- **Registry Node (Phase 2):** Will eventually add the capacity to publish new artifacts from independent origins.

---

## 5. Minimal Network Topology

The simplest "alive" network consists of:
- **Node A:** Reference Registry (IndrasNet).
- **Node B:** Independent Mirror Verifier (e.g., an audit firm).
- **Node C:** Secondary Verifier (e.g., a community member).

Once this topology is active, **Trust Scores become meaningful network signals** rather than internal metrics.

---

## 6. Summary

This scenario represents the transition of DeciRepo from a protocol specification to a **living, breathing verification network**. The appearance of the second node is the single most important event in the project's history.
