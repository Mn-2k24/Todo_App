/**
 * Task types for todo item management.
 *
 * These types mirror the backend Pydantic schemas for type alignment.
 */

/**
 * Task priority levels (mirrors backend Priority enum).
 */
export enum Priority {
  HIGH = "high",
  MEDIUM = "medium",
  LOW = "low",
}

/**
 * Task entity (mirrors backend Task model).
 */
export interface Task {
  id: string;
  user_id: string;
  description: string;
  completed: boolean;
  priority: Priority;
  tags: string[];
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Task creation request.
 */
export interface TaskCreateRequest {
  description: string;
  priority?: Priority;
  tags?: string[];
  due_date?: string | null;
}

/**
 * Task update request (all fields optional).
 */
export interface TaskUpdateRequest {
  description?: string;
  completed?: boolean;
  priority?: Priority;
  tags?: string[];
  due_date?: string | null;
}

/**
 * Task filters for GET /api/tasks query parameters.
 */
export interface TaskFilters {
  status?: "complete" | "incomplete" | "all";
  priority?: Priority;
  tags?: string;
  search?: string;
  sort_by?: "title" | "created" | "due_date" | "priority";
  order?: "asc" | "desc";
}

/**
 * Task sort options.
 */
export interface TaskSort {
  sort_by: "title" | "created" | "due_date" | "priority";
  order: "asc" | "desc";
}
