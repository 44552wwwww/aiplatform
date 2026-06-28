<template>
  <AppLayout>
    <div class="mb-8 flex items-end justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">我的报告</h1>
        <p class="mt-2 text-sm text-[var(--color-muted-foreground)]">管理和查看你的 AI 生成报告</p>
      </div>
    </div>

    <div class="mb-6"><div class="relative max-w-sm">
      <Search class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--color-muted-foreground)]" />
      <input v-model="search" type="text" placeholder="搜索报告..."
        class="h-11 w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-background)] pl-10 pr-4 text-sm placeholder:text-[var(--color-muted-foreground)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1" />
    </div></div>

    <StateWrapper :loading="loading" :error="error" :empty="filteredReports.length === 0 && !loading && !error"
      :empty-description="search ? '没有匹配的报告' : '暂无报告，去 Skills 页面生成第一份报告吧'" :retry="fetchList">
      <div class="space-y-3">
        <div v-for="(r, i) in filteredReports" :key="r.id"
          class="flex items-center justify-between rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] px-6 py-4 shadow-sm transition-shadow hover:shadow-md">
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-3">
              <span class="font-mono text-xs text-[var(--color-muted-foreground)]">#{{ i + 1 }}</span>
              <span class="truncate text-sm font-semibold">{{ r.title }}</span>
              <span class="rounded-full bg-purple-50 px-2 py-0.5 text-xs font-medium text-purple-700 dark:bg-purple-950 dark:text-purple-300">{{ r.skill_id }}</span>
            </div>
            <div class="mt-1 ml-9 text-xs text-[var(--color-muted-foreground)]">{{ formatTime(r.created_at) }}</div>
          </div>
          <div class="ml-4 flex items-center gap-1">
            <Button variant="ghost" size="sm" @click="$router.push(`/report/${r.id}`)">查看</Button>
            <Button variant="ghost" size="sm" class="text-red-500 hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-950" @click="handleDelete(r)">删除</Button>
          </div>
        </div>
      </div>
    </StateWrapper>

    <Teleport to="body">
      <div v-if="deleteTarget" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
        <div class="w-full max-w-sm rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-xl">
          <h3 class="text-lg font-semibold">确认删除</h3>
          <p class="mt-2 text-sm text-[var(--color-muted-foreground)]">确定要删除「{{ deleteTarget.title }}」吗？此操作不可撤销。</p>
          <div class="mt-6 flex justify-end gap-3">
            <Button variant="outline" @click="deleteTarget = null">取消</Button>
            <Button variant="destructive" :disabled="deleting" @click="confirmDelete"><Loader2 v-if="deleting" class="h-4 w-4 animate-spin" />{{ deleting ? '删除中...' : '确认删除' }}</Button>
          </div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Search, Loader2 } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
import StateWrapper from '@/components/shared/StateWrapper.vue'
import Button from '@/components/ui/Button.vue'
import { reportApi, type ReportItem } from '@/api/report'
import { useToast } from '@/composables/useToast'
const toast = useToast()
const loading = ref(true); const error = ref<string | null>(null); const reports = ref<ReportItem[]>([]); const search = ref(''); const deleteTarget = ref<ReportItem | null>(null); const deleting = ref(false)
const filteredReports = computed(() => { if (!search.value.trim()) return reports.value; const q = search.value.toLowerCase(); return reports.value.filter(r => r.title.toLowerCase().includes(q) || r.skill_id.toLowerCase().includes(q)) })
onMounted(() => { fetchList() })
async function fetchList() { loading.value = true; error.value = null; try { const res = await reportApi.list(); reports.value = res.reports } catch (e: unknown) { error.value = (e as Error).message || '加载失败' } finally { loading.value = false } }
function handleDelete(report: ReportItem) { deleteTarget.value = report }
async function confirmDelete() { if (!deleteTarget.value) return; deleting.value = true; try { await reportApi.remove(deleteTarget.value.id); toast.success('报告已删除'); deleteTarget.value = null; await fetchList() } catch (e: unknown) { toast.error((e as Error).message || '删除失败') } finally { deleting.value = false } }
function formatTime(ts: string): string { if (!ts) return '-'; const d = new Date(ts); return d.toLocaleString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }
</script>
