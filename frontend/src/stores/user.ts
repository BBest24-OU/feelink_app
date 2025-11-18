/**
 * User store - manages authentication and user state
 */
import { writable, derived } from 'svelte/store';
import { authApi, userApi } from '../lib/api';

interface User {
  id: number;
  email: string;
  name?: string;
  language: string;
  timezone: string;
  created_at: string;
  updated_at: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  accessToken: localStorage.getItem('access_token'),
  refreshToken: localStorage.getItem('refresh_token'),
  loading: false,
  error: null,
};

export const authStore = writable<AuthState>(initialState);

// Listen for auth:logout event from API interceptor
if (typeof window !== 'undefined') {
  window.addEventListener('auth:logout', () => {
    authStore.set({
      user: null,
      accessToken: null,
      refreshToken: null,
      loading: false,
      error: null,
    });
  });
}

// Derived store for authentication status
export const isAuthenticated = derived(
  authStore,
  ($auth) => !!$auth.accessToken && !!$auth.user
);

// Actions
export const authActions = {
  // Register new user
  async register(email: string, password: string, language: string = 'en') {
    authStore.update((state) => ({ ...state, loading: true, error: null }));

    // Convert locale format (e.g., 'pl-PL' -> 'pl', 'en-US' -> 'en')
    const langCode = language.split('-')[0];

    try {
      const response = await authApi.register({ email, password, language: langCode });
      const { user, tokens } = response.data;

      localStorage.setItem('access_token', tokens.access_token);
      localStorage.setItem('refresh_token', tokens.refresh_token);

      authStore.set({
        user,
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        loading: false,
        error: null,
      });

      return { success: true };
    } catch (error: any) {
      // Format validation errors from FastAPI
      let errorMsg = 'Registration failed';
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
          // Format validation errors into readable messages
          errorMsg = detail.map((err: any) => err.msg || err.message || String(err)).join(', ');
        } else if (typeof detail === 'string') {
          errorMsg = detail;
        }
      }
      authStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Login user
  async login(email: string, password: string) {
    authStore.update((state) => ({ ...state, loading: true, error: null }));

    try {
      const response = await authApi.login(email, password);
      console.log('[AUTH] Login response:', response.data);
      const { user, tokens } = response.data;

      // Ensure tokens are valid before saving
      if (!tokens?.access_token || !tokens?.refresh_token) {
        throw new Error('Invalid token response from server');
      }

      console.log('[AUTH] Saving tokens to localStorage');
      localStorage.setItem('access_token', tokens.access_token);
      localStorage.setItem('refresh_token', tokens.refresh_token);

      // Verify tokens were saved
      const savedToken = localStorage.getItem('access_token');
      console.log('[AUTH] Token saved successfully:', !!savedToken, savedToken?.substring(0, 30) + '...');

      authStore.set({
        user,
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        loading: false,
        error: null,
      });

      console.log('[AUTH] Auth store updated with user:', user.email);

      return { success: true };
    } catch (error: any) {
      console.error('[AUTH] Login error:', error);
      // Format validation errors from FastAPI
      let errorMsg = 'Login failed';
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
          errorMsg = detail.map((err: any) => err.msg || err.message || String(err)).join(', ');
        } else if (typeof detail === 'string') {
          errorMsg = detail;
        }
      }
      authStore.update((state) => ({ ...state, loading: false, error: errorMsg }));
      return { success: false, error: errorMsg };
    }
  },

  // Logout user
  logout() {
    authApi.logout();
    authStore.set({
      user: null,
      accessToken: null,
      refreshToken: null,
      loading: false,
      error: null,
    });
  },

  // Load user profile
  async loadProfile() {
    authStore.update((state) => ({ ...state, loading: true }));

    try {
      const response = await userApi.getProfile();
      authStore.update((state) => ({
        ...state,
        user: response.data,
        loading: false,
      }));
      return { success: true };
    } catch (error: any) {
      authStore.update((state) => ({ ...state, loading: false }));
      return { success: false };
    }
  },

  // Update user profile
  async updateProfile(data: { name?: string; language?: string; timezone?: string }) {
    authStore.update((state) => ({ ...state, loading: true }));

    try {
      const response = await userApi.updateProfile(data);
      authStore.update((state) => ({
        ...state,
        user: response.data,
        loading: false,
      }));
      return { success: true };
    } catch (error: any) {
      authStore.update((state) => ({ ...state, loading: false }));
      return { success: false };
    }
  },
};
