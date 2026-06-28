<template>
  <AppLayout>
    <div class="report-header">
      <div>
        <button class="back-link" @click="$router.push('/history')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" />
          </svg>
          返回列表
        </button>
        <h1 class="report-title">{{ report?.title || '报告详情' }}</h1>
        <div class="report-meta">
          <span>📅 {{ formatTime(report?.created_at || '') }}</span>
          <span class="report-tag">{{ report?.skill_id }}</span>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button class="btn btn-secondary" @click="copyHTML">
          {{ copied ? '✓ 已复制' : '复制 HTML' }}
        </button>
        <button class="btn btn-secondary" @click="printReport">打印</button>
        <button class="btn btn-secondary" @click="toggleFullscreen">
          {{ fullscreen ? '退出全屏' : '全屏' }}
        </button>
      </div>
    </div>

    <!-- Loading / Error / Empty -->
    <div v-if="loading" class="empty-state">
      <span class="loading-spinner" style="margin: 0 auto 1rem;" />
      <div class="empty-state-desc">报告加载中...</div>
    </div>
    <div v-else-if="error" class="empty-state">
      <div class="empty-state-icon">⚠️</div>
      <div class="empty-state-desc">{{ error }}</div>
      <button class="btn btn-primary" @click="fetchReport">重试</button>
    </div>
    <div v-else-if="!report" class="empty-state">
      <div class="empty-state-icon">📄</div>
      <div class="empty-state-title">报告不存在</div>
    </div>

    <!-- Report iframe -->
    <div v-else class="report-container glass-card">
      <div v-if="iframeLoading" class="flex items-center justify-center py-24">
        <span class="loading-spinner" style="width:24px;height:24px;margin-right:8px;" />
        <span class="text-sm text-[var(--text-muted)]">报告渲染中...</span>
      </div>
      <iframe
        ref="iframeRef"
        :srcdoc="report.html || ''"
        :class="['w-full border-0 transition-opacity duration-300', fullscreen ? 'fixed inset-0 z-50 h-full' : 'min-h-[80vh]', iframeLoading ? 'opacity-0' : 'opacity-100']"
        sandbox="allow-same-origin"
        title="分析报告"
        @load="iframeLoading = false"
      />
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import { reportApi, type ReportDetail } from '@/api/report'
import { ApiError } from '@/api/client'
import { useToast } from '@/composables/useToast'

const route = useRoute()
const toast = useToast()
const report = ref<ReportDetail | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const iframeLoading = ref(true)
const copied = ref(false)
const fullscreen = ref(false)
const iframeRef = ref<HTMLIFrameElement>()

function toggleFullscreen() { fullscreen.value = !fullscreen.value }

function formatTime(ts: string): string {
  if (!ts) return '-'
  return new Date(ts).toLocaleString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

async function copyHTML() {
  if (!report.value?.html) return
  try { await navigator.clipboard.writeText(report.value.html); copied.value = true; toast.success('HTML 已复制'); setTimeout(() => { copied.value = false }, 2500) } catch { toast.error('复制失败') }
}

function printReport() { iframeRef.value?.contentWindow?.print() }

async function fetchReport() {
  loading.value = true; error.value = null
  try {
    const id = Number(route.params.reportId)
    report.value = await reportApi.detail(id)
    iframeLoading.value = true
  } catch (e: unknown) {
    report.value = null
    if (!(e instanceof ApiError && e.status === 404)) { error.value = (e as Error).message || '加载失败' }
  } finally { loading.value = false }
}

function onKeydown(e: KeyboardEvent) { if (e.key === 'Escape' && fullscreen.value) fullscreen.value = false }

onMounted(() => { fetchReport(); document.addEventListener('keydown', onKeydown) })
onUnmounted(() => { document.removeEventListener('keydown', onKeydown) })
</script>
