# TaskDeleteUserFeedbackSkill

**Agent:** task-deletion-reliability-fixer
**Purpose:** Show correct success message "Task deleted successfully", show error message ONLY on real failure, and ensure messages align with backend response.

---

## Context

**When to Use This Skill:**
- When success toast shows for failed deletions
- When error toast shows for successful deletions
- When toast messages are generic instead of specific
- When toast variant (color) doesn't match message type

**Symptoms Indicating This Skill is Needed:**
- Green success toast but task deletion failed
- Red error toast but task was actually deleted
- Message says "Task deleted successfully" but task still visible
- Message says "Failed to delete task" but task is gone
- Toast doesn't appear at all after deletion

---

## Problem Analysis

### Root Cause Scenarios

1. **Toast Called in Wrong Block:**
   - Success toast in `catch` block
   - Error toast in `try` block
   - Inverted feedback logic

2. **Toast Variant Hardcoded:**
   - All toasts show green (success variant)
   - Error messages display with success styling
   - User confused by mismatched color and message

3. **Toast Not Called:**
   - State updates but no feedback shown
   - User unsure if action succeeded
   - Silent failures

4. **Generic Messages:**
   - Same message for all errors (network, 404, 403, 500)
   - User can't diagnose issue
   - Poor UX

---

## Execution Steps

### Step 1: Locate Toast Functions

**Goal:** Find where success and error toasts are defined.

**Actions:**
```bash
# Search for toast functions
grep -n "showSuccessToast\|showErrorToast\|setToast\|Toast" frontend/src/app/(protected)/dashboard/page.tsx

# Check Toast component
grep -n "variant\|success\|error" frontend/src/components/ui/Toast.tsx
```

**Expected Findings:**
- `showSuccessToast(message: string)` function
- `showErrorToast(message: string)` function
- Toast component with `variant` prop
- Variants: `success`, `error`, `warning`, `info`

**Document:**
```markdown
Toast System:
- Success function: showSuccessToast (line XX)
- Error function: showErrorToast (line XX)
- Toast component: src/components/ui/Toast.tsx
- Variants: [success, error, warning, info]
```

---

### Step 2: Inspect DELETE Handler Toast Calls

**Goal:** Verify toast calls are in correct try/catch blocks with correct messages.

**Actions:**
```typescript
// Read handleConfirmDelete completely
const handleConfirmDelete = async () => {
  if (!taskToDelete) return;

  setDeleteLoading(true);

  try {
    await apiRequest(`/api/tasks/${taskToDelete}`, {
      method: "DELETE",
    });

    setTasks(tasks.filter((t) => t.id !== taskToDelete));

    // ✅ SUCCESS TOAST SHOULD BE HERE
    showSuccessToast("Task deleted successfully!");

    setDeleteConfirmOpen(false);
    setTaskToDelete(null);
  } catch (error) {
    setError(error);

    // ✅ ERROR TOAST SHOULD BE HERE
    showErrorToast("Failed to delete task. Please try again.");
  } finally {
    setDeleteLoading(false);
  }
};
```

**Key Investigation Points:**
1. **Success toast location:**
   - Inside `try` block? ✅
   - After API call? ✅
   - After state update? ✅

2. **Error toast location:**
   - Inside `catch` block? ✅
   - Includes error details? (optional)

3. **Toast message accuracy:**
   - Success: "Task deleted successfully!" ✅
   - Error: "Failed to delete task. Please try again." ✅

**Document:**
```markdown
Toast Call Analysis:
- Success toast location: [try block | catch block | missing]
- Error toast location: [try block | catch block | missing]
- Success message: "[actual message]"
- Error message: "[actual message]"
```

---

### Step 3: Verify Toast Function Implementations

**Goal:** Ensure showSuccessToast and showErrorToast set correct variants.

**Actions:**
```typescript
// Check toast helper functions
const showSuccessToast = (message: string) => {
  setToastMessage(message);
  setToastVariant("success");  // ✅ Must be "success"
  setShowToast(true);
};

const showErrorToast = (message: string) => {
  setToastMessage(message);
  setToastVariant("error");  // ✅ Must be "error"
  setShowToast(true);
};
```

**Key Investigation Points:**
1. **Variant setting:**
   - Success function sets `variant="success"`? ✅
   - Error function sets `variant="error"`? ✅

2. **State updates:**
   - Sets toast message? ✅
   - Sets visibility to true? ✅

3. **Function exists:**
   - Both functions defined? ✅
   - Called from correct locations? ✅

