<template>
  <div
    :class="cn(
      'rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] text-[var(--color-card-foreground)] shadow-sm',
      className,
    )"
  >
    <div v-if="$slots.header || title" :class="cn('flex flex-col gap-1.5 p-6 pb-0', headerClass)">
      <slot name="header">
        <h3 v-if="title" class="font-semibold leading-none tracking-tight">{{ title }}</h3>
        <p v-if="description" class="text-sm text-[var(--color-muted-foreground)]">{{ description }}</p>
      </slot>
    </div>
    <div v-if="$slots.default" :class="cn('p-6', contentClass)">
      <slot />
    </div>
    <div v-if="$slots.footer" :class="cn('flex items-center p-6 pt-0', footerClass)">
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
  headerClass?: string
  contentClass?: string
  footerClass?: string
}>(), {
  className: '',
  headerClass: '',
  contentClass: '',
  footerClass: '',
})
</script>
