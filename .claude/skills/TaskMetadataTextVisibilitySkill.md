# TaskMetadataTextVisibilitySkill

**Agent:** task-metadata-visibility-fixer
**Purpose:** Fix font color for task priority (Low/Medium/High), due date, and tags in task list to ensure readability without breaking layout.

---

## Context

**When to Use This Skill:**
- When priority labels appear invisible or low-contrast in task list
- When due dates are unreadable (white/light gray on white background)
- When tags in task items have invisible text
- When metadata is visible in form but not in task list

**Symptoms Indicating This Skill is Needed:**
- Priority badges show colored backgrounds but no text
- Due dates invisible or barely visible
- Tags in task list unreadable (different from TaskForm)
- Users report "can't see task details in list"
- Metadata only visible on hover or selection

---

## Problem Analysis

### Root Cause Scenarios

1. **Priority Badge Text Color:**
   - Badge has colored background (`bg-red-100`, `bg-yellow-100`, `bg-green-100`)
   - Text is white or light (`text-white`, `text-gray-100`)
   - Low contrast = unreadable

2. **Due Date Text Color:**
   - Due date uses light text color (`text-gray-300`, `text-white`)
   - Background is white or light gray
   - Text blends into background

3. **Tag Text Color in List:**
   - Different component than TaskForm tags
   - May have different styling
   - White on white issue

4. **Inconsistent Styles:**
   - Metadata visible in form but not in list
   - Different Tailwind classes used
   - Styling not synchronized

---

## Execution Steps

### Step 1: Locate TaskItem Component

**Goal:** Find where individual task items are rendered in the list.

**Actions:**
```bash
# Find TaskItem component
find frontend/src -name "*TaskItem*" -type f

# Check for metadata rendering
grep -n "priority\|dueDate\|due_date\|tags" frontend/src/components/tasks/TaskItem.tsx
```

**Expected Findings:**
- Component: `frontend/src/components/tasks/TaskItem.tsx`
- Priority badge: `<span className="...">{task.priority}</span>`
- Due date: `<span className="...">{task.due_date}</span>`
- Tags: `{task.tags.map(...)}`

**Document:**
```markdown
TaskItem Component:
- File: frontend/src/components/tasks/TaskItem.tsx
- Priority badge: (line XX)
- Due date display: (line XX)
- Tags display: (line XX)
```

---

### Step 2: Inspect Priority Badge Styling

**Goal:** Identify current color classes for priority badges.

**Actions:**
```typescript
// Read TaskItem.tsx
// Look for priority badge rendering:

const priorityStyles = {
  high: "bg-red-100 ...",     // ← Check for text color
  medium: "bg-yellow-100 ...", // ← Check for text color
  low: "bg-green-100 ...",     // ← Check for text color
};

<span className={priorityStyles[task.priority]}>
  {task.priority}
</span>
```

**Key Investigation Points:**
1. **Background colors:**
   - High: `bg-red-100` (light red)
   - Medium: `bg-yellow-100` (light yellow)
   - Low: `bg-green-100` (light green)

2. **Text colors:**
   - High: `text-red-800` (dark red) ✅ OR `text-white` ❌
   - Medium: `text-yellow-800` (dark yellow) ✅ OR `text-white` ❌
   - Low: `text-green-800` (dark green) ✅ OR `text-white` ❌

3. **Missing text color:**
   - No `text-*` class? → Browser default or inherited

**Document:**
```markdown
Priority Badge Styles:
- High bg: [bg-red-100 | other]
- High text: [text-red-800 | text-white | MISSING]
- Medium bg: [bg-yellow-100 | other]
- Medium text: [text-yellow-800 | text-white | MISSING]
- Low bg: [bg-green-100 | other]
- Low text: [text-green-800 | text-white | MISSING]
```

---

### Step 3: Inspect Due Date Styling

**Goal:** Identify current color classes for due date display.

**Actions:**
```typescript
// Look for due date rendering:

{task.due_date && (
  <span className="...">  // ← Check this className
    📅 {formatDate(task.due_date)}
  </span>
)}
```

