# INDRASNET_TO_DECIREPO_LINEAGE_V0_1

Status: Public lineage note  
Scope: Naming, conceptual continuity, and first public technical formalization

---

## Purpose

This note records the public continuity between:

- the earlier Indra's Net / IndrasNet conceptual language,
- the 2025 shift into DAO and product architecture,
- and the 2026 DeciRepo genesis formalization.

It does **not** claim that the early metaphor and the current protocol are identical artifacts.
It records the public lineage of the idea surface and its technical crystallization.

---

## 1. Origin Metaphor

The earliest public layer was expressed through the metaphor of **Indra's Net**:

- a network of mutually reflecting nodes,
- no single center of truth,
- and fragility of the whole when one node carries falsehood or distortion.

In that stage, the language was philosophical and architectural rather than protocol-formal.

Core intuition:

- distortion at one node can propagate through the whole network,
- trust requires more than local assertion,
- and a network cannot remain coherent if falsehood is allowed to pass as truth.

---

## 2. 2025 Architecture Turn

By late 2025, the public language shifted from metaphor into implementation architecture.

Public IndrasNet messaging introduced:

- AI organizers as nodes,
- DAO as a mechanism of consensus,
- ideas becoming products,
- Rust / Solana-based modules,
- and a network understood as a living architecture rather than only a symbol.

This is the point where the earlier metaphor turned into an explicit system design direction:

- each node as an operating unit,
- each interaction as part of a larger network state,
- and the network as something that could produce verifiable history rather than only shared narrative.

In simplified lineage terms:

- **Indra's Net** -> metaphor of interdependence and truth fragility
- **IndrasNet** -> architectural program
- **DAO / product modules** -> operational design surface

---

## 3. 2026 Public Formalization

In 2026, the first public technical formalization appeared through **DeciRepo** and the DLX-compatible public verification surface.

This introduced a stricter protocol language:

- deterministic recomputation,
- MATCH / FAIL verification,
- public artifact lineage,
- root-of-trust publication,
- and independent verification outside the origin environment.

This was the first public point where the earlier network intuition became machine-checkable protocol structure.

The key shift:

- earlier concern: falsehood at one node can corrupt the network
- later protocol expression: published decisions must be independently recomputable and verifiable

This is the bridge from metaphor to protocol.

---

## 4. Genesis Artifact as First Public Root

The first public genesis artifact for this formalized surface is:

- `DR-GENESIS-0001`

Public references:

- Artifact: `https://decirepo.com/artifacts/genesis/DR-GENESIS-0001.json`
- Decision record: `https://decirepo.com/api/decision/DR-GENESIS-0001.json`

Public verification command:

```text
$ node dlx-ref/cli.js verify artifacts/genesis/DR-GENESIS-0001.json
status=PASS
rebuild=MATCH
conformance=PASS
```

Why this matters:

- it is the first public machine-readable root of trust in the DeciRepo protocol surface,
- it can be independently recomputed,
- and it demonstrates that the network did not begin from opaque assertion alone.

In lineage terms, this is the first public technical answer to the earlier intuition that a network must not depend on uncheckable claims at a single node.

---

## 5. Conceptual Continuity

The continuity is not lexical only.

The public through-line is:

1. a network cannot remain trustworthy if falsehood is allowed to propagate invisibly,
2. node interaction must produce a coherent shared surface,
3. shared surface must become externally checkable,
4. protocol trust therefore moves toward recomputation, lineage, and root-of-trust evidence.

This is why the naming continuity matters:

- **IndrasNet** remains the broader ecosystem and stewardship context,
- **DeciRepo** is the public protocol and artifact-verification surface,
- **DLX** is the deterministic execution / boundary-control layer associated with the later architectural turn.

These are distinct layers, but they are not conceptually unrelated.

---

## 6. Scope Boundary

This note establishes public lineage only.

It does **not** claim:

- that all early posts were already protocol specifications,
- that 2025 DAO modules and 2026 DeciRepo were the same implementation,
- or that metaphor should be confused with formal protocol semantics.

What it does claim is narrower:

- the naming,
- the trust model,
- the concern with distortion across nodes,
- and the movement toward verifiable public history

form a coherent public development line from IndrasNet to DeciRepo genesis.

---

## 7. Public Summary

In short:

- **2022-2023**: the problem appeared as a network truth metaphor
- **2025**: the metaphor became architecture and DAO/product language
- **2026**: the architecture reached first public protocol formalization through DeciRepo genesis

That is the lineage this note records.
