# INDRASNET_GOVERNANCE_REGISTRY_V0_1

Status: active operational policy  
Publisher ID: `indrasnet-governance`

## 1) Purpose

Define the first internal anchor publisher for DeciRepo:

- IndrasNet Governance Registry,
- focused on protocol governance and trust operations,
- used for dogfooding with publicly verifiable decision artifacts.

## 2) Allowed publication scope

Only governance-critical records are allowed:

1. Protocol decisions.
2. RFC accept/reject decisions.
3. Trust-root operations.
4. Security/incident governance decisions.
5. Governance phase transition decisions.

Disallowed:

- marketing announcements,
- business PR records,
- non-governance corporate content.

## 3) Canonical seed records (v0.1)

1. `DR-PROTOCOL-0001` — Protocol Freeze v0.1.
2. `DR-TRUST-0001` — Trust Root Initialization.
3. `DR-CONF-0001` — Conformance Suite Release v0.1.
4. `DR-REFNODE-0001` — Reference Node Activation.
5. `DR-GOV-0001` — Governance Policy Adoption.

## 4) RFC linkage rule

For protocol/governance records, `rfc_ref` is mandatory unless an emergency-only path is declared.

Model:

`RFC -> Decision Artifact -> Published Registry Record`

## 5) Publication and visibility model

- Default visibility: private registry state is allowed for drafting.
- Governance records listed above must be published as verifiable artifacts.
- Sensitive payload may be omitted only under proof-only publication policy.

## 6) Legitimacy progression

Stage 1:

- IndrasNet Governance Registry live (publisher active).

Stage 2:

- at least one external mirror verifier validates governance artifacts.

Stage 3:

- at least one independent external registry node publishes compatible records.

## 7) Integrity controls

- All records must pass deterministic validation (`PASS`) and rebuild (`MATCH`).
- All trust-root affecting records must emit trust events.
- Any mismatch triggers challenge/recheck workflow.

## 8) Success criteria (first cycle)

1. Governance records are continuously published and verifiable.
2. Public feed clearly marks `publisher: indrasnet-governance`.
3. At least one external verifier confirms the governance stream.
4. No unresolved critical integrity incidents remain open.

