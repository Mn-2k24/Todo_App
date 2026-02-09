/**
 * ChatEmptyState Component
 *
 * Shown when conversation is empty (no messages yet).
 * Displays:
 * - Welcome message
 * - Sample prompts user can click to get started
 * - Brief explanation of AI assistant capabilities
 */

"use client";

interface ChatEmptyStateProps {
  onPromptClick: (prompt: string) => void;
}

const SAMPLE_PROMPTS = [
  "Add a task to buy groceries tomorrow",
  "Show me all my pending tasks",
  "Mark the first task as completed",
  "Set task 'Buy groceries' to high priority",
  "List all high priority tasks",
  "Delete completed tasks",
];

export default function ChatEmptyState({ onPromptClick }: ChatEmptyStateProps) {
  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl text-center space-y-6">
        {/* Icon */}
        <div className="flex justify-center">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <svg
              className="w-10 h-10 text-white"
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
        </div>

        {/* Welcome message */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            Welcome to AI Task Assistant
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your tasks using natural language. Just tell me what you want to do!
          </p>
        </div>

        {/* Capabilities */}
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-left">
          <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
            I can help you:
          </h3>
          <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300">
            <li className="flex items-start space-x-2">
              <span className="text-green-500 mt-0.5">✓</span>
              <span><strong>Create tasks</strong> with titles, priorities, due dates, and tags</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-green-500 mt-0.5">✓</span>
              <span><strong>List and filter</strong> tasks by status, priority, or tags</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-green-500 mt-0.5">✓</span>
              <span><strong>Update tasks</strong> - change titles, priorities, or due dates</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-green-500 mt-0.5">✓</span>
              <span><strong>Mark tasks complete</strong> or delete them</span>
            </li>
          </ul>
        </div>

        {/* Sample prompts */}
        <div>
          <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-3">
            Try these examples:
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {SAMPLE_PROMPTS.map((prompt, index) => (
              <button
                key={index}
                onClick={() => onPromptClick(prompt)}
                className="px-4 py-3 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-sm text-left hover:bg-blue-50 dark:hover:bg-gray-600 hover:border-blue-300 dark:hover:border-blue-500 transition-colors text-gray-700 dark:text-gray-300"
              >
                &ldquo;{prompt}&rdquo;
              </button>
            ))}
          </div>
        </div>

        {/* Tip */}
        <div className="text-xs text-gray-500 dark:text-gray-400 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
          <strong>💡 Tip:</strong> You can reference tasks by position (e.g., &ldquo;mark the first task as done&rdquo;) or by title.
        </div>
      </div>
    </div>
  );
}
