<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { location } from 'svelte-spa-router';
  import { t } from '../i18n';
  import { authActions } from '../stores/user';
  import {
    LayoutDashboard,
    PenLine,
    FileText,
    Activity,
    Lightbulb,
    Link2,
    LogOut,
    ChevronLeft,
    ChevronRight,
    Heart,
    User,
    Sun,
    Moon
  } from 'lucide-svelte';
  import { themeStore } from '../stores/theme';

  export let minimized = false;

  const dispatch = createEventDispatcher();

  const navItems = [
    { path: '/dashboard', label: 'nav.dashboard', icon: LayoutDashboard },
    { path: '/log', label: 'nav.log', icon: PenLine },
    { path: '/entries', label: 'nav.entries', icon: FileText },
    { path: '/metrics', label: 'nav.metrics', icon: Activity },
    { path: '/insights', label: 'nav.insights', icon: Lightbulb },
    { path: '/correlations', label: 'nav.correlations', icon: Link2 },
    { path: '/profile', label: 'nav.profile', icon: User }
  ];

  function isActive(path: string): boolean {
    return $location === path || $location.startsWith(path + '/');
  }

  function toggleMinimized() {
    minimized = !minimized;
    dispatch('toggle', { minimized });
  }

  async function handleLogout() {
    await authActions.logout();
  }
</script>

<aside
  class="hidden md:flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 h-screen transition-all duration-300 ease-in-out {minimized
    ? 'w-20'
    : 'w-64'}"
>
  <!-- Logo Section -->
  <div class="flex items-center h-16 px-4 border-b border-gray-200 dark:border-gray-700 flex-shrink-0">
    {#if minimized}
      <div class="flex items-center justify-center w-full">
        <div class="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
          <Heart size={20} class="text-white" />
        </div>
      </div>
    {:else}
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
          <Heart size={20} class="text-white" />
        </div>
        <h1 class="text-xl font-bold text-gray-800 dark:text-white">Feelink</h1>
      </div>
    {/if}
  </div>

  <!-- Navigation Items -->
  <nav class="flex-1 py-4 overflow-y-auto">
    <ul class="space-y-1 px-3">
      {#each navItems as item}
        <li>
          <a
            href={`#${item.path}`}
            class="flex items-center rounded-lg transition-all duration-200 {minimized
              ? 'justify-center h-12 w-12 mx-auto'
              : 'px-3 py-3 space-x-3'} {isActive(item.path)
              ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 active:bg-gray-100 dark:active:bg-gray-700'}"
            title={minimized ? $t(item.label) : ''}
          >
            <svelte:component
              this={item.icon}
              size={20}
              strokeWidth={isActive(item.path) ? 2.5 : 2}
            />
            {#if !minimized}
              <span class="font-medium text-sm">{$t(item.label)}</span>
            {/if}
          </a>
        </li>
      {/each}
    </ul>
  </nav>

  <!-- Bottom Section -->
  <div class="border-t border-gray-200 dark:border-gray-700 p-3 space-y-2">
    <!-- Theme Toggle -->
    <button
      on:click={() => themeStore.toggle()}
      class="flex items-center w-full rounded-lg px-3 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 active:bg-gray-100 dark:active:bg-gray-700 transition-colors {minimized
        ? 'justify-center'
        : 'space-x-3'}"
      title={minimized ? ($themeStore.resolvedTheme === 'dark' ? $t('nav.lightMode') : $t('nav.darkMode')) : ''}
    >
      {#if $themeStore.resolvedTheme === 'dark'}
        <Sun size={20} />
      {:else}
        <Moon size={20} />
      {/if}
      {#if !minimized}
        <span class="text-sm font-medium">
          {$themeStore.resolvedTheme === 'dark' ? $t('nav.lightMode') : $t('nav.darkMode')}
        </span>
      {/if}
    </button>

    <!-- Toggle Sidebar Button -->
    <button
      on:click={toggleMinimized}
      class="flex items-center w-full rounded-lg px-3 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 active:bg-gray-100 dark:active:bg-gray-700 transition-colors {minimized
        ? 'justify-center'
        : 'space-x-3'}"
      title={minimized ? $t('nav.expand') : $t('nav.minimize')}
    >
      {#if minimized}
        <ChevronRight size={20} />
      {:else}
        <ChevronLeft size={20} />
        <span class="text-sm font-medium">{$t('nav.minimize')}</span>
      {/if}
    </button>

    <!-- Logout Button -->
    <button
      on:click={handleLogout}
      class="flex items-center w-full rounded-lg px-3 py-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 active:bg-red-100 dark:active:bg-red-900/30 transition-colors {minimized
        ? 'justify-center'
        : 'space-x-3'}"
      title={minimized ? $t('nav.logout') : ''}
    >
      <LogOut size={20} />
      {#if !minimized}
        <span class="text-sm font-medium">{$t('nav.logout')}</span>
      {/if}
    </button>
  </div>
</aside>
