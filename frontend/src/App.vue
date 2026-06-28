<template>
  <div id="app">
    <AppHeader />
    <main>
      <router-view />
    </main>
    <ToastProvider />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
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

<style scoped>
main {
  min-height: calc(100vh - 60px);
}
</style>
