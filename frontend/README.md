# Todo App - Frontend

Next.js-based frontend application with Better Auth authentication, TypeScript, and Tailwind CSS.

## Technology Stack

- **Framework**: Next.js 15.1+ with App Router
- **UI Library**: React 19+
- **Styling**: Tailwind CSS 3.4+
- **Authentication**: Better Auth with JWT
- **Language**: TypeScript 5.3+ (strict mode)
- **HTTP Client**: Fetch API with custom wrapper

## Prerequisites

- Node.js 18 or higher
- npm, yarn, or pnpm
- Backend API running (see [Backend README](../backend/README.md))

## Setup Instructions

### 1. Environment Configuration

Create a `.env.local` file in the `frontend/` directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-auth-secret-min-32-characters-long
BETTER_AUTH_URL=http://localhost:3000
```

**Security Note**: Never commit `.env.local` files. Secrets must not be hardcoded.

### 2. Install Dependencies

Using npm:

```bash
cd frontend
npm install
```

Using yarn:

```bash
cd frontend
yarn install
```

Using pnpm:

```bash
cd frontend
pnpm install
```

### 3. Start the Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

The application will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm run start
```

## Application Structure

```
frontend/
├── src/
│   ├── app/                      # Next.js App Router pages
│   │   ├── (auth)/              # Authentication pages (public)
│   │   │   ├── login/           # Login page
│   │   │   └── register/        # Registration page
│   │   ├── (protected)/         # Protected pages (require auth)
│   │   │   └── dashboard/       # Main dashboard with task management
│   │   ├── layout.tsx           # Root layout
│   │   └── page.tsx             # Home/landing page
│   ├── components/              # React components
│   │   ├── auth/                # Authentication components
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── tasks/               # Task management components
│   │   │   ├── TaskForm.tsx     # Create/edit task form
│   │   │   ├── TaskItem.tsx     # Single task display
│   │   │   ├── TaskList.tsx     # Task list with states
│   │   │   ├── TaskFilters.tsx  # Search and filter controls
│   │   │   └── TaskSort.tsx     # Sort dropdown
│   │   └── ui/                  # Reusable UI components
│   │       ├── Button.tsx
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorMessage.tsx
│   │       ├── EmptyState.tsx
│   │       ├── ConfirmDialog.tsx
│   │       └── Toast.tsx
│   ├── lib/                     # Utility libraries
│   │   ├── api.ts               # API request wrapper
│   │   ├── auth.ts              # Better Auth client setup
│   │   └── utils.ts             # Helper functions
│   ├── types/                   # TypeScript type definitions
│   │   ├── user.ts              # User types
│   │   └── task.ts              # Task types and Priority enum
│   └── styles/
│       └── globals.css          # Global styles and Tailwind
├── public/                      # Static assets
├── .env.local.example           # Example environment variables
├── next.config.js               # Next.js configuration
├── tailwind.config.ts           # Tailwind CSS configuration
├── tsconfig.json                # TypeScript configuration
└── README.md                    # This file
```

## Key Features

### Authentication Flow
1. User registers via `/register` page
2. User logs in via `/login` page to receive JWT token
3. Token stored in Better Auth session
4. Protected routes automatically redirect to login if not authenticated
5. Token sent in `Authorization` header for API requests

### Task Management (Dashboard)
- **Create**: Add new tasks with description, priority, tags, and due date
- **Read**: View all tasks with filters and search
- **Update**: Edit task details inline
- **Delete**: Remove tasks with confirmation dialog
- **Toggle**: Mark tasks complete/incomplete

### Filtering & Search (FR-026 to FR-031)
- **Text Search**: Search task descriptions
- **Status Filter**: Show all/completed/incomplete tasks
- **Priority Filter**: Filter by high/medium/low priority
- **Tags Filter**: Filter by comma-separated tags
- **Combined Filters**: All filters work simultaneously

### Sorting (FR-032 to FR-036)
- **Sort by Title**: Alphabetical order
- **Sort by Created**: Newest first (default)
- **Sort by Due Date**: Nearest first (nulls last)
- **Sort by Priority**: High→Medium→Low
- **Persistent Preference**: Sort choice saved to localStorage

### UI/UX Features
- **Loading States**: Spinners for async operations (FR-041)
- **Error Handling**: User-friendly error messages (FR-042)
- **Empty States**: Context-aware messages (FR-043, FR-031)
- **Responsive Design**: Mobile-first, 320px to 2560px (FR-045)
- **Accessibility**: Keyboard navigation, ARIA labels (FR-046)
- **Overdue Indicators**: Visual distinction for overdue tasks (FR-025)

## Component Documentation

### Task Components

#### `TaskForm`
Create and edit task form with validation.
- **Props**: `task`, `onSubmit`, `onCancel`, `submitLabel`
- **Features**: Description (required, max 500 chars), priority dropdown, tags input with add/remove, due date picker
- **Validation**: Client-side validation with error display

