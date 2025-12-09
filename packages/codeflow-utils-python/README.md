# CodeFlow Utils Python

Shared utility functions for CodeFlow Python projects.

## Installation

```bash
pip install codeflow-utils-python
```

## Usage

### Validation

```python
from codeflow_utils.validation import validate_config, validate_url, sanitize_input

# Validate configuration
config = {"api_key": "test", "base_url": "https://api.example.com"}
is_valid, missing = validate_config(config, ["api_key", "base_url"])

# Validate URL
is_valid, error = validate_url("https://api.example.com", schemes=["https"])

# Sanitize input
clean_input = sanitize_input("  user input  ", max_length=100)
```

### Formatting

```python
from codeflow_utils.formatting.date import format_iso_datetime, format_relative_time
from datetime import datetime

# Format datetime
formatted = format_iso_datetime(datetime.now())

# Relative time
relative = format_relative_time(datetime(2025, 1, 1))
```

### Common Functions

```python
from codeflow_utils.common.retry import retry

@retry(max_attempts=3, delay=1.0)
def api_call():
    # API call that might fail
    pass
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black codeflow_utils tests

# Lint code
ruff check codeflow_utils tests
```

## License

MIT License

