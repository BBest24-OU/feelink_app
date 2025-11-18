<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { location } from 'svelte-spa-router';
  import { t } from '../i18n';
  import { Menu, Heart } from 'lucide-svelte';

  const dispatch = createEventDispatcher();

  function openDrawer() {
    dispatch('opendrawer');
  }
</script>

<!-- Mobile Header -->
<header class="md:hidden bg-white border-b border-gray-200 shadow-sm sticky top-0 z-30">
  <div class="flex items-center justify-between h-14 px-4">
    <button
      on:click={openDrawer}
      class="p-2 rounded-lg text-gray-700 hover:bg-gray-100 active:bg-gray-200 transition-colors -ml-2"
      aria-label={$t('nav.openMenu')}
    >
      <Menu size={24} />
    </button>

    <div class="flex items-center space-x-2">
      <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
        <Heart size={16} class="text-white" />
      </div>
      <h1 class="text-lg font-bold text-gray-800">Feelink</h1>
    </div>

    <!-- Spacer to center the logo -->
    <div class="w-10"></div>
  </div>
</header>

<style>
  /* Safe area for iOS devices with notch/home indicator */
  :global(.safe-area-bottom) {
    padding-bottom: env(safe-area-inset-bottom);
  }
</style>
