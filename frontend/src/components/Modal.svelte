<script lang="ts">
  export let onClose: (() => void) | undefined = undefined;
  export let open: boolean = false;
  export let title: string = '';
  export let size: 'sm' | 'md' | 'lg' = 'md';

  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-2xl',
    lg: 'max-w-4xl'
  };

  function handleClose() {
    if (onClose) {
      onClose();
    } else {
      open = false;
    }
  }

  function handleBackdropClick(e: MouseEvent) {
    if (e.target === e.currentTarget) {
      handleClose();
    }
  }
</script>

{#if open}
<div
  class="fixed inset-0 z-50 overflow-y-auto bg-black bg-opacity-50 flex items-center justify-center p-4"
  on:click={handleBackdropClick}
  on:keydown={(e) => e.key === 'Escape' && handleClose()}
  role="dialog"
  aria-modal="true"
>
  <div class="bg-white rounded-lg shadow-xl {sizes[size]} w-full">
    <div class="flex items-center justify-between p-6 border-b border-gray-200">
      <h2 class="text-2xl font-bold text-gray-800">
        <slot name="title">{title}</slot>
      </h2>
      <button
        on:click={handleClose}
        class="text-gray-400 hover:text-gray-600 transition-colors"
        aria-label="Close modal"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    <div class="p-6">
      <slot name="content">
        <slot />
      </slot>
    </div>
    <div class="flex items-center justify-end gap-3 p-6 border-t border-gray-200">
      <slot name="actions" />
    </div>
  </div>
</div>
{/if}
