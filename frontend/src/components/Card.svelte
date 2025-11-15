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

  $: classes = `bg-white rounded-lg shadow-md ${paddingClasses[padding]} ${hover ? 'hover:shadow-lg transition-shadow cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2' : ''}`;

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
