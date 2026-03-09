# decirepo

Federated decision verification infrastructure. Operational layer of the IndrasNet ecosystem.

Lead Architect: **Oleg Surkov**
DOI (concept): https://doi.org/10.5281/zenodo.18862311
DOI (version v1.0): https://doi.org/10.5281/zenodo.18862312

## Public Change Log

See `PUBLIC_CHANGELOG.md` for public-facing status, governance, commerce mode,
and protocol milestone updates.

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
