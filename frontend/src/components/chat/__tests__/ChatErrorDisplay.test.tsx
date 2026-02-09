/**
 * Unit tests for ChatErrorDisplay component
 *
 * Tests:
 * - Renders error message correctly
 * - Returns null when error is null
 * - Displays retry button when onRetry provided
 * - Displays dismiss button when onDismiss provided
 * - Calls onRetry when retry button clicked
 * - Calls onDismiss when dismiss button clicked
 * - Shows correct error icons for different error types
 * - Displays user-friendly messages for API errors
 */

import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import ChatErrorDisplay from "../ChatErrorDisplay";
import { ApiException } from "@/lib/api";

describe("ChatErrorDisplay", () => {
  const mockOnRetry = jest.fn();
  const mockOnDismiss = jest.fn();

  beforeEach(() => {
    mockOnRetry.mockClear();
    mockOnDismiss.mockClear();
  });

  it("returns null when error is null", () => {
    const { container } = render(<ChatErrorDisplay error={null} />);
    expect(container.firstChild).toBeNull();
  });

  it("renders error message for generic Error", () => {
    const error = new Error("Something went wrong");
    render(<ChatErrorDisplay error={error} />);

    const errorMessage = screen.getByText(/something went wrong/i);
    expect(errorMessage).toBeInTheDocument();
  });

  it("renders user-friendly message for UNAUTHORIZED error", () => {
    const error = new ApiException(
      { error: "Unauthorized", code: "UNAUTHORIZED", status: 401 },
      401
    );
    render(<ChatErrorDisplay error={error} />);

    const message = screen.getByText(/session has expired.*log in again/i);
    expect(message).toBeInTheDocument();
  });

  it("renders user-friendly message for FORBIDDEN error", () => {
    const error = new ApiException(
      { error: "Forbidden", code: "FORBIDDEN", status: 403 },
      403
    );
    render(<ChatErrorDisplay error={error} />);

    const message = screen.getByText(/don't have permission/i);
    expect(message).toBeInTheDocument();
  });

  it("renders user-friendly message for NOT_FOUND error", () => {
    const error = new ApiException(
      { error: "Not found", code: "NOT_FOUND", status: 404 },
      404
    );
    render(<ChatErrorDisplay error={error} />);

    const message = screen.getByText(/conversation not found/i);
    expect(message).toBeInTheDocument();
  });

  it("renders user-friendly message for network error", () => {
    const error = new Error("fetch failed: network error");
    render(<ChatErrorDisplay error={error} />);

    const message = screen.getByText(/network error.*check your connection/i);
    expect(message).toBeInTheDocument();
  });

  it("displays error code for ApiException", () => {
    const error = new ApiException(
      { error: "Bad request", code: "INVALID_INPUT", status: 400 },
      400
    );
    render(<ChatErrorDisplay error={error} />);

    const errorCode = screen.getByText(/error code.*INVALID_INPUT/i);
    expect(errorCode).toBeInTheDocument();
  });

  it("renders retry button when onRetry provided", () => {
    const error = new Error("Test error");
    render(<ChatErrorDisplay error={error} onRetry={mockOnRetry} />);

    const retryButton = screen.getByRole("button", { name: /retry/i });
    expect(retryButton).toBeInTheDocument();
  });

  it("does not render retry button when onRetry not provided", () => {
    const error = new Error("Test error");
    render(<ChatErrorDisplay error={error} />);

    const retryButton = screen.queryByRole("button", { name: /retry/i });
    expect(retryButton).not.toBeInTheDocument();
  });

  it("renders dismiss button when onDismiss provided", () => {
    const error = new Error("Test error");
    render(<ChatErrorDisplay error={error} onDismiss={mockOnDismiss} />);

    const dismissButton = screen.getByLabelText(/dismiss error/i);
    expect(dismissButton).toBeInTheDocument();
  });

  it("does not render dismiss button when onDismiss not provided", () => {
    const error = new Error("Test error");
    render(<ChatErrorDisplay error={error} />);

    const dismissButton = screen.queryByLabelText(/dismiss error/i);
    expect(dismissButton).not.toBeInTheDocument();
  });

  it("calls onRetry when retry button clicked", () => {
    const error = new Error("Test error");
    render(<ChatErrorDisplay error={error} onRetry={mockOnRetry} />);

    const retryButton = screen.getByRole("button", { name: /retry/i });
    fireEvent.click(retryButton);

    expect(mockOnRetry).toHaveBeenCalledTimes(1);
  });

  it("calls onDismiss when dismiss button clicked", () => {
    const error = new Error("Test error");
    render(<ChatErrorDisplay error={error} onDismiss={mockOnDismiss} />);

    const dismissButton = screen.getByLabelText(/dismiss error/i);
    fireEvent.click(dismissButton);

    expect(mockOnDismiss).toHaveBeenCalledTimes(1);
  });

  it("displays correct icon for UNAUTHORIZED error", () => {
    const error = new ApiException(
      { error: "Unauthorized", code: "UNAUTHORIZED", status: 401 },
      401
    );
    render(<ChatErrorDisplay error={error} />);

    const icon = screen.getByText("🔒");
    expect(icon).toBeInTheDocument();
  });

  it("displays correct icon for FORBIDDEN error", () => {
    const error = new ApiException(
      { error: "Forbidden", code: "FORBIDDEN", status: 403 },
      403
    );
    render(<ChatErrorDisplay error={error} />);

    const icon = screen.getByText("⛔");
    expect(icon).toBeInTheDocument();
  });

  it("displays correct icon for NOT_FOUND error", () => {
    const error = new ApiException(
      { error: "Not found", code: "NOT_FOUND", status: 404 },
      404
    );
    render(<ChatErrorDisplay error={error} />);

    const icon = screen.getByText("🔍");
    expect(icon).toBeInTheDocument();
  });

  it("displays generic error icon for unknown errors", () => {
    const error = new Error("Unknown error");
    render(<ChatErrorDisplay error={error} />);

    const icon = screen.getByText("❌");
    expect(icon).toBeInTheDocument();
  });

  it("has correct styling classes", () => {
    const error = new Error("Test error");
    const { container } = render(<ChatErrorDisplay error={error} />);

    const errorContainer = container.firstChild;
    expect(errorContainer).toHaveClass("bg-red-50");
    expect(errorContainer).toHaveClass("border-red-200");
  });

  it("displays custom error message from ApiException", () => {
    const error = new ApiException(
      { error: "Custom error message", code: "CUSTOM_ERROR", status: 400 },
      400
    );
    render(<ChatErrorDisplay error={error} />);

    const message = screen.getByText(/custom error message/i);
    expect(message).toBeInTheDocument();
  });
});
