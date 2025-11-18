<script lang="ts">
  import { onMount } from 'svelte';
  import { metricsStore, metricsActions, type Metric } from '../stores/metrics';
  import { t } from '../i18n';
  import AuthenticatedLayout from '../components/AuthenticatedLayout.svelte';
  import Button from '../components/Button.svelte';
  import Card from '../components/Card.svelte';
  import Loading from '../components/Loading.svelte';
  import Modal from '../components/Modal.svelte';
  import Input from '../components/Input.svelte';
  import Select from '../components/Select.svelte';

  let showCreateModal = false;
  let editingMetric: Metric | null = null;
  let searchQuery = '';
  let selectedCategory = '';
  let showArchived = false;

  // Form fields
  let formData = {
    name_key: '',
    category: '',
    value_type: '',
    min_value: null as number | null,
    max_value: null as number | null,
    description: '',
    color: '#6366f1',
    icon: ''
  };

  const categoryOptions = [
    { value: 'physical', label: $t('metrics.categories.physical') },
    { value: 'psychological', label: $t('metrics.categories.psychological') },
    { value: 'triggers', label: $t('metrics.categories.triggers') },
    { value: 'medications', label: $t('metrics.categories.medications') },
    { value: 'selfcare', label: $t('metrics.categories.selfcare') },
    { value: 'wellness', label: $t('metrics.categories.wellness') },
    { value: 'notes', label: $t('metrics.categories.notes') }
  ];

  const typeOptions = [
    { value: 'range', label: $t('metrics.types.range') },
    { value: 'number', label: $t('metrics.types.number') },
    { value: 'boolean', label: $t('metrics.types.boolean') },
    { value: 'count', label: $t('metrics.types.count') },
    { value: 'text', label: $t('metrics.types.text') }
  ];

  onMount(async () => {
    await metricsActions.load(showArchived);
  });

  $: filteredMetrics = $metricsStore.metrics
    .filter((m) => showArchived || !m.archived)
    .filter((m) => !selectedCategory || m.category === selectedCategory)
    .filter((m) => !searchQuery || m.name_key.toLowerCase().includes(searchQuery.toLowerCase()));

  $: groupedMetrics = filteredMetrics.reduce((acc, metric) => {
    if (!acc[metric.category]) {
      acc[metric.category] = [];
    }
    acc[metric.category].push(metric);
    return acc;
  }, {} as Record<string, Metric[]>);

  function openCreateModal() {
    editingMetric = null;
    resetForm();
    showCreateModal = true;
  }

  function openEditModal(metric: Metric) {
    editingMetric = metric;
    formData = {
      name_key: metric.name_key,
      category: metric.category,
      value_type: metric.value_type,
      min_value: metric.min_value ? Number(metric.min_value) : null,
      max_value: metric.max_value ? Number(metric.max_value) : null,
      description: metric.description || '',
      color: metric.color || '#6366f1',
      icon: metric.icon || ''
    };
    showCreateModal = true;
  }

  function resetForm() {
    formData = {
      name_key: '',
      category: '',
      value_type: '',
      min_value: null,
      max_value: null,
      description: '',
      color: '#6366f1',
      icon: ''
    };
  }

  async function handleSubmit() {
    const data = {
      ...formData,
      name_key: formData.name_key.toLowerCase().replace(/\s+/g, '_')
    };

    if (editingMetric) {
      await metricsActions.update(editingMetric.id, data);
    } else {
      await metricsActions.create(data);
    }

    showCreateModal = false;
    resetForm();
  }

  async function handleArchive(id: number) {
    if (confirm($t('metrics.archive') + '?')) {
      await metricsActions.archive(id);
    }
  }

  async function handleUnarchive(id: number) {
    await metricsActions.unarchive(id);
  }

  function getCategoryColor(category: string): string {
    const colors: Record<string, string> = {
      physical: 'bg-blue-100 text-blue-800',
      psychological: 'bg-purple-100 text-purple-800',
      triggers: 'bg-red-100 text-red-800',
      medications: 'bg-green-100 text-green-800',
      selfcare: 'bg-yellow-100 text-yellow-800',
      wellness: 'bg-indigo-100 text-indigo-800',
      notes: 'bg-gray-100 text-gray-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  }
</script>

<AuthenticatedLayout>
  <div class="flex justify-between items-center mb-8">
    <div>
      <h1 class="text-3xl font-bold text-gray-800">{$t('metrics.title')}</h1>
      <p class="text-gray-600 mt-2">Create and manage your custom tracking metrics.</p>
    </div>
    <Button variant="primary" on:click={openCreateModal}>
      + {$t('metrics.create')}
    </Button>
  </div>

  <div class="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
    <Input
      type="text"
      placeholder={$t('common.search')}
      bind:value={searchQuery}
    />

    <Select
      bind:value={selectedCategory}
      options={categoryOptions}
      label={$t('metrics.category')}
    />

    <div class="flex items-end">
      <label class="flex items-center space-x-2 cursor-pointer">
        <input
          type="checkbox"
          bind:checked={showArchived}
          on:change={() => metricsActions.load(showArchived)}
          class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
        />
        <span class="text-sm text-gray-700">{$t('metrics.showArchived')}</span>
      </label>
    </div>
  </div>

  {#if $metricsStore.loading}
    <Loading />
  {:else if filteredMetrics.length === 0}
    <Card>
      <p class="text-center text-gray-500 py-8">{$t('metrics.noMetrics')}</p>
    </Card>
  {:else}
    <div class="space-y-6">
      {#each Object.entries(groupedMetrics) as [category, metrics]}
        <div>
          <h2 class="text-xl font-semibold text-gray-700 mb-3">
            {$t(`metrics.categories.${category}`)} ({metrics.length})
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {#each metrics as metric}
              <Card hover>
                <div class="flex justify-between items-start mb-2">
                  <div class="flex items-center space-x-2">
                    {#if metric.color}
                      <div class="w-4 h-4 rounded-full" style="background-color: {metric.color}"></div>
                    {/if}
                    <h3 class="font-semibold text-gray-800">{metric.name_key}</h3>
                  </div>
                  <span class="text-xs px-2 py-1 rounded-full {getCategoryColor(metric.category)}">
                    {$t(`metrics.types.${metric.value_type}`)}
                  </span>
                </div>

                {#if metric.description}
                  <p class="text-sm text-gray-600 mb-3">{metric.description}</p>
                {/if}

                {#if metric.value_type === 'range' && metric.min_value !== null && metric.max_value !== null}
                  <p class="text-xs text-gray-500 mb-3">
                    Range: {metric.min_value} - {metric.max_value}
                  </p>
                {/if}

                <div class="flex space-x-2">
                  <Button size="sm" variant="ghost" on:click={() => openEditModal(metric)}>
                    {$t('common.edit')}
                  </Button>
                  {#if metric.archived}
                    <Button size="sm" variant="secondary" on:click={() => handleUnarchive(metric.id)}>
                      {$t('metrics.unarchive')}
                    </Button>
                  {:else}
                    <Button size="sm" variant="danger" on:click={() => handleArchive(metric.id)}>
                      {$t('metrics.archive')}
                    </Button>
                  {/if}
                </div>
              </Card>
            {/each}
          </div>
        </div>
    {/each}
  </div>
  {/if}
</AuthenticatedLayout>

<Modal bind:open={showCreateModal} title={editingMetric ? $t('metrics.edit') : $t('metrics.create')}>
  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <Input
      id="name"
      label={$t('metrics.name')}
      bind:value={formData.name_key}
      required
    />

    <Select
      id="category"
      label={$t('metrics.category')}
      bind:value={formData.category}
      options={categoryOptions}
      required
    />

    <Select
      id="type"
      label={$t('metrics.type')}
      bind:value={formData.value_type}
      options={typeOptions}
      required
      disabled={!!editingMetric}
    />

    {#if formData.value_type === 'range'}
      <div class="grid grid-cols-2 gap-4">
        <Input
          id="min"
          type="number"
          label={$t('metrics.minValue')}
          bind:value={formData.min_value}
          required
        />
        <Input
          id="max"
          type="number"
          label={$t('metrics.maxValue')}
          bind:value={formData.max_value}
          required
        />
      </div>
    {/if}

    <Input
      id="description"
      label={$t('metrics.description')}
      bind:value={formData.description}
    />

    <div class="grid grid-cols-2 gap-4">
      <div>
        <label for="color" class="block text-sm font-medium text-gray-700 mb-1">
          {$t('metrics.color')}
        </label>
        <input
          id="color"
          type="color"
          bind:value={formData.color}
          class="w-full h-10 rounded-lg border border-gray-300"
        />
      </div>

      <Input
        id="icon"
        label={$t('metrics.icon')}
        bind:value={formData.icon}
        placeholder="😊"
      />
    </div>

    <div class="flex justify-end space-x-3 pt-4">
      <Button type="button" variant="ghost" on:click={() => showCreateModal = false}>
        {$t('common.cancel')}
      </Button>
      <Button type="submit" variant="primary" disabled={$metricsStore.loading}>
        {$t('common.save')}
      </Button>
    </div>
  </form>
</Modal>
