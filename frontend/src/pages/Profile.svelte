<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore, authActions } from '../stores/user';
  import { t } from '../i18n';
  import { User, Mail, Globe, Clock, Lock } from 'lucide-svelte';
  import Card from '../components/Card.svelte';
  import Button from '../components/Button.svelte';
  import Input from '../components/Input.svelte';
  import AuthenticatedLayout from '../components/AuthenticatedLayout.svelte';

  let name = '';
  let email = '';
  let language = 'en';
  let timezone = 'UTC';
  let loading = false;
  let success = '';
  let error = '';

  onMount(() => {
    if ($authStore.user) {
      name = $authStore.user.name || '';
      email = $authStore.user.email || '';
      language = $authStore.user.language || 'en';
      timezone = $authStore.user.timezone || 'UTC';
    }
  });

  async function handleSave() {
    error = '';
    success = '';
    loading = true;

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/users/me`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${$authStore.accessToken}`
        },
        body: JSON.stringify({
          name: name || null,
          language,
          timezone
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      const updatedUser = await response.json();

      // Update auth store
      authStore.update((state) => ({
        ...state,
        user: updatedUser
      }));

      success = $t('profile.updateSuccess');
    } catch (err) {
      error = $t('profile.updateError');
    } finally {
      loading = false;
    }
  }

  function handleResetPassword() {
    // Placeholder - no real action yet
    alert($t('profile.resetPasswordPlaceholder'));
  }
</script>

<AuthenticatedLayout maxWidth="lg">
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl md:text-3xl font-bold text-gray-800">{$t('profile.title')}</h1>
      <p class="text-gray-600 mt-1">{$t('profile.subtitle')}</p>
    </div>

    <!-- Profile Information Card -->
    <Card>
      <h2 class="text-xl font-semibold text-gray-800 mb-6 flex items-center space-x-2">
        <User size={24} class="text-primary-600" />
        <span>{$t('profile.personalInfo')}</span>
      </h2>

      <form on:submit|preventDefault={handleSave} class="space-y-6">
        <!-- Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 mb-2">
            <div class="flex items-center space-x-2">
              <User size={16} />
              <span>{$t('profile.name')}</span>
            </div>
          </label>
          <Input
            id="name"
            type="text"
            bind:value={name}
            placeholder={$t('profile.namePlaceholder')}
            disabled={loading}
          />
        </div>

        <!-- Email (read-only) -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            <div class="flex items-center space-x-2">
              <Mail size={16} />
              <span>{$t('profile.email')}</span>
            </div>
          </label>
          <Input id="email" type="email" bind:value={email} disabled readonly />
          <p class="mt-1 text-xs text-gray-500">{$t('profile.emailReadonly')}</p>
        </div>

        <!-- Language -->
        <div>
          <label for="language" class="block text-sm font-medium text-gray-700 mb-2">
            <div class="flex items-center space-x-2">
              <Globe size={16} />
              <span>{$t('profile.language')}</span>
            </div>
          </label>
          <select
            id="language"
            bind:value={language}
            disabled={loading}
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-50 disabled:text-gray-500"
          >
            <option value="en">{$t('settings.languages.en')}</option>
            <option value="pl">{$t('settings.languages.pl')}</option>
          </select>
        </div>

        <!-- Timezone -->
        <div>
          <label for="timezone" class="block text-sm font-medium text-gray-700 mb-2">
            <div class="flex items-center space-x-2">
              <Clock size={16} />
              <span>{$t('profile.timezone')}</span>
            </div>
          </label>
          <Input
            id="timezone"
            type="text"
            bind:value={timezone}
            placeholder="UTC"
            disabled={loading}
          />
        </div>

        <!-- Success/Error Messages -->
        {#if success}
          <div class="p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
            {success}
          </div>
        {/if}

        {#if error}
          <div class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        {/if}

        <!-- Save Button -->
        <Button type="submit" variant="primary" disabled={loading}>
          {loading ? $t('common.loading') : $t('profile.saveChanges')}
        </Button>
      </form>
    </Card>

    <!-- Security Card -->
    <Card>
      <h2 class="text-xl font-semibold text-gray-800 mb-6 flex items-center space-x-2">
        <Lock size={24} class="text-primary-600" />
        <span>{$t('profile.security')}</span>
      </h2>

      <div class="space-y-4">
        <div>
          <h3 class="text-sm font-medium text-gray-700 mb-2">{$t('profile.password')}</h3>
          <p class="text-sm text-gray-600 mb-4">{$t('profile.passwordDescription')}</p>
          <Button variant="secondary" on:click={handleResetPassword}>
            {$t('profile.resetPassword')}
          </Button>
        </div>
      </div>
    </Card>
  </div>
</AuthenticatedLayout>
  import Card from '../components/Card.svelte';
  import Button from '../components/Button.svelte';
  import Modal from '../components/Modal.svelte';

  let isGeneratingDemo = false;
  let isClearingData = false;
  let showClearConfirmModal = false;
  let showDemoConfirmModal = false;
  let error: string | null = null;
  let success: string | null = null;

  console.log('[Profile] Module loaded - script running');

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
    console.log('[Profile] Starting demo data generation');
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
      console.log('[Profile] Demo data generated:', result);
      success = $t('profile.demoDataGenerated');

      // Reload the page after a short delay to show the data
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (err: any) {
      console.error('[Profile] Error generating demo data:', err);
      error = err.message || $t('profile.demoDataError');
    } finally {
      isGeneratingDemo = false;
    }
  }

  async function handleClearData() {
    console.log('[Profile] Starting data clear');
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

      console.log('[Profile] Data cleared successfully');
      success = $t('profile.dataCleared');

      // Reload the page after a short delay
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (err: any) {
      console.error('[Profile] Error clearing data:', err);
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
  <!-- Navigation -->
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

  <!-- Main Content -->
  <div class="container mx-auto p-6 max-w-4xl">
    <!-- Page Title -->
    <div class="mb-8">
      <h2 class="text-3xl font-bold text-gray-800">{$t('profile.title')}</h2>
      <p class="text-sm text-gray-500 mt-2">You are on the Profile page</p>
    </div>

    <!-- Error/Success Messages -->
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
        <h3 class="text-xl font-bold text-gray-800 mb-2">{$t('profile.dataSection')}</h3>
        <p class="text-gray-600 mb-6">{$t('profile.dataSectionDescription')}</p>

        <div class="space-y-4">
          <!-- Demo Data Section -->
          <div class="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 class="font-semibold text-gray-800 mb-2">{$t('profile.demoData')}</h4>
            <p class="text-sm text-gray-600 mb-4">{$t('profile.demoDataDescription')}</p>
            <button
              on:click={() => {
                console.log('[Profile] Demo data button clicked');
                showDemoConfirmModal = true;
              }}
              disabled={isGeneratingDemo || isClearingData}
              class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-colors"
            >
              {#if isGeneratingDemo}
                {$t('common.loading')}
              {:else}
                {$t('profile.generateDemoData')}
              {/if}
            </button>
          </div>

          <!-- Clear Data Section -->
          <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <h4 class="font-semibold text-gray-800 mb-2">{$t('profile.clearData')}</h4>
            <p class="text-sm text-gray-600 mb-4">{$t('profile.clearDataDescription')}</p>
            <button
              on:click={() => {
                console.log('[Profile] Clear data button clicked');
                showClearConfirmModal = true;
              }}
              disabled={isGeneratingDemo || isClearingData}
              class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-colors"
            >
              {#if isClearingData}
                {$t('common.loading')}
              {:else}
                {$t('profile.clearAllData')}
              {/if}
            </button>
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
