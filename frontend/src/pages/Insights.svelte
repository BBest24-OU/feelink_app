<script lang="ts">
  import { onMount } from 'svelte';
  import { metricsActions, activeMetrics } from '../stores/metrics';
  import { entriesActions, entriesStore } from '../stores/entries';
  import type { Metric } from '../stores/metrics';
  import type { Entry } from '../stores/entries';
  import { t } from '../i18n';
  import AuthenticatedLayout from '../components/AuthenticatedLayout.svelte';
  import Card from '../components/Card.svelte';
  import EChart from '../components/EChart.svelte';
  import type { EChartsOption } from 'echarts';
  import { subDays, format } from 'date-fns';
  import { TrendingUp, TrendingDown, Minus as MinusIcon } from 'lucide-svelte';

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

  // Prepare ECharts option
  $: chartOption = (() => {
    const colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'];

    const series = selectedMetrics.map((metricId, index) => {
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

          return [entry.entry_date, yValue];
        })
        .filter((d) => d !== null);

      return {
        name: metric.name_key,
        type: 'line',
        data,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 2,
        },
        itemStyle: {
          color: colors[index % colors.length],
        },
      };
    }).filter((s) => s !== null);

    return {
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%',
        top: selectedMetrics.length > 1 ? '15%' : '10%',
      },
      xAxis: {
        type: 'time',
        name: 'Date',
        nameLocation: 'middle',
        nameGap: 30,
      },
      yAxis: {
        type: 'value',
        name: 'Value',
        nameLocation: 'middle',
        nameGap: 40,
      },
      series,
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
        },
      },
      legend: selectedMetrics.length > 1 ? {
        top: 0,
        left: 'center',
      } : undefined,
    } as EChartsOption;
  })();

  // Calculate statistics for a metric
  function calculateStats(metric: Metric, entries: Entry[]) {
    const values = entries
      .flatMap((e) => e.values)
      .filter((v) => v.metric_id === metric.id)
      .map((v) => {
        if (metric.value_type === 'boolean') return v.value_boolean ? 1 : 0;
        return v.value_numeric ?? 0;
      })
      .filter((v) => v !== null && v !== undefined);

    const count = values.length;
    if (count === 0) return null;

    const mean = values.reduce((a, b) => a + b, 0) / count;
    const min = Math.min(...values);
    const max = Math.max(...values);

    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    const median = sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];

    const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / count;
    const stdDev = Math.sqrt(variance);

    // Calculate trend (last 7 days vs previous 7 days)
    let trend: 'up' | 'down' | 'neutral' = 'neutral';
    if (entries.length >= 14) {
      const sortedEntries = [...entries].sort(
        (a, b) => new Date(b.entry_date).getTime() - new Date(a.entry_date).getTime()
      );

      const recentValues = sortedEntries
        .slice(0, 7)
        .flatMap((e) => e.values)
        .filter((v) => v.metric_id === metric.id)
        .map((v) => (metric.value_type === 'boolean' ? (v.value_boolean ? 1 : 0) : v.value_numeric ?? 0));

      const previousValues = sortedEntries
        .slice(7, 14)
        .flatMap((e) => e.values)
        .filter((v) => v.metric_id === metric.id)
        .map((v) => (metric.value_type === 'boolean' ? (v.value_boolean ? 1 : 0) : v.value_numeric ?? 0));

      if (recentValues.length > 0 && previousValues.length > 0) {
        const recentAvg = recentValues.reduce((a, b) => a + b, 0) / recentValues.length;
        const previousAvg = previousValues.reduce((a, b) => a + b, 0) / previousValues.length;
        const diff = ((recentAvg - previousAvg) / previousAvg) * 100;

        if (Math.abs(diff) >= 5) {
          trend = diff > 0 ? 'up' : 'down';
        }
      }
    }

    return { count, mean, median, stdDev, min, max, trend };
  }

  function formatValue(val: number, metric: Metric): string {
    if (metric.value_type === 'boolean') {
      return val === 1 ? 'Yes' : 'No';
    }
    return val.toFixed(2);
  }

  function toggleMetric(metricId: number) {
    if (selectedMetrics.includes(metricId)) {
      selectedMetrics = selectedMetrics.filter((id) => id !== metricId);
    } else {
      selectedMetrics = [...selectedMetrics, metricId];
    }
  }
</script>

