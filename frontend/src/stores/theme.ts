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

    const root = document.documentElement;

    if (resolvedTheme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }

  // Initialize - apply theme on first load
  if (isBrowser) {
    applyTheme(initialResolvedTheme);

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
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
      const resolvedTheme = resolveTheme(newTheme);

      // Save to localStorage
      if (isBrowser) {
        localStorage.setItem('feelink-theme', newTheme);
      }

      // Apply theme
      applyTheme(resolvedTheme);

      // Update store
      set({ theme: newTheme, resolvedTheme });
    },

    toggle: () => {
      update(state => {
        const newTheme: Theme = state.resolvedTheme === 'dark' ? 'light' : 'dark';
        const resolvedTheme = newTheme;

        // Save to localStorage
        if (isBrowser) {
          localStorage.setItem('feelink-theme', newTheme);
        }

        // Apply theme
        applyTheme(resolvedTheme);

        return { theme: newTheme, resolvedTheme };
      });
    }
  };
}

export const themeStore = createThemeStore();
