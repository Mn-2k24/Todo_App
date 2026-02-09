# ChatKit Frontend Builder Skill

## Agent Identity
**Name**: ChatKit Frontend Builder Agent
**Purpose**: Implement Phase III chat UI using OpenAI ChatKit while preserving all Phase II functionality
**Phase**: Phase III
**Model**: sonnet

---

## Core Responsibilities

### Primary Mission
Build production-ready chat interface that:
1. Creates protected `/chat` route using Next.js App Router
2. Implements chat UI using OpenAI ChatKit components
3. Integrates with Phase III backend chat API (`POST /api/{user_id}/chat`)
4. Manages conversation state in React memory only (no persistent storage)
5. Maintains ZERO modifications to existing Phase II code
6. Provides responsive, accessible chat experience

### Specific Capabilities
- Create isolated Phase III frontend directory structure
- Implement ChatKit-based message list and input components
- Build type-safe API client for chat endpoint
- Handle authentication state using existing Phase II auth system
- Implement proper loading, error, and empty states
- Configure OpenAI domain allowlist for production deployment

---

## Allowed Folder / File Scope

### ALLOWED - Full Write/Read Access
```
frontend/src/app/chat/           # Chat page route (NEW)
├── page.tsx                     # Main chat page component
├── layout.tsx                   # Chat-specific layout (optional)
└── components/                  # Chat-specific components
    ├── MessageList.tsx          # Display conversation history
    ├── MessageInput.tsx         # User input box
    ├── LoadingIndicator.tsx     # Loading state
    ├── ErrorDisplay.tsx         # Error state
    └── EmptyState.tsx           # Initial empty state

frontend/src/components/chat/    # Shared chat components (alternative location)

frontend/src/lib/chat.ts         # Chat API client (NEW)
frontend/src/types/chat.ts       # Chat type definitions (NEW)

frontend/.env.local              # Add NEXT_PUBLIC_OPENAI_DOMAIN_KEY
```

### ALLOWED - Read-Only Access
```
frontend/src/app/                # Understand existing routing
frontend/src/components/         # Identify reusable components
frontend/src/lib/api.ts          # Understand existing API client patterns
frontend/src/types/              # Understand existing type patterns
```

### STRICTLY FORBIDDEN - Zero Access
```
frontend/src/app/(auth)/         # Phase II auth pages (NO MODIFICATION)
frontend/src/app/dashboard/      # Phase II dashboard (NO MODIFICATION)
frontend/src/components/tasks/   # Phase II task components (NO MODIFICATION)
frontend/src/lib/auth.ts         # Phase II auth utilities (NO MODIFICATION - can import only)
backend/                         # Backend code (OUT OF SCOPE)
specs/003-phase-ii-full-stack/   # Phase II specs (NO MODIFICATION)
```

---

## Inputs / Outputs Handled

### Inputs
1. **User Text Message** (from MessageInput component):
   - String: User's chat message
   - Example: "Add a task to buy groceries"

2. **Authentication State** (from Phase II auth system):
   - `user_id`: Authenticated user ID (from existing auth context)
   - Token/session: Existing Phase II authentication mechanism

3. **Backend Chat API Response**:
   ```typescript
   {
     conversation_id: string;
     message_id: string;
     response: string;
     tool_calls?: Array<{
       tool: string;
       parameters: Record<string, any>;
       result: any;
     }>;
   }
   ```

4. **Environment Variables**:
   - `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`: Domain allowlist key for ChatKit

### Outputs
1. **Chat UI Page** (`/chat`):
   - Accessible only to authenticated users
   - Responsive layout (mobile, tablet, desktop)
   - Real-time message display
   - Auto-scroll to latest message

2. **API Requests** (to backend):
   ```typescript
   POST /api/{user_id}/chat
   {
     message: string;
     conversation_id?: string;
   }
   ```

3. **React State Updates**:
   - Conversation ID stored in component state
   - Message history stored in component state
   - NO localStorage, NO sessionStorage (memory only)

4. **User Feedback**:
   - Loading indicators during API calls
   - Error messages on failures
   - Empty state before first message
   - Success confirmation (implicit via message display)

---

## Database Models Affected

### CRITICAL: NO DATABASE ACCESS

Frontend MUST NEVER directly access databases.

**Correct Approach**:
```typescript
// ✅ CORRECT: Call backend API
const response = await fetch(`/api/${userId}/chat`, {
  method: 'POST',
  body: JSON.stringify({ message })
});
```

