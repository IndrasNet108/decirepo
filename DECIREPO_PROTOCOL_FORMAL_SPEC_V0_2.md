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

## 2. Protocol Boundary

The DeciRepo protocol consists only of the minimum rules required to determine whether a decision artifact is protocol-valid and reproducibly verifiable.

The protocol core includes:

1. artifact schema;
2. artifact identity function;
3. verification procedure;
4. reproducibility requirement;
5. compatibility rule.

If any of these semantics change incompatibly, the result is a different protocol version.

## 3. Non-Protocol Surfaces

The following are explicitly outside the protocol core:

- DeciRepo Cloud service operations;
- node topology and network deployment shape;
- trust-root governance process;
- commercial terms, SLAs, and support models;
- UI, site pages, and convenience API surfaces not required for protocol validity;
- policy authoring systems used upstream of artifact publication.

These may evolve without redefining the protocol, provided they do not alter the protocol core.

## 4. Artifact Model

A DeciRepo decision artifact is a structured record describing a decision outcome and the minimum information required for reproducible verification.

Minimum protocol-relevant fields include:

- protocol version;
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

## 5. Artifact Identity Function

Artifact identity is defined by canonical hashing.

```text
artifact_id = HASH(canonical_artifact_representation)
```

Normative requirements:

1. canonicalization must be deterministic;
2. equivalent semantic content must produce the same canonical representation;
3. differing canonical representations are non-identical artifacts;
4. identity must not depend on registry-local metadata outside the canonical artifact surface.

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
2. reconstruct the canonical artifact surface;
3. recompute the required verification result from the same declared inputs;
4. compare recomputed identity and declared identity;
5. emit a deterministic outcome.

Minimum outcome classes are:

- `PASS`
- `FAIL`
- `CONFORMANCE_ERROR`

The protocol does not define business correctness, legal correctness, or policy wisdom.
It defines reproducible verification of the artifact surface only.

## 7. Reproducibility Requirement

The protocol requires deterministic reproducibility.

A reproducibility claim holds only if:

```text
same artifact
+ same canonical representation
+ same verification-relevant inputs
+ same protocol version
+ same validator profile
-> same verification result
```

This requirement is the protocol center.

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

## 9. Compatibility Rule

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

## 10. Implementation Independence

The protocol is implementation-independent.

Possible implementations may include:

- reference Node implementation;
- Rust implementation;
- Go implementation;
- managed cloud registry implementation.

These may differ operationally, but if they alter protocol-core semantics, they are not equivalent implementations of the same protocol version.

## 11. Network Independence

The existence of a DeciRepo-compatible artifact protocol does not imply the existence of a DeciRepo network.

A network exists only when independent parties can:

- publish artifacts,
- verify artifacts,
- replay verification outcomes,

under a shared compatible protocol surface.

Network bootstrap is operationally described separately in:

- `DECIREPO_NETWORK_BOOTSTRAP_NOTE_V0_1.md`

## 12. Protocol Invariants

The formal invariants of the protocol core are:

1. identical canonical artifacts have identical protocol identity;
2. identical verification-critical inputs produce identical verification results;
3. verification outcomes are deterministic under fixed protocol semantics;
4. compatibility claims are invalid if protocol-core semantics drift;
5. protocol meaning is independent of any single managed registry implementation.

If any invariant fails, the implementation is outside the declared compatibility surface.

## 13. Non-Goals

The DeciRepo protocol does not define:

- consensus;
- shared execution;
- universal governance;
- commercial operating terms;
- automatic trust between nodes;
- decision correctness beyond reproducible protocol verification.

## 14. Formal Definition

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
