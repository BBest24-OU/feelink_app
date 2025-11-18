<script lang="ts">
  import Router from 'svelte-spa-router';
  import { wrap } from 'svelte-spa-router/wrap';
  import { onMount } from 'svelte';
  import { authActions, authStore, isAuthenticated } from './stores/user';
  import { initI18n } from './i18n';
  import { get } from 'svelte/store';

  // Pages
  import Login from './pages/Login.svelte';
  import Register from './pages/Register.svelte';
  import Dashboard from './pages/Dashboard.svelte';
  import Metrics from './pages/Metrics.svelte';
  import DailyLog from './pages/DailyLog.svelte';
  import Entries from './pages/Entries.svelte';
  import Insights from './pages/Insights.svelte';
  import Correlations from './pages/Correlations.svelte';
  import Profile from './pages/Profile.svelte';
  import Loading from './components/Loading.svelte';
  import Onboarding from './components/Onboarding.svelte';

  let ready = false;
  let showOnboarding = false;

  onMount(async () => {
    // Initialize i18n first
    await initI18n();

    // Try to load user profile if token exists but user is not already loaded
    const token = localStorage.getItem('access_token');
    const currentAuth = get(authStore);

    if (token && !currentAuth.user) {
      await authActions.loadProfile();
    }
    ready = true;

    // Check if onboarding is needed after loading profile
    checkOnboarding();
  });

  // Check if we should show onboarding
  function checkOnboarding() {
    const currentAuth = get(authStore);
    console.log('[ONBOARDING] Checking onboarding:', {
      isAuthenticated: currentAuth.isAuthenticated,
      hasUser: !!currentAuth.user,
      userName: currentAuth.user?.name,
      shouldShow: currentAuth.isAuthenticated && currentAuth.user && !currentAuth.user.name?.trim()
    });

    if (currentAuth.isAuthenticated && currentAuth.user && !currentAuth.user.name?.trim()) {
      console.log('[ONBOARDING] Showing onboarding modal');
      showOnboarding = true;
    }
  }

  // Subscribe to auth store changes to check onboarding
  authStore.subscribe((auth) => {
    if (ready && auth.isAuthenticated && auth.user && !auth.user.name?.trim() && !showOnboarding) {
      console.log('[ONBOARDING] Auth store changed, showing onboarding');
      showOnboarding = true;
    }
  });

  function handleOnboardingComplete() {
    showOnboarding = false;
  }

  // Routes configuration
  const routes = {
    '/': Login,
    '/login': Login,
    '/register': Register,
    '/dashboard': wrap({
      component: Dashboard,
      conditions: [(detail) => $isAuthenticated]
    }),
    '/metrics': wrap({
      component: Metrics,
      conditions: [(detail) => $isAuthenticated]
    }),
    '/log': wrap({
      component: DailyLog,
      conditions: [(detail) => $isAuthenticated]
    }),
    '/entries': wrap({
      component: Entries,
      conditions: [(detail) => $isAuthenticated]
    }),
    '/insights': wrap({
      component: Insights,
      conditions: [(detail) => $isAuthenticated]
    }),
    '/correlations': wrap({
      component: Correlations,
      conditions: [(detail) => $isAuthenticated]
    }),
    '/profile': wrap({
      component: Profile,
      conditions: [(detail) => $isAuthenticated]
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

  {#if showOnboarding}
    <Onboarding on:complete={handleOnboardingComplete} />
  {/if}
{/if}

<style>
  :global(html),
  :global(body) {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
  }

  :global(#app) {
    margin: 0;
    padding: 0;
    width: 100%;
  }
</style>
