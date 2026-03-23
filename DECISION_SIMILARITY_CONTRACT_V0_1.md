# DECISION_SIMILARITY_CONTRACT_V0_1

**Status:** active governance contract  
**Applies to:** `DeciRepo Protocol v0.1`  
**Purpose:** Deterministic precedent retrieval discipline

## 1. Purpose

Similarity in DeciRepo is a technical mechanism for:
- candidate retrieval (pre-filtering),
- providing precedent comparison context for audit.

**Strict Rule:** Similarity MUST NOT imply recommendation, authority, or correctness of a decision. It is an evidence retrieval tool, not a decision-making advisor.

## 2. Similarity Dimensions

Retrieval is governed by explicit dimensions. A dimension is a field-level match rule.

### Mandatory Dimensions
| Dimension | Field Name | Match Rule | Mismatch Action |
|-----------|------------|------------|-----------------|
| Decision Class | `decision_class` | Exact string match | **EXCLUDE** |
| Policy Family | `policy_family` | Exact string match | **EXCLUDE** |
| Policy Version | `policy_version` | String match (or compatible lineage) | Record mismatch |

### Optional Dimensions
| Dimension | Field Name | Match Rule | Mismatch Action |
|-----------|------------|------------|-----------------|
| Exception Type | `exception_type` | Exact match | Record mismatch |
| Outcome Family | `outcome_family` | Category match | Record mismatch |
| Authority Class| `authority_class`| Exact match | Record mismatch |
| Publisher Class| `publisher_class`| Exact match | Record mismatch |
| Temporal | `generated_at` | Date proximity | Record delta |

## 3. Mandatory Match Conditions

A decision is a valid precedent candidate **ONLY IF** it satisfies all mandatory dimensions.
- If `decision_class` differs → **EXCLUDE**.
- If `policy_family` differs → **EXCLUDE**.

## 4. Similarity Basis

Every retrieval result must expose its `match_basis` and `mismatch` fields to ensure transparency.

**Example Explanation:**
- `match_basis`: [`decision_class`, `policy_family`, `outcome_family`]
- `mismatch`: [`policy_version`, `publisher_class`]

## 5. Ranking Discipline

Ranking must be structured and explainable. General "score" must be decomposed into ranking modes.

### Allowed Ranking Modes
1. `same-policy`: Prioritize candidates with identical `policy_version`.
2. `same-class`: Prioritize candidates within the same `decision_class`.
3. `outcome-divergent`: Prioritize candidates with different outcomes for the same query context (to highlight drift).

### Forbidden Claims
The following terms are **PROHIBITED** in any DeciRepo implementation or UI:
- "best precedent"
- "recommended precedent"
- "most relevant precedent"

## 6. Precedent Exclusion Rules

A decision **MUST NOT** be returned as a precedent if:
1. It fails mandatory match conditions (Class/Family).
2. It has an incompatible policy profile.
3. It contains unresolved policy ambiguity for the current query context.
4. Its artifact validation status is not `PASS`.

## 7. Precedent Search Report Requirements

The `precedent-search-report` artifact must include:
- `reference_decision`: Canonical ID of the query source.
- `candidate_precedents`: List of retrieved candidates with their `match_basis`.
- `similarity_dimensions_used`: List of dimensions active during retrieval.
- `exclusion_rules_applied`: Documentation of any filtered-out candidates.
- `retrieval_timestamp`: Deterministic generation time.

## 8. Governance Rules

- This contract is versioned (`v0.1`).
- Changes to similarity rules are considered protocol changes.
- Breaking changes require a formal RFC and update to `PROTOCOL_STATUS.md`.

## 9. Scope Boundary

- **Governs:** Retrieval logic, candidate eligibility, explanation structure, ranking constraints.
- **Does NOT Govern:** UI styling, specific database indexing methods, non-protocol analytics.
