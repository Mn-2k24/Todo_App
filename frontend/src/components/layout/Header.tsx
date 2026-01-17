"use client";

/**
 * Header component with app name, user menu, profile, and sign out functionality.
 * Per US1: Users can logout and session management.
 *
 * HYDRATION FIX: Uses mounted state guard to prevent SSR/client HTML mismatch.
 * Server cannot access localStorage, so we render neutral state until client mounts.
 */

import { useState, useEffect } from "react";
import { clearAuth, getUser } from "@/lib/auth";
import type { User } from "@/lib/auth";

export default function Header() {
  const [mounted, setMounted] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [showProfile, setShowProfile] = useState(false);

  useEffect(() => {
    // After client mount, check for user in localStorage
    setUser(getUser());
    setMounted(true);
  }, []);

  const handleSignOut = async () => {
    // Clear authentication data (removes token, user, and httpOnly cookie)
    await clearAuth();

    // Use window.location.href for full page reload to clear all state
    window.location.href = "/";
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* App name / logo */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-primary-600">
              <a href="/dashboard">Todo App</a>
            </h1>
          </div>

          {/* User menu - only render after client mount to prevent hydration mismatch */}
          {!mounted ? (
            // Server and initial client render: skeleton
            <div className="flex items-center gap-3">
              <div className="h-8 w-20 bg-gray-200 animate-pulse rounded" />
              <div className="h-8 w-20 bg-gray-200 animate-pulse rounded" />
            </div>
          ) : user ? (
            <div className="flex items-center gap-3">
              {/* Profile button with dropdown */}
              <div className="relative">
                <button
                  onClick={() => setShowProfile(!showProfile)}
                  className="btn btn-outline text-sm"
                  aria-label="Profile"
                  aria-expanded={showProfile}
                >
                  Profile
                </button>

                {/* Profile dropdown */}
                {showProfile && (
                  <div className="absolute right-0 mt-2 w-64 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 z-10">
                    <div className="p-4">
                      <div className="mb-2">
                        <label className="block text-xs font-medium text-gray-500 uppercase tracking-wide">
                          Name
                        </label>
                        <p className="mt-1 text-sm text-gray-900">{user.name}</p>
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-500 uppercase tracking-wide">
                          Email
                        </label>
                        <p className="mt-1 text-sm text-gray-900">{user.email}</p>
                      </div>
                      <button
                        onClick={() => setShowProfile(false)}
                        className="mt-3 w-full text-center text-xs text-gray-500 hover:text-gray-700"
                      >
                        Close
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Sign Out button */}
              <button
                onClick={handleSignOut}
                className="btn btn-outline text-sm"
                aria-label="Sign Out"
              >
                Sign Out
              </button>
            </div>
          ) : null}
        </div>
      </div>
    </header>
  );
}
