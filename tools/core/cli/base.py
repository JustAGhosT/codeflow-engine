"""Base CLI class for linting tools.

This module provides a base class with common CLI argument parsing
that can be extended by specific linting tools.
"""

import argparse
from abc import ABC, abstractmethod
from pathlib import Path
import sys
from typing import Any

from tools.core.cli.formatters import format_report_json, format_report_text
from tools.core.cli.severity import get_severity_threshold


class BaseLinterCLI(ABC):
    """Base class for linter CLI implementations.

    This class provides common argument parsing and output formatting
    that can be shared across different linting tools.
    """

    # Override these in subclasses
    tool_name: str = "linter"
    tool_description: str = "Lint files"
    tool_version: str = "0.1.0"
    file_extensions: set[str] = set()

    def __init__(self) -> None:
        """Initialize the CLI."""
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with common arguments."""
        parser = argparse.ArgumentParser(
            description=self.tool_description,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        # Positional arguments
        parser.add_argument(
            "paths",
            nargs="*",
            default=["."],
            help="Files or directories to check (default: current directory)",
        )

        # Add common argument groups
        self._add_output_arguments(parser)
        self._add_fix_arguments(parser)
        self._add_filter_arguments(parser)

        # Version
        parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {self.tool_version}",
        )

        # Add tool-specific arguments
        self._add_linting_arguments(parser)

        return parser

    def _add_output_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add output-related arguments."""
        output_group = parser.add_argument_group("Output Options")
        output_group.add_argument(
            "--format",
            choices=["text", "json"],
            default="text",
            help="Output format",
        )
        output_group.add_argument(
            "--no-color",
            action="store_true",
            help="Disable colored output",
        )
        output_group.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Increase verbosity (can be used multiple times)",
        )

    def _add_fix_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add fix-related arguments."""
        fix_group = parser.add_argument_group("Fixing Options")
        fix_group.add_argument(
            "--fix",
            action="store_true",
            help="Automatically fix fixable issues",
        )
        fix_group.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be fixed without making changes",
        )

    def _add_filter_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add filtering-related arguments."""
        filter_group = parser.add_argument_group("Filtering Options")
        filter_group.add_argument(
            "--exclude",
            action="append",
            default=[],
            help="Exclude files/directories that match the given glob patterns",
        )
        filter_group.add_argument(
            "--severity",
            choices=["error", "warning", "style"],
            default="warning",
            help="Minimum severity to report",
        )

    @abstractmethod
    def _add_linting_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add tool-specific linting arguments.

        Subclasses must implement this to add their specific options.
        """
        pass

    @abstractmethod
    def create_linter(self, args: argparse.Namespace) -> Any:
        """Create a linter instance with the given configuration.

        Subclasses must implement this to create their specific linter.
        """
        pass

    def parse_args(self, args: list[str] | None = None) -> argparse.Namespace:
        """Parse command line arguments."""
        return self.parser.parse_args(args)

    def process_paths(
        self, linter: Any, paths: list[str], exclude: list[str], verbose: int = 0
    ) -> None:
        """Process all specified paths with the linter.

        Args:
            linter: The linter instance
            paths: List of file/directory paths to process
            exclude: List of glob patterns to exclude
            verbose: Verbosity level
        """
        for path_str in paths:
            path = Path(path_str)

            if path.is_file():
                if not self.file_extensions or path.suffix in self.file_extensions:
                    linter.check_file(path)
                elif verbose > 0:
                    print(f"Skipping file with unsupported extension: {path}")
            elif path.is_dir():
                linter.check_directory(path, exclude=exclude)

    def format_output(
        self, reports: dict, args: argparse.Namespace
    ) -> str:
        """Format the linting output based on arguments."""
        min_severity = get_severity_threshold(args.severity)
        use_color = not args.no_color and sys.stdout.isatty()

        if args.format == "json":
            return format_report_json(reports, min_severity=min_severity)
        return format_report_text(
            reports,
            use_color=use_color,
            verbose=args.verbose,
            min_severity=min_severity,
        )

    def has_issues_at_severity(
        self, reports: dict, severity_name: str
    ) -> bool:
        """Check if any reports have issues at or above the given severity."""
        severity_threshold = get_severity_threshold(severity_name)
        return any(
            any(
                issue.severity.value <= severity_threshold.value
                for issue in report.issues
            )
            for report in reports.values()
        )

    def run(self, args: list[str] | None = None) -> int:
        """Run the linter CLI.

        Args:
            args: Command line arguments (defaults to sys.argv[1:])

        Returns:
            Exit code (0 for success, 1 for issues found)
        """
        try:
            parsed_args = self.parse_args(args)
            linter = self.create_linter(parsed_args)

            # Process paths
            self.process_paths(
                linter,
                parsed_args.paths,
                parsed_args.exclude,
                parsed_args.verbose,
            )

            # Apply fixes if requested
            if parsed_args.fix:
                if parsed_args.dry_run:
                    fixed_count = linter.fix_files(dry_run=True)
                    if parsed_args.verbose > 0:
                        if fixed_count == 0:
                            print("No fixable issues found (dry run)")
                        else:
                            print(f"Would fix {fixed_count} file(s) (dry run)")
                else:
                    fixed_count = linter.fix_files(dry_run=False)
                    if fixed_count > 0 and parsed_args.verbose > 0:
                        print(f"Applied fixes to {fixed_count} file(s)")

            # Format and print output
            output = self.format_output(linter.reports, parsed_args)
            if output.strip():
                print(output)

            # Return exit code based on issues found
            return 1 if self.has_issues_at_severity(linter.reports, parsed_args.severity) else 0

        except KeyboardInterrupt:
            return 130
        except Exception as e:
            if parsed_args.verbose > 0:
                import traceback
                traceback.print_exc()
            else:
                print(f"Error: {e}", file=sys.stderr)
            return 1
