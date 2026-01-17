"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getCurrentUser } from "@/lib/auth";

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check auth using httpOnly cookie via backend
    getCurrentUser().then((user) => {
      setIsAuthenticated(!!user);
      setLoading(false);
    });
  }, []);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-primary-50 to-white px-4">
      <div className="text-center">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          Welcome to <span className="text-primary-600">Todo App</span>
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
          Organize your tasks efficiently with our full-stack todo application.
          Create, manage, and track your tasks with priorities, tags, and due dates.
        </p>
        <div className="mt-10 flex items-center justify-center gap-6">
          {loading ? (
            // Server and initial client render: skeleton matching 2-button layout
            <>
              <div className="h-12 w-40 bg-gray-200 animate-pulse rounded-lg"></div>
              <div className="h-12 w-40 bg-gray-200 animate-pulse rounded-lg"></div>
            </>
          ) : isAuthenticated ? (
            <Link href="/dashboard" className="btn btn-primary text-lg px-8 py-3">
              Get Started
            </Link>
          ) : (
            <>
              <Link href="/login" className="btn btn-primary text-lg px-8 py-3">
                Get Started
              </Link>
              <Link href="/login" className="btn btn-outline text-lg px-8 py-3">
                Sign In
              </Link>
            </>
          )}
        </div>
        <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-3 max-w-4xl">
          <div className="rounded-lg bg-white p-6 shadow-md">
            <div className="text-primary-600 text-3xl font-bold mb-2">✓</div>
            <h3 className="font-semibold text-gray-900 mb-2">Task Management</h3>
            <p className="text-sm text-gray-600">
              Create, edit, and delete tasks with ease
            </p>
          </div>
          <div className="rounded-lg bg-white p-6 shadow-md">
            <div className="text-primary-600 text-3xl font-bold mb-2">⚡</div>
            <h3 className="font-semibold text-gray-900 mb-2">Priorities & Tags</h3>
            <p className="text-sm text-gray-600">
              Organize with priorities and custom tags
            </p>
          </div>
          <div className="rounded-lg bg-white p-6 shadow-md">
            <div className="text-primary-600 text-3xl font-bold mb-2">🔒</div>
            <h3 className="font-semibold text-gray-900 mb-2">Secure & Private</h3>
            <p className="text-sm text-gray-600">
              Your tasks are private and secure
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
