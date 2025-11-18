<script lang="ts">
  import { onMount } from 'svelte';
  import { entriesStore, entriesActions } from '../stores/entries';
  import { metricsStore } from '../stores/metrics';
  import { t } from '../i18n';
  import Button from '../components/Button.svelte';
  import Card from '../components/Card.svelte';
  import Loading from '../components/Loading.svelte';
  import Input from '../components/Input.svelte';

  let dateFrom = '';
  let dateTo = '';
  let searchQuery = '';

  onMount(async () => {
    await entriesActions.load();
  });

  async function handleFilter() {
    await entriesActions.load({
      date_from: dateFrom || undefined,
      date_to: dateTo || undefined
    });
  }

  async function handleDelete(id: number) {
    if (confirm($t('entries.deleteConfirm'))) {
      await entriesActions.delete(id);
    }
  }

  $: filteredEntries = $entriesStore.entries.filter((entry) => {
    if (!searchQuery) return true;
    return entry.notes?.toLowerCase().includes(searchQuery.toLowerCase()) ||
           entry.entry_date.includes(searchQuery);
  });

  function getMetricName(metricId: number): string {
    const metric = $metricsStore.metrics.find(m => m.id === metricId);
    return metric?.name_key || 'Unknown';
  }

  function formatValue(value: any): string {
    if (value.value_numeric !== null) return String(value.value_numeric);
    if (value.value_boolean !== null) return value.value_boolean ? 'Yes' : 'No';
    if (value.value_text !== null) return value.value_text;
    return '-';
  }
</script>

<div class="container mx-auto p-6">
  <div class="flex justify-between items-center mb-8">
    <h1 class="text-3xl font-bold text-gray-800">{$t('entries.title')}</h1>
    <Button variant="primary" on:click={() => window.location.hash = '/log'}>
      + {$t('entries.create')}
    </Button>
  </div>

  <div class="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
    <Input
      type="text"
      placeholder={$t('common.search')}
      bind:value={searchQuery}
    />

    <Input
      type="date"
      label="From"
      bind:value={dateFrom}
      on:change={handleFilter}
    />

    <Input
      type="date"
      label="To"
      bind:value={dateTo}
      on:change={handleFilter}
    />
  </div>

  {#if $entriesStore.loading}
    <Loading />
  {:else if filteredEntries.length === 0}
    <Card>
      <p class="text-center text-gray-500 py-8">{$t('entries.noEntries')}</p>
    </Card>
  {:else}
    <div class="space-y-4">
      {#each filteredEntries as entry}
        <Card>
          <div class="flex justify-between items-start mb-4">
            <div>
              <h3 class="text-lg font-semibold text-gray-800">{entry.entry_date}</h3>
              {#if entry.notes}
                <p class="text-sm text-gray-600 mt-1">{entry.notes}</p>
              {/if}
            </div>
            <div class="flex space-x-2">
              <Button
                size="sm"
                variant="ghost"
                on:click={() => window.location.hash = '/log'}
              >
                {$t('common.edit')}
              </Button>
              <Button
                size="sm"
                variant="danger"
                on:click={() => handleDelete(entry.id)}
              >
                {$t('common.delete')}
              </Button>
            </div>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {#each entry.values as value}
              <div class="bg-gray-50 rounded-lg p-3">
                <p class="text-xs text-gray-500 mb-1">{getMetricName(value.metric_id)}</p>
                <p class="text-sm font-semibold text-gray-800">{formatValue(value)}</p>
              </div>
            {/each}
          </div>
        </Card>
      {/each}
    </div>

    {#if $entriesStore.total > filteredEntries.length}
      <div class="mt-6 text-center">
        <Button variant="ghost" on:click={() => entriesActions.load({ limit: 200 })}>
          Load More
        </Button>
      </div>
    {/if}
  {/if}
</div>
