<script lang="ts">
  import { push } from 'svelte-spa-router';
  import { authActions } from '../stores/user';
  import { t, locale } from '../i18n';
  import { Heart } from 'lucide-svelte';
  import Button from '../components/Button.svelte';
  import Input from '../components/Input.svelte';
  import Card from '../components/Card.svelte';

  let email = '';
  let password = '';
  let confirmPassword = '';
  let loading = false;
  let error = '';

  async function handleRegister() {
    error = '';

    if (password !== confirmPassword) {
      error = $t('auth.passwordMismatch');
      return;
    }

    loading = true;

    const result = await authActions.register(email, password, $locale || 'en');

    if (result.success) {
      push('/dashboard');
    } else {
      error = result.error || $t('auth.registerError');
    }

    loading = false;
  }
</script>

<div class="min-h-screen bg-gray-50 flex items-center justify-center">
  <div class="w-full max-w-md px-4 py-8">
    <!-- Logo -->
    <div class="text-center mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-2xl mb-4">
        <Heart size={32} class="text-white" />
      </div>
      <h1 class="text-3xl font-bold text-gray-800 mb-1">Feelink</h1>
      <p class="text-gray-600 text-sm">{$t('auth.register')}</p>
    </div>

    <Card>
      <form on:submit|preventDefault={handleRegister} class="space-y-6">
        <Input
          id="email"
          type="email"
          label={$t('auth.email')}
          bind:value={email}
          required
          disabled={loading}
        />

        <div>
          <Input
            id="password"
            type="password"
            label={$t('auth.password')}
            bind:value={password}
            required
            disabled={loading}
          />
          <p class="mt-1 text-xs text-gray-500">
            Password must contain at least one uppercase letter
          </p>
        </div>

        <Input
          id="confirmPassword"
          type="password"
          label={$t('auth.confirmPassword')}
          bind:value={confirmPassword}
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
          {loading ? $t('common.loading') : $t('auth.registerButton')}
        </Button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          {$t('auth.hasAccount')}
          <a href="#/login" class="text-primary-600 hover:text-primary-700 font-medium">
            {$t('auth.login')}
          </a>
        </p>
      </div>
    </Card>
  </div>
</div>
