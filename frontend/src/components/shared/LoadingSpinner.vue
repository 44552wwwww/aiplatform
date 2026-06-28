<template>
  <div :class="cn('flex items-center justify-center', className)">
    <Loader2 :class="cn('animate-spin text-[var(--color-muted-foreground)]', sizeClass)" />
  </div>
</template>

<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import { cn } from '@/lib/utils'
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  size?: 'sm' | 'default' | 'lg'
  className?: string
}>(), {
  size: 'default',
  className: '',
})

const sizeClass = computed(() => ({
  sm: 'h-4 w-4',
  default: 'h-8 w-8',
  lg: 'h-12 w-12',
}[props.size]))
</script>
