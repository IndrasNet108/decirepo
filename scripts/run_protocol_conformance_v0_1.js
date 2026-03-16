#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const {
  readJson,
  stableStringify,
  sha256Hex,
  verifyArtifact,
  rebuildArtifact,
  validateTransitionsArtifact
} = require("../dlx-ref/lib/engine");

const ROOT = path.resolve(__dirname, "..");
const DEFAULT_PROFILE_DIR = path.join(ROOT, "conformance", "v0_1");
const REPORT_SCHEMA = "decirepo-conformance-report-v0.1";
const PACKAGE_JSON = readJson(path.join(ROOT, "package.json"));

const ERROR_CODE_MAP = [
  [/^schema_version must be dlx-artifact-v0\.1$/, "SCHEMA_VERSION_INVALID"],
  [/^artifact_hash must be 64-char hex$/, "ARTIFACT_HASH_INVALID"],
  [/^validator_result must be PASS or FAIL$/, "VALIDATOR_RESULT_INVALID"],
  [/^rebuild_result must be MATCH or MISMATCH$/, "REBUILD_RESULT_INVALID"],
  [/^PASS validator_result requires MATCH rebuild_result$/, "PASS_REQUIRES_MATCH"],
  [/^rebuild_hash_expected does not match computed rebuild hash$/, "REBUILD_HASH_EXPECTED_MISMATCH"],
  [/^rebuild_source must be an object when provided$/, "REBUILD_SOURCE_INVALID"],
  [/^rebuild_source object is required$/, "REBUILD_SOURCE_INVALID"],
  [/^transition_chain must be a non-empty array$/, "TRANSITION_CHAIN_INVALID"],
  [/^transition_chain\[/, "TRANSITION_CHAIN_INVALID"]
];

function parseArgs(argv) {
  const args = argv.slice(2);
  let profileDir = DEFAULT_PROFILE_DIR;
  let outFile = null;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--out") {
      outFile = args[i + 1];
      i += 1;
      continue;
    }
    profileDir = path.resolve(arg);
  }

  return { profileDir, outFile };
}

function normalizeErrorCodes(errors) {
  const codes = [];
  const unmapped = [];
  for (const message of errors || []) {
    const row = ERROR_CODE_MAP.find(([pattern]) => pattern.test(String(message)));
    if (!row) {
      unmapped.push(String(message));
      continue;
    }
    codes.push(row[1]);
  }
  return {
    reason_codes: codes.sort(),
    unmapped_errors: unmapped
  };
}

function runCommand(command, artifact) {
  if (command === "verify") return verifyArtifact(artifact);
  if (command === "rebuild") return rebuildArtifact(artifact);
  if (command === "validate") return validateTransitionsArtifact(artifact);
  throw new Error(`unsupported verification_command: ${command}`);
}

function resolveIdentitySurface(artifact, identitySurface) {
  if (identitySurface === "artifact.rebuild_source") {
    return artifact.rebuild_source;
  }
  throw new Error(`unsupported identity_surface: ${identitySurface}`);
}

function canonicalHex(value) {
  return Buffer.from(stableStringify(value), "utf8").toString("hex");
}

function buildNormalizedResult({ rawResult, artifactId, manifest }) {
  const { reason_codes, unmapped_errors } = normalizeErrorCodes(rawResult.errors || []);
  return {
    normalized: {
      status: rawResult.status,
      artifact_id: artifactId,
      reason_codes,
      protocol_version: manifest.protocol_semantics,
      verifier_result_schema: manifest.normalized_result_schema
    },
    unmapped_errors
  };
}

function failKeys(checks) {
  return Object.entries(checks)
    .filter(([, ok]) => !ok)
    .map(([key]) => key);
}

