<script lang="ts">
  import { onMount } from 'svelte';
  import { metricsActions, activeMetrics } from '../stores/metrics';
  import { entriesActions, entriesStore } from '../stores/entries';
  import { analyticsApi } from '../lib/api';
  import AuthenticatedLayout from '../components/AuthenticatedLayout.svelte';
  import Card from '../components/Card.svelte';
  import Button from '../components/Button.svelte';
  import CorrelationMatrix from '../components/CorrelationMatrix.svelte';
  import ScatterPlot from '../components/ScatterPlot.svelte';
  import { subDays, format } from 'date-fns';

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
  let scatterData: Array<{ x: number; y: number }> = [];

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
    return true; // weak includes all
  });

  function getInterpretation(corr: Correlation): string {
    let interpretation = '';

    if (corr.strength === 'strong') {
      interpretation = 'Strong ';
    } else if (corr.strength === 'moderate') {
      interpretation = 'Moderate ';
    } else {
      interpretation = 'Weak ';
    }

    interpretation += corr.direction + ' correlation ';
    interpretation += `(r=${corr.coefficient.toFixed(2)}, `;
    interpretation += corr.significant ? `p=${corr.p_value.toFixed(3)}` : 'not significant';
    interpretation += ') ';

    interpretation += `between ${corr.metric_1_name} and ${corr.metric_2_name}.`;

    if (corr.lag > 0) {
      interpretation += ` ${corr.metric_1_name} shows effects on ${corr.metric_2_name} after ${corr.lag} day${corr.lag > 1 ? 's' : ''}.`;
    }

    // Add plain-language meaning
    if (corr.direction === 'positive' && corr.significant) {
      interpretation += ` When ${corr.metric_1_name} increases, ${corr.metric_2_name} tends to increase.`;
    } else if (corr.direction === 'negative' && corr.significant) {
      interpretation += ` When ${corr.metric_1_name} increases, ${corr.metric_2_name} tends to decrease.`;
    }

    return interpretation;
  }

  async function selectCorrelation(corr: Correlation) {
    selectedCorrelation = corr;

    // Prepare scatter plot data
    const entries = $entriesStore.entries;
    const points: Array<{ x: number; y: number }> = [];

    for (const entry of entries) {
      const value1 = entry.values.find((v) => v.metric_id === corr.metric_1_id);
      const value2 = entry.values.find((v) => v.metric_id === corr.metric_2_id);

      if (value1 && value2) {
        const x = value1.value_numeric ?? (value1.value_boolean ? 1 : 0);
        const y = value2.value_numeric ?? (value2.value_boolean ? 1 : 0);

        if (x !== null && y !== null) {
          points.push({ x, y });
        }
      }
    }

    scatterData = points;
  }

  function getStrengthColor(strength: string): string {
    if (strength === 'strong') return 'text-green-600';
    if (strength === 'moderate') return 'text-yellow-600';
    return 'text-gray-500';
  }
</script>

