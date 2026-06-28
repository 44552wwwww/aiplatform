<template>
  <div id="app" class="flex min-h-screen flex-col">
    <router-view class="flex-1" />
    <ToastProvider />
    <SignatureFooter />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import ToastProvider from '@/components/ui/ToastProvider.vue'
import SignatureFooter from '@/components/shared/SignatureFooter.vue'
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
