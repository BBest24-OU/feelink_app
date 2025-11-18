<script lang="ts">
  import Navigation from './Navigation.svelte';
  import { syncStatus } from '../lib/sync';

  export let maxWidth: 'sm' | 'md' | 'lg' | 'xl' | 'full' = 'xl';

  const maxWidthClasses = {
    sm: 'max-w-2xl',
    md: 'max-w-4xl',
    lg: 'max-w-6xl',
    xl: 'max-w-7xl',
    full: 'max-w-full'
  };
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
  <Navigation />

  <!-- Sync Status Banner (only shown when offline with pending changes) -->
  {#if !$syncStatus.isOnline && $syncStatus.pendingCount > 0}
    <div class="bg-amber-50 border-b border-amber-200">
      <div class="container mx-auto px-6 py-2">
        <p class="text-sm text-amber-800 flex items-center space-x-2">
          <span>⚠️</span>
          <span>You're offline. {$syncStatus.pendingCount} change(s) will sync when you're back online.</span>
        </p>
      </div>
    </div>
  {/if}

  <main class="container mx-auto px-4 sm:px-6 py-6 {maxWidthClasses[maxWidth]}">
    <slot />
  </main>

  <!-- Footer -->
  <footer class="border-t border-gray-200 bg-white mt-12">
    <div class="container mx-auto px-6 py-6">
      <div class="flex flex-col sm:flex-row items-center justify-between space-y-2 sm:space-y-0">
        <p class="text-sm text-gray-500">
          © {new Date().getFullYear()} Feelink. Track your well-being with confidence.
        </p>
        <div class="flex items-center space-x-4 text-sm text-gray-500">
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
  </footer>
</div>

<style>
  /* Smooth scrolling for better UX */
  :global(html) {
    scroll-behavior: smooth;
  }

  /* Enhanced background gradient */
  .bg-gradient-to-br {
    background-image: linear-gradient(to bottom right, var(--tw-gradient-stops));
  }
</style>
