/**
 * Date and time formatting utilities.
 */

/**
 * Format datetime to string.
 *
 * @param date - Date object to format
 * @param format - Format string ('iso' for ISO 8601, or custom format)
 * @returns Formatted datetime string
 */
export function formatDateTime(date: Date, format: string = "default"): string {
  if (format === "iso") {
    return date.toISOString();
  }

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

/**
 * Format datetime as relative time (e.g., "2 hours ago").
 *
 * @param date - Date object
 * @param now - Current date (defaults to now)
 * @returns Relative time string
 */
export function formatRelativeTime(date: Date, now: Date = new Date()): string {
  const delta = now.getTime() - date.getTime();
  const seconds = Math.floor(Math.abs(delta) / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);

  const isFuture = delta < 0;
  const prefix = isFuture ? "in " : "";
  const suffix = isFuture ? "" : " ago";

  if (years > 0) {
    return `${prefix}${years} year${years > 1 ? "s" : ""}${suffix}`;
  } else if (months > 0) {
    return `${prefix}${months} month${months > 1 ? "s" : ""}${suffix}`;
  } else if (days > 0) {
    return `${prefix}${days} day${days > 1 ? "s" : ""}${suffix}`;
  } else if (hours > 0) {
    return `${prefix}${hours} hour${hours > 1 ? "s" : ""}${suffix}`;
  } else if (minutes > 0) {
    return `${prefix}${minutes} minute${minutes > 1 ? "s" : ""}${suffix}`;
  } else {
    return isFuture ? "in a moment" : "just now";
  }
}
