# DeciRepo Strategy (Dual-Track: Protocol + Cloud)

## 1) Product framing

Single product for market:

- `DeciRepo` = decision infrastructure

Internal layers:

- `DLX` = execution/validation engine
- `Registry` = decision artifact storage and retrieval
- `Policy Impact` = simulation/recompute layer
- `Lineage` = graph/context layer

External message:

- "DeciRepo is a verifiable decision registry powered by DLX."

## 2) Dual-track operating model (mandatory)

`DeciRepo` evolves through two clearly separated layers:

1. Neutral infrastructure layer: `DeciRepo Protocol`
2. Commercial managed layer: `DeciRepo Cloud by IndrasNet`

### 2.1 Neutral protocol layer

Scope:

- open artifact + verify + lineage + discovery specifications,
- open conformance criteria and compatibility badge,
- root-of-trust governance with phased path to co-governance/foundation.

Goal:

- maximize adoption, interoperability, and long-term standard viability.

### 2.2 Commercial managed layer

Scope:

- production runtime and managed operations,
- SLA-backed registry service,
- connectors, policy packs, managed trust operations, compliance analytics.

Goal:

- fast revenue and operational differentiation while remaining protocol-compatible.

## 3) Strategic choice: SaaS-first GTM, protocol-first architecture

Chosen model:

- `Protocol-first architecture, SaaS-first go-to-market`

Why:

- SaaS gives fast revenue and control over pilot quality.
- Protocol gives long-term network effects, interoperability, and defensibility.

Execution:

- Sell private DeciRepo tenants now.
- Standardize open artifact/verify/lineage schema in parallel.

## 4) Default visibility policy (critical)

Decision:

- `Private by default, publish by policy.`

Rules:

- Tenant-level default visibility: `private`.
- Decision-level visibility override: `private | organization | public`.
- Optional public proof mode: publish hash + verification status without full payload.
- Public feed includes only explicitly published records.

Why:

- Faster enterprise adoption.
- Lower legal/compliance friction.
- Enables gradual transition to public registry.

## 5) ICP and adoption sequence

Primary ICP (first revenue):

- Corporate risk/compliance committees
- Procurement exception workflows
- Internal audit and sanctions governance teams

Expansion order:

1. Corporate
2. Financial institutions
3. Regulators
4. Public governance

## 6) 6/12/24 month roadmap

### 0-6 months (Pilot to repeatability)

Build:

- Stable 6-screen core: Registry, Decision, Verify, Diff, Policy Impact, Lineage
- Publisher Onboarding: Manual, API Push, Batch Import
- Private tenant model + role-based access
- Basic API package (`/decision`, `/verify`, `/lineage`, `/feed`)

Targets:

- 3-5 paid pilots
- 50k+ decisions/month total throughput
- 90%+ decisions with PASS+MATCH verification

### 6-12 months (Productization)

Build:

- Multi-tenant controls and audit exports
- Policy pack versioning and rollback
- Scheduled recompute jobs for Policy Impact
- Data connectors (GRC/ticketing/warehouse)

Targets:

- 10-20 paying organizations
- Net revenue retention > 100%
- Decision ingestion latency < 5 min for API push flows

### 12-24 months (Network effects)

Build:

- Public publish gateway (opt-in)
- Federated verification model across registries
- Protocol spec v1 (artifact, verify, lineage events)
- Ecosystem tooling (SDKs, webhooks, validation CLI)

Targets:

- 100+ organizations
- Public registry participation from multiple sectors
- Protocol adoption by third-party integrators

## 7) Unit economics (starter model)

Pricing shape:

- Platform fee per tenant
- Usage fee per decision artifact processed
- Premium for simulation workloads (Policy Impact runs)

Reference assumptions:

- Tenant base fee: $2k-$10k/month (tiered by controls/SLA)
- Processing fee: $0.01-$0.10 per decision
- Simulation package: fixed monthly quota + overage

Gross margin drivers:

- Storage efficiency for artifacts
- Simulation compute scheduling
- Support load per tenant

Target profile:

- Gross margin 75%+ after scale
- CAC payback under 12 months for enterprise segment

Decision-flow economics baseline is defined in:

