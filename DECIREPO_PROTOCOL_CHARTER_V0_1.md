# DECIREPO_PROTOCOL_CHARTER_V0_1

Status: active charter  
Applies to: `DeciRepo Protocol v0.1`

## 1) Charter purpose

Define protocol-neutrality commitments for the public DeciRepo protocol layer while allowing commercial managed nodes to operate on top of the same standard.

## 2) Neutrality commitments

1. Open specification: artifact, verify, lineage, discovery, and trust interfaces are public.
2. Open compatibility criteria: conformance profile and required tests are public and versioned.
3. Public compatibility signal: protocol nodes expose machine-readable conformance status.
4. No silent drift: behavior changes must be documented via RFC and changelog.
5. Trust governance transparency: trust-root operations are signed, versioned, and published.

## 3) Separation of layers

- Neutral layer: `DeciRepo Protocol` (standard + conformance + governance).
- Commercial layer: managed registry services operated by organizations (including IndrasNet).

Managed service features (SLA, connectors, support, analytics) must not alter protocol compatibility requirements.

## 4) 90-day commitments

1. Publish this charter and keep it versioned.
2. Run independent verification and implementation grants.
3. Publish protocol conformance report endpoint.
4. Keep compatibility badge policy objective and test-driven.

## 5) Ecosystem openness KPI

Primary openness signal:

- `external_verification_share >= 50%`

Interpretation:

- Below threshold: protocol ecosystem still founder-dominant.
- At or above threshold: protocol ecosystem demonstrates external verification maturity.
