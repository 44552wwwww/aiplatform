<template>
  <teleport to="body">
    <div class="pointer-events-none fixed bottom-6 right-6 z-[9999] flex flex-col gap-2">
      <div v-for="t in toasts" :key="t.id"
        class="pointer-events-auto flex items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium shadow-lg animate-in slide-in-from-right"
        :class="{ 'bg-emerald-600 text-white': t.type === 'success', 'bg-red-600 text-white': t.type === 'error', 'bg-amber-500 text-white': t.type === 'warning', 'bg-[var(--color-foreground)] text-[var(--color-background)]': t.type === 'info' }">
        <CheckCircle v-if="t.type === 'success'" class="h-4 w-4" />
        <AlertCircle v-else-if="t.type === 'error'" class="h-4 w-4" />
        <Info v-else class="h-4 w-4" />
        {{ t.message }}
      </div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { CheckCircle, AlertCircle, Info } from 'lucide-vue-next'
import { useToast } from '@/composables/useToast'
const { toasts } = useToast()
</script>
