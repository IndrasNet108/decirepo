Task:
Implement Divergence Investigation Report artifact and endpoint.

Objective:
Create a deterministic investigation artifact for decision divergence cases.

This artifact must support audit and compliance review when
structurally similar decisions produced different outcomes.

Allowed modifications:

- create api/divergence-investigation-report
- create api/divergence-investigation-report.json
- update api/audit-package
- update api/audit-package.json
- update pages/decision.html
- update README.md

Do NOT modify:

- protocol.json
- DLX engine
- precedent-search endpoint
- similarity contract
- federation logic

--------------------------------------------------

Purpose

The report must formalize divergence review context.

It must not:
- infer intent
- assign blame
- label any decision as correct or incorrect
- claim bias detection

It may only:
- describe structural divergence
- expose explicit matching dimensions
- expose explicit outcome differences
- provide linked evidence context

--------------------------------------------------

Artifact structure

Example:

{
  "report_id": "DIR-0001",
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
      },

      "linked_evidence": {
        "compare": "/pages/diff.html?left=DR-0001&right=DR-0023",
        "verify": "/pages/verify.html?id=DR-0023",
        "decision_explanation": "/api/decision-explanation.json",
        "precedent_search_report": "/api/precedent-search-report.json"
      }
    }
  ],

  "investigation_basis": [
    "same decision_class",
    "same policy_family",
    "same exception_type",
    "different outcome"
  ],

  "generated_at": "2026-03-07T12:00:00Z",
  "protocol_version": "v0.1"
}

--------------------------------------------------

Rules

The report must be:

- deterministic
- explicit
- non-recommendational
- suitable for audit packages

Missing linked evidence must be represented as null or absent.
No inferred evidence links are allowed.

--------------------------------------------------

Audit package integration

Update audit-package to include:

"divergence_investigation_report": "..."

if divergence evidence exists.

Do not fabricate this field when no divergence report exists.

--------------------------------------------------

UI

Update decision.html:

Add action:
OPEN DIVERGENCE REPORT

Add a small Divergence Investigation section that links to the report
when divergence data exists.

No new navigation item.

--------------------------------------------------

Documentation

Add section to README.md:

"Divergence Investigation Report"

The section must clearly state:
- divergence is an investigation signal
- divergence is not proof of bias or error

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
