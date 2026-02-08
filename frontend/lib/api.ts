import { Task, CreateTaskRequest, UpdateTaskRequest, ApiResponse, BackendTask } from './types';

// Update the base URL to match our backend API structure
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// Helper function to convert backend task (snake_case) to frontend task (camelCase)
function mapBackendTaskToFrontend(backendTask: BackendTask): Task {
  return {
    id: String(backendTask.id),
    userId: backendTask.user_id,
    title: backendTask.title,
    description: backendTask.description,
    isCompleted: backendTask.is_completed,
    createdAt: new Date(backendTask.created_at),
    updatedAt: new Date(backendTask.updated_at),
    dueDate: backendTask.due_date ? new Date(backendTask.due_date) : undefined,
    priority: backendTask.priority,
  };
}

// Helper function to convert frontend task request to backend format
function mapFrontendRequestToBackend(request: CreateTaskRequest | UpdateTaskRequest): any {
  const backendRequest: any = {};

  if ('title' in request && request.title !== undefined) {
    backendRequest.title = request.title;
  }
  if ('description' in request && request.description !== undefined) {
    backendRequest.description = request.description;
  }
  if ('isCompleted' in request && request.isCompleted !== undefined) {
    backendRequest.is_completed = request.isCompleted;
  }
  if ('dueDate' in request && request.dueDate !== undefined) {
    backendRequest.due_date = request.dueDate;
  }
  if ('priority' in request && request.priority !== undefined) {
    backendRequest.priority = request.priority;
  }

  return backendRequest;
}

class ApiClient {
  private async request<T>(url: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    // Get the Better Auth session token
    let token: string | null = null;
    if (typeof window !== 'undefined') {
      // In a real Better Auth integration, you'd get the token from Better Auth
      // For now, we'll look for it in localStorage as a placeholder
      token = localStorage.getItem('better-auth-session');

      // Or potentially get it from a cookie if Better Auth stores it there
      if (!token) {
        // Attempt to get from document.cookie if stored there
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
          const [name, value] = cookie.trim().split('=');
          if (name === 'better-auth.session_token') {
            token = value;
            break;
          }
        }
      }
    }

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    try {
      const response = await fetch(`${BASE_URL}${url}`, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Request failed');
      }

      return data;
    } catch (error: any) {
      return {
        success: false,
        error: {
          code: 'GENERAL_001',
          message: error.message || 'Network error occurred',
        },
      };
    }
  }

  // Authentication methods
  async login(email: string, password: string): Promise<ApiResponse<{ token: string; user: any }>> {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async signup(email: string, password: string, name: string): Promise<ApiResponse<{ token: string; user: any }>> {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  async logout(): Promise<ApiResponse<void>> {
    return this.request('/auth/logout', {
      method: 'POST',
    });
  }

  // Task methods (require authentication)
  async getTasks(status?: 'all' | 'active' | 'completed', limit?: number, offset?: number): Promise<ApiResponse<{ tasks: Task[]; total: number; limit: number; offset: number }>> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (limit) params.append('limit', limit.toString());
    if (offset) params.append('offset', offset.toString());

    const queryString = params.toString();
    const url = `/tasks${queryString ? `?${queryString}` : ''}`;

    const response = await this.request<{ tasks: BackendTask[]; total: number; limit: number; offset: number }>(url);

    if (response.success && response.data) {
      return {
        ...response,
        data: {
          ...response.data,
          tasks: response.data.tasks.map(mapBackendTaskToFrontend),
        },
      };
    }

    return response as any;
  }

  async createTask(task: CreateTaskRequest): Promise<ApiResponse<{ task: Task }>> {
    const backendRequest = mapFrontendRequestToBackend(task);
    const response = await this.request<{ task: BackendTask }>('/tasks', {
      method: 'POST',
      body: JSON.stringify(backendRequest),
    });

    if (response.success && response.data) {
      return {
        ...response,
        data: {
          task: mapBackendTaskToFrontend(response.data.task),
        },
      };
    }

    return response as any;
  }

  async getTask(id: string): Promise<ApiResponse<{ task: Task }>> {
    const response = await this.request<{ task: BackendTask }>(`/tasks/${id}`);

    if (response.success && response.data) {
      return {
        ...response,
        data: {
          task: mapBackendTaskToFrontend(response.data.task),
        },
      };
    }

    return response as any;
  }

  async updateTask(id: string, task: UpdateTaskRequest): Promise<ApiResponse<{ task: Task }>> {
    const backendRequest = mapFrontendRequestToBackend(task);
    const response = await this.request<{ task: BackendTask }>(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(backendRequest),
    });

    if (response.success && response.data) {
      return {
        ...response,
        data: {
          task: mapBackendTaskToFrontend(response.data.task),
        },
      };
    }

    return response as any;
  }

  async deleteTask(id: string): Promise<ApiResponse<void>> {
    return this.request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(id: string): Promise<ApiResponse<{ task: Task }>> {
    const response = await this.request<{ task: BackendTask }>(`/tasks/${id}/toggle-status`, {
      method: 'PATCH',
    });

    if (response.success && response.data) {
      return {
        ...response,
        data: {
          task: mapBackendTaskToFrontend(response.data.task),
        },
      };
    }

    return response as any;
  }

  // Chat methods (require authentication)
  async chat(userId: string, message: string, conversationId?: string): Promise<ApiResponse<{
    conversation_id: string;
    response: string;
    tool_calls: Array<{ name: string; parameters: Record<string, any> }>;
  }>> {
    return this.request(`/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId
      }),
    });
  }
}

export const apiClient = new ApiClient();