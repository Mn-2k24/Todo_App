/**
 * ChatErrorDisplay Component
 *
 * Displays chat-specific errors with:
 * - Error icon and message
 * - User-friendly error descriptions
 * - Retry button (optional)
 * - Dismiss button
 */

"use client";

import { ApiException } from "@/lib/api";

interface ChatErrorDisplayProps {
  error: Error | ApiException | null;
  onRetry?: () => void;
  onDismiss?: () => void;
}

export default function ChatErrorDisplay({
  error,
  onRetry,
  onDismiss,
}: ChatErrorDisplayProps) {
  if (!error) {
    return null;
  }

  const getErrorMessage = (): string => {
    if (error instanceof ApiException) {
      // Handle specific error codes
      switch (error.error.code) {
        case "UNAUTHORIZED":
          return "Your session has expired. Please log in again.";
        case "FORBIDDEN":
          return "You don't have permission to access this conversation.";
        case "NOT_FOUND":
          return "Conversation not found. It may have been deleted.";
        case "INVALID_INPUT":
          return error.error.error || "Invalid message. Please check your input.";
        default:
          return error.error.error || "An unexpected error occurred.";
      }
    }

    // Network or other errors
    if (error.message.includes("fetch")) {
      return "Network error. Please check your connection and try again.";
    }

    return error.message || "Something went wrong. Please try again.";
  };

  const getErrorIcon = (): string => {
    if (error instanceof ApiException) {
      switch (error.error.code) {
        case "UNAUTHORIZED":
          return "🔒";
        case "FORBIDDEN":
          return "⛔";
        case "NOT_FOUND":
          return "🔍";
        default:
          return "⚠️";
      }
    }
    return "❌";
  };

  return (
    <div className="mx-4 my-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <div className="flex items-start space-x-3">
        {/* Error icon */}
        <div className="flex-shrink-0 text-2xl">{getErrorIcon()}</div>

        {/* Error content */}
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold text-red-800 dark:text-red-200 mb-1">
            Error
          </h3>
          <p className="text-sm text-red-700 dark:text-red-300">
            {getErrorMessage()}
          </p>

          {/* Error code (for debugging) */}
          {error instanceof ApiException && (
            <p className="text-xs text-red-600 dark:text-red-400 mt-1">
              Error code: {error.error.code}
            </p>
          )}
        </div>

        {/* Actions */}
        <div className="flex-shrink-0 flex items-center space-x-2">
          {onRetry && (
            <button
              onClick={onRetry}
              className="px-3 py-1.5 bg-red-600 text-white text-sm font-medium rounded hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
            >
              Retry
            </button>
          )}
          {onDismiss && (
            <button
              onClick={onDismiss}
              className="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-200 focus:outline-none"
              aria-label="Dismiss error"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
