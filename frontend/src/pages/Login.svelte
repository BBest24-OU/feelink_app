<script lang="ts">
  import { onMount } from 'svelte';
  import { push } from 'svelte-spa-router';
  import { authActions, isAuthenticated } from '../stores/user';
  import { t } from '../i18n';
  import { Heart } from 'lucide-svelte';
  import Button from '../components/Button.svelte';
  import Input from '../components/Input.svelte';
  import Card from '../components/Card.svelte';

  let email = '';
  let password = '';
  let loading = false;
  let error = '';

  onMount(() => {
    // Redirect if already authenticated
    if ($isAuthenticated) {
      push('/dashboard');
    }
  });

  async function handleLogin() {
    error = '';
    loading = true;

    const result = await authActions.login(email, password);

    if (result.success) {
      // Wait for store to update before redirecting
      await new Promise(resolve => setTimeout(resolve, 100));
      push('/dashboard');
    } else {
      error = result.error || $t('auth.loginError');
    }

    loading = false;
  }
</script>

<div class="h-screen w-screen bg-gray-50 flex items-center justify-center overflow-y-auto">
  <div class="w-full max-w-md px-4 py-8 my-auto">
    <!-- Logo -->
    <div class="text-center mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-2xl mb-4">
        <Heart size={32} class="text-white" />
      </div>
      <h1 class="text-3xl font-bold text-gray-800 mb-1">Feelink</h1>
      <p class="text-gray-600 text-sm">{$t('auth.login')}</p>
    </div>

    <Card>
      <form on:submit|preventDefault={handleLogin} class="space-y-6">
        <Input
          id="email"
          type="email"
          label={$t('auth.email')}
          bind:value={email}
          required
          disabled={loading}
        />

        <Input
          id="password"
          type="password"
          label={$t('auth.password')}
          bind:value={password}
          required
          disabled={loading}
        />

        {#if error}
          <div
            role="alert"
            aria-live="assertive"
            class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm"
          >
            {error}
          </div>
        {/if}

        <Button type="submit" variant="primary" fullWidth disabled={loading}>
          {loading ? $t('common.loading') : $t('auth.loginButton')}
        </Button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          {$t('auth.noAccount')}
          <a href="#/register" class="text-primary-600 hover:text-primary-700 font-medium">
            {$t('auth.register')}
          </a>
        </p>
      </div>
    </Card>
  </div>
</div>