**Key Investigation Points:**
1. **Current text color:**
   - `text-gray-500` (medium gray) ✅ Visible on white
   - `text-gray-300` (light gray) ❌ Low contrast on white
   - `text-white` ❌ Invisible on white
   - No class? → Inherited

2. **Icon color:**
   - Emoji (📅) always visible ✅
   - SVG icon? → Check `fill` or `stroke` color

3. **Conditional styling:**
   - Overdue tasks different color?
   - Today's tasks highlighted?

**Document:**
```markdown
Due Date Styles:
- Text color: [text-gray-500 | text-gray-300 | MISSING]
- Icon: [emoji | svg + color]
- Conditional styling: [yes/no]
```

---

### Step 4: Inspect Tags Styling in List

**Goal:** Identify current color classes for tags in task items.

**Actions:**
```typescript
// Look for tags rendering in TaskItem:

{task.tags && task.tags.length > 0 && (
  <div className="...">
    {task.tags.map((tag, index) => (
      <span
        key={index}
        className="..."  // ← Check this
      >
        {tag}
      </span>
    ))}
  </div>
)}
```

**Key Investigation Points:**
1. **Background color:**
   - Same as TaskForm? (`bg-blue-100`)
   - Different? (`bg-gray-200`)

2. **Text color:**
   - Same as TaskForm? (`text-blue-800`)
   - Different or missing?

3. **Consistency:**
   - Do tags in list match tags in form?
   - Should they be identical?

**Document:**
```markdown
Tags in List Styles:
- Background: [bg-blue-100 | bg-gray-200 | other]
- Text: [text-blue-800 | MISSING | other]
- Matches TaskForm: [yes/no]
```

---

### Step 5: Test Current Visibility in Browser

**Goal:** Reproduce issue visually for all three metadata types.

**Actions:**
1. **Open app and navigate to dashboard**
2. **Create test tasks:**
   - Task 1: High priority, due today, tags: ["urgent", "work"]
   - Task 2: Medium priority, due tomorrow, tags: ["meeting"]
   - Task 3: Low priority, due next week, tags: ["personal"]

3. **Observe task list:**
   - Can you read priority labels?
   - Can you read due dates?
   - Can you read tags?
   - Screenshot for documentation

**Expected Issues:**
- Priority: Colored backgrounds, invisible text
- Due dates: Barely visible gray
- Tags: White on light background

**Document:**
```markdown
Visual Test Results:
- Priority readable: [yes/no]
- Due dates readable: [yes/no]
- Tags readable: [yes/no]
- Screenshot: [attach or describe]
```

---

## Solution Strategy

### Fix 1: Priority Badge Text Colors

**Issue:** Priority badges have light backgrounds but white or missing text colors.

**Fix Location:** `frontend/src/components/tasks/TaskItem.tsx` - Priority badge rendering

**Current (Broken):**
```typescript
const priorityStyles = {
  high: "bg-red-100 px-2 py-0.5 rounded text-xs uppercase",     // ❌ No text color
  medium: "bg-yellow-100 px-2 py-0.5 rounded text-xs uppercase", // ❌ No text color
  low: "bg-green-100 px-2 py-0.5 rounded text-xs uppercase",     // ❌ No text color
};
```

**Fixed:**
```typescript
const priorityStyles = {
  high: "bg-red-100 text-red-800 px-2 py-0.5 rounded text-xs font-semibold uppercase",
  // ✅ Added text-red-800 for dark red text on light red background

  medium: "bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded text-xs font-semibold uppercase",
  // ✅ Added text-yellow-800 for dark yellow text on light yellow background

  low: "bg-green-100 text-green-800 px-2 py-0.5 rounded text-xs font-semibold uppercase",
  // ✅ Added text-green-800 for dark green text on light green background
};

<span className={priorityStyles[task.priority]}>
  {task.priority}
</span>
```

