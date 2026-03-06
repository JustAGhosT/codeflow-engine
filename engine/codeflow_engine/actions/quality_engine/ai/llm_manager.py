"""
LLM Manager for Quality Engine

Manages LLM interactions for quality analysis.
"""

import asyncio
import logging
import os
from typing import Any

from codeflow_engine.ai.core.base import LLMMessage
from codeflow_engine.ai.core.providers.manager import LLMProviderManager
from codeflow_engine.config import CodeFlowConfig

logger = logging.getLogger(__name__)


async def initialize_llm_manager() -> LLMProviderManager | None:
    """
    Initialize the LLM provider manager for AI-enhanced quality analysis.

    Returns:
        LLMProviderManager: Configured LLM manager or None if initialization fails
    """
    try:
        # Basic configuration for quality analysis
        config = {
            "providers": {
                "openai": {
                    "api_key": os.getenv("OPENAI_API_KEY", ""),
                    "default_model": "gpt-4",
                    "max_tokens": 4000,
                    "temperature": 0.1,
                },
                "anthropic": {
                    "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
                    "default_model": "claude-3-sonnet-20240229",
                    "max_tokens": 4000,
                    "temperature": 0.1,
                },
            },
            "fallback_order": ["openai", "anthropic"],
            "default_provider": "openai",
        }

        llm_manager = LLMProviderManager(CodeFlowConfig())

        # Guard optional initialize() call
        if hasattr(llm_manager, "initialize"):
            await llm_manager.initialize()

        # Test the connection
        test_messages = [
            LLMMessage(role="system", content="You are a helpful assistant."),
            LLMMessage(role="user", content="Test message"),
        ]
        test_response = await llm_manager.complete(
            test_messages,
            provider="openai",
            model="gpt-4",
            temperature=0.1,
        )

        if test_response and test_response.content:
            logger.info("LLM manager initialized successfully")
            return llm_manager
        else:
            logger.warning("LLM manager test failed - no response received")
            return None

    except Exception as e:
        logger.exception(f"Failed to initialize LLM manager: {e}")
        return None


def get_llm_config_for_quality_analysis() -> dict[str, Any]:
    """
    Get configuration for LLM-based quality analysis.

    Returns:
        dict: Configuration for quality analysis LLM usage
    """
    return {
        "max_tokens": 4000,
        "temperature": 0.1,
        "system_prompt": """You are CodeQualityGPT, an expert code review assistant specialized in identifying improvements,
optimizations, and potential issues in code. Your task is to analyze code snippets and provide detailed,
actionable feedback that goes beyond what static analysis tools can find.

Focus on the following aspects:
1. Architecture and design patterns
2. Performance optimization opportunities
3. Security vulnerabilities or risks
4. Maintainability and readability concerns
5. Edge case handling and robustness
6. Business logic flaws or inconsistencies
7. API design and usability

Provide your feedback in a structured JSON format with:
- Specific issues identified
- Why they matter
- How to fix them
- A confidence score (0-1) for each suggestion""",
        "preferred_providers": ["openai", "anthropic"],
        "fallback_providers": ["groq", "mistral"],
    }
