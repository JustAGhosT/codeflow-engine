/**
 * Analytics Utilities
 *
 * This module provides a scaffold for analytics integration.
 * Production implementation should integrate with a service like:
 * - Plausible Analytics (privacy-focused, recommended for alpha)
 * - Azure Application Insights
 * - Google Analytics 4
 * - Mixpanel
 * - PostHog
 *
 * @audit DEBT-16 - Add analytics integration scaffold
 *
 * TODO: Production hardening required:
 * - Choose and install analytics SDK
 * - Configure site ID/tracking code from environment variables
 * - Implement cookie consent if required (GDPR/CCPA)
 * - Set up conversion goals
 * - Configure custom events for key user actions
 */

/**
 * Standard event types for tracking
 */
export type AnalyticsEventType =
  | "page_view"
  | "click"
  | "form_submit"
  | "conversion"
  | "error"
  | "custom";

/**
 * Event properties for analytics tracking
 */
export interface AnalyticsEvent {
  /** Event name/type */
  name: string;
  /** Event category */
  category?: AnalyticsEventType;
  /** Additional properties */
  properties?: Record<string, string | number | boolean>;
}

/**
 * Check if user has opted out of tracking (Do Not Track)
 */
function hasDoNotTrack(): boolean {
  if (typeof window === "undefined") return true;
  return navigator.doNotTrack === "1" || (window as { doNotTrack?: string }).doNotTrack === "1";
}

/**
 * Track a page view
 *
 * @param path - Page path (defaults to current path)
 * @param title - Page title (defaults to document title)
 *
 * @example
 * ```ts
 * // In a Next.js page component or useEffect
 * trackPageView('/installation', 'Installation Guide');
 * ```
 */
export function trackPageView(path?: string, title?: string): void {
  if (hasDoNotTrack() || hasOptedOut()) return;

  const pagePath = path || (typeof window !== "undefined" ? window.location.pathname : "");
  const pageTitle = title || (typeof document !== "undefined" ? document.title : "");

  // TODO: Replace with actual analytics SDK
  // Example Plausible implementation:
  // if (window.plausible) {
  //   window.plausible('pageview', { props: { path: pagePath, title: pageTitle } });
  // }

  if (process.env.NODE_ENV === "development") {
    console.log("[ANALYTICS] Page view:", { path: pagePath, title: pageTitle });
  }
}

/**
 * Track a custom event
 *
 * @param event - Event details to track
 *
 * @example
 * ```ts
 * trackEvent({
 *   name: 'alpha_signup_click',
 *   category: 'conversion',
 *   properties: { source: 'hero_cta' }
 * });
 * ```
 */
export function trackEvent(event: AnalyticsEvent): void {
  if (hasDoNotTrack() || hasOptedOut()) return;

  // TODO: Replace with actual analytics SDK
  // Example Plausible implementation:
  // if (window.plausible) {
  //   window.plausible(event.name, { props: event.properties });
  // }

  if (process.env.NODE_ENV === "development") {
    console.log("[ANALYTICS] Event:", event);
  }
}

/**
 * Track a click event on a CTA or important element
 *
 * @param elementName - Name/identifier of the clicked element
 * @param properties - Additional properties
 */
export function trackClick(
  elementName: string,
  properties?: Record<string, string | number | boolean>
): void {
  trackEvent({
    name: `click_${elementName}`,
    category: "click",
    properties,
  });
}

/**
 * Track a conversion event (e.g., signup, download)
 *
 * @param conversionType - Type of conversion
 * @param properties - Additional properties
 */
export function trackConversion(
  conversionType: string,
  properties?: Record<string, string | number | boolean>
): void {
  trackEvent({
    name: `conversion_${conversionType}`,
    category: "conversion",
    properties,
  });
}

/**
 * Track form submission
 *
 * @param formName - Name/identifier of the form
 * @param success - Whether submission was successful
 * @param properties - Additional properties
 */
export function trackFormSubmit(
  formName: string,
  success: boolean,
  properties?: Record<string, string | number | boolean>
): void {
  trackEvent({
    name: `form_${formName}_${success ? "success" : "failure"}`,
    category: "form_submit",
    properties: { ...properties, success },
  });
}

/**
 * Initialize analytics (call once at app startup)
 *
 * @param siteId - Analytics site ID or tracking code
 */
export function initializeAnalytics(siteId?: string): void {
  // Respect Do Not Track preference
  if (hasDoNotTrack()) {
    if (process.env.NODE_ENV === "development") {
      console.log("[ANALYTICS] Do Not Track enabled, analytics disabled");
    }
    return;
  }

  // TODO: Replace with actual analytics SDK initialization
  // Example Plausible implementation (add script to head):
  // const script = document.createElement('script');
  // script.defer = true;
  // script.dataset.domain = siteId;
  // script.src = 'https://plausible.io/js/script.js';
  // document.head.appendChild(script);

  if (process.env.NODE_ENV === "development") {
    console.log("[ANALYTICS] Analytics initialized:", {
      siteId: siteId ? "[CONFIGURED]" : "[NOT CONFIGURED]",
    });
  }
}

/**
 * Opt user out of analytics tracking
 * Store preference in localStorage
 */
export function optOutOfTracking(): void {
  if (typeof localStorage !== "undefined") {
    try {
      localStorage.setItem("analytics_opt_out", "true");
    } catch {
      // localStorage unavailable
    }
  }

  if (process.env.NODE_ENV === "development") {
    console.log("[ANALYTICS] User opted out of tracking");
  }
}

/**
 * Check if user has opted out of tracking
 */
export function hasOptedOut(): boolean {
  if (typeof localStorage === "undefined") return false;
  try {
    return localStorage.getItem("analytics_opt_out") === "true";
  } catch {
    return false;
  }
}
