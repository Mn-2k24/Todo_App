# TaskDeleteFrontendStateSyncSkill

**Agent:** task-deletion-reliability-fixer
**Purpose:** Ensure frontend state updates immediately after task deletion, remove deleted task from UI without page reload, and prevent global error UI from triggering incorrectly.

---

## Context

**When to Use This Skill:**
- When tasks remain visible in UI after successful deletion
- When page reload is required to see deletion take effect
- When global "An unexpected error occurred" message appears after successful delete
- When React state doesn't update despite successful API call

**Symptoms Indicating This Skill is Needed:**
- Task visible in list after delete confirmation
- Network tab shows 204/200 response, but UI unchanged
- Global error boundary triggers after successful delete
- Page refresh reveals task was actually deleted

---

## Problem Analysis

### Root Cause Scenarios

1. **State Update Missing:**
   - API call succeeds
   - `catch` block not triggered
   - But `setTasks()` not called
   - UI retains old state

2. **State Update in Wrong Block:**
   - State update inside `try` block before API call
   - API throws error
   - State already updated, but error shown
   - Inconsistent state

3. **Immutable Update Error:**
   - State update uses mutation (`.splice()`, `.push()`)
   - React doesn't detect change
   - UI doesn't re-render

4. **Error Boundary Triggered:**
   - State update throws error
   - Caught by error boundary, not `catch` block
   - Global error UI shown
   - Task deletion succeeded but UI broken

---

## Execution Steps

### Step 1: Locate DELETE Handler in Dashboard

**Goal:** Find the exact function handling task deletion confirmation.

**Actions:**
```bash
# Search for delete handler
grep -n "handleConfirmDelete\|handleDelete\|deleteTask" frontend/src/app/(protected)/dashboard/page.tsx

# Look for confirmation dialog handler
grep -n "ConfirmDialog" frontend/src/app/(protected)/dashboard/page.tsx
```

**Expected Findings:**
- Function name: `handleConfirmDelete` or similar
- State variables: `taskToDelete`, `deleteConfirmOpen`, `deleteLoading`
- API call: `apiRequest(..., method: "DELETE")`

**Document:**
```markdown
DELETE Handler Location:
- File: frontend/src/app/(protected)/dashboard/page.tsx
- Function: handleConfirmDelete (line XX)
- State: taskToDelete, tasks, deleteLoading
```

---

### Step 2: Inspect State Update Logic

**Goal:** Verify if and where `setTasks()` is called after deletion.

**Actions:**
```typescript
// Read handleConfirmDelete function completely
// Check for:

try {
  await apiRequest(`/api/tasks/${taskToDelete}`, {
    method: "DELETE",
  });

  // IS THERE A setTasks() CALL HERE?
  setTasks(tasks.filter((t) => t.id !== taskToDelete));  // ✅ SHOULD BE HERE

  // IS THERE A SUCCESS TOAST?
  showSuccessToast("Task deleted successfully!");  // ✅ SHOULD BE HERE

} catch (error) {
  // Error handling
  showErrorToast("Failed to delete task. Please try again.");
}
```

**Key Investigation Points:**
1. **State update location:**
   - Is `setTasks()` inside `try` block?
   - Is it after API call or before?
   - Is it inside `catch` block by mistake?

2. **Immutability check:**
   - Uses `.filter()` (✅ immutable)
   - Uses `.splice()` (❌ mutation)
   - Uses spread operator `[...tasks]` (✅ immutable)

3. **Conditional execution:**
   - Is state update behind an `if` statement?
   - Could it be skipped?

**Document:**
```markdown
State Update Analysis:
- setTasks() called: [yes/no]
- Location: [inside try | inside catch | missing]
- Method: [filter | splice | other]
- Conditional: [yes/no]
```

---

### Step 3: Check for Error Boundary Issues

**Goal:** Ensure state updates don't throw errors that bypass `catch` block.

**Actions:**
```typescript
// Check if state update could throw
setTasks(tasks.filter((t) => t.id !== taskToDelete));
// Could fail if:
// - tasks is null/undefined
// - taskToDelete is null/undefined
// - filter returns unexpected type
```

**Investigation:**
1. **Null safety:**
   ```typescript
   if (!taskToDelete) return;  // Guard clause at function start?
   ```

2. **Type safety:**
   ```typescript
   // Is tasks always Task[]?
   // Could it be undefined during loading?
   ```

3. **Error boundary:**
   ```bash
   # Check for error boundary in app layout
   grep -r "ErrorBoundary\|componentDidCatch" frontend/src/app
   ```

