#!/usr/bin/env node
"use strict";

/**
 * DeciRepo Registry Sanity Check
 * Lead Architect & Creator: Oleg Surkov
 */

const fs = require('fs');
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const DATA_JS = path.join(ROOT, "assets", "data.js");
const FEED_JSON = path.join(ROOT, "api", "feed.json");
const DISCOVERY = path.join(ROOT, ".well-known", "decirepo-node");
const DISCOVERY_JSON = path.join(ROOT, ".well-known", "decirepo-node.json");
const NODE_MANIFEST = path.join(ROOT, "api", "network", "decirepo-node.json");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function loadDeciRepoData() {
  const src = fs.readFileSync(DATA_JS, "utf8");
  const sandbox = { window: {}, console };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox);
  return sandbox.window.DeciRepoData;
}

function isHex64(value) {
  return /^[0-9a-f]{64}$/i.test(String(value || ""));
}

function fail(message) {
  process.stderr.write(`FAIL ${message}\n`);
  process.exitCode = 1;
}

function pass(message) {
  process.stdout.write(`PASS ${message}\n`);
}

function main() {
  const data = loadDeciRepoData();
  const decisions = data.decisions || [];
  const feed = readJson(FEED_JSON);
  const discovery = readJson(DISCOVERY);
  const discoveryJson = readJson(DISCOVERY_JSON);
  const manifest = readJson(NODE_MANIFEST);

  if (!decisions.length) {
    fail("no decisions found");
    return;
  }
  pass(`decisions_count=${decisions.length}`);

  const ids = new Set();
  const canonicalIds = new Set();
  for (const d of decisions) {
    if (ids.has(d.id)) fail(`duplicate decision id: ${d.id}`);
    ids.add(d.id);
    if (canonicalIds.has(d.canonical_id)) fail(`duplicate canonical_id: ${d.canonical_id}`);
    canonicalIds.add(d.canonical_id);
    if (!isHex64(d.artifact && d.artifact.artifact_hash)) {
      fail(`invalid artifact hash for ${d.id}`);
    }
    if ((d.artifact && d.artifact.validator_result) !== "PASS") {
      fail(`validator_result not PASS for ${d.id}`);
    }
    if ((d.artifact && d.artifact.rebuild_status) !== "MATCH") {
      fail(`rebuild_status not MATCH for ${d.id}`);
    }
    if (!d.publisher) {
      fail(`publisher missing for ${d.id}`);
    }
  }
  pass("decision identity + artifact integrity checks");

  const governanceIds = [
    "DR-PROTOCOL-0001",
    "DR-TRUST-0001",
    "DR-CONF-0001",
    "DR-REFNODE-0001",
    "DR-GOV-0001"
  ];
  for (const id of governanceIds) {
    const row = decisions.find((d) => d.id === id);
    if (!row) {
      fail(`missing governance seed ${id}`);
      continue;
    }
    if (row.publisher !== "indrasnet-governance") {
      fail(`governance seed publisher mismatch for ${id}`);
    }
    if (!/^RFC-\d{4}$/.test(String(row.rfc_ref || ""))) {
      fail(`invalid rfc_ref for ${id}`);
    }
  }
  pass("governance seed checks");

  const feedItems = Array.isArray(feed.items) ? feed.items : [];
  for (const id of governanceIds) {
    const row = feedItems.find((x) => x.legacy_id === id);
    if (!row) {
      fail(`feed missing governance seed ${id}`);
      continue;
    }
    if (row.publisher_id !== "indrasnet-governance") {
      fail(`feed publisher_id mismatch for ${id}`);
    }
    if (!/^RFC-\d{4}$/.test(String(row.rfc_ref || ""))) {
      fail(`feed rfc_ref invalid for ${id}`);
    }
  }
  pass("feed governance coverage");

  const requiredDiscoveryFields = [
    "registry_id",
    "protocol_version",
    "manifest_url",
    "verify_endpoint",
    "trust_endpoint",
    "conformance_report_endpoint",
    "protocol_endpoint",
    "conformance_profile"
  ];
  for (const field of requiredDiscoveryFields) {
    if (!Object.prototype.hasOwnProperty.call(discovery, field)) {
      fail(`discovery missing field ${field}`);
    }
    if (!Object.prototype.hasOwnProperty.call(discoveryJson, field)) {
      fail(`discovery.json missing field ${field}`);
    }
  }
  pass("discovery schema checks");

  if (discovery.registry_id !== manifest.registry_id) {
    fail("discovery registry_id mismatch with node manifest");
  }
  if (discovery.manifest_url !== "/api/network/decirepo-node.json") {
    fail("discovery manifest_url mismatch");
  }
  if (discovery.conformance_report_endpoint !== manifest.conformance_report_endpoint) {
    fail("discovery conformance_report_endpoint mismatch with node manifest");
  }
  if (manifest.conformance_profile !== "decirepo-protocol-v0_1-mandatory") {
    fail("node manifest conformance_profile mismatch");
  }
  if ((manifest.compatibility_badge || {}).status !== "active") {
    fail("node manifest compatibility_badge.status must be active");
  }
  pass("manifest/discovery consistency");

  if (process.exitCode && process.exitCode !== 0) {
    process.stderr.write("\nRegistry sanity FAILED\n");
    process.exit(process.exitCode);
  }
  process.stdout.write("\nRegistry sanity PASSED\n");
}

main();
