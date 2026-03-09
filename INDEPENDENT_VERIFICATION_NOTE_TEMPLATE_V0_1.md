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
- Artifact hash (SHA256): `<hash>`
- Source URI: `<artifact_url>`

## Procedure

Command executed:

```bash
node dlx-ref/cli.js verify DR-GENESIS-0001
```

Optional conformance command:

```bash
node dlx-ref/cli.js conformance DR-GENESIS-0001
```

## Result

- Verification result: `MATCH | FAIL`
- Rebuild result: `<value>`
- Validator result: `<value>`
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

