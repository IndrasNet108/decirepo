# ANCHOR_PUBLISHER_STRATEGY_V0_1

Status: active strategy  
Scope: DeciRepo network legitimacy bootstrap (`v0.1` to `v0.x`)

## 1) Purpose

Define the first anchor publisher profile and launch conditions that make DeciRepo economically viable and institutionally credible.

## 2) Anchor thesis

First anchor publisher should be a large regulated financial institution (bank or payment organization), not a public-sector body.

Rationale:

- high decision volume,
- high cost of audit/compliance failure,
- existing budget ownership for controls,
- immediate demand for reproducible decision evidence.

Bootstrap note:

- Before external anchor onboarding, DeciRepo may run an internal anchor stream via `IndrasNet Governance Registry` (`indrasnet-governance`) for protocol/trust governance dogfooding.

## 3) Anchor publisher profile

Required characteristics:

1. Regulated entity with ongoing AML/KYC/sanctions decision workload.
2. Minimum annual decision artifact volume: `>= 50,000`.
3. Internal compliance/audit owner with signing authority.
4. Capability to run private-by-default publishing with selective public proof.

Preferred characteristics:

- multi-jurisdiction operations,
- existing external audit relationships,
- mature security key management process.

## 4) Minimum anchor deal structure

1. Contract term: `12 months`.
2. Scope: private registry + write pipeline + verification workflow.
3. Volume commitment: `>= 50k artifacts/year`.
4. Public proof commitment: `1% to 5%` of artifacts (proof-only, no sensitive payload).
5. Independent verifier involvement: at least one external audit/assurance party.

## 5) Economic model (anchor tier)

Revenue components:

- enterprise subscription,
- per-artifact write fee,
- assurance services (audit package, trust operations),
- optional simulation workload package.

Principle:

- write is paid by issuer,
- public verify remains free/near-free to maximize network adoption.

## 6) Legitimacy trigger conditions

DeciRepo can claim "network legitimacy bootstrap completed" when all are true:

1. One anchor publisher in production.
2. One independent verifier active on anchor flow.
3. Stable public verify stream (proof-only) with no critical integrity incidents.
4. Conformance and trust telemetry publicly observable.

## 7) Operational rollout phases

Phase A — Private activation:

- deploy private tenant,
- validate deterministic write/verify path,
- run incident drills and trust event logging.

Phase B — Controlled public proof:

- publish proof-only records,
- monitor external verify usage and mismatch rates.

Phase C — Ecosystem signaling:

- publish anchor case metrics,
- expose compatibility and trust evidence for additional publishers.

## 8) Risk controls

Key risks and mitigations:

1. Reputational coupling risk  
   Mitigation: strict protocol compatibility badge policy + transparent incident handling.

2. Data sensitivity risk  
   Mitigation: proof-only publication mode and private-by-default visibility.

3. Protocol drift risk  
   Mitigation: frozen version policy + mandatory conformance before production changes.

4. Vendor capture perception  
   Mitigation: public governance docs + explicit path to co-governance/foundation.

## 9) Success metrics (first 12 months)

1. Anchor artifact writes: target `>= 50k/year`.
2. Deterministic verify success rate: target `>= 99%`.
3. Rebuild match rate: target `>= 99%`.
4. Public proof verify requests: target growth month-over-month.
5. Time-to-audit-package generation: measurable reduction vs baseline process.

## 10) Exit criterion from anchor-only stage

Move from "single anchor" to "multi-publisher ecosystem" when:

1. At least `3` paying publisher organizations are active,
2. at least `1` is outside financial services,
3. external verification traffic share reaches sustained growth,
4. no unresolved critical trust incidents remain open.
