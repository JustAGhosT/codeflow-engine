"""Number formatting utilities."""


def format_number(
    value: float | int,
    decimals: int = 2,
    thousands_separator: str = ",",
    decimal_separator: str = ".",
) -> str:
    """
    Format number with thousands separator and decimal places.

    Args:
        value: Number to format
        decimals: Number of decimal places
        thousands_separator: Thousands separator character
        decimal_separator: Decimal separator character

    Returns:
        Formatted number string
    """
    # Format with decimal places
    formatted = f"{value:,.{decimals}f}"

    # Replace separators if needed
    if thousands_separator != ",":
        formatted = formatted.replace(",", "TEMP_THOUSANDS")
        formatted = formatted.replace(".", decimal_separator)
        formatted = formatted.replace("TEMP_THOUSANDS", thousands_separator)
    elif decimal_separator != ".":
        # Split by decimal point
        parts = formatted.split(".")
        if len(parts) == 2:
            formatted = thousands_separator.join(parts[0].split(",")) + decimal_separator + parts[1]
        else:
            formatted = thousands_separator.join(parts[0].split(","))

    return formatted


def format_bytes(bytes_value: int, binary: bool = False) -> str:
    """
    Format bytes to human-readable string.

    Args:
        bytes_value: Number of bytes
        binary: Use binary (1024) or decimal (1000) units

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    base = 1024 if binary else 1000
    units = ["B", "KB", "MB", "GB", "TB", "PB"] if not binary else ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]

    if bytes_value == 0:
        return "0 B"

    unit_index = 0
    value = float(bytes_value)

    while value >= base and unit_index < len(units) - 1:
        value /= base
        unit_index += 1

    return f"{value:.2f} {units[unit_index]}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format number as percentage.

    Args:
        value: Number to format (0.0 to 1.0 or 0 to 100)
        decimals: Number of decimal places

    Returns:
        Formatted percentage string
    """
    # Assume value is 0-1 if less than 1, otherwise 0-100
    if value <= 1.0:
        percentage = value * 100
    else:
        percentage = value

    return f"{percentage:.{decimals}f}%"
