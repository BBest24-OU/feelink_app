<script lang="ts">
  import Navigation from './Navigation.svelte';
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
</script>

<div class="min-h-screen bg-gray-50">
  <Navigation />

  <!-- Sync Status Banner (only shown when offline with pending changes) -->
  {#if !$syncStatus.isOnline && $syncStatus.pendingCount > 0}
    <div class="bg-amber-50 border-b border-amber-200">
      <div class="container mx-auto px-3 sm:px-4 md:px-6 py-2">
        <p class="text-sm text-amber-800 flex items-center space-x-2">
          <AlertCircle size={16} />
          <span>You're offline. {$syncStatus.pendingCount} change(s) will sync when you're back online.</span>
        </p>
      </div>
    </div>
  {/if}

  <main class="w-full px-3 sm:px-4 md:px-6 py-4 md:py-6 pb-20 md:pb-6">
    <div class="mx-auto {maxWidthClasses[maxWidth]}">
      <slot />
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-gray-200 bg-white mt-8 md:mt-12 mb-16 md:mb-0">
    <div class="w-full px-3 sm:px-4 md:px-6 py-4 md:py-6">
      <div class="mx-auto max-w-7xl">
        <div class="flex flex-col sm:flex-row items-center justify-between space-y-2 sm:space-y-0">
          <p class="text-xs sm:text-sm text-gray-500 text-center sm:text-left">
            © {new Date().getFullYear()} Feelink. Track your well-being.
          </p>
          <div class="flex items-center space-x-4 text-xs sm:text-sm text-gray-500">
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

<style>
  /* Smooth scrolling for better UX */
  :global(html) {
    scroll-behavior: smooth;
  }
</style>
