<template>
  <div class="flex flex-col items-center justify-center py-16 px-4 text-center">
    <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-muted)]">
      <Inbox class="h-7 w-7 text-[var(--color-muted-foreground)]" />
    </div>
    <p class="text-sm text-[var(--color-muted-foreground)]">{{ description || '暂无数据' }}</p>
  </div>
</template>

<script setup lang="ts">
import { Inbox } from 'lucide-vue-next'

defineProps<{
  description?: string
}>()
</script>
