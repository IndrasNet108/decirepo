Task:
Implement the First Mirror Verifier Reference Flow.

Objective:
Define the operational sequence for onboarding and executing the first cross-node verification cycle between a Reference Node and an independent Mirror Verifier.

Scope:
You may modify only:
- FIRST_MIRROR_VERIFIER_REFERENCE_FLOW_V0_1.md (create)
- README.md
- PROTOCOL_STATUS.md

Do NOT modify:
- protocol.json
- DLX engine
- conformance tests
- federation logic

--------------------------------------------------

Purpose:
To move from protocol theory to operational network reality by defining exactly how the first external node interacts with the reference node.

--------------------------------------------------

Deliverables:
1. Create FIRST_MIRROR_VERIFIER_REFERENCE_FLOW_V0_1.md describing:
   - discovery phase
   - artifact resolution phase
   - cross-node verification execution
   - result reporting and graph update
2. Update README.md and PROTOCOL_STATUS.md.

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
