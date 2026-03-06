/**
 * Error Tracking and Monitoring Utilities
 *
 * This module provides a scaffold for error tracking integration.
 * Production implementation should integrate with a service like:
 * - Sentry (https://sentry.io)
 * - Azure Application Insights
 * - LogRocket
 * - Datadog
 *
 * @audit DEBT-15 - Add error tracking integration scaffold
 *
 * TODO: Production hardening required:
 * - Install chosen error tracking SDK (e.g., @sentry/nextjs)
 * - Configure DSN/connection string from environment variables
 * - Set up source maps for production debugging
 * - Configure sampling rates for high-traffic scenarios
 * - Add user context when authenticated
 */

/**
 * Error severity levels
 */
export type ErrorSeverity = "fatal" | "error" | "warning" | "info";

/**
 * Error context for additional debugging information
 */
export interface ErrorContext {
  /** User ID if authenticated */
  userId?: string;
  /** Component or page where error occurred */
  component?: string;
  /** Additional key-value pairs for context */
  tags?: Record<string, string>;
  /** Extra data to attach to the error */
  extra?: Record<string, unknown>;
}

/**
 * Capture and report an error to the monitoring service
 *
 * @param error - The error object to capture
 * @param context - Additional context for debugging
 * @param severity - Error severity level
 *
 * @example
 * ```ts
 * try {
 *   await riskyOperation();
 * } catch (error) {
 *   captureError(error, { component: 'UserProfile' }, 'error');
 * }
 * ```
 */
export function captureError(
  error: Error | unknown,
  context?: ErrorContext,
  severity: ErrorSeverity = "error"
): void {
  // TODO: Replace with actual error tracking SDK
  // Example Sentry implementation:
  // Sentry.captureException(error, {
  //   level: severity,
  //   tags: context?.tags,
  //   extra: context?.extra,
  //   user: context?.userId ? { id: context.userId } : undefined,
  // });

  // Development fallback: log to console
  if (process.env.NODE_ENV === "development") {
    console.error(`[${severity.toUpperCase()}]`, error, context);
  }
}

/**
 * Capture a message/log to the monitoring service
 *
 * @param message - The message to log
 * @param context - Additional context
 * @param severity - Message severity level
 */
export function captureMessage(
  message: string,
  context?: ErrorContext,
  severity: ErrorSeverity = "info"
): void {
  // TODO: Replace with actual error tracking SDK
  // Example Sentry implementation:
  // Sentry.captureMessage(message, {
  //   level: severity,
  //   tags: context?.tags,
  //   extra: context?.extra,
  // });

  if (process.env.NODE_ENV === "development") {
    console.log(`[${severity.toUpperCase()}]`, message, context);
  }
}

/**
 * Set user context for error tracking
 * Call this after user authentication
 *
 * @param userId - User identifier
 * @param email - User email (optional)
 * @param username - Username (optional)
 */
export function setUserContext(
  userId: string,
  email?: string,
  username?: string
): void {
  // TODO: Replace with actual error tracking SDK
  // Example Sentry implementation:
  // Sentry.setUser({
  //   id: userId,
  //   email,
  //   username,
  // });

  if (process.env.NODE_ENV === "development") {
    console.log("[MONITORING] User context set:", { userId, email, username });
  }
}

/**
 * Clear user context (e.g., on logout)
 */
export function clearUserContext(): void {
  // TODO: Replace with actual error tracking SDK
  // Example Sentry implementation:
  // Sentry.setUser(null);

  if (process.env.NODE_ENV === "development") {
    console.log("[MONITORING] User context cleared");
  }
}

/**
 * Initialize error tracking (call once at app startup)
 *
 * @param dsn - Data Source Name/connection string
 * @param environment - Current environment (production, staging, development)
 */
export function initializeErrorTracking(
  dsn?: string,
  environment: string = process.env.NODE_ENV || "development"
): void {
  // TODO: Replace with actual error tracking SDK initialization
  // Example Sentry implementation:
  // Sentry.init({
  //   dsn,
  //   environment,
  //   tracesSampleRate: environment === 'production' ? 0.1 : 1.0,
  //   replaysSessionSampleRate: 0.1,
  //   replaysOnErrorSampleRate: 1.0,
  // });

  if (process.env.NODE_ENV === "development") {
    console.log("[MONITORING] Error tracking initialized:", {
      dsn: dsn ? "[CONFIGURED]" : "[NOT CONFIGURED]",
      environment,
    });
  }
}
