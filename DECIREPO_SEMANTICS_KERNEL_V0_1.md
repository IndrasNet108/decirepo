# DECIREPO_SEMANTICS_KERNEL_V0_1

Status: Draft

## Purpose

This document defines the bounded semantics kernel for the published DeciRepo baseline conformance profile `V0_1`.

It does not claim completeness for all future protocol evolution.
It fixes the smallest semantics surface needed to reason about bounded completeness for the published baseline slice.

The machine-readable companion artifact for this kernel is:

```text
conformance/SEMANTICS_KERNEL_V0_1.json
```

If this document conflicts with a published canonical vector, the published vector wins for `V0_1` compatibility.

## 1. Bounded Domain

The bounded domain for this kernel is declared by:

- `DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2.md`
- `DECIREPO_PROTOCOL_CONFORMANCE_V0_1.md`
- `conformance/DOMAIN_PROFILE_V0_1.json`
- published canonical vectors in `conformance/v0_1/`

The domain is limited to:

- JSON artifact objects;
- the commands `verify`, `validate`, and `rebuild`;
- identity derived from `artifact.rebuild_source`;
- normalized results conforming to `decirepo-verifier-result-v0.1`.

The published baseline compatible conformance path requires `artifact.rebuild_source` to be present and usable as the identity surface.
Artifacts outside that path are not baseline-compatible conformance inputs unless fixed by a published vector.

## 2. Identity Derivation

For baseline `V0_1`, the identity surface is exactly:

```text
artifact.rebuild_source
```

Identity derivation is:

1. resolve `artifact.rebuild_source`;
2. serialize it with `decirepo-json-c14n-v1`;
3. UTF-8 encode the canonical JSON bytes;
4. compute `artifact_id = SHA256(canonical_identity_bytes)`.

Consequences:

- envelope fields outside `artifact.rebuild_source` do not affect identity;
- fields inside `artifact.rebuild_source` do affect identity;
- object-key ordering is normalized recursively;
- array ordering is preserved and therefore semantic for identity.

## 3. Command Semantics

## 3.1 Verify

`verify` evaluates the artifact under the following bounded rule set:

1. `schema_version` must equal `dlx-artifact-v0.1` or emit `SCHEMA_VERSION_INVALID`;
2. if `rebuild_hash_expected` is present and differs from the computed `artifact_id`, emit `REBUILD_HASH_EXPECTED_MISMATCH`;
3. if `validator_result = PASS` and `rebuild_result != MATCH`, emit `PASS_REQUIRES_MATCH`.

For the current published baseline, `verify` does not close all possible artifact-model failures.
Only the published rule set and registry-backed gaps are included in this kernel.

## 3.2 Validate

`validate` evaluates `transition_chain` under the following bounded rule set:

1. `transition_chain` must be a non-empty array;
2. every step must contain `from`, `to`, and `evidence_hash`;
3. allowed local transitions are:
   - `DRAFT -> PROPOSED`
   - `PROPOSED -> VALIDATED`
   - `VALIDATED -> PUBLISHED`
4. continuity is mandatory: each step's `from` must match the previous step's `to`.

Any violation in this bounded rule set emits `TRANSITION_CHAIN_INVALID`.

This kernel does not yet prove completeness for transition semantics beyond local validity and continuity.

## 3.3 Rebuild

`rebuild` evaluates only whether the published rebuild surface is usable.

The bounded rule set is:

1. `rebuild_source` must be present;
2. `rebuild_source` must be an object.

Violation emits `REBUILD_SOURCE_INVALID`.

## 4. Result Production

After command evaluation:

1. collect all reason codes emitted by the bounded rule set;
2. sort `reason_codes` lexicographically;
3. set `status = FAIL` if `reason_codes` is non-empty, otherwise `PASS`;
4. build the normalized result object exactly as:

```json
{
  "status": "PASS | FAIL | CONFORMANCE_ERROR",
  "artifact_id": "<computed hash>",
  "reason_codes": [],
  "protocol_version": "v0.1",
  "verifier_result_schema": "decirepo-verifier-result-v0.1"
}
```

5. canonicalize the normalized result with `decirepo-result-c14n-v1`.

`CONFORMANCE_ERROR` is reserved for cases where the protocol result cannot be meaningfully produced, such as unsupported command dispatch or unresolved identity-surface binding.
No natural published canonical vector currently anchors that status.

## 5. Harness Verdict Semantics

The conformance harness evaluates compatibility, not business correctness.

For each published vector, the harness checks:

- fixture consistency;
- canonical identity bytes match;
- computed `artifact_id` match;
- normalized result bytes match;
- unmapped verifier errors are empty.

Per-vector verdicts are:

- `PASS` if all required checks are true;
- `FAIL` if a normalized protocol result is available but one or more required checks are false;
- `CONFORMANCE_ERROR` if the harness cannot resolve the identity surface, dispatch the command, or normalize the result surface.

Overall verdict is:

- `PASS` only if every vector verdict is `PASS`;
- `CONFORMANCE_ERROR` if any vector verdict is `CONFORMANCE_ERROR`;
- otherwise `FAIL`.

## 6. Bounded Completeness Status

The current published baseline closes the following case classes with canonical vectors:

- baseline verify pass;
- schema version invalid;
- rebuild hash expected mismatch;
- pass requires match;
- transition chain invalid;
- rebuild source invalid;
- tolerated unknown top-level envelope field.

The current published baseline does not yet close:

- absent `rebuild_source` under `verify`;
- natural `CONFORMANCE_ERROR` behavior;
- multi-reason precedence;
- vector coverage for `ARTIFACT_HASH_INVALID`, `VALIDATOR_RESULT_INVALID`, and `REBUILD_RESULT_INVALID`.

Coverage status for each case class is declared in `conformance/CASE_CLASS_MATRIX_V0_1.json`.
