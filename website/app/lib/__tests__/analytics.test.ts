import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import {
  trackPageView,
  trackEvent,
  trackClick,
  trackConversion,
  trackFormSubmit,
  initializeAnalytics,
  optOutOfTracking,
  hasOptedOut,
} from "../analytics";

describe("analytics", () => {
  const originalEnv = process.env.NODE_ENV;
  const consoleSpy = vi.spyOn(console, "log").mockImplementation(() => {});

  // Mock navigator.doNotTrack
  const originalNavigator = global.navigator;

  beforeEach(() => {
    vi.clearAllMocks();
    // @ts-expect-error - modifying process.env for testing
    process.env.NODE_ENV = "development";

    // Reset navigator mock
    Object.defineProperty(global, "navigator", {
      value: { doNotTrack: "0" },
      writable: true,
    });

    // Reset localStorage mock
    vi.stubGlobal("localStorage", {
      getItem: vi.fn().mockReturnValue(null),
      setItem: vi.fn(),
      removeItem: vi.fn(),
    });
  });

  afterEach(() => {
    // @ts-expect-error - modifying process.env for testing
    process.env.NODE_ENV = originalEnv;
    Object.defineProperty(global, "navigator", {
      value: originalNavigator,
      writable: true,
    });
    vi.unstubAllGlobals();
  });

  describe("trackPageView", () => {
    it("logs page view in development", () => {
      trackPageView("/test-page", "Test Page");

      expect(consoleSpy).toHaveBeenCalledWith("[ANALYTICS] Page view:", {
        path: "/test-page",
        title: "Test Page",
      });
    });

    it("respects Do Not Track", () => {
      Object.defineProperty(global, "navigator", {
        value: { doNotTrack: "1" },
        writable: true,
      });

      trackPageView("/test-page", "Test Page");

      expect(consoleSpy).not.toHaveBeenCalled();
    });
  });

  describe("trackEvent", () => {
    it("logs custom event in development", () => {
      trackEvent({
        name: "test_event",
        category: "custom",
        properties: { key: "value" },
      });

      expect(consoleSpy).toHaveBeenCalledWith("[ANALYTICS] Event:", {
        name: "test_event",
        category: "custom",
        properties: { key: "value" },
      });
    });

    it("respects Do Not Track", () => {
      Object.defineProperty(global, "navigator", {
        value: { doNotTrack: "1" },
        writable: true,
      });

      trackEvent({ name: "test_event" });

      expect(consoleSpy).not.toHaveBeenCalled();
    });
  });

  describe("trackClick", () => {
    it("tracks click event with prefixed name", () => {
      trackClick("cta_button", { position: "hero" });

      expect(consoleSpy).toHaveBeenCalledWith("[ANALYTICS] Event:", {
        name: "click_cta_button",
        category: "click",
        properties: { position: "hero" },
      });
    });
  });

  describe("trackConversion", () => {
    it("tracks conversion event with prefixed name", () => {
      trackConversion("alpha_signup", { source: "landing" });

      expect(consoleSpy).toHaveBeenCalledWith("[ANALYTICS] Event:", {
        name: "conversion_alpha_signup",
        category: "conversion",
        properties: { source: "landing" },
      });
    });
  });

  describe("trackFormSubmit", () => {
    it("tracks successful form submission", () => {
      trackFormSubmit("contact", true, { fields: 5 });

      expect(consoleSpy).toHaveBeenCalledWith("[ANALYTICS] Event:", {
        name: "form_contact_success",
        category: "form_submit",
        properties: { fields: 5, success: true },
      });
    });

    it("tracks failed form submission", () => {
      trackFormSubmit("contact", false);

      expect(consoleSpy).toHaveBeenCalledWith("[ANALYTICS] Event:", {
        name: "form_contact_failure",
        category: "form_submit",
        properties: { success: false },
      });
    });
  });

  describe("initializeAnalytics", () => {
    it("logs initialization with site ID", () => {
      initializeAnalytics("example.com");

      expect(consoleSpy).toHaveBeenCalledWith("[ANALYTICS] Analytics initialized:", {
        siteId: "[CONFIGURED]",
      });
    });

    it("logs initialization without site ID", () => {
      initializeAnalytics();

      expect(consoleSpy).toHaveBeenCalledWith("[ANALYTICS] Analytics initialized:", {
        siteId: "[NOT CONFIGURED]",
      });
    });

    it("does not initialize when Do Not Track is enabled", () => {
      Object.defineProperty(global, "navigator", {
        value: { doNotTrack: "1" },
        writable: true,
      });

      initializeAnalytics("example.com");

      expect(consoleSpy).toHaveBeenCalledWith(
        "[ANALYTICS] Do Not Track enabled, analytics disabled"
      );
    });
  });

  describe("optOutOfTracking", () => {
    it("sets opt-out flag in localStorage", () => {
      optOutOfTracking();

      expect(localStorage.setItem).toHaveBeenCalledWith(
        "analytics_opt_out",
        "true"
      );
    });

    it("logs opt-out in development", () => {
      optOutOfTracking();

      expect(consoleSpy).toHaveBeenCalledWith(
        "[ANALYTICS] User opted out of tracking"
      );
    });
  });

  describe("hasOptedOut", () => {
    it("returns false when not opted out", () => {
      expect(hasOptedOut()).toBe(false);
    });

    it("returns true when opted out", () => {
      vi.stubGlobal("localStorage", {
        getItem: vi.fn().mockReturnValue("true"),
        setItem: vi.fn(),
      });

      expect(hasOptedOut()).toBe(true);
    });
  });
});
