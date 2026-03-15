# DeciRepo Network Bootstrap Note v0.1

**Operational playbook for cross-organization artifact exchange**

## Status

```text
Version: 0.1
Protocol dependency: DeciRepo Protocol v0.1 (frozen)
Scope: minimal network bootstrap
```

This document defines the minimum conditions under which independent organizations can exchange and reproducibly verify decision artifacts through the DeciRepo protocol surface.

This document does not define an infrastructure network.
It defines a bootstrap procedure.

## 1. Objective

The objective of the bootstrap procedure is:

```text
enable independent organizations to:
publish
verify
replay
decision artifacts under DeciRepo Protocol v0.1
```

Bootstrap is considered successful if independent parties can reproduce the same verification outcome for the same artifact.

## 2. Node Roles

Bootstrap uses three roles.

### Publisher Node

```text
role: artifact publisher
responsibility:
- produce artifact
- publish artifact through protocol surface
```

The publisher does not perform verification on behalf of other nodes.

### Verification Node

```text
role: artifact verifier
responsibility:
- fetch artifact
- run deterministic verification
- publish verification result
```

The verification node must be organizationally independent from the publisher.

### Replay Node

```text
role: independent reproducibility verifier
responsibility:
- obtain artifact and verification inputs
- independently reproduce verification outcome
```

The replay node confirms deterministic reproducibility.

## 3. Node Manifest

Each node publishes a manifest.

Example:

```json
{
  "node_id": "orgB-verifier",
  "protocol_version": "DeciRepo-Protocol-v0.1",
  "node_role": "verification",
  "verification_engine": "DLX-compatible",
  "artifact_support": ["decision-artifact-v0.1"],
  "replay_capability": true
}
```

The manifest is used only for capability disclosure.

It does not create trust between nodes.

## 4. Handshake

The minimal handshake checks:

```text
protocol_version
artifact_schema
verification_capability
```

Handshake is successful if:

```text
protocol_version match
artifact_schema supported
verification engine declared
```

Handshake does not include:

```text
identity federation
trust establishment
authorization negotiation
```

## 5. Artifact Exchange Flow

Minimal flow:

```text
Publisher -> Registry -> Verifier -> Replay
```

### Step 1 - Publish

The publisher publishes an artifact.

```text
publish(artifact)
```

The registry stores the artifact and its integrity hash.

### Step 2 - Verify

The verifier retrieves the artifact.

```text
fetch(artifact_id)
verify(artifact)
```

The verifier publishes the verification outcome.

### Step 3 - Replay

The replay node performs an independent replay.

```text
fetch(artifact_id)
fetch(verification_inputs)
replay_verification()
```

The outcome must match.

## 6. Replay Contract

Replay is valid if:

```text
artifact identity identical
verification inputs identical
verification outcome identical
```

Replay does not depend on:

```text
publisher runtime
registry implementation
original environment
```

## 7. Artifact Identity

An artifact is identified by its canonical hash.

```text
artifact_id = HASH(canonical_artifact_representation)
```

All nodes must use the same canonical representation before hashing.

If canonicalization differs, artifacts are considered non-identical.

## 8. Verification Inputs Disclosure

A verifier must disclose the minimum input set required to reproduce the verification outcome.

This may include:

```text
artifact identifier
verification engine version
protocol version
invariant snapshot reference
runtime context identifier (if applicable)
```

Replay is invalid if verification-critical inputs are withheld.

## 9. Conformance Minimum

Minimum compatibility level:

```text
artifact schema compatibility
protocol version compatibility
deterministic verification outcome
replay reproducibility
```

Any mismatch is a conformance failure.

## 10. Pilot Success Criteria

The bootstrap pilot is successful only if all of the following are true:

```text
artifact integrity preserved
verification outcome identical
replay independently reproducible
no manual intervention required
```

Any manual correction invalidates the pilot.

## 11. Pilot Log Record

Each participating node should produce a pilot log record containing:

```text
node manifest
artifact identifier
verification outcome
verification engine version
timestamp
```

The pilot log record must be publicly shareable for pilot review.

## 12. Non-Goals

This bootstrap does not introduce:

```text
no consensus layer
no shared execution layer
no universal governance model
no automatic trust transfer between nodes
```

Bootstrap validates reproducible artifact exchange only.

## 13. Interpretation

This document does not declare a network.

It defines a procedure for testing whether a network can exist.

Critical rule:

```text
Zenodo proves protocol existence.
Bootstrap pilot proves network existence.
```
