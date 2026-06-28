<template>
  <AppLayout>
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">我的报告</h1>
        <p class="mt-1 text-sm text-[var(--color-muted-foreground)]">管理和查看你的 AI 生成报告</p>
      </div>
    </div>

    <!-- Search -->
    <div class="mb-6">
      <div class="relative max-w-sm">
        <Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--color-muted-foreground)]" />
        <input
          v-model="search"
          type="text"
          placeholder="搜索报告..."
          class="h-10 w-full rounded-[var(--radius)] border border-[var(--color-border)] bg-[var(--color-background)] pl-10 pr-4 text-sm placeholder:text-[var(--color-muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] transition-colors"
        />
      </div>
    </div>

    <StateWrapper
      :loading="loading"
      :error="error"
      :empty="filteredReports.length === 0 && !loading && !error"
      :empty-description="search ? '没有匹配的报告' : '暂无报告，去 Skills 页面生成第一份报告吧'"
      :retry="fetchList"
    >
      <!-- Table -->
      <div class="overflow-hidden rounded-xl border border-[var(--color-border)]">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-[var(--color-border)] bg-[var(--color-muted)]/50">
                <th class="px-4 py-3 text-left font-medium text-[var(--color-muted-foreground)]">#</th>
                <th class="px-4 py-3 text-left font-medium text-[var(--color-muted-foreground)]">标题</th>
                <th class="px-4 py-3 text-left font-medium text-[var(--color-muted-foreground)]">Skill</th>
                <th class="hidden px-4 py-3 text-left font-medium text-[var(--color-muted-foreground)] sm:table-cell">时间</th>
                <th class="px-4 py-3 text-right font-medium text-[var(--color-muted-foreground)]">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[var(--color-border)]">
              <tr
                v-for="(report, i) in filteredReports"
                :key="report.id"
                class="transition-colors hover:bg-[var(--color-muted)]/30"
              >
                <td class="px-4 py-3 text-[var(--color-muted-foreground)]">{{ i + 1 }}</td>
                <td class="max-w-[200px] truncate px-4 py-3 font-medium">{{ report.title }}</td>
                <td class="px-4 py-3">
                  <span class="rounded-full bg-purple-50 px-2 py-0.5 text-xs font-medium text-purple-700 dark:bg-purple-950 dark:text-purple-300">
                    {{ report.skill_id }}
                  </span>
                </td>
                <td class="hidden whitespace-nowrap px-4 py-3 text-[var(--color-muted-foreground)] sm:table-cell">
                  {{ formatTime(report.created_at) }}
                </td>
                <td class="px-4 py-3 text-right">
                  <div class="flex items-center justify-end gap-1">
                    <Button variant="ghost" size="sm" @click="$router.push(`/report/${report.id}`)">查看</Button>
                    <Button variant="ghost" size="sm" class="text-red-500 hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-950" @click="handleDelete(report)">删除</Button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </StateWrapper>

    <!-- Delete confirmation dialog -->
    <Teleport to="body">
      <div
        v-if="deleteTarget"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm"
        @click.self="deleteTarget = null"
      >
        <div class="w-full max-w-sm rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-xl">
          <h3 class="text-lg font-semibold">确认删除</h3>
          <p class="mt-2 text-sm text-[var(--color-muted-foreground)]">
            确定要删除报告「{{ deleteTarget.title }}」吗？此操作不可撤销。
          </p>
          <div class="mt-6 flex justify-end gap-3">
            <Button variant="outline" @click="deleteTarget = null">取消</Button>
            <Button variant="destructive" :disabled="deleting" @click="confirmDelete">
              <Loader2 v-if="deleting" class="h-4 w-4 animate-spin" />
              {{ deleting ? '删除中...' : '确认删除' }}
            </Button>
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
const loading = ref(true)
const error = ref<string | null>(null)
const reports = ref<ReportItem[]>([])
const search = ref('')
const deleteTarget = ref<ReportItem | null>(null)
const deleting = ref(false)

const filteredReports = computed(() => {
  if (!search.value.trim()) return reports.value
  const q = search.value.toLowerCase()
  return reports.value.filter(r =>
    r.title.toLowerCase().includes(q) ||
    r.skill_id.toLowerCase().includes(q),
  )
})

onMounted(() => { fetchList() })

async function fetchList() {
  loading.value = true
  error.value = null
  try {
    const res = await reportApi.list()
    reports.value = res.reports
  } catch (e: unknown) {
    error.value = (e as Error).message || '加载失败'
  } finally {
    loading.value = false
  }
}

function handleDelete(report: ReportItem) {
  deleteTarget.value = report
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await reportApi.remove(deleteTarget.value.id)
    toast.success('报告已删除')
    deleteTarget.value = null
    await fetchList()
  } catch (e: unknown) {
    toast.error((e as Error).message || '删除失败')
  } finally {
    deleting.value = false
  }
}

function formatTime(ts: string): string {
  if (!ts) return '-'
  const d = new Date(ts)
  return d.toLocaleString('zh-CN', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}
</script>
