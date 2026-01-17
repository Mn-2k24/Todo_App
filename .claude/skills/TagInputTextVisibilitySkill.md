# TagInputTextVisibilitySkill

**Agent:** task-metadata-visibility-fixer
**Purpose:** Fix font color of tags displayed under Add Task input to ensure text is visible on light background using Tailwind CSS utilities only.

---

## Context

**When to Use This Skill:**
- When tag text appears white/invisible on light background in TaskForm
- When users can't read tags they've entered in the Add Task form
- When tag input shows tag pills but text is unreadable
- When tag display works in task list but not in input form

**Symptoms Indicating This Skill is Needed:**
- Tag pills appear as colored rectangles with no visible text
- Text is barely visible (low contrast)
- Tags are white on white background
- Users report "can't see what tags I entered"

---

## Problem Analysis

### Root Cause Scenarios

1. **Text Color Hardcoded to White:**
   - Tag component uses `text-white` class
   - Background is light (gray-50, blue-50, etc.)
   - White on light = invisible

2. **Inherited Text Color:**
   - Parent element sets `text-white` or `text-gray-100`
   - Tag inherits this color
   - Background doesn't provide contrast

3. **Missing Text Color Class:**
   - Tag has background color but no text color
   - Browser default text color is light
   - No explicit dark text class applied

4. **Tailwind Purge Issue:**
   - Text color class defined but purged from production build
   - Works in dev, fails in production

---

## Execution Steps

### Step 1: Locate TaskForm Component

**Goal:** Find where tags are displayed under the Add Task input.

**Actions:**
```bash
# Find TaskForm component
find frontend/src -name "*TaskForm*" -type f

# Check for tag rendering in form
grep -n "tag\|Tag\|badge\|pill" frontend/src/components/tasks/TaskForm.tsx
```

**Expected Findings:**
- Component: `frontend/src/components/tasks/TaskForm.tsx`
- Tag input field: `<input ... placeholder="Add tags" />`
- Tag display: Array of tag pills below input
- Tag remove button: X or × icon

**Document:**
```markdown
TaskForm Component:
- File: frontend/src/components/tasks/TaskForm.tsx
- Tag input: (line XX)
- Tag display: (line XX)
- Tag pill component: [inline | separate component]
```

---

### Step 2: Inspect Tag Pill Rendering Code

**Goal:** Find exact HTML/JSX for tag pills to identify color classes.

**Actions:**
```typescript
// Read TaskForm.tsx
// Look for tag mapping:

{tags.map((tag, index) => (
  <span
    key={index}
    className="..."  // ← FIND THIS
  >
    {tag}
    <button onClick={() => removeTag(index)}>×</button>
  </span>
))}
```

**Key Investigation Points:**
1. **Background color class:**
   - Example: `bg-blue-100`, `bg-gray-200`, `bg-primary-100`

2. **Text color class:**
   - Example: `text-blue-800`, `text-gray-700`
   - **Check if MISSING** ← Common issue

3. **Current className string:**
   ```typescript
   className="bg-blue-100 px-2 py-1 rounded-full text-sm flex items-center gap-1"
   // Notice: No text-* class! Text defaults to parent or browser default
   ```

**Document:**
```markdown
Tag Pill Classes:
- Background: [bg-blue-100 | bg-gray-200 | other]
- Text color: [text-blue-800 | MISSING | other]
- Full className: "[exact string]"
```

---

### Step 3: Identify Contrast Issue

**Goal:** Determine exact color combination causing invisibility.

