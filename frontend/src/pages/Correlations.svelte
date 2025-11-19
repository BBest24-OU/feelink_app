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
  import { TrendingUp, TrendingDown, Minus as MinusIcon, Sparkles, Settings, Info, BarChart3, Clock, AlertTriangle } from 'lucide-svelte';

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
  <!-- Enhanced Header -->
  <div class="mb-8 animate-slide-down">
    <div class="flex items-center gap-3 mb-3">
      <div class="p-3 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl shadow-glow">
        <BarChart3 class="text-white" size={28} />
      </div>
      <div>
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800">Correlations Analysis</h1>
        <p class="text-gray-600 mt-1 text-lg">Discover meaningful relationships between your tracked metrics.</p>
      </div>
    </div>
  </div>

  <!-- Controls -->
  <Card gradient={true}>
    <div class="flex items-center gap-3 mb-6">
      <Settings size={24} class="text-primary-600" />
      <h2 class="text-xl md:text-2xl font-bold text-gray-800">Analysis Settings</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-3">Date Range</label>
        <select
          bind:value={dateRange}
          class="w-full px-5 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 text-base font-medium"
        >
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
          <option value="all">All time</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-3">Algorithm</label>
        <select
          bind:value={algorithm}
          class="w-full px-5 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 text-base font-medium"
        >
          <option value="pearson">Pearson (linear)</option>
          <option value="spearman">Spearman (rank)</option>
          <option value="kendall">Kendall (rank)</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-3">Maximum Lag (days)</label>
        <input
          type="number"
          bind:value={maxLag}
          min="0"
          max="30"
          class="w-full px-5 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 text-base font-semibold"
        />
      </div>
    </div>

    <div class="flex flex-wrap gap-6 mb-6 p-4 bg-gray-50 rounded-xl">
      <label class="flex items-center cursor-pointer group">
        <input type="checkbox" bind:checked={onlySignificant} class="w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500 mr-3" />
        <span class="text-sm font-medium text-gray-700 group-hover:text-gray-900 transition-colors">Only statistically significant (p &lt; 0.05)</span>
      </label>

      <div class="flex items-center gap-3">
        <span class="text-sm font-semibold text-gray-700">Minimum strength:</span>
        <select
          bind:value={minStrength}
          class="px-4 py-2 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 font-medium"
        >
          <option value="all">All</option>
          <option value="weak">Weak+</option>
          <option value="moderate">Moderate+</option>
          <option value="strong">Strong only</option>
        </select>
      </div>
    </div>

    <Button on:click={loadCorrelations} disabled={loading} variant="gradient" size="lg">
      {#if loading}
        <div class="flex items-center gap-2">
          <div class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></div>
          <span>Analyzing...</span>
        </div>
      {:else}
        <div class="flex items-center gap-2">
          <Sparkles size={20} />
          <span>Run Analysis</span>
        </div>
      {/if}
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
        <Card gradient={false}>
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-3">
              <TrendingUp size={24} class="text-primary-600" />
              <h2 class="text-xl md:text-2xl font-bold text-gray-800">
                Found {filteredCorrelations.length} Correlation{filteredCorrelations.length !== 1 ? 's' : ''}
              </h2>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-4">
            {#each filteredCorrelations as corr, index}
              <div
                on:click={() => selectCorrelation(corr)}
                class="group relative overflow-hidden p-5 md:p-6 border-2 rounded-2xl cursor-pointer transition-all duration-300 hover:shadow-medium hover:-translate-y-0.5 animate-fade-in"
                style="animation-delay: {index * 0.05}s; background-color: {selectedCorrelation === corr ? 'rgba(239, 246, 255, 0.5)' : 'white'};"
                class:border-blue-300={selectedCorrelation === corr}
                class:border-gray-200={selectedCorrelation !== corr}
                class:hover:border-primary-300={selectedCorrelation !== corr}
              >
                <!-- Correlation Strength Indicator -->
                <div class="absolute top-0 left-0 w-2 h-full rounded-l-2xl"
                  class:bg-green-500={corr.strength === 'strong'}
                  class:bg-yellow-500={corr.strength === 'moderate'}
                  class:bg-gray-400={corr.strength === 'weak'}
                ></div>

                <div class="ml-4">
                  <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-4 mb-4">
                    <div class="flex-1">
                      <h3 class="text-lg md:text-xl font-bold text-gray-800 mb-2 flex items-center gap-2">
                        <span>{corr.metric_1_name}</span>
                        {#if corr.direction === 'positive'}
                          <TrendingUp size={20} class="text-blue-600" />
                        {:else if corr.direction === 'negative'}
                          <TrendingDown size={20} class="text-red-600" />
                        {:else}
                          <MinusIcon size={20} class="text-gray-500" />
                        {/if}
                        <span>{corr.metric_2_name}</span>
                      </h3>
                      {#if corr.lag > 0}
                        <span class="inline-flex items-center gap-1 px-3 py-1 bg-orange-100 text-orange-700 text-xs font-bold rounded-full">
                          <Clock size={14} />
                          <span>{corr.lag}-day lag effect</span>
                        </span>
                      {/if}
                    </div>

                    <div class="flex flex-row md:flex-col gap-3 md:gap-2 items-center md:items-end">
                      <div class="text-center">
                        <div class="text-3xl md:text-4xl font-bold"
                          class:text-blue-600={corr.direction === 'positive'}
                          class:text-red-600={corr.direction === 'negative'}
                          class:text-gray-500={corr.direction === 'none'}
                        >
                          {corr.coefficient.toFixed(2)}
                        </div>
                      </div>
                      <div class="px-3 py-1 rounded-full text-xs font-bold"
                        class:bg-green-100={corr.strength === 'strong'}
                        class:text-green-700={corr.strength === 'strong'}
                        class:bg-yellow-100={corr.strength === 'moderate'}
                        class:text-yellow-700={corr.strength === 'moderate'}
                        class:bg-gray-100={corr.strength === 'weak'}
                        class:text-gray-700={corr.strength === 'weak'}
                      >
                        {corr.strength.toUpperCase()}
                      </div>
                    </div>
                  </div>

                  <p class="text-sm md:text-base text-gray-700 mb-3 leading-relaxed">
                    {getInterpretation(corr)}
                  </p>

                  <div class="flex flex-wrap gap-3 text-xs font-medium">
                    <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg">
                      p-value: {corr.p_value.toFixed(4)}
                    </span>
                    <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg">
                      n = {corr.sample_size}
                    </span>
                    <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg">
                      {corr.algorithm}
                    </span>
                    {#if !corr.significant}
                      <span class="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-lg flex items-center gap-1">
                        <AlertTriangle size={14} />
                        <span>Not significant</span>
                      </span>
                    {/if}
                  </div>
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
      <Card gradient={true}>
        <div class="flex items-center gap-3 mb-4">
          <div class="p-2 bg-blue-500 rounded-xl">
            <Info size={20} class="text-white" />
          </div>
          <h3 class="text-lg md:text-xl font-bold text-gray-800">About Correlation Analysis</h3>
        </div>
        <div class="text-sm md:text-base text-gray-700 space-y-3 leading-relaxed">
          <p>
            <strong class="text-gray-900">Correlation</strong> measures the statistical relationship between two metrics.
            Values range from -1 (perfect negative) to +1 (perfect positive).
          </p>
          <p class="p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
            <strong class="text-yellow-900">Important:</strong> Correlation does not imply causation. A strong correlation
            means two metrics tend to change together, but one doesn't necessarily cause the other.
          </p>
          <p>
            <strong class="text-gray-900">Lag correlation</strong> detects delayed effects (e.g., sleep today affecting
            mood tomorrow).
          </p>
          <p>
            <strong class="text-gray-900">Statistical significance</strong> (p &lt; 0.05) indicates the correlation is
            unlikely to be due to random chance.
          </p>
        </div>
      </Card>
    </div>
</AuthenticatedLayout>
