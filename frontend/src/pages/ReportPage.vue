<template>
  <div class="page-container">
    <div class="page-header">
      <el-button text @click="$router.push('/history')">← 返回列表</el-button>
      <h1>{{ report?.title || '报告详情' }}</h1>
    </div>

    <StateWrapper
      :loading="loading"
      :error="error"
      :empty="!loading && !report && !error"
      empty-description="报告不存在"
      :retry="fetchReport"
    >
      <div v-if="report" class="report-wrapper">
        <div v-if="iframeLoading" class="report-loading">
          报告渲染中...
        </div>
        <iframe
          :srcdoc="report.html || ''"
          class="report-frame"
          :class="{ 'report-frame--loaded': !iframeLoading }"
          sandbox="allow-same-origin"
          title="分析报告"
          @load="iframeLoading = false"
        />
      </div>
    </StateWrapper>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { reportApi, type ReportDetail } from '@/api/report'
import { ApiError } from '@/api/client'
import StateWrapper from '@/components/StateWrapper.vue'

const route = useRoute()
const report = ref<ReportDetail | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const iframeLoading = ref(true)

onMounted(() => {
  fetchReport()
})

async function fetchReport() {
  loading.value = true
  error.value = null
  try {
    const id = Number(route.params.reportId)
    report.value = await reportApi.detail(id)
    iframeLoading.value = true
  } catch (e: unknown) {
    report.value = null
    if (e instanceof ApiError && e.status === 404) {
      // 真正的 404 — 报告不存在
      error.value = null
    } else {
      error.value = (e as Error).message || '加载报告失败'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.report-wrapper {
  position: relative;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
}
.report-loading {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 14px;
  background: #fff;
  z-index: 1;
}
.report-frame {
  width: 100%;
  min-height: 80vh;
  border: none;
  opacity: 0;
  transition: opacity 0.3s;
}
.report-frame--loaded {
  opacity: 1;
}
</style>
