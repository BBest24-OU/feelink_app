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