**Forbidden Approach**:
```typescript
// ❌ FORBIDDEN: Direct database access
import { prisma } from '@/lib/db';
const messages = await prisma.message.findMany();
```

**Rationale**: Frontend is a stateless UI layer. All data operations go through backend APIs.

---

## External Systems Integrated

### 1. OpenAI ChatKit
- **Library**: `@openai/chatkit` or similar official ChatKit package
- **Integration Point**: Chat UI components
- **Configuration**:
  - Domain key: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` environment variable
  - Initialization: Configure in chat page component
  - Components used:
    - `<ChatMessages>`: Display message history
    - `<ChatInput>`: User input field
    - `<ChatMessage>`: Individual message component
- **Customization**:
  - Styling: Match Phase II design system (Tailwind classes)
  - Theme: Consistent with existing app theme
  - Layout: Responsive grid

### 2. Phase III Backend Chat API
- **Endpoint**: `POST /api/{user_id}/chat`
- **Protocol**: HTTP/HTTPS
- **Authentication**: Use existing Phase II auth mechanism (JWT in headers or cookies)
- **Request Format**:
  ```typescript
  {
    message: string;
    conversation_id?: string;
  }
  ```
- **Response Format**:
  ```typescript
  {
    conversation_id: string;
    message_id: string;
    response: string;
    tool_calls?: Array<ToolCall>;
  }
  ```
- **Error Handling**:
  - Network errors: Show retry button
  - 400 Bad Request: Display validation error
  - 401 Unauthorized: Redirect to login
  - 500 Server Error: Show generic error message

### 3. Phase II Authentication System (Reuse Only)
- **Integration**: Import existing auth hooks/utilities
- **Read-Only**: NEVER modify auth code
- **Usage**:
  - Get current user ID
  - Protect chat route (require authentication)
  - Redirect unauthenticated users to login
- **Example**:
  ```typescript
  import { useAuth } from '@/lib/auth';  // Existing Phase II hook

  export default function ChatPage() {
    const { user, isLoading } = useAuth();
    if (!user) redirect('/login');
    // ... chat implementation
  }
  ```

---

## Error Handling Requirements

### Network Errors
- **Trigger**: Backend API unreachable (timeout, connection failure)
- **Display**:
  ```
  ⚠️ Unable to connect. Please check your connection and try again.
  [Retry Button]
  ```
- **Action**: Provide retry button to resend message

### API Validation Errors (400)
- **Trigger**: Backend rejects request (missing message, invalid format)
- **Display**:
  ```
  ⚠️ Please enter a valid message.
  ```
- **Action**: Keep input box enabled, allow user to correct

### Authentication Errors (401/403)
- **Trigger**: User not authenticated or session expired
- **Action**: Redirect to login page
- **Message**: "Your session has expired. Please log in again."

### Server Errors (500)
- **Trigger**: Backend internal error
- **Display**:
  ```
  ⚠️ Something went wrong. Please try again.
  [Retry Button]
  ```
- **Action**: Log error to console, provide retry button

### Tool Execution Errors (from backend)
- **Trigger**: Backend returns error in tool_calls
- **Display**: Show assistant response that explains the error
- **Example**: "I couldn't complete that action. Please try again later."

### Empty State (no errors)
- **Trigger**: User visits chat page with no messages
- **Display**:
  ```
  💬 Start a conversation
  Ask me to add tasks, view your tasks, or manage your to-do list.
  ```

---

## Rules / Restrictions

### MUST DO
1. **Zero Phase II Modifications**: Create ONLY new files; NEVER edit existing Phase II code
2. **ChatKit Components**: Use official OpenAI ChatKit components for UI
3. **Type Safety**: All components and API calls MUST be TypeScript with strict typing
4. **Responsive Design**: Chat UI MUST work on mobile, tablet, and desktop
5. **Auth Protection**: Chat route MUST require authentication (reuse Phase II mechanism)
6. **Stateless Frontend**: Conversation state ONLY in React memory (no localStorage)
7. **Domain Configuration**: Support `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` for production

### MUST NOT DO
1. **No Phase II Edits**: NEVER modify files in `app/(auth)/`, `app/dashboard/`, `components/tasks/`
2. **No Backend Logic**: NEVER implement AI logic, database queries, or business logic in frontend
3. **No Direct MCP Calls**: NEVER call MCP tools directly from frontend (use chat API only)
4. **No Persistent Storage**: NEVER use localStorage, sessionStorage, or cookies for chat data
5. **No Auth Modifications**: NEVER change existing authentication code (import and use only)
6. **No External UI Libraries**: Use ChatKit only; don't add shadcn, MUI, or other UI frameworks
7. **No Hardcoded API Keys**: NEVER hardcode OpenAI keys or domain keys in code

### Critical Constraints
- **Chat API Only**: ALL backend communication via `POST /api/{user_id}/chat` endpoint
- **Memory-Only State**: Conversation history lives in React state; cleared on page refresh
- **Auth Reuse**: Use existing Phase II auth; don't implement new auth mechanisms
- **Isolated Components**: All Phase III components in `app/chat/` or `components/chat/`

---

## Success Criteria

### Functional Success
- [ ] Chat page accessible at `/chat` route
- [ ] Chat page protected by authentication (redirects unauthenticated users)
- [ ] User can type messages in input field
- [ ] Messages sent to backend API successfully
- [ ] Backend responses displayed in message list
- [ ] Conversation history persists within session (React state)
- [ ] Auto-scroll to latest message works
- [ ] Multiple messages in conversation thread correctly

### UI/UX Success
- [ ] Chat UI uses OpenAI ChatKit components
- [ ] Design matches Phase II aesthetic (colors, fonts, spacing)
- [ ] Responsive layout works on mobile, tablet, desktop
- [ ] Loading indicator shows during API requests
- [ ] Error messages displayed clearly
- [ ] Empty state shown before first message
- [ ] Accessible (keyboard navigation, screen reader support)

### Integration Success
- [ ] Chat API client correctly calls `POST /api/{user_id}/chat`
- [ ] Authentication state integrated from Phase II
- [ ] User ID correctly passed to API
- [ ] Conversation ID managed across multiple messages
- [ ] Tool execution results displayed (if applicable)

### Quality Success
- [ ] All components TypeScript with strict types
- [ ] Type definitions for API requests and responses
- [ ] No TypeScript errors or `any` types
- [ ] Proper error handling for all API scenarios
- [ ] Code follows Next.js App Router conventions

### Security Success
- [ ] Chat route requires authentication
- [ ] No hardcoded API keys or secrets
- [ ] User can only access own chat (enforced by backend)
- [ ] No sensitive data stored in localStorage

### Documentation Success
- [ ] README explains how to access chat feature
- [ ] Environment variable `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` documented
- [ ] Integration with Phase III backend documented

---

## Dependencies on Other Agents

### Upstream Dependencies (Must Complete Before This Agent)
1. **Chat + MCP Bridge Agent** (REQUIRED):
   - Dependency: Backend chat API endpoint must exist and respond
   - Integration Point: Frontend calls `POST /api/{user_id}/chat`
   - Validation: API returns expected response format

2. **Phase II Frontend** (COMPLETE):
   - Dependency: Authentication system must be functional
   - Reason: Reuse existing auth to protect chat route
   - Validation: Can import and use auth hooks/utilities

### Downstream Dependencies (No agents depend on this agent)
- Frontend is the final layer; no downstream dependencies

### Parallel Agents (Can Develop Concurrently)
1. **MCP Server Builder Agent**:
   - Relationship: Indirect (frontend → chat API → MCP tools)
   - No direct interaction

2. **AI Agent Logic Agent**:
   - Relationship: Indirect (frontend → chat API → agent logic → MCP tools)
   - No direct interaction

---

## Example Expected Inputs and Outputs

### Example 1: Initial Chat Page Load
**User Action**: Navigate to `/chat` while authenticated

**Expected UI**:
```
┌─────────────────────────────────────┐
│ My Tasks Chat                       │
├─────────────────────────────────────┤
│                                     │
│         💬                          │
│   Start a conversation              │
│                                     │
│   Ask me to add tasks, view your   │
│   tasks, or manage your to-do list.│
│                                     │
├─────────────────────────────────────┤
│ [Type a message...]          [Send] │
└─────────────────────────────────────┘
```

**State**:
```typescript
{
  messages: [],
  conversationId: null,
  isLoading: false,
  error: null
}
```

### Example 2: User Sends First Message
**User Input**: Types "Add a task to buy groceries" and clicks Send

**Frontend Actions**:
1. Add user message to state optimistically
2. Show loading indicator
3. Call API: `POST /api/user_123/chat`
4. Receive response
5. Add assistant message to state
6. Hide loading indicator

**Expected UI** (after response):
```
┌─────────────────────────────────────┐
│ My Tasks Chat                       │
├─────────────────────────────────────┤
│ You: Add a task to buy groceries    │
│                                     │
│ Assistant: I've added the task      │
│ 'Buy groceries' for you.            │
│                                     │
├─────────────────────────────────────┤
│ [Type a message...]          [Send] │
└─────────────────────────────────────┘
```

**State**:
```typescript
{
  messages: [
    {
      role: 'user',
      content: 'Add a task to buy groceries',
      timestamp: '2026-01-23T10:30:00Z'
    },
    {
      role: 'assistant',
      content: "I've added the task 'Buy groceries' for you.",
      timestamp: '2026-01-23T10:30:01Z',
      tool_calls: [...]
    }
  ],
  conversationId: 'conv_abc123',
  isLoading: false,
  error: null
}
```

### Example 3: Network Error Handling
**User Input**: Types "Show my tasks" and clicks Send

**Scenario**: Backend API is unreachable (network timeout)

**Frontend Actions**:
1. Add user message to state
2. Show loading indicator
3. Call API → timeout after 10 seconds
4. Show error state

**Expected UI**:
```
┌─────────────────────────────────────┐
│ My Tasks Chat                       │
├─────────────────────────────────────┤
│ You: Add a task to buy groceries    │
│ Assistant: I've added the task...   │
│                                     │
│ You: Show my tasks                  │
│                                     │
│ ⚠️ Unable to connect. Please check  │
│ your connection and try again.      │
│ [Retry]                             │
│                                     │
├─────────────────────────────────────┤
│ [Type a message...]          [Send] │
└─────────────────────────────────────┘
```

**State**:
```typescript
{
  messages: [...],
  conversationId: 'conv_abc123',
  isLoading: false,
  error: {
    code: 'NETWORK_ERROR',
    message: 'Unable to connect',
    retryable: true
  }
}
```

### Example 4: Unauthenticated User Access
**User Action**: Navigate to `/chat` without being logged in

**Expected Behavior**:
- Redirect to `/login` (or Phase II login page)
- Show message: "Please log in to access chat"

**Code**:
```typescript
export default function ChatPage() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!user) redirect('/login');

  return <ChatUI />;
}
```

---

## Component Architecture

### Chat Page Structure
```typescript
// frontend/src/app/chat/page.tsx
'use client';  // Client component (uses hooks)

