<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { authStore } from '../stores/user';
  import { t } from '../i18n';
  import { Heart, User } from 'lucide-svelte';
  import Button from './Button.svelte';
  import Input from './Input.svelte';

  const dispatch = createEventDispatcher();

  let name = '';
  let loading = false;
  let error = '';

  async function handleComplete() {
    if (!name.trim()) {
      error = $t('onboarding.nameRequired');
      return;
    }

    error = '';
    loading = true;

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/users/me`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${$authStore.accessToken}`
        },
        body: JSON.stringify({
          name: name.trim()
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update name');
      }

      const updatedUser = await response.json();

      // Update auth store
      authStore.update((state) => ({
        ...state,
        user: updatedUser
      }));

      // Notify parent that onboarding is complete
      dispatch('complete');
    } catch (err) {
      error = $t('onboarding.error');
    } finally {
      loading = false;
    }
  }
</script>

<!-- Full screen overlay -->
<div
  class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
  role="dialog"
  aria-modal="true"
  aria-labelledby="onboarding-title"
>
  <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 space-y-6">
    <!-- Logo and Welcome -->
    <div class="text-center">
      <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-2xl mb-4">
        <Heart size={32} class="text-white" />
      </div>
      <h1 id="onboarding-title" class="text-2xl font-bold text-gray-800 mb-2">
        {$t('onboarding.welcome')}
      </h1>
      <p class="text-gray-600">{$t('onboarding.subtitle')}</p>
    </div>

    <!-- Name Input Form -->
    <form on:submit|preventDefault={handleComplete} class="space-y-6">
      <div>
        <label for="onboarding-name" class="block text-sm font-medium text-gray-700 mb-2">
          <div class="flex items-center space-x-2">
            <User size={16} />
            <span>{$t('onboarding.nameLabel')}</span>
          </div>
        </label>
        <Input
          id="onboarding-name"
          type="text"
          bind:value={name}
          placeholder={$t('onboarding.namePlaceholder')}
          disabled={loading}
          autofocus
        />
        <p class="mt-2 text-xs text-gray-500">{$t('onboarding.nameHint')}</p>
      </div>

      {#if error}
        <div class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      {/if}

      <Button type="submit" variant="primary" fullWidth disabled={loading || !name.trim()}>
        {loading ? $t('common.loading') : $t('onboarding.continue')}
      </Button>
    </form>

    <!-- Optional: Skip button -->
    <button
      on:click={() => dispatch('complete')}
      disabled={loading}
      class="w-full text-sm text-gray-500 hover:text-gray-700 transition-colors disabled:opacity-50"
    >
      {$t('onboarding.skip')}
    </button>
  </div>
</div>
