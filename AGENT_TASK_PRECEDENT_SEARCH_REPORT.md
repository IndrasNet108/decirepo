AGENT TASK
Task

Implement an immutable precedent-search-report artifact and endpoint.

This artifact will allow precedent search results to be included in audit packages.

Scope

You are allowed to modify or create only:

api/precedent-search-report.json
api/precedent-search-report
assets/data.js
pages/precedents.html
README.md

Do NOT modify:

protocol.json
DLX engine
conformance tests
federation logic
Objective

Add a deterministic artifact describing the results of a precedent search query.

The artifact must represent:

query context
match basis
result summary
precedent candidates
selected precedent

This artifact must be suitable for inclusion in an audit package.

Endpoint

Create:

/api/precedent-search-report
/api/precedent-search-report.json

The endpoint must return a deterministic JSON object.

Example structure:

{
  "report_id": "PSR-0001",
  "generated_at": "2026-03-07T12:00:00Z",

  "query_context": {
    "decision_id": "DR-0001",
    "decision_class": "A",
    "policy_version": "RISK_POLICY_V3",
    "search_mode": "by_decision_id"
  },

  "match_basis": [
    "same_decision_class",
    "same_policy_version"
  ],

  "result_summary": {
    "total_precedents": 12,
    "approved": 9,
    "rejected": 3
  },

  "precedent_candidates": [
    {
      "decision_id": "DR-0008",
      "outcome": "approved",
      "publisher": "indrasnet-governance"
    }
  ],

  "selected_precedent": "DR-0008"
}
UI Integration

Update:

pages/precedents.html

When a precedent is selected:

enable OPEN REPORT

link to:

/api/precedent-search-report

The report must reflect the currently selected precedent context.

Constraints

The report must be:

deterministic
explainable
non-recommendational

Add a visible disclaimer:

Precedents are retrieval results.
They are not recommendations.
Validation Required

Run:

bash scripts/validate_ui_target.sh
Success Condition

The task is complete only if:

ALL VALIDATIONS PASSED
Expected Report Format

After completion report only:

files changed
validation commands executed
final PASS/FAIL status

Do not propose new architectural features.
