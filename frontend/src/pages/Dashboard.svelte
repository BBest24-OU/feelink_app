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
  import { TrendingUp, FileText, Activity, Wifi, WifiOff, Flame, Calendar as CalendarIcon, ArrowRight, Hand, Check } from 'lucide-svelte';

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
  <!-- Welcome Header -->
  <div class="mb-8 animate-slide-down">
    <div class="flex items-center gap-3 mb-2">
      <h2 class="text-3xl md:text-4xl font-bold text-gray-800">
        {$t('dashboard.welcome')}, {$authStore.user?.email?.split('@')[0] || $authStore.user?.email}!
      </h2>
      <div class="animate-bounce-soft">
        <Hand size={32} class="text-yellow-500" />
      </div>
    </div>
    <p class="text-gray-600 text-lg">Track your well-being and discover meaningful patterns in your life.</p>
  </div>

  <!-- Stats Cards Grid -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
    <!-- Streak Card -->
    <div class="group relative overflow-hidden bg-gradient-to-br from-orange-500 to-pink-600 rounded-2xl shadow-soft hover:shadow-strong transition-all duration-300 hover:-translate-y-1 animate-fade-in">
      <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
      <div class="relative p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
            <Flame class="text-white" size={24} />
          </div>
          <TrendingUp class="text-white/50" size={20} />
        </div>
        <h3 class="text-white/90 text-sm font-medium mb-2">{$t('dashboard.currentStreak')}</h3>
        <p class="text-4xl md:text-5xl font-bold text-white mb-1">{currentStreak}</p>
        <div class="flex items-center gap-2">
          <p class="text-white/80 text-sm">days in a row</p>
          <Flame size={18} class="text-orange-300" />
        </div>
      </div>
    </div>

    <!-- Total Entries Card -->
    <div class="group relative overflow-hidden bg-gradient-to-br from-blue-500 to-cyan-600 rounded-2xl shadow-soft hover:shadow-strong transition-all duration-300 hover:-translate-y-1 animate-fade-in" style="animation-delay: 0.1s">
      <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
      <div class="relative p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
            <FileText class="text-white" size={24} />
          </div>
          <TrendingUp class="text-white/50" size={20} />
        </div>
        <h3 class="text-white/90 text-sm font-medium mb-2">{$t('dashboard.totalEntries')}</h3>
        <p class="text-4xl md:text-5xl font-bold text-white mb-1">{$entriesStore.total}</p>
        <p class="text-white/80 text-sm">journal entries</p>
      </div>
    </div>

    <!-- Active Metrics Card -->
    <div class="group relative overflow-hidden bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl shadow-soft hover:shadow-strong transition-all duration-300 hover:-translate-y-1 animate-fade-in" style="animation-delay: 0.2s">
      <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
      <div class="relative p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
            <Activity class="text-white" size={24} />
          </div>
          <TrendingUp class="text-white/50" size={20} />
        </div>
        <h3 class="text-white/90 text-sm font-medium mb-2">Active Metrics</h3>
        <p class="text-4xl md:text-5xl font-bold text-white mb-1">{$activeMetrics.length}</p>
        <p class="text-white/80 text-sm">tracking now</p>
      </div>
    </div>

    <!-- Sync Status Card -->
    <div class="group relative overflow-hidden bg-gradient-to-br {$syncStatus.isOnline ? 'from-green-500 to-emerald-600' : 'from-gray-500 to-gray-600'} rounded-2xl shadow-soft hover:shadow-strong transition-all duration-300 hover:-translate-y-1 animate-fade-in" style="animation-delay: 0.3s">
      <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
      <div class="relative p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
            {#if $syncStatus.isOnline}
              <Wifi class="text-white" size={24} />
            {:else}
              <WifiOff class="text-white" size={24} />
            {/if}
          </div>
        </div>
        <h3 class="text-white/90 text-sm font-medium mb-2">Sync Status</h3>
        <p class="text-2xl md:text-3xl font-bold text-white mb-1">
          {$syncStatus.isOnline ? 'Online' : 'Offline'}
        </p>
        {#if $syncStatus.pendingCount > 0}
          <p class="text-white/80 text-sm">{$syncStatus.pendingCount} pending sync</p>
        {:else}
          <div class="flex items-center gap-2">
            <p class="text-white/80 text-sm">All synced</p>
            <Check size={16} class="text-green-300 stroke-[3]" />
          </div>
        {/if}
      </div>
    </div>
  </div>

  <!-- Quick Actions Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
    <!-- Quick Log Card -->
    <Card gradient={true} hover={false}>
      <div class="flex items-center gap-3 mb-4">
        <div class="p-2 bg-gradient-primary rounded-xl">
          <CalendarIcon class="text-white" size={20} />
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-gray-800">{$t('dashboard.quickLog')}</h2>
      </div>
      <p class="text-gray-600 mb-6">Ready to log today's entry? Track your metrics and see how you're feeling.</p>
      <a href="#/log">
        <Button variant="gradient" fullWidth={true}>
          <span class="flex items-center justify-center gap-2">
            <span>{$t('dashboard.quickLog')}</span>
            <ArrowRight size={18} />
          </span>
        </Button>
      </a>
    </Card>

    <!-- Recent Activity Card -->
    <Card gradient={false} hover={false}>
      <div class="flex items-center gap-3 mb-4">
        <div class="p-2 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl">
          <Activity class="text-white" size={20} />
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-gray-800">{$t('dashboard.recentActivity')}</h2>
      </div>
      {#if $entriesStore.entries.length > 0}
        <div class="space-y-2 mb-4">
          {#each $entriesStore.entries.slice(0, 5) as entry, index}
            <div class="flex justify-between items-center p-3 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors duration-200 animate-fade-in" style="animation-delay: {index * 0.05}s">
              <div class="flex items-center gap-3">
                <div class="p-2 bg-primary-100 rounded-lg">
                  <CalendarIcon class="text-primary-600" size={16} />
                </div>
                <span class="font-medium text-gray-700">{entry.entry_date}</span>
              </div>
              <span class="text-sm font-semibold text-primary-600 bg-primary-50 px-3 py-1 rounded-full">
                {entry.values.length} metrics
              </span>
            </div>
          {/each}
        </div>
        <a href="#/entries" class="group inline-flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium transition-colors">
          <span>View all entries</span>
          <ArrowRight size={16} class="group-hover:translate-x-1 transition-transform" />
        </a>
      {:else}
        <div class="text-center py-8">
          <p class="text-gray-500 mb-4">No recent entries yet</p>
          <a href="#/log">
            <Button variant="secondary" size="sm">Create your first entry</Button>
          </a>
        </div>
      {/if}
    </Card>
  </div>

  <!-- Calendar Heatmap -->
  <Card gradient={false} hover={false}>
    <div class="flex items-center gap-3 mb-6">
      <div class="p-2 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-xl">
        <CalendarIcon class="text-white" size={20} />
      </div>
      <h2 class="text-xl md:text-2xl font-bold text-gray-800">Entry Calendar</h2>
    </div>
    <div class="overflow-x-auto">
      <CalendarHeatmap entries={$entriesStore.entries} onDateClick={handleDateClick} />
    </div>
  </Card>
</AuthenticatedLayout>
