# PROTOCOL_STATUS

Protocol Version: `v0.1`  
Status: **Ready for Genesis** (Protocol Baseline Frozen)  
Creator: `Oleg Surkov`  
Steward: `IndrasNet OÜ`  
Next Governance Phase: `Co-Governance` (Trigger: First independent Mirror Verifier)

## Active Baseline

- Protocol constitution: `DECIREPO_PROTOCOL_CONSTITUTION_V0_1.md`
- Canonical policy: `DECIREPO_PROTOCOL_GOVERNANCE_V0_1.md`
- Neutrality charter: `DECIREPO_PROTOCOL_CHARTER_V0_1.md`
- Foundation gates: `FOUNDATION_READINESS_CRITERIA_V0_1.md`
- Handshake spec: `FEDERATION_HANDSHAKE_V0_1.md`
- Negative federation tests: `NEGATIVE_FEDERATION_TESTS_V0_1.json`
- First publisher policy: `INDRASNET_GOVERNANCE_REGISTRY_V0_1.md`
- Node discovery endpoint: `/.well-known/decirepo-node`
- Public conformance report: `/api/conformance-report`
- Network reference architecture: `DECIREPO_NETWORK_REFERENCE_ARCHITECTURE_V0_1.md`
- Category definition: `DECIREPO_CATEGORY_DEFINITION_V0_1.md`
- Core narrative: `DECIREPO_CORE_NARRATIVE_V0_1.md`
- Node deployment guide: `REFERENCE_NODE_DEPLOYMENT_GUIDE_V0_1.md`
- Network economics model: `DECIREPO_NETWORK_ECONOMICS_V0_1.md`
- Go-to-market sequence: `DECIREPO_GO_TO_MARKET_SEQUENCE_V0_1.md`
- Target operator map: `TARGET_OPERATOR_MAP_V0_1.md`
- First real operator list: `FIRST_REAL_OPERATOR_LIST_V0_1.md`
- First contact sequence: `FIRST_CONTACT_SEQUENCE_V0_1.md`
- External operator outreach kit: `FIRST_EXTERNAL_OPERATOR_OUTREACH_KIT_V0_1.md`
- First external operator scenario: `FIRST_EXTERNAL_OPERATOR_SCENARIO_V0_1.md`
- Positioning and comparison: `DECIREPO_POSITIONING_AND_COMPARISON_V0_1.md`
- Reference engine scope: `DLX_REFERENCE_ENGINE_SCOPE_V0_1.md`
- Decision-flow taxonomy: `DECISION_TYPE_TAXONOMY_V0_1.md`
- Decision precedent search: `/api/precedent-search`
- Decision precedent search report: `/api/precedent-search-report`
- Decision similarity contract: `DECISION_SIMILARITY_CONTRACT_V0_1.md`
- Decision verification primitive: `VERIFY_DECISION_SPEC_V0_1.md`
- Network reference architecture: `DECIREPO_NETWORK_REFERENCE_ARCHITECTURE_V0_1.md`
- External operator program: `FIRST_EXTERNAL_OPERATOR_PROGRAM_V0_1.md`
- Verification graph protocol: `VERIFICATION_GRAPH_SPEC_V0_1.md`
- Node-to-node verification protocol: `NODE_TO_NODE_VERIFICATION_PROTOCOL_V0_1.md`
- Verification result API normalization: `VERIFICATION_RESULT_API_SPEC_V0_1.md`
- Trust score derivation spec: `TRUST_SCORE_DERIVATION_SPEC_V0_1.md`
- Mirror verifier reference flow: `FIRST_MIRROR_VERIFIER_REFERENCE_FLOW_V0_1.md`
- Policy drift detection: `/api/policy-drift-detection`

## Current Governance State

- Trust-root signing: single steward (IndrasNet OÜ)
- Conformance authority: canonical suite maintained by current steward
- Reference node status: active
- Breaking change policy in `v0.x`: forbidden unless security-critical exception

## Phase Transition Target (to Co-Governance)

Minimum transition actions:

1. Introduce multi-party trust-root signing (`2-of-3`).
2. Enable public RFC workflow for protocol evolution.
3. Add independent mirror/reference node participation.
4. Publish open conformance CI visibility.

## Foundation Readiness Gate

Transition from Co-Governance to Foundation Stewardship is governed exclusively by:

- `FOUNDATION_READINESS_CRITERIA_V0_1.md`

Readiness decision states:

- `Not ready`
- `Conditionally ready`
- `Ready for foundation transition`

## Update Rule

This file must be updated whenever:

- protocol version changes,
- governance phase changes,
- trust-root control model changes,
- canonical governance/readiness documents are superseded.
