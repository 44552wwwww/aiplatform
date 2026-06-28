<template>
  <div class="grid min-h-screen" style="grid-template-columns: 240px 1fr;">
    <!-- Sidebar -->
    <aside class="flex flex-col border-r border-[var(--color-border)] bg-[var(--color-card)]" style="width:240px;">
      <div class="flex h-14 items-center gap-2.5 border-b border-[var(--color-border)] px-5">
        <Sparkles class="h-5 w-5 text-purple-600" />
        <span class="font-semibold tracking-tight">InsightForge</span>
      </div>

      <nav class="flex-1 space-y-1 overflow-y-auto px-3 py-5">
        <router-link
          v-for="item in navItems" :key="item.to" :to="item.to"
          class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-150"
          :class="$route.path.startsWith(item.to)
            ? 'bg-purple-50 text-purple-700 dark:bg-purple-950 dark:text-purple-300'
            : 'text-[var(--color-muted-foreground)] hover:bg-[var(--color-muted)] hover:text-[var(--color-foreground)]'"
        >
          <component :is="item.icon" class="h-4 w-4" />
          {{ item.label }}
        </router-link>
      </nav>

      <div class="border-t border-[var(--color-border)] p-3">
        <div class="flex items-center gap-3 rounded-xl px-3 py-2.5">
          <div class="flex h-8 w-8 items-center justify-center rounded-full bg-purple-100 text-xs font-bold text-purple-700 dark:bg-purple-900 dark:text-purple-300">
            {{ initial }}
          </div>
          <div class="flex-1 truncate text-sm font-medium">{{ username }}</div>
        </div>
        <button
          class="mt-1 flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-[var(--color-muted-foreground)] transition-colors hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-950 dark:hover:text-red-400"
          @click="handleLogout"
        >
          <LogOut class="h-4 w-4" />
          退出登录
        </button>
      </div>
    </aside>

    <!-- Main -->
    <div class="flex flex-col" style="min-width:0;">
      <header class="flex h-14 flex-shrink-0 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-background)]/80 backdrop-blur-lg px-6">
        <h2 class="text-sm font-medium text-[var(--color-muted-foreground)]">{{ pageTitle }}</h2>
        <div class="flex items-center gap-4">
          <ThemeToggle />
          <span class="text-sm text-[var(--color-muted-foreground)]">{{ username }}</span>
        </div>
      </header>
      <main class="flex-1 overflow-auto p-8">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LayoutDashboard, Puzzle, Clock, Settings, LogOut, Sparkles } from 'lucide-vue-next'
import ThemeToggle from '@/components/shared/ThemeToggle.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const username = computed(() => auth.user?.username || 'User')
const initial = computed(() => (username.value[0] || 'U').toUpperCase())

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/skills', label: 'Skills', icon: Puzzle },
  { to: '/history', label: 'History', icon: Clock },
  { to: '/settings', label: 'Settings', icon: Settings },
]

const pageTitle = computed(() => {
  const item = navItems.find(n => route.path.startsWith(n.to))
  return item?.label || ''
})

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>
