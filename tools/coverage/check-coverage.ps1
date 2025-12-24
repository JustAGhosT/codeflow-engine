# Check test coverage and enforce quality gates
# This script delegates to the unified Python coverage utility

param(
    [int]$CoverageThreshold = 70
)

$ErrorActionPreference = 'Stop'

# Use the unified Python coverage utility
python -m tools.coverage.runner check --threshold $CoverageThreshold
