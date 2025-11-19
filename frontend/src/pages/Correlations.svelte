<script lang="ts">
  import { onMount } from 'svelte';
  import { metricsActions, activeMetrics } from '../stores/metrics';
  import { entriesActions, entriesStore } from '../stores/entries';
  import { analyticsApi } from '../lib/api';
  import AuthenticatedLayout from '../components/AuthenticatedLayout.svelte';
  import Card from '../components/Card.svelte';
  import Button from '../components/Button.svelte';
  import EChart from '../components/EChart.svelte';
  import type { EChartsOption } from 'echarts';
  import { subDays, format } from 'date-fns';
  import { TrendingUp, TrendingDown, Minus as MinusIcon } from 'lucide-svelte';

  interface Correlation {
    metric_1_id: number;
    metric_1_name: string;
    metric_2_id: number;
    metric_2_name: string;
    coefficient: number;
    p_value: number;
    lag: number;
    strength: string;
    significant: boolean;
    direction: string;
    sample_size: number;
    algorithm: string;
  }

  let correlations: Correlation[] = [];
  let loading = false;
  let error = '';

  // Filters
  let dateRange: '30d' | '90d' | 'all' = '30d';
  let algorithm: 'pearson' | 'spearman' | 'kendall' = 'pearson';
  let onlySignificant = true;
  let maxLag = 7;
  let minStrength: 'all' | 'weak' | 'moderate' | 'strong' = 'all';

  // Selected correlation for scatter plot
  let selectedCorrelation: Correlation | null = null;
  let scatterChartOption: EChartsOption | null = null;

  onMount(async () => {
    await metricsActions.load(false);
    await entriesActions.load();
    await loadCorrelations();
  });

  async function loadCorrelations() {
    loading = true;
    error = '';

    try {
      const params: any = {
        algorithm,
        max_lag: maxLag,
        only_significant: onlySignificant,
      };

      if (dateRange !== 'all') {
        const days = dateRange === '30d' ? 30 : 90;
        params.date_from = format(subDays(new Date(), days), 'yyyy-MM-dd');
        params.date_to = format(new Date(), 'yyyy-MM-dd');
      }

      const response = await analyticsApi.getCorrelations(params);
      correlations = response.data.correlations;
    } catch (err: any) {
      error = err.response?.data?.detail || 'Failed to load correlations';
      correlations = [];
    } finally {
      loading = false;
    }
  }

  // Filter correlations by strength
  $: filteredCorrelations = correlations.filter((corr) => {
    if (minStrength === 'all') return true;
    if (minStrength === 'strong') return corr.strength === 'strong';
    if (minStrength === 'moderate') return ['moderate', 'strong'].includes(corr.strength);
    return true;
  });

  function getInterpretation(corr: Correlation): string {
    let parts: string[] = [];

    if (corr.direction === 'positive' && corr.significant) {
      parts.push(`When ${corr.metric_1_name} increases, ${corr.metric_2_name} tends to increase.`);
    } else if (corr.direction === 'negative' && corr.significant) {
      parts.push(`When ${corr.metric_1_name} increases, ${corr.metric_2_name} tends to decrease.`);
    }

    if (corr.lag > 0) {
      parts.push(`Effects appear after ${corr.lag} day${corr.lag > 1 ? 's' : ''}.`);
    }

    return parts.join(' ');
  }

  async function selectCorrelation(corr: Correlation) {
    selectedCorrelation = corr;

    // Prepare scatter plot data for ECharts
    const entries = $entriesStore.entries;
    const points: [number, number][] = [];

    for (const entry of entries) {
      const value1 = entry.values.find((v) => v.metric_id === corr.metric_1_id);
      const value2 = entry.values.find((v) => v.metric_id === corr.metric_2_id);

      if (value1 && value2) {
        const x = value1.value_numeric ?? (value1.value_boolean ? 1 : 0);
        const y = value2.value_numeric ?? (value2.value_boolean ? 1 : 0);

        if (x !== null && y !== null) {
          points.push([x, y]);
        }
      }
    }

    // Create ECharts option
    scatterChartOption = {
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%',
        top: '10%',
      },
      xAxis: {
        name: corr.metric_1_name,
        nameLocation: 'middle',
        nameGap: 30,
        type: 'value',
      },
      yAxis: {
        name: corr.metric_2_name,
        nameLocation: 'middle',
        nameGap: 40,
        type: 'value',
      },
      series: [
        {
          type: 'scatter',
          data: points,
          symbolSize: 8,
          itemStyle: {
            color: '#3b82f6',
            opacity: 0.6,
          },
        },
      ],
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          return `${corr.metric_1_name}: ${params.value[0]}<br/>${corr.metric_2_name}: ${params.value[1]}`;
        },
      },
    };
  }
</script>

