<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore, authActions } from '../stores/user';
  import { metricsActions, activeMetrics } from '../stores/metrics';
  import { entriesActions, entriesStore } from '../stores/entries';
  import { t } from '../i18n';
  import Card from '../components/Card.svelte';
  import Button from '../components/Button.svelte';

  onMount(async () => {
    await metricsActions.load(false);
    await entriesActions.load({ limit: 10 });
  });

  function handleLogout() {
    authActions.logout();
    window.location.hash = '/login';
  }
</script>

<div class="min-h-screen bg-gray-50">
  <nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="container mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-primary-600">FeelInk</h1>
        <div class="flex items-center space-x-6">
          <a href="#/dashboard" class="text-gray-700 hover:text-primary-600 font-medium">
            {$t('nav.dashboard')}
          </a>
          <a href="#/log" class="text-gray-700 hover:text-primary-600 font-medium">
            {$t('nav.log')}
          </a>
          <a href="#/metrics" class="text-gray-700 hover:text-primary-600 font-medium">
            {$t('nav.metrics')}
          </a>
          <a href="#/entries" class="text-gray-700 hover:text-primary-600 font-medium">
            Entries
          </a>
          <Button size="sm" variant="ghost" on:click={handleLogout}>
            {$t('auth.logout')}
          </Button>
        </div>
      </div>
    </div>
  </nav>

  <div class="container mx-auto p-6">
    <div class="mb-8">
      <h2 class="text-3xl font-bold text-gray-800">
        {$t('dashboard.welcome')}, {$authStore.user?.email}!
      </h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <Card>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">{$t('dashboard.currentStreak')}</h3>
        <p class="text-4xl font-bold text-primary-600">0</p>
        <p class="text-sm text-gray-500 mt-1">days</p>
      </Card>

      <Card>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">{$t('dashboard.totalEntries')}</h3>
        <p class="text-4xl font-bold text-secondary-600">{$entriesStore.total}</p>
        <p class="text-sm text-gray-500 mt-1">entries</p>
      </Card>

      <Card>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">Active Metrics</h3>
        <p class="text-4xl font-bold text-indigo-600">{$activeMetrics.length}</p>
        <p class="text-sm text-gray-500 mt-1">metrics</p>
      </Card>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Card>
        <h2 class="text-xl font-bold text-gray-800 mb-4">{$t('dashboard.quickLog')}</h2>
        <p class="text-gray-600 mb-4">Ready to log today's entry?</p>
        <a
          href="#/log"
          class="inline-block px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          {$t('dashboard.quickLog')}
        </a>
      </Card>

      <Card>
        <h2 class="text-xl font-bold text-gray-800 mb-4">{$t('dashboard.recentActivity')}</h2>
        {#if $entriesStore.entries.length > 0}
          <div class="space-y-2">
            {#each $entriesStore.entries.slice(0, 5) as entry}
              <div class="flex justify-between items-center py-2 border-b border-gray-100">
                <span class="text-sm text-gray-700">{entry.entry_date}</span>
                <span class="text-xs text-gray-500">{entry.values.length} metrics</span>
              </div>
            {/each}
          </div>
          <a href="#/entries" class="text-sm text-primary-600 hover:underline mt-4 inline-block">
            View all entries →
          </a>
        {:else}
          <p class="text-gray-500">No recent entries</p>
        {/if}
      </Card>
    </div>
  </div>
</div>
