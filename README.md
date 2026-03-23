# decirepo

Federated decision verification infrastructure. Operational layer of the IndrasNet ecosystem.

Lead Architect: **Oleg Surkov**
Protocol DOI (DeciRepo Decision Protocol v0.1): https://doi.org/10.5281/zenodo.19044692
Earlier archival record (concept): https://doi.org/10.5281/zenodo.18862311
Earlier archival record (version v1.0): https://doi.org/10.5281/zenodo.18862312

## Citation

Use this citation when referring specifically to the public protocol record:

```text
DeciRepo Decision Protocol v0.1.
DOI: https://doi.org/10.5281/zenodo.19044692
```

This DOI documents protocol existence and reference architecture.
It does not claim the existence of a DeciRepo network.

## Public Change Log

See `PUBLIC_CHANGELOG.md` for public-facing status, governance, commerce mode,
and protocol milestone updates.

## Public Repository Scope

This repository intentionally exposes only the public protocol, public site,
publishable artifacts, and verification-facing reference materials.

Private runtime components, operator playbooks, outreach materials, and
commercial planning documents are maintained outside the public repository.

## Independent Verification

Use `INDEPENDENT_VERIFICATION_NOTE_TEMPLATE_V0_1.md` to publish external
recomputation evidence (MATCH/FAIL) from non-origin verifier nodes.

Reference commands:

```bash
node dlx-ref/cli.js verify artifacts/genesis/DR-GENESIS-0001.json
node dlx-ref/cli.js rebuild artifacts/genesis/DR-GENESIS-0001.json
node dlx-ref/cli.js conformance dlx-ref/tests/conformance_v0_1.json
```

## Relationship
Built on principles defined in [dlx-prior-art](../dlx-prior-art).
