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

// 初始化主题
const { theme } = useTheme()
onMounted(() => {
  const root = document.documentElement
  if (theme.value === 'dark') {
    root.setAttribute('data-theme', 'dark')
    root.classList.add('dark')
  } else {
    root.setAttribute('data-theme', 'light')
    root.classList.remove('dark')
  }
})
</script>
