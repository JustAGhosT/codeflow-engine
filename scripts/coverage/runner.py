"""Unified coverage runner for test quality gates.

This module provides a cross-platform Python implementation for running
test coverage, replacing the duplicated bash and PowerShell scripts.
"""

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CoverageResult:
    """Result of a coverage run."""

    total_coverage: float
    by_module: dict[str, float]
    low_coverage_files: list[tuple[str, float]]
    no_coverage_files: list[str]
    success: bool
    error_message: str = ""


class CoverageRunner:
    """Unified coverage runner for running tests and generating reports."""

    def __init__(
        self,
        module_name: str = "codeflow_engine",
        threshold: float = 70.0,
        low_coverage_threshold: float = 50.0,
    ):
        """Initialize the coverage runner.

        Args:
            module_name: The Python module to measure coverage for
            threshold: Minimum coverage percentage required to pass
            low_coverage_threshold: Threshold below which files are flagged
        """
        self.module_name = module_name
        self.threshold = threshold
        self.low_coverage_threshold = low_coverage_threshold

    def run_tests(self, generate_html: bool = True, generate_xml: bool = True) -> bool:
        """Run pytest with coverage.

        Args:
            generate_html: Whether to generate HTML report
            generate_xml: Whether to generate XML report

        Returns:
            True if tests passed, False otherwise
        """
        cmd = [
            "poetry", "run", "pytest",
            f"--cov={self.module_name}",
            "--cov-report=term",
        ]

        if generate_html:
            cmd.append("--cov-report=html")
        if generate_xml:
            cmd.append("--cov-report=xml")

        result = subprocess.run(cmd, capture_output=False)
        return result.returncode == 0

    def get_coverage_report(self) -> str:
        """Get the coverage report output."""
        result = subprocess.run(
            ["poetry", "run", "coverage", "report"],
            capture_output=True,
            text=True,
        )
        return result.stdout

    def get_coverage_report_with_missing(self) -> str:
        """Get the coverage report with missing lines."""
        result = subprocess.run(
            ["poetry", "run", "coverage", "report", "--show-missing"],
            capture_output=True,
            text=True,
        )
        return result.stdout

    def parse_coverage(self, report: str) -> CoverageResult:
        """Parse coverage report and extract metrics.

        Args:
            report: The coverage report output

        Returns:
            CoverageResult with parsed metrics
        """
        total_coverage = 0.0
        by_module: dict[str, float] = {}
        low_coverage_files: list[tuple[str, float]] = []
        no_coverage_files: list[str] = []

        lines = report.strip().split("\n")

        for line in lines:
            # Parse TOTAL line
            if line.startswith("TOTAL"):
                match = re.search(r"(\d+(?:\.\d+)?)%", line)
                if match:
                    total_coverage = float(match.group(1))
                continue

            # Parse module lines
            if self.module_name in line:
                parts = line.split()
                if len(parts) >= 4:
                    file_path = parts[0]
                    # Extract coverage percentage
                    match = re.search(r"(\d+(?:\.\d+)?)%", line)
                    if match:
                        coverage = float(match.group(1))
                        by_module[file_path] = coverage

                        if coverage == 0:
                            no_coverage_files.append(file_path)
                        elif coverage < self.low_coverage_threshold:
                            low_coverage_files.append((file_path, coverage))

        return CoverageResult(
            total_coverage=total_coverage,
            by_module=by_module,
            low_coverage_files=sorted(low_coverage_files, key=lambda x: x[1]),
            no_coverage_files=no_coverage_files,
            success=total_coverage >= self.threshold,
        )

    def print_header(self, title: str) -> None:
        """Print a formatted header."""
        print("=" * 42)
        print(f"CodeFlow Engine - {title}")
        print("=" * 42)
        print()

    def print_section(self, title: str) -> None:
        """Print a formatted section header."""
        print(title)
        print("-" * 40)

    def check_coverage(self) -> int:
        """Check if coverage meets the threshold.

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        self.print_header("Coverage Check")

        # Check if coverage file exists
        if not Path("coverage.xml").exists():
            print("Coverage file not found. Running tests with coverage...")
            if not self.run_tests():
                print("Tests failed!")
                return 1
            print()

        report = self.get_coverage_report()
        result = self.parse_coverage(report)

        print(f"Current coverage: {result.total_coverage}%")
        print(f"Target coverage: {self.threshold}%")
        print()

        if result.success:
            print(f"Coverage {result.total_coverage}% meets threshold of {self.threshold}%")
            return 0
        else:
            print(f"Coverage {result.total_coverage}% is below threshold of {self.threshold}%")
            print()
            self.print_section("Coverage by module:")
            report_with_missing = self.get_coverage_report_with_missing()
            for line in report_with_missing.split("\n"):
                if self.module_name in line:
                    print(line)
            return 1

    def measure_coverage(self) -> int:
        """Measure coverage and generate detailed report.

        Returns:
            Exit code (always 0)
        """
        self.print_header("Coverage Measurement")

        print("Running tests with coverage...")
        self.run_tests(generate_html=True, generate_xml=True)
        print()

        self.print_header("Coverage Summary")

        report = self.get_coverage_report()
        result = self.parse_coverage(report)

        print(f"Overall Coverage: {result.total_coverage}%")
        print()

        self.print_section("Coverage by Module (sorted by coverage %):")
        report_with_missing = self.get_coverage_report_with_missing()
        module_lines = [
            line for line in report_with_missing.split("\n")
            if self.module_name in line
        ]
        for line in sorted(module_lines, key=lambda x: self._extract_coverage(x)):
            print(line)
        print()

        self.print_section(f"Files with Coverage < {self.low_coverage_threshold}%:")
        if result.low_coverage_files:
            for file_path, coverage in result.low_coverage_files:
                print(f"  {file_path}: {coverage}%")
        else:
            print("None")
        print()

        self.print_section("Files with No Coverage:")
        if result.no_coverage_files:
            for file_path in result.no_coverage_files:
                print(f"  {file_path}")
        else:
            print("None")
        print()

        self.print_header("Detailed Report")
        print("HTML report generated: htmlcov/index.html")
        print("XML report generated: coverage.xml")
        print()
        print("Open HTML report:")
        print("  - macOS/Linux: open htmlcov/index.html")
        print("  - Windows: start htmlcov/index.html")
        print()

        return 0

    def _extract_coverage(self, line: str) -> float:
        """Extract coverage percentage from a report line."""
        match = re.search(r"(\d+(?:\.\d+)?)%", line)
        return float(match.group(1)) if match else 0.0


def main() -> int:
    """Main entry point for the coverage CLI."""
    parser = argparse.ArgumentParser(
        description="Unified coverage tool for test quality gates"
    )

    parser.add_argument(
        "command",
        choices=["check", "measure"],
        help="Command to run: 'check' validates threshold, 'measure' generates full report",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=70.0,
        help="Coverage threshold percentage (default: 70)",
    )
    parser.add_argument(
        "--module",
        type=str,
        default="codeflow_engine",
        help="Module name to measure coverage for (default: codeflow_engine)",
    )
    parser.add_argument(
        "--low-threshold",
        type=float,
        default=50.0,
        help="Threshold for flagging low coverage files (default: 50)",
    )

    args = parser.parse_args()

    runner = CoverageRunner(
        module_name=args.module,
        threshold=args.threshold,
        low_coverage_threshold=args.low_threshold,
    )

    if args.command == "check":
        return runner.check_coverage()
    elif args.command == "measure":
        return runner.measure_coverage()

    return 1


if __name__ == "__main__":
    sys.exit(main())
