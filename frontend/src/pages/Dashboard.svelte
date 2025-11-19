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
  import { TrendingUp, FileText, Activity, Wifi, WifiOff, Calendar as CalendarIcon, ArrowRight } from 'lucide-svelte';

  onMount(async () => {
    if (!$authStore.accessToken) {
      window.location.hash = '/login';
      return;
    }

    if (!$authStore.user) {
      await authActions.loadProfile();
    }

    await metricsActions.load(false);
    await entriesActions.load({ limit: 100 });
  });

  function handleDateClick(date: string) {
    window.location.hash = `/log?date=${date}`;
  }

  $: currentStreak = (() => {
    if ($entriesStore.entries.length === 0) return 0;

    const sortedEntries = [...$entriesStore.entries].sort(
      (a, b) => new Date(b.entry_date).getTime() - new Date(a.entry_date).getTime()
    );

    let streak = 0;
    let currentDate = new Date();
    const today = format(currentDate, 'yyyy-MM-dd');

    const todayEntry = sortedEntries.find((e) => e.entry_date === today);
    if (!todayEntry) {
      currentDate = subDays(currentDate, 1);
    }

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
  <!-- Minimal Header -->
  <div class="mb-12">
    <h1 class="text-2xl font-semibold text-gray-900 dark:text-white mb-1">
      {$t('dashboard.welcome')}, {$authStore.user?.email?.split('@')[0] || $authStore.user?.email}
    </h1>
    <p class="text-sm text-gray-600 dark:text-gray-400">
      Track your well-being and discover meaningful patterns in your life.
    </p>
  </div>

  <!-- Minimal Stats Grid -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
    <!-- Streak Card -->
    <Card>
      <div class="flex items-center justify-between mb-4">
        <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
          {$t('dashboard.currentStreak')}
        </div>
        <TrendingUp size={16} class="text-gray-400 dark:text-gray-500" />
      </div>
      <div class="text-3xl font-semibold text-gray-900 dark:text-white mb-1">
        {currentStreak}
      </div>
      <div class="text-xs text-gray-500 dark:text-gray-500">
        days in a row
      </div>
    </Card>

    <!-- Total Entries Card -->
    <Card>
      <div class="flex items-center justify-between mb-4">
        <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
          {$t('dashboard.totalEntries')}
        </div>
        <FileText size={16} class="text-gray-400 dark:text-gray-500" />
      </div>
      <div class="text-3xl font-semibold text-gray-900 dark:text-white mb-1">
        {$entriesStore.total}
      </div>
      <div class="text-xs text-gray-500 dark:text-gray-500">
        journal entries
      </div>
    </Card>

    <!-- Active Metrics Card -->
    <Card>
      <div class="flex items-center justify-between mb-4">
        <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
          Active Metrics
        </div>
        <Activity size={16} class="text-gray-400 dark:text-gray-500" />
      </div>
      <div class="text-3xl font-semibold text-gray-900 dark:text-white mb-1">
        {$activeMetrics.length}
      </div>
      <div class="text-xs text-gray-500 dark:text-gray-500">
        tracking now
      </div>
    </Card>

    <!-- Sync Status Card -->
    <Card>
      <div class="flex items-center justify-between mb-4">
        <div class="text-sm font-medium text-gray-600 dark:text-gray-400">
          Sync Status
        </div>
        {#if $syncStatus.isOnline}
          <Wifi size={16} class="text-green-600 dark:text-green-500" />
        {:else}
          <WifiOff size={16} class="text-gray-400 dark:text-gray-500" />
        {/if}
      </div>
      <div class="text-xl font-semibold text-gray-900 dark:text-white mb-1">
        {$syncStatus.isOnline ? 'Online' : 'Offline'}
      </div>
      <div class="text-xs text-gray-500 dark:text-gray-500">
        {#if $syncStatus.pendingCount > 0}
          {$syncStatus.pendingCount} pending
        {:else}
          all synced
        {/if}
      </div>
    </Card>
  </div>

  <!-- Quick Actions Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
    <!-- Quick Log Card -->
    <Card>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {$t('dashboard.quickLog')}
      </h2>
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
        Ready to log today's entry? Track your metrics and see how you're feeling.
      </p>
      <a href="#/log">
        <Button variant="primary" fullWidth={true}>
          <span class="flex items-center justify-center gap-2">
            <span>{$t('dashboard.quickLog')}</span>
            <ArrowRight size={16} />
          </span>
        </Button>
      </a>
    </Card>

    <!-- Recent Activity Card -->
    <Card>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        {$t('dashboard.recentActivity')}
      </h2>
      {#if $entriesStore.entries.length > 0}
        <div class="space-y-2 mb-4">
          {#each $entriesStore.entries.slice(0, 5) as entry}
            <div class="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700 last:border-0">
              <div class="flex items-center gap-3">
                <CalendarIcon size={14} class="text-gray-400 dark:text-gray-500" />
                <span class="text-sm text-gray-700 dark:text-gray-300">{entry.entry_date}</span>
              </div>
              <span class="text-xs text-gray-500 dark:text-gray-400">
                {entry.values.length} metrics
              </span>
            </div>
          {/each}
        </div>
        <a href="#/entries" class="inline-flex items-center gap-1 text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium">
          <span>View all entries</span>
          <ArrowRight size={14} />
        </a>
      {:else}
        <div class="text-center py-8">
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">No recent entries yet</p>
          <a href="#/log">
            <Button variant="secondary" size="sm">Create your first entry</Button>
          </a>
        </div>
      {/if}
    </Card>
  </div>

  <!-- Calendar Heatmap -->
  <Card>
    <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">Entry Calendar</h2>
    <div class="overflow-x-auto">
      <CalendarHeatmap entries={$entriesStore.entries} onDateClick={handleDateClick} />
    </div>
  </Card>
</AuthenticatedLayout>