**Color Pairing for Priority:**
| Priority | Background | Text | Contrast Ratio |
|----------|------------|------|----------------|
| High | `bg-red-100` (#FEE2E2) | `text-red-800` (#991B1B) | 7.1:1 ✅ |
| Medium | `bg-yellow-100` (#FEF3C7) | `text-yellow-800` (#92400E) | 8.2:1 ✅ |
| Low | `bg-green-100` (#D1FAE5) | `text-green-800` (#166534) | 7.8:1 ✅ |

---

### Fix 2: Due Date Text Color

**Issue:** Due dates use light gray text that's barely visible.

**Fix Location:** `frontend/src/components/tasks/TaskItem.tsx` - Due date rendering

**Current (Broken):**
```typescript
{task.due_date && (
  <span className="text-sm text-gray-300 flex items-center gap-1">
    {/* ❌ text-gray-300 is too light on white background */}
    📅 {formatDate(task.due_date)}
  </span>
)}
```

**Fixed:**
```typescript
{task.due_date && (
  <span className="text-sm text-gray-700 flex items-center gap-1">
    {/* ✅ text-gray-700 is dark enough for readability */}
    📅 {formatDate(task.due_date)}
  </span>
)}
```

**Enhanced with Overdue Highlighting:**
```typescript
{task.due_date && (
  <span
    className={`text-sm flex items-center gap-1 ${
      isOverdue(task.due_date)
        ? "text-red-600 font-semibold"  // Overdue: red + bold
        : "text-gray-700"                // Normal: dark gray
    }`}
  >
    📅 {formatDate(task.due_date)}
  </span>
)}
```

---

### Fix 3: Tags Text Color in List

**Issue:** Tags in task list have different styling than TaskForm, may be unreadable.

**Fix Location:** `frontend/src/components/tasks/TaskItem.tsx` - Tags rendering

**Current (Broken):**
```typescript
{task.tags.map((tag, index) => (
  <span
    key={index}
    className="bg-blue-100 px-2 py-0.5 rounded-full text-xs"
    // ❌ No text color class
  >
    {tag}
  </span>
))}
```

**Fixed (Consistent with TaskForm):**
```typescript
{task.tags.map((tag, index) => (
  <span
    key={index}
    className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full text-xs"
    // ✅ Added text-blue-800 to match TaskForm tags
  >
    {tag}
  </span>
))}
```

**Alternative (Gray Tags):**
```typescript
{task.tags.map((tag, index) => (
  <span
    key={index}
    className="bg-gray-200 text-gray-800 px-2 py-0.5 rounded-full text-xs"
    // ✅ Neutral gray tags
  >
    {tag}
  </span>
))}
```

---

### Fix 4: Comprehensive Metadata Styling

**Issue:** All metadata needs consistent, readable styling.

**Fix Location:** `frontend/src/components/tasks/TaskItem.tsx` - Complete component

**Comprehensive Fix:**
```typescript
export default function TaskItem({ task, onToggle, onEdit, onDelete }: TaskItemProps) {
  // Priority styles with high contrast
  const priorityStyles = {
    high: "bg-red-100 text-red-800 px-2 py-0.5 rounded text-xs font-semibold uppercase",
    medium: "bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded text-xs font-semibold uppercase",
    low: "bg-green-100 text-green-800 px-2 py-0.5 rounded text-xs font-semibold uppercase",
  };

  return (
    <div className="task-item border rounded-lg p-4 bg-white">
      {/* Task description */}
      <div className="flex items-start justify-between">
        <p className="text-gray-900 flex-1">{task.description}</p>
      </div>

      {/* Metadata row */}
      <div className="mt-3 flex flex-wrap items-center gap-2">
        {/* Priority badge */}
        <span className={priorityStyles[task.priority]}>
          {task.priority}
        </span>

        {/* Due date */}
        {task.due_date && (
          <span className="text-sm text-gray-700 flex items-center gap-1">
            📅 {formatDate(task.due_date)}
          </span>
        )}

        {/* Tags */}
        {task.tags && task.tags.length > 0 && (
          <div className="flex gap-1 flex-wrap">
            {task.tags.map((tag, index) => (
              <span
                key={index}
                className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full text-xs"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Action buttons */}
      <div className="mt-3 flex gap-2">
        {/* ... buttons ... */}
      </div>
    </div>
  );
}
```

---

## Acceptance Criteria

**MUST Pass All:**
- [ ] Priority badges have readable text (dark on light)
- [ ] High priority: Red background + dark red text
- [ ] Medium priority: Yellow background + dark yellow text
- [ ] Low priority: Green background + dark green text
- [ ] Due dates have readable text (gray-700 or darker)
- [ ] Tags have readable text (blue-800 or gray-800)
- [ ] All metadata has minimum 4.5:1 contrast ratio
- [ ] Styling consistent with TaskForm where applicable
- [ ] No layout shifts or visual glitches

**Visual Requirements:**
| Element | Background | Text | Contrast |
|---------|------------|------|----------|
| High Priority | `bg-red-100` | `text-red-800` | 7.1:1 ✅ |
| Medium Priority | `bg-yellow-100` | `text-yellow-800` | 8.2:1 ✅ |
| Low Priority | `bg-green-100` | `text-green-800` | 7.8:1 ✅ |
| Due Date | N/A (transparent) | `text-gray-700` | 4.8:1 ✅ |
| Tags | `bg-blue-100` | `text-blue-800` | 8.5:1 ✅ |

**Test Cases:**
1. **High Priority Task:** Create task → Priority badge readable
2. **Medium Priority Task:** Create task → Priority badge readable
3. **Low Priority Task:** Create task → Priority badge readable
4. **Due Date:** Set due date → Date text readable
5. **Multiple Tags:** Add 3 tags → All tags readable
6. **All Metadata:** Task with all metadata → Everything readable

---

## Implementation Checklist

**Phase 1: Diagnosis**
- [ ] Locate TaskItem.tsx component
- [ ] Identify priority badge styling
- [ ] Identify due date styling
- [ ] Identify tags styling
- [ ] Test current visibility in browser

**Phase 2: Fix**
- [ ] Add text colors to priority badges
- [ ] Change due date text from gray-300 to gray-700
- [ ] Add text colors to tags
- [ ] Verify consistency with TaskForm
- [ ] Add font-semibold for better readability

**Phase 3: Testing**
- [ ] Create tasks with all priority levels
- [ ] Add due dates to tasks
- [ ] Add multiple tags to tasks
- [ ] Verify all metadata readable
- [ ] Test in different browsers
- [ ] Test production build

---

## Error Handling

**If Priority Text Still Invisible:**

1. **Check browser DevTools:**
   - Inspect priority badge element
   - Check computed `color` style
   - Look for conflicting CSS

2. **Check priority value:**
   - Is `task.priority` lowercase? ("high" vs "High")
   - Does it match keys in `priorityStyles` object?

3. **Check Tailwind purge:**
   - Are color classes in final CSS?
   - Add to safelist if needed

**If Due Dates Barely Visible:**

1. **Try darker text:**
   - `text-gray-700` → `text-gray-900`
   - `text-gray-800` → More contrast

2. **Check parent opacity:**
   - Parent might have `opacity-50`

**If Tags Different in List vs Form:**

1. **Synchronize classes:**
   - Use exact same className for consistency
   - Extract to shared constant if needed

---

## Related Skills

- **TagInputTextVisibilitySkill** - Fixes tag text in TaskForm (not list)
- **frontend-ui-professional** (agent) - General UI/UX quality review
- **TaskDeleteUserFeedbackSkill** - Toast message styling (related pattern)

---

## Notes

**Key Principle:**
> Metadata should be scannable at a glance. Use consistent color coding with high contrast for instant recognition.

**Common Pitfall:**
> Using brand colors for metadata without considering contrast. Always test light background + light text combinations.

**Best Practice:**
> Priority badges should use semantic colors:
> - **High**: Red (urgency, danger)
> - **Medium**: Yellow/Orange (caution, attention)
> - **Low**: Green (calm, low risk)
>
> Always pair with appropriately dark text (-800 or -900 suffix).

**Accessibility:**
> Color-blind users benefit from:
> - Text labels (not just color coding)
> - Icons in addition to colors
> - High contrast regardless of hue
> - Consistent positioning of metadata

**Design Consistency:**
> Metadata styling should match across:
> - Task list items
> - Task creation form
> - Task edit form
> - Task detail view (if exists)
>
> Use shared Tailwind classes or components for consistency.