**Document:**
```markdown
Error Boundary Check:
- Guard clauses present: [yes/no]
- tasks type: [Task[] | Task[] | undefined]
- Error boundary exists: [yes/no]
- Could state update throw: [yes/no]
```

---

### Step 4: Verify React Renders UI Update

**Goal:** Confirm React detects state change and re-renders TaskList.

**Actions:**
```typescript
// Check TaskList component receives updated tasks prop
<TaskList
  tasks={tasks}  // This should trigger re-render when tasks changes
  onDelete={handleDeleteClick}
  ...
/>
```

**Key Investigation Points:**
1. **Prop passing:**
   - Is `tasks` state passed to `TaskList`?
   - Is it passed directly or transformed?

2. **Memo/optimization:**
   - Is `TaskList` wrapped in `React.memo()`?
   - Are there useMemo/useCallback preventing re-render?

3. **Key prop:**
   - Does each TaskItem have unique `key={task.id}`?
   - Could duplicate keys prevent updates?

**Document:**
```markdown
React Rendering:
- tasks passed to TaskList: [yes/no]
- TaskList memoized: [yes/no]
- TaskItem keys: [task.id | index | other]
```

---

### Step 5: Reproduce and Debug

**Goal:** Trace execution path during deletion to find where it breaks.

**Actions:**
1. **Add console.log debugging:**
   ```typescript
   const handleConfirmDelete = async () => {
     console.log("1. Starting delete for task:", taskToDelete);

     try {
       console.log("2. Calling API DELETE...");
       await apiRequest(`/api/tasks/${taskToDelete}`, {
         method: "DELETE",
       });
       console.log("3. API DELETE succeeded");

       console.log("4. Updating state, tasks before:", tasks.length);
       setTasks(tasks.filter((t) => t.id !== taskToDelete));
       console.log("5. State updated");

       showSuccessToast("Task deleted successfully!");
       console.log("6. Toast shown");
     } catch (error) {
       console.log("ERROR CAUGHT:", error);
     }
   };
   ```

2. **Test deletion and observe console**
3. **Note which log appears last**

**Expected Output (Success):**
```
1. Starting delete for task: abc-123
2. Calling API DELETE...
3. API DELETE succeeded
4. Updating state, tasks before: 5
5. State updated
6. Toast shown
```

**If logs stop at step 3:**
- State update is missing or unreachable

**If logs show ERROR CAUGHT:**
- API call failed (check TaskDeleteApiResponseValidationSkill)

**If logs complete but UI unchanged:**
- React re-render issue (check immutability)

---

## Solution Strategy

### Fix 1: Add Missing State Update

**Issue:** `setTasks()` call is missing after successful DELETE.

**Fix Location:** `frontend/src/app/(protected)/dashboard/page.tsx` - `handleConfirmDelete`

**Fix Strategy:**
```typescript
const handleConfirmDelete = async () => {
  if (!taskToDelete) return;

  setDeleteLoading(true);

  try {
    await apiRequest(`/api/tasks/${taskToDelete}`, {
      method: "DELETE",
    });

    // ✅ ADD THIS: Remove task from state immutably
    setTasks(tasks.filter((t) => t.id !== taskToDelete));

    // ✅ ADD THIS: Show success feedback
    showSuccessToast("Task deleted successfully!");

    // Reset dialog state
    setDeleteConfirmOpen(false);
    setTaskToDelete(null);
  } catch (error) {
    setError(error);
    showErrorToast("Failed to delete task. Please try again.");
  } finally {
    setDeleteLoading(false);
  }
};
```

---

### Fix 2: Ensure Immutable State Update

**Issue:** State update uses mutation, React doesn't detect change.

**Wrong (Mutation):**
```typescript
// ❌ BAD: Mutates array
const index = tasks.findIndex((t) => t.id === taskToDelete);
tasks.splice(index, 1);
setTasks(tasks);  // React won't detect change
```

**Correct (Immutable):**
```typescript
// ✅ GOOD: Creates new array
setTasks(tasks.filter((t) => t.id !== taskToDelete));

// ✅ ALSO GOOD: Spread operator
setTasks([...tasks.filter((t) => t.id !== taskToDelete)]);
```

---

### Fix 3: Guard Against Null/Undefined

**Issue:** State update throws error when `tasks` or `taskToDelete` is null.

