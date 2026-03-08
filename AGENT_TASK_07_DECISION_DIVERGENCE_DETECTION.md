Task:
Implement Decision Divergence Detection artifact and endpoint.

Objective:
Detect cases where structurally similar decisions resulted in different outcomes.

This module must remain deterministic and explainable.

Allowed modifications:

- create api/decision-divergence
- create api/decision-divergence.json
- update pages/precedents.html
- update pages/decision.html
- update README.md

Do NOT modify:

- protocol.json
- DLX engine
- similarity contract
- federation logic
- precedent-search endpoint

--------------------------------------------------

Definition of divergence

A divergence exists when:

decision_class matches
AND policy_family matches
AND exception_type matches
BUT outcome differs

Example:

Decision A
policy_family: AML-PROC
decision_class: vendor-risk-exception
exception_type: urgency
outcome: approved

Decision B
policy_family: AML-PROC
decision_class: vendor-risk-exception
exception_type: urgency
outcome: rejected

--------------------------------------------------

Artifact structure

Example:

{
  "reference_decision": "DR-0001",

  "divergent_decisions": [
    {
      "decision_id": "DR-0023",

      "matching_dimensions": [
        "decision_class",
        "policy_family",
        "exception_type"
      ],

      "outcome_difference": {
        "reference_outcome": "approved",
        "divergent_outcome": "rejected"
      }
    }
  ],

  "detected_at": "...",
  "protocol_version": "v0.1"
}

--------------------------------------------------

Rules

Divergence detection must:

- rely only on explicit artifact fields
- not infer motivation
- not assign blame
- not rank decisions as correct or incorrect

--------------------------------------------------

UI

Update decision.html:

Add panel:

Decision Divergence

Display:

- divergent decisions
- outcome difference
- matching dimensions

Update precedents.html:

Add optional filter:

Show divergent precedents.

--------------------------------------------------

Documentation

Add section:

"Decision Divergence Detection"

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
