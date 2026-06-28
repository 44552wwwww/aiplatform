<template>
  <button
    :class="cn(
      'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-medium transition-all duration-200',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ring)] focus-visible:ring-offset-2',
      'disabled:pointer-events-none disabled:opacity-50',
      'active:scale-[0.98]',
      {
        'bg-purple-600 text-white shadow-sm hover:bg-purple-700 hover:shadow-md': variant === 'default',
        'bg-red-600 text-white shadow-sm hover:bg-red-700': variant === 'destructive',
        'border border-[var(--color-border)] bg-[var(--color-card)] shadow-sm hover:bg-[var(--color-muted)] hover:shadow-md': variant === 'outline',
        'hover:bg-[var(--color-muted)] hover:text-[var(--color-foreground)]': variant === 'ghost',
        'text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] underline-offset-4 hover:underline': variant === 'link',
        'h-10 px-5 py-2': size === 'default',
        'h-8 rounded-lg px-3 text-xs': size === 'sm',
        'h-12 rounded-xl px-8 text-base': size === 'lg',
        'h-10 w-10 p-0': size === 'icon',
      },
      className,
    )"
    :disabled="disabled"
    :type="type"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { cn } from '@/lib/utils'

withDefaults(defineProps<{
  variant?: 'default' | 'destructive' | 'outline' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  className?: string
}>(), {
  variant: 'default',
  size: 'default',
  disabled: false,
  type: 'button',
  className: '',
})
</script>
