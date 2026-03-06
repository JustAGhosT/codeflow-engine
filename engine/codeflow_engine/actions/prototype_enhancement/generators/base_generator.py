"""
Base Generator Module

Provides the BaseGenerator class that all specialized generators inherit from.
"""

from abc import ABC, abstractmethod
from dataclasses import asdict
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

from codeflow_engine.actions.prototype_enhancement.platform_configs import (
    PlatformConfig,
)


if TYPE_CHECKING:
    from codeflow_engine.actions.prototype_enhancement.generators.template_utils import (
        TemplateManager,
    )

T = TypeVar("T")


class BaseGenerator(ABC):
    """Base class for all file generators.

    Provides common functionality and interface for generating files.
    """

    def __init__(
        self,
        template_manager: "TemplateManager",
        platform_config: PlatformConfig | None = None,
    ):
        """Initialize the base generator.

        Args:
            template_manager: The template manager instance to use for rendering templates
            platform_config: Optional platform configuration
        """
        self.template_manager = template_manager
        self.platform_config = platform_config

    @abstractmethod
    def generate(self, output_dir: str, **kwargs) -> list[str]:
        """Generate files in the specified output directory.

        Args:
            output_dir: The directory to generate files in
            **kwargs: Additional arguments specific to the generator

        Returns:
            List of paths to generated files
        """

    def _write_file(self, file_path: str, content: str) -> None:
        """Write content to a file, creating parent directories if needed.

        Args:
            file_path: Path to the file to write
            content: Content to write to the file
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _render_template(
        self,
        template_key: str,
        variables: dict[str, Any] | None = None,
        variants: list[str] | None = None,
    ) -> str | None:
        """Render a template using the template manager.

        Args:
            template_key: Key identifying the template
            variables: Variables to pass to the template
            variants: List of template variants to apply
        Returns:
            Rendered template content, or None if template not found
        """
        return self.template_manager.render(template_key, variables, variants)

    def _template_exists(self, template_key: str) -> bool:
        """Check whether a template key exists in the registry."""
        registry = getattr(self.template_manager, "template_registry", None)
        if registry is None:
            return False
        get_metadata = getattr(registry, "get_metadata", None)
        if callable(get_metadata):
            return get_metadata(template_key) is not None
        return False

    def _read_json_file(self, file_path: str) -> dict[str, Any] | None:
        """Read a JSON file into a dictionary."""
        path = Path(file_path)
        if not path.exists():
            return None
        try:
            with path.open(encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return None
        return data if isinstance(data, dict) else None

    def _write_json_file(self, file_path: str, data: dict[str, Any]) -> None:
        """Write a dictionary to a JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def _get_platform_variables(self) -> dict[str, Any]:
        """Get platform-specific variables for template rendering.

        Returns:
            Dictionary of platform variables
        """
        if not self.platform_config:
            return {}

        return {
            "platform": self.platform_config.name,
            "platform_config": asdict(self.platform_config),
            "platform_vars": {},
        }
