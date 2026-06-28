<template>
  <div class="dashboard-layout">
    <!-- 侧边栏遮罩 -->
    <div class="sidebar-overlay" :class="{ active: sidebarOpen }" @click="sidebarOpen = false" />

    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <router-link to="/" class="sidebar-logo">
          <div class="navbar-logo-icon">✨</div>
          <span>InsightForge</span>
        </router-link>
      </div>

      <nav class="sidebar-nav">
        <div class="nav-section">
          <div class="nav-section-title">主菜单</div>
          <router-link
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="nav-item"
            :class="{ active: $route.path.startsWith(item.to) }"
          >
            <component :is="item.icon" class="nav-icon" />
            <span>{{ item.label }}</span>
          </router-link>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ initial }}</div>
          <div class="user-details">
            <div class="user-name">{{ username }}</div>
            <div class="user-role">Free User</div>
          </div>
        </div>
        <button class="logout-btn" @click="handleLogout">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          退出登录
        </button>
      </div>
    </aside>

    <!-- 主内容 -->
    <main class="main-content">
      <header class="topbar">
        <div class="topbar-title">{{ pageTitle }}</div>
        <div class="topbar-actions">
          <button class="theme-toggle" @click="toggleTheme" :title="themeLabel">
            {{ themeIcon }}
          </button>
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
        </div>
      </header>

      <div class="page-content">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LayoutGrid, Puzzle, Clock, Settings } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const { theme, toggle } = useTheme()
const sidebarOpen = ref(false)

const username = computed(() => auth.user?.username || 'User')
const initial = computed(() => (username.value[0] || 'U').toUpperCase())

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutGrid },
  { to: '/skills', label: 'Skills', icon: Puzzle },
  { to: '/history', label: 'History', icon: Clock },
  { to: '/settings', label: 'Settings', icon: Settings },
]

const pageTitle = computed(() => {
  // 优先从路由meta获取title，否则用navItems匹配
  const metaTitle = route.meta.title as string
  if (metaTitle) return metaTitle
  const item = navItems.find(n => route.path.startsWith(n.to))
  return item?.label || ''
})

const themeIcon = computed(() => (theme.value === 'dark' ? '☀️' : '🌙'))
const themeLabel = computed(() => (theme.value === 'dark' ? '切换浅色主题' : '切换深色主题'))

function toggleTheme() {
  toggle()
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>
