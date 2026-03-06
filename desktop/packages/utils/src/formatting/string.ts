/**
 * String formatting utilities.
 */

/**
 * Truncate string to maximum length.
 *
 * @param value - String to truncate
 * @param maxLength - Maximum length (including suffix)
 * @param suffix - Suffix to add if truncated
 * @param preserveWords - Whether to preserve word boundaries
 * @returns Truncated string
 */
export function truncateString(
  value: string,
  maxLength: number,
  suffix: string = "...",
  preserveWords: boolean = true
): string {
  if (value.length <= maxLength) {
    return value;
  }

  if (preserveWords) {
    const truncated = value.substring(0, maxLength - suffix.length);
    const lastSpace = truncated.lastIndexOf(" ");
    if (lastSpace > maxLength * 0.5) {
      return truncated.substring(0, lastSpace) + suffix;
    }
    return truncated + suffix;
  }

  return value.substring(0, maxLength - suffix.length) + suffix;
}

/**
 * Convert string to URL-friendly slug.
 *
 * @param value - String to slugify
 * @param separator - Word separator character
 * @returns Slugified string
 */
export function slugify(value: string, separator: string = "-"): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[\s_]+/g, separator)
    .replace(/[^\w\-]+/g, "")
    .replace(new RegExp(`${separator}+`, "g"), separator)
    .replace(new RegExp(`^${separator}|${separator}$`, "g"), "");
}

/**
 * Convert camelCase to snake_case.
 *
 * @param value - CamelCase string
 * @returns snake_case string
 */
export function camelToSnake(value: string): string {
  return value
    .replace(/([A-Z])/g, "_$1")
    .toLowerCase()
    .replace(/^_/, "");
}

/**
 * Convert snake_case to camelCase.
 *
 * @param value - snake_case string
 * @param capitalizeFirst - Whether to capitalize first letter (PascalCase)
 * @returns camelCase or PascalCase string
 */
export function snakeToCamel(
  value: string,
  capitalizeFirst: boolean = false
): string {
  const components = value.split("_");
  const first = capitalizeFirst
    ? components[0].charAt(0).toUpperCase() + components[0].slice(1)
    : components[0];
  const rest = components
    .slice(1)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1));
  return first + rest.join("");
}
