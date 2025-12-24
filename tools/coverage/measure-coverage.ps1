# Measure current test coverage and generate detailed report
# This script delegates to the unified Python coverage utility

$ErrorActionPreference = 'Stop'

# Use the unified Python coverage utility
python -m tools.coverage.runner measure
