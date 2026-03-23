param(
  [string]$ProfileDir = "",
  [string]$OutFile = ""
)

$RootDir = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($ProfileDir)) {
  $ProfileDir = Join-Path $RootDir 'conformance/v0_1'
}
if ([string]::IsNullOrWhiteSpace($OutFile)) {
  $OutFile = Join-Path $RootDir 'out/conformance/v0_1/CONFORMANCE_REPORT.json'
}

$OutDir = Split-Path -Parent $OutFile
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
node (Join-Path $RootDir 'scripts/run_protocol_conformance_v0_1.js') $ProfileDir --out $OutFile
Write-Host "Wrote conformance report: $OutFile"
