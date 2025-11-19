import { writable } from 'svelte/store';

export type Theme = 'light' | 'dark' | 'system';

interface ThemeState {
  theme: Theme;
  resolvedTheme: 'light' | 'dark';
}

// Helper to detect if running in browser
const isBrowser = typeof window !== 'undefined';

// Get initial theme from localStorage or default to system
function getInitialTheme(): Theme {
  if (!isBrowser) return 'system';

  const stored = localStorage.getItem('feelink-theme') as Theme;
  if (stored && ['light', 'dark', 'system'].includes(stored)) {
    return stored;
  }
  return 'system';
}

// Resolve system preference
function getSystemTheme(): 'light' | 'dark' {
  if (!isBrowser) return 'light';

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Resolve theme (system -> actual theme)
function resolveTheme(theme: Theme): 'light' | 'dark' {
  if (theme === 'system') {
    return getSystemTheme();
  }
  return theme;
}

// Create the store
function createThemeStore() {
  const initialTheme = getInitialTheme();
  const initialResolvedTheme = resolveTheme(initialTheme);

  const { subscribe, set, update } = writable<ThemeState>({
    theme: initialTheme,
    resolvedTheme: initialResolvedTheme
  });

  // Apply theme to document
  function applyTheme(resolvedTheme: 'light' | 'dark') {
    if (!isBrowser) return;

    console.log('[ThemeStore] Applying theme:', resolvedTheme);
    const root = document.documentElement;

    if (resolvedTheme === 'dark') {
      root.classList.add('dark');
      console.log('[ThemeStore] Added "dark" class to <html>');
    } else {
      root.classList.remove('dark');
      console.log('[ThemeStore] Removed "dark" class from <html>');
    }

    console.log('[ThemeStore] Current classes on <html>:', root.className);
  }

  // Initialize - apply theme on first load
  if (isBrowser) {
    console.log('[ThemeStore] Initializing theme store');
    console.log('[ThemeStore] Initial theme:', initialTheme);
    console.log('[ThemeStore] Initial resolved theme:', initialResolvedTheme);
    applyTheme(initialResolvedTheme);

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
      console.log('[ThemeStore] System theme changed:', e.matches ? 'dark' : 'light');
      update(state => {
        if (state.theme === 'system') {
          const newResolvedTheme = e.matches ? 'dark' : 'light';
          applyTheme(newResolvedTheme);
          return { ...state, resolvedTheme: newResolvedTheme };
        }
        return state;
      });
    });
  }

  return {
    subscribe,

    setTheme: (newTheme: Theme) => {
      console.log('[ThemeStore] setTheme called with:', newTheme);
      const resolvedTheme = resolveTheme(newTheme);
      console.log('[ThemeStore] Resolved to:', resolvedTheme);

      // Save to localStorage
      if (isBrowser) {
        localStorage.setItem('feelink-theme', newTheme);
        console.log('[ThemeStore] Saved to localStorage:', newTheme);
      }

      // Apply theme
      applyTheme(resolvedTheme);

      // Update store
      set({ theme: newTheme, resolvedTheme });
      console.log('[ThemeStore] Store updated');
    },

    toggle: () => {
      console.log('[ThemeStore] toggle() called');
      update(state => {
        console.log('[ThemeStore] Current state:', state);
        const newTheme: Theme = state.resolvedTheme === 'dark' ? 'light' : 'dark';
        const resolvedTheme = newTheme;
        console.log('[ThemeStore] Toggling to:', newTheme);

        // Save to localStorage
        if (isBrowser) {
          localStorage.setItem('feelink-theme', newTheme);
          console.log('[ThemeStore] Saved to localStorage:', newTheme);
        }

        // Apply theme
        applyTheme(resolvedTheme);

        return { theme: newTheme, resolvedTheme };
      });
    }
  };
}

export const themeStore = createThemeStore();
