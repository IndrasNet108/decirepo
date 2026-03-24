# DECIREPO_GENESIS_EVIDENCE_LAYER_V0_1

Status: Public appendix  
Scope: Genesis artifact proof layer and verification references

---

## 1. Purpose

This appendix records the public evidence layer around the DeciRepo genesis artifact:

- `DR-GENESIS-0001`

It is not a replacement for the protocol specification or the lineage note.
Its purpose is narrower:

- to identify the first public root artifact,
- to record its public verification status,
- and to point to the machine-checkable references that make the genesis state independently auditable.

---

## 2. Public Root

The first public genesis artifact for the DeciRepo protocol surface is:

- `decision_id`: `DR-GENESIS-0001`

Public references:

- Artifact JSON: `https://decirepo.com/artifacts/genesis/DR-GENESIS-0001.json`
- Decision Record: `https://decirepo.com/api/decision/DR-GENESIS-0001.json`

This artifact functions as the first published root of trust for the public DeciRepo verification surface.

---

## 3. Verification Status

The published genesis artifact records:

- `validator_result: PASS`
- `rebuild_result: MATCH`
- `conformance: PASS`

These three states matter for different reasons:

- `PASS` means the validator accepted the artifact under the active profile,
- `MATCH` means deterministic recomputation produced the same artifact identity,
- `conformance: PASS` means the artifact and verification surface remain consistent with the published protocol baseline.

Together, they establish that the genesis artifact is not only published, but reproducibly verifiable.

---

## 4. Artifact Identity

Published identity values:

- `artifact_hash: c630adc482c72a19ef20254f80411d7bf2ad5075bdb58f2a82751761ac6d2a4e`
- `rebuild_result_hash: c630adc482c72a19ef20254f80411d7bf2ad5075bdb58f2a82751761ac6d2a4e`
- `artifact_hash_semantics: rebuild_result_hash`
- `rebuild_hash_expected: c630adc482c72a19ef20254f80411d7bf2ad5075bdb58f2a82751761ac6d2a4e`

Why this matters:

- the public artifact identity is not left ambiguous,
- the rebuild identity and published identity are aligned,
- and the semantics of the hash are explicitly declared rather than implied.

This is part of what allows an independent node to verify the artifact without relying on the origin node's internal explanation.

---

## 5. Rebuild Source Context

Published `rebuild_source` values include:

- `authority: IndrasNet Protocol Steward`
- `publisher: indrasnet-governance`
- `policy_version: DECIREPO_PROTOCOL_CONSTITUTION_V0_1`
- `network_status: genesis`
- `steward_id: indrasnet-steward-001`
- `target_verification_density: 1`

This context matters because the genesis artifact is not just a hash.
It is a public root published within a declared governance and protocol context.

The artifact therefore binds:

- a specific decision identifier,
- a specific protocol constitution,
- and a specific genesis network posture.

---

## 6. Transition Chain

The genesis artifact publishes the following transition chain:

1. `DRAFT -> PROPOSED`  
   `evidence_hash: 976a2b5455edbf7b02102501d236e07b0312046fca8946a79cacb2cb58d05944`

2. `PROPOSED -> VALIDATED`  
   `evidence_hash: 9c3e2c057d035f690b892503382f8594a811e7ce042c6506987291f078091709`

3. `VALIDATED -> PUBLISHED`  
   `evidence_hash: bed2693ec9f38f7abb62dd82172e16837a800d49ab3c972209b85f54eee5e4c8`

This means the public genesis root is not presented as a flat final assertion only.
It carries a published state progression with evidence hashes for each transition.

In practical terms:

- genesis is not just "published";
- genesis is published together with a declared transition path into publication.

---

## 7. Evidence Bundle References

The published artifact also points to its supporting verification layer:

- `artifact_file_sha256_uri: /artifacts/genesis/DR-GENESIS-0001.sha256`
- `decision_record_sha256_uri: /api/decision/DR-GENESIS-0001.sha256`
- `evidence_manifest_uri: /api/evidence-bundle-manifest-genesis.json`
- `evidence_manifest_sha256_uri: /api/evidence-bundle-manifest-genesis.sha256`

These references matter because the genesis artifact is not an isolated file.
It sits inside a public bundle structure with:

- integrity references,
- machine-readable manifest paths,
- and reproducible verification entry points.

---

## 8. Public Verification Command

Published verification command:

```text
$ node dlx-ref/cli.js verify artifacts/genesis/DR-GENESIS-0001.json
status=PASS
rebuild=MATCH
conformance=PASS
```

This command is the public minimal proof that an independent node can:

- retrieve the genesis artifact,
- recompute it,
- and compare the rebuild result against the published identity.

The significance is not only that the command exists,
but that it yields a reproducible PASS / MATCH / PASS surface rather than a trust-me narrative.

---

## 9. Why This Matters

The genesis evidence layer matters because it establishes that the public DeciRepo network surface did not begin from opaque declaration alone.

It began from:

- a machine-readable root artifact,
- explicit identity values,
- published transition hashes,
- and independent recomputation semantics.

That is the first public technical answer to a simpler trust problem:

- a network should not depend on an uncheckable claim at one node.

Genesis therefore functions as both:

- a technical starting point,
- and a public trust posture statement.

---

## 10. Scope Boundary

This appendix does **not** attempt to:

- describe the full DLX runtime,
- replace the DeciRepo formal specification,
- or explain every downstream artifact and protocol module.

Its scope is narrower:

- the public genesis artifact,
- the evidence references attached to it,
- and the verification posture that makes it independently auditable.

---

## 11. Related Public References

- `INDRASNET_TO_DECIREPO_LINEAGE_V0_1.md`
- `PUBLIC_CHANGELOG.md`
- `DECIREPO_PROTOCOL_CONSTITUTION_V0_1.md`
- `https://decirepo.com/artifacts/genesis/DR-GENESIS-0001.json`
- `https://decirepo.com/api/decision/DR-GENESIS-0001.json`
- `https://decirepo.com/api/evidence-bundle-manifest-genesis.json`
