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
  import { Calendar, CheckCircle2, Circle, Plus, Minus, StickyNote, Sparkles } from 'lucide-svelte';

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
  <!-- Enhanced Header with Gradient -->
  <div class="mb-8 animate-slide-down">
    <div class="flex items-center gap-3 mb-3">
      <div class="p-3 bg-gradient-primary rounded-2xl shadow-glow">
        <Sparkles class="text-white" size={28} />
      </div>
      <div>
        <h1 class="text-3xl md:text-4xl font-bold text-gray-800">{$t('entries.title')}</h1>
        <p class="text-gray-600 mt-1">Log your daily metrics and track how you're feeling.</p>
      </div>
    </div>

    <!-- Date and Progress Card -->
    <Card gradient={true} padding="md">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Date Picker -->
        <div>
          <label class="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-3">
            <Calendar size={18} class="text-primary-600" />
            <span>{$t('entries.date')}</span>
          </label>
          <input
            type="date"
            bind:value={selectedDate}
            on:change={handleDateChange}
            class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 text-lg font-medium"
          />
        </div>

        <!-- Progress Indicator -->
        <div class="flex flex-col justify-center">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-semibold text-gray-700">Your Progress</span>
            <span class="text-sm font-bold text-primary-600">{Math.round(progress)}%</span>
          </div>
          <div class="relative w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              class="absolute top-0 left-0 h-full bg-gradient-primary rounded-full transition-all duration-500 ease-out shadow-glow"
              style="width: {progress}%"
            ></div>
          </div>
          <div class="flex items-center gap-2 mt-2">
            <CheckCircle2 size={16} class="text-green-600" />
            <span class="text-xs text-gray-600">{completedCount} of {totalCount} metrics completed</span>
          </div>
        </div>
      </div>
    </Card>
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
      {#each Object.entries($metricsByCategory) as [category, metrics], categoryIndex}
        <Card gradient={categoryIndex % 2 === 0} animate={true}>
          <div class="flex items-center gap-3 mb-6">
            <div class="h-1 w-12 bg-gradient-primary rounded-full"></div>
            <h2 class="text-xl md:text-2xl font-bold text-gray-800">
              {$t(`metrics.categories.${category}`)}
            </h2>
          </div>

          <div class="grid grid-cols-1 gap-6">
            {#each metrics as metric}
              <div class="group p-4 md:p-5 bg-gray-50/50 hover:bg-gray-50 rounded-xl border-2 border-transparent hover:border-primary-200 transition-all duration-300">
                <label class="block mb-4">
                  <span class="text-base md:text-lg font-semibold text-gray-800 flex items-center gap-2">
                    <Circle size={8} class="text-primary-600 fill-primary-600" />
                    {metric.name_key}
                  </span>
                  {#if metric.description}
                    <span class="text-sm text-gray-500 mt-1 block ml-4">{metric.description}</span>
                  {/if}
                </label>

                {#if metric.value_type === 'range'}
                  <!-- Enhanced Range Slider -->
                  <div class="space-y-3">
                    <div class="relative">
                      <input
                        type="range"
                        min={metric.min_value}
                        max={metric.max_value}
                        step="0.1"
                        value={getMetricValue(metric.id, metric)}
                        on:input={(e) => {
                          setMetricValue(metric.id, Number(e.currentTarget.value));
                          activeRangeTooltip = metric.id;
                        }}
                        on:mouseenter={() => activeRangeTooltip = metric.id}
                        on:mouseleave={() => activeRangeTooltip = null}
                        class="w-full h-3 bg-gradient-to-r from-gray-200 via-primary-300 to-primary-600 rounded-full appearance-none cursor-pointer slider-thumb"
                        style="
                          background: linear-gradient(to right,
                            #e5e7eb 0%,
                            #a5b4fc {((getMetricValue(metric.id, metric) - metric.min_value) / (metric.max_value - metric.min_value)) * 50}%,
                            #4f46e5 {((getMetricValue(metric.id, metric) - metric.min_value) / (metric.max_value - metric.min_value)) * 100}%,
                            #e5e7eb {((getMetricValue(metric.id, metric) - metric.min_value) / (metric.max_value - metric.min_value)) * 100}%
                          );
                        "
                      />
                      {#if activeRangeTooltip === metric.id}
                        <div class="absolute -top-12 left-1/2 transform -translate-x-1/2 px-3 py-2 bg-gray-900 text-white text-sm font-bold rounded-lg shadow-lg animate-scale-in">
                          {getMetricValue(metric.id, metric) || metric.min_value}
                          <div class="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-gray-900 rotate-45"></div>
                        </div>
                      {/if}
                    </div>
                    <div class="flex justify-between items-center text-sm">
                      <span class="text-gray-500 font-medium">{metric.min_value}</span>
                      <span class="text-xl font-bold text-primary-600 px-4 py-1 bg-primary-50 rounded-lg">
                        {getMetricValue(metric.id, metric) || metric.min_value}
                      </span>
                      <span class="text-gray-500 font-medium">{metric.max_value}</span>
                    </div>
                  </div>

                {:else if metric.value_type === 'number'}
                  <input
                    type="number"
                    step="0.01"
                    value={getMetricValue(metric.id, metric)}
                    on:input={(e) => setMetricValue(metric.id, Number(e.currentTarget.value))}
                    class="w-full px-5 py-3 text-lg font-semibold border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200"
                  />

                {:else if metric.value_type === 'count'}
                  <!-- Enhanced Counter -->
                  <div class="flex items-center justify-center gap-4 md:gap-6">
                    <button
                      type="button"
                      on:click={() => setMetricValue(metric.id, Math.max(0, (getMetricValue(metric.id, metric) || 0) - 1))}
                      class="group/btn p-4 md:p-5 bg-gradient-to-br from-red-50 to-red-100 hover:from-red-100 hover:to-red-200 rounded-2xl shadow-soft hover:shadow-medium active:scale-95 transition-all duration-200"
                    >
                      <Minus size={24} class="text-red-600 group-hover/btn:scale-110 transition-transform" />
                    </button>
                    <div class="min-w-[100px] md:min-w-[120px] text-center">
                      <span class="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-primary">
                        {getMetricValue(metric.id, metric) || 0}
                      </span>
                    </div>
                    <button
                      type="button"
                      on:click={() => setMetricValue(metric.id, (getMetricValue(metric.id, metric) || 0) + 1)}
                      class="group/btn p-4 md:p-5 bg-gradient-to-br from-green-50 to-green-100 hover:from-green-100 hover:to-green-200 rounded-2xl shadow-soft hover:shadow-medium active:scale-95 transition-all duration-200"
                    >
                      <Plus size={24} class="text-green-600 group-hover/btn:scale-110 transition-transform" />
                    </button>
                  </div>

                {:else if metric.value_type === 'boolean'}
                  <!-- Toggle Switch -->
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={getMetricValue(metric.id, metric)}
                      on:change={(e) => setMetricValue(metric.id, e.currentTarget.checked)}
                      class="sr-only peer"
                    />
                    <div class="w-16 h-8 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-8 peer-checked:after:border-white after:content-[''] after:absolute after:top-1 after:left-1 after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-gradient-primary shadow-soft"></div>
                    <span class="ml-4 text-lg font-semibold" class:text-primary-600={getMetricValue(metric.id, metric)} class:text-gray-500={!getMetricValue(metric.id, metric)}>
                      {getMetricValue(metric.id, metric) ? 'Yes' : 'No'}
                    </span>
                  </label>

                {:else if metric.value_type === 'text'}
                  <textarea
                    value={getMetricValue(metric.id, metric)}
                    on:input={(e) => setMetricValue(metric.id, e.currentTarget.value)}
                    rows="4"
                    placeholder="Write your thoughts..."
                    class="w-full px-5 py-4 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 resize-none text-base"
                  ></textarea>
                {/if}
              </div>
            {/each}
          </div>
        </Card>
      {/each}

      <!-- Enhanced Notes Section -->
      <Card gradient={true}>
        <div class="flex items-center gap-3 mb-4">
          <StickyNote size={24} class="text-primary-600" />
          <h3 class="text-xl font-bold text-gray-800">{$t('entries.notes')}</h3>
        </div>
        <textarea
          bind:value={notes}
          placeholder={$t('entries.addNote')}
          rows="5"
          class="w-full px-5 py-4 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 resize-none text-base placeholder:text-gray-400"
        ></textarea>
      </Card>

      <!-- Action Buttons -->
      <div class="sticky bottom-4 flex flex-col sm:flex-row gap-3 sm:gap-4 p-6 bg-white/90 backdrop-blur-lg rounded-2xl shadow-strong border border-gray-100 animate-slide-up">
        <Button type="button" variant="ghost" fullWidth={true} on:click={() => push('/dashboard')}>
          {$t('common.cancel')}
        </Button>
        <Button
          type="submit"
          variant="gradient"
          fullWidth={true}
          disabled={saving || completedCount === 0}
        >
          {#if saving}
            <div class="flex items-center justify-center gap-2">
              <div class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></div>
              <span>{$t('common.loading')}</span>
            </div>
          {:else}
            <div class="flex items-center justify-center gap-2">
              <CheckCircle2 size={20} />
              <span>{$t('entries.saveEntry')}</span>
            </div>
          {/if}
        </Button>
      </div>
    </form>
  {/if}
</AuthenticatedLayout>

<style>
  /* Custom slider thumb styling */
  :global(.slider-thumb::-webkit-slider-thumb) {
    -webkit-appearance: none;
    appearance: none;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
    transition: all 0.2s ease;
  }

  :global(.slider-thumb::-webkit-slider-thumb:hover) {
    transform: scale(1.2);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.6);
  }

  :global(.slider-thumb::-webkit-slider-thumb:active) {
    transform: scale(1.1);
  }

  :global(.slider-thumb::-moz-range-thumb) {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
    transition: all 0.2s ease;
  }

  :global(.slider-thumb::-moz-range-thumb:hover) {
    transform: scale(1.2);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.6);
  }

  :global(.slider-thumb::-moz-range-thumb:active) {
    transform: scale(1.1);
  }
</style>
