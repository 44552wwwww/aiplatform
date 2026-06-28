<template>
  <AppLayout>
    <!-- Welcome -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Welcome, {{ username }}</h1>
      <p class="mt-1 text-sm text-[var(--color-muted-foreground)]">{{ greeting }}</p>
    </div>

    <!-- Stats -->
    <StateWrapper :loading="loading" :error="error" :empty="false" :retry="fetchData">
      <div class="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card v-for="stat in stats" :key="stat.label">
          <div class="flex items-center gap-4">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg" :class="stat.bg">
              <component :is="stat.icon" class="h-5 w-5" :class="stat.color" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ stat.value }}</div>
              <div class="text-xs text-[var(--color-muted-foreground)]">{{ stat.label }}</div>
            </div>
          </div>
        </Card>
      </div>
    </StateWrapper>

    <!-- Quick Actions + Recent Reports -->
    <div class="grid gap-6 lg:grid-cols-2">
      <!-- Quick Actions -->
      <Card title="快捷操作">
        <div class="space-y-2">
          <button
            v-for="action in quickActions"
            :key="action.label"
            class="flex w-full items-center gap-3 rounded-lg px-4 py-3 text-left text-sm transition-colors hover:bg-[var(--color-muted)]"
            @click="$router.push(action.to)"
          >
            <component :is="action.icon" class="h-4 w-4 text-[var(--color-muted-foreground)]" />
            <div>
              <div class="font-medium">{{ action.label }}</div>
              <div class="text-xs text-[var(--color-muted-foreground)]">{{ action.desc }}</div>
            </div>
          </button>
        </div>
      </Card>

      <!-- Recent Reports -->
      <Card title="最近报告">
        <div v-if="recentReports.length" class="divide-y divide-[var(--color-border)]">
          <div
            v-for="r in recentReports.slice(0, 5)"
            :key="r.id"
            class="flex items-center justify-between py-3 first:pt-0 last:pb-0"
          >
            <div class="min-w-0 flex-1">
              <div class="truncate text-sm font-medium">{{ r.title }}</div>
              <div class="flex items-center gap-2 text-xs text-[var(--color-muted-foreground)]">
                <span>{{ r.skill_id }}</span>
                <span>·</span>
                <span>{{ formatTime(r.created_at) }}</span>
              </div>
            </div>
            <Button variant="ghost" size="sm" @click="$router.push(`/report/${r.id}`)">查看</Button>
          </div>
        </div>
        <EmptyState v-else description="暂无报告" />
      </Card>
    </div>

    <!-- System Status -->
    <Card title="系统状态" class="mt-6">
      <div class="flex flex-wrap gap-4">
        <div v-for="s in systemStatus" :key="s.label" class="flex items-center gap-2 rounded-lg border border-[var(--color-border)] px-4 py-3">
          <div class="flex h-2 w-2 rounded-full" :class="s.ok ? 'bg-emerald-500' : 'bg-red-500'" />
          <span class="text-sm">{{ s.label }}</span>
          <span class="text-xs text-[var(--color-muted-foreground)]">{{ s.detail }}</span>
        </div>
      </div>
    </Card>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { LayoutDashboard, Puzzle, FileText, Activity, Zap, Clock, Plus } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import StateWrapper from '@/components/shared/StateWrapper.vue'
import EmptyState from '@/components/shared/EmptyState.vue'
import { useAuthStore } from '@/stores/auth'
import { useSkillStore } from '@/stores/skill'
import { reportApi, type ReportItem } from '@/api/report'

const router = useRouter()
const auth = useAuthStore()
const skillStore = useSkillStore()

const loading = ref(true)
const error = ref<string | null>(null)
const recentReports = ref<ReportItem[]>([])

const username = computed(() => auth.user?.username || 'User')

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '早上好！AI Platform 已就绪，今天想生成什么报告？'
  if (hour < 18) return '下午好！探索 AI 技能，发现个性化分析的力量。'
  return '晚上好！AI 引擎 24/7 运行，随时为你生成报告。'
})

const stats = computed(() => [
  { label: '可用 Skills', value: skillStore.skills.length, icon: Puzzle, bg: 'bg-purple-100 dark:bg-purple-900/40', color: 'text-purple-600 dark:text-purple-400' },
  { label: '我的报告', value: recentReports.value.length, icon: FileText, bg: 'bg-emerald-100 dark:bg-emerald-900/40', color: 'text-emerald-600 dark:text-emerald-400' },
  { label: '账户状态', value: 'Active', icon: Activity, bg: 'bg-blue-100 dark:bg-blue-900/40', color: 'text-blue-600 dark:text-blue-400' },
  { label: 'API 版本', value: 'v1.0', icon: Zap, bg: 'bg-amber-100 dark:bg-amber-900/40', color: 'text-amber-600 dark:text-amber-400' },
])

const systemStatus = computed(() => [
  { label: 'API Online', detail: 'Railway', ok: true },
  { label: 'Skills Loaded', detail: `${skillStore.skills.length} skills`, ok: skillStore.skills.length > 0 },
  { label: 'User Logged In', detail: username.value, ok: !!auth.token },
])

const quickActions = [
  { label: '浏览 Skills', desc: '查看所有可用的 AI 分析能力', icon: Puzzle, to: '/skills' },
  { label: '查看历史', desc: '管理已生成的报告', icon: Clock, to: '/history' },
  { label: '生成报告', desc: '创建一份新的 AI 分析报告', icon: Plus, to: '/skills' },
]

onMounted(() => { fetchData() })

async function fetchData() {
  loading.value = true
  error.value = null
  try {
    const [reportRes] = await Promise.all([
      reportApi.list().catch(() => ({ reports: [] as ReportItem[] })),
      skillStore.fetchSkills(),
    ])
    recentReports.value = reportRes.reports
  } catch (e: unknown) {
    error.value = (e as Error).message || '加载失败'
  } finally {
    loading.value = false
  }
}

function formatTime(ts: string): string {
  if (!ts) return '-'
  return new Date(ts).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>
