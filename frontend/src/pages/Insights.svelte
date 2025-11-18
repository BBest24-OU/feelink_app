<script lang="ts">
  import { onMount } from 'svelte';
  import { metricsActions, activeMetrics } from '../stores/metrics';
  import { entriesActions, entriesStore } from '../stores/entries';
  import type { Metric } from '../stores/metrics';
  import type { Entry } from '../stores/entries';
  import { t } from '../i18n';
  import Card from '../components/Card.svelte';
  import LineChart from '../components/LineChart.svelte';
  import StatisticsPanel from '../components/StatisticsPanel.svelte';
  import Select from '../components/Select.svelte';
  import { subDays, format } from 'date-fns';

  let selectedMetrics: number[] = [];
  let dateRange: '7d' | '30d' | '90d' | 'all' = '30d';
  let loading = false;

  onMount(async () => {
    loading = true;
    await metricsActions.load(false);
    await entriesActions.load();

    // Auto-select first metric if available
    if ($activeMetrics.length > 0) {
      selectedMetrics = [$activeMetrics[0].id];
    }

    loading = false;
  });

  // Filter entries by date range
  $: filteredEntries = (() => {
    if (dateRange === 'all') return $entriesStore.entries;

    const days = dateRange === '7d' ? 7 : dateRange === '30d' ? 30 : 90;
    const cutoffDate = format(subDays(new Date(), days), 'yyyy-MM-dd');

    return $entriesStore.entries.filter((e) => e.entry_date >= cutoffDate);
  })();

  // Prepare chart datasets
  $: chartDatasets = selectedMetrics
    .map((metricId) => {
      const metric = $activeMetrics.find((m) => m.id === metricId);
      if (!metric) return null;

      const data = filteredEntries
        .map((entry) => {
          const value = entry.values.find((v) => v.metric_id === metricId);
          if (!value) return null;

          let yValue = 0;
          if (metric.value_type === 'boolean') {
            yValue = value.value_boolean ? 1 : 0;
          } else if (value.value_numeric !== null && value.value_numeric !== undefined) {
            yValue = value.value_numeric;
          }

          return {
            x: entry.entry_date,
            y: yValue,
          };
        })
        .filter((d) => d !== null)
        .sort((a, b) => new Date(a!.x).getTime() - new Date(b!.x).getTime()) as Array<{
        x: string;
        y: number;
      }>;

      return {
        label: metric.name_key,
        data,
        borderColor: metric.color || undefined,
        backgroundColor: metric.color ? `${metric.color}33` : undefined,
      };
    })
    .filter((ds) => ds !== null) as Array<{
    label: string;
    data: Array<{ x: string; y: number }>;
    borderColor?: string;
    backgroundColor?: string;
  }>;

  function toggleMetric(metricId: number) {
    if (selectedMetrics.includes(metricId)) {
      selectedMetrics = selectedMetrics.filter((id) => id !== metricId);
    } else {
      selectedMetrics = [...selectedMetrics, metricId];
    }
  }
</script>

<div class="min-h-screen bg-gray-50 p-6">
  <div class="container mx-auto">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-800">Insights & Analytics</h1>
      <p class="text-gray-600 mt-2">Visualize your metrics and discover trends</p>
    </div>

    {#if loading}
      <div class="text-center py-12">
        <div class="inline-block animate-spin w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full"></div>
        <p class="mt-4 text-gray-600">Loading insights...</p>
      </div>
    {:else if $activeMetrics.length === 0}
      <Card>
        <div class="text-center py-12">
          <p class="text-gray-600 mb-4">No metrics available. Create some metrics to see insights!</p>
          <a
            href="#/metrics"
            class="inline-block px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Create Metrics
          </a>
        </div>
      </Card>
    {:else}
      <!-- Controls -->
      <div class="mb-6 flex flex-wrap gap-4">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 mb-2">Date Range</label>
          <select
            bind:value={dateRange}
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="all">All time</option>
          </select>
        </div>
      </div>

      <!-- Metric Selection -->
      <Card>
        <h2 class="text-xl font-bold text-gray-800 mb-4">Select Metrics to View</h2>
        <div class="flex flex-wrap gap-2">
          {#each $activeMetrics as metric}
            <button
              on:click={() => toggleMetric(metric.id)}
              class="px-4 py-2 rounded-lg border-2 transition-colors"
              class:bg-primary-600={selectedMetrics.includes(metric.id)}
              class:text-white={selectedMetrics.includes(metric.id)}
              class:border-primary-600={selectedMetrics.includes(metric.id)}
              class:bg-white={!selectedMetrics.includes(metric.id)}
              class:text-gray-700={!selectedMetrics.includes(metric.id)}
              class:border-gray-300={!selectedMetrics.includes(metric.id)}
            >
              {metric.name_key}
            </button>
          {/each}
        </div>
      </Card>

      {#if selectedMetrics.length > 0}
        <!-- Trend Chart -->
        <div class="mt-6">
          <Card>
            <h2 class="text-xl font-bold text-gray-800 mb-4">Trend Over Time</h2>
            {#if chartDatasets.length > 0 && chartDatasets.some((ds) => ds.data.length > 0)}
              <LineChart
                title=""
                datasets={chartDatasets}
                height={400}
                xAxisType="time"
              />
            {:else}
              <p class="text-gray-500 py-8 text-center">No data available for the selected date range</p>
            {/if}
          </Card>
        </div>

        <!-- Statistics Panels -->
        <div class="mt-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-4">Statistics</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each selectedMetrics as metricId}
              {@const metric = $activeMetrics.find((m) => m.id === metricId)}
              {#if metric}
                <StatisticsPanel {metric} entries={filteredEntries} />
              {/if}
            {/each}
          </div>
        </div>
      {:else}
        <Card>
          <div class="text-center py-12">
            <p class="text-gray-600">Select at least one metric to view insights</p>
          </div>
        </Card>
      {/if}
    {/if}
  </div>
</div>
