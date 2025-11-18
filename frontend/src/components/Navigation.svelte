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

<nav class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
  <div class="container mx-auto px-3 sm:px-4 md:px-6">
    <div class="flex items-center justify-between h-14 md:h-16">
      <!-- Logo and Brand -->
      <div class="flex items-center space-x-8">
        <a href="#/dashboard" class="flex items-center space-x-2 group">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center transform group-hover:scale-105 transition-transform">
            <span class="text-white font-bold text-lg">F</span>
          </div>
          <span class="text-xl font-semibold text-gray-800 tracking-tight">Feelink</span>
        </a>

        <!-- Main Navigation -->
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
      <div class="flex items-center space-x-4">
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
          class="px-3 py-2 text-sm font-medium text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors flex items-center space-x-2"
        >
          <LogOut size={18} />
          <span class="hidden sm:inline">{$t('auth.logout')}</span>
        </button>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <div class="md:hidden pb-2 flex items-center gap-1 overflow-x-auto">
      {#each navItems as item}
        <a
          href={`#${item.path}`}
          class="px-3 py-2.5 rounded-lg text-xs font-medium transition-all duration-200 flex items-center gap-1.5 whitespace-nowrap min-h-[44px]
            {isActive(item.path)
              ? 'bg-primary-50 text-primary-700'
              : 'text-gray-600 active:bg-gray-100'}"
        >
          <svelte:component this={item.icon} size={18} />
          <span>{$t(item.label)}</span>
        </a>
      {/each}
    </div>
  </div>
</nav>

<style>
  /* Custom scrollbar for mobile navigation */
  .overflow-x-auto::-webkit-scrollbar {
    height: 4px;
  }

  .overflow-x-auto::-webkit-scrollbar-track {
    background: transparent;
  }

  .overflow-x-auto::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 2px;
  }

  .overflow-x-auto::-webkit-scrollbar-thumb:hover {
    background: #9ca3af;
  }
</style>
