# DECISION_PRECEDENT_SEARCH_REPORT_V0_1

Status: active report contract  
Applies to: `DeciRepo Protocol v0.1`

## 1) Purpose

Define a deterministic, auditable artifact for precedent retrieval runs.

Core role:

- attach precedent evidence to decision/audit packages.

## 2) Endpoint

- `GET /api/precedent-search-report`
- `GET /api/precedent-search-report.json`

## 3) Required report fields

- `report_id`
- `generated_at`
- `query_context`
- `results_summary`
- `returned_precedents[]`
- `selected_precedent`
- `links` (`compare`, `verify`, `open_decision`)
- `safety` flags (`recommendation_mode=false`)

## 4) Determinism rules

1. Report must reference explicit query context.
2. Same query + same corpus snapshot must produce identical precedent order.
3. Tie-breaker must be explicit (lexical decision id or equivalent).

## 5) Safety boundary

Precedent report is evidence, not decision authority.

- no automatic approval/rejection,
- no hidden scoring factors,
- explicit match basis required.
