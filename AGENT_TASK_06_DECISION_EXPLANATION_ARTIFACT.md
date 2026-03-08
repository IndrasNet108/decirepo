Task:
Implement a deterministic Decision Explanation Artifact.

Objective:
Provide structured explanation of how a decision relates to
precedents, policy context, and outcome.

This artifact must be deterministic and suitable for audit packages.

Allowed modifications:

- create api/decision-explanation
- create api/decision-explanation.json
- update api/audit-package
- update api/audit-package.json
- update pages/decision.html
- update README.md

Do NOT modify:

- protocol.json
- DLX engine
- precedent-search endpoint
- federation logic
- similarity contract

--------------------------------------------------

Artifact structure

Example:

{
  "decision_id": "DR-0001",

  "policy_context": {
    "policy_family": "...",
    "policy_version": "...",
    "authority": "..."
  },

  "precedent_context": {
    "reference_precedents": [
      {
        "decision_id": "...",
        "match_basis": ["decision_class","policy_family"],
        "similarity_score": 0.84
      }
    ]
  },

  "decision_outcome": {
    "outcome": "...",
    "exception_type": "...",
    "authority_action": "approve|reject|override"
  },

  "explanation_basis": [
    "same policy family precedent",
    "matching decision class",
    "exception pattern observed"
  ],

  "generated_at": "...",
  "protocol_version": "v0.1"
}

--------------------------------------------------

Requirements

The explanation must:

- use only explicit artifact fields
- not generate narrative reasoning
- not infer intent or recommendation
- remain reproducible across nodes

--------------------------------------------------

Audit package integration

The audit-package artifact must include:

decision_explanation reference

Example:

{
  "audit_package_id": "...",
  "decision": "...",
  "precedent_search_report": "...",
  "decision_explanation": "...",
  "verify_report": "..."
}

--------------------------------------------------

UI

Update decision.html to display:

Decision Explanation panel:

- policy context
- precedent context
- explanation basis

--------------------------------------------------

Documentation

Add section:

"Decision Explanation Artifact"

to README.md.

--------------------------------------------------

Validation required:

bash scripts/validate_ui_target.sh

--------------------------------------------------

Success condition:

ALL VALIDATIONS PASSED

--------------------------------------------------

Final report format:

- files changed
- validation commands executed
- final PASS/FAIL status

Do not propose next steps.
