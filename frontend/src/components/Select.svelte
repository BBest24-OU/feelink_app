<script lang="ts">
  export let value: string = '';
  export let label: string = '';
  export let options: Array<{ value: string; label: string }> = [];
  export let error: string = '';
  export let disabled: boolean = false;
  export let required: boolean = false;
  export let id: string = '';

  const selectClasses = 'w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-transparent disabled:bg-gray-100 dark:disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors';
  const errorClasses = 'border-red-500 dark:border-red-400 focus:ring-red-500 dark:focus:ring-red-400';
</script>

<div class="w-full">
  {#if label}
    <label for={id} class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {label}
      {#if required}<span class="text-red-500 dark:text-red-400">*</span>{/if}
    </label>
  {/if}

  <select
    {id}
    {disabled}
    {required}
    bind:value
    class="{selectClasses} {error ? errorClasses : 'border-gray-300 dark:border-gray-600'}"
    on:change
  >
    <option value="">Select...</option>
    {#each options as option}
      <option value={option.value}>{option.label}</option>
    {/each}
  </select>

  {#if error}
    <p class="mt-1 text-sm text-red-600 dark:text-red-400">{error}</p>
  {/if}
</div>
