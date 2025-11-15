<script lang="ts">
  import Router from 'svelte-spa-router';
  import { wrap } from 'svelte-spa-router/wrap';
  import { onMount } from 'svelte';
  import { authActions, isAuthenticated } from './stores/user';
  import { initI18n } from './i18n';

  // Pages
  import Login from './pages/Login.svelte';
  import Register from './pages/Register.svelte';
  import Dashboard from './pages/Dashboard.svelte';
  import Loading from './components/Loading.svelte';

  // Initialize i18n
  initI18n();

  let ready = false;

  onMount(async () => {
    // Try to load user profile if token exists
    const token = localStorage.getItem('access_token');
    if (token) {
      await authActions.loadProfile();
    }
    ready = true;
  });

  // Routes configuration
  const routes = {
    '/': Login,
    '/login': Login,
    '/register': Register,
    '/dashboard': wrap({
      component: Dashboard,
      conditions: [
        (detail) => {
          return $isAuthenticated;
        }
      ]
    }),
  };

  function conditionsFailed(event: any) {
    // Redirect to login if not authenticated
    window.location.hash = '/login';
  }
</script>

{#if !ready}
  <Loading text="Loading FeelInk..." />
{:else}
  <Router {routes} on:conditionsFailed={conditionsFailed} />
{/if}

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
</style>
