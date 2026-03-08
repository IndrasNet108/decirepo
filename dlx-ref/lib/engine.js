"use strict";

/**
 * DLX Reference Engine
 * Lead Architect & Creator: Oleg Surkov
 */

const fs = require('fs');
const path = require("path");
const crypto = require("crypto");

const ARTIFACT_SCHEMA_VERSION = "dlx-artifact-v0.1";
const HEX64 = /^[0-9a-f]{64}$/i;

const ALLOWED_TRANSITIONS = {
  DRAFT: ["PROPOSED"],
  PROPOSED: ["VALIDATED"],
  VALIDATED: ["PUBLISHED", "SUSPENDED"],
  PUBLISHED: ["SUSPENDED", "REVOKED"],
  SUSPENDED: ["REVOKED"]
};

function stableStringify(value) {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableStringify(item)).join(",")}]`;
  }
  const keys = Object.keys(value).sort();
  const body = keys
    .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
    .join(",");
  return `{${body}}`;
}

function sha256Hex(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

function readJson(filePath) {
  const abs = path.resolve(filePath);
  return JSON.parse(fs.readFileSync(abs, "utf8"));
}

function isHex64(value) {
  return HEX64.test(String(value || ""));
}

function validateTransitionChain(chain) {
  const errors = [];
  if (!Array.isArray(chain) || chain.length === 0) {
    return { ok: false, errors: ["transition_chain must be a non-empty array"] };
  }

  for (let i = 0; i < chain.length; i += 1) {
    const step = chain[i];
    const prefix = `transition_chain[${i}]`;
    if (!step || typeof step !== "object") {
      errors.push(`${prefix} must be an object`);
      continue;
    }
    if (!step.from || !step.to) {
      errors.push(`${prefix} requires from/to`);
      continue;
    }
    if (!isHex64(step.evidence_hash)) {
      errors.push(`${prefix}.evidence_hash must be 64-char hex`);
    }
    const allowed = ALLOWED_TRANSITIONS[step.from] || [];
    if (!allowed.includes(step.to)) {
      errors.push(`${prefix} invalid transition ${step.from} -> ${step.to}`);
    }
    if (i > 0) {
      const prev = chain[i - 1];
      if (prev && prev.to !== step.from) {
        errors.push(`${prefix} chain break: previous.to (${prev.to}) != current.from (${step.from})`);
      }
    }
  }

  return { ok: errors.length === 0, errors };
}

function verifyArtifact(artifact) {
  const errors = [];
  const warnings = [];

  if (!artifact || typeof artifact !== "object") {
    return {
      command: "verify",
      status: "FAIL",
      errors: ["artifact must be an object"],
      warnings
    };
  }

  if (artifact.schema_version !== ARTIFACT_SCHEMA_VERSION) {
    errors.push(`schema_version must be ${ARTIFACT_SCHEMA_VERSION}`);
  }

  if (!isHex64(artifact.artifact_hash)) {
    errors.push("artifact_hash must be 64-char hex");
  }

  if (!["PASS", "FAIL"].includes(artifact.validator_result)) {
    errors.push("validator_result must be PASS or FAIL");
  }

  if (!["MATCH", "MISMATCH"].includes(artifact.rebuild_result)) {
    errors.push("rebuild_result must be MATCH or MISMATCH");
  }

  if (artifact.validator_result === "PASS" && artifact.rebuild_result !== "MATCH") {
    errors.push("PASS validator_result requires MATCH rebuild_result");
  }

  let computedRebuildHash = null;
  if (artifact.rebuild_source && typeof artifact.rebuild_source === "object") {
    computedRebuildHash = sha256Hex(stableStringify(artifact.rebuild_source));
    if (artifact.rebuild_hash_expected && artifact.rebuild_hash_expected !== computedRebuildHash) {
      errors.push("rebuild_hash_expected does not match computed rebuild hash");
    }
  } else if (artifact.rebuild_source !== undefined) {
    errors.push("rebuild_source must be an object when provided");
  } else {
    warnings.push("rebuild_source not present; rebuild determinism check skipped");
  }

  if (artifact.transition_chain !== undefined) {
    const transitionCheck = validateTransitionChain(artifact.transition_chain);
    if (!transitionCheck.ok) {
      errors.push(...transitionCheck.errors);
    }
  }

  return {
    command: "verify",
    status: errors.length === 0 ? "PASS" : "FAIL",
    errors,
    warnings,
    derived: {
      computed_rebuild_hash: computedRebuildHash
    }
  };
}

function rebuildArtifact(artifact) {
  if (!artifact || typeof artifact !== "object") {
    return {
      command: "rebuild",
      status: "FAIL",
      errors: ["artifact must be an object"]
    };
  }

  if (!artifact.rebuild_source || typeof artifact.rebuild_source !== "object") {
    return {
      command: "rebuild",
      status: "FAIL",
      errors: ["rebuild_source object is required"]
    };
  }

  const rebuiltHash = sha256Hex(stableStringify(artifact.rebuild_source));
  const expected = artifact.rebuild_hash_expected || null;
  const matchExpected = expected ? expected === rebuiltHash : null;

  return {
    command: "rebuild",
    status: matchExpected === false ? "FAIL" : "PASS",
    rebuilt_hash: rebuiltHash,
    expected_rebuild_hash: expected,
    match_expected: matchExpected
  };
}

function validateTransitionsArtifact(artifact) {
  if (!artifact || typeof artifact !== "object") {
    return {
      command: "validate",
      status: "FAIL",
      errors: ["artifact must be an object"]
    };
  }

  const result = validateTransitionChain(artifact.transition_chain);
  return {
    command: "validate",
    status: result.ok ? "PASS" : "FAIL",
    errors: result.errors
  };
}

function runConformanceSuite(suite, baseDir) {
  const rows = [];
  let failed = 0;

  for (const testCase of suite.cases || []) {
    const filePath = path.resolve(baseDir, testCase.file || "");
    const artifact = readJson(filePath);
    let actual;
    if (testCase.command === "verify") {
      actual = verifyArtifact(artifact);
    } else if (testCase.command === "rebuild") {
      actual = rebuildArtifact(artifact);
    } else if (testCase.command === "validate") {
      actual = validateTransitionsArtifact(artifact);
    } else {
      actual = {
        command: testCase.command,
        status: "FAIL",
        errors: [`unsupported command ${testCase.command}`]
      };
    }

    const expectedStatus = (testCase.expect && testCase.expect.status) || "PASS";
    let ok = actual.status === expectedStatus;
    if (ok && testCase.expect && testCase.expect.match_expected !== undefined) {
      ok = actual.match_expected === testCase.expect.match_expected;
    }

    if (!ok) failed += 1;
    rows.push({
      id: testCase.id || "UNKNOWN",
      command: testCase.command || "UNKNOWN",
      file: testCase.file || "",
      expected_status: expectedStatus,
      actual_status: actual.status,
      ok,
      detail: actual
    });
  }

  return {
    status: failed === 0 ? "PASS" : "FAIL",
    suite_id: suite.suite_id || "dlx-ref-conformance",
    total: rows.length,
    passed: rows.filter((row) => row.ok).length,
    failed,
    results: rows
  };
}

module.exports = {
  ARTIFACT_SCHEMA_VERSION,
  stableStringify,
  sha256Hex,
  readJson,
  verifyArtifact,
  rebuildArtifact,
  validateTransitionsArtifact,
  runConformanceSuite
};

