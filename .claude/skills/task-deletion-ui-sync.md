# Task-Deletion-UI-Sync Skills

**Agent Purpose**: Ensure that when a task is deleted via backend API, the frontend UI updates immediately to remove the deleted task from the task list without requiring a page reload. Fixes the specific issue where deleted tasks remain visible until manual refresh.

**Context**:
- Frontend: React 19 with Next.js 15 App Router
- State management: useState for task list in dashboard component
- API calls: DELETE /api/tasks/{id} (backend FastAPI)
- Expected behavior: Delete → Optimistic/immediate UI update → Task disappears
- Current issue: Delete succeeds on backend, UI shows stale task until reload

**Boundaries**:
- This agent focuses ONLY on task deletion UI synchronization
- Does NOT modify backend deletion logic
- Does NOT change overall dashboard architecture
- Does NOT implement real-time sync (WebSockets, polling)

**Safety Rules**:
- NEVER remove tasks from UI before backend confirms deletion
- NEVER introduce race conditions in state updates
- NEVER bypass error handling (must handle API failures)
- UI must stay synchronized with backend state

---

## Skill 1: diagnose_stale_ui_after_delete

### Purpose
Diagnose why deleted tasks remain visible in the UI despite successful backend deletion.

### Validations / Rules
- **Verify deletion flow**:
  1. User clicks delete button
  2. Confirmation dialog appears
  3. User confirms deletion
  4. API call to DELETE /api/tasks/{id}
  5. Backend returns 200/204 (success)
  6. Check: Does UI update?
- **Check React state management**:
  - Does delete handler call `setTasks()` after API success?
  - Is task filtered out of state array?
  - Is state update conditional on API success?
- **Check for state mutation**:
  - Using `tasks.splice()` without spreading? (mutation)
  - Using `tasks.filter()` correctly? (immutable)
