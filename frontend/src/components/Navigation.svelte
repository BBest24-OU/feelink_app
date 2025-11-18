<script lang="ts">
  import { location } from 'svelte-spa-router';
  import { authStore, authActions } from '../stores/user';
  import { t } from '../i18n';
  import {
    LayoutDashboard,
    PenLine,
    FileText,
    Activity,
    Lightbulb,
    Link2,
    LogOut
  } from 'lucide-svelte';

  // Navigation items
  const navItems = [
    { path: '/dashboard', label: 'nav.dashboard', icon: LayoutDashboard },
    { path: '/log', label: 'nav.log', icon: PenLine },
    { path: '/entries', label: 'nav.entries', icon: FileText },
    { path: '/metrics', label: 'nav.metrics', icon: Activity },
    { path: '/insights', label: 'nav.insights', icon: Lightbulb },
    { path: '/correlations', label: 'nav.correlations', icon: Link2 },
  ];

  function handleLogout() {
    authActions.logout();
    window.location.hash = '/login';
  }

  function isActive(path: string): boolean {
    return $location === path || $location.startsWith(path + '?');
  }
</script>

<!-- Top Navigation Bar -->
<nav class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
  <div class="w-full px-3 sm:px-4 md:px-6">
    <div class="flex items-center justify-between h-14 md:h-16 max-w-7xl mx-auto">
      <!-- Logo and Brand -->
      <div class="flex items-center space-x-8">
        <a href="#/dashboard" class="flex items-center space-x-2 group">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center transform group-hover:scale-105 transition-transform">
            <span class="text-white font-bold text-lg">F</span>
          </div>
          <span class="text-xl font-semibold text-gray-800 tracking-tight">Feelink</span>
        </a>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-1">
          {#each navItems as item}
            <a
              href={`#${item.path}`}
              class="px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center space-x-2
                {isActive(item.path)
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'}"
            >
              <svelte:component this={item.icon} size={18} />
              <span>{$t(item.label)}</span>
            </a>
          {/each}
        </div>
      </div>

      <!-- User Menu -->
      <div class="flex items-center space-x-2 sm:space-x-4">
        <div class="hidden sm:flex items-center space-x-3 px-3 py-2 bg-gray-50 rounded-lg">
          <div class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
            <span class="text-white text-sm font-semibold">
              {$authStore.user?.email?.charAt(0).toUpperCase() || 'U'}
            </span>
          </div>
          <span class="text-sm text-gray-700 font-medium max-w-[150px] truncate">
            {$authStore.user?.email || 'User'}
          </span>
        </div>

        <button
          on:click={handleLogout}
          class="px-2 sm:px-3 py-2 text-sm font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors flex items-center space-x-2"
        >
          <LogOut size={18} />
          <span class="hidden sm:inline">{$t('auth.logout')}</span>
        </button>
      </div>
    </div>
  </div>
</nav>

<!-- Bottom Navigation (Mobile Only) -->
<nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50 safe-area-bottom">
  <div class="grid grid-cols-5 h-16">
    {#each navItems.slice(0, 5) as item}
      <a
        href={`#${item.path}`}
        class="flex flex-col items-center justify-center space-y-1 transition-colors min-h-[64px]
          {isActive(item.path)
            ? 'text-primary-600'
            : 'text-gray-600 active:bg-gray-50'}"
      >
        <svelte:component this={item.icon} size={22} strokeWidth={isActive(item.path) ? 2.5 : 2} />
        <span class="text-[10px] font-medium">{$t(item.label)}</span>
      </a>
    {/each}
  </div>
</nav>

<style>
  /* Safe area for iOS devices with notch/home indicator */
  .safe-area-bottom {
    padding-bottom: env(safe-area-inset-bottom);
  }
</style>
