// User Session Type
export interface UserSession {
  userId: string;
  email: string;
  isAuthenticated: boolean;
  themePreference: 'light' | 'dark' | 'system';
  lastLoginAt: Date;
  sessionToken: string;
}

// Task Type
export interface Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  isCompleted: boolean;
  createdAt: Date;
  updatedAt: Date;
  dueDate?: Date;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  category?: string;
}

// UI Component Type
export interface UIComponent {
  componentName: string;
  propsSchema: object;
  stylingRules: object;
  accessibilityProps: object;
  responsiveBehaviors: object;
}

// Theme Settings Type
export interface ThemeSettings {
  themeType: 'light' | 'dark' | 'system';
  primaryColor: string;
  secondaryColor: string;
  borderRadius: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full';
  fontFamily: string;
  reducedMotion: boolean;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

// Task API Response Types
export interface CreateTaskRequest {
  title: string;
  description?: string;
  dueDate?: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  isCompleted?: boolean;
  dueDate?: string;
  priority?: 'low' | 'medium' | 'high' | 'urgent';
}