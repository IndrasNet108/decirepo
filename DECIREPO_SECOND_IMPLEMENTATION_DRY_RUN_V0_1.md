# DECIREPO_SECOND_IMPLEMENTATION_DRY_RUN_V0_1

Status: Draft

## Purpose

This document defines the minimum dry-run contour for attempting a second DeciRepo-compatible implementation without reading the reference implementation code.

The goal is simple:

```text
Can an independent engineer implement the current public baseline without dlx-ref?
```

## 1. Allowed Files

The dry run may read only the current public baseline materials:

- `DECIREPO_PROTOCOL_FORMAL_SPEC_V0_2.md`
- `DECIREPO_PROTOCOL_CONFORMANCE_V0_1.md`
- `DECIREPO_SECOND_IMPLEMENTATION_PATH_V0_1.md`
- `conformance/v0_1/**`
- `conformance/CONFORMANCE_REPORT_SCHEMA.json`
- `conformance/REFERENCE_CONFORMANCE_REPORT_V0_1.json`

Allowed use of these materials includes:

- vector structure
- vector manifests
- expected outputs
- report schema

The dry run must not read or rely on:

- `dlx-ref/`
- runner code
- internal scripts
- bundle contents as implementation hints if they expose execution convenience beyond the public baseline
- commit history as semantic guidance

If the dry run needs those materials to continue, that is a real protocol or conformance clarity failure.

## 2. Success Criteria

### 2.1 Minimum Success

Minimum success means the independent implementation can:

1. compute `artifact_id` from the published baseline rules;
2. emit the normalized result surface in the required schema;
3. pass all published conformance vectors;
4. produce an overall `PASS`;
5. do all of the above without reading `dlx-ref`.

### 2.2 Strong Success

Strong success means the implementation also can explain, from public materials alone:

1. where the verifier/harness boundary is;
2. how verdict classification works;
3. which parts of the baseline were fully explicit and did not require guesswork.

## 3. Blocker Criteria

A blocker is only something that cannot be implemented honestly without author guesswork.

Count as a blocker only if:

- a rule affects conformance verdict but is not explicit;
- byte-for-byte comparison depends on unspecified ordering or canonicalization;
- the same case can be classified in more than one valid way;
- the verifier/harness boundary cannot be derived from the public baseline;
- vector semantics require guessing baseline behavior;
- an identifier exists but its authoritative algorithm binding is unclear.

Do not count as a blocker:

- the documents are long;
- careful reading was required;
- a simpler example would have been nicer.

## 4. Dry-Run Logging

During the dry run, keep exactly three logs:

### A. Implementation Log

What was implemented, step by step.

### B. Ambiguity Log

Where a design choice had to be made instead of directly following the public baseline.

### C. Blocker Log

Where implementation could not continue honestly without reading forbidden materials.

## 5. Dry-Run Rule

During the dry run:

- do not edit protocol documents on the fly;
- do not add vectors on the fly;
- do not open `dlx-ref`;
- do not ask the author to explain semantics mid-run.

First go as far as possible on the public baseline alone.
Only after that evaluate what actually blocked the implementation.

## 6. Output

The result of the dry run must be one of:

- `PASS`
- `PARTIAL`
- `BLOCKED`

And it must include:

- the ambiguity list;
- the true blocker list;
- the set of things that turned out to be fully explicit.
