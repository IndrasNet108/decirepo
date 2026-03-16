# DeciRepo Genesis Verification Bundle v0.1

## Purpose

This bundle provides a minimal reproducible verification path for the canonical
DeciRepo Genesis artifact.

It is designed to anchor three things in one place:

- the protocol snapshot (`protocol.json`)
- the canonical Genesis artifact (`genesis_artifact.json`)
- canonical identity-surface bytes (`canonical_bytes.hex`)
- the expected protocol identity (`expected_artifact_id.txt`)
- the canonical vector manifest (`vector_manifest.json`)
- canonical normalized result bytes (`expected_verification_result.canonical.hex`)
- a minimal deterministic reference verifier (`dlx-ref`)

## What This Demonstrates

Using the same Genesis artifact and the same reference verifier, an external
reviewer can reproduce:

- `verify` -> `PASS`
- `rebuild` -> `PASS`
- `validate` -> `PASS`

This is reproducibility evidence for the protocol artifact.
It also contains the first canonical conformance vector for the frozen public baseline.

## What This Does Not Demonstrate

This bundle does not demonstrate:

- network existence
- legal correctness
- business correctness
- policy completeness

## Quickstart

Requirements:

- Node.js 18+ or later
- standard SHA256 tooling (optional)

Run the full path:

```bash
bash scripts/run_genesis_verification.sh all
```

Run individual steps:

```bash
bash scripts/run_genesis_verification.sh verify
bash scripts/run_genesis_verification.sh rebuild
bash scripts/run_genesis_verification.sh validate
```

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_genesis_verification.ps1 -Mode all
```

Expected JSON outputs are stored in `expected/`.
The normalized expected verification result is stored in `expected_verification_result.json`.
Canonical normalized result bytes are stored in `expected_verification_result.canonical.hex`.

## Integrity

The file `genesis_artifact.sha256` contains the SHA256 checksum for the copied
canonical artifact in this bundle.

The file `SHA256SUMS.txt` contains checksums for the bundle contents.