#### `TaskItem`
Display single task with actions.
- **Props**: `task`, `onToggle`, `onEdit`, `onDelete`
- **Features**: Checkbox for completion, priority badge, tag badges, due date with overdue indicator, edit/delete buttons
- **States**: Loading states for toggle and delete operations

#### `TaskList`
Render list of tasks with empty/error states.
- **Props**: `tasks`, `loading`, `error`, `onToggle`, `onEdit`, `onDelete`, `hasActiveFilters`
- **States**: Loading spinner, error message, context-aware empty state

#### `TaskFilters`
Search and filter controls.
- **Props**: `selectedPriority`, `onPriorityChange`, `selectedTags`, `onTagsChange`, `searchText`, `onSearchChange`, `selectedStatus`, `onStatusChange`
- **Features**: Text search input, status dropdown, priority dropdown, tags input

#### `TaskSort`
Sort dropdown with persistence.
- **Props**: `selectedSort`, `onSortChange`
- **Features**: 4 sort options, preference saved to localStorage

### UI Components

All UI components follow consistent patterns:
- Loading states with disabled interactions
- Error handling with user-friendly messages
- Accessibility attributes (ARIA labels, keyboard navigation)
- Responsive design with Tailwind classes

## Styling Guidelines

### Tailwind CSS Custom Classes

Defined in `globals.css`:

```css
.btn          /* Base button styles */
.btn-primary  /* Primary action button */
.btn-secondary /* Secondary action button */
.btn-ghost    /* Minimal button */

.input        /* Form input fields */

.card         /* Container with shadow and padding */

.badge               /* Base badge styles */
.badge-high          /* High priority (red) */
.badge-medium        /* Medium priority (yellow) */
.badge-low           /* Low priority (green) */
.badge-default       /* Default badge (gray) */
```

### Color Scheme
- Primary: Blue tones for main actions
- Success: Green for completed/success states
- Error: Red for errors and high priority
- Warning: Yellow/Orange for medium priority and warnings
- Neutral: Gray for secondary elements

## Development Workflow

### Adding a New Component

1. Create component file in appropriate directory (`src/components/`)
2. Define TypeScript interfaces for props
3. Implement component with proper error handling and loading states
4. Add accessibility attributes (ARIA labels, keyboard support)
5. Style with Tailwind CSS utility classes
6. Document component usage

### API Integration

Use the `apiRequest` helper from `src/lib/api.ts`:

```typescript
import { apiRequest } from "@/lib/api";

// GET request
const tasks = await apiRequest<Task[]>("/api/tasks");

// POST request with body
const newTask = await apiRequest<Task>("/api/tasks", {
  method: "POST",
  body: { description: "Task description", priority: "medium" }
});
```

The helper automatically:
- Attaches JWT token from Better Auth session
- Handles JSON serialization
- Throws typed errors for HTTP errors
- Parses error responses from backend

### State Management

The dashboard uses React hooks for state management:
- `useState` for local component state
- `useEffect` for side effects (API calls, localStorage)
- Prop drilling for parent-child communication
- No global state management library (per constitution simplicity principle)

## Testing

### Running Tests

```bash
npm run test
# or
yarn test
# or
pnpm test
```

### Manual Testing Checklist

- [ ] Registration flow (create account)
- [ ] Login flow (authenticate)
- [ ] Create task with all fields
- [ ] Edit task
- [ ] Delete task with confirmation
- [ ] Toggle task completion
- [ ] Search tasks by text
- [ ] Filter by status (all/completed/incomplete)
- [ ] Filter by priority
- [ ] Filter by tags
- [ ] Sort by each option
- [ ] Verify sort persists after refresh
- [ ] Test responsive design (mobile, tablet, desktop)
- [ ] Test keyboard navigation
- [ ] Verify overdue task indicators
- [ ] Test error states (network errors, validation errors)
- [ ] Test empty states (no tasks, no matching filters)

## Performance Optimization

- Server Components for static content
- Client Components only where interactivity needed
- Lazy loading for modals and dialogs
- Optimized images with Next.js Image component
- Debouncing for search input (consider implementing)

## Accessibility (FR-046)

- Semantic HTML elements
- ARIA labels for interactive elements
- Keyboard navigation support (Tab, Enter, Escape)
- Focus indicators
- Screen reader friendly error messages
- Color contrast ratios meet WCAG AA standards

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

## Troubleshooting

### Backend Connection Issues
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check backend is running at specified URL
- Verify CORS is configured correctly in backend

### Authentication Issues
- Clear browser cookies and localStorage
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check JWT token expiration (default 60 minutes)

### Build Errors
- Delete `.next/` directory and rebuild
- Clear npm/yarn/pnpm cache
- Verify all dependencies are installed

## Related Documentation

- [Backend README](../backend/README.md)
- [Quickstart Guide](../specs/003-phase-ii-full-stack/quickstart.md)
- [Feature Specification](../specs/003-phase-ii-full-stack/spec.md)
- [Architecture Plan](../specs/003-phase-ii-full-stack/plan.md)
