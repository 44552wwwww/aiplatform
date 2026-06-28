<template>
  <teleport to="body">
    <div class="fixed bottom-4 right-4 z-[9999] flex flex-col gap-2">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="cn(
          'rounded-[var(--radius)] px-4 py-3 text-sm font-medium shadow-lg animate-in slide-in-from-right',
          {
            'bg-emerald-600 text-white': toast.type === 'success',
            'bg-red-600 text-white': toast.type === 'error',
            'bg-amber-500 text-white': toast.type === 'warning',
            'bg-[var(--color-foreground)] text-[var(--color-background)]': toast.type === 'info',
          },
        )"
      >
        {{ toast.message }}
      </div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { useToast } from '@/composables/useToast'
import { cn } from '@/lib/utils'

const { toasts } = useToast()
</script>
