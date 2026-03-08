Task:
Implement the immutable precedent-search-report artifact and endpoint.

Scope:
You may modify only:
- api/precedent-search-report
- api/precedent-search-report.json
- assets/data.js
- pages/precedents.html
- README.md

Do NOT modify:
- api/protocol.json
- DLX engine
- conformance tests
- federation logic

Objective:
Create a deterministic precedent-search-report artifact suitable for audit packages.

Required JSON structure:
- report_id
- generated_at
- query_context
- match_basis
- result_summary
- precedent_candidates
- selected_precedent

Rules:
- Precedents are retrieval results, not recommendations.
- match_basis is mandatory.
- selected_precedent must be explicit and never inferred automatically.
- report output must be deterministic.

UI requirements:
- Add OPEN REPORT action in precedents.html
- The report must reflect the currently selected precedent context
- Show visible disclaimer:
  "Precedents are retrieval results. They are not recommendations."

Validation required:
bash scripts/validate_ui_target.sh

Success condition:
ALL VALIDATIONS PASSED

Final report format:
- files changed
- validation commands executed
- final PASS/FAIL status
- do not propose next steps
