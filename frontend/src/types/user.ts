/**
 * User types for authentication and user management.
 *
 * These types mirror the backend Pydantic schemas for type alignment.
 */

/**
 * User entity (mirrors backend User model).
 */
export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

/**
 * User registration request.
 */
export interface RegisterRequest {
  email: string;
  name: string;
  password: string;
}

/**
 * User login request.
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Authentication response (login/register).
 */
export interface AuthResponse {
  user: User;
  token: string;
  token_type: string;
}
