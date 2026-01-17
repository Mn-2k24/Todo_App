# TaskDeleteApiResponseValidationSkill

**Agent:** task-deletion-reliability-fixer
**Purpose:** Validate DELETE task API responses correctly, distinguish between true failure and successful deletion, and prevent false error states after successful delete.

---

## Context

**When to Use This Skill:**
- When users report "Failed to delete task" errors despite backend successfully deleting the task
- When frontend shows error toast but task is gone after page reload
- When DELETE requests return unexpected status codes (200, 204, etc.)
- When frontend error handling treats successful deletion as failure

**Symptoms Indicating This Skill is Needed:**
- Frontend displays: "Failed to delete task, please try again"
- Backend logs show: `DELETE /api/tasks/{id}` returned 200 or 204
- Task is deleted from database but UI shows error
- Page refresh reveals task was actually deleted

---

## Problem Analysis

### Root Cause Scenarios

1. **Status Code Mismatch:**
   - Frontend expects HTTP 204 (No Content)
   - Backend returns HTTP 200 (OK)
   - Frontend treats 200 as error

2. **Empty Response Body Handling:**
   - Backend returns 204 with no body
   - Frontend tries to parse JSON from empty response
   - JSON parsing fails → triggers error handler

3. **Response Validation Logic:**
   - Frontend checks `response.ok` but also validates body
   - Empty body fails validation
   - Error state triggered despite successful deletion

---

## Execution Steps

### Step 1: Inspect Backend DELETE Endpoint

**Goal:** Understand what the backend actually returns on successful deletion.

**Actions:**
```bash
# Check backend DELETE endpoint code
grep -A 20 "DELETE.*tasks.*{task_id}" backend/src/api/tasks.py

# Look for status code definition
grep -B 5 -A 10 "status_code.*204\|status_code.*200" backend/src/api/tasks.py
```

**Expected Findings:**
- Status code: 204 (No Content) or 200 (OK)
- Response body: None or empty JSON `{}`
- Return type annotation in FastAPI

**Document:**
```markdown
Backend DELETE Response:
- Status Code: [204 | 200]
- Response Body: [None | {}]
- Headers: [Content-Type if any]
```

---

### Step 2: Inspect Frontend DELETE Request Handler

**Goal:** Identify how frontend handles DELETE API responses.

**Actions:**
```typescript
// Check frontend delete handler
// File: frontend/src/app/(protected)/dashboard/page.tsx

// Look for handleDeleteClick or handleConfirmDelete
// Examine apiRequest call for DELETE method
```

**Key Investigation Points:**
1. **Status code expectation:**
   - Does frontend expect 204 or 200?
   - Is there explicit status code checking?

2. **Response body parsing:**
   - Does frontend try to parse JSON?
   - Does it handle empty body correctly?

3. **Error detection logic:**
   - What conditions trigger `catch` block?
   - Does `apiRequest` throw on 204 with empty body?

**Document:**
```markdown
Frontend DELETE Handler:
- Expected status: [status code]
- Response parsing: [yes/no JSON parse]
- Error condition: [what triggers catch block]
```

---

### Step 3: Inspect `apiRequest` Utility Function

**Goal:** Understand generic API request handling logic.

**Actions:**
```typescript
// File: frontend/src/lib/api.ts

// Examine apiRequest function
// Check response.ok validation
// Check JSON parsing logic
// Check error throwing conditions
```

**Key Investigation Points:**
1. **Response validation:**
   ```typescript
   if (!response.ok) {
     throw new Error(...);
   }
   ```

2. **JSON parsing:**
   ```typescript
   const data = await response.json();  // Fails on empty body?
   ```

3. **Empty body handling:**
   ```typescript
   // Does it check Content-Length or Content-Type?
   // Does it handle 204 specially?
   ```

**Document:**
```markdown
apiRequest DELETE Handling:
- Validates response.ok: [yes/no]
- Parses JSON: [always | conditionally]
- Handles 204: [specially | same as 200]
- Throws on empty body: [yes/no]
```

---

### Step 4: Reproduce and Diagnose

**Goal:** Confirm exact failure mode with network inspection.

**Actions:**
1. **Open browser DevTools → Network tab**
2. **Delete a task**
3. **Capture DELETE request details:**
   - Request URL: `/api/tasks/{id}`
   - Response status: `200` or `204`
   - Response headers: `Content-Type`, `Content-Length`
   - Response body: (empty or JSON)

4. **Observe frontend behavior:**
   - Console errors (JSON parse error?)
   - Error toast shown?
   - Task removed from UI?

**Document:**
```markdown
Actual DELETE Behavior:
- Backend Status: [200 | 204]
- Backend Body: [empty | {}]
- Frontend Error: [specific error message]
- UI State: [task visible | removed]
```

