# Getting Started with DeciRepo

This guide provides a rapid path to deploying a DeciRepo node and performing your first decision verification.

---

## 1. Quick Install

Ensure you have **Node.js (v18+)** installed.

```bash
git clone https://github.com/indrasnet/DeciRepo.git
cd DeciRepo
npm install
```

## 2. Run Local Validation

Verify that your environment matches the protocol reference:

```bash
bash scripts/validate_all.sh
```

A successful run should end with `ALL VALIDATIONS PASSED`.

## 3. Perform Your First Verification

Verify the **Genesis Artifact** against the reference engine:

```bash
node dlx-ref/cli.js verify ./dlx-ref/test-vectors/artifacts/valid_governance_artifact.json
```

## 4. Deploy a Mirror Verifier

To join the network as an independent verifier:

1. **Configure Identity:** Run `node scripts/generate_node_identity.js`.
2. **Setup Manifest:** Create `/.well-known/decirepo-node` using the [Operator Schema](./OPERATOR_NODE_MANIFEST_SCHEMA_V0_1.md).
3. **Public Endpoint:** Expose your node via HTTPS.

For full details, see the [Reference Node Deployment Guide](./REFERENCE_NODE_DEPLOYMENT_GUIDE_V0_1.md).

---

## 5. Core Primitives to Explore

- **Verify:** `verify(decision_id)` via `dlx-ref`.
- **Investigate:** Explore the evidence chain in `api/`.
- **Federate:** View the verification graph in `pages/network.html`.

**DeciRepo: The Verification Layer for Institutional Decisions.**
