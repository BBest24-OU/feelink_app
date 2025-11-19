<script lang="ts">
  import { onMount } from 'svelte';
  import Navigation from './Navigation.svelte';
  import Sidebar from './Sidebar.svelte';
  import Drawer from './Drawer.svelte';
  import { syncStatus } from '../lib/sync';
  import { AlertCircle } from 'lucide-svelte';

  export let maxWidth: 'sm' | 'md' | 'lg' | 'xl' | 'full' = 'xl';

  const maxWidthClasses = {
    sm: 'max-w-2xl',
    md: 'max-w-4xl',
    lg: 'max-w-6xl',
    xl: 'max-w-7xl',
    full: 'max-w-full'
  };

  let sidebarMinimized = false;
  let drawerOpen = false;

  // Load sidebar state from localStorage
  onMount(() => {
    const savedState = localStorage.getItem('sidebarMinimized');
    if (savedState !== null) {
      sidebarMinimized = savedState === 'true';
    }
  });

  function handleSidebarToggle(event: CustomEvent) {
    sidebarMinimized = event.detail.minimized;
    localStorage.setItem('sidebarMinimized', String(sidebarMinimized));
  }

  function handleDrawerOpen() {
    drawerOpen = true;
  }

  function handleDrawerClose() {
    drawerOpen = false;
  }
</script>

<!-- Full screen flex layout -->
<div class="h-screen w-screen flex overflow-hidden bg-gray-50 dark:bg-gray-900">
  <!-- Desktop Sidebar -->
  <Sidebar minimized={sidebarMinimized} on:toggle={handleSidebarToggle} />

  <!-- Mobile Drawer -->
  <Drawer open={drawerOpen} on:close={handleDrawerClose} />

  <!-- Main Content Area -->
  <div class="flex-1 flex flex-col overflow-hidden">
    <!-- Mobile Header -->
    <Navigation on:opendrawer={handleDrawerOpen} />

    <!-- Content Container -->
    <div class="flex-1 overflow-y-auto">
      <div class="flex flex-col min-h-full">
        <!-- Sync Status Banner (only shown when offline with pending changes) -->
        {#if !$syncStatus.isOnline && $syncStatus.pendingCount > 0}
          <div class="bg-amber-50 dark:bg-amber-900/20 border-b border-amber-200 dark:border-amber-800">
            <div class="px-4 md:px-6 py-2">
              <p class="text-sm text-amber-800 dark:text-amber-200 flex items-center space-x-2">
                <AlertCircle size={16} />
                <span
                  >You're offline. {$syncStatus.pendingCount} change(s) will sync when you're back
                  online.</span
                >
              </p>
            </div>
          </div>
        {/if}

        <!-- Main Content -->
        <main class="flex-grow px-4 md:px-6 py-4 md:py-6">
          <div class="mx-auto {maxWidthClasses[maxWidth]}">
            <slot />
          </div>
        </main>

        <!-- Footer - mt-auto ensures it stays at bottom -->
        <footer class="mt-auto border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          <div class="px-4 md:px-6 py-4 md:py-6">
            <div class="mx-auto max-w-7xl">
              <div
                class="flex flex-col sm:flex-row items-center justify-between space-y-2 sm:space-y-0"
              >
                <p class="text-xs sm:text-sm text-gray-500 dark:text-gray-400 text-center sm:text-left">
                  © {new Date().getFullYear()} Feelink. Track your well-being.
                </p>
                <div class="flex items-center space-x-4 text-xs sm:text-sm text-gray-500 dark:text-gray-400">
                  <span class="flex items-center space-x-1">
                    {#if $syncStatus.isOnline}
                      <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                      <span>Online</span>
                    {:else}
                      <span class="w-2 h-2 bg-gray-400 rounded-full"></span>
                      <span>Offline</span>
                    {/if}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  </div>
</div>

<style>
  /* Smooth scrolling for better UX */
  :global(html) {
    scroll-behavior: smooth;
  }
</style>
