<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore, authActions } from '../stores/user';
  import { t } from '../i18n';
  import Card from '../components/Card.svelte';
  import Button from '../components/Button.svelte';
  import Modal from '../components/Modal.svelte';

  let isGeneratingDemo = false;
  let isClearingData = false;
  let showClearConfirmModal = false;
  let showDemoConfirmModal = false;
  let error: string | null = null;
  let success: string | null = null;

  onMount(async () => {
    console.log('[Profile] Component mounted');
    if (!$authStore.accessToken) {
      window.location.hash = '/login';
      return;
    }

    if (!$authStore.user) {
      await authActions.loadProfile();
    }
    console.log('[Profile] User loaded:', $authStore.user);
  });

  async function handleGenerateDemoData() {
    showDemoConfirmModal = false;
    isGeneratingDemo = true;
    error = null;
    success = null;

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/demo-data/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${$authStore.accessToken}`
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate demo data');
      }

      const result = await response.json();
      success = $t('profile.demoDataGenerated');

      // Reload the page after a short delay to show the data
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (err: any) {
      error = err.message || $t('profile.demoDataError');
    } finally {
      isGeneratingDemo = false;
    }
  }

  async function handleClearData() {
    showClearConfirmModal = false;
    isClearingData = true;
    error = null;
    success = null;

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/demo-data/clear`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${$authStore.accessToken}`
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to clear data');
      }

      success = $t('profile.dataCleared');

      // Reload the page after a short delay
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (err: any) {
      error = err.message || $t('profile.clearDataError');
    } finally {
      isClearingData = false;
    }
  }

  function handleLogout() {
    authActions.logout();
    window.location.hash = '/login';
  }
</script>

<div class="min-h-screen bg-gray-50">
  <nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="container mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-primary-600">FeelInk</h1>
        <div class="flex items-center space-x-6">
          <a href="#/dashboard" class="text-gray-700 hover:text-primary-600 font-medium">
            {$t('nav.dashboard')}
          </a>
          <a href="#/log" class="text-gray-700 hover:text-primary-600 font-medium">
            {$t('nav.log')}
          </a>
          <a href="#/metrics" class="text-gray-700 hover:text-primary-600 font-medium">
            {$t('nav.metrics')}
          </a>
          <a href="#/entries" class="text-gray-700 hover:text-primary-600 font-medium">
            Entries
          </a>
          <a href="#/insights" class="text-gray-700 hover:text-primary-600 font-medium">
            Insights
          </a>
          <a href="#/correlations" class="text-gray-700 hover:text-primary-600 font-medium">
            Correlations
          </a>
          <a href="#/profile" class="text-primary-600 hover:text-primary-700 font-medium">
            {$t('nav.profile')}
          </a>
          <Button size="sm" variant="ghost" on:click={handleLogout}>
            {$t('auth.logout')}
          </Button>
        </div>
      </div>
    </div>
  </nav>

  <div class="container mx-auto p-6 max-w-4xl">
    <div class="mb-8">
      <h2 class="text-3xl font-bold text-gray-800">{$t('profile.title')}</h2>
    </div>

    {#if error}
      <div class="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-700">{error}</p>
      </div>
    {/if}

    {#if success}
      <div class="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-green-700">{success}</p>
      </div>
    {/if}

    <div class="space-y-6">
      <!-- Account Information -->
      <Card>
        <h3 class="text-xl font-bold text-gray-800 mb-4">{$t('profile.accountInfo')}</h3>
        <div class="space-y-3">
          <div>
            <label class="text-sm font-medium text-gray-600">{$t('auth.email')}</label>
            <p class="text-gray-800">{$authStore.user?.email || ''}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-600">{$t('settings.language')}</label>
            <p class="text-gray-800">{$authStore.user?.language === 'pl' ? 'Polski' : 'English'}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-600">{$t('settings.timezone')}</label>
            <p class="text-gray-800">{$authStore.user?.timezone || 'UTC'}</p>
          </div>
        </div>
      </Card>

      <!-- Data Section -->
      <Card>
        <h3 class="text-xl font-bold text-gray-800 mb-2">
          {$t('profile.dataSection')}
          <!-- Debug: Section is rendering -->
        </h3>
        <p class="text-gray-600 mb-6">{$t('profile.dataSectionDescription')}</p>

        <div class="space-y-4">
          <!-- Demo Data Section -->
          <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 class="font-semibold text-gray-800 mb-2">{$t('profile.demoData')}</h4>
            <p class="text-sm text-gray-600 mb-4">{$t('profile.demoDataDescription')}</p>
            <p class="text-xs text-gray-500 mb-2">Debug: Button should appear below</p>
            <Button
              on:click={() => {
                console.log('[Profile] Demo data button clicked');
                showDemoConfirmModal = true;
              }}
              variant="primary"
              disabled={isGeneratingDemo || isClearingData}
            >
              {#if isGeneratingDemo}
                {$t('common.loading')}
              {:else}
                {$t('profile.generateDemoData')}
              {/if}
            </Button>
          </div>

          <!-- Clear Data Section -->
          <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <h4 class="font-semibold text-gray-800 mb-2">{$t('profile.clearData')}</h4>
            <p class="text-sm text-gray-600 mb-4">{$t('profile.clearDataDescription')}</p>
            <p class="text-xs text-gray-500 mb-2">Debug: Button should appear below</p>
            <Button
              on:click={() => {
                console.log('[Profile] Clear data button clicked');
                showClearConfirmModal = true;
              }}
              variant="danger"
              disabled={isGeneratingDemo || isClearingData}
            >
              {#if isClearingData}
                {$t('common.loading')}
              {:else}
                {$t('profile.clearAllData')}
              {/if}
            </Button>
          </div>
        </div>
      </Card>
    </div>
  </div>
</div>

<!-- Demo Data Confirmation Modal -->
{#if showDemoConfirmModal}
  <Modal onClose={() => showDemoConfirmModal = false}>
    <h3 slot="title">{$t('profile.confirmDemoData')}</h3>
    <div slot="content">
      <p class="text-gray-700">{$t('profile.confirmDemoDataMessage')}</p>
    </div>
    <div slot="actions" class="flex space-x-3">
      <Button variant="ghost" on:click={() => showDemoConfirmModal = false}>
        {$t('common.cancel')}
      </Button>
      <Button variant="primary" on:click={handleGenerateDemoData}>
        {$t('common.confirm')}
      </Button>
    </div>
  </Modal>
{/if}

<!-- Clear Data Confirmation Modal -->
{#if showClearConfirmModal}
  <Modal onClose={() => showClearConfirmModal = false}>
    <h3 slot="title">{$t('profile.confirmClearData')}</h3>
    <div slot="content">
      <p class="text-gray-700 mb-4">{$t('profile.confirmClearDataMessage')}</p>
      <p class="text-red-600 font-semibold">{$t('profile.clearDataWarning')}</p>
    </div>
    <div slot="actions" class="flex space-x-3">
      <Button variant="ghost" on:click={() => showClearConfirmModal = false}>
        {$t('common.cancel')}
      </Button>
      <Button variant="danger" on:click={handleClearData}>
        {$t('profile.clearAllData')}
      </Button>
    </div>
  </Modal>
{/if}

<style>
</style>
