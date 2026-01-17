# Task-Registration-Fixer Skills

**Agent Purpose**: Fix three specific issues in the Todo App: (1) Task deletion UI sync with success messages, (2) Task sorting dropdown functionality for all options, (3) Registration form Name field integration with backend.

**Context**:
- Frontend: React 19 with Next.js 15 App Router
- State management: useState for task list and form state
- Backend: FastAPI with JWT authentication, httpOnly cookies
- Task operations: CRUD via REST API (/api/tasks)
- Registration: POST /api/auth/register with email, password, name
- Current issues: Delete works but no success message, sorting doesn't reorder UI, Name field missing

**Boundaries**:
- This agent focuses ONLY on these three specific fixes
- Does NOT refactor unrelated code
- Does NOT change overall architecture
- Does NOT modify backend logic (only integration)

**Safety Rules**:
- NEVER remove existing functionality
- NEVER bypass authentication or validation
- NEVER introduce security vulnerabilities
- Changes must maintain backward compatibility

---

## Skill 1: fix_task_deletion_success_message

### Purpose
Ensure task deletion displays "Task deleted successfully!" message immediately after successful deletion and updates UI without page reload.

### Validations / Rules
- **Verify current delete flow**:
  ```typescript
  // Current implementation should have:
  const handleConfirmDelete = async () => {
    try {
      await apiRequest(`/api/tasks/${taskToDelete}`, { method: "DELETE" });
      setTasks(tasks.filter((t) => t.id !== taskToDelete));
      showSuccessToast("Task deleted successfully!");  // ✅ Check this exists
    } catch (error) {
      // Error handling
    }
  };
  ```
- **Success message requirements**:
  - Message text MUST be: "Task deleted successfully!"
  - Must use existing toast/notification system
  - Must appear AFTER API success
  - Must be visible for 3-5 seconds
  - Must auto-dismiss
- **UI update requirements**:
  - Task removed from state immediately
  - No page reload required
  - Smooth transition (no flicker)
  - Task count updates
- **Timing**:
  - Message shows AFTER state update
  - Message shows BEFORE dialog closes

### Fail Conditions
- No success message shown after delete
- Wrong message text (not "Task deleted successfully!")
- Message shows before deletion completes
- UI doesn't update (task still visible)
- Page reload required to see deletion
- Toast notification component missing

### Used By
- Task-Deletion-UI-Sync (validates deletion sync)
- Frontend-UI-Professional (validates toast UX)
- Frontend-Auth-UI-Agent (validates UI updates)

---

## Skill 2: fix_task_sorting_dropdown

### Purpose
Implement complete task sorting functionality for all four dropdown options: Nearest First, A-Z, Due Date, and Priority High to Low.

### Validations / Rules
- **Sort options to implement**:
  1. **Nearest First** (sort by `created_at`, newest first)
     - API: `?sort_by=created&order=desc`
     - Frontend: Display newest tasks at top

  2. **A-Z** (sort by `description`, alphabetical)
     - API: `?sort_by=title&order=asc` (or `description`)
     - Frontend: Display tasks alphabetically by description

  3. **Due Date** (sort by `due_date`, soonest first)
     - API: `?sort_by=due_date&order=asc`
     - Frontend: Display tasks with nearest due date first
     - Handle tasks without due dates (put at end)

  4. **Priority High to Low** (sort by `priority`, high → medium → low)
     - API: `?sort_by=priority&order=desc`
     - Frontend: Display high priority first, then medium, then low

- **Implementation pattern**:
  ```typescript
  const [sortBy, setSortBy] = useState("created");

  const handleSortChange = (newSort: string) => {
    setSortBy(newSort);
    // Trigger refetch with new sort parameter
  };

  // In fetchTasks:
  const params = new URLSearchParams();
  if (sortBy) {
    params.append("sort_by", sortBy);
    params.append("order", getOrderForSort(sortBy));
  }
  ```

- **Dropdown requirements**:
  - All 4 options visible in dropdown
  - Selected option highlighted
  - Clicking option triggers immediate re-sort
  - Tasks reorder without page reload
  - Loading indicator during fetch
  - Persists selection in localStorage (existing behavior)

- **Backend integration**:
  - Backend `/api/tasks` endpoint supports `sort_by` parameter
  - Backend supports `order` parameter (asc/desc)
  - Frontend sends correct parameter names
  - Frontend handles response correctly

