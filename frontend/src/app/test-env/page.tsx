"use client";

/**
 * Test page to verify environment variables are available in browser
 */

export default function TestEnvPage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  return (
    <div style={{ padding: "20px", fontFamily: "monospace" }}>
      <h1>Environment Variable Test</h1>
      <div style={{ marginTop: "20px", padding: "10px", background: "#f0f0f0" }}>
        <p><strong>NEXT_PUBLIC_API_URL:</strong></p>
        <p style={{ color: apiUrl ? "green" : "red", fontSize: "18px" }}>
          {apiUrl || "UNDEFINED"}
        </p>
      </div>

      <div style={{ marginTop: "20px" }}>
        <p><strong>Test URL construction:</strong></p>
        <code style={{ display: "block", padding: "10px", background: "#f0f0f0", marginTop: "10px" }}>
          {`${apiUrl}/api/test-user/chat`}
        </code>
      </div>

      <div style={{ marginTop: "20px" }}>
        <p><strong>typeof:</strong> {typeof apiUrl}</p>
        <p><strong>window.location.origin:</strong> {typeof window !== 'undefined' ? window.location.origin : 'N/A'}</p>
      </div>
    </div>
  );
}
