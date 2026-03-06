import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { FeatureCard } from "../FeatureCard";

describe("FeatureCard", () => {
  const defaultProps = {
    icon: "🤖",
    title: "Test Feature",
    description: "This is a test description",
  };

  describe("Static Card (no link)", () => {
    it("renders icon, title, and description", () => {
      render(<FeatureCard {...defaultProps} />);

      expect(screen.getByText(/🤖/)).toBeInTheDocument();
      expect(screen.getByText(/Test Feature/)).toBeInTheDocument();
      expect(
        screen.getByText("This is a test description")
      ).toBeInTheDocument();
    });

    it("renders as a div when no href provided", () => {
      const { container } = render(<FeatureCard {...defaultProps} />);

      // Should be a div, not a link
      expect(container.querySelector("div")).toBeInTheDocument();
      expect(container.querySelector("a")).not.toBeInTheDocument();
    });

    it("applies correct styling classes", () => {
      const { container } = render(<FeatureCard {...defaultProps} />);
      const card = container.firstChild as HTMLElement;

      expect(card).toHaveClass("rounded-lg");
      expect(card).toHaveClass("border");
      expect(card).toHaveClass("p-6");
    });
  });

  describe("Internal Link Card", () => {
    it("renders as a Next.js Link when href provided", () => {
      const { container } = render(
        <FeatureCard {...defaultProps} href="/features" />
      );

      const link = container.querySelector("a");
      expect(link).toBeInTheDocument();
      expect(link).toHaveAttribute("href", "/features");
    });

    it("does not have target or rel attributes for internal links", () => {
      const { container } = render(
        <FeatureCard {...defaultProps} href="/features" />
      );

      const link = container.querySelector("a");
      expect(link).not.toHaveAttribute("target");
      expect(link).not.toHaveAttribute("rel");
    });

    it("applies hover styles", () => {
      const { container } = render(
        <FeatureCard {...defaultProps} href="/features" />
      );

      const link = container.querySelector("a");
      expect(link).toHaveClass("hover:border-blue-300");
    });
  });

  describe("External Link Card", () => {
    it("renders with target and rel attributes when isExternal", () => {
      const { container } = render(
        <FeatureCard
          {...defaultProps}
          href="https://example.com"
          isExternal={true}
        />
      );

      const link = container.querySelector("a");
      expect(link).toBeInTheDocument();
      expect(link).toHaveAttribute("href", "https://example.com");
      expect(link).toHaveAttribute("target", "_blank");
      expect(link).toHaveAttribute("rel", "noopener noreferrer");
    });
  });

  describe("Content rendering", () => {
    it("combines icon and title in heading", () => {
      render(<FeatureCard {...defaultProps} />);

      const heading = screen.getByRole("heading", { level: 3 });
      expect(heading).toHaveTextContent("🤖 Test Feature");
    });

    it("renders description in paragraph", () => {
      render(<FeatureCard {...defaultProps} />);

      const description = screen.getByText("This is a test description");
      expect(description.tagName).toBe("P");
    });

    it("handles multi-line descriptions", () => {
      const longDescription =
        "This is a longer description that spans multiple sentences. It should still render correctly.";

      render(<FeatureCard {...defaultProps} description={longDescription} />);

      expect(screen.getByText(longDescription)).toBeInTheDocument();
    });
  });
});
