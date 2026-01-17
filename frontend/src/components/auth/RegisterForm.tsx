"use client";

/**
 * User registration form component.
 * Per US1: Users can register, login, logout, and maintain authenticated sessions.
 */

import { useState } from "react";
import { apiRequestPublic } from "@/lib/api";
import { saveUser } from "@/lib/auth";
import type { AuthResponse, RegisterRequest } from "@/types/user";
import ErrorMessage from "@/components/ui/ErrorMessage";
import { LoadingButton } from "@/components/ui/LoadingSpinner";

export default function RegisterForm() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Client-side validation
    if (name.length < 2 || name.length > 100) {
      setError({
        error: { error: "Name must be between 2 and 100 characters", code: "VALIDATION_ERROR", status: 400 },
      });
      return;
    }

    if (password !== confirmPassword) {
      setError({ error: { error: "Passwords do not match", code: "VALIDATION_ERROR", status: 400 } });
      return;
    }

    if (password.length < 8) {
      setError({
        error: { error: "Password must be at least 8 characters", code: "VALIDATION_ERROR", status: 400 },
      });
      return;
    }

    setLoading(true);

    try {
      const requestData: RegisterRequest = {
        email,
        name,
        password,
      };

      const response = await apiRequestPublic<AuthResponse>("/api/auth/register", {
        method: "POST",
        body: requestData,
      });

      // Save user to localStorage (token is in httpOnly cookie)
      saveUser(response.user);

      // Use window.location.href for full page reload to ensure cookies
      // are properly set before middleware checks authentication state
      window.location.href = "/dashboard";
    } catch (err) {
      setError(err);
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error ? <ErrorMessage error={error} onDismiss={() => setError(null)} /> : null}

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email address
        </label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={loading}
          className="input mt-1"
          placeholder="you@example.com"
        />
      </div>

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Full Name
        </label>
        <input
          id="name"
          name="name"
          type="text"
          autoComplete="name"
          required
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={loading}
          className="input mt-1"
          placeholder="John Doe"
          minLength={2}
          maxLength={100}
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="new-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          className="input mt-1"
          placeholder="Minimum 8 characters"
          minLength={8}
        />
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          autoComplete="new-password"
          required
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          disabled={loading}
          className="input mt-1"
          placeholder="Re-enter password"
          minLength={8}
        />
      </div>

      <button type="submit" disabled={loading} className="btn btn-primary w-full">
        {loading ? <LoadingButton>Creating account...</LoadingButton> : "Create account"}
      </button>

      <p className="text-center text-sm text-gray-600">
        Already have an account?{" "}
        <a href="/login" className="font-medium text-primary-600 hover:text-primary-500">
          Sign in
        </a>
      </p>
    </form>
  );
}
