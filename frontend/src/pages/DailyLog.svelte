<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import { metricsStore, metricsActions, activeMetrics, metricsByCategory } from '../stores/metrics';
  import { entriesActions } from '../stores/entries';
  import { t } from '../i18n';
  import AuthenticatedLayout from '../components/AuthenticatedLayout.svelte';
  import Button from '../components/Button.svelte';
  import Card from '../components/Card.svelte';
  import Loading from '../components/Loading.svelte';
  import Input from '../components/Input.svelte';
  import { Calendar, CheckCircle2, Plus, Minus, StickyNote } from 'lucide-svelte';

  let selectedDate = new Date().toISOString().split('T')[0];
  let notes = '';
  let metricValues: Record<number, any> = {};
  let loading = false;
  let saving = false;
  let existingEntry: any = null;
  let activeRangeTooltip: number | null = null;

  onMount(async () => {
    await metricsActions.load(false);
    await loadEntryForDate(selectedDate);
  });

  async function loadEntryForDate(date: string) {
    loading = true;
    const result = await entriesActions.getByDate(date);
    if (result.success && result.data) {
      existingEntry = result.data;
      notes = result.data.notes || '';
      metricValues = {};
      result.data.values.forEach((v: any) => {
        if (v.value_numeric !== null) {
          metricValues[v.metric_id] = Number(v.value_numeric);
        } else if (v.value_boolean !== null) {
          metricValues[v.metric_id] = v.value_boolean;
        } else if (v.value_text !== null) {
          metricValues[v.metric_id] = v.value_text;
        }
      });
    } else {
      existingEntry = null;
      notes = '';
      metricValues = {};
    }
    loading = false;
  }

  async function handleDateChange() {
    await loadEntryForDate(selectedDate);
  }

  async function handleSave() {
    saving = true;

    const values = Object.entries(metricValues)
      .filter(([_, value]) => value !== null && value !== undefined && value !== '')
      .map(([metricId, value]) => ({
        metric_id: Number(metricId),
        value: value
      }));

    if (values.length === 0) {
      alert('Please add at least one metric value');
      saving = false;
      return;
    }

    const data = {
      entry_date: selectedDate,
      notes: notes || undefined,
      values
    };

    let result;
    if (existingEntry) {
      result = await entriesActions.update(existingEntry.id, data);
    } else {
      result = await entriesActions.create(data);
    }

    saving = false;

    if (result.success) {
      alert($t('entries.completeEntry'));
      push('/dashboard');
    } else {
      alert('Error: ' + (result.error || 'Failed to save entry'));
    }
  }

  function getMetricValue(metricId: number, metric: any) {
    const value = metricValues[metricId];
    if (value === undefined || value === null) {
      if (metric.value_type === 'boolean') return false;
      if (metric.value_type === 'count' || metric.value_type === 'number') return 0;
      return '';
    }
    return value;
  }

  function setMetricValue(metricId: number, value: any) {
    metricValues = { ...metricValues, [metricId]: value };
  }

  $: completedCount = Object.keys(metricValues).filter(id => {
    const val = metricValues[Number(id)];
    return val !== null && val !== undefined && val !== '';
  }).length;

  $: totalCount = $activeMetrics.length;
  $: progress = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;
</script>

