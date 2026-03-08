# DeciRepo Go-To-Market Sequence v0.1

**Status:** Active Operational Roadmap  
**Objective:** Transition to Multi-Node Verification Network

---

## 1. Purpose

Define the exact sequence of steps required to launch the first real multi-node DeciRepo network. This roadmap ensures that the transition from a single reference node to an active verification graph is orderly, measurable, and technically sound.

---

## 2. Current Network State (Day Zero)

- **Reference Node:** IndrasNet (Node A) - Active.
- **External Nodes:** None.
- **Verification Graph:** Single node (internal edges only).
- **Trust Signals:** Internal/steward-based only.

---

## 3. Phase 1 — Anchor Stability

Ensure the Reference Node is fully prepared for external interaction.
- **Public Reference Endpoint:** Accessible via standard web protocols.
- **Stable Verification API:** 100% compliance with `VERIFICATION_RESULT_API_SPEC_V0_1.md`.
- **Public Example Artifacts:** A feed of diverse, valid decisions for external testing.
- **Public Graph Endpoint:** `/api/verification-graph` ready for external edges.

**Goal:** External operators must be able to verify Reference Node artifacts immediately upon deployment.

---

## 4. Phase 2 — First Mirror Verifier (Network Genesis)

Recruit and onboard the first independent operator.
- **Ideal Profile:** Mid-size audit or security firm with engineering/DevOps capability.
- **Onboarding:** Deployment using the `REFERENCE_NODE_DEPLOYMENT_GUIDE_V0_1.md`.
- **Genesis Event:** Node B performs the first successful cross-node verification of a Node A artifact.
- **Result:** Edge A → B appears in the Verification Graph.

---

## 5. Phase 3 — Second Verifier (Systemic Validation)

Add a second independent node to prove protocol interoperability.
- **Candidate Type:** Compliance automation provider or security consulting firm.
- **Verification Density:** Both Node B and Node C verify artifacts from Node A.
- **Emergence:** Trust Scores become meaningful network-derived signals.

---

## 6. Phase 4 — First Registry Node (Bi-directional Federation)

Introduce a node that both verifies and **publishes** artifacts.
- **Example:** An enterprise platform or workflow engine.
- **Network State:** Transition from "Hub and Spoke" to a peer-to-peer verification mesh.

---

## 7. Success Criteria for Network Launch

The DeciRepo network is considered "Alive" when:
1. **Nodes:** ≥ 3 independent nodes are operational.
2. **Activity:** ≥ 10 successful cross-node verification events recorded.
3. **Independence:** ≥ 2 operators exist outside the protocol steward.
4. **Visibility:** The Verification Graph is publicly visible and updated in real-time.

---

## 8. Summary

DeciRepo moves from a specification to a living infrastructure the moment independent organizations begin verifying each other's artifacts. Trust then emerges from **recomputation**, making institutional decisions truly verifiable for the first time.
