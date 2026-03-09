# PUBLIC_CHANGELOG

This changelog records only publicly significant changes.

Included:
- protocol version changes
- governance/public policy changes
- public status changes
- commerce mode changes
- public site posture changes
- public verification/network milestones

Excluded:
- internal refactors
- minor wording changes
- private operational details
- non-public infrastructure changes

---

## 2026-03-09

### First external recomputation published
Independent external recomputation of `DR-GENESIS-0001` was completed and published.

Result:
- Verification status: PASS
- Rebuild result: MATCH
- Conformance status: PASS

Published references:
- Decision Record: `https://decirepo.com/api/decision/DR-GENESIS-0001.json`
- Artifact Envelope: `https://decirepo.com/artifacts/genesis/DR-GENESIS-0001.json`
- Evidence Manifest: `https://decirepo.com/api/evidence-bundle-manifest-genesis.json`

Primary public evidence package:
- University Lab A
- Commit: `15fd8961687a1559a0b103e857fcdefa9126645b`
- Timestamp (UTC): `2026-03-09T14:04:08Z`
- Archive SHA256: `3c9741816db4e5831f93c8a050d5e6a6c6799724ead0abc9357bc85e1b2ded3c`

### Second independent recomputation confirmed
A second independent recomputation of `DR-GENESIS-0001` was also completed successfully.

Result:
- Verification status: PASS
- Rebuild result: MATCH
- Conformance status: PASS

Additional evidence package:
- OpenAI-Codex
- Commit: `15fd8961687a1559a0b103e857fcdefa9126645b`
- Timestamp (UTC): `2026-03-09T12:50:31Z`
- Archive SHA256: `b70517bbcc1c1afd3593b6bd11d94fa01d4a37480a3e397783b468013738be21`

Shared verification values across both runs:
- Expected rebuild hash: `c630adc482c72a19ef20254f80411d7bf2ad5075bdb58f2a82751761ac6d2a4e`
- Published artifact file SHA256: `9e9c6d28a16fccc8459a20dba004e933c1cc05d43dd45d126848b06506326778`

### Public site posture updated
- Main site moved to `Request Pilot` mode.
- Public self-serve checkout remains disabled.
- Billing page explicitly states pilot-by-agreement mode.
- Legal pages added: Terms, Privacy, Disclaimer, Billing.

### Commerce mode clarified
- Public commerce posture set to:
  - pilot-by-agreement
  - no public self-serve Stripe checkout

### Node operations documentation published
- Private node operations repo initialized:
  - `decirepo-node-ops`
- Operational documentation added for:
  - second verifier node operations
  - commerce readiness gate
  - release checklist
- Public independent verification template published:
  - `INDEPENDENT_VERIFICATION_NOTE_TEMPLATE_V0_1.md`

### Public protocol status
- DeciRepo remains in Genesis-phase public deployment.
- Public surface is live.
- Independent external recomputation has been confirmed by two evidence packages.

---

## 2026-03-08

### Public repository state updated
- DOI reference committed to public `decirepo`.
- Public/public-private boundary tightened.
- `evidence-corpus` moved to private visibility.

### Branch protection posture updated
- Default branch protections applied to public repositories.
- Force push and branch deletion protections confirmed on protected branches.

---

## 2026-03-07

### Genesis deployment baseline established
- Public infrastructure deployed for DeciRepo.
- Genesis artifact published:
  - `DR-GENESIS-0001`
- Public protocol messaging aligned around:
  - deterministic recomputation
  - verification
  - MATCH / FAIL

---

## Status snapshot

Current public status:
- Protocol phase: Genesis
- Verification posture: public
- Commerce posture: pilot-by-agreement
- Public self-serve checkout: disabled
- Independent verifier network: two external recomputation packages confirmed
