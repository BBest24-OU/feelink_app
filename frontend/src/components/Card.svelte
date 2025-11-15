<script lang="ts">
  export let padding: 'none' | 'sm' | 'md' | 'lg' = 'md';
  export let hover: boolean = false;

  const paddingClasses = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8'
  };

  $: classes = `bg-white rounded-lg shadow-md ${paddingClasses[padding]} ${hover ? 'hover:shadow-lg transition-shadow cursor-pointer' : ''}`;
</script>

<div class={classes} on:click>
  <slot />
</div>
