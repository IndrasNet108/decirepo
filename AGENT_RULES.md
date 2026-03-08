You are editing the DeciRepo reference implementation.

Constraints:

1. Protocol is authoritative.
   See:
   api/protocol.json

2. protocol.json is immutable without explicit instruction.
   Do not "optimize" or change endpoints silently.

3. Any change affecting:
   - registry
   - protocol
   - artifacts
   - federation
   must preserve conformance.

4. After editing code you must run:
   bash scripts/validate_all.sh

5. If tests fail:
   stop and report failure. Do not attempt to guess a fix without reading logs.

6. Do not guess missing context.
   If unsure, read the relevant file first.

7. Never modify UI logic without reading the full file first.
   Partial reads lead to broken DOM references.

8. After completing the requested change:
   - Report only: files changed, validation commands executed, and final pass/fail status.
   - Do not propose next architectural steps unless explicitly asked.
   - Do not infer roadmap priorities from previous discussion.