**Document:**
```markdown
Toast Functions:
- showSuccessToast sets variant: [success | error | hardcoded]
- showErrorToast sets variant: [success | error | hardcoded]
- Functions defined: [yes/no]
```

---

### Step 4: Check Toast Component Variant Handling

**Goal:** Ensure Toast component renders different styles for different variants.

**Actions:**
```typescript
// File: frontend/src/components/ui/Toast.tsx

// Check variant prop
interface ToastProps {
  message: string;
  variant: "success" | "error" | "warning" | "info";  // ✅ Should support all
  isVisible: boolean;
  onDismiss: () => void;
}

// Check variant-based styling
const variantStyles = {
  success: "bg-green-50 border-green-200 text-green-800",  // ✅ Green
  error: "bg-red-50 border-red-200 text-red-800",  // ✅ Red
  warning: "bg-yellow-50 border-yellow-200 text-yellow-800",
  info: "bg-blue-50 border-blue-200 text-blue-800",
};
```

**Key Investigation Points:**
1. **Variant prop type:**
   - Accepts "success" and "error"? ✅
   - Type-safe? ✅

2. **Styling applied:**
   - Different background colors? ✅
   - Different text colors? ✅
   - Different icons? ✅

3. **Default variant:**
   - Has safe default? ✅
   - Handles invalid variants? ✅

**Document:**
```markdown
Toast Component:
- Supports variants: [success, error, warning, info]
- Success style: [green | other]
- Error style: [red | other]
- Variant applied: [yes/no]
```

---

### Step 5: Test All Toast Scenarios

**Goal:** Verify toast feedback for all deletion outcomes.

**Test Cases:**

**Test 1: Successful Deletion**
1. Delete a task
2. Expected:
   - ✅ Green toast appears
   - ✅ Message: "Task deleted successfully!"
   - ✅ Task removed from UI

**Test 2: Network Error**
1. Stop backend server
2. Try to delete task
3. Expected:
   - ✅ Red toast appears
   - ✅ Message: "Failed to delete task. Please try again."
   - ✅ Task remains visible

**Test 3: Permission Error (403)**
1. Try to delete another user's task
2. Expected:
   - ✅ Red toast appears
   - ✅ Message: "Failed to delete task. Please try again."
   - ✅ Task remains visible

**Test 4: Not Found Error (404)**
1. Delete task that was already deleted
2. Expected:
   - ✅ Red toast appears
   - ✅ Message: "Failed to delete task. Please try again."
   - ✅ UI handles gracefully

**Document Results:**
```markdown
Toast Testing:
- Success case: [correct variant + message]
- Network error: [correct variant + message]
- Permission error: [correct variant + message]
- Not found error: [correct variant + message]
```

---

## Solution Strategy

### Fix 1: Create Toast Helper Functions (if missing)

**Issue:** No dedicated functions for showing toasts.

**Fix Location:** `frontend/src/app/(protected)/dashboard/page.tsx`

**Fix Strategy:**
```typescript
// Add toast state if missing
const [toastMessage, setToastMessage] = useState("");
const [toastVariant, setToastVariant] = useState<"success" | "error">("success");
const [showToast, setShowToast] = useState(false);

// Add toast helper functions
const showSuccessToast = (message: string) => {
  setToastMessage(message);
  setToastVariant("success");
  setShowToast(true);
};

const showErrorToast = (message: string) => {
  setToastMessage(message);
  setToastVariant("error");
  setShowToast(true);
};
```

---

### Fix 2: Call Toast Functions in Correct Locations

**Issue:** Toast called in wrong try/catch block or not called at all.

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

    setTasks(tasks.filter((t) => t.id !== taskToDelete));

    // ✅ SUCCESS TOAST IN TRY BLOCK
    showSuccessToast("Task deleted successfully!");

    setDeleteConfirmOpen(false);
    setTaskToDelete(null);
  } catch (error) {
    setError(error);

    // ✅ ERROR TOAST IN CATCH BLOCK
    showErrorToast("Failed to delete task. Please try again.");
  } finally {
    setDeleteLoading(false);
  }
};
```

---

### Fix 3: Fix Hardcoded Toast Variant

**Issue:** All toasts show green even for errors.

**Wrong Implementation:**
```typescript
// ❌ BAD: Hardcoded variant
<Toast
  message={toastMessage}
  variant="success"  // Always green!
  isVisible={showToast}
  onDismiss={() => setShowToast(false)}
/>
```

**Correct Implementation:**
```typescript
// ✅ GOOD: Dynamic variant
const [toastVariant, setToastVariant] = useState<"success" | "error">("success");

