<template>
  <div v-if="error" class="error-display">
    <div class="error-display__card">
      <div class="error-display__icon">!</div>
      <h3 class="error-display__title">加载失败</h3>
      <p class="error-display__message">{{ error }}</p>
      <button v-if="retry" class="error-display__retry" @click="retry">
        重试
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  error: string | null
  retry?: () => void
}>()
</script>

<style scoped>
.error-display {
  display: flex;
  justify-content: center;
  padding: 48px 16px;
}

.error-display__card {
  text-align: center;
  max-width: 400px;
}

.error-display__icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: var(--el-color-danger-light-9, #fef0f0);
  color: var(--el-color-danger, #f56c6c);
  font-size: 28px;
  font-weight: 700;
  line-height: 56px;
}

.error-display__title {
  font-size: 18px;
  color: #303133;
  margin: 0 0 8px;
}

.error-display__message {
  font-size: 14px;
  color: #909399;
  margin: 0 0 20px;
  word-break: break-word;
}

.error-display__retry {
  display: inline-block;
  padding: 8px 24px;
  border: 1px solid var(--el-color-primary, #409eff);
  border-radius: 6px;
  background: #fff;
  color: var(--el-color-primary, #409eff);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.error-display__retry:hover {
  background: var(--el-color-primary, #409eff);
  color: #fff;
}
</style>
