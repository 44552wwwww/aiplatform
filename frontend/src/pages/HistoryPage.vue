<template>
  <AppLayout>
    <div class="page-header">
      <h1 class="page-title">我的报告</h1>
      <p class="page-desc">管理和查看你的 AI 生成报告</p>
    </div>

    <!-- 搜索 -->
    <div class="search-bar" style="max-width: 360px; margin-bottom: var(--spacing-xl);">
      <span class="search-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      </span>
      <input v-model="search" type="text" class="search-input" placeholder="搜索报告..." />
    </div>

    <!-- Loading / Error -->
    <div v-if="loading" class="empty-state">
      <span class="loading-spinner" style="margin: 0 auto 1rem;" />
      <div class="empty-state-desc">加载中...</div>
    </div>
    <div v-else-if="error" class="empty-state">
      <div class="empty-state-icon">⚠️</div>
      <div class="empty-state-desc">{{ error }}</div>
      <button class="btn btn-primary" @click="fetchList">重试</button>
    </div>
    <div v-else-if="filteredReports.length === 0" class="panel glass-card">
      <div class="empty-state">
        <div class="empty-state-icon">📄</div>
        <div class="empty-state-title">{{ search ? '没有匹配的报告' : '暂无报告' }}</div>
        <div class="empty-state-desc">{{ search ? '尝试其他关键词' : '去 Skills 页面生成第一份报告吧' }}</div>
        <router-link v-if="!search" to="/skills" class="btn btn-primary">浏览 Skills</router-link>
      </div>
    </div>

    <!-- Report List -->
    <div v-else class="space-y-3">
      <div v-for="(r, i) in filteredReports" :key="r.id" class="panel glass-card flex items-center justify-between">
        <div class="min-w-0 flex-1">
          <div class="flex items-center gap-3">
            <span style="font-family: monospace; font-size: 0.75rem; color: var(--text-muted);">#{{ i + 1 }}</span>
            <span class="truncate text-sm font-semibold">{{ r.title }}</span>
            <span class="skill-badge">{{ r.skill_id }}</span>
          </div>
          <div class="mt-1" style="margin-left: 2.25rem; font-size: 0.75rem; color: var(--text-muted);">{{ formatTime(r.created_at) }}</div>
        </div>
        <div class="flex items-center gap-1" style="margin-left: 1rem;">
          <button class="btn btn-ghost text-sm" @click="$router.push(`/report/${r.id}`)">查看</button>
          <button class="btn btn-ghost text-sm" style="color: var(--color-destructive);" @click="handleDelete(r)">删除</button>
        </div>
      </div>
    </div>

    <!-- 删除确认弹窗 -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
        <div class="glass-card" style="width: 100%; max-width: 400px; padding: var(--spacing-xl);">
          <h3 class="text-lg font-semibold mb-4">确认删除</h3>
          <p class="text-sm text-[var(--text-secondary)] mb-6">确定要删除「{{ deleteTarget.title }}」吗？此操作不可撤销。</p>
          <div class="flex justify-end gap-3">
            <button class="btn btn-secondary" @click="deleteTarget = null">取消</button>
            <button class="btn btn-primary" :class="{ 'btn-loading': deleting }" :disabled="deleting" @click="confirmDelete" style="background: var(--color-destructive);">
              <span v-if="deleting" class="loading-spinner" />{{ deleting ? '删除中...' : '确认删除' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { reportApi, type ReportItem } from '@/api/report'
import { useToast } from '@/composables/useToast'

const toast = useToast()
const loading = ref(true)
const error = ref<string | null>(null)
const reports = ref<ReportItem[]>([])
const search = ref('')
const deleteTarget = ref<ReportItem | null>(null)
const deleting = ref(false)

const filteredReports = computed(() => {
  if (!search.value.trim()) return reports.value
  const q = search.value.toLowerCase()
  return reports.value.filter(r => r.title.toLowerCase().includes(q) || r.skill_id.toLowerCase().includes(q))
})

onMounted(() => { fetchList() })

async function fetchList() {
  loading.value = true; error.value = null
  try { const res = await reportApi.list(); reports.value = res.reports } catch (e: unknown) { error.value = (e as Error).message || '加载失败' } finally { loading.value = false }
}

function handleDelete(report: ReportItem) { deleteTarget.value = report }

async function confirmDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try { await reportApi.remove(deleteTarget.value.id); toast.success('报告已删除'); deleteTarget.value = null; await fetchList() } catch (e: unknown) { toast.error((e as Error).message || '删除失败') } finally { deleting.value = false }
}

function formatTime(ts: string): string {
  if (!ts) return '-'
  const d = new Date(ts)
  return d.toLocaleString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>
