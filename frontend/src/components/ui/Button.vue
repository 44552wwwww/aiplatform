<template>
  <button
    :class="cn(
      'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-[var(--radius)] text-sm font-medium transition-colors',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ring)] focus-visible:ring-offset-2',
      'disabled:pointer-events-none disabled:opacity-50',
      {
        'bg-[var(--color-primary)] text-[var(--color-primary-foreground)] hover:opacity-90': variant === 'default',
        'bg-[var(--color-destructive)] text-[var(--color-destructive-foreground)] hover:opacity-90': variant === 'destructive',
        'border border-[var(--color-border)] bg-[var(--color-background)] hover:bg-[var(--color-accent)]': variant === 'outline',
        'hover:bg-[var(--color-accent)] hover:text-[var(--color-accent-foreground)]': variant === 'ghost',
        'text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)]': variant === 'link',
        'h-9 px-4 py-2': size === 'default',
        'h-8 rounded-md px-3 text-xs': size === 'sm',
        'h-11 rounded-md px-8 text-base': size === 'lg',
        'h-9 w-9 p-0': size === 'icon',
      },
      className,
    )"
    :disabled="disabled"
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
  className?: string
}>(), {
  variant: 'default',
  size: 'default',
  disabled: false,
  className: '',
})
</script>
