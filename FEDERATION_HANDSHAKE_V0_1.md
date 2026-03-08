# FEDERATION_HANDSHAKE_V0_1

Status: draft (operational)
Protocol baseline: `v0.1` (frozen)

## Purpose

Define deterministic onboarding and verification exchange between registry nodes.

## Handshake Sequence

1. Discover node manifest
- Fetch target discovery document from `/.well-known/decirepo-node` (or equivalent endpoint).
- Resolve `manifest_url` from discovery document, then fetch manifest.
- Validate required fields: `registry_id`, `verify_endpoint`, `protocol_version`, `public_keys`, `signature`.

2. Check protocol compatibility
- Compare source protocol with target `protocol_version`.
- If incompatible: fail-closed, emit trust event `protocol_non_compliance`.

3. Fetch trust profile
- Read target trust and root policy (`/api/trust`, `/api/root-of-trust`).
- Ensure required validators and policy profile references exist.

4. Run verification probe
- Execute probe against target `verify_endpoint` with known artifact.
- Validate deterministic response (`PASS` + `MATCH`) and hash consistency.

5. Register verification edge
- Add/update edge in verification graph with metrics and status.
- Emit trust event (`registry_added` or `score_changed`).

## Challenge / Recheck Flow

If source and target disagree on verification:

1. Emit `verification_mismatch_detected` event.
2. Trigger deterministic recheck with same artifact and payload.
3. Compare first result vs recheck result.
4. If mismatch persists, downgrade edge status and apply incident penalty.
5. If threshold is exceeded, trigger suspension policy.

## Fail-Closed Conditions

- Missing or invalid signed node manifest.
- Protocol incompatibility with no migration path.
- Repeated rebuild mismatch beyond policy threshold.
- Undeclared breaking change (silent drift).

## Required Telemetry

- `verify_success_rate`
- `rebuild_match_rate`
- `last_verified_at`
- `edge_status`
- trust events stream (`/api/trust-events`)

## Determinism Rule

Any ambiguity in handshake interpretation resolves to `deny / quarantine` until explicit policy update.
