<script lang="ts">
  export let padding: 'none' | 'sm' | 'md' | 'lg' = 'md';
  export let hover: boolean = false;
  export let ariaLabel: string | undefined = undefined;

  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };

  $: classes = `
    bg-white dark:bg-gray-800
    border border-gray-200 dark:border-gray-700
    rounded-lg
    ${paddingClasses[padding]}
    ${hover ? 'hover:border-gray-300 dark:hover:border-gray-600 cursor-pointer transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:ring-offset-2 dark:focus:ring-offset-gray-900' : ''}
  `.trim();

  function handleKeyPress(event: KeyboardEvent) {
    if (hover && (event.key === 'Enter' || event.key === ' ')) {
      event.preventDefault();
      (event.target as HTMLElement).click();
    }
  }
</script>

<div
  class={classes}
  on:click
  on:keypress={handleKeyPress}
  tabindex={hover ? 0 : undefined}
  role={hover ? 'button' : undefined}
  aria-label={ariaLabel}
>
  <slot />
</div>
