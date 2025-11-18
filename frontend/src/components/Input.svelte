<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let type: string = 'text';
  export let value: string = '';
  export let placeholder: string = '';
  export let label: string = '';
  export let error: string = '';
  export let disabled: boolean = false;
  export let required: boolean = false;
  export let id: string = '';

  const dispatch = createEventDispatcher();
  const inputClasses = 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed';
  const errorClasses = 'border-red-500 focus:ring-red-500';

  function handleInput(e: Event) {
    const target = e.currentTarget as HTMLInputElement;
    value = target.value;
    dispatch('input', value);
  }
</script>

<div class="w-full">
  {#if label}
    <label for={id} class="block text-sm font-medium text-gray-700 mb-1">
      {label}
      {#if required}<span class="text-red-500">*</span>{/if}
    </label>
  {/if}

  <input
    {id}
    {type}
    {placeholder}
    {disabled}
    {required}
    {value}
    class="{inputClasses} {error ? errorClasses : 'border-gray-300'}"
    on:input={handleInput}
    on:blur
    on:focus
  />

  {#if error}
    <p class="mt-1 text-sm text-red-600">{error}</p>
  {/if}
</div>
