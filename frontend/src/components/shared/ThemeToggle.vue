<template>
  <button
    class="inline-flex h-9 w-9 items-center justify-center rounded-md text-[var(--color-muted-foreground)] hover:bg-[var(--color-accent)] hover:text-[var(--color-foreground)] transition-colors"
    @click="toggle"
    :title="theme === 'dark' ? '切换亮色模式' : '切换深色模式'"
  >
    <Sun v-if="theme === 'dark'" class="h-5 w-5" />
    <Moon v-else class="h-5 w-5" />
  </button>
</template>

<script setup lang="ts">
import { Sun, Moon } from 'lucide-vue-next'
import { useTheme } from '@/composables/useTheme'

const { theme, toggle } = useTheme()
</script>
