"use client";

/**
 * User login form component.
 * Per US1: Users can register, login, logout, and maintain authenticated sessions.
 */

import { useState } from "react";
import { apiRequestPublic } from "@/lib/api";
import { saveUser } from "@/lib/auth";
import type { AuthResponse, LoginRequest } from "@/types/user";
import ErrorMessage from "@/components/ui/ErrorMessage";
import { LoadingButton } from "@/components/ui/LoadingSpinner";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const requestData: LoginRequest = {
        email,
        password,
      };

      const response = await apiRequestPublic<AuthResponse>("/api/auth/login", {
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
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading}
          className="input mt-1"
          placeholder="Enter your password"
        />
      </div>

      <button type="submit" disabled={loading} className="btn btn-primary w-full">
        {loading ? <LoadingButton>Signing in...</LoadingButton> : "Sign in"}
      </button>

      <p className="text-center text-sm text-gray-600">
        Don&apos;t have an account?{" "}
        <a href="/register" className="font-medium text-primary-600 hover:text-primary-500">
          Create account
        </a>
      </p>
    </form>
  );
}
