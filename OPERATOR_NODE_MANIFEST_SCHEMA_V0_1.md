# OPERATOR_NODE_MANIFEST_SCHEMA_V0_1.md

## Node Manifest Schema

Defines the required JSON structure for node discovery files located at `/.well-known/decirepo-node`.

### Required Fields
- `node_id`: (string) Unique identifier for the node.
- `operator`: (string) Legal or organizational name of the operator.
- `node_type`: (enum) `reference` | `mirror_verifier` | `registry`.
- `software_version`: (string) Version of the DeciRepo node software.
- `verification_endpoint`: (url) Absolute URI for the `verify` primitive.
- `conformance_status`: (enum) `PASS` | `FAIL` | `PENDING`.
- `public_key`: (string) Public key used for manifest/artifact signing.

### Optional Fields
- `jurisdiction`: (string) Legal jurisdiction of the operator.
- `contact`: (email/url) Technical contact point.
- `documentation_url`: (url) Link to operator-specific node documentation.
- `capabilities`: (array) List of supported optional protocol features.
