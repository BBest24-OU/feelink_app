<script lang="ts">
  import type { Entry } from '../stores/entries';
  import type { Metric } from '../stores/metrics';
  import Card from './Card.svelte';
  import { t } from '../i18n';

  export let metric: Metric;
  export let entries: Entry[] = [];

  // Calculate statistics
  $: values = entries
    .flatMap((e) => e.values)
    .filter((v) => v.metric_id === metric.id)
    .map((v) => {
      if (metric.value_type === 'boolean') return v.value_boolean ? 1 : 0;
      return v.value_numeric ?? 0;
    })
    .filter((v) => v !== null && v !== undefined);

  $: count = values.length;
  $: mean = count > 0 ? values.reduce((a, b) => a + b, 0) / count : 0;
  $: min = count > 0 ? Math.min(...values) : 0;
  $: max = count > 0 ? Math.max(...values) : 0;

  // Calculate median
  $: median = (() => {
    if (count === 0) return 0;
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
  })();

  // Calculate standard deviation
  $: stdDev = (() => {
    if (count < 2) return 0;
    const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / count;
    return Math.sqrt(variance);
  })();

  // Calculate trend (last 7 days vs previous 7 days)
  $: trend = (() => {
    if (entries.length < 14) return 'neutral';

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

    if (recentValues.length === 0 || previousValues.length === 0) return 'neutral';

    const recentAvg = recentValues.reduce((a, b) => a + b, 0) / recentValues.length;
    const previousAvg = previousValues.reduce((a, b) => a + b, 0) / previousValues.length;

    const diff = ((recentAvg - previousAvg) / previousAvg) * 100;

    if (Math.abs(diff) < 5) return 'neutral';
    return diff > 0 ? 'up' : 'down';
  })();

  function formatValue(val: number): string {
    if (metric.value_type === 'boolean') {
      return val === 1 ? 'Yes' : 'No';
    }
    return val.toFixed(2);
  }
</script>

<Card>
  <div class="statistics-panel">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">{metric.name_key}</h3>

    {#if count === 0}
      <p class="text-gray-500">No data available</p>
    {:else}
      <div class="grid grid-cols-2 gap-4">
        <div class="stat-item">
          <span class="stat-label">Count</span>
          <span class="stat-value">{count}</span>
        </div>

        <div class="stat-item">
          <span class="stat-label">Mean</span>
          <span class="stat-value">{formatValue(mean)}</span>
        </div>

        <div class="stat-item">
          <span class="stat-label">Median</span>
          <span class="stat-value">{formatValue(median)}</span>
        </div>

        <div class="stat-item">
          <span class="stat-label">Std Dev</span>
          <span class="stat-value">{stdDev.toFixed(2)}</span>
        </div>

        {#if metric.value_type !== 'boolean'}
          <div class="stat-item">
            <span class="stat-label">Min</span>
            <span class="stat-value">{formatValue(min)}</span>
          </div>

          <div class="stat-item">
            <span class="stat-label">Max</span>
            <span class="stat-value">{formatValue(max)}</span>
          </div>
        {/if}

        <div class="stat-item col-span-2">
          <span class="stat-label">7-Day Trend</span>
          <span
            class="stat-value flex items-center"
            class:text-green-600={trend === 'up'}
            class:text-red-600={trend === 'down'}
            class:text-gray-600={trend === 'neutral'}
          >
            {#if trend === 'up'}
              ↑ Increasing
            {:else if trend === 'down'}
              ↓ Decreasing
            {:else}
              → Stable
            {/if}
          </span>
        </div>
      </div>
    {/if}
  </div>
</Card>

<style>
  .statistics-panel {
    padding: 1rem;
  }

  .stat-item {
    display: flex;
    flex-direction: column;
  }

  .stat-label {
    font-size: 0.875rem;
    color: #6b7280;
    margin-bottom: 0.25rem;
  }

  .stat-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
  }
</style>
