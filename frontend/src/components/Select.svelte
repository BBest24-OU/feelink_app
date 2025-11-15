<script lang="ts">
  export let value: string = '';
  export let label: string = '';
  export let options: Array<{ value: string; label: string }> = [];
  export let error: string = '';
  export let disabled: boolean = false;
  export let required: boolean = false;
  export let id: string = '';

  const selectClasses = 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed';
  const errorClasses = 'border-red-500 focus:ring-red-500';
</script>

<div class="w-full">
  {#if label}
    <label for={id} class="block text-sm font-medium text-gray-700 mb-1">
      {label}
      {#if required}<span class="text-red-500">*</span>{/if}
    </label>
  {/if}

  <select
    {id}
    {disabled}
    {required}
    bind:value
    class="{selectClasses} {error ? errorClasses : 'border-gray-300'}"
    on:change
  >
    <option value="">Select...</option>
    {#each options as option}
      <option value={option.value}>{option.label}</option>
    {/each}
  </select>

  {#if error}
    <p class="mt-1 text-sm text-red-600">{error}</p>
  {/if}
</div>
