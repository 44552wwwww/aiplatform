<template>
  <div v-if="message" class="flex flex-col items-center justify-center py-16 px-4 text-center">
    <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/20">
      <AlertCircle class="h-7 w-7 text-red-600 dark:text-red-400" />
    </div>
    <h3 class="mb-1 text-lg font-semibold">加载失败</h3>
    <p class="mb-5 max-w-sm text-sm text-[var(--color-muted-foreground)]">{{ message }}</p>
    <Button v-if="retry" variant="outline" @click="retry">重试</Button>
  </div>
</template>

<script setup lang="ts">
import { AlertCircle } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'

defineProps<{
  message: string | null
  retry?: () => void
}>()
</script>
