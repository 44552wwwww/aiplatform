<template>
  <AppLayout>
    <div class="page-header">
      <h1 class="page-title">Settings</h1>
      <p class="page-desc">管理你的账户和应用设置</p>
    </div>

    <div class="max-w-2xl space-y-6">
      <!-- Account -->
      <div class="settings-section glass-card">
        <h3 class="settings-section-title">Account</h3>
        <div class="settings-item">
          <span class="settings-item-label">用户名</span>
          <span class="settings-item-value">{{ auth.user?.username || '-' }}</span>
        </div>
        <div class="settings-item">
          <span class="settings-item-label">User ID</span>
          <span class="settings-item-value" style="font-family: monospace;">{{ auth.user?.id ?? '-' }}</span>
        </div>
        <div class="settings-item">
          <span class="settings-item-label">登录状态</span>
          <span class="settings-item-value" :style="{ color: auth.isLoggedIn ? 'var(--brand-primary)' : '#ef4444' }">
            ● {{ auth.isLoggedIn ? '已登录' : '未登录' }}
          </span>
        </div>
        <div class="settings-item">
          <span class="settings-item-label">JWT</span>
          <span class="settings-item-value" style="font-family: monospace; font-size: 0.75rem;" :style="{ color: auth.token ? 'var(--brand-primary)' : 'var(--text-muted)' }">
            {{ tokenPreview || '无' }}
          </span>
        </div>
      </div>

      <!-- Appearance -->
      <div class="settings-section glass-card">
        <h3 class="settings-section-title">Appearance</h3>
        <div class="settings-item">
          <div>
            <div class="settings-item-label" style="margin-bottom: 4px;">主题</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">选择你喜欢的界面主题</div>
          </div>
          <div class="theme-options">
            <button
              v-for="opt in themeOptions"
              :key="opt.value"
              class="theme-option"
              :class="{ active: themeVal === opt.value }"
              @click="setTheme(opt.value)"
            >
              <span class="theme-option-icon">{{ opt.icon }}</span>
              <span>{{ opt.label }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- System -->
      <div class="settings-section glass-card">
        <h3 class="settings-section-title">System</h3>
        <div v-for="s in sysItems" :key="s.label" class="settings-item">
          <span class="settings-item-label">{{ s.label }}</span>
          <span class="settings-item-value" :style="{ fontFamily: s.mono ? 'monospace' : 'inherit', fontSize: s.mono ? '0.75rem' : '0.875rem' }">{{ s.value }}</span>
        </div>
      </div>

      <!-- About -->
      <div class="settings-section glass-card">
        <h3 class="settings-section-title">About</h3>
        <div class="settings-item" style="flex-direction: column; align-items: flex-start; gap: var(--spacing-sm);">
          <p class="text-sm text-[var(--text-secondary)] leading-relaxed">
            InsightForge AI Platform — 基于插件架构的 AI 结构化报告生成平台。
          </p>
          <div class="flex flex-wrap gap-2">
            <span v-for="t in techStack" :key="t" class="skill-badge">{{ t }}</span>
          </div>
          <div class="flex items-center gap-3 text-xs text-[var(--text-muted)]">
            <a href="https://github.com/44552wwwww/aiplatform" target="_blank" class="settings-item-link">GitHub</a>
            <span>·</span>
            <span>MIT License</span>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'

const auth = useAuthStore()
const { theme, set } = useTheme()
const themeVal = computed(() => theme.value)

const themeOptions = [
  { value: 'light' as const, label: 'Light', icon: '☀️' },
  { value: 'dark' as const, label: 'Dark', icon: '🌙' },
  { value: 'system' as const, label: 'System', icon: '💻' },
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

const sysItems = computed(() => [
  { label: 'Frontend', value: 'v2.0', mono: true },
  { label: 'API Base', value: apiUrl.value, mono: true },
  { label: 'Environment', value: isProd.value ? 'Production' : 'Development' },
  { label: 'API Version', value: 'v1.0', mono: true },
])

const techStack = ['Vue 3', 'TypeScript', 'TailwindCSS', 'FastAPI', 'SQLAlchemy', 'PostgreSQL', 'Railway', 'Docker', 'DeepSeek']
</script>
