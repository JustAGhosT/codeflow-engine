"""
Example usage of the Quality Engine with dependency injection.
"""

import asyncio

from codeflow_engine.actions.quality_engine.engine import create_quality_engine
from codeflow_engine.actions.quality_engine.models import QualityInputs, QualityMode


async def run_quality_analysis(files: list[str]) -> None:
    """
    Run quality analysis on files.

    Args:
        files: List of files to analyze
    """
    # Create an engine instance with DI
    engine = create_quality_engine()

    # Run a focused MyPy-oriented pass
    mypy_result = await engine.run(
        QualityInputs(
            mode=QualityMode.FAST,
            files=files,
            volume=500,
        )
    )

    # Run ESLint tool for JavaScript files
    js_files = [f for f in files if f.endswith((".js", ".jsx", ".ts", ".tsx"))]
    if js_files:
        eslint_result = await engine.run(
            QualityInputs(
                mode=QualityMode.FAST,
                files=js_files,
                volume=500,
            )
        )
    else:
        eslint_result = None

    # Run a broader linting pass
    all_results = await engine.run(
        QualityInputs(
            mode=QualityMode.SMART,
            files=files,
            volume=500,
        )
    )

    # Summarize results
    _ = mypy_result, eslint_result, all_results


if __name__ == "__main__":
    # Example files
    python_files = [
        "codeflow/actions/quality_engine/engine.py",
        "codeflow/actions/quality_engine/handler_registry.py",
    ]

    # Run analysis
    asyncio.run(run_quality_analysis(python_files))