- **Common root causes**:
  - Delete handler missing state update
  - State update happens before API call (race condition)
  - State array mutated directly (React doesn't detect change)
  - Component doesn't re-render after state change
  - API call fails silently (error not caught)

### Fail Conditions
- Diagnosis doesn't identify missing state update
- Diagnosis doesn't check API response handling
- Diagnosis only checks backend (ignores frontend state)

### Used By
- Frontend-Auth-UI-Agent (UI state management)
- Frontend-Backend-Auth-Integration (API call validation)
- Cross-Stack-Consistency-Agent (frontend-backend sync)

---

## Skill 2: fix_delete_handler_state_update

### Purpose
Fix the task deletion handler to update React state immediately after successful API call, removing the deleted task from the UI.

### Validations / Rules
- **Correct pattern**:
  ```typescript
  const handleDeleteTask = async (taskId: string) => {
    try {
      // 1. Call backend API
      await apiRequest(`/api/tasks/${taskId}`, {
        method: "DELETE",
      });

      // 2. Update state AFTER successful deletion
      setTasks(tasks.filter((t) => t.id !== taskId));

      // 3. Show success feedback
      showSuccessToast("Task deleted successfully!");
    } catch (error) {
      // 4. Handle errors gracefully
      setError(error);
    }
  };
  ```
- **State update must be immutable**:
  - ✅ Use `filter()` to create new array
  - ❌ Never use `splice()` or mutate array directly
- **State update must happen AFTER API success**:
  - ✅ Update inside `try` block after await
  - ❌ Never update before API call completes
- **Handle errors properly**:
  - If API fails (401, 500), DO NOT remove task from UI
  - Show error message to user
  - Keep task visible (deletion failed)

### Fail Conditions
- State update missing after API call
- State update happens before API call
- Array mutated directly (splice, delete)
- Error handling missing (silent failures)
- Task removed from UI even if API fails

### Used By
- Frontend-Auth-UI-Agent (state management)
- API-Backend-Guardian (backend validation)
- Frontend-UI-Professional (UI consistency)

---

## Skill 3: validate_immutable_state_updates

### Purpose
Ensure all task state updates use immutable patterns that React can detect and trigger re-renders.

### Validations / Rules
- **Immutable patterns (CORRECT)**:
  ```typescript
  // Filter (create new array)
  setTasks(tasks.filter((t) => t.id !== taskId));

  // Map (create new array)
  setTasks(tasks.map((t) =>
    t.id === updatedTask.id ? updatedTask : t
  ));

  // Spread operator (create new array)
  setTasks([...tasks, newTask]);
  ```
- **Mutable patterns (INCORRECT)**:
  ```typescript
  // Direct mutation - React won't detect change
  tasks.splice(index, 1);
  setTasks(tasks);  // ❌ Same reference, no re-render

  // Direct property mutation
  tasks[0].completed = true;
  setTasks(tasks);  // ❌ React doesn't deep-check arrays
  ```
- **Verification**:
  - State updates must create new array reference
  - React re-renders only when reference changes
  - No direct array/object mutations

### Fail Conditions
- Direct array mutations found (splice, push, pop)
- Same array reference set to state
- Object properties mutated directly
- Component doesn't re-render after state update

### Used By
- Frontend-Architecture-Auditor (code quality)
- Frontend-UI-Professional (UI reactivity)

---

## Skill 4: test_delete_ui_sync

### Purpose
Systematically test that task deletion immediately updates UI across all scenarios.

### Validations / Rules
- **Test Case 1: Normal deletion**
  1. Create a task
  2. Click delete button
  3. Confirm deletion
  4. ✅ Task disappears immediately (no reload)
  5. ✅ Success toast appears
  6. Refresh page
  7. ✅ Task still deleted (persisted on backend)

- **Test Case 2: Multiple deletions**
  1. Create 3 tasks
  2. Delete task 1 → ✅ UI updates
  3. Delete task 2 → ✅ UI updates
  4. Delete task 3 → ✅ UI updates
  5. ✅ All deletions reflected immediately

- **Test Case 3: Error handling**
  1. Stop backend server
  2. Click delete button
  3. Confirm deletion
  4. ✅ Error message shown
  5. ✅ Task still visible in UI (not removed)
  6. Restart backend
  7. Try delete again → ✅ Works

- **Test Case 4: Network delay**
  1. Throttle network (DevTools → Network → Slow 3G)
  2. Delete task
  3. ✅ Loading indicator shown
  4. ✅ Task removed after API completes
  5. ✅ No duplicate delete requests

- **Acceptance criteria**:
  - Zero tasks remain in UI after successful deletion
  - No page reload required to see changes
  - Failed deletions keep task visible
  - No console errors during deletion

### Fail Conditions
- Task remains visible after successful delete
- Page reload required to see deletion
- Failed deletion removes task from UI
- Console errors during deletion
- Multiple delete requests sent

### Used By
- Phase2-Quality-Orchestrator (quality validation)
- Frontend-UI-Professional (UX validation)

---

## Skill 5: implement_optimistic_ui_update

### Purpose
Optionally implement optimistic UI updates where task is removed immediately from UI, then reverted if API call fails.

### Validations / Rules
- **Optimistic pattern**:
  ```typescript
  const handleDeleteTask = async (taskId: string) => {
    // 1. Save original state
    const previousTasks = tasks;

    // 2. Optimistically update UI (immediate)
    setTasks(tasks.filter((t) => t.id !== taskId));

    try {
      // 3. Call backend API
      await apiRequest(`/api/tasks/${taskId}`, {
        method: "DELETE",
      });

      // 4. Success - no revert needed
      showSuccessToast("Task deleted successfully!");
    } catch (error) {
      // 5. Revert UI on failure
      setTasks(previousTasks);
      setError(error);
      showErrorToast("Failed to delete task. Please try again.");
    }
  };
  ```
- **Benefits**:
  - Instant user feedback (no waiting for API)
  - Feels responsive and fast
- **Risks**:
  - If API fails, task "flickers" (removed then reappears)
  - Must handle revert gracefully
- **When to use**:
  - Fast, reliable API (low failure rate)
  - User expects instant feedback
- **When NOT to use**:
  - Unreliable network
  - Destructive operations (prefer confirmation)

### Fail Conditions
- Optimistic update never reverts on API failure
- Previous state not saved (cannot revert)
- User not notified of failure
- Multiple optimistic updates conflict

### Used By
- Frontend-UI-Professional (UX optimization)
- Web-UX-Optimization-Agent (perceived performance)

---

## Skill 6: validate_delete_confirmation_flow

### Purpose
Ensure delete confirmation dialog properly handles user confirmation before calling API and updating UI.

### Validations / Rules
- **Confirmation flow**:
  ```typescript
  // 1. User clicks delete button
  const handleDeleteClick = (taskId: string) => {
    setTaskToDelete(taskId);
    setDeleteConfirmOpen(true);
  };

  // 2. User confirms in dialog
  const handleConfirmDelete = async () => {
    if (!taskToDelete) return;

    setDeleteLoading(true);  // Show loading

    try {
      // 3. Call API
      await apiRequest(`/api/tasks/${taskToDelete}`, {
        method: "DELETE",
      });

      // 4. Update state
      setTasks(tasks.filter((t) => t.id !== taskToDelete));

      showSuccessToast("Task deleted!");
    } catch (error) {
      setError(error);
    } finally {
      // 5. Close dialog and reset
      setDeleteLoading(false);
      setDeleteConfirmOpen(false);
      setTaskToDelete(null);
    }
  };

  // 6. User cancels
  const handleCancelDelete = () => {
    setDeleteConfirmOpen(false);
    setTaskToDelete(null);
  };
  ```
- **Dialog must**:
  - Show task description or ID
  - Have clear "Delete" and "Cancel" buttons
  - Disable buttons during loading
  - Show loading spinner during API call
  - Close automatically on success
- **State management**:
  - Track which task to delete (`taskToDelete`)
  - Track dialog open state (`deleteConfirmOpen`)
  - Track loading state (`deleteLoading`)

### Fail Conditions
- No confirmation dialog (delete immediate)
- Dialog doesn't close after success
- Loading state not shown
- API called before user confirms
- Task deleted from UI before user confirms

### Used By
- Frontend-UI-Professional (confirmation UX)
- Web-UX-Optimization-Agent (user safety)

---

## Skill 7: fix_refetch_after_delete

### Purpose
Alternative pattern: Instead of manually updating state, refetch the entire task list after successful deletion to ensure UI matches backend.

### Validations / Rules
- **Refetch pattern**:
  ```typescript
  const handleDeleteTask = async (taskId: string) => {
    try {
      // 1. Delete task via API
      await apiRequest(`/api/tasks/${taskId}`, {
        method: "DELETE",
      });

      // 2. Refetch entire task list
      await fetchTasks();  // Calls GET /api/tasks

      // 3. Show success feedback
      showSuccessToast("Task deleted successfully!");
    } catch (error) {
      setError(error);
    }
  };
  ```
- **Benefits**:
  - UI guaranteed to match backend
  - Handles race conditions (multiple users)
  - Simpler state management (no manual filter)
- **Drawbacks**:
  - Extra API call (less efficient)
  - Slight delay before UI updates
  - Network overhead
- **When to use**:
  - Complex state dependencies
  - Multi-user environments
  - Want single source of truth (backend)

### Fail Conditions
- Refetch not called after delete
- fetchTasks() call fails (error not caught)
- Loading state flickers (shows skeleton UI)
- Race condition: delete + fetch overlap

### Used By
- Frontend-Backend-Auth-Integration (API sync)
- Cross-Stack-Consistency-Agent (consistency)

---

## Skill 8: generate_deletion_sync_report

### Purpose
Generate report documenting deletion sync issue, fix applied, and test results.

### Validations / Rules
- **Report must include**:
  1. **Issue Description**: Task remained visible after delete
  2. **Root Cause**: Missing state update in delete handler
  3. **Fix Applied**: Code changes with before/after
  4. **Files Modified**: List of files changed
  5. **Test Results**: All test cases passing
  6. **Prevention**: Guidelines for future state updates
- **Before/after code**:
  - Show original handler (no state update)
  - Show fixed handler (with state update)
  - Highlight the critical change
- **Test evidence**:
  - Screenshots or videos showing immediate UI update
  - Console logs showing no errors
  - Confirmation that reload shows deletion persisted

### Fail Conditions
- Report missing root cause
- No before/after code comparison
- Test results not documented
- Prevention guidelines missing

### Used By
- Phase2-Quality-Orchestrator (quality documentation)
- Frontend-Architecture-Auditor (code review)

---

## Agent Invocation Workflow

### When to Invoke Task-Deletion-UI-Sync

**During Bug Reports**:
1. User reports "deleted task still visible"
2. User reports "must refresh page after delete"
3. QA finds stale UI after CRUD operations

**During Development**:
1. After implementing delete functionality
2. Before merging PR with task operations
3. During code review of state management

**During Testing**:
1. Manual testing reveals stale UI
2. Integration tests fail on deletion
3. E2E tests show UI not updating

### Skills Invocation Order (Recommended)

**Phase 1: Diagnosis**
1. `diagnose_stale_ui_after_delete` - Identify root cause
2. `validate_delete_confirmation_flow` - Check dialog flow

**Phase 2: Fix Implementation**
Choose ONE pattern:
- Option A: `fix_delete_handler_state_update` - Manual state update
- Option B: `fix_refetch_after_delete` - Refetch pattern
- Optional: `implement_optimistic_ui_update` - Optimistic UI

3. `validate_immutable_state_updates` - Ensure React detects changes

**Phase 3: Validation**
4. `test_delete_ui_sync` - Comprehensive testing
5. `generate_deletion_sync_report` - Document fix

### Integration with Other Agents

- **Frontend-Auth-UI-Agent**: Validates UI updates correctly
- **Frontend-Backend-Auth-Integration**: Ensures API calls work
- **API-Backend-Guardian**: Validates backend deletion works
- **Frontend-UI-Professional**: Validates deletion UX

---

## Success Criteria

Task-Deletion-UI-Sync PASSES when:
- ✅ Task disappears immediately after successful delete
- ✅ No page reload required to see deletion
- ✅ Failed deletion keeps task visible with error message
- ✅ Loading indicator shown during API call
- ✅ Success toast shown after deletion
- ✅ Page refresh confirms deletion persisted
- ✅ No console errors during deletion
- ✅ Multiple deletions work correctly
- ✅ State updates use immutable patterns

Task-Deletion-UI-Sync FAILS when:
- ❌ Task remains visible after successful delete
- ❌ Page reload required to see deletion
- ❌ Failed deletion removes task from UI
- ❌ No loading indicator shown
- ❌ Console errors during deletion
- ❌ State mutations (splice, direct assignment)
- ❌ Race conditions with multiple deletes
- ❌ Confirmation dialog not working

---

## Notes

- This is a common React state management issue (forgetting to update state after API)
- Pattern applies to ALL CRUD operations (create, update, delete)
- Always update state immutably (filter, map, spread)
- Consider refetch pattern for complex state or multi-user scenarios
- Optimistic UI is advanced pattern - start with simpler wait-for-API pattern
- Test deletion with network throttling to catch race conditions
- Confirmation dialogs are UX best practice for destructive operations
