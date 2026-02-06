# Data Model: Modern & Best-in-Class Frontend UI

## Key Entities

### User Session
**Representation**: Authentication state and user preferences (theme selection, UI settings)
**Fields**:
- userId: string (unique identifier from authentication system)
- email: string (user's email address)
- isAuthenticated: boolean (authentication status)
- themePreference: "light" | "dark" | "system" (user's theme choice)
- lastLoginAt: Date (timestamp of last login)
- sessionToken: string (JWT token for API authentication)

### Task
**Representation**: Individual todo items with properties like title, description, completion status, due date, priority
**Fields**:
- id: string (unique identifier for the task)
- userId: string (foreign key linking to the owning user)
- title: string (task title, 1-200 characters)
- description?: string (optional detailed description)
- isCompleted: boolean (completion status)
- createdAt: Date (timestamp when task was created)
- updatedAt: Date (timestamp when task was last updated)
- dueDate?: Date (optional deadline for the task)
- priority: "low" | "medium" | "high" | "urgent" (task importance level)
- category?: string (optional category/grouping)

### UI Components
**Representation**: Reusable interface elements following atomic design principles and consistent styling
**Fields**:
- componentName: string (name of the component)
- propsSchema: object (definition of expected props)
- stylingRules: object (Tailwind CSS classes and theme variants)
- accessibilityProps: object (ARIA attributes and keyboard navigation support)
- responsiveBehaviors: object (how component adapts to different screen sizes)

### Theme Settings
**Representation**: User preferences for light/dark mode and associated visual properties
**Fields**:
- themeType: "light" | "dark" | "system" (current theme mode)
- primaryColor: string (primary brand color in hex format)
- secondaryColor: string (secondary color in hex format)
- borderRadius: "none" | "sm" | "md" | "lg" | "xl" | "full" (UI corner rounding)
- fontFamily: string (font family preference)
- reducedMotion: boolean (whether to disable animations for accessibility)

## State Transitions

### User Session Transitions
- **Logged Out** → **Logging In** → **Authenticated** → **Logging Out** → **Logged Out**
- **Theme Change**: System → Light → Dark → System (circular selection)

### Task State Transitions
- **Created** → **Active** → **Completed** → **Editing** → **Active** (or Completed if edited to completed)
- **Deleting**: Active/Completed → **Pending Deletion** → **Deleted**

## Validation Rules

### User Session Validation
- Email must be valid format (RFC 5322 compliant)
- Session token must be present when isAuthenticated is true
- Theme preference must be one of the allowed values

### Task Validation
- Title must be 1-200 characters
- Title cannot be empty or only whitespace
- Due date (if present) must not be in the past (for certain use cases)
- Priority must be one of the allowed values
- userId must match authenticated user (enforced by backend)

### Theme Settings Validation
- All color values must be valid CSS color formats (hex, rgb, hsl)
- Border radius must be one of the predefined options
- Reduced motion must be boolean value

## Relationships
- User Session "has many" Tasks (one-to-many relationship)
- Tasks belong to a single User Session
- Theme Settings belong to a single User Session