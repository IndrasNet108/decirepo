# DECISION_POLICY_DRIFT_DETECTION_V0_1

Status: active feature spec  
Applies to: `DeciRepo Protocol v0.1` and `DeciRepo Cloud by IndrasNet`

## 1) Purpose

Detect and quantify outcome drift caused by policy-version changes using deterministic re-evaluation.

Core question:

- "How many decisions would change outcome under a new policy profile?"

## 2) Scope (v0.1)

Inputs:

- baseline policy version
- target policy version
- decision scope/filter

Output:

- changed vs unchanged counts
- drift rate
- transition matrix (`A->R`, `R->A`, etc.)
- rule/driver breakdown
- changed decision list with explainable rule deltas

## 3) Determinism guarantees

1. Rule evaluation is deterministic and versioned.
2. Same corpus snapshot + same policy pair => identical results.
3. No probabilistic or LLM decisioning in drift detection.

## 4) API contract

Endpoint:

- `GET /api/policy-drift-detection`
- `GET /api/policy-drift-detection.json`

Minimum fields:

- `query`
- `summary`
- `drift_drivers[]`
- `changed_decisions[]`
- `safety`

## 5) Safety boundary

Policy drift detection is analytics support, not decision authority.

- It must not auto-approve/auto-reject cases.
- It must expose rule-based explainability for every changed outcome.