---

## Solution Strategy

### Scenario A: Backend Returns 204 No Content

**Issue:** Frontend tries to parse empty body as JSON.

**Fix Location:** `frontend/src/lib/api.ts` - `apiRequest` function

**Fix Strategy:**
```typescript
// Before parsing JSON, check status code
if (response.status === 204) {
  return undefined;  // No content to parse
}

// Or check Content-Type header
const contentType = response.headers.get('content-type');
if (!contentType || !contentType.includes('application/json')) {
  return undefined;  // Not JSON
}

const data = await response.json();
return data;
```

---

### Scenario B: Backend Returns 200 OK with Empty Body

**Issue:** Frontend tries to parse empty string as JSON.

**Fix Location:** `frontend/src/lib/api.ts` - `apiRequest` function

**Fix Strategy:**
```typescript
// Check response text length before parsing
const text = await response.text();
if (!text || text.trim().length === 0) {
  return undefined;  // Empty response
}

const data = JSON.parse(text);
return data;
```

---

### Scenario C: DELETE Handler Expects JSON Response

**Issue:** DELETE handler assumes `apiRequest` always returns data.

**Fix Location:** `frontend/src/app/(protected)/dashboard/page.tsx` - `handleConfirmDelete`

**Fix Strategy:**
```typescript
const handleConfirmDelete = async () => {
  if (!taskToDelete) return;

  setDeleteLoading(true);

  try {
    // DELETE may return undefined for 204 responses
    await apiRequest(`/api/tasks/${taskToDelete}`, {
      method: "DELETE",
    });
    // Don't expect response data ^

    // Success: remove from UI
    setTasks(tasks.filter((t) => t.id !== taskToDelete));
    showSuccessToast("Task deleted successfully!");
    setDeleteConfirmOpen(false);
    setTaskToDelete(null);
  } catch (error) {
    // Real error handling
    setError(error);
    showErrorToast("Failed to delete task. Please try again.");
  } finally {
    setDeleteLoading(false);
  }
};
```

---

## Acceptance Criteria

**MUST Pass All:**
- [ ] Backend DELETE returns 204 No Content OR 200 OK
- [ ] Frontend correctly handles 204 responses (no JSON parsing)
- [ ] Frontend correctly handles empty body responses
- [ ] Delete success shows: "Task deleted successfully!" (green toast)
- [ ] Delete failure shows: "Failed to delete task" (red toast)
- [ ] Task removed from UI immediately on success
- [ ] Task remains visible on true failure
- [ ] No console errors on successful deletion
- [ ] No false error toasts on successful deletion
- [ ] Page reload confirms task is deleted

**Test Cases:**
1. **Success Case:** Delete task → Backend 204 → UI updates → Success toast
2. **Network Error:** Stop backend → Delete → Error toast → Task visible
3. **Permission Error:** Delete other user's task → 403 → Error toast
4. **Not Found:** Delete non-existent task → 404 → Error toast

---

## Implementation Checklist

**Phase 1: Diagnosis**
- [ ] Read backend DELETE endpoint code
- [ ] Read frontend DELETE handler code
- [ ] Read `apiRequest` function code
- [ ] Reproduce issue with network inspection
- [ ] Document actual vs expected behavior

**Phase 2: Fix Selection**
- [ ] Choose Scenario A, B, or C based on diagnosis
- [ ] Identify exact code location for fix
- [ ] Write fix code snippet

**Phase 3: Testing**
- [ ] Test successful deletion (200/204)
- [ ] Test network error (backend stopped)
- [ ] Test permission error (403)
- [ ] Verify no console errors
- [ ] Verify correct toast messages

---

## Error Handling

**If Fix Doesn't Work:**

1. **Console still shows errors:**
   - Check for other API request utilities
   - Check if component has its own error handling
   - Look for global error boundaries

2. **Task still shows error toast:**
   - Verify `catch` block is not triggered
   - Add console.log to trace execution path
   - Check if error is from state update, not API

3. **Backend returns unexpected status:**
   - Verify backend framework version
   - Check FastAPI DELETE response behavior
   - Test with `curl` to isolate frontend

---

## Related Skills

- **TaskDeleteFrontendStateSyncSkill** - Ensures UI updates after successful delete
- **TaskDeleteUserFeedbackSkill** - Shows correct success/error messages
- **api-backend-guardian** - Backend API contract validation

---

## Notes

**Key Principle:**
> HTTP 204 No Content is the standard response for successful DELETE operations with no response body. Frontend MUST handle this without attempting JSON parsing.

**Common Pitfall:**
> Many API clients default to `response.json()` which throws on empty body. Always check status code or Content-Type before parsing.

**Best Practice:**
> Use TypeScript's `void` or `undefined` return type for DELETE operations that don't return data.
