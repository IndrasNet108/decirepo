# FOUNDATION_READINESS_CRITERIA_V0_1

Status: active criteria set  
Applies to: transition from `Phase 2 — Co-Governance` to `Phase 3 — Foundation Stewardship`

## 1) Purpose

Define objective conditions under which DeciRepo Protocol governance should move from company-led/co-governed model to neutral foundation stewardship.

## 2) Core readiness criteria (all required)

1. Independent production registries  
   Threshold: `>= 3` non-IndrasNet production registry nodes operating continuously.

2. External verification traffic share  
   Threshold: `>= 50%` of verification traffic originates from non-IndrasNet registries/clients.

3. Stable protocol releases without breaking drift  
   Threshold: `>= 2` consecutive protocol releases with no undeclared breaking behavior.

4. Independent conformance execution  
   Threshold: `>= 2` independent CI runners (outside IndrasNet control) executing conformance suite with public result visibility.

5. Mirror trust-root capability  
   Threshold: at least `1` independent signed mirror of trust-root list with verified consistency checks.

6. Non-IndrasNet reference implementation  
   Threshold: `>= 1` external implementation passes full mandatory conformance profile for current protocol version.

## 3) Supporting readiness criteria (must be satisfied)

1. Governance charter draft exists and is publicly reviewable.
2. Foundation legal pathway is documented (jurisdiction, board model, conflict-of-interest policy).
3. Trust-root multi-signature key ceremony plan is documented.
4. RFC process is operational and has at least one externally authored accepted RFC.
5. Revocation/suspension policy is exercised in at least one completed drill.

## 4) Measurement definitions

- Production registry: node serving real verification traffic with signed manifest and uptime telemetry.
- External verification traffic: requests not initiated by IndrasNet-controlled infrastructure.
- Breaking drift: conformance outcome changes for previously passing artifacts without declared breaking version/migration.
- Independent CI runner: conformance executor controlled by an external organization with reproducible logs.

## 5) Assessment cadence

- Review frequency: quarterly.
- Evidence sources:
  - verification graph telemetry,
  - trust events stream,
  - conformance run history,
  - signed root-of-trust changelog,
  - public RFC registry.

Assessment output:

- `Not ready`,
- `Conditionally ready` (explicit remediation plan),
- `Ready for foundation transition`.

## 6) Transition decision process

1. Publish readiness report against all criteria.
2. Open public comment window.
3. Final vote under current governance rules.
4. Execute key handover and governance cutover plan.
5. Publish post-transition operational policy with effective date.

## 7) Fallback / rollback rules

If cutover introduces protocol instability:

- temporary dual-steward mode is allowed,
- emergency trust-root safeguarding remains fail-closed,
- rollback requires published incident + remediation timeline.

## 8) Anti-patterns (explicitly disallowed)

- Foundation launch before criteria completion.
- Foundation in name only with no independent signing/conformance capacity.
- Opaque trust-root operations after transition.
- Informal governance changes without RFC + changelog.

## 9) Transition readiness summary template

```
Protocol Version: <x.y>
Current Stewardship: <phase>
Independent Registries: <n>
External Verify Traffic: <x%>
Stable Releases (no breaking drift): <n>
Independent CI Runners: <n>
External Reference Implementations (passing): <n>
Mirror Trust-Root Status: <ok/not ok>
Readiness Decision: <not ready/conditionally ready/ready>
```

