# DECIREPO_SECOND_IMPLEMENTATION_RESULT_NOTE_V0_1

Status: Internal note

## Purpose

This note records the practical outcome of the first constrained second-implementation dry run.

It is not part of the normative protocol surface.
It is an internal evidence summary for deciding which claims DeciRepo can now make honestly.

Primary evidence inputs:

- `/tmp/decirepo_second_impl_dry_run_v0_1/DRY_RUN_RESULT.md`
- `/tmp/decirepo_second_impl_dry_run_v0_1/DRY_RUN_RESULT.json`
- `/tmp/decirepo_second_impl_dry_run_v0_1/out/CONFORMANCE_REPORT.json`

## 1. What Was Proven

The constrained dry run reproduced the currently published conformance baseline for:

```text
vector_001 through vector_007
```

The second implementation was able to:

- derive `artifact_id` from the published baseline rules;
- emit the normalized verification result surface;
- produce canonical result bytes matching the published fixtures;
- emit a conformance report matching the published report schema;
- obtain overall `PASS` for the current published vector set.

Practical conclusion:

```text
The current public baseline is independently reproducible for the published conformance set vector_001 through vector_007.
```

## 2. What Was NOT Proven

The dry run did not prove:

- courtroom-grade clean-room independence;
- completeness of semantics outside the published vectors;
- maturity of the full future conformance framework;
- resolution of still-unvectored ambiguity classes such as canonical `CONFORMANCE_ERROR` behavior or published treatment of absent `rebuild_source`.

This dry run was constrained and honest, but not formally isolated.

## 3. Public Claims That Are Now Defensible

The following claims are now supportable:

1. `DeciRepo baseline v0.1 is independently reproducible for the currently published conformance set.`
2. `A second minimal verifier/harness can reproduce the published vectors without relying on dlx-ref during the dry-run implementation phase.`
3. `The published baseline is strong enough to support an implementation-level conformance claim for vectors 001-007.`

These claims should always be paired with scope language such as:

```text
for the currently published conformance baseline
for vector_001 through vector_007
```

## 4. Public Claims That Are NOT Yet Defensible

The following claims should not be made yet:

1. `DeciRepo is fully clean-room proven.`
2. `DeciRepo has no remaining semantic ambiguities.`
3. `The entire protocol is author-independent in all edge cases.`
4. `The conformance framework is complete or maturity-grade.`
5. `All future independent implementations will converge without further clarification.`

## 5. Communication Rule

If this result is referenced publicly, the recommended wording is:

```text
A constrained second-implementation dry run reproduced the current published DeciRepo conformance baseline (vector_001 through vector_007) and achieved PASS without using the reference implementation during the dry-run execution phase.
```

And the required caveat is:

```text
This was a constrained dry run, not a formally isolated clean-room certification.
```

## 6. Next Step

No new protocol notes should be added before evidence from a cleaner second-implementation attempt or a new real blocker appears.

The next useful step is one of:

1. repeat the dry run in a truly clean session or by an external engineer;
2. address only blockers discovered in that cleaner run.
