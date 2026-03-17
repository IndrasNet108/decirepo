# DECIREPO_PROTOCOL_CONFORMANCE_V0_1

Status: Draft

## Scope

This document defines the conformance and compatibility verification procedures for implementations claiming compatibility with the protocol boundary formalized in:

```text
DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2.md
```

This conformance profile applies to the frozen public baseline semantics of `DeciRepo Protocol v0.1` as formalized by the `v0.2` draft specification.

Version mapping for this document:

```text
Conformance Profile: V0_1
Protocol Specification: v0.2
Protocol Semantics Baseline: v0.1
```

This conformance profile defines compatibility testing for DeciRepo Protocol Formal Specification `v0.2` implementing baseline semantics of protocol version `v0.1`.

The purpose of this document is to ensure that independent implementations:

- produce identical artifact identities;
- execute the same mandatory verification procedure;
- produce identical normalized verification results;
- when processing identical protocol artifacts.

This document does not define the protocol itself.
It defines how protocol conformance is verified.

## Scope Support Artifacts

The bounded-completeness support artifacts for this profile are:

- `DECIREPO_SEMANTICS_KERNEL_V0_1.md`
- `conformance/SEMANTICS_KERNEL_V0_1.json`
- `conformance/DOMAIN_PROFILE_V0_1.json`
- `conformance/CASE_CLASS_MATRIX_V0_1.json`
- `conformance/GAP_CLASSIFICATION_V0_1.json`
- `conformance/BOUNDED_COMPLETENESS_STATUS_V0_1.json`
- `conformance/generated_corpus_v0_1/manifest.json`
- `conformance/domain_guided_generated_corpus_v0_1/manifest.json`
- `conformance/boundary_corpus_v0_1/manifest.json`
- `conformance/adversarial_corpus_v0_1/manifest.json`
- `conformance/malformed_corpus_v0_1/manifest.json`

These artifacts clarify domain membership, bounded evaluation order, case-class coverage, empirical corpus provenance, and the currently known gap boundary for profile `V0_1`.
They do not override published canonical vectors.

## 1. Conformance Definition

An implementation is considered DeciRepo-compatible for the `v0.1` baseline if and only if it satisfies all of the following conditions:

1. it accepts artifacts conforming to the DeciRepo artifact model;
2. it computes the same canonical artifact serialization;
3. it produces identical artifact identities;
4. it executes the mandatory verification procedure;
5. it produces identical normalized verification results.

Failure to satisfy any of the above conditions means the implementation MUST NOT claim DeciRepo compatibility for the baseline covered by this profile.

## 2. Conformance Test Method

Conformance is verified using canonical protocol test vectors.

Each test vector includes:

- artifact input;
- canonical serialization;
- expected artifact identity;
- expected verification result.

Implementations MUST reproduce these results exactly.

## 3. Canonical Test Vector Format

Each conformance vector MUST include the following elements:

```text
artifact.json
canonical_bytes.hex
expected_artifact_id.txt
expected_verification_result.json
expected_verification_result.canonical.hex
vector_manifest.json
```

Definitions:

`artifact.json`
The artifact in protocol-defined structure form.

`canonical_bytes.hex`
The canonical serialized byte sequence of the protocol identity surface used for hashing.

`expected_artifact_id.txt`
The expected identity hash derived from canonical serialization.

`expected_verification_result.json`
The expected normalized verification output.

`expected_verification_result.canonical.hex`
The canonical serialized byte sequence of the normalized verification result object.

`vector_manifest.json`
The vector metadata binding the fixture to a protocol baseline, canonicalization rules, hash function, and verification command.

## 4. Canonical Test Vector Set

The reference conformance vectors are stored in:

```text
conformance/v0_1/
```

Canonical directory structure:

```text
conformance/
  v0_1/
    vector_001_genesis/
      artifact.json
      canonical_bytes.hex
      expected_artifact_id.txt
      expected_verification_result.json
      expected_verification_result.canonical.hex
      vector_manifest.json
```

The currently published vector set includes:

