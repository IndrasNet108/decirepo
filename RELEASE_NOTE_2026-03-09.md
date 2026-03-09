# RELEASE_NOTE_2026-03-09

## DeciRepo Genesis Surface

This release marks the public Genesis surface of the DeciRepo protocol.

DeciRepo introduces a model for verifying institutional decisions through deterministic recomputation.
Decisions are stored as structured artifacts that can be independently recomputed by compatible verifier nodes.

Verification follows a simple primitive:

`verify(decision_id) -> MATCH / FAIL`

If independent nodes obtain the same result through recomputation, the decision is considered reproducible.

---

## Genesis artifact

Genesis artifact published:

`DR-GENESIS-0001`

This artifact serves as the initial anchor for the public DeciRepo verification surface.

---

## Public infrastructure

The following components are now live:

- Public protocol repository: `decirepo`
- Public site: `decirepo.com`
- Public verification surface and artifact registry
- Public protocol documentation
- Public changelog (`PUBLIC_CHANGELOG.md`)

Operational documentation for verifier nodes is maintained in:

`decirepo-node-ops` (private operations repository)

---

## Protocol status

Protocol phase: **Genesis**

Verification model: **deterministic recomputation**

Network status: **independent verifier node bootstrap**

Governance surface: **published**

---

## Commerce posture

DeciRepo currently operates in **pilot-by-agreement** mode.

Public self-serve checkout is intentionally disabled.
Pilot engagements are initiated via **Request Pilot** and defined by mutual scope agreement.

---

## Operational safeguards

The current release includes:

- public release checklist
- commerce readiness gate
- public changelog tracking
- automated CI guard for the site posture

These controls prevent accidental activation of public self-serve commerce or deviation from pilot-only mode.

---

## Scope clarification

DeciRepo verifies **reproducibility of decisions**, not their correctness, legality, or normative legitimacy.

The protocol answers one question:

Did the declared procedure produce the same artifact when recomputed?

It does not answer whether the decision itself was appropriate.

---

## Operator

Protocol steward: **IndrasNet OÜ**
Location: Estonia

---

## References

Public site:
<https://decirepo.com>

Protocol repository:
<https://github.com/IndrasNet108/decirepo>

Public changelog:
`PUBLIC_CHANGELOG.md`
