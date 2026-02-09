"use client";

/**
 * Chat Page - AI-powered natural language task management interface.
 *
 * Phase III: Provides conversational interface to manage tasks using AI.
 * Features:
 * - Natural language input (e.g., "Add a task to buy groceries tomorrow")
 * - AI-powered intent recognition and entity extraction
 * - Automatic MCP tool execution (add_task, list_tasks, update_task, etc.)
 * - Conversation history persistence across sessions
 * - Real-time tool execution feedback
 */

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { getCurrentUser } from "@/lib/auth";
import { ApiException } from "@/lib/api";
import {
  sendChatMessage,
  chatResponseToMessage,
  createUserMessage,
  ChatMessage,
} from "@/lib/api/chat";
import MessageList from "@/components/chat/MessageList";
import MessageInput from "@/components/chat/MessageInput";
import ChatEmptyState from "@/components/chat/ChatEmptyState";
import ChatErrorDisplay from "@/components/chat/ChatErrorDisplay";

export default function ChatPage() {
  const router = useRouter();

  // Authentication state
  const [userId, setUserId] = useState<string | null>(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Conversation state
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // UI state
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | ApiException | null>(null);

  // Check authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const currentUser = await getCurrentUser();
        if (!currentUser) {
          // Not authenticated - redirect to login
          router.push("/login");
          return;
        }

        setUserId(currentUser.id);
        setAuthLoading(false);
      } catch (err) {
        console.error("Auth check failed:", err);
        router.push("/login");
      }
    };

    checkAuth();
  }, [router]);

  // Handle sending a message
  const handleSendMessage = useCallback(
    async (messageText: string) => {
      if (!userId) {
        setError(new Error("Not authenticated"));
        return;
      }

      // Clear previous error
      setError(null);

      // Optimistic UI update: Add user message immediately
      const userMessage = createUserMessage(messageText, conversationId || undefined);
      setMessages((prev) => [...prev, userMessage]);

      // Set loading state
      setIsLoading(true);

      try {
        // Send message to backend
        const response = await sendChatMessage(userId, messageText, conversationId);

        // Update conversation ID if this is first message
        if (!conversationId) {
          setConversationId(response.conversation_id);
        }

        // Add assistant response to messages
        const assistantMessage = chatResponseToMessage(response);
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        console.error("Error sending message:", err);
        setError(err as Error | ApiException);

        // Remove optimistic user message on error
        setMessages((prev) => prev.filter((msg) => msg.id !== userMessage.id));

        // Handle 401 - redirect to login
        if (err instanceof ApiException && err.status === 401) {
          router.push("/login");
        }
      } finally {
        setIsLoading(false);
      }
    },
    [userId, conversationId, router]
  );

  // Handle sample prompt click
  const handlePromptClick = useCallback(
    (prompt: string) => {
      handleSendMessage(prompt);
    },
    [handleSendMessage]
  );

  // Handle error retry
  const handleRetry = useCallback(() => {
    setError(null);
  }, []);

  // Handle error dismiss
  const handleDismiss = useCallback(() => {
    setError(null);
  }, []);

  // Show loading state while checking authentication
  if (authLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                AI Task Assistant
              </h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Manage tasks with natural language
              </p>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex items-center space-x-4">
            <button
              onClick={() => router.push("/dashboard")}
              className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
            >
              ← Back to Dashboard
            </button>

            {/* New conversation button */}
            {messages.length > 0 && (
              <button
                onClick={() => {
                  setMessages([]);
                  setConversationId(null);
                  setError(null);
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                New Conversation
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Error display */}
      {error && (
        <ChatErrorDisplay
          error={error}
          onRetry={handleRetry}
          onDismiss={handleDismiss}
        />
      )}

      {/* Messages area */}
      <div className="flex-1 flex flex-col min-h-0 bg-white dark:bg-gray-800">
        {messages.length === 0 && !isLoading ? (
          <ChatEmptyState onPromptClick={handlePromptClick} />
        ) : (
          <MessageList messages={messages} isLoading={isLoading} />
        )}
      </div>

      {/* Input area */}
      <MessageInput onSend={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}
