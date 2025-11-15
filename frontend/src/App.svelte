<script lang="ts">
  import { onMount } from 'svelte';

  let apiStatus = 'Checking...';
  let apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  onMount(async () => {
    try {
      const response = await fetch(apiUrl);
      const data = await response.json();
      apiStatus = `✅ Connected: ${data.message}`;
    } catch (error) {
      apiStatus = '❌ Backend not reachable';
      console.error('API connection error:', error);
    }
  });
</script>

<main class="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-gray-900 dark:to-gray-800">
  <div class="container mx-auto px-4 py-16">
    <div class="max-w-4xl mx-auto text-center">
      <h1 class="text-6xl font-bold text-primary-600 dark:text-primary-400 mb-4">
        FeelInk 🎯
      </h1>

      <p class="text-2xl text-gray-700 dark:text-gray-300 mb-8">
        Mental Health & Wellness Tracking PWA
      </p>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8 mb-8">
        <h2 class="text-3xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
          STAGE 0: Infrastructure ✅
        </h2>

        <div class="space-y-4 text-left">
          <div class="flex items-center space-x-2">
            <span class="text-green-500 text-2xl">✓</span>
            <span class="text-gray-700 dark:text-gray-300">Frontend: Svelte + TypeScript + Vite</span>
          </div>

          <div class="flex items-center space-x-2">
            <span class="text-green-500 text-2xl">✓</span>
            <span class="text-gray-700 dark:text-gray-300">Backend: FastAPI + Python</span>
          </div>

          <div class="flex items-center space-x-2">
            <span class="text-green-500 text-2xl">✓</span>
            <span class="text-gray-700 dark:text-gray-300">Database: PostgreSQL + Redis</span>
          </div>

          <div class="flex items-center space-x-2">
            <span class="text-green-500 text-2xl">✓</span>
            <span class="text-gray-700 dark:text-gray-300">Styling: Tailwind CSS</span>
          </div>

          <div class="flex items-center space-x-2">
            <span class="text-green-500 text-2xl">✓</span>
            <span class="text-gray-700 dark:text-gray-300">PWA: Service Worker Ready</span>
          </div>
        </div>

        <div class="mt-8 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
          <p class="text-lg font-medium text-gray-800 dark:text-gray-200">
            Backend Status: <span class="font-bold">{apiStatus}</span>
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 class="text-xl font-semibold text-primary-600 dark:text-primary-400 mb-2">
            Track
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            Log daily metrics, mood, and activities
          </p>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 class="text-xl font-semibold text-primary-600 dark:text-primary-400 mb-2">
            Analyze
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            Discover correlations and patterns
          </p>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 class="text-xl font-semibold text-primary-600 dark:text-primary-400 mb-2">
            Improve
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            Make informed decisions for better wellbeing
          </p>
        </div>
      </div>
    </div>
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
</style>
