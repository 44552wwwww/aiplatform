<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 z-40 flex w-60 flex-col border-r border-[var(--color-border)] bg-[var(--color-card)]">
      <!-- Logo -->
      <div class="flex h-14 items-center gap-2 border-b border-[var(--color-border)] px-4">
        <Sparkles class="h-5 w-5 text-purple-600" />
        <span class="font-semibold">InsightForge</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 space-y-1 px-3 py-4">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
          :class="$route.path === item.to
            ? 'bg-purple-50 text-purple-700 dark:bg-purple-950 dark:text-purple-300'
            : 'text-[var(--color-muted-foreground)] hover:bg-[var(--color-muted)] hover:text-[var(--color-foreground)]'"
        >
          <component :is="item.icon" class="h-4 w-4" />
          {{ item.label }}
        </router-link>
      </nav>

      <!-- User -->
      <div class="border-t border-[var(--color-border)] px-3 py-3">
        <div class="flex items-center gap-3 rounded-lg px-3 py-2">
          <div class="flex h-7 w-7 items-center justify-center rounded-full bg-purple-100 text-xs font-bold text-purple-700 dark:bg-purple-900 dark:text-purple-300">
            {{ initial }}
          </div>
          <div class="flex-1 truncate text-sm font-medium">{{ username }}</div>
        </div>
        <button
          class="mt-1 flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-[var(--color-muted-foreground)] hover:bg-[var(--color-muted)] hover:text-[var(--color-foreground)] transition-colors"
          @click="handleLogout"
        >
          <LogOut class="h-4 w-4" />
          退出登录
        </button>
      </div>
    </aside>

    <!-- Main area -->
    <div class="ml-60 flex flex-1 flex-col">
      <!-- Header -->
      <header class="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-background)]/80 backdrop-blur-lg px-6">
        <h2 class="text-sm font-medium text-[var(--color-muted-foreground)]">{{ pageTitle }}</h2>
        <div class="flex items-center gap-3">
          <ThemeToggle />
          <span class="text-sm text-[var(--color-muted-foreground)]">{{ username }}</span>
        </div>
      </header>

      <!-- Content -->
      <main class="flex-1 p-6">
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
