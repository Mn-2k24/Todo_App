/**
 * Unit tests for MessageInput component
 *
 * Tests:
 * - Text input renders and accepts input
 * - Send button calls onSend with trimmed message
 * - Send button disabled when message is empty or loading
 * - Enter key sends message (without Shift)
 * - Shift+Enter adds new line without sending
 * - Character counter shown when approaching limit
 * - Send button disabled when over character limit
 * - Placeholder text displayed
 * - Help text for keyboard shortcuts displayed
 */

import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import MessageInput from "../MessageInput";

describe("MessageInput", () => {
  const mockOnSend = jest.fn();

  beforeEach(() => {
    mockOnSend.mockClear();
  });

  it("renders textarea and send button", () => {
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);
    expect(textarea).toBeInTheDocument();

    const sendButton = screen.getByRole("button", { name: /send/i });
    expect(sendButton).toBeInTheDocument();
  });

  it("allows typing in textarea", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i) as HTMLTextAreaElement;
    await user.type(textarea, "Test message");

    expect(textarea.value).toBe("Test message");
  });

  it("calls onSend when send button clicked with valid message", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);
    const sendButton = screen.getByRole("button", { name: /send/i });

    await user.type(textarea, "Test message");
    await user.click(sendButton);

    expect(mockOnSend).toHaveBeenCalledTimes(1);
    expect(mockOnSend).toHaveBeenCalledWith("Test message");
  });

  it("trims whitespace when sending message", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);
    const sendButton = screen.getByRole("button", { name: /send/i });

    await user.type(textarea, "  Test message  ");
    await user.click(sendButton);

    expect(mockOnSend).toHaveBeenCalledWith("Test message");
  });

  it("clears textarea after sending message", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i) as HTMLTextAreaElement;
    const sendButton = screen.getByRole("button", { name: /send/i });

    await user.type(textarea, "Test message");
    await user.click(sendButton);

    expect(textarea.value).toBe("");
  });

  it("disables send button when message is empty", () => {
    render(<MessageInput onSend={mockOnSend} />);

    const sendButton = screen.getByRole("button", { name: /send/i });
    expect(sendButton).toBeDisabled();
  });

  it("disables send button when message is only whitespace", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);
    const sendButton = screen.getByRole("button", { name: /send/i });

    await user.type(textarea, "   ");

    expect(sendButton).toBeDisabled();
  });

  it("disables send button when isLoading=true", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} isLoading={true} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);
    const sendButton = screen.getByRole("button", { name: /sending/i });

    await user.type(textarea, "Test message");

    expect(sendButton).toBeDisabled();
  });

  it("shows loading state when isLoading=true", () => {
    render(<MessageInput onSend={mockOnSend} isLoading={true} />);

    const sendButton = screen.getByRole("button", { name: /sending/i });
    expect(sendButton).toBeInTheDocument();

    // Check for spinner
    const spinner = sendButton.querySelector(".animate-spin");
    expect(spinner).toBeInTheDocument();
  });

  it("sends message when Enter key pressed (without Shift)", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);

    await user.type(textarea, "Test message");
    await user.keyboard("{Enter}");

    expect(mockOnSend).toHaveBeenCalledWith("Test message");
  });

  it("does NOT send message when Shift+Enter pressed", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i) as HTMLTextAreaElement;

    await user.type(textarea, "Line 1");
    await user.keyboard("{Shift>}{Enter}{/Shift}");
    await user.type(textarea, "Line 2");

    // Should not have called onSend
    expect(mockOnSend).not.toHaveBeenCalled();

    // Textarea should contain newline
    expect(textarea.value).toContain("\n");
  });

  it("displays character counter when approaching limit", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);

    // Type 1950 characters (within 100 of limit)
    const longMessage = "a".repeat(1950);
    await user.type(textarea, longMessage);

    const counter = screen.getByText(/50 chars remaining/i);
    expect(counter).toBeInTheDocument();
  });

  it("shows warning color when over limit", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);

    // Type 2050 characters (over limit)
    const tooLongMessage = "a".repeat(2050);
    await user.type(textarea, tooLongMessage);

    const counter = screen.getByText(/-50 chars remaining/i);
    expect(counter).toBeInTheDocument();
    expect(counter).toHaveClass("text-red-600");
  });

  it("disables send button when over character limit", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);
    const sendButton = screen.getByRole("button", { name: /send/i });

    // Type 2050 characters (over limit)
    const tooLongMessage = "a".repeat(2050);
    await user.type(textarea, tooLongMessage);

    expect(sendButton).toBeDisabled();
  });

  it("displays custom placeholder", () => {
    render(<MessageInput onSend={mockOnSend} placeholder="Custom placeholder" />);

    const textarea = screen.getByPlaceholderText("Custom placeholder");
    expect(textarea).toBeInTheDocument();
  });

  it("displays keyboard shortcut help text", () => {
    render(<MessageInput onSend={mockOnSend} />);

    const helpText = screen.getByText(/Enter.*to send/i);
    expect(helpText).toBeInTheDocument();

    const shiftEnterText = screen.getByText(/Shift\+Enter.*new line/i);
    expect(shiftEnterText).toBeInTheDocument();
  });

  it("disables textarea when isLoading=true", () => {
    render(<MessageInput onSend={mockOnSend} isLoading={true} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);
    expect(textarea).toBeDisabled();
  });

  it("does not call onSend when clicking send with empty message", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const sendButton = screen.getByRole("button", { name: /send/i });

    // Button should be disabled, but try clicking anyway
    await user.click(sendButton);

    expect(mockOnSend).not.toHaveBeenCalled();
  });

  it("handles rapid Enter key presses gracefully", async () => {
    const user = userEvent.setup();
    render(<MessageInput onSend={mockOnSend} />);

    const textarea = screen.getByPlaceholderText(/Type your message/i);

    await user.type(textarea, "Test");
    await user.keyboard("{Enter}");
    await user.keyboard("{Enter}"); // Second Enter on empty textarea

    // Should only send once (second Enter has no message)
    expect(mockOnSend).toHaveBeenCalledTimes(1);
  });
});
