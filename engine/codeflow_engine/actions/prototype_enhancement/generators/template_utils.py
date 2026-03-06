"""
Template Utilities Module

Provides template management and rendering functionality.
"""

from pathlib import Path
from typing import Any

import jinja2

from codeflow_engine.actions.prototype_enhancement.template_metadata import (
    TemplateMetadata,
    TemplateRegistry,
)


class TemplateManager:
    """Manages template loading and rendering with support for variants and inheritance."""

    def __init__(self, templates_dir: str):
        """Initialize the template manager.

        Args:
            templates_dir: Directory containing template files
        """
        self.templates_dir = Path(templates_dir)
        self.jinja_env = self._create_jinja_environment()
        self.template_registry = TemplateRegistry(templates_dir)

    def _create_jinja_environment(self) -> jinja2.Environment:
        """Create and configure a Jinja2 environment.

        Returns:
            Configured Jinja2 environment
        """
        # Create a custom loader that can handle our template structure
        loader = jinja2.FileSystemLoader(
            searchpath=str(self.templates_dir), encoding="utf-8", followlinks=True
        )

        return jinja2.Environment(
            loader=loader,
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        # Add custom filters and globals here if needed
        # env.filters['custom_filter'] = custom_filter_function

    def render(
        self,
        template_key: str,
        variables: dict[str, Any] | None = None,
        variants: list[str] | None = None,
    ) -> str | None:
        """Render a template with the given variables and variants.

        Args:
            template_key: Key identifying the template (e.g., 'docker/Dockerfile')
            variables: Variables to pass to the template
            variants: List of variants to apply
        Returns:
            Rendered template content, or None if template not found
        """
        rendered = self.template_registry.generate_template(
            template_key,
            variables=variables,
            variants=variants,
        )
        if rendered is None:
            return None

        metadata = self.template_registry.get_metadata(template_key)
        if metadata is None:
            return rendered

        template_path = metadata.template_file_path
        if template_path.suffix == ".j2":
            template = self.jinja_env.from_string(rendered)
            return template.render(**(variables or {}))

        return rendered

    def _apply_variants(
        self, template_meta: TemplateMetadata, variants: list[str]
    ) -> TemplateMetadata:
        """Apply variants to a template metadata.

        Args:
            template_meta: Original template metadata
            variants: List of variant names to apply

        Returns:
            New template metadata with variants applied
        """
        _ = variants
        return template_meta
