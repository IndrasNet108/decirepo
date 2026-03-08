Task:
Implement deterministic rebuild of audit packages.

Objective:
Allow any audit package to be reconstructed from its referenced artifacts.

Scope:
You may modify only:

- api/audit-package
- api/audit-package.json
- assets/data.js
- README.md

Do NOT modify:

- protocol.json
- DLX engine
- conformance tests
- federation logic

Goal:
Add deterministic rebuild metadata to the audit package.

Required fields:

{
  "audit_package_id": "...",

  "artifact_refs": {
    "decision": "...",
    "verify_report": "...",
    "compare_report": "...",
    "precedent_search_report": "...",
    "policy_drift_report": "..."
  },

  "rebuild_metadata": {
    "protocol_version": "v0.1",
    "dlx_engine": "dlx-ref",
    "rebuild_hash": "...",
    "generated_at": "..."
  }
}

Rules:

- rebuild_hash must be deterministic
- artifact references must be explicit
- missing artifacts must be null or absent
- no implicit inference allowed

Purpose:

Any node must be able to verify that the audit package can be reproduced.

UI:

No new UI required.

Documentation:

Update README.md with section:

"Audit Package Rebuildability"

Validation required:

bash scripts/validate_ui_target.sh

Success condition:

ALL VALIDATIONS PASSED

Final report format:

- files changed
- validation commands executed
- final PASS/FAIL status
- do not propose next steps
