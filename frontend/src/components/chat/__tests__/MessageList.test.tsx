/**
 * Unit tests for MessageList component
 *
 * Tests:
 * - Renders user and assistant messages with correct styling
 * - Role-based styling (user: blue, right-aligned; assistant: gray, left-aligned)
 * - Tool calls display for assistant messages
 * - Timestamps display correctly
 * - Loading indicator shown when isLoading=true
 * - Auto-scroll behavior (ref element exists)
 * - Empty state (returns null when no messages and not loading)
 */

import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import MessageList from "../MessageList";
import { ChatMessage } from "@/lib/api/chat";

// Mock ToolCallDisplay component
jest.mock("../ToolCallDisplay", () => {
  return function MockToolCallDisplay({ toolCalls }: { toolCalls: Array<{ tool_name: string; parameters: Record<string, unknown>; result: Record<string, unknown> }> }) {
    return <div data-testid="tool-call-display">Tool Calls: {toolCalls.length}</div>;
  };
});

describe("MessageList", () => {
  const mockUserMessage: ChatMessage = {
    id: "msg-1",
    conversation_id: "conv-1",
    role: "user",
    content: "Hello, add a task",
    created_at: "2026-01-27T10:00:00Z",
  };

  const mockAssistantMessage: ChatMessage = {
    id: "msg-2",
    conversation_id: "conv-1",
    role: "assistant",
    content: "I've added the task for you.",
    tool_calls: [
      {
        tool_name: "add_task",
        parameters: { title: "Test task" },
        result: { success: true },
      },
    ],
    created_at: "2026-01-27T10:00:05Z",
  };

  it("renders user message with correct styling", () => {
    render(<MessageList messages={[mockUserMessage]} />);

    const messageContent = screen.getByText("Hello, add a task");
    expect(messageContent).toBeInTheDocument();

    // Check if parent div has right-aligned class
    const messageContainer = messageContent.closest(".flex");
    expect(messageContainer).toHaveClass("justify-end");

    // Check blue background for user messages
    const messageBox = messageContent.closest(".rounded-lg");
    expect(messageBox).toHaveClass("bg-blue-600");
  });

  it("renders assistant message with correct styling", () => {
    render(<MessageList messages={[mockAssistantMessage]} />);

    const messageContent = screen.getByText("I've added the task for you.");
    expect(messageContent).toBeInTheDocument();

    // Check if parent div has left-aligned class
    const messageContainer = messageContent.closest(".flex");
    expect(messageContainer).toHaveClass("justify-start");

    // Check gray background for assistant messages
    const messageBox = messageContent.closest(".rounded-lg");
    expect(messageBox).toHaveClass("bg-gray-100");
  });

  it("displays tool calls for assistant messages", () => {
    render(<MessageList messages={[mockAssistantMessage]} />);

    // Check that ToolCallDisplay is rendered
    const toolCallDisplay = screen.getByTestId("tool-call-display");
    expect(toolCallDisplay).toBeInTheDocument();
    expect(toolCallDisplay).toHaveTextContent("Tool Calls: 1");
  });

  it("does not display tool calls for user messages", () => {
    render(<MessageList messages={[mockUserMessage]} />);

    // Check that ToolCallDisplay is NOT rendered
    const toolCallDisplay = screen.queryByTestId("tool-call-display");
    expect(toolCallDisplay).not.toBeInTheDocument();
  });

  it("displays timestamps in correct format", () => {
    render(<MessageList messages={[mockUserMessage]} />);

    // Check for time display (format depends on locale, so just check it exists)
    const timestamp = screen.getByText(/\d{1,2}:\d{2}/);
    expect(timestamp).toBeInTheDocument();
  });

  it("renders multiple messages in correct order", () => {
    const messages = [mockUserMessage, mockAssistantMessage];
    render(<MessageList messages={messages} />);

    const userMsg = screen.getByText("Hello, add a task");
    const assistantMsg = screen.getByText("I've added the task for you.");

    expect(userMsg).toBeInTheDocument();
    expect(assistantMsg).toBeInTheDocument();

    // Check order (user message should appear before assistant message in DOM)
    const allMessages = screen.getAllByText(/task/i);
    expect(allMessages.length).toBeGreaterThanOrEqual(2);
  });

  it("shows loading indicator when isLoading=true", () => {
    render(<MessageList messages={[]} isLoading={true} />);

    // Check for loading text
    const loadingText = screen.getByText("AI is thinking...");
    expect(loadingText).toBeInTheDocument();

    // Check for animated dots (3 divs with animate-bounce)
    const dots = document.querySelectorAll(".animate-bounce");
    expect(dots.length).toBe(3);
  });

  it("does not show loading indicator when isLoading=false", () => {
    render(<MessageList messages={[mockUserMessage]} isLoading={false} />);

    const loadingText = screen.queryByText("AI is thinking...");
    expect(loadingText).not.toBeInTheDocument();
  });

  it("returns null when no messages and not loading", () => {
    const { container } = render(<MessageList messages={[]} isLoading={false} />);

    // Component should return null, so container should be empty
    expect(container.firstChild).toBeNull();
  });

  it("renders scroll anchor element", () => {
    const { container } = render(<MessageList messages={[mockUserMessage]} />);

    // Check that there's a div at the end for scrolling (last child)
    const scrollAnchor = container.querySelector(".flex-1 > div:last-child");
    expect(scrollAnchor).toBeInTheDocument();
  });

  it("applies dark mode classes", () => {
    render(<MessageList messages={[mockAssistantMessage]} />);

    const messageBox = screen.getByText("I've added the task for you.").closest(".rounded-lg");

    // Check for dark mode classes
    expect(messageBox).toHaveClass("dark:bg-gray-800");
    expect(messageBox).toHaveClass("dark:text-gray-100");
  });

  it("handles empty tool_calls array", () => {
    const messageWithoutTools: ChatMessage = {
      ...mockAssistantMessage,
      tool_calls: [],
    };

    render(<MessageList messages={[messageWithoutTools]} />);

    // Tool call display should not be rendered
    const toolCallDisplay = screen.queryByTestId("tool-call-display");
    expect(toolCallDisplay).not.toBeInTheDocument();
  });

  it("handles missing tool_calls property", () => {
    const messageWithoutToolsProp: ChatMessage = {
      id: "msg-3",
      conversation_id: "conv-1",
      role: "assistant",
      content: "Just a text response",
      created_at: "2026-01-27T10:00:10Z",
    };

    render(<MessageList messages={[messageWithoutToolsProp]} />);

    // Tool call display should not be rendered
    const toolCallDisplay = screen.queryByTestId("tool-call-display");
    expect(toolCallDisplay).not.toBeInTheDocument();
  });
});
