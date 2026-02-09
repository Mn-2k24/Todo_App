/**
 * MessageList Component
 *
 * Displays conversation history with:
 * - User messages (right-aligned, blue background)
 * - Assistant messages (left-aligned, gray background)
 * - Tool call results (collapsible, shown below assistant messages)
 * - Auto-scroll to bottom on new messages
 * - Loading indicator for in-progress messages
 */

"use client";

import { useEffect, useRef } from "react";
import { ChatMessage } from "@/lib/api/chat";
import ToolCallDisplay from "./ToolCallDisplay";

interface MessageListProps {
  messages: ChatMessage[];
  isLoading?: boolean;
}

export default function MessageList({ messages, isLoading }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return null; // EmptyState will be shown by parent
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${
            message.role === "user" ? "justify-end" : "justify-start"
          }`}
        >
          <div
            className={`max-w-[80%] rounded-lg px-4 py-3 ${
              message.role === "user"
                ? "bg-blue-600 text-white"
                : "bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100"
            }`}
          >
            {/* Message content */}
            <div className="whitespace-pre-wrap break-words">
              {message.content}
            </div>

            {/* Tool calls (only for assistant messages) */}
            {message.role === "assistant" && message.tool_calls && message.tool_calls.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-300 dark:border-gray-600">
                <ToolCallDisplay toolCalls={message.tool_calls} />
              </div>
            )}

            {/* Timestamp */}
            <div
              className={`text-xs mt-2 ${
                message.role === "user"
                  ? "text-blue-200"
                  : "text-gray-500 dark:text-gray-400"
              }`}
            >
              {new Date(message.created_at).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </div>
          </div>
        </div>
      ))}

      {/* Loading indicator */}
      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-3 max-w-[80%]">
            <div className="flex items-center space-x-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
              </div>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                AI is thinking...
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  );
}
