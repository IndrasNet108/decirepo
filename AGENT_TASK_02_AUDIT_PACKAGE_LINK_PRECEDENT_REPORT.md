Task:
Integrate precedent-search-report into the audit package model.

Scope:
You may modify only:
- api/audit-package
- api/audit-package.json
- pages/decision.html
- pages/precedents.html
- assets/data.js
- README.md

If api/audit-package does not yet exist, create:
- api/audit-package
- api/audit-package.json

Do NOT modify:
- protocol semantics
- DLX engine
- conformance tests
- federation logic

Objective:
Make precedent-search-report a first-class audit evidence artifact.

Required audit package contents:
- decision artifact reference
- verify report reference
- compare report reference (if available)
- policy drift report reference (if available)
- precedent-search-report reference (if available)

Rules:
- audit package must remain deterministic
- references must be explicit, not inferred
- missing optional artifacts must be represented as null or absent according to existing style
- do not fabricate compare/drift links if no source artifact exists

UI requirements:
- On decision page add AUDIT PACKAGE action
- If precedent-search-report exists, show it in the package
- If it does not exist, do not pretend it exists

Validation required:
bash scripts/validate_ui_target.sh

Success condition:
ALL VALIDATIONS PASSED

Final report format:
- files changed
- validation commands executed
- final PASS/FAIL status
- do not propose next steps
