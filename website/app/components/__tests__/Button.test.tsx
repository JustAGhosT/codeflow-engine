import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "../Button";

describe("Button", () => {
  describe("Button element rendering", () => {
    it("renders as a button by default", () => {
      render(<Button>Click me</Button>);

      const button = screen.getByRole("button", { name: "Click me" });
      expect(button).toBeInTheDocument();
      expect(button.tagName).toBe("BUTTON");
    });

    it("handles click events", () => {
      const handleClick = vi.fn();
      render(<Button onClick={handleClick}>Click me</Button>);

      const button = screen.getByRole("button", { name: "Click me" });
      fireEvent.click(button);

      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it("can be disabled", () => {
      const handleClick = vi.fn();
      render(
        <Button onClick={handleClick} disabled>
          Disabled
        </Button>
      );

      const button = screen.getByRole("button", { name: "Disabled" });
      expect(button).toBeDisabled();
      expect(button).toHaveClass("disabled:opacity-50");

      fireEvent.click(button);
      expect(handleClick).not.toHaveBeenCalled();
    });

    it("passes button attributes", () => {
      render(
        <Button type="submit" name="test-button">
          Submit
        </Button>
      );

      const button = screen.getByRole("button", { name: "Submit" });
      expect(button).toHaveAttribute("type", "submit");
      expect(button).toHaveAttribute("name", "test-button");
    });
  });

  describe("Link rendering", () => {
    it("renders as a Next.js Link for internal routes", () => {
      const { container } = render(
        <Button as="a" href="/installation">
          Get Started
        </Button>
      );

      const link = container.querySelector("a");
      expect(link).toBeInTheDocument();
      expect(link).toHaveAttribute("href", "/installation");
      expect(link).not.toHaveAttribute("target");
      expect(link).not.toHaveAttribute("rel");
    });

    it("renders as external link with target and rel", () => {
      const { container } = render(
        <Button as="a" href="https://github.com" isExternal>
          GitHub
        </Button>
      );

      const link = container.querySelector("a");
      expect(link).toBeInTheDocument();
      expect(link).toHaveAttribute("href", "https://github.com");
      expect(link).toHaveAttribute("target", "_blank");
      expect(link).toHaveAttribute("rel", "noopener noreferrer");
    });
  });

  describe("Variants", () => {
    it("applies primary variant styles by default", () => {
      render(<Button>Primary</Button>);

      const button = screen.getByRole("button", { name: "Primary" });
      expect(button).toHaveClass("bg-gradient-to-r");
      expect(button).toHaveClass("from-blue-600");
      expect(button).toHaveClass("to-purple-600");
    });

    it("applies secondary variant styles", () => {
      render(<Button variant="secondary">Secondary</Button>);

      const button = screen.getByRole("button", { name: "Secondary" });
      expect(button).toHaveClass("bg-slate-800");
      expect(button).toHaveClass("text-white");
    });

    it("applies outline variant styles", () => {
      render(<Button variant="outline">Outline</Button>);

      const button = screen.getByRole("button", { name: "Outline" });
      expect(button).toHaveClass("border-2");
      expect(button).toHaveClass("border-slate-300");
      expect(button).toHaveClass("bg-white/50");
    });
  });

  describe("Sizes", () => {
    it("applies medium size by default", () => {
      render(<Button>Medium</Button>);

      const button = screen.getByRole("button", { name: "Medium" });
      expect(button).toHaveClass("px-6");
      expect(button).toHaveClass("py-2.5");
      expect(button).toHaveClass("text-base");
    });

    it("applies small size", () => {
      render(<Button size="sm">Small</Button>);

      const button = screen.getByRole("button", { name: "Small" });
      expect(button).toHaveClass("px-4");
      expect(button).toHaveClass("py-2");
      expect(button).toHaveClass("text-sm");
    });

    it("applies large size", () => {
      render(<Button size="lg">Large</Button>);

      const button = screen.getByRole("button", { name: "Large" });
      expect(button).toHaveClass("px-8");
      expect(button).toHaveClass("py-3");
      expect(button).toHaveClass("text-lg");
    });
  });

  describe("Base styles", () => {
    it("applies base styles to all buttons", () => {
      render(<Button>Styled</Button>);

      const button = screen.getByRole("button", { name: "Styled" });
      expect(button).toHaveClass("inline-block");
      expect(button).toHaveClass("rounded-lg");
      expect(button).toHaveClass("font-semibold");
      expect(button).toHaveClass("transition-all");
    });

    it("applies focus ring styles for accessibility", () => {
      render(<Button>Accessible</Button>);

      const button = screen.getByRole("button", { name: "Accessible" });
      expect(button).toHaveClass("focus:ring-2");
      expect(button).toHaveClass("focus:ring-blue-500");
    });
  });

  describe("Custom className", () => {
    it("merges custom className with default styles", () => {
      render(<Button className="custom-class">Custom</Button>);

      const button = screen.getByRole("button", { name: "Custom" });
      expect(button).toHaveClass("custom-class");
      expect(button).toHaveClass("rounded-lg"); // Still has base styles
    });
  });

  describe("Snapshot tests", () => {
    it("matches snapshot for primary button", () => {
      const { container } = render(
        <Button variant="primary" size="lg">
          Primary Large
        </Button>
      );
      expect(container.firstChild).toMatchSnapshot();
    });

    it("matches snapshot for secondary button", () => {
      const { container } = render(
        <Button variant="secondary" size="md">
          Secondary Medium
        </Button>
      );
      expect(container.firstChild).toMatchSnapshot();
    });

    it("matches snapshot for outline button", () => {
      const { container } = render(
        <Button variant="outline" size="sm">
          Outline Small
        </Button>
      );
      expect(container.firstChild).toMatchSnapshot();
    });

    it("matches snapshot for link button", () => {
      const { container } = render(
        <Button as="a" href="/test" variant="primary">
          Link Button
        </Button>
      );
      expect(container.firstChild).toMatchSnapshot();
    });
  });
});
