# DECIREPO_DLX_BOUNDARY_POSITION_NOTE_V0_1

Status: Public note  
Scope: Canonical boundary framing for DeciRepo and DLX

---

## 1. Purpose

This note fixes one narrow public distinction:

- what DeciRepo is,
- what DLX is,
- and where the execution boundary matters.

It is intentionally short.
It does not restate the full protocol, roadmap, or implementation internals.

---

## 2. Boundary

DeciRepo is the public registry surface.

DLX sits behind it.

It does one thing:

it verifies that a bounded decision
remains the same decision when it is executed.

Not described.
Not interpreted.

Executed.

A bounded artifact can be verified.
A bounded transition can be enforced.

DeciRepo records the result:

public, addressable,
and independently recomputable.

Everything else comes later.

First, one condition has to hold:

a decision must be recomputable
and arrive at the same result.

---

## 3. AI Governance Implication

For AI governance, the shift is simple:

governance stops being descriptive.

It becomes enforceable.

Not after the fact.

At the moment of execution.

Before anything is sent, one condition must hold:

the reviewed version
and the outbound version
must remain the same position.

If they diverge, the system does not continue.

---

## 4. Scope Boundary

This note does **not** claim:

- full implementation disclosure,
- broader deployment beyond the currently evidenced public DeciRepo surface,
- or a public roadmap beyond the current Genesis-phase posture.

Its claim is narrower:

- DeciRepo is the registry surface,
- DLX is the verification / control layer behind it,
- and the execution boundary is where governance becomes enforceable.