- `DECISION_TYPE_TAXONOMY_V0_1.md`

## 8) What to build next (immediate)

1. `Publisher Onboarding` screen with channel stats (`published/pending/rejected`)
2. `Public Feed` as event stream (`published`, `verified`, `recalculated`)
3. Visibility controls (`private/public`) at decision and tenant level
4. Signed artifact envelope format (spec draft)
5. `dlx-ref` skeleton for neutral executable protocol semantics (`verify/rebuild/validate/conformance`)
6. `/api/conformance-report` with latest CI verdict and compatibility status
7. `decision precedent search` MVP endpoint (`/api/precedent-search`)
8. `precedent console` UI (`/pages/precedents.html`) with deterministic match-basis output
9. `precedent search report` artifact (`/api/precedent-search-report`) for audit-ready evidence
10. `policy drift detection` endpoint (`/api/policy-drift-detection`) with rule-delta explainability

## 8.1) First anchor publisher (dogfooding)

Initial anchor publisher: `IndrasNet Governance Registry` with strict scope:

- protocol decisions,
- RFC decisions,
- trust-root operations,
- security governance events.

Policy is fixed in `INDRASNET_GOVERNANCE_REGISTRY_V0_1.md`.

## 9) 90-day execution priorities

1. Publish protocol charter with neutrality commitments.
2. Launch independent verification + implementation grants.
3. Launch paid managed registry tier (`DeciRepo Cloud by IndrasNet`).
4. Expose compliance-ready API report endpoint (`/api/conformance-report`).
5. Adopt decision-flow taxonomy (`A/B/C/D`) for pipeline prioritization and pricing controls.

Primary balance KPI:

- `external_verification_share >= 50%`

## 10) Operating principle

Do not split into separate brands/products at this stage.

- Brand: `DeciRepo`
- Engine mention: `Powered by DLX`
- Features: Verify, Diff, Policy Impact, Lineage as product modules

## 11) Registry control model (publication vs public interest)

Control should be layered, not centralized in one actor.

- `Tenant control`: organization owns its private decisions and publication policy.
- `Protocol control`: open artifact/verify/lineage spec managed through versioned RFC process.
- `Trust control`: verification keys and validator policies published in a transparent trust registry.

Practical rules:

- Publication defaults to private.
- Public publication requires explicit policy and legal scope.
- Immutable audit log for publication and verification events.
- Policy/spec changes require public changelog and compatibility window.

Target outcome:

- Prevent unilateral censorship or silent rule drift.
- Keep enterprise adoption feasible while enabling public-interest verification.

Operationalization:

- `Root of Trust` policy is published as machine-readable endpoint (`/api/root-of-trust`)
  and rendered in UI (`/pages/root-of-trust.html`) with admission, reputation, governance,
  and revocation rules.
- `Trust Score` is exposed per registry (`/api/trust-score`) using a transparent weighted model
  for verify/rebuild/uptime/policy compatibility and incident penalties.
- `Verification Graph` (`/api/verification-graph`) and `Trust Events` (`/api/trust-events`)
  form the auditable trust telemetry layer.
- `Precedent Search` (`/api/precedent-search`) provides deterministic similar-decision lookup.
- `Policy Drift Detection` (`/api/policy-drift-detection`) quantifies outcome drift under policy change.
- Signed node manifests and handshake flow are documented in `FEDERATION_HANDSHAKE_V0_1.md`.
- Challenge/recheck lifecycle is exposed through `/api/challenges` and `/api/rechecks`
  to support dispute resolution and deterministic revalidation.
- Protocol governance policy is fixed in `DECIREPO_PROTOCOL_GOVERNANCE_V0_1.md`.
- Foundation transition gates are fixed in `FOUNDATION_READINESS_CRITERIA_V0_1.md`.
- Decision classes and publisher-class targeting are fixed in `DECISION_TYPE_TAXONOMY_V0_1.md`.
- Decision precedent lookup contract is fixed in `DECISION_PRECEDENT_SEARCH_V0_1.md`.
- Policy drift detection contract is fixed in `DECISION_POLICY_DRIFT_DETECTION_V0_1.md`.
