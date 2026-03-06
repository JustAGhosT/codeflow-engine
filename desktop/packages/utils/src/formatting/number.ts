/**
 * Number formatting utilities.
 */

/**
 * Format number with thousands separator and decimal places.
 *
 * @param value - Number to format
 * @param decimals - Number of decimal places
 * @param thousandsSeparator - Thousands separator character
 * @param decimalSeparator - Decimal separator character
 * @returns Formatted number string
 */
export function formatNumber(
  value: number,
  decimals: number = 2,
  thousandsSeparator: string = ",",
  decimalSeparator: string = "."
): string {
  return value.toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })
    .replace(/,/g, thousandsSeparator)
    .replace(/\./g, decimalSeparator);
}

/**
 * Format bytes to human-readable string.
 *
 * @param bytesValue - Number of bytes
 * @param binary - Use binary (1024) or decimal (1000) units
 * @returns Formatted string (e.g., "1.5 MB")
 */
export function formatBytes(bytesValue: number, binary: boolean = false): string {
  const base = binary ? 1024 : 1000;
  const units = binary
    ? ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    : ["B", "KB", "MB", "GB", "TB", "PB"];

  if (bytesValue === 0) {
    return "0 B";
  }

  let unitIndex = 0;
  let value = bytesValue;

  while (value >= base && unitIndex < units.length - 1) {
    value /= base;
    unitIndex++;
  }

  return `${value.toFixed(2)} ${units[unitIndex]}`;
}

/**
 * Format number as percentage.
 *
 * @param value - Number to format (0.0 to 1.0 or 0 to 100)
 * @param decimals - Number of decimal places
 * @returns Formatted percentage string
 */
export function formatPercentage(value: number, decimals: number = 1): string {
  const percentage = value <= 1.0 ? value * 100 : value;
  return `${percentage.toFixed(decimals)}%`;
}
