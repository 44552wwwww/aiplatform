<template>
  <div id="app">
    <router-view />
    <ToastProvider />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import ToastProvider from '@/components/ui/ToastProvider.vue'
import { useTheme } from '@/composables/useTheme'

// Initialize theme on app mount
const { theme } = useTheme()
onMounted(() => {
  const root = document.documentElement
  if (theme.value === 'dark') {
    root.classList.add('dark')
  } else {
    root.classList.remove('dark')
  }
})
</script>

<style>
#app {
  min-height: 100vh;
}
</style>
