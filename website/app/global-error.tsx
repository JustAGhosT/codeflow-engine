'use client';

import { useEffect } from 'react';
import { captureError } from '@/app/lib/monitoring';

interface GlobalErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function GlobalError({ error, reset }: GlobalErrorProps) {
  useEffect(() => {
    // Report error to monitoring service
    captureError(error, { component: 'GlobalErrorBoundary' }, 'fatal');
  }, [error]);

  return (
    <html lang="en">
      <body>
        <div
          style={{
            display: 'flex',
            minHeight: '100vh',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '1.5rem',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            backgroundColor: '#f8fafc',
          }}
        >
          <div style={{ maxWidth: '28rem', textAlign: 'center' }}>
            <h1
              style={{
                marginBottom: '1rem',
                fontSize: '2.25rem',
                fontWeight: 'bold',
                color: '#0f172a',
              }}
            >
              Something went wrong
            </h1>
            <p
              style={{
                marginBottom: '2rem',
                fontSize: '1.125rem',
                color: '#64748b',
              }}
            >
              A critical error occurred. Please refresh the page or contact support if the problem persists.
            </p>
            {error.digest && (
              <p
                style={{
                  marginBottom: '1rem',
                  fontFamily: 'monospace',
                  fontSize: '0.875rem',
                  color: '#94a3b8',
                }}
              >
                Error ID: {error.digest}
              </p>
            )}
            <button
              onClick={reset}
              style={{
                padding: '0.75rem 1.5rem',
                fontSize: '1rem',
                fontWeight: '600',
                color: 'white',
                backgroundColor: '#2563eb',
                border: 'none',
                borderRadius: '0.5rem',
                cursor: 'pointer',
              }}
            >
              Try again
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