### Fail Conditions
- Dropdown exists but options don't work
- Clicking sort option has no effect
- Tasks don't reorder in UI
- Wrong sort order (e.g., Z-A instead of A-Z)
- Sort parameter not sent to backend
- Backend doesn't support sort parameter
- Page reload required to see sorted order

### Used By
- Frontend-UI-Professional (dropdown UX)
- API-Backend-Guardian (backend API validation)
- Frontend-Backend-Auth-Integration (API parameter passing)

---

## Skill 3: add_registration_name_field

### Purpose
Add a Name field to the registration form, validate it on frontend, and integrate with backend authentication API.

### Validations / Rules
- **Form field requirements**:
  ```typescript
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
  ```

- **Field position**:
  - Place BEFORE email field (top of form)
  - OR after email field (before password)
  - Match existing input styling
  - Consistent spacing with other fields

- **Validation rules**:
  - Required field (HTML `required` attribute)
  - Minimum 2 characters
  - Maximum 100 characters
  - No special validation (allow all characters)
  - Trim whitespace on submit
  - Show validation error if empty on submit

- **Backend integration**:
  ```typescript
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const requestData: RegisterRequest = {
      email,
      password,
      name: name.trim(),  // ✅ Add name field
    };

    const response = await apiRequestPublic<AuthResponse>("/api/auth/register", {
      method: "POST",
      body: requestData,
    });
  };
  ```

- **Backend API**:
  - Check if backend `/api/auth/register` accepts `name` field
  - If not, add to backend schema:
    ```python
    class RegisterRequest(BaseModel):
        email: EmailStr
        password: str
        name: str  # Add this field
    ```
  - Store name in User model
  - Return name in response

- **State management**:
  ```typescript
  const [name, setName] = useState("");
  ```

- **Error handling**:
  - If backend rejects name field, show error
  - If name too short/long, show validation error
  - Handle network errors gracefully

### Fail Conditions
- Name field not visible in form
- Name field not required
- Name not sent to backend API
- Backend doesn't accept name field
- Name not stored in database
- Form submission works without name (should fail)
- Validation not working (accepts empty name)

### Used By
- Frontend-Auth-UI-Agent (form validation)
- Auth-Integration-Auditor (backend integration)
- API-Backend-Guardian (backend schema validation)
- Security-Guardian (input validation)

---

## Skill 4: validate_task_deletion_complete_flow

### Purpose
Comprehensive validation that task deletion works correctly with immediate UI update, success message, and database persistence.

### Validations / Rules
- **Test flow**:
  1. User clicks delete button on a task
  2. Confirmation dialog appears
  3. User clicks "Delete" to confirm
  4. Loading spinner shows (button disabled)
  5. API call to DELETE /api/tasks/{id}
  6. Backend returns 200/204
  7. **IMMEDIATELY**: Task disappears from UI
  8. **IMMEDIATELY**: Toast shows "Task deleted successfully!"
  9. Dialog closes
  10. Task count updates (e.g., "5 tasks" → "4 tasks")
  11. Refresh page → Task still deleted (persisted)

- **Error scenario**:
  1. Backend returns error (500, 401, etc.)
  2. Task remains visible in UI
  3. Error message shown to user
  4. Dialog stays open (user can retry)

- **Edge cases**:
  - Delete last task → Empty state shows
  - Delete while filters active → Count updates correctly
  - Delete task at top/bottom of list → No jump scroll
  - Multiple rapid deletes → Each handled correctly

### Fail Conditions
- Task visible after successful delete
- No success message shown
- Wrong success message text
- Page reload required
- Task reappears after refresh (not persisted)
- Error not shown on failure
- Dialog closes on error (should stay open)

### Used By
- Phase2-Quality-Orchestrator (quality gate)
- Task-Deletion-UI-Sync (deletion validation)
- Frontend-UI-Professional (UX validation)

---

## Skill 5: validate_sorting_all_options

### Purpose
Systematically test all four sorting options to ensure tasks reorder correctly in UI.

### Validations / Rules
- **Test setup**:
  - Create 5+ tasks with:
    - Different descriptions (A, M, Z prefixes)
    - Different priorities (high, medium, low)
    - Different due dates (some with, some without)
    - Different creation times

- **Test Case 1: Nearest First**
  1. Select "Nearest First" from dropdown
  2. Verify: Newest task appears first
  3. Verify: Oldest task appears last
  4. Order: Most recently created → Oldest created

- **Test Case 2: A-Z**
  1. Select "A-Z" from dropdown
  2. Verify: Task starting with 'A' appears first
  3. Verify: Task starting with 'Z' appears last
  4. Order: Alphabetical by description

