<template>
  <Teleport to="body">
    <div class="toast-container">
      <div v-for="t in toasts" :key="t.id" class="toast" :class="t.type">
        <span class="toast-icon">{{ t.type === 'success' ? '✓' : t.type === 'error' ? '✕' : 'ℹ' }}</span>
        <span class="toast-message">{{ t.message }}</span>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToast } from '@/composables/useToast'
const { toasts } = useToast()
</script>
