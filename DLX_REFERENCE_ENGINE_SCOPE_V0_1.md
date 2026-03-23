# DLX_REFERENCE_ENGINE_SCOPE_V0_1

Status: active scope policy  
Reference engine: `dlx-ref` (neutral executable semantics)

## 1) Purpose

Define strict boundaries for the DLX reference engine to ensure protocol correctness without turning reference implementation into production runtime.

## 2) In-scope (open reference behavior)

`dlx-ref` includes only:

1. Deterministic `verify` behavior for artifact envelopes.
2. Deterministic `rebuild` behavior for canonical rebuild source.
3. Deterministic `validate transitions` behavior for transition chains.
4. `conformance` execution against test vectors (`PASS/FAIL`).
5. Canonical, inspectable output for debugging protocol semantics.

## 3) Out-of-scope (not part of `dlx-ref`)

`dlx-ref` explicitly excludes:

1. High-performance production runtime optimizations.
2. Enterprise orchestration and workflow automation.
3. Ops/SLA tooling and managed runtime controls.
4. Commercial policy packs and tenant-specific logic.
5. Vendor-specific integration adapters.

## 4) Design constraints

1. Determinism over speed.
2. Fail-closed on malformed artifacts.
3. Explicit schema checks before semantic checks.
4. No hidden network dependencies for local verification.
5. Stable CLI contract (`verify`, `rebuild`, `validate`, `conformance`).

## 5) Relationship to DeciRepo Protocol

- `dlx-ref` defines executable neutral semantics for protocol correctness.
- Production runtimes may optimize execution, but must pass protocol conformance.
- Protocol meaning is anchored by spec + conformance + reference behavior.

