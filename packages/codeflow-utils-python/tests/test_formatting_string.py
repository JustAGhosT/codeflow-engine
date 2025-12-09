"""Tests for string formatting utilities."""

import pytest

from codeflow_utils.formatting.string import (
    truncate_string,
    slugify,
    camel_to_snake,
    snake_to_camel,
)


def test_truncate_string():
    """Test string truncation."""
    assert truncate_string("short", 10) == "short"
    assert truncate_string("very long string", 10) == "very lo..."
    assert truncate_string("word boundary test", 15, preserve_words=True) == "word boundary..."


def test_slugify():
    """Test slugification."""
    assert slugify("Hello World") == "hello-world"
    assert slugify("Test_String 123") == "test-string-123"
    assert slugify("Special!@#Characters") == "specialcharacters"
    assert slugify("Multiple   Spaces") == "multiple-spaces"


def test_camel_to_snake():
    """Test camelCase to snake_case conversion."""
    assert camel_to_snake("camelCase") == "camel_case"
    assert camel_to_snake("PascalCase") == "pascal_case"
    assert camel_to_snake("already_snake") == "already_snake"


def test_snake_to_camel():
    """Test snake_case to camelCase conversion."""
    assert snake_to_camel("snake_case") == "snakeCase"
    assert snake_to_camel("snake_case", capitalize_first=True) == "SnakeCase"
    assert snake_to_camel("alreadyCamel") == "alreadyCamel"

