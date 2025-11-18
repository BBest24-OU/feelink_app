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

  let selectedDate = new Date().toISOString().split('T')[0];
  let notes = '';
  let metricValues: Record<number, any> = {};
  let loading = false;
  let saving = false;
  let existingEntry: any = null;

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
    metricValues[metricId] = value;
  }

  $: completedCount = Object.keys(metricValues).filter(id => {
    const val = metricValues[Number(id)];
    return val !== null && val !== undefined && val !== '';
  }).length;

  $: totalCount = $activeMetrics.length;
  $: progress = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;
</script>

<AuthenticatedLayout maxWidth="lg">
  <div class="mb-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-2">{$t('entries.title')}</h1>
    <p class="text-gray-600">Log your daily metrics and track how you're feeling.</p>

    <div class="flex items-center space-x-4 mb-4">
      <Input
        type="date"
        bind:value={selectedDate}
        on:change={handleDateChange}
        label={$t('entries.date')}
      />
      <div class="flex-1">
        <p class="text-sm text-gray-600 mb-1">Progress</p>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div class="bg-primary-600 h-2.5 rounded-full transition-all" style="width: {progress}%"></div>
        </div>
        <p class="text-xs text-gray-500 mt-1">{completedCount} / {totalCount} metrics</p>
      </div>
    </div>
  </div>

  {#if loading}
    <Loading />
  {:else if $activeMetrics.length === 0}
    <Card>
      <p class="text-center text-gray-500 py-8">
        No metrics yet. <a href="#/metrics" class="text-primary-600 hover:underline">Create your first metric</a>
      </p>
    </Card>
  {:else}
    <form on:submit|preventDefault={handleSave} class="space-y-6">
      {#each Object.entries($metricsByCategory) as [category, metrics]}
        <Card>
          <h2 class="text-xl font-semibold text-gray-700 mb-4">
            {$t(`metrics.categories.${category}`)}
          </h2>

          <div class="space-y-4">
            {#each metrics as metric}
              <div class="border-b border-gray-100 pb-4 last:border-0">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {metric.name_key}
                  {#if metric.description}
                    <span class="text-xs text-gray-500 block">{metric.description}</span>
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
                      class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                    <div class="flex justify-between text-sm text-gray-600">
                      <span>{metric.min_value}</span>
                      <span class="font-semibold text-primary-600">{getMetricValue(metric.id, metric) || metric.min_value}</span>
                      <span>{metric.max_value}</span>
                    </div>
                  </div>

                {:else if metric.value_type === 'number'}
                  <input
                    type="number"
                    step="0.01"
                    value={getMetricValue(metric.id, metric)}
                    on:input={(e) => setMetricValue(metric.id, Number(e.currentTarget.value))}
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />

                {:else if metric.value_type === 'count'}
                  <div class="flex items-center space-x-4">
                    <button
                      type="button"
                      on:click={() => setMetricValue(metric.id, Math.max(0, (getMetricValue(metric.id, metric) || 0) - 1))}
                      class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-bold"
                    >
                      -
                    </button>
                    <span class="text-2xl font-bold text-primary-600 min-w-[60px] text-center">
                      {getMetricValue(metric.id, metric) || 0}
                    </span>
                    <button
                      type="button"
                      on:click={() => setMetricValue(metric.id, (getMetricValue(metric.id, metric) || 0) + 1)}
                      class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-bold"
                    >
                      +
                    </button>
                  </div>

                {:else if metric.value_type === 'boolean'}
                  <label class="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={getMetricValue(metric.id, metric)}
                      on:change={(e) => setMetricValue(metric.id, e.currentTarget.checked)}
                      class="w-6 h-6 text-primary-600 rounded focus:ring-primary-500"
                    />
                    <span class="text-gray-700">{getMetricValue(metric.id, metric) ? 'Yes' : 'No'}</span>
                  </label>

                {:else if metric.value_type === 'text'}
                  <textarea
                    value={getMetricValue(metric.id, metric)}
                    on:input={(e) => setMetricValue(metric.id, e.currentTarget.value)}
                    rows="3"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  ></textarea>
                {/if}
              </div>
            {/each}
          </div>
        </Card>
      {/each}

      <Card>
        <h3 class="text-lg font-semibold text-gray-700 mb-3">{$t('entries.notes')}</h3>
        <textarea
          bind:value={notes}
          placeholder={$t('entries.addNote')}
          rows="4"
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        ></textarea>
      </Card>

      <div class="flex justify-end space-x-4">
        <Button type="button" variant="ghost" on:click={() => push('/dashboard')}>
          {$t('common.cancel')}
        </Button>
        <Button type="submit" variant="primary" disabled={saving || completedCount === 0}>
          {saving ? $t('common.loading') : $t('entries.saveEntry')}
        </Button>
    </div>
  </form>
  {/if}
</AuthenticatedLayout>
