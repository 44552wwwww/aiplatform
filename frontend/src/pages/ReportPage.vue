<template>
  <AppLayout>
    <div class="mb-6 flex flex-wrap items-center justify-between gap-3">
      <button class="inline-flex items-center gap-1.5 text-sm text-[var(--color-muted-foreground)] transition-colors hover:text-[var(--color-foreground)]" @click="$router.push('/history')"><ArrowLeft class="h-4 w-4" />返回列表</button>
      <div class="flex items-center gap-2">
        <Button variant="outline" size="sm" @click="copyHTML"><Copy v-if="!copied" class="h-4 w-4" /><Check v-else class="h-4 w-4 text-emerald-500" />{{ copied ? '已复制' : '复制 HTML' }}</Button>
        <Button variant="outline" size="sm" @click="printReport"><Printer class="h-4 w-4" /></Button>
        <Button variant="outline" size="sm" @click="toggleFullscreen"><Maximize class="h-4 w-4" /></Button>
      </div>
    </div>

    <StateWrapper :loading="loading" :error="error" :empty="!report && !loading && !error" empty-description="报告不存在" :retry="fetchReport">
      <div v-if="report" class="overflow-hidden rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] shadow-sm">
        <div class="border-b border-[var(--color-border)] px-6 py-4">
          <h1 class="text-lg font-semibold">{{ report.title }}</h1>
          <div class="mt-1.5 flex flex-wrap items-center gap-3 text-xs text-[var(--color-muted-foreground)]">
            <span class="rounded-full bg-purple-50 px-2 py-0.5 font-medium text-purple-700 dark:bg-purple-950 dark:text-purple-300">{{ report.skill_id }}</span>
            <span>{{ formatTime(report.created_at) }}</span>
          </div>
        </div>
        <div v-if="iframeLoading" class="flex items-center justify-center py-24"><Loader2 class="h-6 w-6 animate-spin text-[var(--color-muted-foreground)]" /><span class="ml-2 text-sm text-[var(--color-muted-foreground)]">报告渲染中...</span></div>
        <div :class="['relative', { 'min-h-[80vh]': !fullscreen }]">
          <iframe ref="iframeRef" :srcdoc="report.html || ''"
            :class="['w-full border-0 transition-opacity duration-300', fullscreen ? 'fixed inset-0 z-50 h-full bg-white dark:bg-[#0a0a0f]' : 'min-h-[80vh]', iframeLoading ? 'opacity-0' : 'opacity-100']"
            sandbox="allow-same-origin" title="分析报告" @load="iframeLoading = false" />
        </div>
        <div v-if="fullscreen" class="fixed right-4 top-4 z-[60]"><Button variant="outline" size="sm" @click="toggleFullscreen"><Minimize class="h-4 w-4" /></Button></div>
      </div>
    </StateWrapper>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, Copy, Check, Printer, Maximize, Minimize, Loader2 } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
import Button from '@/components/ui/Button.vue'
import StateWrapper from '@/components/shared/StateWrapper.vue'
import { reportApi, type ReportDetail } from '@/api/report'
import { ApiError } from '@/api/client'
import { useToast } from '@/composables/useToast'
const route = useRoute(); const toast = useToast()
const report = ref<ReportDetail | null>(null); const loading = ref(true); const error = ref<string | null>(null); const iframeLoading = ref(true); const copied = ref(false); const fullscreen = ref(false); const iframeRef = ref<HTMLIFrameElement>()
function toggleFullscreen() { fullscreen.value = !fullscreen.value }
function formatTime(ts: string): string { if (!ts) return '-'; return new Date(ts).toLocaleString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }
async function copyHTML() { if (!report.value?.html) return; try { await navigator.clipboard.writeText(report.value.html); copied.value = true; toast.success('HTML 已复制'); setTimeout(() => { copied.value = false }, 2500) } catch { toast.error('复制失败') } }
function printReport() { iframeRef.value?.contentWindow?.print() }
async function fetchReport() { loading.value = true; error.value = null; try { const id = Number(route.params.reportId); report.value = await reportApi.detail(id); iframeLoading.value = true } catch (e: unknown) { report.value = null; if (!(e instanceof ApiError && e.status === 404)) { error.value = (e as Error).message || '加载失败' } } finally { loading.value = false } }
function onKeydown(e: KeyboardEvent) { if (e.key === 'Escape' && fullscreen.value) fullscreen.value = false }
onMounted(() => { fetchReport(); document.addEventListener('keydown', onKeydown) })
onUnmounted(() => { document.removeEventListener('keydown', onKeydown) })
</script>
