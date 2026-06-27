<template>
  <teleport to="body">
    <div v-if="visible" class="loading-overlay" role="alert" aria-busy="true">
      <div class="loading-overlay__content">
        <div class="loading-overlay__spinner">
          <span class="el-icon el-icon--loading">
            <svg viewBox="0 0 1024 1024" width="1em" height="1em" fill="currentColor">
              <path d="M512 64a32 32 0 0 1 32 32v192a32 32 0 1 1-64 0V96a32 32 0 0 1 32-32zm0 640a32 32 0 0 1 32 32v192a32 32 0 1 1-64 0V736a32 32 0 0 1 32-32zm448-192a32 32 0 0 1-32 32H736a32 32 0 1 1 0-64h192a32 32 0 0 1 32 32zm-640 0a32 32 0 0 1-32 32H96a32 32 0 1 1 0-64h192a32 32 0 0 1 32 32zM195.2 195.2a32 32 0 0 1 45.248 0L376.32 331.008a32 32 0 1 1-45.248 45.248L195.2 240.448a32 32 0 0 1 0-45.248zm452.544 452.544a32 32 0 0 1 45.248 0L828.8 787.648a32 32 0 1 1-45.248 45.248L647.744 697.088a32 32 0 0 1 0-45.248zM828.8 195.264a32 32 0 0 1 0 45.184L697.088 376.32a32 32 0 1 1-45.248-45.248l135.808-135.808a32 32 0 0 1 45.248 0zM240.448 647.744a32 32 0 0 1 0 45.248L104.64 828.8a32 32 0 1 1-45.248-45.248l135.808-135.808a32 32 0 0 1 45.248 0z"/>
            </svg>
          </span>
        </div>
        <p v-if="message" class="loading-overlay__text">{{ message }}</p>
      </div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  visible?: boolean
  message?: string
}>(), {
  visible: true,
})
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(4px);
}

.loading-overlay__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-overlay__spinner {
  font-size: 40px;
  color: var(--el-color-primary, #409eff);
  animation: spin 1s linear infinite;
}

.loading-overlay__text {
  font-size: 15px;
  color: #606266;
  margin: 0;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
