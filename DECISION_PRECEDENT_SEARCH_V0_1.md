# DECISION_PRECEDENT_SEARCH_V0_1

Status: active feature spec  
Applies to: `DeciRepo Protocol v0.1` and `DeciRepo Cloud by IndrasNet`

## 1) Purpose

Define deterministic precedent lookup for similar decision artifacts.

Core question:

- "Who already made a similar decision and with what outcome?"

## 2) Scope (v0.1 MVP)

Input filters:

- `decision_class` (`A/B/C/D`)
- `policy_family` (string)
- `outcome` (`APPROVED/REJECTED`, optional)
- `time_range` (optional)

Similarity factors:

- class match
- policy family match
- reason code proximity
- numeric risk distance (if available)

Output:

- ordered list of precedent records
- deterministic `similarity_score` in `0..1`
- short `why_matched` explanation

## 3) Determinism requirements

1. Stable scoring weights per protocol version.
2. Same query and corpus snapshot must return same order.
3. Tie-breaker must be canonical (`decision_id` lexical order).

## 4) API contract (MVP)

Endpoint:

- `GET /api/precedent-search`
- `GET /api/precedent-search.json`

Response fields:

- `query`
- `total_candidates`
- `returned`
- `results[]` with:
  - `decision_id`
  - `canonical_id`
  - `decision_class`
  - `policy_family`
  - `outcome`
  - `similarity_score`
  - `why_matched`

## 5) Economic role

Precedent search is a second-layer value product above registry write flow.

- Registry writes: operational base layer
- Precedent search: decision intelligence layer

## 6) Safety constraints

1. Respect visibility policy (`private by default`).
2. Public endpoint must expose only publishable fields.
3. No hidden-policy leakage via match explanations.
