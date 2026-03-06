#!/bin/bash
# Check test coverage and enforce quality gates

set -e

COVERAGE_THRESHOLD=${1:-70}
COVERAGE_FILE="coverage.xml"

echo "=========================================="
echo "CodeFlow Engine - Coverage Check"
echo "=========================================="
echo ""

# Check if coverage file exists
if [ ! -f "$COVERAGE_FILE" ]; then
    echo "⚠️  Coverage file not found. Running tests with coverage..."
    poetry run pytest --cov=codeflow_engine --cov-report=xml --cov-report=term
fi

# Get current coverage percentage
COVERAGE=$(poetry run coverage report | grep TOTAL | awk '{print $NF}' | sed 's/%//')

echo "Current coverage: ${COVERAGE}%"
echo "Target coverage: ${COVERAGE_THRESHOLD}%"
echo ""

# Check if coverage meets threshold
if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
    echo "❌ Coverage ${COVERAGE}% is below threshold of ${COVERAGE_THRESHOLD}%"
    echo ""
    echo "Coverage by module:"
    poetry run coverage report --show-missing | grep -E "codeflow_engine" | head -20
    exit 1
else
    echo "✅ Coverage ${COVERAGE}% meets threshold of ${COVERAGE_THRESHOLD}%"
    exit 0
fi

