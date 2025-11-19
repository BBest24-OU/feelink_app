<script lang="ts">
  export let padding: 'none' | 'sm' | 'md' | 'lg' = 'md';
  export let hover: boolean = false;
  export let ariaLabel: string | undefined = undefined;
  export let gradient: boolean = false;
  export let animate: boolean = true;

  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };

  $: classes = `
    bg-white rounded-2xl shadow-soft border border-gray-100
    ${paddingClasses[padding]}
    ${hover ? 'hover:shadow-medium hover:border-gray-200 hover:-translate-y-0.5 transition-all duration-300 cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2' : 'transition-all duration-200'}
    ${gradient ? 'bg-gradient-to-br from-white via-white to-primary-50/30' : ''}
    ${animate ? 'animate-fade-in' : ''}
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
