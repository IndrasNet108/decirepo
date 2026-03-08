# DeciRepo Protocol Constitution v0.1

**Status:** Active Governance Contract  
**Creator:** Oleg Surkov  
**Steward:** IndrasNet OÜ  
**Foundation Principle:** Trust through deterministic recomputation.

---

## 1. Purpose
The purpose of this Constitution is to ensure the long-term stability, interoperability, and integrity of the DeciRepo protocol. It defines the boundaries of the protocol and the rules by which it may evolve.

---

## 2. Protocol Scope (The Baseline)
The following components constitute the **DeciRepo Protocol Baseline**. Any modification to these components is considered a protocol change:
- **DLX Deterministic Execution Model:** The formal rules for recomputing decisions.
- **Decision Artifact Schema:** The canonical structure of recorded decisions.
- **`verify(decision_id)` Primitive:** The core logic of identity and rebuild validation.
- **Verification Result API:** The standardized format for reporting outcomes.
- **Node Manifest Schema:** The discovery and identity format for nodes.
- **Trust Score Derivation:** The methodology for computing network-derived trust.

---

## 3. Non-Protocol Components
The following are considered implementation details and are NOT governed by this Constitution:
- UI/UX presentation layers.
- Specific database or storage technologies.
- Commercial service levels (SLA).
- Analytics and business intelligence tools built atop the protocol.

---

## 4. Versioning & Compatibility
- **Major Version (vX.0.0):** Breaking changes to artifact identity or verification semantics.
- **Minor Version (v0.X.0):** Backward-compatible extensions to the schema or API.
- **Patch (v0.0.X):** Documentation updates, security fixes, or non-functional changes.

---

## 5. Protocol Change Process
Evolution of the protocol must follow a transparent, five-step path:
1. **Proposal (RFC):** Public documentation of the intended change.
2. **Review:** Technical evaluation by the Protocol Steward and active operators.
3. **Reference Implementation:** Update to the `dlx-ref` engine.
4. **Conformance Update:** Integration into the mandatory test suite.
5. **Adoption:** Independent nodes elect to upgrade to the new version.

---

## 6. Role of the Protocol Steward
**IndrasNet OÜ** acts as the initial Steward. The Steward’s role is to:
- Maintain the reference implementation and conformance suite.
- Coordinate the RFC process.
- Ensure the neutrality and stability of the baseline documentation.
- **Note:** The Steward coordinates the protocol but does not control the independent nodes of the network.

---

## 7. Federation Autonomy
Every node in the DeciRepo network is autonomous. Nodes have the right to:
- Independently execute verifications.
- Elect which version of the protocol to support.
- Publish artifacts according to their own internal policies.

---

## 8. Fork Definition
A fork occurs when a network participant alters the **Identity Rules**, **Verification Semantics**, or **Execution Model** in a way that breaks interoperability with the Baseline. A fork is not a protocol upgrade unless it is adopted by the Steward into the Baseline.

---

## 9. Compatibility Guarantees
The protocol must strive to ensure that an artifact produced today remains:
- **Reproducible:** Using the same model and inputs.
- **Verifiable:** Using the canonical `verify` primitive.
- **Stable:** Immune to silent mutations in the underlying infrastructure.

---

## 10. The Long-term Principle
**Trust must emerge from independent recomputation rather than institutional authority.**

DeciRepo exists to provide the infrastructure where proof replaces claims. This principle is immutable and overrides any commercial or technical convenience.