<AuthenticatedLayout maxWidth="lg">
  <!-- Minimal Header -->
  <div class="mb-12">
    <h1 class="text-2xl font-semibold text-gray-900 dark:text-white mb-1">
      {$t('entries.title')}
    </h1>
    <p class="text-sm text-gray-600 dark:text-gray-400">
      Log your daily metrics and track how you're feeling.
    </p>
  </div>

  <!-- Date and Progress Card -->
  <Card>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Date Picker -->
      <div>
        <label class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          <Calendar size={16} class="text-gray-400 dark:text-gray-500" />
          <span>{$t('entries.date')}</span>
        </label>
        <input
          type="date"
          bind:value={selectedDate}
          on:change={handleDateChange}
          class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-150"
        />
      </div>

      <!-- Progress Indicator -->
      <div class="flex flex-col justify-center">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Progress</span>
          <span class="text-sm font-semibold text-primary-600 dark:text-primary-500">{Math.round(progress)}%</span>
        </div>
        <div class="relative w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
          <div
            class="absolute top-0 left-0 h-full bg-primary-600 dark:bg-primary-500 rounded-full transition-all duration-300"
            style="width: {progress}%"
          ></div>
        </div>
        <div class="flex items-center gap-2 mt-2">
          <CheckCircle2 size={14} class="text-gray-400 dark:text-gray-500" />
          <span class="text-xs text-gray-600 dark:text-gray-400">{completedCount} of {totalCount} metrics</span>
        </div>
      </div>
    </div>
  </Card>

  {#if loading}
    <Loading />
  {:else if $activeMetrics.length === 0}
    <Card>
      <p class="text-center text-gray-500 dark:text-gray-400 py-8">
        No metrics yet. <a href="#/metrics" class="text-primary-600 hover:underline">Create your first metric</a>
      </p>
    </Card>
  {:else}
    <form on:submit|preventDefault={handleSave} class="space-y-6">
      {#each Object.entries($metricsByCategory) as [category, metrics]}
        <Card>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-6">
            {$t(`metrics.categories.${category}`)}
          </h2>

          <div class="space-y-6">
            {#each metrics as metric}
              <div class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                <label class="block mb-3">
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {metric.name_key}
                  </span>
                  {#if metric.description}
                    <span class="text-xs text-gray-600 dark:text-gray-400 mt-1 block">{metric.description}</span>
                  {/if}
                </label>

                {#if metric.value_type === 'range'}
                  <div class="space-y-2">
                    <input
                      type="range"
                      min={metric.min_value}
                      max={metric.max_value}
                      step="0.1"
                      value={getMetricValue(metric.id, metric)}
                      on:input={(e) => setMetricValue(metric.id, Number(e.currentTarget.value))}
                      class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <div class="flex justify-between items-center text-sm">
                      <span class="text-gray-600 dark:text-gray-400">{metric.min_value}</span>
                      <span class="text-lg font-semibold text-gray-900 dark:text-white">
                        {getMetricValue(metric.id, metric) || metric.min_value}
                      </span>
                      <span class="text-gray-600 dark:text-gray-400">{metric.max_value}</span>
                    </div>
                  </div>

                {:else if metric.value_type === 'number'}
                  <input
                    type="number"
                    step="0.01"
                    value={getMetricValue(metric.id, metric)}
                    on:input={(e) => setMetricValue(metric.id, Number(e.currentTarget.value))}
                    class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-150"
                  />

                {:else if metric.value_type === 'count'}
                  <div class="flex items-center justify-center gap-4">
                    <button
                      type="button"
                      on:click={() => setMetricValue(metric.id, Math.max(0, (getMetricValue(metric.id, metric) || 0) - 1))}
                      class="p-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors duration-150"
                    >
                      <Minus size={18} class="text-gray-600 dark:text-gray-400" />
                    </button>
                    <div class="min-w-[80px] text-center">
                      <span class="text-3xl font-semibold text-gray-900 dark:text-white">
                        {getMetricValue(metric.id, metric) || 0}
                      </span>
                    </div>
                    <button
                      type="button"
                      on:click={() => setMetricValue(metric.id, (getMetricValue(metric.id, metric) || 0) + 1)}
                      class="p-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-lg transition-colors duration-150"
                    >
                      <Plus size={18} class="text-gray-600 dark:text-gray-400" />
                    </button>
                  </div>

                {:else if metric.value_type === 'boolean'}
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={getMetricValue(metric.id, metric)}
                      on:change={(e) => setMetricValue(metric.id, e.currentTarget.checked)}
                      class="sr-only peer"
                    />
                    <div class="w-14 h-7 bg-gray-300 dark:bg-gray-600 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary-500 rounded-full peer peer-checked:after:translate-x-7 peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-primary-600 dark:peer-checked:bg-primary-500"></div>
                    <span class="ml-3 text-sm font-medium text-gray-900 dark:text-white">
                      {getMetricValue(metric.id, metric) ? 'Yes' : 'No'}
                    </span>
                  </label>

                {:else if metric.value_type === 'text'}
                  <textarea
                    value={getMetricValue(metric.id, metric)}
                    on:input={(e) => setMetricValue(metric.id, e.currentTarget.value)}
                    rows="4"
                    placeholder="Write your thoughts..."
                    class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white dark:placeholder:text-gray-500 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-150 resize-none"
                  ></textarea>
                {/if}
              </div>
            {/each}
          </div>
        </Card>
      {/each}

      <!-- Notes Section -->
      <Card>
        <div class="flex items-center gap-2 mb-4">
          <StickyNote size={16} class="text-gray-400 dark:text-gray-500" />
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{$t('entries.notes')}</h3>
        </div>
        <textarea
          bind:value={notes}
          placeholder={$t('entries.addNote')}
          rows="5"
          class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-500 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-150 resize-none"
        ></textarea>
      </Card>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-3">
        <Button type="button" variant="secondary" fullWidth={true} on:click={() => push('/dashboard')}>
          {$t('common.cancel')}
        </Button>
        <Button
          type="submit"
          variant="primary"
          fullWidth={true}
          disabled={saving || completedCount === 0}
        >
          {#if saving}
            <div class="flex items-center justify-center gap-2">
              <div class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
              <span>{$t('common.loading')}</span>
            </div>
          {:else}
            <div class="flex items-center justify-center gap-2">
              <CheckCircle2 size={16} />
              <span>{$t('entries.saveEntry')}</span>
            </div>
          {/if}
        </Button>
      </div>
    </form>
  {/if}
</AuthenticatedLayout>

