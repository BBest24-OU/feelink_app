<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore, authActions } from '../stores/user';
  import { t } from '../i18n';
  import { User, Mail, Globe, Clock, Lock, Database, Sparkles, Sun, Moon, Monitor } from 'lucide-svelte';
  import Card from '../components/Card.svelte';
  import Button from '../components/Button.svelte';
  import Input from '../components/Input.svelte';
  import Modal from '../components/Modal.svelte';
  import AuthenticatedLayout from '../components/AuthenticatedLayout.svelte';
  import { themeStore } from '../stores/theme';
  import type { Theme } from '../stores/theme';

  let name = '';
  let email = '';
  let language = 'en';
  let timezone = 'UTC';
  let loading = false;
  let success: string | null = '';
  let error: string | null = '';
  let isGeneratingDemo = false;
  let isClearingData = false;
  let showClearConfirmModal = false;
  let showDemoConfirmModal = false;

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

  async function handleGenerateDemoData() {
    console.log('[Profile] Starting demo data generation');
    showDemoConfirmModal = false;
    isGeneratingDemo = true;
    error = null;
    success = null;

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/demo-data/generate`, {
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
      success = $t('onboarding.demoDataGenerated');

      // Close modal and reload page after a short delay to show the data
      setTimeout(() => {
        showDemoConfirmModal = false;
      }, 1000);

      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (err: any) {
      console.error('[Profile] Error generating demo data:', err);
      error = err.message || $t('onboarding.demoDataError');
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
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/demo-data/clear`, {
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
      success = $t('onboarding.dataCleared');

      // Close modal and reload page after a short delay
      setTimeout(() => {
        showClearConfirmModal = false;
      }, 1000);

      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (err: any) {
      console.error('[Profile] Error clearing data:', err);
      error = err.message || $t('onboarding.clearDataError');
    } finally {
      isClearingData = false;
    }
  }

  function handleLogout() {
    authActions.logout();
    window.location.hash = '/login';
  }
</script>

<AuthenticatedLayout maxWidth="lg">
  <div class="space-y-6 md:space-y-8">
    <!-- Enhanced Header -->
    <div class="animate-slide-down">
      <div class="flex items-center gap-3 mb-3">
        <div class="p-3 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl shadow-glow">
          <User size={28} class="text-white" />
        </div>
        <div>
          <h1 class="text-3xl md:text-4xl font-bold text-gray-800 dark:text-white">{$t('profile.title')}</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1 text-lg">{$t('profile.subtitle')}</p>
        </div>
      </div>
    </div>

    <!-- Profile Information Card -->
    <Card gradient={true}>
      <div class="flex items-center gap-3 mb-6">
        <div class="p-2 bg-primary-600 rounded-xl">
          <User size={20} class="text-white" />
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-gray-800 dark:text-white">{$t('profile.personalInfo')}</h2>
      </div>

      <form on:submit|preventDefault={handleSave} class="space-y-6">
        <!-- Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
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
          <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            <div class="flex items-center space-x-2">
              <Mail size={16} />
              <span>{$t('profile.email')}</span>
            </div>
          </label>
          <Input id="email" type="email" bind:value={email} disabled readonly />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">{$t('profile.emailReadonly')}</p>
        </div>

        <!-- Language -->
        <div>
          <label for="language" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            <div class="flex items-center space-x-2">
              <Globe size={16} />
              <span>{$t('profile.language')}</span>
            </div>
          </label>
          <select
            id="language"
            bind:value={language}
            disabled={loading}
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-50 disabled:text-gray-500"
          >
            <option value="en">{$t('settings.languages.en')}</option>
            <option value="pl">{$t('settings.languages.pl')}</option>
          </select>
        </div>

        <!-- Timezone -->
        <div>
          <label for="timezone" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
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
          <div class="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg text-green-700 dark:text-green-300 text-sm">
            {success}
          </div>
        {/if}

        {#if error}
          <div class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300 text-sm">
            {error}
          </div>
        {/if}

        <!-- Save Button -->
        <Button type="submit" variant="primary" disabled={loading}>
          {loading ? $t('common.loading') : $t('profile.saveChanges')}
        </Button>
      </form>
    </Card>

    <!-- Theme Settings Card -->
    <Card gradient={false}>
      <div class="flex items-center gap-3 mb-6">
        <div class="p-2 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-xl">
          <Sun size={20} class="text-white" />
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-gray-800 dark:text-white">{$t('profile.theme')}</h2>
      </div>

      <div class="space-y-4">
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">{$t('profile.themeDescription')}</p>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <!-- Light Theme Option -->
          <button
            type="button"
            on:click={() => themeStore.setTheme('light')}
            class="p-4 rounded-xl border-2 transition-all duration-200 {$themeStore.theme === 'light'
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
              : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600'}"
          >
            <div class="flex flex-col items-center space-y-2">
              <Sun size={24} class={$themeStore.theme === 'light' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'} />
              <span class="font-medium text-sm {$themeStore.theme === 'light' ? 'text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'}">
                {$t('profile.lightTheme')}
              </span>
            </div>
          </button>

          <!-- Dark Theme Option -->
          <button
            type="button"
            on:click={() => themeStore.setTheme('dark')}
            class="p-4 rounded-xl border-2 transition-all duration-200 {$themeStore.theme === 'dark'
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
              : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600'}"
          >
            <div class="flex flex-col items-center space-y-2">
              <Moon size={24} class={$themeStore.theme === 'dark' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'} />
              <span class="font-medium text-sm {$themeStore.theme === 'dark' ? 'text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'}">
                {$t('profile.darkTheme')}
              </span>
            </div>
          </button>

          <!-- System Theme Option -->
          <button
            type="button"
            on:click={() => themeStore.setTheme('system')}
            class="p-4 rounded-xl border-2 transition-all duration-200 {$themeStore.theme === 'system'
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
              : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600'}"
          >
            <div class="flex flex-col items-center space-y-2">
              <Monitor size={24} class={$themeStore.theme === 'system' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'} />
              <span class="font-medium text-sm {$themeStore.theme === 'system' ? 'text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300'}">
                {$t('profile.systemTheme')}
              </span>
            </div>
          </button>
        </div>

        <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
          {$t('profile.currentTheme')}: <span class="font-semibold capitalize">{$themeStore.resolvedTheme}</span>
        </p>
      </div>
    </Card>

    <!-- Security Card -->
    <Card gradient={false}>
      <div class="flex items-center gap-3 mb-6">
        <div class="p-2 bg-gradient-to-br from-red-500 to-pink-600 rounded-xl">
          <Lock size={20} class="text-white" />
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-gray-800 dark:text-white">{$t('profile.security')}</h2>
      </div>

      <div class="space-y-4 p-5 bg-gray-50 dark:bg-gray-700 rounded-xl">
        <div>
          <h3 class="text-base font-semibold text-gray-800 dark:text-white mb-2">{$t('profile.password')}</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">{$t('profile.passwordDescription')}</p>
          <Button variant="secondary" size="md" on:click={handleResetPassword}>
            {$t('profile.resetPassword')}
          </Button>
        </div>
      </div>
    </Card>

    <!-- Data Management Card -->
    <Card gradient={true}>
      <div class="flex items-center gap-3 mb-6">
        <div class="p-2 bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl">
          <Database size={20} class="text-white" />
        </div>
        <h2 class="text-xl md:text-2xl font-bold text-gray-800 dark:text-white">{$t('onboarding.dataSection')}</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Demo Data Section -->
        <div class="p-5 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-xl border-2 border-blue-200 dark:border-blue-800 hover:border-blue-300 dark:hover:border-blue-700 transition-colors">
          <h3 class="text-base font-bold text-gray-800 dark:text-white mb-2 flex items-center gap-2">
            <Sparkles size={18} class="text-blue-600 dark:text-blue-400" />
            <span>{$t('onboarding.demoData')}</span>
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4 leading-relaxed">{$t('onboarding.demoDataDescription')}</p>
          <Button
            variant="secondary"
            size="md"
            fullWidth={true}
            disabled={isGeneratingDemo}
            on:click={() => {
              console.log('[Profile] Demo button clicked, showing modal');
              showDemoConfirmModal = true;
            }}
          >
            {#if isGeneratingDemo}
              <div class="flex items-center justify-center gap-2">
                <div class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
                <span>{$t('common.loading')}</span>
              </div>
            {:else}
              <span>{$t('onboarding.generateDemoData')}</span>
            {/if}
          </Button>
        </div>

        <!-- Clear Data Section -->
        <div class="p-5 bg-gradient-to-br from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20 rounded-xl border-2 border-red-200 dark:border-red-800 hover:border-red-300 dark:hover:border-red-700 transition-colors">
          <h3 class="text-base font-bold text-gray-800 dark:text-white mb-2 flex items-center gap-2">
            <Database size={18} class="text-red-600 dark:text-red-400" />
            <span>{$t('onboarding.clearData')}</span>
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4 leading-relaxed">{$t('onboarding.clearDataDescription')}</p>
          <Button
            variant="danger"
            size="md"
            fullWidth={true}
            disabled={isClearingData}
            on:click={() => {
              console.log('[Profile] Clear button clicked, showing modal');
              showClearConfirmModal = true;
            }}
          >
            {#if isClearingData}
              <div class="flex items-center justify-center gap-2">
                <div class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
                <span>{$t('common.loading')}</span>
              </div>
            {:else}
              <span>{$t('onboarding.clearAllData')}</span>
            {/if}
          </Button>
        </div>

        <!-- Success/Error Messages for Data Operations -->
        {#if success && (isGeneratingDemo || isClearingData)}
          <div class="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg text-green-700 dark:text-green-300 text-sm">
            {success}
          </div>
        {/if}

        {#if error && (isGeneratingDemo || isClearingData)}
          <div class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300 text-sm">
            {error}
          </div>
        {/if}
      </div>
    </Card>
  </div>
</AuthenticatedLayout>

<!-- Demo Data Confirmation Modal -->
<Modal open={showDemoConfirmModal} onClose={() => !isGeneratingDemo && (showDemoConfirmModal = false)}>
  <h3 slot="title">{isGeneratingDemo ? $t('common.loading') : $t('onboarding.confirmDemoData')}</h3>
  <div slot="content">
    {#if isGeneratingDemo}
      <div class="space-y-4">
        <p class="text-gray-700 dark:text-gray-300">{$t('onboarding.demoDataDescription')}</p>
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Generating demo data...</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">In progress</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div class="bg-primary-600 h-2 rounded-full animate-pulse w-3/4"></div>
          </div>
        </div>
      </div>
    {:else}
      <p class="text-gray-700 dark:text-gray-300">{$t('onboarding.confirmDemoDataMessage')}</p>
    {/if}
  </div>
  <div slot="actions" class="flex space-x-3">
    {#if !isGeneratingDemo}
      <Button variant="ghost" on:click={() => showDemoConfirmModal = false}>
        {$t('common.cancel')}
      </Button>
      <Button variant="primary" on:click={handleGenerateDemoData}>
        {$t('common.confirm')}
      </Button>
    {/if}
  </div>
</Modal>

<!-- Clear Data Confirmation Modal -->
<Modal open={showClearConfirmModal} onClose={() => !isClearingData && (showClearConfirmModal = false)}>
  <h3 slot="title">{isClearingData ? $t('common.loading') : $t('onboarding.confirmClearData')}</h3>
  <div slot="content">
    {#if isClearingData}
      <div class="space-y-4">
        <p class="text-gray-700 dark:text-gray-300">{$t('onboarding.clearDataDescription')}</p>
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Clearing all data...</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">In progress</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div class="bg-red-600 h-2 rounded-full animate-pulse w-3/4"></div>
          </div>
        </div>
      </div>
    {:else}
      <div>
        <p class="text-gray-700 dark:text-gray-300 mb-4">{$t('onboarding.confirmClearDataMessage')}</p>
        <p class="text-red-600 dark:text-red-400 font-semibold">{$t('onboarding.clearDataWarning')}</p>
      </div>
    {/if}
  </div>
  <div slot="actions" class="flex space-x-3">
    {#if !isClearingData}
      <Button variant="ghost" on:click={() => showClearConfirmModal = false}>
        {$t('common.cancel')}
      </Button>
      <Button variant="danger" on:click={handleClearData}>
        {$t('onboarding.clearAllData')}
      </Button>
    {/if}
  </div>
</Modal>
