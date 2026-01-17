/**
 * Error message component for displaying user-friendly errors.
 * Per FR-042: System MUST display user-friendly error messages when operations fail.
 */

import { getErrorMessage } from "@/lib/errors";

interface ErrorMessageProps {
  error: unknown;
  className?: string;
  onDismiss?: () => void;
}

export default function ErrorMessage({
  error,
  className = "",
  onDismiss,
}: ErrorMessageProps) {
  const message = getErrorMessage(error);

  return (
    <div
      className={`rounded-lg bg-error-50 border border-error-200 p-4 ${className}`}
      role="alert"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg
            className="h-5 w-5 text-error-400"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <p className="text-sm text-error-800">{message}</p>
        </div>
        {onDismiss && (
          <button
            type="button"
            onClick={onDismiss}
            className="ml-3 inline-flex rounded-md bg-error-50 p-1.5 text-error-500 hover:bg-error-100 focus:outline-none focus:ring-2 focus:ring-error-600 focus:ring-offset-2 focus:ring-offset-error-50"
            aria-label="Dismiss"
          >
            <svg
              className="h-5 w-5"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}

/**
 * Simple inline error message (no dismiss button).
 */
export function ErrorInline({ error, className = "" }: { error: unknown; className?: string }) {
  const message = getErrorMessage(error);

  return (
    <p className={`text-sm text-error-600 ${className}`} role="alert">
      {message}
    </p>
  );
}