**Fix Strategy:**
```typescript
const handleConfirmDelete = async () => {
  // Guard clauses at top
  if (!taskToDelete) {
    console.error("No task selected for deletion");
    return;
  }

  if (!tasks || tasks.length === 0) {
    console.error("Tasks array is empty or undefined");
    return;
  }

  setDeleteLoading(true);

  try {
    await apiRequest(`/api/tasks/${taskToDelete}`, {
      method: "DELETE",
    });

    // Safe to update state now
    setTasks(tasks.filter((t) => t.id !== taskToDelete));
    showSuccessToast("Task deleted successfully!");

    setDeleteConfirmOpen(false);
    setTaskToDelete(null);
  } catch (error) {
    setError(error);
    showErrorToast("Failed to delete task. Please try again.");
  } finally {
    setDeleteLoading(false);
  }
};
```

---

### Fix 4: Prevent Error Boundary Triggering

**Issue:** Unhandled error in state update triggers global error boundary.

**Fix Strategy:**
```typescript
try {
  await apiRequest(`/api/tasks/${taskToDelete}`, {
    method: "DELETE",
  });

  // Wrap state update in try to catch its errors
  try {
    setTasks(tasks.filter((t) => t.id !== taskToDelete));
    showSuccessToast("Task deleted successfully!");
  } catch (stateError) {
    // State update failed, but deletion succeeded
    console.error("State update error:", stateError);
    showErrorToast("Task deleted but UI update failed. Please refresh.");
  }

  setDeleteConfirmOpen(false);
  setTaskToDelete(null);
} catch (error) {
  // API deletion failed
  setError(error);
  showErrorToast("Failed to delete task. Please try again.");
} finally {
  setDeleteLoading(false);
}
```

---

## Acceptance Criteria

**MUST Pass All:**
- [ ] DELETE API call succeeds (204/200 status)
- [ ] Task removed from `tasks` state immediately
- [ ] Task disappears from UI without page reload
- [ ] Success toast shows: "Task deleted successfully!"
- [ ] No global error boundary triggered
- [ ] No console errors after deletion
- [ ] Task count decreases by 1 in UI
- [ ] Empty state shows if last task deleted
- [ ] Deleting multiple tasks works consecutively

**Test Cases:**
1. **Single Delete:** Delete 1 task → Immediate UI update
2. **Multiple Delete:** Delete 3 tasks in a row → All updates work
3. **Last Task:** Delete last task → Empty state appears
4. **Fast Clicking:** Double-click delete → No duplicate API calls
5. **Cancel Delete:** Open dialog, cancel → Task remains visible

---

## Implementation Checklist

**Phase 1: Diagnosis**
- [ ] Locate handleConfirmDelete function
- [ ] Check if setTasks() is called
- [ ] Verify immutable state update pattern
- [ ] Check for guard clauses
- [ ] Test current behavior with console logs

**Phase 2: Fix**
- [ ] Add missing setTasks() call if absent
- [ ] Replace mutation with immutable update
- [ ] Add guard clauses for null safety
- [ ] Wrap state update in error handling if needed

**Phase 3: Testing**
- [ ] Test single task deletion
- [ ] Test multiple consecutive deletions
- [ ] Test deleting last task (empty state)
- [ ] Verify no console errors
- [ ] Verify UI updates without reload

---

## Error Handling

**If Task Still Visible After Delete:**

1. **Check console logs:**
   - Did state update execute?
   - Any errors in console?

2. **Check React DevTools:**
   - Is `tasks` state updated?
   - Is TaskList receiving new prop?

3. **Check component memoization:**
   - Is TaskList or TaskItem memoized incorrectly?

**If Error Boundary Triggers:**

1. **Inspect error message**
2. **Check if state update is in try-catch**
3. **Add error boundary handling around state update**

**If Multiple Deletes Fail:**

1. **Check if state is stale** (use functional setState)
   ```typescript
   setTasks((prevTasks) => prevTasks.filter((t) => t.id !== taskToDelete));
   ```

---

## Related Skills

- **TaskDeleteApiResponseValidationSkill** - Handles API response validation
- **TaskDeleteUserFeedbackSkill** - Shows correct success/error messages
- **task-deletion-ui-sync** (agent) - Parent agent coordinating all deletion fixes

---

## Notes

**Key Principle:**
> React state updates must be immutable. Always create a new array/object reference for React to detect changes.

**Common Pitfall:**
> Updating state before API call completes. Always update state AFTER successful API response.

**Best Practice:**
> Use functional setState when new state depends on previous state to avoid race conditions:
> ```typescript
> setTasks((prev) => prev.filter((t) => t.id !== taskToDelete));
> ```
