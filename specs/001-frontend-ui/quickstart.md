# Quickstart Guide: Modern & Best-in-Class Frontend UI

## Setup Environment

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Git for version control

### Initial Setup
```bash
# Clone the repository (if starting fresh)
git clone <repo-url>
cd <repo-directory>

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install
```

### Environment Variables
Create a `.env.local` file in the frontend directory with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-here
```

## Running the Application

### Development Mode
```bash
# Start the development server
npm run dev
# or
yarn dev

# The application will be available at http://localhost:3000
```

### Production Build
```bash
# Build the application for production
npm run build
# or
yarn build

# Start the production server
npm run start
# or
yarn start
```

## Key Technologies & Structure

### Tech Stack
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **Icons**: Lucide React
- **Authentication**: Better Auth with JWT

### Project Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── globals.css         # Global styles and Tailwind configuration
│   ├── layout.tsx          # Root layout with theme provider
│   ├── page.tsx            # Home page
│   └── dashboard/
│       ├── page.tsx        # Main dashboard with task management
│       └── layout.tsx      # Dashboard-specific layout
├── components/            # Reusable UI components
│   ├── ui/                # Atomic components (Button, Input, etc.)
│   ├── auth/              # Authentication-related components
│   └── tasks/             # Task-specific components
├── lib/                   # Utility functions and API client
│   ├── api.ts             # API client with JWT handling
│   └── types.ts           # TypeScript type definitions
├── hooks/                 # Custom React hooks
└── providers/             # Context providers (theme, auth, etc.)
```

## Key Components to Build

### 1. Authentication Components
```typescript
// components/auth/login-form.tsx
export function LoginForm() { ... }

// components/auth/signup-form.tsx
export function SignupForm() { ... }
```

### 2. Core UI Components
```typescript
// components/ui/button.tsx
export function Button() { ... }

// components/ui/input.tsx
export function Input() { ... }

// components/ui/card.tsx
export function Card() { ... }
```

### 3. Task Management Components
```typescript
// components/tasks/task-list.tsx
export function TaskList() { ... }

// components/tasks/task-item.tsx
export function TaskItem({ task, onComplete, onDelete }) { ... }

// components/tasks/task-form.tsx
export function TaskForm() { ... }
```

## Theming System

### CSS Variables Setup
The theme system uses CSS variables that can be dynamically switched:

```css
:root,
.light {
  --background: 255 255 255;
  --foreground: 0 0 0;
  --primary: 59 130 246;
  --primary-foreground: 255 255 255;
}

.dark {
  --background: 0 0 0;
  --foreground: 255 255 255;
  --primary: 59 130 246;
  --primary-foreground: 255 255 255;
}
```

### Theme Provider
```tsx
// providers/theme-provider.tsx
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  // Handles theme switching and persistence
}
```

## API Integration

### API Client with JWT Handling
```tsx
// lib/api.ts
export const apiClient = {
  get: async (url: string) => { /* attaches JWT token */ },
  post: async (url: string, data: any) => { /* attaches JWT token */ },
  put: async (url: string, data: any) => { /* attaches JWT token */ },
  delete: async (url: string) => { /* attaches JWT token */ }
}
```

## Running Tests

### Unit Tests
```bash
npm run test
# or
yarn test
```

### Linting
```bash
npm run lint
# or
yarn lint
```

### Formatting
```bash
npm run format
# or
yarn format
```

## Common Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run test` | Run unit tests |
| `npm run lint` | Check code for linting issues |
| `npm run format` | Format code with Prettier |

## Next Steps
1. Begin with creating the core UI components in `/components/ui/`
2. Implement the authentication flow in `/app/auth/`
3. Build the task management interface in `/app/dashboard/`
4. Add responsive design and theme switching capabilities
5. Implement loading states and accessibility features