**Actions:**
1. **Note background color:**
   - `bg-blue-100` = Very light blue (#DBEAFE)
   - `bg-gray-200` = Light gray (#E5E7EB)
   - `bg-primary-100` = Light primary color

2. **Note current text color:**
   - `text-white` = White (#FFFFFF)
   - `text-gray-100` = Very light gray (#F3F4F6)
   - No class = Browser default (often black, but could be inherited)

3. **Check contrast ratio:**
   - White (#FFFFFF) on light blue (#DBEAFE) = **1.2:1** ❌ (WCAG requires 4.5:1)
   - Need dark text: `text-blue-800` (#1E40AF) on light blue = **8.5:1** ✅

**Document:**
```markdown
Contrast Analysis:
- Current background: [color name + hex]
- Current text: [color name + hex]
- Contrast ratio: [calculated ratio]
- WCAG compliant: [yes/no]
- Required fix: [text color needed]
```

---

### Step 4: Check Parent Element Styles

**Goal:** Ensure parent doesn't force white text color.

**Actions:**
```typescript
// Read parent div/container wrapping tags
<div className="...">  // ← Check this
  {tags.map((tag) => (
    <span className="...">  // ← And this
      {tag}
    </span>
  ))}
</div>
```

**Key Investigation Points:**
1. **Parent text color:**
   - Parent has `text-white`? → Tags inherit white text ❌
   - Parent has `text-gray-700`? → Tags inherit dark text ✅

2. **Form-level text color:**
   - Form component has global text color?
   - Could be affecting all child text

**Document:**
```markdown
Parent Styles:
- Parent div classes: "[exact classes]"
- Parent text color: [color class | none]
- Inheritance issue: [yes/no]
```

---

### Step 5: Test Current Visibility

**Goal:** Reproduce issue visually to confirm diagnosis.

**Actions:**
1. **Open app in browser**
2. **Navigate to Add Task form**
3. **Enter tags:** "urgent", "work", "meeting"
4. **Observe tag pills:**
   - Can you read the text?
   - Screenshot for documentation

**Expected Result:**
- Tags appear as colored pills
- Text is **invisible** or **barely visible**

**Document:**
```markdown
Visual Test:
- Tags visible: [yes/no]
- Text readable: [yes/no]
- Screenshot: [attach or describe]
```

---

## Solution Strategy

### Fix 1: Add Dark Text Color Class

**Issue:** Tag pills missing text color class, defaulting to white or inherited light color.

**Fix Location:** `frontend/src/components/tasks/TaskForm.tsx` - Tag pill rendering

**Current (Broken):**
```typescript
{tags.map((tag, index) => (
  <span
    key={index}
    className="bg-blue-100 px-2 py-1 rounded-full text-sm flex items-center gap-1"
    // ❌ No text color!
  >
    {tag}
    <button onClick={() => removeTag(index)}>×</button>
  </span>
))}
```

**Fixed:**
```typescript
{tags.map((tag, index) => (
  <span
    key={index}
    className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm flex items-center gap-1"
    // ✅ Added text-blue-800 for dark blue text
  >
    {tag}
    <button
      onClick={() => removeTag(index)}
      className="text-blue-600 hover:text-blue-800"
      // ✅ Explicit color for remove button
    >
      ×
    </button>
  </span>
))}
```

**Color Pairing Guidelines:**
| Background Class | Text Class (High Contrast) |
|------------------|----------------------------|
| `bg-blue-100` | `text-blue-800` or `text-blue-900` |
| `bg-gray-200` | `text-gray-800` or `text-gray-900` |
| `bg-green-100` | `text-green-800` or `text-green-900` |
| `bg-primary-100` | `text-primary-800` or `text-primary-900` |
| `bg-red-100` | `text-red-800` or `text-red-900` |

---

### Fix 2: Override Parent Text Color

**Issue:** Parent element forces white text, affecting all children.

**Fix Location:** `frontend/src/components/tasks/TaskForm.tsx` - Parent container

**Current (Broken):**
```typescript
<div className="mt-2 flex flex-wrap gap-2 text-white">
  {/* ❌ text-white affects all children */}
  {tags.map((tag) => (
    <span className="bg-blue-100 ...">
      {tag}  {/* Inherits white text */}
    </span>
  ))}
</div>
```

**Fixed:**
```typescript
<div className="mt-2 flex flex-wrap gap-2">
  {/* ✅ Removed text-white */}
  {tags.map((tag) => (
    <span className="bg-blue-100 text-blue-800 ...">
      {tag}  {/* Explicit dark text */}
    </span>
  ))}
</div>
```

**Or use override:**
```typescript
<div className="mt-2 flex flex-wrap gap-2 text-white">
  {tags.map((tag) => (
    <span className="bg-blue-100 !text-blue-800 ...">
      {/* ✅ !important override with ! prefix */}
      {tag}
    </span>
  ))}
</div>
```

---

### Fix 3: Ensure Tailwind Classes Not Purged

**Issue:** Text color class purged in production build.

**Fix Location:** `frontend/tailwind.config.js` - Safelist configuration

**Add to tailwind.config.js:**
```javascript
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  safelist: [
    // Ensure tag text colors are never purged
    'text-blue-800',
    'text-blue-900',
    'text-gray-800',
    'text-gray-900',
    'text-green-800',
    'text-red-800',
  ],
  theme: {
    // ...
  },
};
```

**Then rebuild:**
```bash
cd frontend
npm run build
```

---

## Acceptance Criteria

**MUST Pass All:**
- [ ] Tag text is readable (dark color on light background)
- [ ] Tag text has minimum 4.5:1 contrast ratio (WCAG AA)
- [ ] Tag pills use Tailwind classes only (no inline styles)
- [ ] Tag remove button (×) is visible and clickable
- [ ] Tags in Add Task form match style of tags in task list
- [ ] Fix works in both dev and production builds
- [ ] No CSS warnings in console

**Visual Requirements:**
- [ ] Background: Light blue/gray (`bg-blue-100` or `bg-gray-200`)
- [ ] Text: Dark blue/gray (`text-blue-800` or `text-gray-800`)
- [ ] Remove button: Visible, dark color, hover effect

**Test Cases:**
1. **Add Single Tag:** Enter "urgent" → Tag pill appears with readable text
2. **Add Multiple Tags:** Enter "work", "urgent", "meeting" → All readable
3. **Remove Tag:** Click × → Tag removed, no visual glitches
4. **Long Tag:** Enter "very-long-tag-name" → Text doesn't overflow
5. **Production Build:** `npm run build` → Tags still readable

---

## Implementation Checklist

**Phase 1: Diagnosis**
- [ ] Locate TaskForm.tsx tag rendering code
- [ ] Identify current className for tag pills
- [ ] Check background color class
- [ ] Check text color class (or missing)
- [ ] Test current visibility in browser

**Phase 2: Fix**
- [ ] Add `text-blue-800` or `text-gray-800` class
- [ ] Remove conflicting parent `text-white` class
- [ ] Add explicit color to remove button
- [ ] Rebuild frontend if needed

**Phase 3: Testing**
- [ ] Test in dev mode: `npm run dev`
- [ ] Add multiple tags and verify readability
- [ ] Test remove button functionality
- [ ] Build for production: `npm run build`
- [ ] Test production build
- [ ] Verify contrast ratio with browser DevTools

---

## Error Handling

**If Text Still Invisible:**

1. **Check browser DevTools:**
   - Inspect tag element
   - Check computed styles
   - Look for conflicting CSS

2. **Check Tailwind build:**
   - Is text color class in final CSS?
   - Run `grep "text-blue-800" .next/static/css/*.css`

3. **Check CSS specificity:**
   - Parent might have `!important` override
   - Use `!text-blue-800` to force

**If Only Some Tags Invisible:**

1. **Check conditional rendering:**
   - Different tags might have different classes
   - Tag priority/status affecting color?

2. **Check tag data structure:**
   - Tags array might contain objects instead of strings

---

## Related Skills

- **TaskMetadataTextVisibilitySkill** - Fixes text color in task list (not form)
- **frontend-ui-professional** (agent) - General UI/UX quality review

---

## Notes

**Key Principle:**
> WCAG 2.1 Level AA requires minimum 4.5:1 contrast ratio for normal text. Always pair light backgrounds with dark text.

**Common Pitfall:**
> Forgetting to add text color class, assuming browser default will be dark. Always be explicit.

**Best Practice:**
> Use Tailwind's `-100` backgrounds with `-800` or `-900` text colors for optimal readability:
> ```
> bg-blue-100 + text-blue-800 = Perfect contrast
> bg-gray-200 + text-gray-900 = Perfect contrast
> ```

**Accessibility:**
> High contrast benefits everyone:
> - Users with low vision
> - Users with color blindness
> - Users in bright sunlight
> - Older users with reduced vision
