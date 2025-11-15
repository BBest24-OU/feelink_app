/**
 * API client for backend communication
 */
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest: any = error.config;

    // If 401 and not already retried, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: (data: { email: string; password: string; language?: string; timezone?: string }) =>
    api.post('/api/v1/auth/register', data),

  login: (email: string, password: string) =>
    api.post('/api/v1/auth/login', { email, password }),

  refreshToken: (refreshToken: string) =>
    api.post('/api/v1/auth/refresh', { refresh_token: refreshToken }),

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

// User API
export const userApi = {
  getProfile: () => api.get('/api/v1/users/me'),
  updateProfile: (data: { language?: string; timezone?: string }) =>
    api.patch('/api/v1/users/me', data),
  deleteAccount: () => api.delete('/api/v1/users/me'),
};

// Metrics API
export const metricsApi = {
  list: (includeArchived: boolean = false) =>
    api.get('/api/v1/metrics', { params: { include_archived: includeArchived } }),

  create: (data: any) => api.post('/api/v1/metrics', data),

  get: (id: number) => api.get(`/api/v1/metrics/${id}`),

  update: (id: number, data: any) => api.patch(`/api/v1/metrics/${id}`, data),

  archive: (id: number) => api.delete(`/api/v1/metrics/${id}`),

  unarchive: (id: number) => api.post(`/api/v1/metrics/${id}/unarchive`),
};

// Entries API
export const entriesApi = {
  list: (params?: { date_from?: string; date_to?: string; limit?: number; offset?: number }) =>
    api.get('/api/v1/entries', { params }),

  create: (data: any) => api.post('/api/v1/entries', data),

  get: (id: number) => api.get(`/api/v1/entries/${id}`),

  getByDate: (date: string) => api.get(`/api/v1/entries/date/${date}`),

  update: (id: number, data: any) => api.patch(`/api/v1/entries/${id}`, data),

  delete: (id: number) => api.delete(`/api/v1/entries/${id}`),
};

// Analytics API
export const analyticsApi = {
  getCorrelations: (params?: {
    metric_ids?: number[];
    date_from?: string;
    date_to?: string;
    algorithm?: string;
    max_lag?: number;
    min_significance?: number;
    only_significant?: boolean;
  }) => api.post('/api/v1/analytics/correlations', params || {}),

  getStatistics: (params?: {
    metric_ids?: string;
    date_from?: string;
    date_to?: string;
  }) => api.get('/api/v1/analytics/statistics', { params }),
};

export default api;
