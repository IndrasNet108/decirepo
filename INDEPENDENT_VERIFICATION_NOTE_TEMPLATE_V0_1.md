# INDEPENDENT_VERIFICATION_NOTE_TEMPLATE_V0_1

Use this template for the first and subsequent independent verification publications.

Purpose:
- publish one external recomputation event in a machine-readable and human-readable form;
- confirm that verification happened outside the origin operator environment.

Status rule:
- publish only after an actual external run;
- if evidence is incomplete, do not publish.

---

## Independent Verifier

- Verifier organization or individual: `<name>`
- Contact or public reference: `<url_or_email>`
- Operator role: `external mirror verifier`

## Node Context

- Node environment summary: `<os/runtime/commit>`
- Registry ID: `<registry_id>`
- Protocol version: `DeciRepo v0.1`

## Artifact Under Verification

- Artifact ID: `DR-GENESIS-0001`
- Artifact envelope URI: `/artifacts/genesis/DR-GENESIS-0001.json`
- Artifact envelope SHA256 URI: `/artifacts/genesis/DR-GENESIS-0001.sha256`
- Artifact file SHA256: `<sha256_of_artifact_file>`
- Rebuild result hash: `<rebuild_result_hash>`
- Hash semantics: `artifact_hash` in the envelope is `rebuild_result_hash` in `v0.1`
- Decision record URI: `/api/decision/DR-GENESIS-0001.json`
- Decision record SHA256 URI: `/api/decision/DR-GENESIS-0001.sha256`
- Evidence manifest URI: `/api/evidence-bundle-manifest-genesis.json`
- Evidence manifest SHA256 URI: `/api/evidence-bundle-manifest-genesis.sha256`

## Procedure

Verification command executed:

```bash
node dlx-ref/cli.js verify artifacts/genesis/DR-GENESIS-0001.json
```

Deterministic rebuild command:

```bash
node dlx-ref/cli.js rebuild artifacts/genesis/DR-GENESIS-0001.json
```

Optional conformance command:

```bash
node dlx-ref/cli.js conformance dlx-ref/tests/conformance_v0_1.json
```

## Result

- Verification status: `PASS | FAIL`
- Rebuild match: `MATCH | MISMATCH`
- Overall publication result: `MATCH | FAIL`
- Verifier node ID: `<node_id>`
- Timestamp (UTC): `<YYYY-MM-DDTHH:MM:SSZ>`

## Evidence

- Command output (redacted if needed): `<path_or_block>`
- Evidence hash (SHA256): `<hash>`
- Additional logs: `<path_or_url>`

## Scope Clarification

This note confirms reproducibility by independent recomputation.

It does **not** assert:
- legal correctness,
- normative legitimacy,
- policy appropriateness.

## Publication

- Published by: `IndrasNet OÜ`
- Publication date (UTC): `<YYYY-MM-DD>`
- Linked in: `PUBLIC_CHANGELOG.md`
