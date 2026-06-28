<template>
  <div
    :class="cn(
      'rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] text-[var(--color-card-foreground)] shadow-sm',
      className,
    )"
  >
    <div v-if="$slots.header || title" class="border-b border-[var(--color-border)] p-6 pb-4">
      <slot name="header">
        <h3 v-if="title" class="font-semibold leading-none tracking-tight">{{ title }}</h3>
        <p v-if="description" class="mt-1 text-sm text-[var(--color-muted-foreground)]">{{ description }}</p>
      </slot>
    </div>
    <div v-if="$slots.default" class="p-6">
      <slot />
    </div>
    <div v-if="$slots.footer" class="border-t border-[var(--color-border)] px-6 py-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { cn } from '@/lib/utils'

withDefaults(defineProps<{
  title?: string
  description?: string
  className?: string
}>(), { className: '' })
</script>
