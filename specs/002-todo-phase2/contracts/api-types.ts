// TypeScript API Client Types - Auto-generated from OpenAPI spec
// Generated: 2025-12-31

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// =============================================================================
// Authentication Types
// =============================================================================

export interface SignupRequest {
  email: string; // format: email, max: 255
  password: string; // min: 8, max: 128
}

export interface SigninRequest {
  email: string; // format: email
  password: string;
}

export interface UserResponse {
  id: string; // uuid
  email: string;
  name: string | null;
  created_at: string; // date-time
}

export interface AuthResponse {
  token: string;
  user: UserResponse;
}

// =============================================================================
// Task Types
// =============================================================================

export interface TaskCreateRequest {
  title: string; // min: 3, max: 100
  description?: string; // max: 500
}

export interface TaskUpdateRequest {
  title?: string; // min: 3, max: 100
  description?: string; // max: 500
  completed?: boolean;
}

export interface TaskResponse {
  id: number;
  user_id: string; // uuid
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string; // date-time
  updated_at: string; // date-time
}

export type TaskListResponse = TaskResponse[];

// =============================================================================
// API Client
// =============================================================================

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  setToken(token: string) {
    this.token = token;
  }

  clearToken() {
    this.token = null;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    if (response.status === 204) {
      return undefined as T;
    }

    return response.json() as Promise<T>;
  }

  // Authentication
  async signup(data: SignupRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async signin(data: SigninRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/api/auth/signin', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getCurrentUser(): Promise<UserResponse> {
    return this.request<UserResponse>('/api/auth/me');
  }

  // Tasks
  async getTasks(userId: string): Promise<TaskListResponse> {
    return this.request<TaskListResponse>(`/api/${userId}/tasks`);
  }

  async createTask(userId: string, data: TaskCreateRequest): Promise<TaskResponse> {
    return this.request<TaskResponse>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getTask(userId: string, taskId: number): Promise<TaskResponse> {
    return this.request<TaskResponse>(`/api/${userId}/tasks/${taskId}`);
  }

  async updateTask(
    userId: string,
    taskId: number,
    data: TaskUpdateRequest
  ): Promise<TaskResponse> {
    return this.request<TaskResponse>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    return this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTask(userId: string, taskId: number): Promise<TaskResponse> {
    return this.request<TaskResponse>(`/api/${userId}/tasks/${taskId}/toggle`, {
      method: 'PATCH',
    });
  }
}

export const api = new ApiClient();
export default api;
