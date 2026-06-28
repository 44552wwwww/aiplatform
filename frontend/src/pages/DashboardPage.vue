<template>
  <AppLayout>
    <div class="mb-10">
      <h1 class="text-2xl font-bold tracking-tight">Welcome, {{ username }}</h1>
      <p class="mt-2 text-sm text-[var(--color-muted-foreground)]">{{ greeting }}</p>
    </div>

    <StateWrapper :loading="loading" :error="error" :empty="false" :retry="fetchData">
      <!-- Stats -->
      <div class="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div v-for="stat in stats" :key="stat.label"
          class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-5 shadow-sm transition-shadow hover:shadow-md">
          <div class="flex items-center gap-4">
            <div class="flex h-11 w-11 items-center justify-center rounded-xl" :class="stat.bg">
              <component :is="stat.icon" class="h-5 w-5" :class="stat.color" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ stat.value }}</div>
              <div class="text-xs text-[var(--color-muted-foreground)]">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </StateWrapper>

    <!-- Main CTA + Recent -->
    <div class="grid gap-6 lg:grid-cols-2">
      <div class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm">
        <h3 class="mb-4 font-semibold">快捷操作</h3>
        <div class="space-y-2">
          <div v-for="a in quickActions" :key="a.label"
            class="flex w-full items-center gap-3 rounded-xl px-4 py-3.5 text-left text-sm transition-colors hover:bg-[var(--color-muted)] cursor-pointer"
            @click="$router.push(a.to)">
            <component :is="a.icon" class="h-4 w-4 text-[var(--color-muted-foreground)]" />
            <div>
              <div class="font-medium">{{ a.label }}</div>
              <div class="text-xs text-[var(--color-muted-foreground)]">{{ a.desc }}</div>
            </div>
          </div>
        </div>
        <router-link to="/skills"
          class="mt-4 inline-flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-purple-600 text-sm font-semibold text-white shadow-sm transition-all hover:bg-purple-700 hover:shadow-md active:scale-[0.98]">
          <Zap class="h-4 w-4" /> 立即生成报告
        </router-link>
      </div>

      <div class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm">
        <h3 class="mb-4 font-semibold">最近报告</h3>
        <div v-if="recentReports.length" class="divide-y divide-[var(--color-border)]">
          <div v-for="r in recentReports.slice(0, 5)" :key="r.id" class="flex items-center justify-between py-3 first:pt-0 last:pb-0">
            <div class="min-w-0 flex-1">
              <div class="truncate text-sm font-medium">{{ r.title }}</div>
              <div class="mt-0.5 flex items-center gap-2 text-xs text-[var(--color-muted-foreground)]">
                <span class="rounded bg-purple-50 px-1.5 py-0.5 font-medium text-purple-700 dark:bg-purple-950 dark:text-purple-300">{{ r.skill_id }}</span>
                <span>{{ formatTime(r.created_at) }}</span>
              </div>
            </div>
            <Button variant="ghost" size="sm" @click="$router.push(`/report/${r.id}`)">查看</Button>
          </div>
        </div>
        <EmptyState v-else description="暂无报告" />
      </div>
    </div>

    <!-- System Status -->
    <div class="mt-6 rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm">
      <h3 class="mb-4 font-semibold">系统状态</h3>
      <div class="flex flex-wrap gap-3">
        <div v-for="s in systemStatus" :key="s.label" class="flex items-center gap-2 rounded-xl border border-[var(--color-border)] px-4 py-2.5 text-sm">
          <div class="h-2 w-2 rounded-full" :class="s.ok ? 'bg-emerald-500' : 'bg-red-500'" />
          <span>{{ s.label }}</span>
          <span class="text-xs text-[var(--color-muted-foreground)]">{{ s.detail }}</span>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Puzzle, FileText, Activity, Zap } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
import Button from '@/components/ui/Button.vue'
import StateWrapper from '@/components/shared/StateWrapper.vue'
import EmptyState from '@/components/shared/EmptyState.vue'
import { useAuthStore } from '@/stores/auth'
import { useSkillStore } from '@/stores/skill'
import { reportApi, type ReportItem } from '@/api/report'

const auth = useAuthStore()
const skillStore = useSkillStore()

const loading = ref(true)
const error = ref<string | null>(null)
const recentReports = ref<ReportItem[]>([])

const username = computed(() => auth.user?.username || 'User')
const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return '早上好！AI Platform 已就绪。'
  if (h < 18) return '下午好！探索 AI 技能，发现个性化分析的力量。'
  return '晚上好！AI 引擎 24/7 运行。'
})

const stats = computed(() => [
  { label: 'Skills', value: skillStore.skills.length, icon: Puzzle, bg: 'bg-purple-100 dark:bg-purple-900/40', color: 'text-purple-600 dark:text-purple-400' },
  { label: '报告', value: recentReports.value.length, icon: FileText, bg: 'bg-emerald-100 dark:bg-emerald-900/40', color: 'text-emerald-600 dark:text-emerald-400' },
  { label: '状态', value: 'Active', icon: Activity, bg: 'bg-blue-100 dark:bg-blue-900/40', color: 'text-blue-600 dark:text-blue-400' },
  { label: 'API', value: 'v1.0', icon: Zap, bg: 'bg-amber-100 dark:bg-amber-900/40', color: 'text-amber-600 dark:text-amber-400' },
])

const systemStatus = computed(() => [
  { label: 'API Online', detail: 'Railway', ok: true },
  { label: 'Skills', detail: `${skillStore.skills.length} loaded`, ok: skillStore.skills.length > 0 },
  { label: 'User', detail: username.value, ok: !!auth.token },
])

const quickActions = [
  { label: '浏览 Skills', desc: '查看所有可用的 AI 分析能力', icon: Puzzle, to: '/skills' },
  { label: '查看历史', desc: '管理已生成的报告', icon: FileText, to: '/history' },
]

onMounted(() => { fetchData() })

async function fetchData() {
  loading.value = true; error.value = null
  try {
    const [reportRes] = await Promise.all([
      reportApi.list().catch(() => ({ reports: [] as ReportItem[] })),
      skillStore.fetchSkills(),
    ])
    recentReports.value = reportRes.reports
  } catch (e: unknown) { error.value = (e as Error).message || '加载失败' }
  finally { loading.value = false }
}

function formatTime(ts: string): string {
  if (!ts) return '-'
  return new Date(ts).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>
