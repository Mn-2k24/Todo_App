"use client";

/**
 * TaskFilters component - Filter tasks by priority, tags, search text, and status.
 * Per FR-026: Text search in task description.
 * Per FR-027: Status filtering (completed/incomplete).
 * Per FR-028: Priority filtering dropdown.
 * Per FR-029: Tag filtering with comma-separated input.
 */

import { Priority } from "@/types/task";

interface TaskFiltersProps {
  selectedPriority: Priority | null;
  onPriorityChange: (priority: Priority | null) => void;
  selectedTags: string;
  onTagsChange: (tags: string) => void;
  searchText: string;
  onSearchChange: (search: string) => void;
  selectedStatus: string;
  onStatusChange: (status: string) => void;
  className?: string;
}

export default function TaskFilters({
  selectedPriority,
  onPriorityChange,
  selectedTags,
  onTagsChange,
  searchText,
  onSearchChange,
  selectedStatus,
  onStatusChange,
  className = "",
}: TaskFiltersProps) {
  return (
    <div className={`flex flex-col gap-4 ${className}`}>
      {/* Search input - FR-026 */}
      <div className="flex items-center gap-2">
        <label htmlFor="search-filter" className="text-sm font-medium text-gray-700 flex-shrink-0">
          Search:
        </label>
        <input
          id="search-filter"
          type="text"
          value={searchText}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Search task descriptions..."
          className="input flex-1"
        />
      </div>

      {/* Status, Priority, Tags filters */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
        {/* Status filter - FR-027 */}
        <div className="flex items-center gap-2">
          <label htmlFor="status-filter" className="text-sm font-medium text-gray-700">
            Status:
          </label>
          <select
            id="status-filter"
            value={selectedStatus}
            onChange={(e) => onStatusChange(e.target.value)}
            className="input w-auto"
          >
            <option value="">All</option>
            <option value="completed">Completed</option>
            <option value="incomplete">Incomplete</option>
          </select>
        </div>

        {/* Priority filter - FR-028 */}
        <div className="flex items-center gap-2">
          <label htmlFor="priority-filter" className="text-sm font-medium text-gray-700">
            Priority:
          </label>
          <select
            id="priority-filter"
            value={selectedPriority || ""}
            onChange={(e) => {
              const value = e.target.value;
              onPriorityChange(value ? (value as Priority) : null);
            }}
            className="input w-auto"
          >
            <option value="">All</option>
            <option value={Priority.HIGH}>High</option>
            <option value={Priority.MEDIUM}>Medium</option>
            <option value={Priority.LOW}>Low</option>
          </select>
        </div>

        {/* Tags filter - FR-029 */}
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <label htmlFor="tags-filter" className="text-sm font-medium text-gray-700 flex-shrink-0">
            Tags:
          </label>
          <input
            id="tags-filter"
            type="text"
            value={selectedTags}
            onChange={(e) => onTagsChange(e.target.value)}
            placeholder="Enter tags (comma-separated)..."
            className="input flex-1"
          />
        </div>
      </div>
    </div>
  );
}
