#!/bin/bash
# Check test coverage and enforce quality gates
# This script delegates to the unified Python coverage utility

set -e

COVERAGE_THRESHOLD=${1:-70}

# Use the unified Python coverage utility
python -m tools.coverage.runner check --threshold "$COVERAGE_THRESHOLD"
