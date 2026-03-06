import Link from "next/link";

/**
 * Props for the FeatureCard component
 */
export interface FeatureCardProps {
  /** Emoji or icon to display */
  icon: string;
  /** Card title */
  title: string;
  /** Card description */
  description: string;
  /** Optional link URL - if provided, card becomes clickable */
  href?: string;
  /** Optional external link indicator */
  isExternal?: boolean;
}

/**
 * Reusable feature card component for displaying product features
 * Supports both static and linked variants
 *
 * @audit DEBT-11 - Extract FeatureCard from inline JSX in page.tsx
 *
 * @example
 * ```tsx
 * <FeatureCard
 *   icon="🤖"
 *   title="AI-Powered Analysis"
 *   description="Intelligent code analysis using GPT-4 and Claude"
 * />
 * ```
 */
export function FeatureCard({
  icon,
  title,
  description,
  href,
  isExternal = false,
}: FeatureCardProps) {
  const cardContent = (
    <>
      <h3 className="mb-3 text-xl font-semibold text-slate-900 dark:text-slate-50">
        {icon} {title}
      </h3>
      <p className="text-slate-600 dark:text-slate-400">{description}</p>
    </>
  );

  const cardClasses =
    "rounded-lg border border-slate-200 bg-white/60 p-6 backdrop-blur-sm transition-colors dark:border-slate-700 dark:bg-slate-800/60";

  // If href is provided, render as a link
  if (href) {
    if (isExternal) {
      return (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className={`${cardClasses} hover:border-blue-300 hover:bg-white/80 dark:hover:border-blue-700 dark:hover:bg-slate-800/80`}
        >
          {cardContent}
        </a>
      );
    }

    return (
      <Link
        href={href}
        className={`${cardClasses} hover:border-blue-300 hover:bg-white/80 dark:hover:border-blue-700 dark:hover:bg-slate-800/80`}
      >
        {cardContent}
      </Link>
    );
  }

  // Static card (no link)
  return <div className={cardClasses}>{cardContent}</div>;
}

export default FeatureCard;
