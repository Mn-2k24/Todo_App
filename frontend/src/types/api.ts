/**
 * API response types for error handling and pagination.
 *
 * These types mirror the backend error response schemas.
 */

/**
 * API error response (mirrors backend error schema).
 */
export interface ApiError {
  error: string;
  code: string;
  status: number;
  [key: string]: unknown;
}

/**
 * Paginated response wrapper (for future pagination support).
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  has_next: boolean;
  has_prev: boolean;
}

/**
 * Generic success response.
 */
export interface SuccessResponse {
  message: string;
  [key: string]: unknown;
}
