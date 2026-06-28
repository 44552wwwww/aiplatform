<template>
  <AppLayout>
    <div class="mb-8">
      <h1 class="text-2xl font-bold">Settings</h1>
      <p class="mt-1 text-sm text-[var(--color-muted-foreground)]">管理你的账户和应用设置</p>
    </div>

    <div class="max-w-2xl space-y-6">
      <!-- Account -->
      <Card title="Account">
        <div class="divide-y divide-[var(--color-border)]">
          <div class="flex items-center justify-between py-3 first:pt-0">
            <span class="text-sm text-[var(--color-muted-foreground)]">用户名</span>
            <span class="text-sm font-medium">{{ auth.user?.username || '-' }}</span>
          </div>
          <div class="flex items-center justify-between py-3">
            <span class="text-sm text-[var(--color-muted-foreground)]">User ID</span>
            <span class="font-mono text-sm">{{ auth.user?.id ?? '-' }}</span>
          </div>
          <div class="flex items-center justify-between py-3">
            <span class="text-sm text-[var(--color-muted-foreground)]">登录状态</span>
            <span class="inline-flex items-center gap-1.5 text-sm">
              <span class="h-2 w-2 rounded-full" :class="auth.isLoggedIn ? 'bg-emerald-500' : 'bg-red-500'" />
              {{ auth.isLoggedIn ? '已登录' : '未登录' }}
            </span>
          </div>
          <div class="flex items-center justify-between py-3 last:pb-0">
            <span class="text-sm text-[var(--color-muted-foreground)]">JWT</span>
            <span class="font-mono text-xs" :class="auth.token ? 'text-emerald-600 dark:text-emerald-400' : 'text-[var(--color-muted-foreground)]'">
              {{ auth.token ? tokenPreview : '无' }}
            </span>
          </div>
        </div>
      </Card>

      <!-- Appearance -->
      <Card title="Appearance">
        <div class="flex items-center justify-between py-1">
          <div>
            <div class="text-sm font-medium">主题</div>
            <div class="text-xs text-[var(--color-muted-foreground)]">选择你喜欢的界面主题</div>
          </div>
          <div class="flex rounded-lg border border-[var(--color-border)] p-0.5">
            <button
              v-for="opt in themeOptions"
              :key="opt.value"
              class="rounded-md px-3 py-1.5 text-xs font-medium transition-colors"
              :class="themeVal === opt.value
                ? 'bg-[var(--color-primary)] text-[var(--color-primary-foreground)] shadow-sm'
                : 'text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)]'"
              @click="setTheme(opt.value)"
            >
              <component :is="opt.icon" class="mr-1 inline h-3 w-3" />
              {{ opt.label }}
            </button>
          </div>
        </div>
      </Card>

      <!-- System -->
      <Card title="System">
        <div class="divide-y divide-[var(--color-border)]">
          <div class="flex items-center justify-between py-3 first:pt-0">
            <span class="text-sm text-[var(--color-muted-foreground)]">Frontend Version</span>
            <span class="font-mono text-xs">v2.0.0</span>
          </div>
          <div class="flex items-center justify-between py-3">
            <span class="text-sm text-[var(--color-muted-foreground)]">API Base URL</span>
            <span class="font-mono text-xs">{{ apiUrl }}</span>
          </div>
          <div class="flex items-center justify-between py-3">
            <span class="text-sm text-[var(--color-muted-foreground)]">Environment</span>
            <span class="rounded-full px-2 py-0.5 text-xs font-medium"
              :class="isProd
                ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400'
                : 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400'"
            >
              {{ isProd ? 'Production' : 'Development' }}
            </span>
          </div>
          <div class="flex items-center justify-between py-3">
            <span class="text-sm text-[var(--color-muted-foreground)]">Railway Status</span>
            <span class="inline-flex items-center gap-1.5 text-sm">
              <span class="h-2 w-2 rounded-full bg-emerald-500" />
              Deployed
            </span>
          </div>
          <div class="flex items-center justify-between py-3 last:pb-0">
            <span class="text-sm text-[var(--color-muted-foreground)]">API Version</span>
            <span class="font-mono text-xs">v1.0.0</span>
          </div>
        </div>
      </Card>

      <!-- About -->
      <Card title="About">
        <p class="mb-4 text-sm text-[var(--color-muted-foreground)] leading-relaxed">
          InsightForge AI Platform — 基于插件架构的 AI 结构化报告生成平台。
          平台负责用户系统与基础设施，Skill 负责 AI 分析能力。
        </p>
        <div class="flex flex-wrap gap-2">
          <span v-for="tech in techStack" :key="tech"
            class="rounded-full border border-[var(--color-border)] px-2.5 py-0.5 text-xs text-[var(--color-muted-foreground)]"
          >{{ tech }}</span>
        </div>
        <div class="mt-4 flex items-center gap-4 text-xs text-[var(--color-muted-foreground)]">
          <a href="https://github.com/44552wwwww/aiplatform" target="_blank"
            class="hover:text-[var(--color-foreground)] transition-colors">GitHub</a>
          <span>·</span>
          <span>MIT License</span>
        </div>
      </Card>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Sun, Moon, Monitor } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
import Card from '@/components/ui/Card.vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'

const auth = useAuthStore()
const { theme, set } = useTheme()
const themeVal = computed(() => theme.value)

const themeOptions = [
  { value: 'light' as const, label: 'Light', icon: Sun },
  { value: 'dark' as const, label: 'Dark', icon: Moon },
  { value: 'system' as const, label: 'System', icon: Monitor },
]

function setTheme(t: string) {
  if (t === 'system') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    set(prefersDark ? 'dark' : 'light')
  } else {
    set(t as 'light' | 'dark')
  }
}

const tokenPreview = computed(() => {
  const t = auth.token
  if (!t) return ''
  return t.length > 30 ? t.slice(0, 15) + '...' + t.slice(-10) : t
})

const apiUrl = computed(() => import.meta.env.VITE_API_URL || '(nginx proxy)')
const isProd = computed(() => apiUrl.value.includes('railway') || apiUrl.value.includes('production'))

const techStack = [
  'Vue 3', 'TypeScript', 'TailwindCSS', 'FastAPI', 'SQLAlchemy',
  'PostgreSQL', 'Railway', 'Docker', 'DeepSeek',
]
</script>
