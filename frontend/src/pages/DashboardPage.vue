<template>
  <AppLayout>
    <!-- 欢迎信息 -->
    <div class="page-header">
      <h1 class="page-title">Welcome, {{ username }} 👋</h1>
      <p class="page-desc">{{ greeting }}</p>
    </div>

    <!-- 加载状态 -->
    <template v-if="loading && !error">
      <div class="stats-row">
        <div v-for="i in 4" :key="i" class="stat-card glass-card"><div class="loading-spinner" /></div>
      </div>
    </template>

    <!-- 错误状态 -->
    <div v-else-if="error" class="empty-state">
      <div class="empty-state-icon">⚠️</div>
      <div class="empty-state-title">加载失败</div>
      <div class="empty-state-desc">{{ error }}</div>
      <button class="btn btn-primary" @click="fetchData">重试</button>
    </div>

    <template v-else>
      <!-- 统计卡片 -->
      <div class="stats-row">
        <div class="stat-card glass-card" v-for="stat in stats" :key="stat.label">
          <div class="stat-card-icon" :class="stat.iconClass">
            <component :is="stat.icon" style="width:24px;height:24px;" />
          </div>
          <div>
            <div class="stat-card-value">{{ stat.value }}</div>
            <div class="stat-card-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>

      <!-- 快捷操作和最近报告 -->
      <div class="dashboard-grid">
        <div class="panel glass-card">
          <div class="panel-header">
            <h3 class="panel-title">快捷操作</h3>
          </div>
          <div class="quick-actions">
            <a v-for="a in quickActions" :key="a.label" class="quick-action-item" @click.prevent="$router.push(a.to)">
              <div class="quick-action-icon">
                <component :is="a.icon" style="width:20px;height:20px;" />
              </div>
              <div class="quick-action-text">
                <div class="quick-action-title">{{ a.label }}</div>
                <div class="quick-action-desc">{{ a.desc }}</div>
              </div>
              <div class="quick-action-arrow">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9 18 15 12 9 6" />
                </svg>
              </div>
            </a>
          </div>
          <router-link to="/skills" class="btn btn-primary btn-full">立即生成报告</router-link>
        </div>

        <div class="panel glass-card">
          <div class="panel-header">
            <h3 class="panel-title">最近报告</h3>
          </div>
          <div v-if="recentReports.length" class="divide-y divide-[var(--border-color)]">
            <div v-for="r in recentReports.slice(0, 5)" :key="r.id" class="flex items-center justify-between py-3 first:pt-0 last:pb-0">
              <div class="min-w-0 flex-1">
                <div class="truncate text-sm font-medium">{{ r.title }}</div>
                <div class="mt-0.5 flex items-center gap-2 text-xs text-[var(--text-muted)]">
                  <span class="skill-badge">{{ r.skill_id }}</span>
                  <span>{{ formatTime(r.created_at) }}</span>
                </div>
              </div>
              <button class="btn btn-ghost text-sm" @click="$router.push(`/report/${r.id}`)">查看</button>
            </div>
          </div>
          <div v-else class="empty-state">
            <div class="empty-state-icon">📄</div>
            <div class="empty-state-title">暂无报告</div>
            <div class="empty-state-desc">去 Skills 页面生成第一份报告吧</div>
            <router-link to="/skills" class="btn btn-primary">浏览 Skills</router-link>
          </div>
        </div>
      </div>

      <!-- 系统状态 -->
      <div class="panel glass-card" style="margin-top: var(--spacing-lg);">
        <div class="panel-header">
          <h3 class="panel-title">系统状态</h3>
        </div>
        <div class="system-status">
          <div v-for="s in systemStatus" :key="s.label" class="status-item">
            <span class="status-dot" :style="{ background: s.ok ? 'var(--brand-primary)' : '#ef4444' }" />
            <span>{{ s.label }}</span>
            <span style="color: var(--text-muted); font-size: 0.75rem;">{{ s.detail }}</span>
          </div>
        </div>
      </div>
    </template>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Puzzle, FileText, Activity, Zap } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
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
  { label: 'Skills', value: skillStore.skills.length, icon: Puzzle, iconClass: 'purple' },
  { label: '报告', value: recentReports.value.length, icon: FileText, iconClass: 'green' },
  { label: '状态', value: 'Active', icon: Activity, iconClass: 'blue' },
  { label: 'API', value: 'v1.0', icon: Zap, iconClass: 'amber' },
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
