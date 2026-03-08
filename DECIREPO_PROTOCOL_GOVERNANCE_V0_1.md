# DECIREPO_PROTOCOL_GOVERNANCE_V0_1

Status: active policy  
Protocol baseline: `DeciRepo Protocol v0.1`  
Current stewardship phase: `Phase 1 — Founder Stewardship (IndrasNet OÜ)`

## 1) Purpose

Define how the DeciRepo Protocol is governed so that:

- protocol meaning is canonical and testable,
- compatibility is enforceable,
- trust-root management is transparent,
- transition to neutral stewardship is possible when ecosystem independence is reached.

## 2) Governance principles

1. Determinism first.
2. Spec + conformance + trust-root are the control plane.
3. Fail-closed on ambiguity.
4. No silent breaking changes.
5. Public changelog for all governance-relevant changes.

The DeciRepo Protocol is intended to transition to neutral foundation stewardship when the ecosystem reaches sufficient independence.

## 3) Stewardship phases

## Phase 1 — Founder Stewardship (`v0.1` to `v0.3`)

Owner: `IndrasNet OÜ`

Responsibilities:

- canonical protocol specification,
- canonical reference node behavior,
- conformance suite publication and maintenance,
- signed root-of-trust publication and rotation policy,
- compatibility badge policy.

Goal: stabilize protocol semantics and prevent early fragmentation.

## Phase 2 — Co-Governance (`v0.4` to `v0.x`)

Control model:

- multi-party trust-root signing (`2-of-3` minimum),
- public RFC process for protocol evolution,
- independent mirror/reference nodes,
- open conformance CI visibility.

Typical signers:

- IndrasNet OÜ,
- independent registry operator,
- external auditor.

## Phase 3 — Foundation Stewardship (`v1.x+`)

Neutral foundation manages:

- protocol specification lifecycle,
- conformance suite and compatibility criteria,
- trust-root governance and admission policy,
- deprecation policy and compatibility windows.

IndrasNet may continue to operate commercial DeciRepo runtime/services under its own business terms.

## 4) Change management model

Changes are classified as:

1. Additive: new optional fields/endpoints, no behavioral drift.
2. Compatible behavioral: clarified semantics without changing pass/fail outcomes.
3. Breaking: any change that can alter validation outcomes for previously valid artifacts.

Rules:

- In `v0.x`, breaking changes are forbidden unless a security-critical exception is declared.
- Security-critical exceptions require incident record + migration plan + compatibility note.
- Every accepted change requires conformance impact annotation.

## 5) RFC process

Lifecycle:

1. Draft RFC (`proposal`, `motivation`, `compatibility impact`, `test impact`).
2. Open review window.
3. Decision (`accept`, `accept-with-changes`, `reject`).
4. Spec update + conformance update in same release cycle.
5. Changelog publication.

Minimum RFC sections:

- protocol scope touched,
- backward compatibility statement,
- trust-root impact statement,
- required endpoint/schema updates,
- rollout and deprecation plan.

## 6) Compatibility guarantees

For each protocol release:

- explicit `protocol_version`,
- compatibility matrix (`source_version` x `target_version`),
- deprecated field policy with removal horizon,
- deterministic pass/fail criteria for federation handshake.

Compatible node definition:

- passes official conformance suite for declared version,
- exposes required discovery + verify + trust endpoints,
- publishes valid signed node manifest.

## 7) Root-of-trust governance

Root-of-trust must be:

- cryptographically signed,
- versioned,
- publicly accessible,
- accompanied by changelog.

Trust list operations:

- admission,
- suspension/quarantine,
- revocation,
- key rotation.

Each operation must emit a trust event and reference reason code.

## 8) Conformance and badge policy

`DeciRepo Protocol Compatible` badge requires:

- passing mandatory conformance profile for target protocol version,
- no unresolved critical negative test failures,
- valid signed manifest and discoverability endpoint.

Badge revocation conditions:

- repeated protocol non-compliance,
- unresolved rebuild mismatches above threshold,
- undeclared breaking drift.

## 9) Security and emergency governance

Emergency path is allowed only for:

- cryptographic compromise,
- deterministic verification corruption,
- trust-root key compromise.

Emergency changes must be followed by:

- post-incident report,
- formal RFC normalization,
- conformance backfill.

## 10) Scope boundary (protocol vs product)

Open governance scope:

- protocol specification,
- reference behavior,
- conformance rules,
- trust-root process.

Out-of-scope (product domain):

- proprietary production runtime optimizations,
- enterprise SLA/operations tooling,
- commercial integrations and support contracts.