function main() {
  const { profileDir, outFile } = parseArgs(process.argv);
  const vectorDirs = fs
    .readdirSync(profileDir, { withFileTypes: true })
    .filter((row) => row.isDirectory() && row.name.startsWith("vector_"))
    .map((row) => row.name)
    .sort()
    .map((name) => path.join(profileDir, name));

  const results = [];

  for (const vectorDir of vectorDirs) {
    const vectorId = path.basename(vectorDir);
    const manifest = readJson(path.join(vectorDir, "vector_manifest.json"));
    const artifact = readJson(path.join(vectorDir, "artifact.json"));
    const expectedArtifactId = fs.readFileSync(path.join(vectorDir, "expected_artifact_id.txt"), "utf8").trim();
    const expectedCanonicalIdentityHex = fs.readFileSync(path.join(vectorDir, "canonical_bytes.hex"), "utf8").trim();
    const expectedResult = readJson(path.join(vectorDir, "expected_verification_result.json"));
    const expectedResultHex = fs
      .readFileSync(path.join(vectorDir, "expected_verification_result.canonical.hex"), "utf8")
      .trim();
    const command = manifest.verification_command || "verify";

    let reportRow;
    try {
      const identitySurface = resolveIdentitySurface(artifact, manifest.identity_surface);
      const actualCanonicalIdentityHex = canonicalHex(identitySurface);
      const actualArtifactId = sha256Hex(stableStringify(identitySurface));
      const vectorConsistency = {
        expected_identity_from_fixture_matches_file:
          sha256Hex(Buffer.from(expectedCanonicalIdentityHex, "hex").toString("utf8")) === expectedArtifactId,
        expected_result_json_matches_canonical_hex: canonicalHex(expectedResult) === expectedResultHex
      };

      const rawResult = runCommand(command, artifact);
      const { normalized, unmapped_errors } = buildNormalizedResult({
        rawResult,
        artifactId: actualArtifactId,
        manifest
      });
      const actualResultHex = canonicalHex(normalized);

      const checks = {
        vector_consistency_ok: Object.values(vectorConsistency).every(Boolean),
        canonical_identity_bytes_match: actualCanonicalIdentityHex === expectedCanonicalIdentityHex,
        artifact_id_match: actualArtifactId === expectedArtifactId,
        normalized_result_match: actualResultHex === expectedResultHex,
        unmapped_errors_empty: unmapped_errors.length === 0
      };

      const ok = Object.values(checks).every(Boolean);
      const identityCheck = checks.canonical_identity_bytes_match && checks.artifact_id_match;
      const verificationCheck =
        rawResult.status === expectedResult.status &&
        JSON.stringify(normalized.reason_codes) === JSON.stringify(expectedResult.reason_codes);
      const resultBytesCheck = checks.normalized_result_match;
      reportRow = {
        vector_id: vectorId,
        command,
        ok,
        verdict: ok ? "PASS" : "FAIL",
        reason: ok ? "matched_expected_outputs" : failKeys(checks).join(","),
        identity_check: identityCheck,
        verification_check: verificationCheck,
        result_bytes_check: resultBytesCheck,
        checks,
        failures: failKeys(checks),
        manifest,
        raw_result: rawResult,
        expected_normalized_result: expectedResult,
        actual_normalized_result: normalized,
        unmapped_errors
      };
    } catch (error) {
      reportRow = {
        vector_id: vectorId,
        command,
        ok: false,
        verdict: "CONFORMANCE_ERROR",
        reason: "runner_error",
        identity_check: false,
        verification_check: false,
        result_bytes_check: false,
        checks: {
          runner_ok: false
        },
        failures: ["runner_error"],
        error: String(error && error.message ? error.message : error)
      };
    }

    const mark = reportRow.ok ? "PASS" : "FAIL";
    process.stdout.write(`${mark} ${reportRow.vector_id} command=${reportRow.command}\n`);
    if (!reportRow.ok) {
      process.stdout.write(`  failures=${reportRow.failures.join(",")}\n`);
    }
    results.push(reportRow);
  }

  const failed = results.filter((row) => !row.ok).length;
  const hasConformanceError = results.some((row) => row.verdict === "CONFORMANCE_ERROR");
  const overallVerdict = hasConformanceError ? "CONFORMANCE_ERROR" : failed === 0 ? "PASS" : "FAIL";
  const report = {
    report_schema: REPORT_SCHEMA,
    implementation_name: PACKAGE_JSON.name,
    implementation_version: PACKAGE_JSON.version,
    conformance_profile: "V0_1",
    protocol_specification: "v0.2",
    protocol_semantics: "v0.1",
    vectors_total: results.length,
    vectors_passed: results.length - failed,
    vectors_failed: failed,
    overall_verdict: overallVerdict,
    status: overallVerdict,
    total: results.length,
    passed: results.length - failed,
    failed,
    results
  };

  if (outFile) {
    const absOut = path.resolve(outFile);
    fs.mkdirSync(path.dirname(absOut), { recursive: true });
    fs.writeFileSync(absOut, `${JSON.stringify(report, null, 2)}\n`);
  }

  process.stdout.write("\n");
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  process.exit(report.overall_verdict === "PASS" ? 0 : 1);
}

main();
