<template>
  <!-- 优先级：loading > error > empty > content -->
  <LoadingOverlay v-if="loading" visible :message="loadingMessage" />
  <ErrorDisplay v-else-if="error" :error="error" :retry="retry" />
  <div v-else-if="empty" class="state-wrapper__empty">
    <slot name="empty">
      <div class="state-wrapper__empty-icon">—</div>
      <p class="state-wrapper__empty-text">{{ emptyDescription || '暂无数据' }}</p>
    </slot>
  </div>
  <slot v-else />
</template>

<script setup lang="ts">
import LoadingOverlay from './LoadingOverlay.vue'
import ErrorDisplay from './ErrorDisplay.vue'

defineProps<{
  loading: boolean
  error: string | null
  empty: boolean
  emptyDescription?: string
  loadingMessage?: string
  retry?: () => void
}>()
</script>

<style scoped>
.state-wrapper__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 16px;
  text-align: center;
}

.state-wrapper__empty-icon {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 12px;
}

.state-wrapper__empty-text {
  font-size: 15px;
  color: #909399;
  margin: 0;
}
</style>
