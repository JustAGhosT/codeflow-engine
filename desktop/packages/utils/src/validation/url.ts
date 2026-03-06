/**
 * URL validation utilities.
 */

export interface UrlValidationResult {
  valid: boolean;
  error?: string;
}

/**
 * Validate URL format.
 *
 * @param url - URL string to validate
 * @param schemes - Allowed URL schemes (optional)
 * @returns Validation result with valid flag and optional error message
 */
export function validateUrl(
  url: string,
  schemes?: string[]
): UrlValidationResult {
  if (!url || typeof url !== "string") {
    return { valid: false, error: "URL must be a non-empty string" };
  }

  try {
    const parsed = new URL(url);
    const scheme = parsed.protocol.slice(0, -1); // Remove trailing ':'

    if (schemes && !schemes.includes(scheme)) {
      return {
        valid: false,
        error: `URL scheme must be one of: ${schemes.join(", ")}`,
      };
    }

    return { valid: true };
  } catch (error) {
    return {
      valid: false,
      error: `Invalid URL format: ${error instanceof Error ? error.message : String(error)}`,
    };
  }
}

/**
 * Check if URL is valid.
 *
 * @param url - URL string to check
 * @param schemes - Allowed URL schemes (optional)
 * @returns True if URL is valid, false otherwise
 */
export function isValidUrl(url: string, schemes?: string[]): boolean {
  return validateUrl(url, schemes).valid;
}
