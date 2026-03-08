Task:
Implement the Evidence Bundle Manifest artifact.

Objective:
Create a deterministic container that aggregates all artifacts required for a decision investigation.

Scope:
You may modify only:
- api/evidence-bundle-manifest
- api/evidence-bundle-manifest.json
- api/audit-package.json
- api/audit-package
- assets/data.js
- README.md

Do NOT modify:
- protocol.json
- DLX engine
- conformance tests
- federation logic

--------------------------------------------------

Purpose:
The Evidence Bundle Manifest acts as a "git tree" for a decision investigation. 
It provides a single hash identity for the entire set of evidence artifacts.

--------------------------------------------------

Artifact structure (JSON):
{
  "bundle_id": "EBM-...",
  "decision_id": "...",
  "generated_at": "...",
  "artifacts": [
    {
      "type": "decision_artifact",
      "uri": "/api/decision/...",
      "hash": "..."
    },
    {
      "type": "precedent_search_report",
      "uri": "/api/precedent-search-report.json",
      "hash": "..."
    },
    {
      "type": "decision_explanation",
      "uri": "/api/decision-explanation.json",
      "hash": "..."
    },
    {
      "type": "divergence_investigation_report",
      "uri": "/api/divergence-investigation-report.json",
      "hash": "..."
    }
  ],
  "manifest_identity": {
    "protocol_version": "v0.1",
    "bundle_hash": "..."
  }
}

--------------------------------------------------

Rules:
- bundle_hash must be a deterministic hash of the canonical serialization of the artifacts list.
- all references must be explicit.
- missing optional artifacts must be omitted from the list.

--------------------------------------------------

Integration:
- Update audit-package to include a reference to the evidence-bundle-manifest.

--------------------------------------------------

Validation required:
bash scripts/validate_all.sh

Success condition:
ALL VALIDATIONS PASSED

Final report format:
- files changed
- validation commands executed
- final PASS/FAIL status
- do not propose next steps
