# DECIREPO_SECOND_IMPLEMENTATION_PATH_V0_1

Status: Draft

## Purpose

This document is written for an external engineering team attempting a second DeciRepo-compatible implementation.

It is not a new protocol layer.
It is an execution-facing path that removes residual dependence on author intuition.

If this document conflicts with a normative artifact, the following precedence order applies:

1. `DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2.md`
2. `DECIREPO_PROTOCOL_CONFORMANCE_V0_1.md`
3. `conformance/CONFORMANCE_REPORT_SCHEMA.json`
4. published canonical vectors in `conformance/v0_1/`

## 1. Protocol Core

An external team claiming baseline DeciRepo compatibility must implement only the protocol core:

- artifact model
- artifact identity function
- verification procedure
- reproducibility requirement
- compatibility clause

The external team does not need to reproduce:

- repository layout
- CI setup
- site pages
- bundle packaging
- drift guards
- the reference implementation codebase

Compatibility is determined by protocol-core behavior, not by project scaffolding.

## 2. Minimum Implementation Path

The shortest practical route to first compatibility is:

1. implement `decirepo-json-c14n-v1` for the identity surface;
2. implement `artifact_id = SHA256(canonical_identity_bytes)`;
3. bind baseline `v0.1` identity to `artifact.rebuild_source`;
4. implement the baseline `verify` command;
5. emit the normalized verification result object;
6. implement `decirepo-result-c14n-v1` for normalized result bytes;
7. pass `vector_001_genesis`;
8. then pass `vector_002` through `vector_006`;
9. emit a conformance report matching `conformance/CONFORMANCE_REPORT_SCHEMA.json`.

Do not begin with CI, bundle packaging, or report publication.
Begin with vector-by-vector compatibility.

## 3. Conformance Claim Requirements

An external team may claim baseline DeciRepo compatibility only if all of the following are true:

1. the implementation passes every published canonical vector in `conformance/v0_1/`;
2. the implementation reproduces the expected artifact identities;
3. the implementation reproduces the expected normalized verification results byte-for-byte;
4. the implementation can emit a conformance report matching `conformance/CONFORMANCE_REPORT_SCHEMA.json`;
5. the implementation does not require `dlx-ref` code to execute its own verifier logic;
6. the baseline compatible conformance path is evaluated only on artifacts for which `artifact.rebuild_source` is present and usable as the published identity surface.

The public reference report:

- `conformance/REFERENCE_CONFORMANCE_REPORT_V0_1.json`

is a reference example of successful baseline output.
It is not an independent source of protocol truth and must not be treated as a hidden oracle overriding the vectors or the conformance profile.

A local verifier may still expose operational behavior outside the published baseline compatible path.
Such behavior does not become a compatibility anchor unless it is fixed by published vectors and the conformance profile.

## 4. Verifier vs Harness Boundary

### 4.1 Verifier Responsibilities

The verifier is responsible for:

- accepting a protocol artifact;
- validating protocol-relevant inputs for the requested command;
- computing identity where required;
- executing protocol verification semantics;
- emitting or making derivable the normalized verification result object.

### 4.2 Conformance Harness Responsibilities

The conformance harness is responsible for:

- loading canonical vectors;
- validating fixture completeness;
- checking canonical identity bytes and expected artifact identity;
- executing the verifier for the declared command;
- canonicalizing the normalized verification result object;
- comparing actual results to canonical expected outputs;
- emitting per-vector and overall conformance verdicts.

### 4.3 Boundary Rule

The verifier evaluates protocol artifacts.
The harness evaluates verifier compatibility.

The harness must not repair or reinterpret verifier behavior into compatibility.
The verifier must not rely on harness-side normalization to become protocol-compatible.

## 5. Verdict Classification Rules

The following table defines the intended baseline classification model.

| Situation | Normalized result object available? | Verdict |
| --- | --- | --- |
| Artifact is processable and satisfies the requested protocol checks | yes | `PASS` |
| Artifact is processable but violates protocol structure or verification semantics | yes | `FAIL` |
| Expected identity bytes, artifact identity, or normalized result bytes do not match canonical fixtures | yes | `FAIL` |
| Verifier output is malformed but still normalizable and comparable | yes | `FAIL` |
| Harness or verifier cannot complete protocol-compatible comparison at all | no | `CONFORMANCE_ERROR` |
| Declared conformance command is unsupported by the implementation | no | `CONFORMANCE_ERROR` |
| Verifier output cannot be normalized into the protocol result surface | no | `CONFORMANCE_ERROR` |
| Fixture cannot be loaded or required comparison data is unavailable | no | `CONFORMANCE_ERROR` |

Practical rules:

- malformed verifier output gives `FAIL` if the harness can still derive the protocol result surface and compare it;
- malformed verifier output gives `CONFORMANCE_ERROR` if the harness cannot derive the protocol result surface at all;
- abort conditions map to `CONFORMANCE_ERROR` when protocol comparison cannot be completed;
- overall conformance verdict is `PASS` only if all vectors pass;
- any `CONFORMANCE_ERROR` takes precedence over ordinary `FAIL` at the overall verdict level.

## 6. Canonical Result Production

For conformance purposes, raw verifier output must be reduced to the normalized verification result object:

```json
{
  "status": "PASS | FAIL | CONFORMANCE_ERROR",
  "artifact_id": "<hash>",
  "reason_codes": [],
  "protocol_version": "v0.1",
  "verifier_result_schema": "decirepo-verifier-result-v0.1"
}
```

Canonical result production requires:

