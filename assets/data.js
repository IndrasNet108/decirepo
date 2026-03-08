(function () {
  const CANONICAL_PREFIX = "\u2B21";
  const LOCAL_REGISTRY_ID = "decirepo.com";
  const GOVERNANCE_PUBLISHER_ID = "indrasnet-governance";
  const registries = [
    {
      registry_id: "decirepo.com",
      registry_pubkey: "drpk_6f4d39deci_local_root",
      verify_endpoint: "../api/verify.json",
      conformance_report_endpoint: "../api/conformance-report",
      node_endpoint: "../.well-known/decirepo-node",
      manifest_endpoint: "../api/network/decirepo-node.json",
      trust_score_endpoint: "../api/trust-score",
      conformance_profile: "decirepo-protocol-v0_1-mandatory",
      status: "active"
    },
    {
      registry_id: "bank-registry.eu",
      registry_pubkey: "drpk_91ac22bank_registry",
      verify_endpoint: "../api/network/bank-registry/verify.json",
      node_endpoint: "../api/network/bank-registry/node.json",
      manifest_endpoint: "../api/network/bank-registry/node.json",
      trust_score_endpoint: "../api/trust-score",
      status: "connected"
    },
    {
      registry_id: "municipal-registry.gov",
      registry_pubkey: "drpk_27f11amunicipal_registry",
      verify_endpoint: "../api/network/municipal-registry/verify.json",
      node_endpoint: "../api/network/municipal-registry/node.json",
      manifest_endpoint: "../api/network/municipal-registry/node.json",
      trust_score_endpoint: "../api/trust-score",
      status: "connected"
    }
  ];

  const trustRegistry = {
    validators: [
      {
        validator_id: "DLX-CORE-V1",
        public_key: "valpk_8A3F_dlx_core_v1",
        environment: "DLX v1.0",
        status: "trusted"
      },
      {
        validator_id: "EU-RISK-POLICY-V1",
        public_key: "valpk_5B8C_eu_risk_v1",
        environment: "DLX v1.0",
        status: "trusted"
      },
      {
        validator_id: "MUNICIPAL-PROC-V1",
        public_key: "valpk_72A1_municipal_v1",
        environment: "DLX v1.0",
        status: "trusted"
      }
    ],
    policy_profiles: [
      {
        profile_id: "PROCUREMENT-2026-03",
        policy_versions: ["PROCUREMENT_RULES_V1", "PROCUREMENT_RULES_V2"],
        status: "active"
      },
      {
        profile_id: "FIN-RISK-2026-03",
        policy_versions: ["AUDIT_PROTOCOL_V1"],
        status: "active"
      }
    ],
    trusted_registries: registries.map((registry) => ({
      registry_id: registry.registry_id,
      registry_pubkey: registry.registry_pubkey,
      verify_endpoint: registry.verify_endpoint,
      manifest_endpoint: registry.manifest_endpoint || registry.node_endpoint,
      trust_score_endpoint: registry.trust_score_endpoint || "../api/trust-score",
      status: registry.status
    }))
  };

  const trustScoreModel = {
    model_id: "decirepo-trust-score-v0_1",
    scale: "0..100",
    weights: {
      verify_success_rate: 0.35,
      rebuild_match_rate: 0.30,
      uptime_score: 0.20,
      policy_compatibility: 0.10,
      incident_penalty: 0.05
    }
  };

  const trustMetricsByPerspective = {
    "decirepo.com": {
      "decirepo.com": {
        verify_success_rate: 0.992,
        rebuild_match_rate: 0.987,
        uptime_score: 0.996,
        policy_compatibility: 0.91,
        incident_penalty: -0.01
      },
      "bank-registry.eu": {
        verify_success_rate: 0.976,
        rebuild_match_rate: 0.969,
        uptime_score: 0.989,
        policy_compatibility: 0.88,
        incident_penalty: -0.03
      },
      "municipal-registry.gov": {
        verify_success_rate: 0.955,
        rebuild_match_rate: 0.948,
        uptime_score: 0.974,
        policy_compatibility: 0.83,
        incident_penalty: -0.05
      }
    },
    "bank-registry.eu": {
      "decirepo.com": {
        verify_success_rate: 0.984,
        rebuild_match_rate: 0.978,
        uptime_score: 0.992,
        policy_compatibility: 0.89,
        incident_penalty: -0.02
      },
      "bank-registry.eu": {
        verify_success_rate: 0.989,
        rebuild_match_rate: 0.982,
        uptime_score: 0.993,
        policy_compatibility: 0.92,
        incident_penalty: -0.01
      },
      "municipal-registry.gov": {
        verify_success_rate: 0.951,
        rebuild_match_rate: 0.944,
        uptime_score: 0.968,
        policy_compatibility: 0.79,
        incident_penalty: -0.06
      }
    },
    "municipal-registry.gov": {
      "decirepo.com": {
        verify_success_rate: 0.979,
        rebuild_match_rate: 0.972,
        uptime_score: 0.988,
        policy_compatibility: 0.87,
        incident_penalty: -0.03
      },
      "bank-registry.eu": {
        verify_success_rate: 0.958,
        rebuild_match_rate: 0.949,
        uptime_score: 0.971,
        policy_compatibility: 0.82,
        incident_penalty: -0.05
      },
      "municipal-registry.gov": {
        verify_success_rate: 0.972,
        rebuild_match_rate: 0.964,
        uptime_score: 0.987,
        policy_compatibility: 0.9,
        incident_penalty: -0.02
      }
    }
  };

  const trustMetricsByRegistry = trustMetricsByPerspective[LOCAL_REGISTRY_ID];

  const verificationGraphEdges = [
    {
      source_registry: "decirepo.com",
      target_registry: "bank-registry.eu",
      verify_success_rate: 0.976,
      rebuild_match_rate: 0.969,
      last_verified_at: "2026-03-07T18:12:00Z",
      edge_status: "healthy"
    },
    {
      source_registry: "decirepo.com",
      target_registry: "municipal-registry.gov",
      verify_success_rate: 0.955,
      rebuild_match_rate: 0.948,
      last_verified_at: "2026-03-07T18:10:00Z",
      edge_status: "watch"
    },
    {
      source_registry: "bank-registry.eu",
      target_registry: "decirepo.com",
      verify_success_rate: 0.984,
      rebuild_match_rate: 0.978,
      last_verified_at: "2026-03-07T18:08:00Z",
      edge_status: "healthy"
    },
    {
      source_registry: "bank-registry.eu",
      target_registry: "municipal-registry.gov",
      verify_success_rate: 0.951,
      rebuild_match_rate: 0.944,
      last_verified_at: "2026-03-07T18:07:00Z",
      edge_status: "watch"
    },
    {
      source_registry: "municipal-registry.gov",
      target_registry: "decirepo.com",
      verify_success_rate: 0.979,
      rebuild_match_rate: 0.972,
      last_verified_at: "2026-03-07T18:06:00Z",
      edge_status: "healthy"
    },
    {
      source_registry: "municipal-registry.gov",
      target_registry: "bank-registry.eu",
      verify_success_rate: 0.958,
      rebuild_match_rate: 0.949,
      last_verified_at: "2026-03-07T18:04:00Z",
      edge_status: "watch"
    }
  ];

  const trustEvents = [
    {
      event_id: "te_0001",
      timestamp: "2026-03-07T17:40:00Z",
      type: "registry_added",
      source_registry: "decirepo.com",
      target_registry: "municipal-registry.gov",
      severity: "info",
      details: "Registry admitted after protocol v0.1 compatibility checks."
    },
    {
      event_id: "te_0002",
      timestamp: "2026-03-07T17:51:00Z",
      type: "score_changed",
      source_registry: "decirepo.com",
      target_registry: "bank-registry.eu",
      severity: "info",
      details: "Trust score updated from 90.9 to 91.7 after successful rebuild probes."
    },
    {
      event_id: "te_0003",
      timestamp: "2026-03-07T18:02:00Z",
      type: "verification_mismatch_detected",
      source_registry: "decirepo.com",
      target_registry: "municipal-registry.gov",
      severity: "warning",
      details: "Single mismatch detected and cleared on recheck."
    },
    {
      event_id: "te_0004",
      timestamp: "2026-03-07T18:14:00Z",
      type: "key_rotated",
      source_registry: "bank-registry.eu",
      target_registry: "bank-registry.eu",
      severity: "info",
      details: "Node manifest key rotation announced and signature revalidated."
    },
    {
      event_id: "te_0005",
      timestamp: "2026-03-07T18:16:00Z",
      type: "policy_profile_changed",
      source_registry: "municipal-registry.gov",
      target_registry: "municipal-registry.gov",
      severity: "info",
      details: "Profile MUNICIPAL-PROC-V1 marked active for protocol v0.1."
    }
  ];

  const nodeManifests = {
    "decirepo.com": {
      registry_id: "decirepo.com",
      verify_endpoint: "../api/verify.json",
      trust_endpoint: "../api/trust",
      trust_score_endpoint: "../api/trust-score",
      conformance_report_endpoint: "../api/conformance-report",
      protocol_endpoint: "../api/protocol",
      protocol_version: "v0.1",
      conformance_profile: "decirepo-protocol-v0_1-mandatory",
      compatibility_badge: {
        label: "DeciRepo Protocol Compatible",
        status: "active"
      },
      manifest_url: "../api/network/decirepo-node.json",
      discovery_endpoint: "../.well-known/decirepo-node",
      public_keys: [
        {
          key_id: "drpk_6f4d39deci_local_root",
          algorithm: "ed25519",
          purpose: "registry_signature"
        }
      ],
      capabilities: ["verify", "lineage", "trust-score", "policy-impact", "conformance-report"],
      manifest_issued_at: "2026-03-07T18:00:00Z",
      signature: {
        algorithm: "ed25519",
        signed_payload_hash: "4f83c7e5d36f3c19a97d4ef2df5ad4b2dc40b1db7beffeb193331668ec0db30f",
        value: "sig_decirepo_manifest_v0_1_9c11"
      }
    },
    "bank-registry.eu": {
      registry_id: "bank-registry.eu",
      verify_endpoint: "../api/network/bank-registry/verify.json",
      trust_endpoint: "../api/trust",
      trust_score_endpoint: "../api/trust-score",
      protocol_version: "v0.1",
      public_keys: [
        {
          key_id: "drpk_91ac22bank_registry",
          algorithm: "ed25519",
          purpose: "registry_signature"
        }
      ],
      capabilities: ["verify", "lineage", "trust-score"],
      manifest_issued_at: "2026-03-07T17:58:00Z",
      signature: {
        algorithm: "ed25519",
        signed_payload_hash: "dd9d2b8e3055e223f4f4cd0e19cf5f5f2ad274a2fa2fda2a5f3d708c26ef30bc",
        value: "sig_bank_manifest_v0_1_1a7b"
      }
    },
    "municipal-registry.gov": {
      registry_id: "municipal-registry.gov",
      verify_endpoint: "../api/network/municipal-registry/verify.json",
      trust_endpoint: "../api/trust",
      trust_score_endpoint: "../api/trust-score",
      protocol_version: "v0.1",
      public_keys: [
        {
          key_id: "drpk_27f11amunicipal_registry",
          algorithm: "ed25519",
          purpose: "registry_signature"
        }
      ],
      capabilities: ["verify", "lineage"],
      manifest_issued_at: "2026-03-07T17:56:00Z",
      signature: {
        algorithm: "ed25519",
        signed_payload_hash: "f0f31a8b67f52f15ab4c07ad5cf971fbc6cb67f0d8a7f366d2c6dbb6ec66cf0d",
        value: "sig_municipal_manifest_v0_1_4e2f"
      }
    }
  };

  const decisions = [
    {
      id: "DR-GENESIS-0001",
      title: "DeciRepo Network Genesis Anchor",
      authority: "IndrasNet Protocol Steward",
      outcome: "APPROVED",
      policy: "V0.1",
      policyVersion: "DECIREPO_PROTOCOL_V0_1",
      date: "2026-03-07",
      publisher: GOVERNANCE_PUBLISHER_ID,
      input: {
        network_status: "genesis",
        steward_id: "indrasnet-steward-001"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "NETWORK_GENESIS_INITIALIZED"
      },
      artifact: {
        artifact_hash: "7770000000000000000000000000000000000000000000000000000000000777",
        validator_result: "PASS",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID
      }
    },
    {
      id: "DR-PROTOCOL-0001",
      title: "Protocol Freeze v0.1",
      authority: "IndrasNet Protocol Council",
      outcome: "APPROVED",
      policy: "V0.1",
      policyVersion: "DECIREPO_PROTOCOL_V0_1",
      date: "2026-03-07",
      publisher: GOVERNANCE_PUBLISHER_ID,
      rfc_ref: "RFC-0001",
      input: {
        proposal_type: "protocol_freeze",
        scope: "artifact_spec + verify_contract + handshake",
        breaking_changes_allowed: false,
        exception_path: "security_critical_only",
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Protocol semantics must be deterministic and versioned",
        exception_rule: "Security-critical emergency path only"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "PROTOCOL_FREEZE_ADOPTED"
      },
      artifact: {
        artifact_hash: "91fbb68f8f1232d2f2d2d6d875f7e6c2684f3aef2b9e06dcb1598ac3dbf4a501",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-TRUST-0001",
      title: "Trust Root Initialization",
      authority: "IndrasNet Trust Operations Board",
      outcome: "APPROVED",
      policy: "V0.1",
      policyVersion: "ROOT_OF_TRUST_V0_1",
      date: "2026-03-07",
      publisher: GOVERNANCE_PUBLISHER_ID,
      rfc_ref: "RFC-0002",
      input: {
        operation: "trust_root_bootstrap",
        signing_model: "single_steward",
        publication_mode: "signed_public_list",
        changelog_required: true,
        risk_score: "high"
      },
      policyContext: {
        policy_rule: "Trust list operations must be signed and versioned",
        exception_rule: "No unsigned trust updates allowed"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "TRUST_ROOT_BOOTSTRAPPED"
      },
      artifact: {
        artifact_hash: "3f4c17fd0a47b562c3f66a6871b70b7dc98113ac0b4dc005456ed3edeb487a39",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-CONF-0001",
      title: "Conformance Suite Release v0.1",
      authority: "IndrasNet Verification Engineering",
      outcome: "APPROVED",
      policy: "V0.1",
      policyVersion: "CONFORMANCE_POLICY_V0_1",
      date: "2026-03-07",
      publisher: GOVERNANCE_PUBLISHER_ID,
      rfc_ref: "RFC-0003",
      input: {
        suite_scope: "artifact + manifest + handshake + negative_tests",
        mandatory_profile: "protocol_v0_1",
        ci_visibility: "public",
        fail_closed_required: true,
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Compatibility is determined by deterministic pass/fail tests",
        exception_rule: "No compatibility badge without conformance pass"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "CONFORMANCE_V0_1_RELEASED"
      },
      artifact: {
        artifact_hash: "5d92b99e21e9ac34bb23d1f99074269763718fce877d71f5e47ef4206f52a4e0",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-REFNODE-0001",
      title: "Reference Node Activation",
      authority: "IndrasNet Infrastructure Operations",
      outcome: "APPROVED",
      policy: "V0.1",
      policyVersion: "REFERENCE_NODE_POLICY_V0_1",
      date: "2026-03-07",
      publisher: GOVERNANCE_PUBLISHER_ID,
      rfc_ref: "RFC-0004",
      input: {
        endpoint_discovery: "/.well-known/decirepo-node",
        manifest_signature: "required",
        uptime_target: "99.9%",
        verify_endpoint: "active",
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Reference behavior must be discoverable and verifiable",
        exception_rule: "No silent protocol capability changes"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "REFERENCE_NODE_ACTIVATED"
      },
      artifact: {
        artifact_hash: "2ae941dc9496a6de087b6fdd8f73f3c6f7f77d8b3b98991c5e3f64d07b18e1c6",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-GOV-0001",
      title: "Governance Policy Adoption",
      authority: "IndrasNet Governance Council",
      outcome: "APPROVED",
      policy: "V0.1",
      policyVersion: "GOVERNANCE_POLICY_V0_1",
      date: "2026-03-07",
      publisher: GOVERNANCE_PUBLISHER_ID,
      rfc_ref: "RFC-0005",
      input: {
        governance_model: "founder_to_foundation_phased",
        current_phase: "founder_stewardship",
        next_phase: "co-governance",
        readiness_gate: "foundation_readiness_criteria_v0_1",
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Governance transitions require objective readiness criteria",
        exception_rule: "No phase transition without published readiness report"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "GOVERNANCE_POLICY_ADOPTED"
      },
      artifact: {
        artifact_hash: "b7478651169472eb80e6ba42d9df4ed6cf4b1e22ba95f0f05c2e39484a69fd43",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-0001",
      title: "Emergency Heating Fuel Waiver",
      authority: "Municipal Procurement Committee",
      outcome: "APPROVED",
      policy: "V1",
      policyVersion: "PROCUREMENT_RULES_V1",
      date: "2026-03-01",
      input: {
        procurement_type: "heating_fuel",
        estimated_amount: "240000",
        emergency_condition: true,
        exception_requested: true,
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Open tender required above threshold",
        exception_rule: "Waiver allowed under emergency condition"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "EMERGENCY_SUPPLY_EXCEPTION"
      },
      artifact: {
        artifact_hash: "a9d325b8f1d4c3ee28733f5e0f5d9479e1c207bcafe4da77d5d47f1120aa3c4f",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-0002",
      title: "Non-Emergency Fuel Request",
      authority: "Municipal Procurement Committee",
      outcome: "REJECTED",
      policy: "V1",
      policyVersion: "PROCUREMENT_RULES_V1",
      date: "2026-03-01",
      input: {
        procurement_type: "heating_fuel",
        estimated_amount: "240000",
        emergency_condition: false,
        exception_requested: true,
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Open tender required above threshold",
        exception_rule: "Waiver allowed under emergency condition"
      },
      outcomeFields: {
        decision: "REJECTED",
        reason_code: "NO_EMERGENCY_CONDITION"
      },
      artifact: {
        artifact_hash: "4e7fdff3dc13f61f6f0c32aa4d53757a729f4d62189c74dbfdff8a1ad2124ea2",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-0003",
      title: "Approved Vendor Waiver",
      authority: "Municipal Procurement Committee",
      outcome: "APPROVED",
      policy: "V1",
      policyVersion: "PROCUREMENT_RULES_V1",
      date: "2026-03-02",
      input: {
        procurement_type: "heating_fuel",
        estimated_amount: "210000",
        emergency_condition: true,
        exception_requested: true,
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Verified vendor required for direct waiver",
        exception_rule: "Emergency waiver for verified vendor"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "VERIFIED_VENDOR_EXCEPTION"
      },
      artifact: {
        artifact_hash: "2e2dbf0727412b653595f0ab9b89fc8a426ea51f30e97352c7d18548fe2eec6d",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-0004",
      title: "Unverified Vendor Request",
      authority: "Municipal Procurement Committee",
      outcome: "REJECTED",
      policy: "V1",
      policyVersion: "PROCUREMENT_RULES_V1",
      date: "2026-03-02",
      input: {
        procurement_type: "heating_fuel",
        estimated_amount: "210000",
        emergency_condition: true,
        exception_requested: true,
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Verified vendor required for direct waiver",
        exception_rule: "Emergency waiver for verified vendor"
      },
      outcomeFields: {
        decision: "REJECTED",
        reason_code: "UNVERIFIED_VENDOR"
      },
      artifact: {
        artifact_hash: "f10e92d4a8972c4b76f6630a17cf7f4d938cbcc99901b05702229f0a5b1cc812",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-0005",
      title: "Purchase Below Tender Threshold",
      authority: "Municipal Procurement Committee",
      outcome: "APPROVED",
      policy: "V1",
      policyVersion: "PROCUREMENT_RULES_V1",
      date: "2026-03-03",
      input: {
        procurement_type: "heating_fuel",
        estimated_amount: "180000",
        emergency_condition: false,
        exception_requested: false,
        risk_score: "low"
      },
      policyContext: {
        policy_rule: "Open tender required above threshold",
        exception_rule: "Not required below threshold"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "BELOW_THRESHOLD_STANDARD_PROCESS"
      },
      artifact: {
        artifact_hash: "cbf004172faef93606d7d6744f8fd2e8b94f0df292f2668e43d51a69aa301146",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-0006",
      title: "Purchase Above Threshold",
      authority: "Municipal Procurement Committee",
      outcome: "REJECTED",
      policy: "V1",
      policyVersion: "PROCUREMENT_RULES_V1",
      date: "2026-03-03",
      input: {
        procurement_type: "heating_fuel",
        estimated_amount: "260000",
        emergency_condition: false,
        exception_requested: false,
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "Open tender required above threshold",
        exception_rule: "Waiver allowed only under emergency"
      },
      outcomeFields: {
        decision: "REJECTED",
        reason_code: "ABOVE_THRESHOLD_TENDER_REQUIRED"
      },
      artifact: {
        artifact_hash: "a10ed2a595d3ecf21338117408f99fd0f9adf7324f17b2d45bff320f97fca416",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: "municipal-registry.gov",
        validator_profile: "MUNICIPAL-PROC-V1"
      }
    },
    {
      id: "DR-0007",
      title: "Decision Under Procurement Policy V1",
      authority: "Municipal Procurement Committee",
      outcome: "APPROVED",
      policy: "V1",
      policyVersion: "PROCUREMENT_RULES_V1",
      date: "2026-03-04",
      input: {
        procurement_type: "heating_fuel",
        estimated_amount: "220000",
        emergency_condition: true,
        exception_requested: true,
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "V1 allows waiver with low stock window",
        exception_rule: "Stock window exception"
      },
      outcomeFields: {
        decision: "APPROVED",
        reason_code: "V1_STOCK_WINDOW_EXCEPTION"
      },
      artifact: {
        artifact_hash: "8f2a621a2a8b340f5e81dd1f2be46efe8fd3270f4b59431895f6f649d8cb8804",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-0008",
      title: "Decision Under Procurement Policy V2",
      authority: "Municipal Procurement Committee",
      outcome: "REJECTED",
      policy: "V2",
      policyVersion: "PROCUREMENT_RULES_V2",
      date: "2026-03-04",
      input: {
        procurement_type: "heating_fuel",
        estimated_amount: "220000",
        emergency_condition: true,
        exception_requested: true,
        risk_score: "medium"
      },
      policyContext: {
        policy_rule: "V2 requires formal emergency declaration",
        exception_rule: "Waiver requires formal declaration"
      },
      outcomeFields: {
        decision: "REJECTED",
        reason_code: "MISSING_FORMAL_EMERGENCY_DECLARATION"
      },
      artifact: {
        artifact_hash: "d2f08b9f2d241b7bb3e4f3453f58cd1947b0d41a7d19f013ba4a2fb2112767fb",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: "bank-registry.eu",
        validator_profile: "EU-RISK-POLICY-V1"
      }
    },
    {
      id: "DR-0009",
      title: "Artifact Verification Example",
      authority: "City Internal Audit Unit",
      outcome: "VERIFIED",
      policy: "V2",
      policyVersion: "AUDIT_PROTOCOL_V1",
      date: "2026-03-05",
      input: {
        decision_reference: "DR-0001",
        verification_scope: "artifact_integrity",
        exception_requested: false,
        risk_score: "low"
      },
      policyContext: {
        policy_rule: "Every decision must be verifiable",
        exception_rule: "None"
      },
      outcomeFields: {
        decision: "VERIFIED",
        reason_code: "ARTIFACT_INTEGRITY_VALID"
      },
      artifact: {
        artifact_hash: "6a6ad0dc873e031b913f3ed5528ec25106e56a6f0f3f2706f4cf149ca90ecdd8",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    },
    {
      id: "DR-0010",
      title: "Rebuild Identity Example",
      authority: "City Runtime Control Unit",
      outcome: "VERIFIED",
      policy: "V2",
      policyVersion: "AUDIT_PROTOCOL_V1",
      date: "2026-03-06",
      input: {
        decision_reference: "DR-0001",
        rebuild_engine: "deterministic_runtime_v1",
        exception_requested: false,
        risk_score: "low"
      },
      policyContext: {
        policy_rule: "Rebuild hash must match",
        exception_rule: "None"
      },
      outcomeFields: {
        decision: "VERIFIED",
        reason_code: "REBUILD_IDENTICAL_HASH"
      },
      artifact: {
        artifact_hash: "3a4fbd631f6d84877d9d04df44216cdd8fcb80a5478d3d7a58bf0263fd6e4b3a",
        validator_result: "PASS",
        runtime_identity: "VERIFIED",
        rebuild_status: "MATCH",
        origin_registry: LOCAL_REGISTRY_ID,
        validator_profile: "DLX-CORE-V1"
      }
    }
  ];

  function shortHashFromFullHash(fullHash) {
    return String(fullHash || "").slice(0, 6).toUpperCase();
  }

  function canonicalIdForDecision(decision) {
    return `${CANONICAL_PREFIX}${shortHashFromFullHash(decision.artifact.artifact_hash)}`;
  }

  const publisherLabels = {
    "indrasnet-governance": "IndrasNet Governance",
    "municipal-procurement-demo": "Municipal Procurement Demo"
  };

  function resolvePublisherLabel(publisherId) {
    const key = String(publisherId || "").trim().toLowerCase();
    return publisherLabels[key] || key || "unknown";
  }

  decisions.forEach((decision) => {
    if (!decision.publisher) {
      decision.publisher = "municipal-procurement-demo";
    }
    decision.short_hash = shortHashFromFullHash(decision.artifact.artifact_hash);
    decision.canonical_id = canonicalIdForDecision(decision);
    decision.publisher_label = resolvePublisherLabel(decision.publisher);
  });

  const primaryIds = [
    "DR-0001",
    "DR-0002",
    "DR-0003",
    "DR-0004",
    "DR-0005",
    "DR-0006",
    "DR-0007",
    "DR-0008"
  ];

  const comparePairs = {
    "DR-PROTOCOL-0001": "DR-TRUST-0001",
    "DR-TRUST-0001": "DR-PROTOCOL-0001",
    "DR-CONF-0001": "DR-REFNODE-0001",
    "DR-REFNODE-0001": "DR-CONF-0001",
    "DR-0001": "DR-0002",
    "DR-0002": "DR-0001",
    "DR-0003": "DR-0004",
    "DR-0004": "DR-0003",
    "DR-0005": "DR-0006",
    "DR-0006": "DR-0005",
    "DR-0007": "DR-0008",
    "DR-0008": "DR-0007"
  };

  const lineageEdges = [
    { parent: "DR-PROTOCOL-0001", child: "DR-TRUST-0001", relation: "Freeze anchors trust-root initialization" },
    { parent: "DR-TRUST-0001", child: "DR-CONF-0001", relation: "Trust root scopes conformance release" },
    { parent: "DR-CONF-0001", child: "DR-REFNODE-0001", relation: "Conformance enables reference-node activation" },
    { parent: "DR-REFNODE-0001", child: "DR-GOV-0001", relation: "Reference operations formalized in governance policy" },
    { parent: "DR-0001", child: "DR-0002", relation: "Emergency condition removed" },
    { parent: "DR-0003", child: "DR-0004", relation: "Vendor verification failed" },
    { parent: "DR-0005", child: "DR-0006", relation: "Threshold exceeded" },
    { parent: "DR-0007", child: "DR-0008", relation: "Policy V2 stricter declaration" },
    { parent: "DR-0001", child: "DR-0009", relation: "Audit verification" },
    { parent: "DR-0001", child: "DR-0010", relation: "Runtime rebuild identity" }
  ];

  function getDecisionById(id) {
    return decisions.find((d) => d.id === id) || null;
  }

  function getDecisionByHash(hash) {
    const normalized = String(hash || "").trim().toLowerCase();
    return decisions.find((d) => d.artifact.artifact_hash.toLowerCase() === normalized) || null;
  }

  function getDecisionByShortHash(shortHash) {
    const normalized = String(shortHash || "").trim().toUpperCase();
    return decisions.find((d) => d.short_hash === normalized) || null;
  }

  function getDecisionByCanonicalId(canonicalId) {
    const normalized = String(canonicalId || "").trim().toUpperCase();
    return decisions.find((d) => d.canonical_id.toUpperCase() === normalized) || null;
  }

  function normalizeCanonicalLikeQuery(query) {
    return String(query || "")
      .trim()
      .toUpperCase()
      .replace(CANONICAL_PREFIX, "")
      .replace(/^0X/, "")
      .replace(/[^0-9A-F]/g, "");
  }

  function resolveDecision(query) {
    const raw = String(query || "").trim();
    if (!raw) return null;

    const byId = getDecisionById(raw.toUpperCase());
    if (byId) return byId;

    const byCanonical = getDecisionByCanonicalId(raw);
    if (byCanonical) return byCanonical;

    const normalizedHex = normalizeCanonicalLikeQuery(raw);
    if (normalizedHex.length === 6) {
      const byShort = getDecisionByShortHash(normalizedHex);
      if (byShort) return byShort;
    }
    if (normalizedHex.length === 64) {
      const byFullHash = getDecisionByHash(normalizedHex);
      if (byFullHash) return byFullHash;
    }

    return getDecisionByHash(raw);
  }

  function primaryDecisions() {
    return primaryIds.map(getDecisionById).filter(Boolean);
  }

  function getPairId(id) {
    return comparePairs[id] || null;
  }

  function getRegistryById(registryId) {
    const id = String(registryId || "").trim().toLowerCase();
    return registries.find((registry) => registry.registry_id.toLowerCase() === id) || null;
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function getTrustComponents(registryId, perspectiveRegistryId = LOCAL_REGISTRY_ID) {
    const targetId = String(registryId || "").trim().toLowerCase();
    const perspectiveId = String(perspectiveRegistryId || LOCAL_REGISTRY_ID).trim().toLowerCase();
    const perspectiveMap = trustMetricsByPerspective[perspectiveId] || trustMetricsByPerspective[LOCAL_REGISTRY_ID];
    return perspectiveMap ? (perspectiveMap[targetId] || null) : null;
  }

  function computeTrustScoreFromComponents(components) {
    if (!components) return null;
    const w = trustScoreModel.weights;
    const verifySuccessRate = clamp(Number(components.verify_success_rate || 0), 0, 1);
    const rebuildMatchRate = clamp(Number(components.rebuild_match_rate || 0), 0, 1);
    const uptimeScore = clamp(Number(components.uptime_score || 0), 0, 1);
    const policyCompatibility = clamp(Number(components.policy_compatibility || 0), 0, 1);
    const incidentPenalty = clamp(Number(components.incident_penalty || 0), -1, 0);

    const scoreRaw = (
      w.verify_success_rate * verifySuccessRate +
      w.rebuild_match_rate * rebuildMatchRate +
      w.uptime_score * uptimeScore +
      w.policy_compatibility * policyCompatibility +
      w.incident_penalty * incidentPenalty
    );
    const trustScore = clamp(scoreRaw * 100, 0, 100);

    return {
      trust_score: Number(trustScore.toFixed(1)),
      components: {
        verify_success_rate: verifySuccessRate,
        rebuild_match_rate: rebuildMatchRate,
        uptime_score: uptimeScore,
        policy_compatibility: policyCompatibility,
        incident_penalty: incidentPenalty
      }
    };
  }

  function getTrustScore(registryId, perspectiveRegistryId = LOCAL_REGISTRY_ID) {
    const registry = getRegistryById(registryId);
    const components = getTrustComponents(registryId, perspectiveRegistryId);
    if (!registry || !components) return null;
    const result = computeTrustScoreFromComponents(components);
    return {
      perspective_registry: String(perspectiveRegistryId || LOCAL_REGISTRY_ID).trim().toLowerCase(),
      registry: registry.registry_id,
      trust_score: result.trust_score,
      components: result.components
    };
  }

  function getAllTrustScores(perspectiveRegistryId = LOCAL_REGISTRY_ID) {
    return registries
      .map((registry) => getTrustScore(registry.registry_id, perspectiveRegistryId))
      .filter(Boolean);
  }

  function buildTrustScorePayload(perspectiveRegistryId = LOCAL_REGISTRY_ID) {
    return {
      perspective_registry: String(perspectiveRegistryId || LOCAL_REGISTRY_ID).trim().toLowerCase(),
      model: trustScoreModel,
      registries: getAllTrustScores(perspectiveRegistryId),
      last_updated: "2026-03-07T18:20:00Z"
    };
  }

  function resolveEdgeStatus(verifySuccessRate, rebuildMatchRate) {
    if (verifySuccessRate >= 0.97 && rebuildMatchRate >= 0.96) return "healthy";
    if (verifySuccessRate >= 0.94 && rebuildMatchRate >= 0.93) return "watch";
    return "degraded";
  }

  function buildVerificationGraphPayload(perspectiveRegistryId = LOCAL_REGISTRY_ID) {
    const sourceRegistry = String(perspectiveRegistryId || LOCAL_REGISTRY_ID).trim().toLowerCase();
    const scores = getAllTrustScores(sourceRegistry).filter((row) => row.registry !== sourceRegistry);
    const edges = scores.map((row, idx) => ({
      source_registry: sourceRegistry,
      target_registry: row.registry,
      verify_success_rate: row.components.verify_success_rate,
      rebuild_match_rate: row.components.rebuild_match_rate,
      last_verified_at: `2026-03-07T18:${String(12 - idx).padStart(2, "0")}:00Z`,
      edge_status: resolveEdgeStatus(row.components.verify_success_rate, row.components.rebuild_match_rate)
    }));
    return {
      perspective_registry: sourceRegistry,
      edges,
      generated_at: "2026-03-07T18:20:00Z"
    };
  }

  function buildTrustEventsPayload() {
    return {
      perspective_registry: LOCAL_REGISTRY_ID,
      events: trustEvents,
      last_updated: "2026-03-07T18:20:00Z"
    };
  }

  function getNodeManifest(registryId) {
    const id = String(registryId || "").trim().toLowerCase();
    return nodeManifests[id] || null;
  }

  async function verifyWithRegistry(decision, options = {}) {
    if (!decision || !decision.artifact) {
      return { ok: false, source: "local", reason: "DECISION_NOT_FOUND" };
    }

    const originRegistryId = decision.artifact.origin_registry || LOCAL_REGISTRY_ID;
    const registry = getRegistryById(originRegistryId);
    if (!registry) {
      return { ok: false, source: "network", reason: "REGISTRY_NOT_TRUSTED", origin_registry: originRegistryId };
    }

    if (originRegistryId === LOCAL_REGISTRY_ID) {
      const localOk = decision.artifact.validator_result === "PASS" && decision.artifact.rebuild_status === "MATCH";
      return {
        ok: localOk,
        source: "local",
        origin_registry: originRegistryId,
        validator: decision.artifact.validator_result,
        rebuild_result: decision.artifact.rebuild_status,
        environment: "DLX v1.0"
      };
    }

    const timeoutMs = Number(options.timeout_ms || 2500);
    const signalController = typeof AbortController !== "undefined" ? new AbortController() : null;
    let timeoutHandle = null;
    if (signalController) {
      timeoutHandle = setTimeout(() => signalController.abort(), timeoutMs);
    }

    try {
      const response = await fetch(registry.verify_endpoint, {
        cache: "no-store",
        signal: signalController ? signalController.signal : undefined
      });
      if (!response.ok) {
        return { ok: false, source: "network", origin_registry: originRegistryId, reason: `REMOTE_HTTP_${response.status}` };
      }
      const payload = await response.json();
      const hashMatch = String(payload.artifact_hash || "").toLowerCase() === String(decision.artifact.artifact_hash || "").toLowerCase();
      const statusOk = String(payload.status || "").toUpperCase() === "VERIFIED" || String(payload.validator || "").toUpperCase() === "PASS";
      const rebuildOk = String(payload.rebuild_result || "").toUpperCase() === "MATCH";
      return {
        ok: hashMatch && statusOk && rebuildOk,
        source: "network",
        origin_registry: originRegistryId,
        validator: payload.validator || "UNKNOWN",
        rebuild_result: payload.rebuild_result || "UNKNOWN",
        environment: payload.environment || "N/A",
        artifact_hash: payload.artifact_hash || "",
        reason: hashMatch ? undefined : "REMOTE_HASH_MISMATCH"
      };
    } catch (error) {
      return {
        ok: false,
        source: "network",
        origin_registry: originRegistryId,
        reason: "REMOTE_VERIFY_UNAVAILABLE",
        error: String(error && error.message ? error.message : error || "")
      };
    } finally {
      if (timeoutHandle) clearTimeout(timeoutHandle);
    }
  }

  function childrenOf(id) {
    const decisionId = String(id || "");
    return lineageEdges.filter((edge) => edge.parent === decisionId);
  }

  function parentsOf(id) {
    const decisionId = String(id || "");
    return lineageEdges.filter((edge) => edge.child === decisionId);
  }

  window.DeciRepoData = {
    decisions,
    CANONICAL_PREFIX,
    LOCAL_REGISTRY_ID,
    registries,
    trustRegistry,
    trustScoreModel,
    trustMetricsByRegistry,
    trustMetricsByPerspective,
    verificationGraphEdges,
    trustEvents,
    nodeManifests,
    primaryIds,
    lineageEdges,
    getDecisionById,
    getDecisionByHash,
    getDecisionByShortHash,
    getDecisionByCanonicalId,
    resolveDecision,
    primaryDecisions,
    getPairId,
    getRegistryById,
    getTrustComponents,
    computeTrustScoreFromComponents,
    getTrustScore,
    getAllTrustScores,
    buildTrustScorePayload,
    buildVerificationGraphPayload,
    buildTrustEventsPayload,
    getNodeManifest,
    verifyWithRegistry,
    childrenOf,
    parentsOf
  };
})();
