<script lang="ts">
  export let variant: 'primary' | 'secondary' | 'danger' | 'ghost' | 'gradient' = 'primary';
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let disabled: boolean = false;
  export let type: 'button' | 'submit' | 'reset' = 'button';
  export let fullWidth: boolean = false;

  const baseClasses = 'font-medium rounded-xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98]';

  const variantClasses = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 shadow-soft hover:shadow-medium focus:ring-primary-500',
    secondary: 'bg-secondary-600 text-white hover:bg-secondary-700 shadow-soft hover:shadow-medium focus:ring-secondary-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 shadow-soft hover:shadow-medium focus:ring-red-500',
    ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:ring-gray-500',
    gradient: 'bg-gradient-primary text-white shadow-soft hover:shadow-glow focus:ring-primary-500'
  };

  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-2.5 text-base',
    lg: 'px-8 py-3.5 text-lg'
  };

  $: classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${fullWidth ? 'w-full' : ''}`;
</script>

<button {type} {disabled} class={classes} on:click>
  <slot />
</button>
