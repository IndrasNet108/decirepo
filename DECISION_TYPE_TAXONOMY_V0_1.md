# DECISION_TYPE_TAXONOMY_V0_1

Status: active taxonomy  
Applies to: `DeciRepo Protocol v0.1` and `DeciRepo Cloud by IndrasNet`

## 1) Purpose

Define canonical decision-flow classes that drive:

- ingestion priorities,
- publisher targeting,
- write-pricing strategy,
- network capacity planning.

## 2) Core principle

Economic throughput is expected to come from high-volume policy exceptions, not from low-frequency governance/security events.

## 3) Decision classes

### Class A — High-volume policy exceptions (primary flow)

Examples:

- KYC override
- AML review override
- risk waiver
- vendor risk acceptance
- policy exception

Profile:

- frequency: very high
- dispute pressure: high
- audit pressure: high
- expected role in network economics: primary write volume

### Class B — Operational governance exceptions

Examples:

- procurement exception
- privileged access approval
- segregation-of-duties override

Profile:

- frequency: medium
- dispute pressure: medium-high
- expected role in network economics: stable secondary flow

### Class C — Financial/regulatory operational actions

Examples:

- transaction unblock
- payment exception
- credit override

Profile:

- frequency: low-medium
- unit criticality: high
- expected role in network economics: high-value write flow

### Class D — Protocol/security/governance anchors

Examples:

- trust-root update
- protocol governance decision
- key rotation
- RFC acceptance

Profile:

- frequency: low
- network trust impact: very high
- expected role in network economics: anchor trust layer, not volume driver

## 4) Publisher-class model

Primary expected publisher class for scale:

1. compliance platforms
2. risk engines
3. workflow/governance systems

Secondary publisher class:

- enterprise internal committees (bank/corporate)
- public institutions and regulators

Reason:

- platform operators have repeatable high-frequency policy exception flows and lower publishing friction.

## 5) Pricing model (two-axis)

Write-pricing should be based on:

1. decision class (`A/B/C/D`)
2. artifact complexity tier (`T1/T2/T3`)

Complexity tier guidelines:

- `T1`: single-policy decision, minimal attachments
- `T2`: multi-factor decision, standard evidence package
- `T3`: multi-policy or high-assurance decision with extended evidence

Indicative write-pricing ranges (USD):

- `Class A`: `$0.50 - $1.00` per artifact
- `Class B`: `$1.00 - $2.00` per artifact
- `Class C`: `$2.00 - $5.00` per artifact
- `Class D`: `$0.00 - $0.25` per artifact for protocol/public-trust events (policy option: free)

Note:

- Class D monetization should not undermine protocol neutrality/trust governance.

## 6) Network KPI alignment

Primary throughput KPI:

- class A share of total writes (expected dominant)

Primary openness KPI:

- `external_verification_share >= 50%`

Quality KPI:

- class-level `PASS + MATCH` verification rate by publisher class

## 7) Non-breaking adoption path (v0.1)

To preserve protocol freeze in `v0.x`:

- keep taxonomy fields optional in metadata (`decision_class`, `complexity_tier`, `publisher_class`),
- enforce as required only in a future versioned profile.