```text
vector_001_genesis
vector_002_invalid_structure
vector_003_identity_mismatch
vector_004_verification_failure
vector_005_transition_chain_invalid
vector_006_rebuild_source_invalid
vector_007_unknown_envelope_field
```

Published vector purposes:

- `vector_001_genesis`: baseline PASS case
- `vector_002_invalid_structure`: invalid artifact structure
- `vector_003_identity_mismatch`: expected identity or rebuild-hash mismatch
- `vector_004_verification_failure`: rule-level verification failure on otherwise structured artifact
- `vector_005_transition_chain_invalid`: invalid transition-chain semantics under `validate`
- `vector_006_rebuild_source_invalid`: invalid rebuild-source surface under `rebuild`
- `vector_007_unknown_envelope_field`: single unknown top-level field outside `artifact.rebuild_source` does not affect baseline `verify` identity or normalized result

Published vectors MUST NOT be modified once released.
New vectors MUST be added as new fixtures rather than by rewriting an existing canonical vector.

## 5. Verification Result Surface

Verification output MUST conform to the normalized verification result surface defined by the formal specification.

For this conformance profile, the normalized verification result object MUST have the following structure:

```json
{
  "status": "PASS | FAIL | CONFORMANCE_ERROR",
  "artifact_id": "<hash>",
  "reason_codes": [],
  "protocol_version": "v0.1",
  "verifier_result_schema": "decirepo-verifier-result-v0.1"
}
```

Definitions:

`status`
Possible values:

```text
PASS
FAIL
CONFORMANCE_ERROR
```

`artifact_id`
The computed artifact identity.

`reason_codes`
An ordered list of protocol reason codes. The list MUST be deterministic and lexicographically ordered.

`protocol_version`
The protocol version bound to the verification result.

`verifier_result_schema`
The normalized verifier result schema identifier.

When compared as canonical normalized result bytes, verification outputs MUST match the canonical expected results byte-for-byte.

## 5.1 Result Canonicalization

Canonical normalized verification result bytes for this profile MUST use:

```text
decirepo-result-c14n-v1
```

`decirepo-result-c14n-v1` is defined as:

1. deterministic JSON serialization;
2. UTF-8 encoding;
3. lexicographically sorted object keys;
4. preserved array order;
5. lowercase hexadecimal encoding where hex values appear;
6. no fields outside the normalized verification result surface.

For conformance mode:

- absent and `null` MUST be treated as different states;
- fields outside the normalized result surface MUST NOT appear in canonical result bytes;
- whitespace outside canonical JSON serialization MUST NOT affect canonical result bytes.

## 5.2 Extension Policy

Implementations MAY emit additional diagnostic fields outside the normalized verification result object.

However:

1. extension fields MUST NOT participate in canonical normalized result bytes;
2. extension fields MUST NOT alter the protocol result surface;
3. extension fields MUST NOT appear in `expected_verification_result.canonical.hex`;
4. extension fields are forbidden inside the normalized result object during conformance comparison.

## 6. Reason Code Registry

The following protocol-defined reason codes are normative for the baseline verifier semantics:

```text
SCHEMA_VERSION_INVALID
ARTIFACT_HASH_INVALID
VALIDATOR_RESULT_INVALID
REBUILD_RESULT_INVALID
PASS_REQUIRES_MATCH
REBUILD_HASH_EXPECTED_MISMATCH
REBUILD_SOURCE_INVALID
TRANSITION_CHAIN_INVALID
```

Definitions for the published vector set:

- `SCHEMA_VERSION_INVALID`: artifact schema version does not match the required protocol artifact version
- `REBUILD_HASH_EXPECTED_MISMATCH`: declared expected rebuild hash does not match the hash derived from the canonical identity surface
- `PASS_REQUIRES_MATCH`: an artifact declares `validator_result = PASS` while `rebuild_result != MATCH`

Implementations MAY introduce additional local reason codes.

Local codes MUST:

1. NOT conflict with protocol-defined codes;
2. be namespaced;
3. NOT alter the normalized verification result surface.

Reason codes in the normalized verification result object MUST be ordered lexicographically.

Coverage status for protocol-defined reason-code classes is declared in:

