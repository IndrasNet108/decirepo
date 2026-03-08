Task:
Add a precedent evidence panel to the decision page.

Scope:
You may modify only:
- pages/decision.html
- assets/data.js
- assets/styles.css
- README.md

Do NOT modify:
- protocol.json
- DLX engine
- conformance tests
- federation logic

Objective:
Show precedent evidence as a structured retrieval context on the decision page.

Panel requirements:
- title: Precedent Evidence
- show whether precedent-search-report exists
- show selected precedent ID if available
- show result_summary if available
- show match_basis
- provide actions:
  - OPEN REPORT
  - COMPARE
  - VERIFY
  - OPEN LINEAGE

Rules:
- panel must never imply recommendation
- panel must explicitly state:
  "This panel shows retrieved precedent evidence, not a recommended decision."
- if no precedent report exists, show a neutral empty state
- do not invent precedent data

Design requirements:
- follow current dark UI style
- no layout changes outside the decision evidence area
- no new global navigation item

Validation required:
bash scripts/validate_ui_target.sh

Success condition:
ALL VALIDATIONS PASSED

Final report format:
- files changed
- validation commands executed
- final PASS/FAIL status
- do not propose next steps
