"use client";

/**
 * TaskSort component - Sort tasks by various criteria.
 * Per FR-032: Sort by title alphabetically.
 * Per FR-033: Sort by creation date newest first.
 * Per FR-034: Sort by due date nearest first.
 * Per FR-035: Sort by priority High→Medium→Low.
 */

interface TaskSortProps {
  selectedSort: string;
  onSortChange: (sortBy: string) => void;
  className?: string;
}

export default function TaskSort({
  selectedSort,
  onSortChange,
  className = "",
}: TaskSortProps) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <label htmlFor="sort-select" className="text-sm font-medium text-gray-700">
        Sort by:
      </label>
      <select
        id="sort-select"
        value={selectedSort}
        onChange={(e) => onSortChange(e.target.value)}
        className="input w-auto"
      >
        <option value="created">Newest First (Default)</option>
        <option value="title">Title (A-Z)</option>
        <option value="due_date">Due Date (Nearest First)</option>
        <option value="priority">Priority (High to Low)</option>
      </select>
    </div>
  );
}
