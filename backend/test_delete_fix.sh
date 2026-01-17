#!/bin/bash
# Manual test script for task delete fix verification
# Prerequisites: Backend and frontend must be running

set -e

echo "========================================="
echo "Task Delete Fix - Manual Test Script"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend is running
if ! pgrep -f "uvicorn" > /dev/null; then
    echo -e "${RED}ERROR: Backend is not running${NC}"
    echo "Start backend with: cd backend && source venv/bin/activate && uvicorn src.main:app --reload"
    exit 1
fi

# Check if frontend is running
if ! pgrep -f "next" > /dev/null; then
    echo -e "${RED}ERROR: Frontend is not running${NC}"
    echo "Start frontend with: cd frontend && npm run dev"
    exit 1
fi

echo -e "${GREEN}✓ Backend is running${NC}"
echo -e "${GREEN}✓ Frontend is running${NC}"
echo ""

echo "========================================="
echo "Test 1: Create and Delete Task"
echo "========================================="

# Get auth token (you'll need to replace this with actual token or use login flow)
echo -e "${YELLOW}Note: You need to be logged in to test this${NC}"
echo ""
echo "Manual Test Steps:"
echo ""
echo "1. Open browser to http://localhost:3000"
echo "2. Login with test credentials"
echo "3. Create a new task (e.g., 'Test Delete Task')"
echo "4. Click delete button on the task"
echo "5. Confirm deletion in dialog"
echo ""
echo "Expected Results:"
echo "  ✓ Task should be removed from UI immediately"
echo "  ✓ Green success toast: 'Task deleted successfully!'"
echo "  ✓ No errors in browser console"
echo "  ✓ No 'An unexpected error occurred' message"
echo "  ✓ No page reload needed"
echo ""

echo "========================================="
echo "Test 2: Verify Backend Response"
echo "========================================="
echo ""
echo "1. Open browser DevTools (F12)"
echo "2. Go to Network tab"
echo "3. Delete a task"
echo "4. Check the DELETE request"
echo ""
echo "Expected Network Response:"
echo "  ✓ Status: 204 No Content"
echo "  ✓ Response body: Empty"
echo "  ✓ No JSON parse errors in console"
echo ""

echo "========================================="
echo "Test 3: Error Handling"
echo "========================================="
echo ""
echo "1. Stop backend: pkill -f uvicorn"
echo "2. Try to delete a task"
echo "3. Restart backend and try again"
echo ""
echo "Expected Results (Backend Stopped):"
echo "  ✓ Red error toast: 'Failed to delete task. Please try again.'"
echo "  ✓ Task remains visible in UI"
echo "  ✓ No crash or global error"
echo ""
echo "Expected Results (Backend Restarted):"
echo "  ✓ Delete works normally"
echo "  ✓ Green success toast shown"
echo ""

echo "========================================="
echo "Test 4: Multiple Deletes"
echo "========================================="
echo ""
echo "1. Create 3-5 tasks"
echo "2. Delete them one by one quickly"
echo ""
echo "Expected Results:"
echo "  ✓ All deletes work correctly"
echo "  ✓ Each shows green success toast"
echo "  ✓ UI updates smoothly"
echo "  ✓ No errors accumulate"
echo ""

echo "========================================="
echo "Code Review Checklist"
echo "========================================="
echo ""
echo "Backend (src/api/tasks.py):"
echo "  ✓ DELETE endpoint returns 204 No Content (line 179)"
echo "  ✓ No response body returned"
echo ""
echo "Frontend (src/lib/api.ts):"
echo "  ✓ Checks for 204 status before JSON parse (line 86-88)"
echo "  ✓ Returns undefined for 204 responses"
echo "  ✓ JSON parse only for responses with body"
echo ""
echo "Frontend (dashboard/page.tsx):"
echo "  ✓ handleConfirmDelete in try-catch (lines 205-233)"
echo "  ✓ setTasks with filter (immutable update, line 217)"
echo "  ✓ showSuccessToast in try block (line 220)"
echo "  ✓ showErrorToast in catch block (line 228)"
echo ""

echo "========================================="
echo "Fix Summary"
echo "========================================="
echo ""
echo "Root Cause:"
echo "  - Frontend tried to parse JSON from empty 204 response"
echo "  - JSON parse threw error, caught by catch block"
echo "  - Error toast shown despite successful deletion"
echo ""
echo "Solution:"
echo "  - Check response.status === 204 before parsing JSON"
echo "  - Return undefined for 204 No Content responses"
echo "  - Allow DELETE to succeed without parsing error"
echo ""
echo "Files Modified:"
echo "  - frontend/src/lib/api.ts (added 204 handler)"
echo ""
echo "Files Reviewed (No Changes):"
echo "  - backend/src/api/tasks.py (already correct)"
echo "  - frontend/src/app/(protected)/dashboard/page.tsx (already correct)"
echo ""

echo "========================================="
echo "Ready for Testing!"
echo "========================================="
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
