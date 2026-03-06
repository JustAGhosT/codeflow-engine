/**
 * Root loading component for Next.js App Router
 * Displays while route segments are loading
 *
 * @audit DEBT-14 - Add loading states for navigation feedback
 */
export default function Loading() {
  return (
    <div
      className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-slate-50/80 to-slate-100/50 dark:from-slate-900/80 dark:to-slate-950/50"
      role="status"
      aria-live="polite"
      aria-label="Loading content"
    >
      <div className="flex flex-col items-center gap-4">
        {/* Animated spinner */}
        <div
          className="h-12 w-12 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600 dark:border-slate-700 dark:border-t-blue-400"
          aria-hidden="true"
        />

        {/* Loading text with pulse animation */}
        <p className="animate-pulse text-lg font-medium text-slate-600 dark:text-slate-400">
          Loading...
        </p>
      </div>
    </div>
  );
}
