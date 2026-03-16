# DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2

Status: draft formal specification  
Applies to: `DeciRepo Protocol v0.1` semantics, formalized as `v0.2` specification draft

## 1. Purpose

This document defines the formal boundary of the DeciRepo protocol.

Its purpose is to separate:

- the protocol itself,
- reference and commercial implementations,
- network and governance surfaces.

This document is not a network declaration.
It is a protocol-boundary document.

Normative keywords in this document are to be interpreted as:

- `MUST`
- `MUST NOT`
- `SHOULD`
- `MAY`

## 2. Protocol Boundary

The DeciRepo protocol consists only of the minimum rules required to determine whether a decision artifact is protocol-valid and reproducibly verifiable.

The protocol core includes:

1. artifact model;
2. artifact identity function;
3. verification procedure;
4. reproducibility requirement;
5. compatibility clause.

If any of these semantics change incompatibly, the result is a different protocol version.

A DeciRepo-compatible system MUST implement:

1. the artifact model defined in Section 4;
2. the artifact identity function defined in Section 5;
3. the verification procedure defined in Section 6;
4. the reproducibility requirement defined in Section 7;
5. the compatibility clause defined in Section 9.

A system that omits or weakens any of these protocol-core obligations MUST NOT claim DeciRepo compatibility for the same protocol version.

## 3. Non-Protocol Surfaces

The following are explicitly outside the protocol core:

- DeciRepo Cloud service operations;
- node topology and network deployment shape;
- storage layer and storage-network design;
- transport layer and message-delivery mechanism;
- execution environment and runtime packaging;
- trust-root governance process;
- commercial terms, SLAs, and support models;
- UI, site pages, and convenience API surfaces not required for protocol validity;
- policy authoring systems used upstream of artifact publication.

These may evolve without redefining the protocol, provided they do not alter the protocol core.

## 4. Artifact Model

A DeciRepo decision artifact is a structured record describing a decision outcome and the minimum information required for reproducible verification.

The artifact model contains three distinct protocol surfaces:

1. artifact structure;
2. canonical serialization;
3. hashing surface.

These surfaces MUST be interpreted separately. A system that preserves one but alters another is not protocol-equivalent.

### 4.1 Artifact Structure

Minimum protocol-relevant fields include:

- protocol version identifier or version binding;
- artifact schema version;
- decision identity;
- canonical artifact payload;
- artifact integrity hash;
- verification-relevant inputs or references;
- origin registry identifier;
- validator profile identifier;
- policy version identifier where applicable.

The public machine-readable protocol contract is represented by:

- `api/protocol.json`

The canonical reference artifact for the frozen public baseline is:

- `artifacts/genesis/DR-GENESIS-0001.json`

### 4.2 Canonical Serialization

Artifact identity MUST be derived from canonical artifact bytes.

For `v0.1`, canonical artifact bytes are defined as:

1. deterministic JSON serialization;
2. UTF-8 encoding;
3. lexicographically sorted object keys;
4. preserved array order;
5. no inclusion of non-protocol metadata outside the canonical artifact surface.

If two implementations serialize the same protocol artifact differently, they are not protocol-compatible for identity purposes.

### 4.3 Hashing Surface

The hashing surface is the exact canonical artifact surface that participates in identity derivation.

Registry-local metadata, convenience annotations, UI fields, transport wrappers, and storage-layer envelopes MUST NOT affect artifact identity unless they are explicitly part of the canonical artifact surface for the protocol version.

For the frozen public baseline `v0.1`, the hashing surface is the canonical serialization of:

```text
artifact.rebuild_source
```

The full artifact envelope is not the identity surface for `v0.1`.
Envelope-level file integrity MAY be tracked separately, but it MUST NOT be confused with protocol identity.

## 5. Artifact Identity Function

Artifact identity is defined by canonical hashing.

```text
artifact_id = SHA256(canonical_identity_bytes)
```

Normative requirements:

1. canonical serialization must be deterministic;
2. equivalent protocol content must produce the same canonical artifact bytes;
3. differing canonical representations are non-identical artifacts;
4. identity must not depend on registry-local metadata outside the canonical artifact surface.

The identity function therefore consists of two inseparable parts:

1. canonical serialization;
2. SHA256 hashing of the resulting canonical bytes.

For `v0.1`, `canonical_identity_bytes` MUST be the canonical serialization of `artifact.rebuild_source`.

In `v0.1`, the active hash compatibility rule is:

```text
artifact_hash == rebuild_result_hash
```

with:

```text
artifact_hash
```

retained as a compatibility alias for:

```text
rebuild_result_hash
```

This aliasing rule is part of `v0.1` compatibility behavior and may be removed only through an explicit versioned migration.

## 6. Verification Procedure

The protocol verification procedure determines whether a decision artifact is reproducibly verifiable under the declared protocol and validator profile.

At minimum, verification must:

1. load the declared artifact;
2. validate the artifact structure required by the protocol version;
3. reconstruct the canonical artifact surface;
4. derive canonical artifact bytes;
5. recompute artifact identity from the canonical bytes;
6. resolve the declared verification-critical inputs;
7. recompute the required verification result from the same declared inputs;
8. compare recomputed identity and recomputed verification outputs to the declared values;
9. emit a deterministic outcome.

Minimum outcome classes are:

- `PASS`
- `FAIL`
- `CONFORMANCE_ERROR`

The protocol does not define business correctness, legal correctness, or policy wisdom.
It defines reproducible verification of the artifact surface only.

An implementation that skips a required verification step or replaces it with a weaker check MUST NOT claim protocol-equivalent verification for the same protocol version.

The mandatory verification core MUST be deterministic and self-contained for protocol validity.

