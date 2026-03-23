# DeciRepo Reference Node Deployment Guide v0.1

**Status:** Active Operational Guide  
**Applies to:** Mirror Verifier and Registry Nodes

---

## 1. Node Types

Before deployment, select the appropriate node role:

- **Mirror Verifier Node (Recommended):** Independently verifies decisions from other nodes. Does not publish new decision artifacts. Ideal for audit and compliance firms.
- **Registry Node:** Capable of both publishing and verifying decision artifacts. Suitable for organizations that generate institutional decisions.

---

## 2. Minimal Hardware Requirements

- **CPU:** 4 cores (optimized for deterministic recomputation)
- **RAM:** 8 GB
- **Storage:** 100 GB (persistent, SSD recommended)
- **Network:** Public HTTPS endpoint with valid SSL/TLS certificate.

---

## 3. Deployment Steps

### Step 1: Software Installation
```bash
git clone https://github.com/indrasnet/DeciRepo.git
cd DeciRepo
npm install
```

### Step 2: Identity & Security
1. **Generate Identity:** `node scripts/generate_node_identity.js` (produces Ed25519 keypair).
2. **Key Protection:** Store the private key in a secure vault or encrypted environment variable.
3. **Transport Security:** Ensure TLS 1.3 is enabled on your reverse proxy (Nginx/Envoy).
4. **API Protection:** Implement rate limiting for the `/api/verify-request` endpoint to prevent DoS attacks.

### Step 3: Network Bootstrapping
A node can discover the network through multiple sources:
- **Reference Node:** `https://reference.decirepo.com/.well-known/decirepo-node`
- **Public Node Directory:** (if available) Distributed list of trusted manifest URLs.
- **Verification Graph API:** Discover peers by observing existing verification edges.

### Step 4: Publish Discovery Manifest
Create your manifest at `/.well-known/decirepo-node`. Ensure `public_key` matches your generated identity.

---

## 4. Node Health & Monitoring

To maintain a high **Trust Score**, nodes must expose:
- **Uptime:** Consistent availability of the verification API.
- **Health Check:** `GET /api/health` returning software version and runtime status.
- **Activity Log:** Periodic publication of verification counts to the trust events stream.

---

## 5. Conformance Check
Verify that your environment is fully protocol-compliant:
```bash
bash scripts/validate_all.sh
```

---

## 6. Summary
A successfully deployed node provides independent verification capacity. Trust in DeciRepo is not a claim—it is a result of **independent deterministic recomputation** executed by nodes like yours.
