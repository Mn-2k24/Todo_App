/**
 * Integration tests for Chat Page
 *
 * Tests:
 * - Redirects to login when not authenticated
 * - Loads and displays empty state for new conversation
 * - Sends message and displays user message immediately (optimistic update)
 * - Displays assistant response after API call
 * - Displays tool execution results
 * - Handles error states (401, 403, 404, 500)
 * - Handles multi-turn conversations
 * - New conversation button clears messages
 */

import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import { useRouter } from "next/navigation";
import ChatPage from "../page";
import * as authModule from "@/lib/auth";
import * as chatApiModule from "@/lib/api/chat";

// Mock Next.js router
jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));

// Mock auth module
jest.mock("@/lib/auth");

// Mock chat API module
jest.mock("@/lib/api/chat");

describe("ChatPage Integration Tests", () => {
  const mockPush = jest.fn();
  const mockGetCurrentUser = authModule.getCurrentUser as jest.MockedFunction<
    typeof authModule.getCurrentUser
  >;
  const mockSendChatMessage = chatApiModule.sendChatMessage as jest.MockedFunction<
    typeof chatApiModule.sendChatMessage
  >;

  beforeEach(() => {
    jest.clearAllMocks();
    (useRouter as jest.Mock).mockReturnValue({ push: mockPush });
  });

  it("redirects to login when not authenticated", async () => {
    mockGetCurrentUser.mockResolvedValue(null);

    render(<ChatPage />);

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/login");
    });
  });

  it("displays loading state while checking authentication", () => {
    mockGetCurrentUser.mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<ChatPage />);

    const loadingText = screen.getByText(/loading/i);
    expect(loadingText).toBeInTheDocument();
  });

  it("loads authenticated user and displays empty state", async () => {
    mockGetCurrentUser.mockResolvedValue({
      id: "user-123",
      email: "test@example.com",
      created_at: "2026-01-27T10:00:00Z",
    });

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByText(/welcome to ai task assistant/i)).toBeInTheDocument();
    });

    // Check for sample prompts
    const samplePrompt = screen.getByText(/add a task to buy groceries/i);
    expect(samplePrompt).toBeInTheDocument();
  });

  it("sends message and displays user message immediately", async () => {
    const user = userEvent.setup();
    mockGetCurrentUser.mockResolvedValue({
      id: "user-123",
      email: "test@example.com",
      created_at: "2026-01-27T10:00:00Z",
    });

    mockSendChatMessage.mockResolvedValue({
      conversation_id: "conv-123",
      message_id: "msg-456",
      response: "I've added the task for you.",
      tool_calls: [],
      created_at: "2026-01-27T10:00:05Z",
    });

    render(<ChatPage />);

    // Wait for empty state
    await waitFor(() => {
      expect(screen.getByText(/welcome to ai task assistant/i)).toBeInTheDocument();
    });

    // Type message
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, "Add a task to buy groceries");

    // Send message
    const sendButton = screen.getByRole("button", { name: /send/i });
    await user.click(sendButton);

    // User message should appear immediately (optimistic update)
    await waitFor(() => {
      expect(screen.getByText("Add a task to buy groceries")).toBeInTheDocument();
    });

    // API should be called
    expect(mockSendChatMessage).toHaveBeenCalledWith(
      "user-123",
      "Add a task to buy groceries",
      null
    );
  });

  it("displays assistant response after API call", async () => {
    const user = userEvent.setup();
    mockGetCurrentUser.mockResolvedValue({
      id: "user-123",
      email: "test@example.com",
      created_at: "2026-01-27T10:00:00Z",
    });

    mockSendChatMessage.mockResolvedValue({
      conversation_id: "conv-123",
      message_id: "msg-456",
      response: "I've added the task 'Buy groceries'.",
      tool_calls: [
        {
          tool_name: "add_task",
          parameters: { title: "Buy groceries" },
          result: { success: true, task: { id: 1 } },
        },
      ],
      created_at: "2026-01-27T10:00:05Z",
    });

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    });

    // Type and send message
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, "Add a task");
    const sendButton = screen.getByRole("button", { name: /send/i });
    await user.click(sendButton);

    // Wait for assistant response
    await waitFor(() => {
      expect(screen.getByText(/I've added the task 'Buy groceries'/i)).toBeInTheDocument();
    });

    // Tool calls should be displayed
    const toolCallsSection = screen.getByText(/actions performed/i);
    expect(toolCallsSection).toBeInTheDocument();
  });

  it("handles error responses and shows error display", async () => {
    const user = userEvent.setup();
    mockGetCurrentUser.mockResolvedValue({
      id: "user-123",
      email: "test@example.com",
      created_at: "2026-01-27T10:00:00Z",
    });

    const mockError = new Error("Network error");
    mockSendChatMessage.mockRejectedValue(mockError);

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    });

    // Type and send message
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, "Test message");
    const sendButton = screen.getByRole("button", { name: /send/i });
    await user.click(sendButton);

    // Wait for error display
    await waitFor(() => {
      expect(screen.getByText(/network error/i)).toBeInTheDocument();
    });

    // User message should be removed (optimistic update rollback)
    expect(screen.queryByText("Test message")).not.toBeInTheDocument();
  });

  it("handles 401 error and redirects to login", async () => {
    const user = userEvent.setup();
    mockGetCurrentUser.mockResolvedValue({
      id: "user-123",
      email: "test@example.com",
      created_at: "2026-01-27T10:00:00Z",
    });

    const mockError = {
      name: "ApiException",
      message: "Unauthorized",
      error: { error: "Unauthorized", code: "UNAUTHORIZED", status: 401 },
      status: 401,
    };
    mockSendChatMessage.mockRejectedValue(mockError);

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, "Test");
    const sendButton = screen.getByRole("button", { name: /send/i });
    await user.click(sendButton);

    // Should redirect to login
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/login");
    });
  });

  it("handles multi-turn conversations", async () => {
    const user = userEvent.setup();
    mockGetCurrentUser.mockResolvedValue({
      id: "user-123",
      email: "test@example.com",
      created_at: "2026-01-27T10:00:00Z",
    });

    // First message
    mockSendChatMessage.mockResolvedValueOnce({
      conversation_id: "conv-123",
      message_id: "msg-1",
      response: "Task added.",
      tool_calls: [],
      created_at: "2026-01-27T10:00:05Z",
    });

    // Second message
    mockSendChatMessage.mockResolvedValueOnce({
      conversation_id: "conv-123",
      message_id: "msg-2",
      response: "Here are your tasks.",
      tool_calls: [],
      created_at: "2026-01-27T10:00:10Z",
    });

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText(/type your message/i);

    // First message
    await user.type(input, "Add task");
    await user.click(screen.getByRole("button", { name: /send/i }));

    await waitFor(() => {
      expect(screen.getByText("Task added.")).toBeInTheDocument();
    });

    // Second message (should include conversation_id)
    await user.type(input, "List tasks");
    await user.click(screen.getByRole("button", { name: /send/i }));

    await waitFor(() => {
      expect(screen.getByText("Here are your tasks.")).toBeInTheDocument();
    });

    // Verify second call included conversation_id
    expect(mockSendChatMessage).toHaveBeenLastCalledWith(
      "user-123",
      "List tasks",
      "conv-123"
    );
  });

  it("new conversation button clears messages", async () => {
    const user = userEvent.setup();
    mockGetCurrentUser.mockResolvedValue({
      id: "user-123",
      email: "test@example.com",
      created_at: "2026-01-27T10:00:00Z",
    });

    mockSendChatMessage.mockResolvedValue({
      conversation_id: "conv-123",
      message_id: "msg-1",
      response: "Response",
      tool_calls: [],
      created_at: "2026-01-27T10:00:05Z",
    });

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    });

    // Send a message
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, "Test");
    await user.click(screen.getByRole("button", { name: /send/i }));

    await waitFor(() => {
      expect(screen.getByText("Response")).toBeInTheDocument();
    });

    // Click new conversation button
    const newConversationButton = screen.getByRole("button", {
      name: /new conversation/i,
    });
    await user.click(newConversationButton);

    // Messages should be cleared, empty state shown
    await waitFor(() => {
      expect(screen.getByText(/welcome to ai task assistant/i)).toBeInTheDocument();
    });

    expect(screen.queryByText("Response")).not.toBeInTheDocument();
  });

  it("clicking sample prompt sends message", async () => {
    const user = userEvent.setup();
    mockGetCurrentUser.mockResolvedValue({
      id: "user-123",
      email: "test@example.com",
      created_at: "2026-01-27T10:00:00Z",
    });

    mockSendChatMessage.mockResolvedValue({
      conversation_id: "conv-123",
      message_id: "msg-1",
      response: "Task added.",
      tool_calls: [],
      created_at: "2026-01-27T10:00:05Z",
    });

    render(<ChatPage />);

    await waitFor(() => {
      expect(screen.getByText(/welcome to ai task assistant/i)).toBeInTheDocument();
    });

    // Click sample prompt
    const samplePrompt = screen.getByText(/add a task to buy groceries tomorrow/i);
    await user.click(samplePrompt);

    // Should send the prompt
    expect(mockSendChatMessage).toHaveBeenCalledWith(
      "user-123",
      "Add a task to buy groceries tomorrow",
      null
    );
  });
});