- **Test Case 3: Due Date**
  1. Select "Due Date" from dropdown
  2. Verify: Task with nearest due date first
  3. Verify: Tasks without due dates at end
  4. Order: Soonest due date → Latest due date → No due date

- **Test Case 4: Priority High to Low**
  1. Select "Priority High to Low" from dropdown
  2. Verify: High priority tasks first
  3. Verify: Medium priority in middle
  4. Verify: Low priority last
  5. Order: High → Medium → Low

- **Acceptance criteria for ALL tests**:
  - Tasks reorder within 500ms (API call + render)
  - No page reload required
  - Loading indicator shown during fetch
  - Selected sort persists on page refresh
  - No console errors

### Fail Conditions
- Any sort option doesn't work
- Tasks don't reorder
- Wrong sort order
- Page reload required
- Sort selection not persisted
- Console errors during sort

### Used By
- Frontend-UI-Professional (sorting UX)
- Phase2-Quality-Orchestrator (feature completeness)

---

## Skill 6: validate_registration_name_integration

### Purpose
Verify Name field is properly integrated in registration form and backend stores name correctly.

### Validations / Rules
- **Frontend validation**:
  1. Open registration page
  2. Verify Name field visible (above or below email)
  3. Try submit with empty name → Validation error
  4. Try submit with 1 character → Validation error (min 2)
  5. Enter valid name (2+ chars) → Submit works
  6. Verify name included in API request body

- **Backend validation**:
  1. Register with name "Test User"
  2. Check backend logs/database
  3. Verify name stored in user record
  4. Verify name returned in auth response

- **Integration validation**:
  1. Register with name "John Doe"
  2. After registration, check profile
  3. Verify name displays correctly (if UI shows name)
  4. Logout and login
  5. Verify name persists

- **Error scenarios**:
  1. Backend doesn't accept name field → Show clear error
  2. Name too long (>100 chars) → Validation error
  3. Network error during registration → Error shown

### Fail Conditions
- Name field not visible
- Name field not required
- Can submit without name
- Name not sent to backend
- Backend returns error about name field
- Name not stored in database
- Name not available after registration

### Used By
- Auth-Integration-Auditor (auth flow validation)
- Frontend-Auth-UI-Agent (form validation)
- API-Backend-Guardian (backend validation)

---

## Skill 7: implement_success_toast_system

### Purpose
Ensure success toast notification system is properly configured for all operations (delete, create, update).

### Validations / Rules
- **Toast component requirements**:
  ```typescript
  <Toast
    message={toastMessage}
    variant="success"  // or "error"
    isVisible={showToast}
    onDismiss={() => setShowToast(false)}
  />
  ```

- **Toast state management**:
  ```typescript
  const [toastMessage, setToastMessage] = useState("");
  const [showToast, setShowToast] = useState(false);

  const showSuccessToast = (message: string) => {
    setToastMessage(message);
    setShowToast(true);
  };
  ```

- **Toast behavior**:
  - Auto-dismiss after 3-5 seconds
  - Manual dismiss on click
  - Success variant: Green background
  - Position: Top-right or bottom-center
  - Animation: Slide in, fade out
  - Accessible (screen reader announces)

- **Integration points**:
  - After task created: "Task created successfully!"
  - After task updated: "Task updated successfully!"
  - After task deleted: "Task deleted successfully!"
  - After toggle completion: "Task marked as complete/incomplete!"

### Fail Conditions
- Toast component missing
- Toast doesn't show
- Toast doesn't auto-dismiss
- Toast shows wrong message
- Toast not accessible
- Multiple toasts stack incorrectly

### Used By
- Frontend-UI-Professional (notification UX)
- Web-UX-Optimization-Agent (user feedback)

---

## Skill 8: debug_sort_parameter_mismatch

### Purpose
Debug and fix any mismatch between frontend sort parameters and backend API expectations.

### Validations / Rules
- **Check frontend parameters**:
  ```typescript
  // What frontend sends:
  const params = new URLSearchParams();
  params.append("sort_by", "created");  // Check this matches backend
  params.append("order", "desc");       // Check this matches backend
  ```

- **Check backend expectations**:
  ```python
  # What backend expects:
  @router.get("")
  async def get_tasks(
      sort_by: Optional[str] = Query(None),  # "created", "title", "due_date", "priority"
      order: Optional[str] = Query("desc"),   # "asc" or "desc"
  ):
  ```

