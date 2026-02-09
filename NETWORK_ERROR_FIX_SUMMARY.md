# Network Error Fix Summary

## Problem
Frontend chat page was throwing "Network error. Please check your connection" when trying to send messages.

## Root Causes Identified

### 1. Next.js Config - Undefined Rewrite Destination
**File:** `frontend/next.config.js`
**Issue:** The `rewrites()` function used `process.env.NEXT_PUBLIC_API_URL` which was undefined at config load time (before .env.local is loaded), creating invalid rewrite destination `"undefined/api/:path*"` that corrupted Next.js routing.

**Fix:**
```javascript
async rewrites() {
  // Use fallback value since process.env is not populated from .env.local at config load time
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  return [
    {
      source: '/api/:path*',
      destination: `${apiUrl}/api/:path*`,
    },
  ];
}
```

### 2. MCP Server Config - Missing DATABASE_URL
**File:** `backend/mcp_server/config.py`
**Issue:** MCP server config read `DATABASE_URL` directly from `os.getenv()` at module import time, but the variable was only in the `.env` file (loaded by FastAPI settings, not shell environment). This caused `ValueError` when `MCPClient` tried to import MCP tools.

**Fix:**
```python
# Before:
DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise ValueError(...)

# After:
from src.config import get_settings
settings = get_settings()
DATABASE_URL = settings.database_url  # Already validated and converted to asyncpg
```

### 3. Gemini LLM Config - Missing GEMINI_API_KEY
**File:** `backend/phase3/llm/config.py`
**Issue:** Same as DATABASE_URL - reading environment variable directly instead of using FastAPI settings system.

**Fix:**
1. Added `gemini_api_key` field to `src/config.py` Settings class:
```python
# Phase III: Gemini API Configuration
gemini_api_key: str = Field(
    ...,
    min_length=1,
    description="Google Gemini API key for Phase III AI chatbot",
    json_schema_extra={"env": "GEMINI_API_KEY"},
)
```

2. Updated `get_gemini_api_key()` function:
```python
# Before:
api_key = os.getenv(GEMINI_API_KEY_ENV)
if not api_key:
    raise ValueError(...)

# After:
settings = get_settings()
return settings.gemini_api_key
```

## Error Progression

1. **Initial Error:** `TypeError: Failed to fetch` → "Network error" (frontend couldn't reach backend)
   - **Cause:** Next.js rewrite configuration corruption
   - **Fix:** Added fallback in `next.config.js`

2. **Second Error:** `ValueError: DATABASE_URL environment variable is required`
   - **Cause:** MCP server config reading env vars directly
   - **Fix:** Use FastAPI settings for DATABASE_URL

3. **Third Error:** `ValueError: GEMINI_API_KEY environment variable is required`
   - **Cause:** Gemini config reading env vars directly
   - **Fix:** Use FastAPI settings for GEMINI_API_KEY

## Files Modified

1. `frontend/next.config.js` - Fixed rewrite configuration
2. `backend/mcp_server/config.py` - Use FastAPI settings for DATABASE_URL
3. `backend/src/config.py` - Added gemini_api_key field
4. `backend/phase3/llm/config.py` - Use FastAPI settings for GEMINI_API_KEY

## Verification

✅ Frontend: Next.js dev server running on port 3000
✅ Frontend: Environment variable `NEXT_PUBLIC_API_URL=http://localhost:8000` loaded
✅ Frontend: Rewrite configuration valid: `/api/:path*` → `http://localhost:8000/api/:path*`

✅ Backend: FastAPI server running on port 8000
✅ Backend: Health endpoint responding
✅ Backend: DATABASE_URL loaded from settings (asyncpg format)
✅ Backend: GEMINI_API_KEY loaded from settings (39 characters)
✅ Backend: MCP Client initialized with 5 tools
✅ Backend: No ValueError exceptions during startup

## Network Error Status: RESOLVED ✅

The chat functionality should now work correctly:
- Frontend can reach backend (no more TypeError)
- Backend can initialize all Phase III components (MCP, Gemini)
- Proper HTTP responses returned (200 OK or 401/403/400 for errors)

## Lesson Learned

**Always use the centralized configuration system** (FastAPI settings in this case) rather than reading environment variables directly with `os.getenv()`. This ensures:
- Consistent environment variable loading from `.env` files
- Validation and type checking
- Easier testing and configuration management
- Single source of truth for configuration

When adding new environment-dependent modules (MCP server, Gemini client), they should import from `src.config.get_settings()` rather than using `os.getenv()` directly.
