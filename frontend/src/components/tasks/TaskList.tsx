"use client";

/**
 * TaskList component - Render list of tasks with states.
 * Per FR-041: Loading states, FR-042: Error states, FR-043: Empty states.
 */

import type { Task } from "@/types/task";
import TaskItem from "./TaskItem";
import EmptyState from "@/components/ui/EmptyState";
import ErrorMessage from "@/components/ui/ErrorMessage";
import { LoadingPage } from "@/components/ui/LoadingSpinner";

interface TaskListProps {
  tasks: Task[];
  loading?: boolean;
  error?: unknown;
  onToggle: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => Promise<void>;
  hasActiveFilters?: boolean;
  className?: string;
}

export default function TaskList({
  tasks,
  loading = false,
  error = null,
  onToggle,
  onEdit,
  onDelete,
  hasActiveFilters = false,
  className = "",
}: TaskListProps) {
  // Loading state
  if (loading) {
    return <LoadingPage />;
  }

  // Error state
  if (error) {
    return (
      <div className={className}>
        <ErrorMessage error={error} />
      </div>
    );
  }

  // Empty state - different message for filtered results vs no tasks (FR-031)
  if (tasks.length === 0) {
    return (
      <div className={className}>
        <EmptyState
          icon={
            hasActiveFilters ? (
              <svg
                className="h-16 w-16"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            ) : (
              <svg
                className="h-16 w-16"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
            )
          }
          title={hasActiveFilters ? "No tasks match your filters" : "No tasks yet"}
          message={
            hasActiveFilters
              ? "Try adjusting your filters or search criteria to find tasks."
              : "Get started by creating your first task above."
          }
        />
      </div>
    );
  }

  // Task list
  return (
    <div className={`space-y-3 ${className}`}>
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
