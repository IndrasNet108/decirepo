# DECIREPO_CLOUD_COMMERCIAL_TIER_V0_1

Status: commercial service policy  
Service brand: `DeciRepo Cloud by IndrasNet`

## 1) Service scope

Managed commercial registry layer on top of the neutral DeciRepo protocol.

Includes:

- production SLA-backed runtime,
- managed trust operations,
- enterprise connectors,
- policy packs and compliance analytics,
- onboarding and support.

## 2) Separation rule

Commercial features must not change protocol compatibility rules.

- Protocol compatibility is determined by conformance profile and tests.
- Commercial service quality is determined by SLA and managed operations.

## 3) Service tiers (v0.1 baseline)

1. Starter
   - managed registry access,
   - base verify API,
   - limited monthly decision throughput.
2. Professional
   - policy impact and lineage operations,
   - expanded API limits,
   - audit export package.
3. Enterprise
   - private managed node options,
   - high SLA and incident response,
   - advanced connectors and trust operations.

## 4) Revenue model

- Tenant subscription.
- Decision artifact write processing.
- Premium assurance modules (audit/compliance packs, managed trust ops).

Write-processing classes and indicative ranges are defined in:

- `DECISION_TYPE_TAXONOMY_V0_1.md`

## 5) Compatibility signal

Commercial node status should expose:

- protocol version,
- conformance profile,
- latest conformance report endpoint.
