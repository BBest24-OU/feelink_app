<script lang="ts">
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let text: string = 'Loading...';

  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };
</script>

<div class="flex flex-col items-center justify-center p-8" role="status" aria-live="polite" aria-busy="true">
  <div class="{sizes[size]} border-4 border-gray-200 dark:border-gray-700 border-t-primary-600 dark:border-t-primary-500 rounded-full animate-spin" aria-hidden="true"></div>
  {#if text}
    <p class="mt-4 text-gray-600 dark:text-gray-400">{text}</p>
  {:else}
    <span class="sr-only">Loading...</span>
  {/if}
</div>

<style>
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
</style>
