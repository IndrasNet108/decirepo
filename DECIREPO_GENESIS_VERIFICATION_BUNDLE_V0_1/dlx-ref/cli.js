#!/usr/bin/env node
"use strict";

const path = require("path");
const {
  readJson,
  verifyArtifact,
  rebuildArtifact,
  validateTransitionsArtifact,
  runConformanceSuite
} = require("./lib/engine");

function usage() {
  console.error(
    [
      "Usage:",
      "  dlx-ref verify <artifact.json>",
      "  dlx-ref rebuild <artifact.json>",
      "  dlx-ref validate <artifact.json>",
      "  dlx-ref conformance <suite.json | suite_dir>",
      "",
      "Examples:",
      "  node dlx-ref/cli.js verify dlx-ref/test-vectors/artifacts/valid_governance_artifact.json",
      "  node dlx-ref/cli.js conformance dlx-ref/tests/conformance_v0_1.json"
    ].join("\n")
  );
}

function printJson(obj) {
  process.stdout.write(`${JSON.stringify(obj, null, 2)}\n`);
}

function resolveSuitePath(inputPath) {
  const abs = path.resolve(inputPath);
  if (abs.endsWith(".json")) return abs;
  return path.join(abs, "conformance_v0_1.json");
}

function main() {
  const [command, inputPath] = process.argv.slice(2);
  if (!command || !inputPath) {
    usage();
    process.exit(1);
  }

  try {
    if (command === "verify") {
      const artifact = readJson(inputPath);
      const result = verifyArtifact(artifact);
      printJson(result);
      process.exit(result.status === "PASS" ? 0 : 1);
    }

    if (command === "rebuild") {
      const artifact = readJson(inputPath);
      const result = rebuildArtifact(artifact);
      printJson(result);
      process.exit(result.status === "PASS" ? 0 : 1);
    }

    if (command === "validate") {
      const artifact = readJson(inputPath);
      const result = validateTransitionsArtifact(artifact);
      printJson(result);
      process.exit(result.status === "PASS" ? 0 : 1);
    }

    if (command === "conformance") {
      const suitePath = resolveSuitePath(inputPath);
      const suite = readJson(suitePath);
      const result = runConformanceSuite(suite, path.dirname(suitePath));
      for (const row of result.results) {
        const mark = row.ok ? "PASS" : "FAIL";
        process.stdout.write(
          `${mark} ${row.id} ${row.command} file=${row.file} expected=${row.expected_status} actual=${row.actual_status}\n`
        );
      }
      process.stdout.write("\n");
      printJson({
        status: result.status,
        suite_id: result.suite_id,
        total: result.total,
        passed: result.passed,
        failed: result.failed
      });
      process.exit(result.status === "PASS" ? 0 : 1);
    }

    usage();
    process.exit(1);
  } catch (error) {
    printJson({
      status: "FAIL",
      command,
      error: String(error && error.message ? error.message : error)
    });
    process.exit(1);
  }
}

main();

