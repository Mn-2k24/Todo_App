"use client";

/**
 * Dashboard page - Task management interface.
 * Per US2: CRUD operations with loading, error, empty states.
 */

import { useEffect, useState, useCallback } from "react";
import { getCurrentUser } from "@/lib/auth";
import { apiRequest, ApiException } from "@/lib/api";
import type { User } from "@/types/user";
import type { Task, TaskCreateRequest, TaskUpdateRequest } from "@/types/task";
import { Priority } from "@/types/task";
import TaskForm from "@/components/tasks/TaskForm";
import TaskList from "@/components/tasks/TaskList";
import TaskFilters from "@/components/tasks/TaskFilters";
import TaskSort from "@/components/tasks/TaskSort";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import Toast from "@/components/ui/Toast";

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);

  // Filter state
  const [priorityFilter, setPriorityFilter] = useState<Priority | null>(null);
  const [tagsFilter, setTagsFilter] = useState<string>("");
  const [searchFilter, setSearchFilter] = useState<string>("");
  const [statusFilter, setStatusFilter] = useState<string>("");

  // Sort state with localStorage persistence per FR-036
  const [sortBy, setSortBy] = useState<string>(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("taskSortPreference") || "created";
    }
    return "created";
  });

  // Edit state
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isEditMode, setIsEditMode] = useState(false);

  // Delete confirmation state
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState<string | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // Toast state
  const [toastMessage, setToastMessage] = useState("");
  const [toastVariant, setToastVariant] = useState<"success" | "error">("success");
  const [showToast, setShowToast] = useState(false);

  // Define fetchTasks with useCallback BEFORE useEffect that uses it
  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // Build query string with all filters and sort if set per FR-030
      const params = new URLSearchParams();
      if (priorityFilter) {
        params.append("priority", priorityFilter);
      }
      if (tagsFilter.trim()) {
        params.append("tags", tagsFilter.trim());
      }
      if (searchFilter.trim()) {
        params.append("search", searchFilter.trim());
      }
      if (statusFilter) {
        params.append("status", statusFilter);
      }
      if (sortBy) {
        params.append("sort_by", sortBy);

        // Set order based on sort option to match UI labels:
        // - title (A-Z) → asc
        // - due_date (Nearest First = soonest) → asc
        // - priority (High to Low: high=0, medium=1, low=2) → asc
        // - created (Newest First) → desc
        const order = sortBy === "created" ? "desc" : "asc";
        params.append("order", order);
      }

      const queryString = params.toString();
      const endpoint = queryString ? `/api/tasks?${queryString}` : "/api/tasks";

      const data = await apiRequest<Task[]>(endpoint, {
        method: "GET",
      });
      setTasks(data);
    } catch (err) {
      setError(err);
      // If 401, redirect to login (only here, not in apiRequest)
      if (err instanceof ApiException && err.status === 401) {
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
      }
    } finally {
      setLoading(false);
    }
  }, [priorityFilter, tagsFilter, searchFilter, statusFilter, sortBy]);

  // Fetch user data on mount (middleware already verified authentication)
  useEffect(() => {
    const loadUserData = async () => {
      try {
        const currentUser = await getCurrentUser();
        if (currentUser) {
          setUser(currentUser);
        }
      } catch {
        // Silently fail - middleware already verified token exists
        // User info is optional for UI display
      }
    };

    loadUserData();
  }, []);

  // Fetch tasks on mount and when filters or sort change
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Save sort preference to localStorage per FR-036
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("taskSortPreference", sortBy);
    }
  }, [sortBy]);

  const handleCreateTask = async (description: string, priority: Priority, tags: string[], dueDate: string | null) => {
    const requestData: TaskCreateRequest = {
      description,
      priority,
      tags,
      due_date: dueDate || undefined,
    };

    const newTask = await apiRequest<Task>("/api/tasks", {
      method: "POST",
      body: requestData,
    });

    setTasks([newTask, ...tasks]);
    showSuccessToast("Task created successfully!");
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setIsEditMode(true);
  };

  const handleUpdateTask = async (description: string, priority: Priority, tags: string[], dueDate: string | null) => {
    if (!editingTask) return;

    const requestData: TaskUpdateRequest = {
      description,
      priority,
      tags,
      due_date: dueDate || undefined,
    };

    const updatedTask = await apiRequest<Task>(`/api/tasks/${editingTask.id}`, {
      method: "PUT",
      body: requestData,
    });

    setTasks(tasks.map((t) => (t.id === updatedTask.id ? updatedTask : t)));
    setIsEditMode(false);
    setEditingTask(null);
    showSuccessToast("Task updated successfully!");
  };

  const handleCancelEdit = () => {
    setIsEditMode(false);
    setEditingTask(null);
  };

  const handleToggleCompletion = async (taskId: string) => {
    const updatedTask = await apiRequest<Task>(
      `/api/tasks/${taskId}/complete`,
      {
        method: "PATCH",
      }
    );

    setTasks(tasks.map((t) => (t.id === updatedTask.id ? updatedTask : t)));
    showSuccessToast(
      updatedTask.completed
        ? "Task marked as complete!"
        : "Task marked as incomplete!"
    );
  };

  const handleDeleteClick = async (taskId: string) => {
    setTaskToDelete(taskId);
    setDeleteConfirmOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!taskToDelete) return;

    setDeleteLoading(true);

    try {
      // Call backend API to delete task
      await apiRequest(`/api/tasks/${taskToDelete}`, {
        method: "DELETE",
      });

      // Update state immutably - filter creates new array without deleted task
      setTasks(tasks.filter((t) => t.id !== taskToDelete));

      // Show success feedback
      showSuccessToast("Task deleted successfully!");

      // Close dialog and reset state
      setDeleteConfirmOpen(false);
      setTaskToDelete(null);
    } catch (error) {
      // Handle errors gracefully - keep task visible, show error
      setError(error);
      showErrorToast("Failed to delete task. Please try again.");
    } finally {
      // Always reset loading state
      setDeleteLoading(false);
    }
  };

  const handleCancelDelete = () => {
    setDeleteConfirmOpen(false);
    setTaskToDelete(null);
  };

  const showSuccessToast = (message: string) => {
    setToastMessage(message);
    setToastVariant("success");
    setShowToast(true);
  };

  const showErrorToast = (message: string) => {
    setToastMessage(message);
    setToastVariant("error");
    setShowToast(true);
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        {user && (
          <p className="mt-2 text-gray-600">
            Welcome back, <span className="font-medium">{user.name}</span>!
          </p>
        )}
      </div>

      {/* Task Form */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          {isEditMode ? "Edit Task" : "Create New Task"}
        </h2>
        <TaskForm
          task={editingTask}
          onSubmit={isEditMode ? handleUpdateTask : handleCreateTask}
          onCancel={isEditMode ? handleCancelEdit : undefined}
          submitLabel={isEditMode ? "Save Changes" : "Add Task"}
        />
      </div>

      {/* Filters */}
      <div className="card mb-4">
        <TaskFilters
          selectedPriority={priorityFilter}
          onPriorityChange={setPriorityFilter}
          selectedTags={tagsFilter}
          onTagsChange={setTagsFilter}
          searchText={searchFilter}
          onSearchChange={setSearchFilter}
          selectedStatus={statusFilter}
          onStatusChange={setStatusFilter}
        />
      </div>

      {/* Sort */}
      <div className="card mb-4">
        <TaskSort selectedSort={sortBy} onSortChange={setSortBy} />
      </div>

      {/* Task List */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          All Tasks ({tasks.length})
        </h2>
        <TaskList
          tasks={tasks}
          loading={loading}
          error={error}
          onToggle={handleToggleCompletion}
          onEdit={handleEditTask}
          onDelete={handleDeleteClick}
          hasActiveFilters={!!(priorityFilter || tagsFilter || searchFilter || statusFilter)}
        />
      </div>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={deleteConfirmOpen}
        title="Delete Task"
        message="Are you sure you want to delete this task? This action cannot be undone."
        confirmLabel="Delete"
        cancelLabel="Cancel"
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        loading={deleteLoading}
      />

      {/* Toast Notifications */}
      <Toast
        message={toastMessage}
        variant={toastVariant}
        isVisible={showToast}
        onDismiss={() => setShowToast(false)}
      />
    </div>
  );
}
