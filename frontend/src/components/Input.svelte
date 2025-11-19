<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { Eye, EyeOff } from 'lucide-svelte';

  export let type: string = 'text';
  export let value: string = '';
  export let placeholder: string = '';
  export let label: string = '';
  export let error: string = '';
  export let disabled: boolean = false;
  export let required: boolean = false;
  export let id: string = '';
  export let autofocus: boolean = false;
  export let readonly: boolean = false;

  const dispatch = createEventDispatcher();

  let showPassword = false;
  let inputType = type;

  $: isPasswordField = type === 'password';
  $: inputType = isPasswordField && showPassword ? 'text' : type;

  const inputClasses = 'w-full px-4 py-2 border rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-transparent disabled:bg-gray-100 dark:disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors';
  const errorClasses = 'border-red-500 dark:border-red-400 focus:ring-red-500 dark:focus:ring-red-400';

  function handleInput(e: Event) {
    const target = e.currentTarget as HTMLInputElement;
    value = target.value;
    dispatch('input', value);
  }

  function togglePasswordVisibility() {
    showPassword = !showPassword;
  }
</script>

<div class="w-full">
  {#if label}
    <label for={id} class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1 text-left">
      {label}
      {#if required}<span class="text-red-500 dark:text-red-400">*</span>{/if}
    </label>
  {/if}

  <div class="relative">
    <input
      {id}
      type={inputType}
      {placeholder}
      {disabled}
      {required}
      {readonly}
      {value}
      class="{inputClasses} {error ? errorClasses : 'border-gray-300 dark:border-gray-600'} {isPasswordField ? 'pr-10' : ''}"
      on:input={handleInput}
      on:blur
      on:focus
      autofocus={autofocus}
    />

    {#if isPasswordField}
      <button
        type="button"
        on:click={togglePasswordVisibility}
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 focus:outline-none focus:text-gray-700 dark:focus:text-gray-300"
        tabindex="-1"
        aria-label={showPassword ? 'Hide password' : 'Show password'}
      >
        {#if showPassword}
          <EyeOff size={20} />
        {:else}
          <Eye size={20} />
        {/if}
      </button>
    {/if}
  </div>

  {#if error}
    <p class="mt-1 text-sm text-red-600 dark:text-red-400">{error}</p>
  {/if}
</div>
