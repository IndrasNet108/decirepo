# Mirror Verifier Pilot Checklist v0.1

## Phase 1: Pre-Deployment
- [ ] Select node role: `mirror_verifier`.
- [ ] Generate Ed25519 identity keypair.
- [ ] Configure public HTTPS endpoint with TLS 1.3.
- [ ] Create and host `/.well-known/decirepo-node`.

## Phase 2: Verification Readiness
- [ ] Install `dlx-ref` reference engine.
- [ ] Execute `bash scripts/validate_all.sh` and achieve **PASS**.
- [ ] Perform first remote verify against the Reference Node.
- [ ] Confirm verification result API matches `VERIFICATION_RESULT_API_SPEC_V0_1.md`.

## Phase 3: Pilot Activity
- [ ] Verify at least 10 artifacts from the Reference Node feed.
- [ ] Ensure results are correctly published to your node's API.
- [ ] Verify that your node appears in the global **Verification Graph**.

## Phase 4: Exit Criteria
- [ ] Maintain 99.9% uptime for 30 consecutive days.
- [ ] Zero unresolved protocol conformance failures.
- [ ] Successful participation in at least one pilot investigation report.
