<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore } from '../stores/user';
  import { t } from '../i18n';
  import Card from '../components/Card.svelte';

  onMount(async () => {
    // Load user data if needed
  });
</script>

<div class="container mx-auto p-6">
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-gray-800">
      {$t('dashboard.welcome')}, {$authStore.user?.email}!
    </h1>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
    <Card>
      <h3 class="text-lg font-semibold text-gray-700 mb-2">{$t('dashboard.currentStreak')}</h3>
      <p class="text-4xl font-bold text-primary-600">0</p>
      <p class="text-sm text-gray-500 mt-1">days</p>
    </Card>

    <Card>
      <h3 class="text-lg font-semibold text-gray-700 mb-2">{$t('dashboard.totalEntries')}</h3>
      <p class="text-4xl font-bold text-secondary-600">0</p>
      <p class="text-sm text-gray-500 mt-1">entries</p>
    </Card>

    <Card>
      <h3 class="text-lg font-semibold text-gray-700 mb-2">Active Metrics</h3>
      <p class="text-4xl font-bold text-indigo-600">0</p>
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
      <p class="text-gray-500">No recent entries</p>
    </Card>
  </div>
</div>
