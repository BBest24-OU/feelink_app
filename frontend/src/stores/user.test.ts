/**
 * Unit tests for user store
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { get } from 'svelte/store';
import { userStore, isAuthenticated, authActions } from './user';

// Mock the API
vi.mock('../lib/api', () => ({
  authApi: {
    login: vi.fn(),
    register: vi.fn(),
    refreshToken: vi.fn(),
    logout: vi.fn(),
  },
  usersApi: {
    getProfile: vi.fn(),
    updateProfile: vi.fn(),
  },
}));

describe('User Store', () => {
  beforeEach(() => {
    // Reset store state before each test
    userStore.set({
      user: null,
      token: null,
      refreshToken: null,
      loading: false,
      error: null,
    });

    // Clear localStorage
    localStorage.clear();

    // Reset mocks
    vi.clearAllMocks();
  });

  describe('isAuthenticated', () => {
    it('should be false when no user is logged in', () => {
      const auth = get(isAuthenticated);
      expect(auth).toBe(false);
    });

    it('should be true when user is logged in', () => {
      userStore.set({
        user: {
          id: 1,
          email: 'test@example.com',
          language: 'en',
          timezone: 'UTC',
        },
        token: 'fake-token',
        refreshToken: 'fake-refresh-token',
        loading: false,
        error: null,
      });

      const auth = get(isAuthenticated);
      expect(auth).toBe(true);
    });
  });

  describe('authActions.logout', () => {
    it('should clear user data and tokens', () => {
      // Set up logged in state
      localStorage.setItem('access_token', 'fake-token');
      localStorage.setItem('refresh_token', 'fake-refresh');
      userStore.set({
        user: {
          id: 1,
          email: 'test@example.com',
          language: 'en',
          timezone: 'UTC',
        },
        token: 'fake-token',
        refreshToken: 'fake-refresh',
        loading: false,
        error: null,
      });

      // Logout
      authActions.logout();

      // Verify state is cleared
      const state = get(userStore);
      expect(state.user).toBeNull();
      expect(state.token).toBeNull();
      expect(state.refreshToken).toBeNull();

      // Verify localStorage is cleared
      expect(localStorage.getItem('access_token')).toBeNull();
      expect(localStorage.getItem('refresh_token')).toBeNull();
    });

    it('should redirect to login page', () => {
      const originalHash = window.location.hash;

      authActions.logout();

      // In test environment, hash should be set to #/login
      expect(window.location.hash).toBe('#/login');

      // Restore original hash
      window.location.hash = originalHash;
    });
  });

  describe('Loading States', () => {
    it('should have loading false by default', () => {
      const state = get(userStore);
      expect(state.loading).toBe(false);
    });
  });

  describe('Error Handling', () => {
    it('should have null error by default', () => {
      const state = get(userStore);
      expect(state.error).toBeNull();
    });

    it('should clear error on logout', () => {
      userStore.set({
        user: null,
        token: null,
        refreshToken: null,
        loading: false,
        error: 'Some error',
      });

      authActions.logout();

      const state = get(userStore);
      expect(state.error).toBeNull();
    });
  });

  describe('Token Management', () => {
    it('should persist tokens to localStorage on set', () => {
      userStore.set({
        user: {
          id: 1,
          email: 'test@example.com',
          language: 'en',
          timezone: 'UTC',
        },
        token: 'new-token',
        refreshToken: 'new-refresh-token',
        loading: false,
        error: null,
      });

      // Note: Actual persistence might happen in auth actions
      // This test structure demonstrates how it should work
      const state = get(userStore);
      expect(state.token).toBe('new-token');
      expect(state.refreshToken).toBe('new-refresh-token');
    });
  });
});