```text
conformance/CASE_CLASS_MATRIX_V0_1.json
```

## 7. Canonicalization Identifier Registry

The following canonicalization identifiers are valid for this profile:

```text
decirepo-json-c14n-v1
decirepo-result-c14n-v1
```

Definitions:

`decirepo-json-c14n-v1`
Canonical serialization of the protocol identity surface for hashing.

`decirepo-result-c14n-v1`
Canonical serialization of the normalized verification result object.

## 8. Genesis Conformance Vector

The DeciRepo Genesis artifact defines the initial reference verification case.

The Genesis vector is stored at:

```text
conformance/v0_1/vector_001_genesis/
```

It includes:

```text
artifact.json
canonical_bytes.hex
expected_artifact_id.txt
expected_verification_result.json
expected_verification_result.canonical.hex
vector_manifest.json
```

All DeciRepo-compatible implementations MUST successfully reproduce the Genesis verification result.

Failure to reproduce the Genesis result indicates protocol incompatibility for this baseline profile.

The Genesis vector is immutable.
It MUST NOT be modified in any future protocol revision.

## 9. Deterministic Execution Requirement

Verification MUST produce identical normalized outputs across:

- independent implementations;
- independent environments;
- independent organizations.

Any implementation that produces different normalized verification results for the same artifact, canonical bytes, and verification-critical inputs MUST be considered non-conformant.

## 10. Compatibility Testing Procedure

To verify compatibility, an implementation MUST:

1. load the canonical artifact;
2. apply canonical serialization rules;
3. compute the artifact identity;
4. execute the mandatory protocol verification procedure;
5. compare results with the expected outputs.

All required outputs MUST match the canonical test vectors exactly.

## 11. Conformance Claim

An implementation MAY claim DeciRepo compatibility for this baseline only if:

1. all published canonical vectors pass;
2. the Genesis verification vector matches;
3. normalized verification outputs match the protocol-defined result surface.

Implementations SHOULD publish conformance reports when claiming compatibility.

## 12. Reference Conformance Bundle

The official initial compatibility anchor is distributed in the bundle:

```text
DECIREPO_GENESIS_VERIFICATION_BUNDLE_V0_1
```

The bundle contains:

- canonical artifact;
- canonical serialized bytes;
- expected artifact identity;
- expected normalized verification result;
- expected canonical normalized result bytes;
- vector manifest;
- verification script;
- protocol version binding.

The bundle serves as the initial reproducibility and compatibility anchor for the protocol baseline.
The Genesis Verification Bundle contains the first canonical conformance vector.

## 13. Required Match Conditions

A conformant implementation MUST match the published vectors on all of the following:

1. exact canonical byte sequence;
2. exact artifact identity;
3. exact `status` value;
4. exact ordered `reason_codes` array;
5. exact `protocol_version` value;
6. exact `verifier_result_schema` value.

Command-specific comparison outputs, where defined by a vector, MUST also match exactly.
Canonical byte sequences and canonical normalized result bytes MUST match exactly.

## 14. Future Conformance Versions

Future protocol revisions MAY introduce:

- additional conformance vectors;
- extended verification result fields outside the normalized baseline surface;
- new normative reason codes;
- protocol-version-specific result schemas.

Backward compatibility rules will be defined by future protocol versions and their corresponding conformance profiles.

## 15. Conformance Report Surface

A machine-runnable conformance harness MAY emit diagnostic data in addition to the protocol compatibility verdict.

For this baseline, the conformance report surface is divided into:

1. normative report fields;
2. diagnostic report fields.

Normative top-level report fields are:

- `report_schema`
- `implementation_name`
- `implementation_version`
- `conformance_profile`
- `protocol_specification`
- `protocol_semantics`
- `vectors_total`
- `vectors_passed`
- `vectors_failed`
- `overall_verdict`
- `results`

Normative per-vector fields are:

- `vector_id`
- `verdict`
- `identity_check`
- `verification_check`
- `result_bytes_check`

Diagnostic fields MAY be included only inside a dedicated diagnostics object.
Diagnostic fields MUST NOT alter normative report interpretation.