<AuthenticatedLayout>
  <!-- Minimal Header -->
  <div class="mb-12">
    <h1 class="text-2xl font-semibold text-gray-900 dark:text-white mb-1">
      Correlations Analysis
    </h1>
    <p class="text-sm text-gray-600 dark:text-gray-400">
      Discover meaningful relationships between your tracked metrics.
    </p>
  </div>

  <!-- Analysis Settings -->
  <Card>
    <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
      Analysis Settings
    </h2>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Date Range
        </label>
        <select
          bind:value={dateRange}
          class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:text-white"
        >
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
          <option value="all">All time</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Algorithm
        </label>
        <select
          bind:value={algorithm}
          class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:text-white"
        >
          <option value="pearson">Pearson (linear)</option>
          <option value="spearman">Spearman (rank)</option>
          <option value="kendall">Kendall (rank)</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Maximum Lag (days)
        </label>
        <input
          type="number"
          bind:value={maxLag}
          min="0"
          max="30"
          class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:text-white"
        />
      </div>
    </div>

    <div class="flex flex-wrap gap-4 items-center mb-6">
      <label class="flex items-center cursor-pointer">
        <input type="checkbox" bind:checked={onlySignificant} class="w-4 h-4 text-primary-600 rounded focus:ring-2 focus:ring-primary-500 mr-2" />
        <span class="text-sm text-gray-700 dark:text-gray-300">Only significant (p &lt; 0.05)</span>
      </label>

      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-700 dark:text-gray-300">Minimum strength:</span>
        <select
          bind:value={minStrength}
          class="px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:text-white"
        >
          <option value="all">All</option>
          <option value="weak">Weak+</option>
          <option value="moderate">Moderate+</option>
          <option value="strong">Strong only</option>
        </select>
      </div>
    </div>

    <Button on:click={loadCorrelations} disabled={loading} variant="primary">
      {loading ? 'Analyzing...' : 'Run Analysis'}
    </Button>
  </Card>

  {#if error}
    <Card>
      <p class="text-sm text-red-600 dark:text-red-400">{error}</p>
    </Card>
  {/if}

  {#if loading}
    <div class="text-center py-12">
      <div class="inline-block animate-spin w-8 h-8 border-2 border-primary-600 border-t-transparent rounded-full"></div>
      <p class="mt-4 text-sm text-gray-600 dark:text-gray-400">Analyzing correlations...</p>
    </div>
  {:else if filteredCorrelations.length === 0 && !error}
    <Card>
      <div class="text-center py-12">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
          No correlations found. Try adjusting your filters or logging more data.
        </p>
        <p class="text-xs text-gray-500 dark:text-gray-500">
          Minimum 7 data points required per metric.
        </p>
      </div>
    </Card>
  {:else}
    <!-- Correlations List -->
    <Card>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
        {filteredCorrelations.length} Correlation{filteredCorrelations.length !== 1 ? 's' : ''} Found
      </h2>

      <div class="space-y-3">
        {#each filteredCorrelations as corr}
          <div
            on:click={() => selectCorrelation(corr)}
            class="p-4 border rounded-lg cursor-pointer transition-colors"
            class:border-primary-500={selectedCorrelation === corr}
            class:dark:border-primary-400={selectedCorrelation === corr}
            class:border-gray-200={selectedCorrelation !== corr}
            class:dark:border-gray-700={selectedCorrelation !== corr}
            class:hover:border-gray-300={selectedCorrelation !== corr}
            class:dark:hover:border-gray-600={selectedCorrelation !== corr}
          >
            <div class="flex justify-between items-start mb-3">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {corr.metric_1_name}
                  </span>
                  {#if corr.direction === 'positive'}
                    <TrendingUp size={14} class="text-gray-500 dark:text-gray-400" />
                  {:else if corr.direction === 'negative'}
                    <TrendingDown size={14} class="text-gray-500 dark:text-gray-400" />
                  {:else}
                    <MinusIcon size={14} class="text-gray-500 dark:text-gray-400" />
                  {/if}
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {corr.metric_2_name}
                  </span>
                </div>
                {#if getInterpretation(corr)}
                  <p class="text-xs text-gray-600 dark:text-gray-400">
                    {getInterpretation(corr)}
                  </p>
                {/if}
              </div>

              <div class="text-right">
                <div class="text-lg font-semibold text-gray-900 dark:text-white">
                  {corr.coefficient.toFixed(2)}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-500">
                  {corr.strength}
                </div>
              </div>
            </div>

            <div class="flex flex-wrap gap-2 text-xs">
              <span class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">
                p={corr.p_value.toFixed(4)}
              </span>
              <span class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">
                n={corr.sample_size}
              </span>
              {#if corr.lag > 0}
                <span class="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">
                  {corr.lag}d lag
                </span>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    </Card>

    <!-- Scatter Plot with ECharts -->
    {#if selectedCorrelation && scatterChartOption}
      <Card>
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
          {selectedCorrelation.metric_1_name} vs {selectedCorrelation.metric_2_name}
        </h2>
        <EChart option={scatterChartOption} height="400px" />
      </Card>
    {/if}

    <!-- Information -->
    <Card>
      <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">
        About Correlation Analysis
      </h3>
      <div class="text-xs text-gray-600 dark:text-gray-400 space-y-2">
        <p>
          Correlation measures the statistical relationship between two metrics.
          Values range from -1 (perfect negative) to +1 (perfect positive).
        </p>
        <p class="py-2 px-3 bg-gray-50 dark:bg-gray-800 rounded border-l-2 border-gray-300 dark:border-gray-600">
          <strong>Important:</strong> Correlation does not imply causation.
        </p>
      </div>
    </Card>
  {/if}
</AuthenticatedLayout>