<AuthenticatedLayout>
  <!-- Minimal Header -->
  <div class="mb-12">
    <h1 class="text-2xl font-semibold text-gray-900 dark:text-white mb-1">
      Insights & Analytics
    </h1>
    <p class="text-sm text-gray-600 dark:text-gray-400">
      Visualize your metrics and discover trends over time.
    </p>
  </div>

  {#if loading}
    <div class="text-center py-12">
      <div class="inline-block animate-spin w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full"></div>
      <p class="mt-4 text-sm text-gray-600 dark:text-gray-400">Loading insights...</p>
    </div>
  {:else if $activeMetrics.length === 0}
    <Card>
      <div class="text-center py-12">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
          No metrics available. Create some metrics to see insights!
        </p>
        <a
          href="#/metrics"
          class="inline-block px-4 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 dark:bg-primary-500 dark:hover:bg-primary-600 transition-colors"
        >
          Create Metrics
        </a>
      </div>
    </Card>
  {:else}
    <!-- Controls -->
    <Card>
      <div class="flex flex-wrap items-center gap-6">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Date Range
          </label>
          <select
            bind:value={dateRange}
            class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="all">All time</option>
          </select>
        </div>
      </div>
    </Card>

    <!-- Metric Selection -->
    <Card>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Select Metrics
      </h2>
      <div class="flex flex-wrap gap-2">
        {#each $activeMetrics as metric}
          <button
            on:click={() => toggleMetric(metric.id)}
            class="px-3 py-1.5 text-sm rounded-lg border transition-colors duration-150"
            class:bg-primary-600={selectedMetrics.includes(metric.id)}
            class:text-white={selectedMetrics.includes(metric.id)}
            class:border-primary-600={selectedMetrics.includes(metric.id)}
            class:dark:bg-primary-500={selectedMetrics.includes(metric.id)}
            class:dark:border-primary-500={selectedMetrics.includes(metric.id)}
            class:bg-white={!selectedMetrics.includes(metric.id)}
            class:dark:bg-gray-800={!selectedMetrics.includes(metric.id)}
            class:text-gray-700={!selectedMetrics.includes(metric.id)}
            class:dark:text-gray-300={!selectedMetrics.includes(metric.id)}
            class:border-gray-300={!selectedMetrics.includes(metric.id)}
            class:dark:border-gray-600={!selectedMetrics.includes(metric.id)}
            class:hover:border-gray-400={!selectedMetrics.includes(metric.id)}
            class:dark:hover:border-gray-500={!selectedMetrics.includes(metric.id)}
          >
            {metric.name_key}
          </button>
        {/each}
      </div>
    </Card>

    {#if selectedMetrics.length > 0}
      <!-- Trend Chart -->
      <Card>
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
          Trend Over Time
        </h2>
        {#if chartOption.series && chartOption.series.length > 0}
          <EChart option={chartOption} height="400px" />
        {:else}
          <p class="text-sm text-gray-600 dark:text-gray-400 py-8 text-center">
            No data available for the selected date range
          </p>
        {/if}
      </Card>

      <!-- Statistics -->
      <Card>
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
          Statistics
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each selectedMetrics as metricId}
            {@const metric = $activeMetrics.find((m) => m.id === metricId)}
            {#if metric}
              {@const stats = calculateStats(metric, filteredEntries)}
              {#if stats}
                <div class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-4">
                    {metric.name_key}
                  </h3>

                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                        Count
                      </div>
                      <div class="text-lg font-semibold text-gray-900 dark:text-white">
                        {stats.count}
                      </div>
                    </div>

                    <div>
                      <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                        Mean
                      </div>
                      <div class="text-lg font-semibold text-gray-900 dark:text-white">
                        {formatValue(stats.mean, metric)}
                      </div>
                    </div>

                    <div>
                      <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                        Median
                      </div>
                      <div class="text-lg font-semibold text-gray-900 dark:text-white">
                        {formatValue(stats.median, metric)}
                      </div>
                    </div>

                    <div>
                      <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                        Std Dev
                      </div>
                      <div class="text-lg font-semibold text-gray-900 dark:text-white">
                        {stats.stdDev.toFixed(2)}
                      </div>
                    </div>

                    {#if metric.value_type !== 'boolean'}
                      <div>
                        <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                          Min
                        </div>
                        <div class="text-lg font-semibold text-gray-900 dark:text-white">
                          {formatValue(stats.min, metric)}
                        </div>
                      </div>

                      <div>
                        <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                          Max
                        </div>
                        <div class="text-lg font-semibold text-gray-900 dark:text-white">
                          {formatValue(stats.max, metric)}
                        </div>
                      </div>
                    {/if}

                    <div class="col-span-2">
                      <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">
                        7-Day Trend
                      </div>
                      <div class="flex items-center gap-1 text-sm font-medium">
                        {#if stats.trend === 'up'}
                          <TrendingUp size={14} class="text-green-600 dark:text-green-500" />
                          <span class="text-green-600 dark:text-green-500">Increasing</span>
                        {:else if stats.trend === 'down'}
                          <TrendingDown size={14} class="text-red-600 dark:text-red-500" />
                          <span class="text-red-600 dark:text-red-500">Decreasing</span>
                        {:else}
                          <MinusIcon size={14} class="text-gray-600 dark:text-gray-400" />
                          <span class="text-gray-600 dark:text-gray-400">Stable</span>
                        {/if}
                      </div>
                    </div>
                  </div>
                </div>
              {:else}
                <div class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    {metric.name_key}
                  </h3>
                  <p class="text-xs text-gray-600 dark:text-gray-400">No data available</p>
                </div>
              {/if}
            {/if}
          {/each}
        </div>
      </Card>
    {:else}
      <Card>
        <div class="text-center py-12">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Select at least one metric to view insights
          </p>
        </div>
      </Card>
    {/if}
  {/if}
</AuthenticatedLayout>