<AuthenticatedLayout>
  <div class="mb-6">
    <h1 class="text-3xl font-bold text-gray-800">Correlations Analysis</h1>
    <p class="text-gray-600 mt-2">Discover meaningful relationships between your tracked metrics.</p>
  </div>

    <!-- Controls -->
    <Card>
      <h2 class="text-xl font-bold text-gray-800 mb-4">Analysis Settings</h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Date Range</label>
          <select
            bind:value={dateRange}
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="all">All time</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Algorithm</label>
          <select
            bind:value={algorithm}
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option value="pearson">Pearson (linear)</option>
            <option value="spearman">Spearman (rank)</option>
            <option value="kendall">Kendall (rank)</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Maximum Lag (days)</label>
          <input
            type="number"
            bind:value={maxLag}
            min="0"
            max="30"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      <div class="flex flex-wrap gap-4 mb-4">
        <label class="flex items-center">
          <input type="checkbox" bind:checked={onlySignificant} class="mr-2" />
          <span class="text-sm text-gray-700">Only statistically significant (p &lt; 0.05)</span>
        </label>

        <div class="flex items-center gap-2">
          <span class="text-sm font-medium text-gray-700">Minimum strength:</span>
          <select
            bind:value={minStrength}
            class="px-3 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-primary-500"
          >
            <option value="all">All</option>
            <option value="weak">Weak+</option>
            <option value="moderate">Moderate+</option>
            <option value="strong">Strong only</option>
          </select>
        </div>
      </div>

      <Button on:click={loadCorrelations} disabled={loading}>
        {loading ? 'Analyzing...' : 'Run Analysis'}
      </Button>
    </Card>

    {#if error}
      <Card>
        <div class="text-red-600 p-4">
          {error}
        </div>
      </Card>
    {/if}

    {#if loading}
      <div class="text-center py-12">
        <div class="inline-block animate-spin w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full"></div>
        <p class="mt-4 text-gray-600">Analyzing correlations...</p>
      </div>
    {:else if filteredCorrelations.length === 0 && !error}
      <Card>
        <div class="text-center py-12">
          <p class="text-gray-600 mb-4">
            No correlations found. Try adjusting your filters or logging more data.
          </p>
          <p class="text-sm text-gray-500">
            Minimum 7 data points required per metric for correlation analysis.
          </p>
        </div>
      </Card>
    {:else}
      <!-- Correlation Matrix -->
      <div class="mt-6">
        <Card>
          <h2 class="text-xl font-bold text-gray-800 mb-4">Correlation Matrix</h2>
          <CorrelationMatrix correlations={filteredCorrelations} />
        </Card>
      </div>

      <!-- Correlations List -->
      <div class="mt-6">
        <Card>
          <h2 class="text-xl font-bold text-gray-800 mb-4">
            Correlations ({filteredCorrelations.length})
          </h2>

          <div class="space-y-4">
            {#each filteredCorrelations as corr}
              <div
                class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                on:click={() => selectCorrelation(corr)}
                class:bg-blue-50={selectedCorrelation === corr}
                class:border-blue-300={selectedCorrelation === corr}
              >
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <h3 class="font-semibold text-gray-800">
                      {corr.metric_1_name} ↔ {corr.metric_2_name}
                    </h3>
                    {#if corr.lag > 0}
                      <span class="text-xs text-orange-600 font-medium">
                        {corr.lag}-day lag effect
                      </span>
                    {/if}
                  </div>

                  <div class="text-right">
                    <div class="text-2xl font-bold {corr.direction === 'positive' ? 'text-blue-600' : 'text-red-600'}">
                      {corr.coefficient.toFixed(2)}
                    </div>
                    <div class="text-xs {getStrengthColor(corr.strength)}">
                      {corr.strength}
                    </div>
                  </div>
                </div>

                <p class="text-sm text-gray-700 mb-2">
                  {getInterpretation(corr)}
                </p>

                <div class="flex gap-4 text-xs text-gray-500">
                  <span>p-value: {corr.p_value.toFixed(4)}</span>
                  <span>n = {corr.sample_size}</span>
                  <span>{corr.algorithm}</span>
                  {#if !corr.significant}
                    <span class="text-yellow-600">⚠ Not significant</span>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
        </Card>
      </div>

      <!-- Scatter Plot -->
      {#if selectedCorrelation && scatterData.length > 0}
        <div class="mt-6">
          <Card>
            <h2 class="text-xl font-bold text-gray-800 mb-4">Scatter Plot</h2>
            <ScatterPlot
              title="{selectedCorrelation.metric_1_name} vs {selectedCorrelation.metric_2_name}"
              xLabel={selectedCorrelation.metric_1_name}
              yLabel={selectedCorrelation.metric_2_name}
              data={scatterData}
              coefficient={selectedCorrelation.coefficient}
              height={400}
            />
          </Card>
        </div>
      {/if}
    {/if}

    <!-- Information Box -->
    <div class="mt-6">
      <Card>
        <h3 class="font-semibold text-gray-800 mb-2">About Correlation Analysis</h3>
        <div class="text-sm text-gray-600 space-y-2">
          <p>
            <strong>Correlation</strong> measures the statistical relationship between two metrics.
            Values range from -1 (perfect negative) to +1 (perfect positive).
          </p>
          <p>
            <strong>Important:</strong> Correlation does not imply causation. A strong correlation
            means two metrics tend to change together, but one doesn't necessarily cause the other.
          </p>
          <p>
            <strong>Lag correlation</strong> detects delayed effects (e.g., sleep today affecting
            mood tomorrow).
          </p>
          <p>
            <strong>Statistical significance</strong> (p &lt; 0.05) indicates the correlation is
            unlikely to be due to random chance.
          </p>
      </div>
    </Card>
  </div>
</AuthenticatedLayout>
