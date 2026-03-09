# PRIVATE_PUBLIC_BOUNDARY_V0_1

Status: Normative boundary contract  
Applies to: DLX runtime and DeciRepo public protocol surfaces

## Invariant

The public protocol surface must remain reproducible without access to private runtime components or private infrastructure.

## Scope

This document defines the boundary between private DLX runtime components and public DeciRepo protocol surfaces.

It governs:
- artifact generation
- artifact publication
- operational release path

## Public repositories

- `decirepo`  
  protocol reference, schemas, public artifacts, verification tooling

- `decirepo-site`  
  static presentation surface

Public repositories must remain buildable and inspectable without private runtime access.

## Private repositories

- `dlx-runtime-private`  
  deterministic artifact generation runtime

- `decirepo-ops-private`  
  operational tooling, release pipeline, secrets management

## Publish contract

Allowed for public publication:

- artifact envelopes
- artifact SHA256 sidecars
- evidence manifests
- independent verification notes
- deterministic reports explicitly marked publishable

Any new publishable artifact type must be explicitly added to this allowlist.

All published artifacts must be derivable from the public repository state and the artifact itself.

## Never publish

- private runtime code
- internal configuration files
- secrets or credentials
- internal operator logs
- unpublished policy drafts
- non-public test fixtures

## Non-interpretation rule

Public repositories may display deterministic outputs.

They must not compute, modify, or reinterpret them.

Interpretation must occur in the deterministic runtime layer, not in the public presentation surface.

## Workspace rule

Active DLX source:

- `/mnt/d/IndrasNet_Project_Full/DLX`

Frozen DLX baseline:

- `/home/indrasnet/DLX`

The frozen baseline must not be used for active development or artifact generation.

## Operational release path

private runtime
-> deterministic artifact generation
-> immutable publication to decirepo
-> static exposure through decirepo-site

Public repositories must never execute private runtime code.

## Change control

Any change affecting these boundaries requires a versioned protocol change.
