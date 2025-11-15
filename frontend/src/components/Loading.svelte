<script lang="ts">
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let text: string = 'Loading...';

  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };
</script>

<div class="flex flex-col items-center justify-center p-8">
  <div class="{sizes[size]} border-4 border-gray-200 border-t-primary-600 rounded-full animate-spin"></div>
  {#if text}
    <p class="mt-4 text-gray-600">{text}</p>
  {/if}
</div>
