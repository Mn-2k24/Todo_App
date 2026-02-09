/**
 * ToolCallDisplay Component
 *
 * Displays MCP tool execution results in a collapsible, formatted view.
 * Shows:
 * - Tool name (e.g., "add_task", "list_tasks")
 * - Parameters passed to the tool
 * - Execution result (success/failure, returned data)
 */

"use client";

import { useState } from "react";
import { ToolCall } from "@/lib/api/chat";

interface ToolCallDisplayProps {
  toolCalls: ToolCall[];
}

export default function ToolCallDisplay({ toolCalls }: ToolCallDisplayProps) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  const toggleExpand = (index: number) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  const formatToolName = (toolName: string): string => {
    return toolName
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  const getToolIcon = (toolName: string): string => {
    const iconMap: Record<string, string> = {
      add_task: "➕",
      list_tasks: "📋",
      update_task: "✏️",
      complete_task: "✅",
      delete_task: "🗑️",
    };
    return iconMap[toolName] || "🔧";
  };

  const isSuccess = (result: Record<string, unknown>): boolean => {
    return result.success === true || !("error" in result);
  };

  return (
    <div className="space-y-2">
      <div className="text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide">
        Actions Performed
      </div>

      {toolCalls.map((toolCall, index) => {
        const success = isSuccess(toolCall.result);
        const isExpanded = expandedIndex === index;

        return (
          <div
            key={index}
            className="bg-white dark:bg-gray-700 rounded border border-gray-200 dark:border-gray-600 overflow-hidden"
          >
            {/* Tool header (clickable) */}
            <button
              onClick={() => toggleExpand(index)}
              className="w-full px-3 py-2 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
            >
              <div className="flex items-center space-x-2">
                <span className="text-lg">{getToolIcon(toolCall.tool_name)}</span>
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {formatToolName(toolCall.tool_name)}
                </span>
                {success ? (
                  <span className="text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-2 py-0.5 rounded">
                    Success
                  </span>
                ) : (
                  <span className="text-xs bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 px-2 py-0.5 rounded">
                    Failed
                  </span>
                )}
              </div>
              <svg
                className={`w-4 h-4 text-gray-500 transition-transform ${
                  isExpanded ? "rotate-180" : ""
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            {/* Tool details (expandable) - User-friendly display only */}
            {isExpanded && (
              <div className="px-3 py-2 border-t border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-800">
                <div className="text-xs text-gray-600 dark:text-gray-400">
                  {success ? (
                    <span className="text-green-600 dark:text-green-400">
                      ✓ Operation completed successfully
                    </span>
                  ) : (
                    <span className="text-red-600 dark:text-red-400">
                      ✗ Operation failed: {toolCall.result.message || "Unknown error"}
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
