<template>
  <AppLayout>
    <div class="mb-10"><h1 class="text-2xl font-bold tracking-tight">Settings</h1><p class="mt-2 text-sm text-[var(--color-muted-foreground)]">管理你的账户和应用设置</p></div>
    <div class="max-w-2xl space-y-6">
      <div class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] shadow-sm">
        <div class="border-b border-[var(--color-border)] px-6 py-4"><h3 class="font-semibold">Account</h3></div>
        <div class="divide-y divide-[var(--color-border)] px-6">
          <div class="flex items-center justify-between py-4"><span class="text-sm text-[var(--color-muted-foreground)]">用户名</span><span class="text-sm font-medium">{{ auth.user?.username || '-' }}</span></div>
          <div class="flex items-center justify-between py-4"><span class="text-sm text-[var(--color-muted-foreground)]">User ID</span><span class="font-mono text-sm">{{ auth.user?.id ?? '-' }}</span></div>
          <div class="flex items-center justify-between py-4"><span class="text-sm text-[var(--color-muted-foreground)]">登录状态</span><span class="inline-flex items-center gap-1.5 text-sm"><span class="h-2 w-2 rounded-full" :class="auth.isLoggedIn ? 'bg-emerald-500' : 'bg-red-500'" />{{ auth.isLoggedIn ? '已登录' : '未登录' }}</span></div>
          <div class="flex items-center justify-between py-4"><span class="text-sm text-[var(--color-muted-foreground)]">JWT</span><span class="font-mono text-xs" :class="auth.token ? 'text-emerald-600 dark:text-emerald-400' : 'text-[var(--color-muted-foreground)]'">{{ auth.token ? tokenPreview : '无' }}</span></div>
        </div>
      </div>

      <div class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] shadow-sm">
        <div class="border-b border-[var(--color-border)] px-6 py-4"><h3 class="font-semibold">Appearance</h3></div>
        <div class="flex items-center justify-between px-6 py-5">
          <div><div class="text-sm font-medium">主题</div><div class="text-xs text-[var(--color-muted-foreground)]">选择你喜欢的界面主题</div></div>
          <div class="flex rounded-lg border border-[var(--color-border)] p-0.5">
            <button v-for="opt in themeOptions" :key="opt.value" class="flex items-center gap-1 rounded-md px-3 py-1.5 text-xs font-medium transition-all duration-150"
              :class="themeVal === opt.value ? 'bg-purple-600 text-white shadow-sm' : 'text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)]'" @click="setTheme(opt.value)">
              <component :is="opt.icon" class="h-3 w-3" />{{ opt.label }}</button>
          </div>
        </div>
      </div>

      <div class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] shadow-sm">
        <div class="border-b border-[var(--color-border)] px-6 py-4"><h3 class="font-semibold">System</h3></div>
        <div class="divide-y divide-[var(--color-border)] px-6">
          <div v-for="s in sysItems" :key="s.label" class="flex items-center justify-between py-4"><span class="text-sm text-[var(--color-muted-foreground)]">{{ s.label }}</span><span class="text-sm" :class="s.mono ? 'font-mono text-xs' : ''">{{ s.value }}</span></div>
        </div>
      </div>

      <div class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] shadow-sm">
        <div class="border-b border-[var(--color-border)] px-6 py-4"><h3 class="font-semibold">About</h3></div>
        <div class="space-y-4 px-6 py-5">
          <p class="text-sm text-[var(--color-muted-foreground)] leading-relaxed">InsightForge AI Platform — 基于插件架构的 AI 结构化报告生成平台。</p>
          <div class="flex flex-wrap gap-2"> <span v-for="t in techStack" :key="t" class="rounded-full border border-[var(--color-border)] px-2.5 py-0.5 text-xs text-[var(--color-muted-foreground)]">{{ t }}</span> </div>
          <div class="flex items-center gap-4 text-xs text-[var(--color-muted-foreground)]"><a href="https://github.com/44552wwwww/aiplatform" target="_blank" class="transition-colors hover:text-[var(--color-foreground)]">GitHub</a><span>·</span><span>MIT License</span></div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Sun, Moon, Monitor } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'
const auth = useAuthStore(); const { theme, set } = useTheme(); const themeVal = computed(() => theme.value)
const themeOptions = [{ value: 'light' as const, label: 'Light', icon: Sun },{ value: 'dark' as const, label: 'Dark', icon: Moon },{ value: 'system' as const, label: 'System', icon: Monitor }]
function setTheme(t: string) { if (t === 'system') { const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches; set(prefersDark ? 'dark' : 'light') } else { set(t as 'light' | 'dark') } }
const tokenPreview = computed(() => { const t = auth.token; if (!t) return ''; return t.length > 30 ? t.slice(0, 15) + '...' + t.slice(-10) : t })
const apiUrl = computed(() => import.meta.env.VITE_API_URL || '(nginx proxy)')
const isProd = computed(() => apiUrl.value.includes('railway') || apiUrl.value.includes('production'))
const sysItems = computed(() => [{ label: 'Frontend', value: 'v2.0', mono: true },{ label: 'API Base', value: apiUrl.value, mono: true },{ label: 'Environment', value: isProd.value ? 'Production' : 'Development' },{ label: 'API Version', value: 'v1.0', mono: true }])
const techStack = ['Vue 3','TypeScript','TailwindCSS','FastAPI','SQLAlchemy','PostgreSQL','Railway','Docker','DeepSeek']
</script>
