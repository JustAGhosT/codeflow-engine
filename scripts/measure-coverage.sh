#!/bin/bash
# Measure current test coverage and generate detailed report

set -e

echo "=========================================="
echo "CodeFlow Engine - Coverage Measurement"
echo "=========================================="
echo ""

# Run tests with coverage
echo "Running tests with coverage..."
poetry run pytest --cov=codeflow_engine --cov-report=html --cov-report=term --cov-report=xml

echo ""
echo "=========================================="
echo "Coverage Summary"
echo "=========================================="
echo ""

# Get overall coverage
COVERAGE=$(poetry run coverage report | grep TOTAL | awk '{print $NF}')
echo "Overall Coverage: ${COVERAGE}"
echo ""

# Show coverage by module
echo "Coverage by Module (sorted by coverage %):"
echo "----------------------------------------"
poetry run coverage report --show-missing | grep -E "codeflow_engine" | sort -k4 -n
echo ""

# Show files with low coverage
echo "Files with Coverage < 50%:"
echo "----------------------------------------"
poetry run coverage report | grep -E "codeflow_engine.*[0-9]+.*[0-9]+.*[0-9]+%" | awk '$NF < 50 {print}' || echo "None"
echo ""

# Show files with no coverage
echo "Files with No Coverage:"
echo "----------------------------------------"
poetry run coverage report --show-missing | grep -E "codeflow_engine.*0.*0.*0%" || echo "None"
echo ""

echo "=========================================="
echo "Detailed Report"
echo "=========================================="
echo "HTML report generated: htmlcov/index.html"
echo "XML report generated: coverage.xml"
echo ""
echo "Open HTML report: open htmlcov/index.html"
echo ""

