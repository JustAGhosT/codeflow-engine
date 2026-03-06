"""
Deployment Generator Module

Handles generation of deployment-related configuration files and scripts
for different platforms and deployment targets.
"""

import logging
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

from codeflow_engine.actions.prototype_enhancement.generators.base_generator import BaseGenerator

if TYPE_CHECKING:
    from codeflow_engine.actions.prototype_enhancement.generators.template_utils import (
        TemplateManager,
    )


logger = logging.getLogger(__name__)


class DeploymentGenerator(BaseGenerator):
    """
    Generates deployment configuration files for various platforms.
    """

    def __init__(
        self,
        template_manager: "TemplateManager",
        **kwargs: Any,
    ) -> None:
        """
        Initialize the deployment generator.

        Args:
            template_manager: Template manager used for rendering deployment templates
        """
        super().__init__(template_manager, kwargs.get("platform_config"))
        self.template_name = "deployment"

    def generate(self, output_dir: str, **kwargs: Any) -> list[str]:
        """
        Generate deployment configuration files.

        Args:
            output_dir: Directory to write generated files to
            **kwargs: Additional generation options including platform and context

        Returns:
            List of generated file paths
        """
        platform = str(kwargs.get("platform", ""))
        context = dict(kwargs.get("context") or {})
        output_path = Path(output_dir)

        # Add platform-specific context
        context["platform"] = platform

        # Generate platform-specific deployment files
        if platform == "replit":
            return self._generate_replit_deployment(output_path, context)
        if platform == "vercel":
            return self._generate_vercel_deployment(output_path, context)
        if platform == "render":
            return self._generate_render_deployment(output_path, context)
        logger.warning(f"Unsupported deployment platform: {platform}")
        return []

    def _generate_replit_deployment(
        self, output_dir: Path, context: dict[str, Any]
    ) -> list[str]:
        """Generate Replit-specific deployment files."""
        generated_files: list[str] = []

        # Generate .replit file
        replit_config = self._render_template("replit_config.toml", context)
        if replit_config:
            replit_path = output_dir / ".replit"
            replit_path.write_text(replit_config, encoding="utf-8")
            generated_files.append(str(replit_path))

        # Generate replit.nix if needed
        if context.get("needs_custom_environment"):
            replit_nix = self._render_template("replit.nix", context)
            if replit_nix:
                nix_path = output_dir / "replit.nix"
                nix_path.write_text(replit_nix, encoding="utf-8")
                generated_files.append(str(nix_path))

        return generated_files

    def _generate_vercel_deployment(
        self, output_dir: Path, context: dict[str, Any]
    ) -> list[str]:
        """Generate Vercel deployment configuration."""
        generated_files: list[str] = []

        # Generate vercel.json
        vercel_config = self._render_template("vercel.json", context)
        if vercel_config:
            vercel_path = output_dir / "vercel.json"
            vercel_path.write_text(vercel_config, encoding="utf-8")
            generated_files.append(str(vercel_path))

        return generated_files

    def _generate_render_deployment(
        self, output_dir: Path, context: dict[str, Any]
    ) -> list[str]:
        """Generate Render deployment configuration."""
        generated_files: list[str] = []

        # Generate render.yaml
        render_config = self._render_template("render.yaml", context)
        if render_config:
            render_path = output_dir / "render.yaml"
            render_path.write_text(render_config, encoding="utf-8")
            generated_files.append(str(render_path))

        return generated_files
