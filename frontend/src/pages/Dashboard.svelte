<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore, authActions } from '../stores/user';
  import { metricsActions, activeMetrics } from '../stores/metrics';
  import { entriesActions, entriesStore } from '../stores/entries';
  import { syncStatus } from '../lib/sync';
  import { t } from '../i18n';
  import AuthenticatedLayout from '../components/AuthenticatedLayout.svelte';
  import Card from '../components/Card.svelte';
  import Button from '../components/Button.svelte';
  import CalendarHeatmap from '../components/CalendarHeatmap.svelte';
  import { format, subDays, parseISO } from 'date-fns';

  onMount(async () => {
    // Ensure user is authenticated before loading data
    if (!$authStore.accessToken) {
      window.location.hash = '/login';
      return;
    }

    // Load user profile first to ensure we have user data
    if (!$authStore.user) {
      await authActions.loadProfile();
    }

    // Then load metrics and entries
    await metricsActions.load(false);
    await entriesActions.load({ limit: 100 });
  });

  function handleDateClick(date: string) {
    window.location.hash = `/log?date=${date}`;
  }

  // Calculate current streak
  $: currentStreak = (() => {
    if ($entriesStore.entries.length === 0) return 0;

    const sortedEntries = [...$entriesStore.entries].sort(
      (a, b) => new Date(b.entry_date).getTime() - new Date(a.entry_date).getTime()
    );

    let streak = 0;
    let currentDate = new Date();
    const today = format(currentDate, 'yyyy-MM-dd');

    // Check if there's an entry for today
    const todayEntry = sortedEntries.find((e) => e.entry_date === today);
    if (!todayEntry) {
      // If no entry today, check yesterday
      currentDate = subDays(currentDate, 1);
    }

    // Count consecutive days
    for (let i = 0; i < sortedEntries.length; i++) {
      const expectedDate = format(subDays(currentDate, streak), 'yyyy-MM-dd');
      const entry = sortedEntries.find((e) => e.entry_date === expectedDate);

      if (entry && entry.values.length > 0) {
        streak++;
      } else {
        break;
      }
    }

    return streak;
  })();
</script>

<AuthenticatedLayout>
  <div class="mb-8">
    <h2 class="text-3xl font-bold text-gray-800">
      {$t('dashboard.welcome')}, {$authStore.user?.email?.split('@')[0]}!
    </h2>
    <p class="text-gray-600 mt-2">Track your well-being and discover meaningful patterns in your life.</p>
  </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <Card>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">{$t('dashboard.currentStreak')}</h3>
        <p class="text-4xl font-bold text-primary-600">{currentStreak}</p>
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

      <Card>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">Sync Status</h3>
        <p class="text-2xl font-bold" class:text-green-600={$syncStatus.isOnline} class:text-red-600={!$syncStatus.isOnline}>
          {$syncStatus.isOnline ? 'Online' : 'Offline'}
        </p>
        {#if $syncStatus.pendingCount > 0}
          <p class="text-sm text-gray-500 mt-1">{$syncStatus.pendingCount} pending</p>
        {:else}
          <p class="text-sm text-gray-500 mt-1">All synced</p>
        {/if}
      </Card>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
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

  <Card>
    <h2 class="text-xl font-bold text-gray-800 mb-4">Entry Calendar</h2>
    <CalendarHeatmap entries={$entriesStore.entries} onDateClick={handleDateClick} />
  </Card>
</AuthenticatedLayout>
