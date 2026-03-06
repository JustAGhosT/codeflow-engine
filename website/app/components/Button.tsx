import Link from "next/link";
import { forwardRef, type ButtonHTMLAttributes, type AnchorHTMLAttributes, type ReactNode } from "react";

/**
 * Button variant definitions
 * - primary: Gradient blue-to-purple, high emphasis
 * - secondary: Solid dark/light, medium emphasis
 * - outline: Border only, low emphasis
 */
export type ButtonVariant = "primary" | "secondary" | "outline";

/**
 * Button size definitions
 */
export type ButtonSize = "sm" | "md" | "lg";

/**
 * Base props shared across all button types
 */
interface BaseButtonProps {
  /** Visual variant of the button */
  variant?: ButtonVariant;
  /** Size of the button */
  size?: ButtonSize;
  /** Additional CSS classes */
  className?: string;
  /** Button content */
  children: ReactNode;
}

/**
 * Props when rendering as a button element
 */
interface ButtonAsButton extends BaseButtonProps, Omit<ButtonHTMLAttributes<HTMLButtonElement>, keyof BaseButtonProps> {
  /** Render as a native button */
  as?: "button";
  /** href is not allowed for button */
  href?: never;
  /** isExternal is not allowed for button */
  isExternal?: never;
}

/**
 * Props when rendering as a link (anchor or Next.js Link)
 */
interface ButtonAsLink extends BaseButtonProps, Omit<AnchorHTMLAttributes<HTMLAnchorElement>, keyof BaseButtonProps | "href"> {
  /** Render as a link */
  as: "a";
  /** Link destination (required for link variant) */
  href: string;
  /** Whether link opens in new tab */
  isExternal?: boolean;
}

export type ButtonProps = ButtonAsButton | ButtonAsLink;

/**
 * Variant style mappings
 */
const variantStyles: Record<ButtonVariant, string> = {
  primary:
    "bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 hover:shadow-lg",
  secondary:
    "bg-slate-800 text-white hover:bg-slate-700 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200",
  outline:
    "border-2 border-slate-300 bg-white/50 text-slate-900 backdrop-blur-sm hover:border-slate-400 dark:border-slate-600 dark:bg-slate-800/50 dark:text-slate-50 dark:hover:border-slate-500",
};

/**
 * Size style mappings
 */
const sizeStyles: Record<ButtonSize, string> = {
  sm: "px-4 py-2 text-sm",
  md: "px-6 py-2.5 text-base",
  lg: "px-8 py-3 text-lg",
};

/**
 * Base styles applied to all buttons
 */
const baseStyles =
  "inline-block rounded-lg font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

/**
 * Standardized Button component with consistent styling across the application
 *
 * Supports three variants (primary, secondary, outline) and three sizes (sm, md, lg).
 * Can render as a button element or a link (using Next.js Link for internal routes).
 *
 * @audit DEBT-12 - Standardize button styles across pages
 *
 * @example
 * ```tsx
 * // As a button
 * <Button variant="primary" size="lg" onClick={handleClick}>
 *   Submit
 * </Button>
 *
 * // As an internal link
 * <Button as="a" href="/installation" variant="secondary">
 *   Get Started
 * </Button>
 *
 * // As an external link
 * <Button as="a" href="https://github.com" variant="outline" isExternal>
 *   View on GitHub
 * </Button>
 * ```
 */
export const Button = forwardRef<HTMLButtonElement | HTMLAnchorElement, ButtonProps>(
  function Button(props, ref) {
    const {
      variant = "primary",
      size = "md",
      className = "",
      children,
      ...rest
    } = props;

    const combinedClassName = `${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`.trim();

    // Render as link
    if (props.as === "a") {
      const { href, isExternal, as: _asLink, ...linkRest } = rest as ButtonAsLink;
      void _asLink; // Intentionally unused - destructured to exclude from spread

      if (isExternal) {
        return (
          <a
            ref={ref as React.Ref<HTMLAnchorElement>}
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className={combinedClassName}
            {...linkRest}
          >
            {children}
          </a>
        );
      }

      return (
        <Link
          ref={ref as React.Ref<HTMLAnchorElement>}
          href={href}
          className={combinedClassName}
          {...linkRest}
        >
          {children}
        </Link>
      );
    }

    // Render as button
    const { as: _asButton, ...buttonRest } = rest as ButtonAsButton;
    void _asButton; // Intentionally unused - destructured to exclude from spread
    return (
      <button
        ref={ref as React.Ref<HTMLButtonElement>}
        className={combinedClassName}
        {...buttonRest}
      >
        {children}
      </button>
    );
  }
);

export default Button;
