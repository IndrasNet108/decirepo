Task:
Create a formal Decision Similarity Contract for precedent retrieval.

Objective:
Define deterministic rules for how DeciRepo determines and explains
similarity between decisions without introducing recommendation logic.

This is a governance + protocol support document, not a search engine implementation.

Output file:
DECISION_SIMILARITY_CONTRACT_V0_1.md

Allowed modifications:
- create DECISION_SIMILARITY_CONTRACT_V0_1.md
- update README.md to reference the document
- update PROTOCOL_STATUS.md if needed

Do NOT modify:
- protocol.json
- dlx engine
- precedent-search endpoint
- federation logic
- UI pages

Purpose:
Ensure precedent-search and precedent-search-report operate under a clear,
deterministic similarity discipline.

The contract must define the following sections.

--------------------------------------------------

1. Purpose

Explain that similarity is used only for:
- candidate retrieval
- precedent comparison context

Similarity MUST NOT imply recommendation or authority.

--------------------------------------------------

2. Similarity Dimensions

Define the canonical similarity axes.

Mandatory dimensions:

- decision_class
- policy_family
- policy_version (or compatible policy lineage)

Optional dimensions:

- exception_type
- outcome_family
- authority_class
- publisher_class
- temporal proximity

Each dimension must specify:

- field name
- match rule
- whether mismatch disqualifies similarity.

--------------------------------------------------

3. Mandatory Match Conditions

A decision may only be considered a valid precedent candidate if:

- decision_class matches
- policy_family matches

If either condition fails, the decision must be excluded from
precedent candidate sets.

--------------------------------------------------

4. Similarity Basis

Each precedent result must expose explicit match basis.

Example:

match_basis:
- decision_class
- policy_family
- outcome_family

Mismatch fields must also be visible.

Example:

mismatch:
- policy_version
- publisher_class

--------------------------------------------------

5. Ranking Discipline

Ranking must be explainable and structured.

Allowed ranking modes:

- same-policy precedents
- same-class precedents
- outcome-divergent precedents

Forbidden ranking claims:

- "best precedent"
- "recommended precedent"
- "most relevant precedent"

--------------------------------------------------

6. Precedent Exclusion Rules

Define cases where a decision MUST NOT be returned as precedent.

Examples:

- incompatible policy family
- incompatible decision class
- unresolved policy ambiguity
- artifact validation failure

--------------------------------------------------

7. Precedent Search Report Requirements

Define mandatory fields for precedent-search-report artifact.

Example structure:

{
  "reference_decision": "...",
  "candidate_precedents": [...],
  "similarity_dimensions_used": [...],
  "exclusion_rules_applied": [...],
  "retrieval_timestamp": "..."
}

--------------------------------------------------

8. Governance Rules

The similarity contract:

- must be versioned
- must not change silently
- must remain compatible with precedent-search artifacts.

Breaking changes require a protocol RFC.

--------------------------------------------------

9. Scope Boundary

This contract governs:

- similarity logic
- precedent candidate eligibility
- explanation structure

It does NOT govern:

- UI presentation
- ranking heuristics beyond defined modes
- enterprise analytics layers.

--------------------------------------------------

Documentation updates:

Add to README.md under specifications index.

--------------------------------------------------

Validation required:

bash scripts/validate_ui_target.sh

Success condition:

ALL VALIDATIONS PASSED

--------------------------------------------------

Final report format:

- files changed
- validation commands executed
- final PASS/FAIL status

Do not propose next steps.
