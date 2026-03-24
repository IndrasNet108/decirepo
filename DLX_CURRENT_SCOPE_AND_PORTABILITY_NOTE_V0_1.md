# DLX_CURRENT_SCOPE_AND_PORTABILITY_NOTE_V0_1

Status: Public note  
Scope: Current applied scope of DLX, public verification surface, and portability boundary

---

## 1. Purpose

This note defines the current public scope of DLX as of the DeciRepo `Genesis` phase.

Its purpose is to separate:

- what is publicly deployed and evidenced today,
- what is designed to be portable in principle,
- and what is **not** yet claimed as a public fact.

This note is intentionally conservative.
It exists to prevent theoretical portability from being presented as current multi-network deployment.

---

## 2. Current Applied Scope

At the current public stage, DLX is applied **inside the DeciRepo / IndrasNet ecosystem only**.

Publicly evidenced usage today includes:

- deterministic verification of DeciRepo decision artifacts,
- public `MATCH / FAIL` recomputation surface,
- genesis artifact verification,
- protocol and governance decision verification,
- and bounded municipal procurement challenge/demo cases inside the DeciRepo public surface.

In practical terms, this means:

- DLX is currently part of the DeciRepo control and verification stack,
- not a publicly proven multi-network deployment layer.

---

## 3. What Is Publicly Exposed Today

The public DeciRepo surface currently exposes DLX-compatible verification through:

- `dlx-ref`
- public verification command surface
- public decision artifacts
- public cases and protocol references

Examples in the current public surface include:

- `DR-GENESIS-0001`
- `DR-PROTOCOL-0001`
- `DR-GOV-0001`
- bounded municipal procurement cases in the public demonstration registry

Public verification reference:

```text
$ node dlx-ref/cli.js verify artifacts/genesis/DR-GENESIS-0001.json
status=PASS
rebuild=MATCH
conformance=PASS
```

This is the currently demonstrated public layer.

---

## 4. What Is Not Publicly Claimed

The current public record does **not** claim that DLX is already:

- deployed across multiple independent blockchains,
- integrated into other DAO stacks outside DeciRepo,
- operating as a publicly released standalone SDK for external teams,
- or serving as a live universal plugin across enterprise AI systems.

It also does **not** claim current public production usage in:

- Ethereum governance stacks,
- external Solana governance systems outside the DeciRepo public surface,
- third-party enterprise agent platforms,
- or unrelated public AI networks.

The correct public statement is narrower:

- DLX is currently demonstrated within the DeciRepo / IndrasNet public and reference surface.

---

## 5. Portability by Design

DLX is designed in a way that makes broader applicability plausible in principle.

Publicly visible design indicators include:

- deterministic recomputation,
- hash-based rebuild comparison,
- compatible-node verification posture,
- and execution-bound control framing that is not logically tied to one chain alone.

This makes DLX **portable by design direction**.

But design portability is not the same as public deployment evidence.

That distinction matters.

---

## 6. Why the Distinction Matters

If a system is described as portable, people often assume it is already widely deployed.

That is not the right reading here.

The safer public position is:

- current scope: DeciRepo / IndrasNet
- design intent: broader applicability
- public proof today: DeciRepo artifacts, verification surface, cases, and genesis evidence

This keeps the public record honest.

It also protects the architectural claim from being weakened by premature overreach.

---

## 7. Current Best Public Summary

The most accurate public summary today is:

- DLX is currently a control and verification layer within the DeciRepo public surface,
- not yet a publicly evidenced universal deployment layer across other networks.

At the same time:

- the architecture is intentionally modular enough that broader portability remains a real design direction.

That is a statement of scope, not a marketing ceiling.

---

## 8. Relation to DeciRepo and IndrasNet

The current relationship is best described as:

- **IndrasNet** — broader ecosystem and stewardship context
- **DeciRepo** — public protocol and artifact verification surface
- **DLX** — deterministic execution-bound verification / control layer within that surface

This means DLX should not currently be described as a separate publicly deployed network in its own right.

It is better described as:

- a distinct layer,
- already visible inside DeciRepo,
- with potential future portability beyond it.

---

## 9. Public Summary

In short:

- DLX is public,
- DLX is active,
- DLX is evidenced inside DeciRepo,
- but DLX is not yet publicly evidenced as a broadly deployed external layer across other ecosystems.

That is the correct current boundary.

---

## 10. Related Public References

- `DECIREPO_COMMITMENT_DRIFT_CONTROL_NOTE_V0_1.md`
- `DECIREPO_GENESIS_EVIDENCE_LAYER_V0_1.md`
- `INDRASNET_TO_DECIREPO_LINEAGE_V0_1.md`
- `INDRASNET_SOURCE_TIMELINE_V0_1.md`
- `https://decirepo.com/pages/cases.html`
- `https://decirepo.com/artifacts/genesis/DR-GENESIS-0001.json`
