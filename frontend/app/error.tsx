'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="container mx-auto py-10">
      <div className="max-w-md mx-auto text-center">
        <div className="bg-destructive/10 p-6 rounded-lg border border-destructive/20">
          <h2 className="text-xl font-bold text-destructive mb-2">Something went wrong!</h2>
          <p className="text-destructive/80 mb-4">
            We apologize for the inconvenience. Our team has been notified of the issue.
          </p>
          <button
            onClick={() => reset()}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  );
}