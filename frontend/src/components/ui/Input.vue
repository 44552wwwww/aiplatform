<template>
  <input
    :class="cn(
      'flex h-9 w-full rounded-[var(--radius)] border border-[var(--color-border)] bg-[var(--color-background)] px-3 py-1 text-sm text-[var(--color-foreground)] shadow-sm transition-colors',
      'file:border-0 file:bg-transparent file:text-sm file:font-medium',
      'placeholder:text-[var(--color-muted-foreground)]',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-ring)] focus-visible:ring-offset-1',
      'disabled:cursor-not-allowed disabled:opacity-50',
      error && 'border-[var(--color-destructive)] focus-visible:ring-[var(--color-destructive)]',
      className,
    )"
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>

<script setup lang="ts">
import { cn } from '@/lib/utils'

withDefaults(defineProps<{
  modelValue?: string | number
  type?: string
  placeholder?: string
  disabled?: boolean
  error?: boolean
  className?: string
}>(), {
  type: 'text',
  disabled: false,
  error: false,
  className: '',
})

defineEmits<{
  'update:modelValue': [value: string | number]
}>()
</script>