<Toast
  message={toastMessage}
  variant={toastVariant}  // Dynamic based on success/error
  isVisible={showToast}
  onDismiss={() => setShowToast(false)}
/>
```

---

### Fix 4: Enhance Error Messages (Optional)

**Issue:** Generic error message doesn't help user understand issue.

**Basic (Current):**
```typescript
showErrorToast("Failed to delete task. Please try again.");
```

**Enhanced (Optional):**
```typescript
catch (error) {
  let errorMessage = "Failed to delete task. Please try again.";

  if (error instanceof ApiException) {
    if (error.status === 403) {
      errorMessage = "You don't have permission to delete this task.";
    } else if (error.status === 404) {
      errorMessage = "Task not found. It may have been already deleted.";
    } else if (error.status === 500) {
      errorMessage = "Server error. Please try again later.";
    }
  } else {
    errorMessage = "Network error. Check your connection and try again.";
  }

  setError(error);
  showErrorToast(errorMessage);
}
```

---

## Acceptance Criteria

**MUST Pass All:**
- [ ] Successful deletion shows green "Task deleted successfully!" toast
- [ ] Failed deletion shows red "Failed to delete task" toast
- [ ] Success toast appears ONLY when task is deleted
- [ ] Error toast appears ONLY when deletion fails
- [ ] Toast variant (color) matches message type
- [ ] Toast appears for 3-5 seconds then auto-dismisses
- [ ] Toast can be manually dismissed by clicking X
- [ ] Multiple toasts queue properly (don't overlap)

**Test Matrix:**
| Scenario | Expected Toast | Variant | Task UI |
|----------|----------------|---------|---------|
| Success (204) | "Task deleted successfully!" | success (green) | Removed |
| Network error | "Failed to delete task" | error (red) | Visible |
| 403 Forbidden | "Failed to delete task" | error (red) | Visible |
| 404 Not Found | "Failed to delete task" | error (red) | Visible |
| 500 Server Error | "Failed to delete task" | error (red) | Visible |

---

## Implementation Checklist

**Phase 1: Diagnosis**
- [ ] Locate toast functions (showSuccessToast, showErrorToast)
- [ ] Check DELETE handler toast call locations
- [ ] Verify Toast component variant handling
- [ ] Test current toast behavior

**Phase 2: Fix**
- [ ] Create toast helper functions if missing
- [ ] Move success toast to try block
- [ ] Move error toast to catch block
- [ ] Fix hardcoded variant to dynamic
- [ ] Enhance error messages (optional)

**Phase 3: Testing**
- [ ] Test successful deletion → green toast
- [ ] Test network error → red toast
- [ ] Test permission error → red toast
- [ ] Verify toast auto-dismisses
- [ ] Verify toast can be manually dismissed

---

## Error Handling

**If Toast Doesn't Appear:**

1. **Check console for errors**
2. **Verify Toast component is rendered**
   ```typescript
   <Toast
     message={toastMessage}
     variant={toastVariant}
     isVisible={showToast}  // Check this is true
     onDismiss={() => setShowToast(false)}
   />
   ```
3. **Check z-index** (toast might be behind other elements)

**If Wrong Color Shown:**

1. **Check toastVariant state value**
2. **Verify variant prop passed to Toast component**
3. **Check Toast component variant styling**

**If Toast Doesn't Dismiss:**

1. **Check auto-dismiss timer in Toast component**
2. **Verify onDismiss callback works**
3. **Check isVisible state updates**

---

## Related Skills

- **TaskDeleteApiResponseValidationSkill** - Validates API responses to determine success/error
- **TaskDeleteFrontendStateSyncSkill** - Syncs UI state after deletion
- **task-deletion-ui-sync** (agent) - Parent agent coordinating all deletion fixes

---

## Notes

**Key Principle:**
> User feedback must be immediate, accurate, and visually distinct. Success and error states must be unmistakable.

**Common Pitfall:**
> Showing generic "success" message when operation failed. Always verify backend response before showing success feedback.

**Best Practice:**
> Toast messages should:
> 1. Be concise (5-10 words)
> 2. State what happened ("Task deleted")
> 3. Be actionable ("Try again", "Check connection")
> 4. Match the visual variant (green=success, red=error)

**Accessibility:**
> Toasts should:
> - Have ARIA role="alert" for screen readers
> - Include both color AND icon (not just color)
> - Auto-dismiss after 3-5 seconds
> - Be manually dismissible
