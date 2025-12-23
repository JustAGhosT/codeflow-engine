"""Command-line interface for the YAML linter."""

import argparse
import sys

from tools.core.cli.base import BaseLinterCLI
from tools.yaml_lint.linter import YAMLLinter


class YAMLLinterCLI(BaseLinterCLI):
    """CLI for the YAML linter."""

    tool_name = "yaml-lint"
    tool_description = "Lint and fix YAML files."
    tool_version = "0.1.0"
    file_extensions = {".yml", ".yaml"}

    def _add_linting_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add YAML-specific linting arguments."""
        lint_group = parser.add_argument_group("Linting Options")
        lint_group.add_argument(
            "--max-line-length",
            type=int,
            default=120,
            help="Maximum allowed line length",
        )
        lint_group.add_argument(
            "--indent-size",
            type=int,
            default=2,
            help="Expected indentation size",
        )
        lint_group.add_argument(
            "--no-document-start",
            dest="enforce_document_start",
            action="store_false",
            default=True,
            help="Don't require document start marker (---)",
        )
        lint_group.add_argument(
            "--document-end",
            dest="enforce_document_end",
            action="store_true",
            default=False,
            help="Require document end marker (...)",
        )
        lint_group.add_argument(
            "--no-empty-values",
            dest="check_empty_values",
            action="store_false",
            default=True,
            help="Don't check for empty values",
        )
        lint_group.add_argument(
            "--no-truthy",
            dest="check_truthy",
            action="store_false",
            default=True,
            help="Don't check for problematic truthy values",
        )

    def create_linter(self, args: argparse.Namespace) -> YAMLLinter:
        """Create a YAMLLinter instance with the given configuration."""
        # Merge provided args with defaults to ensure all config keys are present
        config = {
            **YAMLLinter.DEFAULT_CONFIG,
            "max_line_length": args.max_line_length,
            "indent_size": args.indent_size,
            "enforce_document_start": args.enforce_document_start,
            "enforce_document_end": args.enforce_document_end,
            "check_empty_values": args.check_empty_values,
            "check_truthy": args.check_truthy,
        }
        return YAMLLinter(config)


def main(args: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    cli = YAMLLinterCLI()
    return cli.run(args)


if __name__ == "__main__":
    sys.exit(main())
