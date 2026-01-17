"use client";

/**
 * TaskItem component - Display single task with actions.
 * Per FR-041: Loading states for all operations.
 */

import { useState } from "react";
import type { Task } from "@/types/task";
import { Priority } from "@/types/task";
import Button from "@/components/ui/Button";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

interface TaskItemProps {
  task: Task;
  onToggle: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => Promise<void>;
  className?: string;
}

/**
 * Get priority badge styles per FR-020 (visual distinction).
 */
function getPriorityBadgeClass(priority: Priority): string {
  switch (priority) {
    case Priority.HIGH:
      return "badge badge-high";
    case Priority.MEDIUM:
      return "badge badge-medium";
    case Priority.LOW:
      return "badge badge-low";
    default:
      return "badge";
  }
}

/**
 * Check if task is overdue per FR-025.
 */
function isTaskOverdue(dueDate: string | null | undefined): boolean {
  if (!dueDate) return false;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const due = new Date(dueDate);
  due.setHours(0, 0, 0, 0);
  return due < today;
}

/**
 * Format due date for display.
 */
function formatDueDate(dueDate: string): string {
  const date = new Date(dueDate);
  return date.toLocaleDateString();
}

export default function TaskItem({
  task,
  onToggle,
  onEdit,
  onDelete,
  className = "",
}: TaskItemProps) {
  const [toggleLoading, setToggleLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const handleToggle = async () => {
    setToggleLoading(true);
    try {
      await onToggle(task.id);
    } finally {
      setToggleLoading(false);
    }
  };

  const handleDelete = async () => {
    setDeleteLoading(true);
    try {
      await onDelete(task.id);
    } finally {
      setDeleteLoading(false);
    }
  };

  const isLoading = toggleLoading || deleteLoading;
  const isOverdue = isTaskOverdue(task.due_date);

  return (
    <div
      className={`
        flex items-start gap-4 p-4 rounded-lg border border-gray-200 bg-white
        hover:shadow-sm transition-shadow duration-200
        ${isLoading ? "opacity-50" : ""}
        ${className}
      `}
    >
      {/* Completion checkbox */}
      <div className="flex-shrink-0 pt-1">
        {toggleLoading ? (
          <LoadingSpinner size="sm" />
        ) : (
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggle}
            className="h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
            disabled={isLoading}
            aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          />
        )}
      </div>

      {/* Task description */}
      <div className="flex-1 min-w-0">
        <p
          className={`
            text-base break-words
            ${task.completed ? "line-through text-gray-500" : "text-gray-900"}
          `}
        >
          {task.description}
        </p>
        <div className="mt-2 flex items-center gap-2 flex-wrap">
          <span className={getPriorityBadgeClass(task.priority)}>
            {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
          </span>
          {task.tags && task.tags.length > 0 && (
            <>
              {task.tags.map((tag) => (
                <span key={tag} className="badge badge-default">
                  {tag}
                </span>
              ))}
            </>
          )}
          {task.due_date && (
            <span className={`text-xs font-medium ${isOverdue ? "text-error-600" : "text-gray-700"}`}>
              {isOverdue && (
                <svg
                  className="inline h-4 w-4 mr-1"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  aria-label="Overdue"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
              Due: {formatDueDate(task.due_date)}
            </span>
          )}
          <span className="text-xs text-gray-500">
            Created {new Date(task.created_at).toLocaleDateString()}
          </span>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex-shrink-0 flex items-center gap-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onEdit(task)}
          disabled={isLoading}
          aria-label="Edit task"
        >
          <svg
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
            />
          </svg>
        </Button>

        <Button
          variant="ghost"
          size="sm"
          onClick={handleDelete}
          disabled={isLoading}
          loading={deleteLoading}
          aria-label="Delete task"
          className="text-error-600 hover:bg-error-50"
        >
          {!deleteLoading && (
            <svg
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          )}
        </Button>
      </div>
    </div>
  );
}