import { useState } from 'react';
import { useAuth } from '@/lib/auth';  // Existing Phase II hook
import { MessageList } from './components/MessageList';
import { MessageInput } from './components/MessageInput';
import { sendMessage } from '@/lib/chat';  // API client

export default function ChatPage() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSendMessage = async (message: string) => {
    setIsLoading(true);
    setError(null);

    // Optimistically add user message
    setMessages(prev => [...prev, { role: 'user', content: message }]);

    try {
      const response = await sendMessage(user.id, message, conversationId);
      setConversationId(response.conversation_id);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls
      }]);
    } catch (err) {
      setError(err);
      // Remove optimistic user message on error
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      {error && <ErrorDisplay error={error} />}
      <MessageInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  );
}
```

### API Client Implementation
```typescript
// frontend/src/lib/chat.ts
export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message_id: string;
  response: string;
  tool_calls?: Array<ToolCall>;
}

export async function sendMessage(
  userId: string,
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const response = await fetch(`/api/${userId}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, conversation_id: conversationId })
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
```

---

## Validation Checklist Before Completion

### Code Quality
- [ ] All components TypeScript with strict types
- [ ] No `any` types used
- [ ] All API calls have type definitions
- [ ] Proper error handling on all async operations
- [ ] Code follows Next.js App Router conventions

### Functionality
- [ ] Chat page accessible at `/chat`
- [ ] User can send and receive messages
- [ ] Conversation history displays correctly
- [ ] Auto-scroll to latest message works
- [ ] Multiple messages in thread work

### UI/UX
- [ ] ChatKit components integrated
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Loading states during API calls
- [ ] Error states with retry buttons
- [ ] Empty state before first message

### Integration
- [ ] API calls to backend succeed
- [ ] Authentication protection works
- [ ] User ID correctly passed to API
- [ ] Conversation ID managed correctly

### Phase II Isolation
- [ ] ZERO Phase II files modified (verify with git diff)
- [ ] Auth system reused, not reimplemented
- [ ] No changes to existing routes or components

### Security
- [ ] Chat route requires authentication
- [ ] No hardcoded secrets
- [ ] No localStorage for sensitive data

### Configuration
- [ ] `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` environment variable supported
- [ ] ChatKit domain configuration works

---

**Skill Version**: 1.0.0
**Last Updated**: 2026-01-23
**Maintained By**: Phase III Frontend Architecture Team
