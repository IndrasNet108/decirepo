# INDEPENDENT_VERIFICATION_GRANTS_V0_1

Status: active program spec  
Program owner: `IndrasNet OÜ` (Phase 1 steward)

## 1) Purpose

Accelerate neutral protocol adoption by funding independent verification capacity and independent DLX-compatible implementations.

## 2) Grant tracks

1. Mirror verifier node
   - Deploy a public DeciRepo-compatible verifier.
   - Publish signed node manifest and discovery endpoint.
2. External registry node
   - Operate an independent decision registry node with protocol-compatible endpoints.
3. Independent implementation
   - Build a non-IndrasNet DLX-compatible engine and pass conformance suite.

## 3) Mandatory deliverables

- Public repository or binary release notes.
- Conformance results against current mandatory profile.
- Reproducible run instructions.
- Signed node manifest (for node tracks).
- Operational incident policy.

## 4) Selection criteria

1. Technical capability to run deterministic verification.
2. Independence from IndrasNet runtime/control plane.
3. Operational reliability and security hygiene.
4. Commitment to protocol compatibility and public changelogs.

## 5) Funding model

- Milestone-based disbursement.
- Final milestone requires conformance pass.
- Failed conformance blocks final disbursement.

## 6) Program success metrics

- Number of independent production verifier nodes.
- Number of independent conformance runners.
- Number of external implementations passing conformance.
- Share of external verification traffic (`target >= 50%`).
