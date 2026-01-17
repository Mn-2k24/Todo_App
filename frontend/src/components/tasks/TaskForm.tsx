"use client";

/**
 * TaskForm component - Create and edit tasks with validation.
 * Per FR-015: Description required, FR-041: Loading states, FR-042: Error display.
 */

import { useState, useEffect } from "react";
import type { Task } from "@/types/task";
import { Priority } from "@/types/task";
import Button from "@/components/ui/Button";
import { ErrorInline } from "@/components/ui/ErrorMessage";

interface TaskFormProps {
  task?: Task | null;
  onSubmit: (description: string, priority: Priority, tags: string[], dueDate: string | null) => Promise<void>;
  onCancel?: () => void;
  submitLabel?: string;
  className?: string;
}

export default function TaskForm({
  task = null,
  onSubmit,
  onCancel,
  submitLabel = "Add Task",
  className = "",
}: TaskFormProps) {
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<Priority>(Priority.MEDIUM);
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState("");
  const [dueDate, setDueDate] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);

  // Populate form when editing
  useEffect(() => {
    if (task) {
      setDescription(task.description);
      setPriority(task.priority);
      setTags(task.tags || []);
      setDueDate(task.due_date || "");
    }
  }, [task]);

  const handleAddTag = () => {
    const trimmedTag = tagInput.trim();
    if (trimmedTag && !tags.includes(trimmedTag)) {
      setTags([...tags, trimmedTag]);
      setTagInput("");
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter((tag) => tag !== tagToRemove));
  };

  const handleTagInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleAddTag();
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Client-side validation
    const trimmedDescription = description.trim();
    if (!trimmedDescription) {
      setError({
        error: {
          error: "Task description cannot be empty",
          code: "INVALID_INPUT",
          status: 400,
        },
      });
      return;
    }

    if (trimmedDescription.length > 500) {
      setError({
        error: {
          error: "Task description cannot exceed 500 characters",
          code: "INVALID_INPUT",
          status: 400,
        },
      });
      return;
    }

    setLoading(true);

    try {
      await onSubmit(trimmedDescription, priority, tags, dueDate || null);

      // Reset form after successful creation (not edit)
      if (!task) {
        setDescription("");
        setPriority(Priority.MEDIUM);
        setTags([]);
        setTagInput("");
        setDueDate("");
      }
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={`space-y-4 ${className}`}>
      {error ? <ErrorInline error={error} /> : null}

      <div>
        <label htmlFor="task-description" className="block text-sm font-medium text-gray-700 mb-2">
          Task Description *
        </label>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description..."
          rows={3}
          className="input resize-none"
          disabled={loading}
          maxLength={500}
          required
        />
        <p className="mt-1 text-xs text-gray-500">
          {description.length}/500 characters
        </p>
      </div>

      <div>
        <label htmlFor="task-priority" className="block text-sm font-medium text-gray-700 mb-2">
          Priority
        </label>
        <select
          id="task-priority"
          value={priority}
          onChange={(e) => setPriority(e.target.value as Priority)}
          className="input"
          disabled={loading}
        >
          <option value={Priority.HIGH}>High</option>
          <option value={Priority.MEDIUM}>Medium</option>
          <option value={Priority.LOW}>Low</option>
        </select>
        <p className="mt-1 text-xs text-gray-500">
          
        </p>
      </div>

      <div>
        <label htmlFor="task-tags" className="block text-sm font-medium text-gray-700 mb-2">
          Tags
        </label>
        <div className="flex gap-2 mb-2">
          <input
            id="task-tags"
            type="text"
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyDown={handleTagInputKeyDown}
            placeholder="Enter tag and press Enter..."
            className="input flex-1"
            disabled={loading}
          />
          <Button
            type="button"
            variant="secondary"
            onClick={handleAddTag}
            disabled={loading || !tagInput.trim()}
          >
            Add Tag
          </Button>
        </div>
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {tags.map((tag) => (
              <span
                key={tag}
                className="badge badge-default flex items-center gap-1"
              >
                {tag}
                <button
                  type="button"
                  onClick={() => handleRemoveTag(tag)}
                  disabled={loading}
                  className="text-gray-600 hover:text-gray-900 focus:outline-none"
                  aria-label={`Remove tag ${tag}`}
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        )}
        <p className="mt-1 text-xs text-gray-500">
          
        </p>
      </div>

      <div>
        <label htmlFor="task-due-date" className="block text-sm font-medium text-gray-700 mb-2">
          Due Date (Optional)
        </label>
        <input
          id="task-due-date"
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="input"
          disabled={loading}
        />
        <p className="mt-1 text-xs text-gray-500">
          
        </p>
      </div>

      <div className="flex gap-3">
        <Button type="submit" variant="primary" loading={loading} disabled={loading}>
          {submitLabel}
        </Button>

        {onCancel && (
          <Button
            type="button"
            variant="ghost"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}
