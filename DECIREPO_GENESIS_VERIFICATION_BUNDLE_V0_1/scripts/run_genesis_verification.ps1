param(
  [ValidateSet('verify','rebuild','validate','all')]
  [string]$Mode = 'all'
)

$RootDir = Split-Path -Parent $PSScriptRoot
$Cli = Join-Path $RootDir 'dlx-ref/cli.js'
$Artifact = Join-Path $RootDir 'genesis_artifact.json'

function Run-Verify {
  node $Cli verify $Artifact
}

function Run-Rebuild {
  node $Cli rebuild $Artifact
}

function Run-Validate {
  node $Cli validate $Artifact
}

switch ($Mode) {
  'verify' { Run-Verify }
  'rebuild' { Run-Rebuild }
  'validate' { Run-Validate }
  'all' {
    Write-Host '# verify'
    Run-Verify
    Write-Host ''
    Write-Host '# rebuild'
    Run-Rebuild
    Write-Host ''
    Write-Host '# validate'
    Run-Validate
  }
}
