"""Command-line interface for the markdown linter."""

import argparse
import sys

from tools.core.cli.base import BaseLinterCLI
from tools.markdown_lint.linter import MarkdownLinter


class MarkdownLinterCLI(BaseLinterCLI):
    """CLI for the markdown linter."""

    tool_name = "markdown-lint"
    tool_description = "Lint and fix markdown files."
    tool_version = "0.1.0"
    file_extensions = {".md", ".markdown"}

    def _add_linting_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add markdown-specific linting arguments."""
        lint_group = parser.add_argument_group("Linting Options")
        lint_group.add_argument(
            "--max-line-length",
            type=int,
            default=120,
            help="Maximum allowed line length",
        )
        lint_group.add_argument(
            "--no-blank-line-before-heading",
            action="store_false",
            dest="require_blank_line_before_heading",
            help="Don't require blank lines before headings",
        )
        lint_group.add_argument(
            "--no-blank-line-after-heading",
            action="store_false",
            dest="require_blank_line_after_heading",
            help="Don't require blank lines after headings",
        )
        lint_group.add_argument(
            "--allow-multiple-blank-lines",
            action="store_true",
            help="Allow multiple consecutive blank lines",
        )
        lint_group.add_argument(
            "--no-trim-trailing-whitespace",
            action="store_false",
            dest="trim_trailing_whitespace",
            help="Don't trim trailing whitespace",
        )
        lint_group.add_argument(
            "--no-check-blank-lines-around-headings",
            action="store_false",
            dest="check_blank_lines_around_headings",
            help="Disable MD022: Don't check for blank lines around headings",
        )
        lint_group.add_argument(
            "--no-check-blank-lines-around-lists",
            action="store_false",
            dest="check_blank_lines_around_lists",
            help="Disable MD032: Don't check for blank lines around lists",
        )
        lint_group.add_argument(
            "--no-check-ordered-list-numbering",
            action="store_false",
            dest="check_ordered_list_numbering",
            help="Disable MD029: Don't check ordered list item numbering",
        )
        lint_group.add_argument(
            "--no-check-fenced-code-blocks",
            action="store_false",
            dest="check_fenced_code_blocks",
            help="Disable MD031/MD040: Don't check fenced code blocks spacing and language",
        )
        lint_group.add_argument(
            "--no-check-duplicate-headings",
            action="store_false",
            dest="check_duplicate_headings",
            help="Disable MD024: Don't check for duplicate headings",
        )
        lint_group.add_argument(
            "--no-check-bare-urls",
            action="store_false",
            dest="check_bare_urls",
            help="Disable MD034: Don't check for bare URLs",
        )
        lint_group.add_argument(
            "--no-insert-final-newline",
            action="store_false",
            dest="insert_final_newline",
            help="Don't require a final newline at the end of files",
        )

    def create_linter(self, args: argparse.Namespace) -> MarkdownLinter:
        """Create a MarkdownLinter instance with the given configuration."""
        return MarkdownLinter(
            {
                "max_line_length": args.max_line_length,
                "require_blank_line_before_heading": args.require_blank_line_before_heading,
                "require_blank_line_after_heading": args.require_blank_line_after_heading,
                "allow_multiple_blank_lines": args.allow_multiple_blank_lines,
                "trim_trailing_whitespace": args.trim_trailing_whitespace,
                "insert_final_newline": args.insert_final_newline,
                "check_blank_lines_around_headings": args.check_blank_lines_around_headings,
                "check_blank_lines_around_lists": args.check_blank_lines_around_lists,
                "check_ordered_list_numbering": args.check_ordered_list_numbering,
                "check_fenced_code_blocks": args.check_fenced_code_blocks,
                "check_duplicate_headings": args.check_duplicate_headings,
                "check_bare_urls": args.check_bare_urls,
            }
        )


def main() -> int:
    """Main entry point for the CLI."""
    cli = MarkdownLinterCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
