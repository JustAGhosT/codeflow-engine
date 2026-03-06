import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import {
  captureError,
  captureMessage,
  setUserContext,
  clearUserContext,
  initializeErrorTracking,
} from "../monitoring";

describe("monitoring", () => {
  const originalEnv = process.env.NODE_ENV;
  const consoleSpy = {
    error: vi.spyOn(console, "error").mockImplementation(() => {}),
    log: vi.spyOn(console, "log").mockImplementation(() => {}),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    // @ts-expect-error - modifying process.env for testing
    process.env.NODE_ENV = "development";
  });

  afterEach(() => {
    // @ts-expect-error - modifying process.env for testing
    process.env.NODE_ENV = originalEnv;
  });

  describe("captureError", () => {
    it("logs error to console in development", () => {
      const error = new Error("Test error");
      captureError(error);

      expect(consoleSpy.error).toHaveBeenCalledWith(
        "[ERROR]",
        error,
        undefined
      );
    });

    it("logs with context when provided", () => {
      const error = new Error("Test error");
      const context = { component: "TestComponent" };
      captureError(error, context);

      expect(consoleSpy.error).toHaveBeenCalledWith("[ERROR]", error, context);
    });

    it("uses specified severity level", () => {
      const error = new Error("Fatal error");
      captureError(error, undefined, "fatal");

      expect(consoleSpy.error).toHaveBeenCalledWith(
        "[FATAL]",
        error,
        undefined
      );
    });

    it("handles non-Error objects", () => {
      const errorLike = { message: "Something went wrong" };
      captureError(errorLike);

      expect(consoleSpy.error).toHaveBeenCalledWith(
        "[ERROR]",
        errorLike,
        undefined
      );
    });
  });

  describe("captureMessage", () => {
    it("logs message to console in development", () => {
      captureMessage("Test message");

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[INFO]",
        "Test message",
        undefined
      );
    });

    it("logs with context when provided", () => {
      const context = { tags: { feature: "auth" } };
      captureMessage("Auth event", context);

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[INFO]",
        "Auth event",
        context
      );
    });

    it("uses specified severity level", () => {
      captureMessage("Warning message", undefined, "warning");

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[WARNING]",
        "Warning message",
        undefined
      );
    });
  });

  describe("setUserContext", () => {
    it("logs user context in development", () => {
      setUserContext("user-123", "test@example.com", "testuser");

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[MONITORING] User context set:",
        {
          userId: "user-123",
          email: "test@example.com",
          username: "testuser",
        }
      );
    });

    it("handles optional parameters", () => {
      setUserContext("user-456");

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[MONITORING] User context set:",
        {
          userId: "user-456",
          email: undefined,
          username: undefined,
        }
      );
    });
  });

  describe("clearUserContext", () => {
    it("logs context cleared in development", () => {
      clearUserContext();

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[MONITORING] User context cleared"
      );
    });
  });

  describe("initializeErrorTracking", () => {
    it("logs initialization status in development", () => {
      initializeErrorTracking("https://sentry.io/dsn");

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[MONITORING] Error tracking initialized:",
        {
          dsn: "[CONFIGURED]",
          environment: "development",
        }
      );
    });

    it("indicates when DSN is not configured", () => {
      initializeErrorTracking();

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[MONITORING] Error tracking initialized:",
        {
          dsn: "[NOT CONFIGURED]",
          environment: "development",
        }
      );
    });

    it("uses provided environment", () => {
      initializeErrorTracking("dsn", "staging");

      expect(consoleSpy.log).toHaveBeenCalledWith(
        "[MONITORING] Error tracking initialized:",
        {
          dsn: "[CONFIGURED]",
          environment: "staging",
        }
      );
    });
  });
});