- **Common mismatches**:
  - Frontend sends "title" but backend expects "description"
  - Frontend sends "name" but backend expects "title"
  - Frontend sends "creation_date" but backend expects "created"
  - Frontend doesn't send "order" parameter

- **Fix pattern**:
  ```typescript
  // Map frontend sort options to backend parameters
  const sortMapping = {
    "nearest": { sort_by: "created_at", order: "desc" },
    "alphabetical": { sort_by: "description", order: "asc" },
    "due_date": { sort_by: "due_date", order: "asc" },
    "priority": { sort_by: "priority", order: "desc" },
  };

  const { sort_by, order } = sortMapping[selectedSort];
  params.append("sort_by", sort_by);
  params.append("order", order);
  ```

### Fail Conditions
- Frontend sends parameter backend doesn't recognize
- Backend returns error about invalid sort parameter
- Backend ignores sort parameter (no effect)
- Sort order reversed (asc/desc mismatch)

### Used By
- Frontend-Backend-Auth-Integration (parameter validation)
- API-Backend-Guardian (API contract validation)

---

## Agent Invocation Workflow

### When to Invoke Task-Registration-Fixer

**During Bug Reports**:
1. User reports "deleted task still visible"
2. User reports "no success message after delete"
3. User reports "sort dropdown doesn't work"
4. User reports "can't enter name during registration"

**During Feature Development**:
1. After implementing task deletion
2. After implementing sort dropdown
3. After implementing registration form
4. Before merging PR with these features

**During Testing**:
1. QA finds missing success messages
2. Integration tests show sorting not working
3. E2E tests fail on registration without name

### Skills Invocation Order (Recommended)

**Issue 1: Task Deletion + Success Message**
1. `validate_task_deletion_complete_flow` - Verify current behavior
2. `fix_task_deletion_success_message` - Ensure toast shows
3. `implement_success_toast_system` - Validate toast component
4. `validate_task_deletion_complete_flow` (rerun) - Confirm fix

**Issue 2: Task Sorting**
1. `validate_sorting_all_options` - Test all 4 options
2. `debug_sort_parameter_mismatch` - Check frontend-backend params
3. `fix_task_sorting_dropdown` - Implement correct sorting
4. `validate_sorting_all_options` (rerun) - Confirm all work

**Issue 3: Registration Name Field**
1. `validate_registration_name_integration` - Check current form
2. `add_registration_name_field` - Add Name field to form
3. `validate_registration_name_integration` (rerun) - Confirm integration

### Integration with Other Agents

- **Task-Deletion-UI-Sync**: Validates deletion behavior
- **Frontend-UI-Professional**: Validates toast UX and form layout
- **Frontend-Backend-Auth-Integration**: Validates API integration
- **API-Backend-Guardian**: Validates backend accepts parameters
- **Auth-Integration-Auditor**: Validates registration flow

---

## Success Criteria

Task-Registration-Fixer PASSES when:
- ✅ Task deletion shows "Task deleted successfully!" message
- ✅ Deleted task disappears immediately (no reload)
- ✅ All 4 sort options reorder tasks correctly
- ✅ Sort selection persists on page refresh
- ✅ Registration form has Name field (required)
- ✅ Name field validates (min 2 chars)
- ✅ Name sent to backend and stored
- ✅ No console errors during operations
- ✅ All existing functionality still works

Task-Registration-Fixer FAILS when:
- ❌ No success message after delete
- ❌ Task visible after delete
- ❌ Any sort option doesn't work
- ❌ Tasks don't reorder in UI
- ❌ Name field missing from registration
- ❌ Can register without name
- ❌ Backend doesn't accept/store name
- ❌ Existing features broken

---

## Notes

### Task Deletion Success Message
- Likely already implemented (check `showSuccessToast("Task deleted successfully!")`)
- If missing, just add one line to delete handler
- Verify Toast component exists and works

### Task Sorting
- Backend likely already supports sort parameters
- Frontend needs to send correct parameter names
- Check backend API documentation for exact parameter names
- Map dropdown options to backend parameters

### Registration Name Field
- Simple form field addition
- Check if backend User model has `name` field
- If not, backend needs schema update
- Coordinate with backend team if needed

### Common Pitfalls
- Parameter naming mismatch (frontend vs backend)
- Toast component not imported
- Name field validation not triggered
- Sort not persisting due to state management issue

### Testing Priority
1. **High**: Task deletion with message (user-facing, frequently used)
2. **High**: Sort functionality (core feature)
3. **Medium**: Registration name (one-time use, but important)
