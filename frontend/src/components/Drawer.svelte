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
    X,
    Heart
  } from 'lucide-svelte';

  export let open = false;

  const dispatch = createEventDispatcher();

  const navItems = [
    { path: '/dashboard', label: 'nav.dashboard', icon: LayoutDashboard },
    { path: '/log', label: 'nav.log', icon: PenLine },
    { path: '/entries', label: 'nav.entries', icon: FileText },
    { path: '/metrics', label: 'nav.metrics', icon: Activity },
    { path: '/insights', label: 'nav.insights', icon: Lightbulb },
    { path: '/correlations', label: 'nav.correlations', icon: Link2 }
  ];

  function isActive(path: string): boolean {
    return $location === path || $location.startsWith(path + '/');
  }

  function close() {
    open = false;
    dispatch('close');
  }

  async function handleLogout() {
    await authActions.logout();
    close();
  }

  function handleBackdropClick() {
    close();
  }

  function handleNavClick() {
    // Close drawer after navigation on mobile
    close();
  }
</script>

{#if open}
  <!-- Backdrop -->
  <div
    class="md:hidden fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300"
    on:click={handleBackdropClick}
    on:keydown={(e) => e.key === 'Escape' && close()}
    role="button"
    tabindex="0"
    aria-label={$t('nav.closeMenu')}
  ></div>

  <!-- Drawer -->
  <aside
    class="md:hidden fixed top-0 left-0 h-full w-80 max-w-[85vw] bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out flex flex-col"
  >
    <!-- Header -->
    <div class="flex items-center justify-between h-16 px-4 border-b border-gray-200 flex-shrink-0">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
          <Heart size={20} class="text-white" />
        </div>
        <h1 class="text-xl font-bold text-gray-800">Feelink</h1>
      </div>
      <button
        on:click={close}
        class="p-2 rounded-lg text-gray-500 hover:bg-gray-100 active:bg-gray-200 transition-colors"
        aria-label={$t('nav.closeMenu')}
      >
        <X size={24} />
      </button>
    </div>

    <!-- Navigation Items -->
    <nav class="flex-1 py-4 overflow-y-auto">
      <ul class="space-y-1 px-3">
        {#each navItems as item}
          <li>
            <a
              href={`#${item.path}`}
              on:click={handleNavClick}
              class="flex items-center px-4 py-3 space-x-3 rounded-lg transition-colors {isActive(
                item.path
              )
                ? 'bg-primary-50 text-primary-700'
                : 'text-gray-700 hover:bg-gray-50 active:bg-gray-100'}"
            >
              <svelte:component
                this={item.icon}
                size={22}
                strokeWidth={isActive(item.path) ? 2.5 : 2}
              />
              <span class="font-medium">{$t(item.label)}</span>
            </a>
          </li>
        {/each}
      </ul>
    </nav>

    <!-- Bottom Section -->
    <div class="border-t border-gray-200 p-3">
      <button
        on:click={handleLogout}
        class="flex items-center w-full px-4 py-3 space-x-3 rounded-lg text-red-600 hover:bg-red-50 active:bg-red-100 transition-colors"
      >
        <LogOut size={22} />
        <span class="font-medium">{$t('nav.logout')}</span>
      </button>
    </div>
  </aside>
{/if}