1. determine `status`;
2. determine `artifact_id` from the protocol identity surface;
3. map protocol-relevant failure conditions into canonical `reason_codes`;
4. order `reason_codes` lexicographically;
5. bind `protocol_version`;
6. bind `verifier_result_schema`;
7. canonicalize the result with `decirepo-result-c14n-v1`.

For the published baseline:

- `reason_codes` ordering is canonical, not expressive;
- multiple failure reasons are allowed, but the array must be lexicographically ordered;
- diagnostic or extension fields must remain outside the normalized result object.

### 6.1 Authoritative Binding of Identifiers

The identifiers are authoritative only when read together with their defining documents:

- `decirepo-json-c14n-v1`: defined by the artifact canonicalization rules in `DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2.md` and bound in each `vector_manifest.json`;
- `decirepo-result-c14n-v1`: defined by the result canonicalization rules in `DECIREPO_PROTOCOL_CONFORMANCE_V0_1.md` and bound in each `vector_manifest.json`;
- `decirepo-verifier-result-v0.1`: bound by the conformance profile and the published report schema.

The identifier name alone is not sufficient.
Compatibility depends on the rules attached to that identifier.

## 7. Unknown Field Policy

### 7.1 Unknown Fields in the Normalized Result Object

Unknown fields are forbidden inside the normalized verification result object during conformance comparison.

If extra fields appear inside that object, they are not part of canonical result bytes and should be treated as a compatibility problem.

### 7.2 Unknown Fields in the Artifact Envelope

For the current published baseline, use the conservative rule:

- unknown artifact-envelope fields must not affect canonical identity bytes;
- unknown artifact-envelope fields must not affect the normalized verification result surface.

The current baseline does not yet publish a dedicated vector deciding whether such fields must be rejected or ignored.
Do not infer a stronger rule solely from the reference implementation.

### 7.3 Unknown Fields Inside `artifact.rebuild_source`

`artifact.rebuild_source` is itself the identity surface for baseline `v0.1`.
Therefore, fields inside `rebuild_source` are not outside the surface.

If a field exists inside `rebuild_source`, it participates in canonical identity bytes unless a future protocol version says otherwise.

## 8. Rebuild Source Exact Semantics

For baseline `v0.1`, the identity surface is exactly:

```text
artifact.rebuild_source
```

This means:

- not the full artifact envelope;
- not the transport wrapper;
- not non-protocol file metadata;
- the value stored in the `rebuild_source` field.

### 8.1 Serialization Rules

`artifact.rebuild_source` is serialized with `decirepo-json-c14n-v1`:

- deterministic JSON serialization;
- UTF-8 encoding;
- lexicographically sorted object keys;
- preserved array order.

Consequences:

- object-key reordering inside `rebuild_source` does not change identity;
- array reordering inside `rebuild_source` does change identity;
- nested objects are reorderable by key because canonicalization sorts keys recursively;
- nested arrays are not reorderable without changing identity.

### 8.2 Presence, Null, and Empty Object

For the current published baseline:

- the published baseline compatible conformance path requires `artifact.rebuild_source` to be present and usable as the identity surface;
- under `rebuild`, `rebuild_source` must be present and must be an object;
- under `rebuild`, `null`, absence, or non-object values are rebuild-surface failures;
- local `verify` behavior without `rebuild_source` is not a published compatibility anchor for baseline conformance;
- an empty object is canonically serializable, but no current published vector defines it as a meaningful successful business artifact.

### 8.3 Stage Boundary

For the current baseline, `rebuild_source` concerns two different stages:

- identity stage: canonical bytes are derived from `artifact.rebuild_source`;
- rebuild stage: the `rebuild` command checks whether rebuild execution can derive the expected rebuild hash from that surface.

Do not collapse identity derivation and rebuild execution into one undifferentiated rule.

## 9. Transition Chain Validation Notes

### 9.1 Validity Shape

For the current published baseline, a transition chain is valid only if it is a non-empty array of step objects, each containing:

- `from`
- `to`
- `evidence_hash`

The currently observed baseline behavior expects `evidence_hash` to be a 64-character hexadecimal value.

### 9.2 Continuity and Order

Order is semantically relevant.

For each step after the first:

```text
previous.to == current.from
```

A mismatch is a chain-break failure.

### 9.3 Allowed Local Transitions

The currently published baseline behavior recognizes the following local transitions:

```text
DRAFT -> PROPOSED
PROPOSED -> VALIDATED
VALIDATED -> PUBLISHED | SUSPENDED
PUBLISHED -> SUSPENDED | REVOKED
SUSPENDED -> REVOKED
```

Any step outside this set is invalid.

### 9.4 Structural Invalid vs Semantic Invalid

For the current baseline compatibility layer, the published vectors do not distinguish separate canonical reason codes for:

- malformed transition step shape;
- invalid local transition value;
- transition-chain continuity break.

At the current profile level, these failures belong to the same transition-chain failure class.
Do not invent finer-grained canonical categories unless a later profile publishes them.

### 9.5 What Is Not Yet Fixed

The current baseline does not yet fully fix:

- whether a valid chain must begin from one specific initial state;
- whether a valid chain must end at one specific terminal state;
- whether chain completeness is required beyond local validity and continuity.

Implement only what is fixed by the current profile and vectors.
Do not add stronger chain-completeness rules and still call them baseline DeciRepo behavior.

## 10. What Is Not Required

An external team does not need the following to make a baseline compatibility claim:

- the `dlx-ref` codebase;
- the DeciRepo CI workflows;
- bundle repackaging;
- the site repository;
- the drift-guard scripts;
- publication of CI artifacts;
- reproduction of repository-internal operational tooling;
- stronger semantics than those fixed by the current published vectors.

A second implementation needs protocol compatibility, not repository mimicry.