Optional enrichment MAY be performed only if it is explicitly separated from the mandatory verification core.
Optional enrichment MUST NOT alter:

- `status`
- `artifact_id`
- `reason_codes`
- `protocol_version`
- `verifier_result_schema`
- any other field in the normalized verification result object

### 6.1 Verification Result Surface

For protocol conformance, a verifier MUST expose or make derivable a normalized verification result object.

The normalized verification result object MUST include:

- `status`
- `artifact_id`
- ordered `reason_codes`
- `protocol_version`
- `verifier_result_schema`

If `status = PASS`, the ordered `reason_codes` set MUST be empty.
If `status = FAIL` or `status = CONFORMANCE_ERROR`, the ordered `reason_codes` set MUST be deterministic and stable for the same inputs.

Implementation-specific output MAY include additional diagnostic fields, but those fields MUST NOT alter the normalized verification result object.

## 7. Reproducibility Requirement

The protocol requires deterministic reproducibility.

A reproducibility claim holds only if:

```text
same artifact
+ same canonical artifact bytes
+ same verification-relevant inputs
+ same protocol version
+ same validator profile
-> same verification result
```

This requirement is the protocol center.

For protocol purposes, the verification result MUST include:

1. the outcome class;
2. the artifact identity values required by the version;
3. the ordered reason-code set;
4. the declared protocol version;
5. the verifier result schema identifier;
6. any protocol-defined comparison result required to establish match or mismatch.

For a valid artifact `A`, fixed verification-critical inputs `I`, protocol version `P`, and validator profile `V`:

```text
verify(A, I, P, V)
```

MUST produce the same verification result across independent compatible implementations.

Without reproducibility, an implementation may still emit results, but it is not DeciRepo-compatible in the protocol sense.

## 8. Verification Inputs

Verification-critical inputs must be disclosed or referenceable.

At minimum, this includes:

- artifact identifier or canonical artifact body;
- protocol version;
- validator profile;
- policy version or invariant reference where applicable;
- runtime or context identifier if it affects verification semantics.

If verification-critical inputs are hidden, reproducibility is not established.

## 9. Compatibility Clause

A system is DeciRepo-compatible only if it preserves all protocol-core semantics.

A compatible implementation must:

1. accept the declared protocol artifact structure;
2. apply the same identity function;
3. apply the same verification procedure semantics;
4. satisfy the same reproducibility requirement;
5. expose any mandatory compatibility metadata defined for the version.

Compatibility does not require:

- identical infrastructure deployment;
- identical codebase;
- identical service packaging.

Compatibility does require semantic equivalence at the protocol core.

Compatibility claims MUST be testable against canonical fixtures and required match conditions defined by the active conformance profile.

Formal clause:

```text
A system S is DeciRepo-compatible for protocol version P
if and only if S produces identical artifact identity and
identical verification outcome for all valid artifacts under P,
given the same canonical artifact bytes and the same
verification-critical inputs.
```

The canonical conformance anchor for the frozen public baseline is defined separately in:

- `DECIREPO_PROTOCOL_CONFORMANCE_V0_1.md`

## 10. Versioning Rule

Protocol versioning MUST distinguish between semantic-preserving clarification and protocol-breaking change.

The following changes are semantic-preserving only if they do not alter any protocol-core obligation:

- editorial clarifications;
- non-normative explanatory text;
- implementation examples outside the protocol core.

The following changes are protocol-breaking and MUST create a new protocol version namespace:

- artifact-structure changes;
- canonical-serialization changes;
- hashing-surface changes;
- identity-function changes;
- verification-procedure changes;
- reproducibility-rule changes;
- normalized verification result-surface changes;
- normative reason-code registry changes that alter conformance meaning;
- compatibility-clause changes.

A verifier MAY support earlier protocol versions only if it explicitly preserves the version-specific semantics for those versions.

If a version identifier is part of the canonical artifact surface for a given protocol version, it participates in artifact identity for that version.
If version metadata is not part of the canonical artifact surface, it MUST still be bound as verification-critical input.

## 11. Implementation Independence

The protocol is implementation-independent.

Possible implementations may include:

- reference Node implementation;
- Rust implementation;
- Go implementation;
- managed cloud registry implementation.

These may differ operationally, but if they alter protocol-core semantics, they are not equivalent implementations of the same protocol version.

## 12. Network Independence

The existence of a DeciRepo-compatible artifact protocol does not imply the existence of a DeciRepo network.

A network exists only when independent parties can:

- publish artifacts,
- verify artifacts,
- replay verification outcomes,

under a shared compatible protocol surface.

Network bootstrap is operationally described separately in:

- `DECIREPO_NETWORK_BOOTSTRAP_NOTE_V0_1.md`

## 13. Protocol Invariants

The formal invariants of the protocol core are:

1. identical canonical artifacts have identical protocol identity;
2. identical verification-critical inputs produce identical verification results;
3. verification outcomes are deterministic under fixed protocol semantics;
4. compatibility claims are invalid if protocol-core semantics drift;
5. protocol meaning is independent of any single managed registry implementation.

If any invariant fails, the implementation is outside the declared compatibility surface.

## 14. Non-Goals

The DeciRepo protocol does not define:

- consensus;
- node network topology;
- shared execution;
- execution engine;
- storage network;
- universal governance;
- commercial operating terms;
- automatic trust between nodes;
- decision correctness beyond reproducible protocol verification.

## 15. Formal Definition

A DeciRepo-compatible system is a system in which:

```text
decision artifact
-> canonical identity
-> verification procedure
-> deterministic reproducibility
```

holds under the same declared protocol semantics.

This is the protocol boundary.

Everything else belongs to implementation, service, or network layers.
