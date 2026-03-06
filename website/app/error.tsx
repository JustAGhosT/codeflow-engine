'use client';

import { useEffect } from 'react';
import { captureError } from '@/app/lib/monitoring';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Report error to monitoring service
    captureError(error, { component: 'ErrorBoundary' }, 'error');
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-slate-50/80 to-slate-100/50 px-6 dark:from-slate-900/80 dark:to-slate-950/50">
      <div className="max-w-md text-center">
        <h1 className="mb-4 text-4xl font-bold tracking-tight text-slate-900 dark:text-slate-50">
          Something went wrong
        </h1>
        <p className="mb-8 text-lg text-slate-600 dark:text-slate-400">
          An unexpected error occurred. Please try again or contact support if the problem persists.
        </p>
        {error.digest && (
          <p className="mb-4 font-mono text-sm text-slate-500 dark:text-slate-500">
            Error ID: {error.digest}
          </p>
        )}
        <button
          onClick={reset}
          className="rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-3 font-semibold text-white transition-all hover:from-blue-700 hover:to-purple-700 hover:shadow-lg"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
