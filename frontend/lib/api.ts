import { Task, CreateTaskRequest, UpdateTaskRequest, ApiResponse } from './types';

// Update the base URL to match our backend API structure
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

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

    return this.request(url);
  }

  async createTask(task: CreateTaskRequest): Promise<ApiResponse<{ task: Task }>> {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(task),
    });
  }

  async getTask(id: string): Promise<ApiResponse<{ task: Task }>> {
    return this.request(`/tasks/${id}`);
  }

  async updateTask(id: string, task: UpdateTaskRequest): Promise<ApiResponse<{ task: Task }>> {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(task),
    });
  }

  async deleteTask(id: string): Promise<ApiResponse<void>> {
    return this.request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(id: string): Promise<ApiResponse<{ task: Task }>> {
    return this.request(`/tasks/${id}/toggle-status`, {
      method: 'PATCH',
    });
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