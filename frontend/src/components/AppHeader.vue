<template>
  <el-header class="app-header">
    <div class="header-left">
      <router-link to="/" class="logo">🔮 InsightForge</router-link>
    </div>
    <div class="header-right desktop-nav">
      <template v-if="auth.isLoggedIn">
        <span class="user-tag">👤 {{ auth.user?.username }}</span>
        <el-button text @click="$router.push('/history')">我的报告</el-button>
        <el-button text type="danger" @click="handleLogout">退出</el-button>
      </template>
      <template v-else>
        <el-button text @click="$router.push('/login')">登录</el-button>
        <el-button type="primary" size="small" @click="$router.push('/register')">注册</el-button>
      </template>
    </div>
    <div class="mobile-nav">
      <el-button text class="hamburger" @click="drawerOpen = true">
        ☰
      </el-button>
    </div>
  </el-header>

  <!-- 移动端抽屉导航 -->
  <teleport to="body">
    <div v-if="drawerOpen" class="drawer-overlay" @click.self="drawerOpen = false">
      <div class="drawer-panel">
        <div class="drawer-header">
          <span class="drawer-title">导航</span>
          <el-button text @click="drawerOpen = false">✕</el-button>
        </div>
        <div class="drawer-body">
          <template v-if="auth.isLoggedIn">
            <div class="drawer-user">👤 {{ auth.user?.username }}</div>
            <el-button text class="drawer-link" @click="nav('/history')">
              我的报告
            </el-button>
            <el-button text class="drawer-link" type="danger" @click="handleLogout()">
              退出登录
            </el-button>
          </template>
          <template v-else>
            <el-button text class="drawer-link" @click="nav('/login')">
              登录
            </el-button>
            <el-button type="primary" class="drawer-link" @click="nav('/register')">
              注册
            </el-button>
          </template>
        </div>
      </div>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const drawerOpen = ref(false)

function handleLogout() {
  auth.logout()
  drawerOpen.value = false
  router.push('/login')
}

function nav(path: string) {
  drawerOpen.value = false
  router.push(path)
}
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}
.header-left .logo {
  font-size: 1.2em;
  font-weight: 700;
  color: #8b4513;
  text-decoration: none;
  letter-spacing: 0.04em;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.user-tag {
  color: #606266;
  font-size: 0.9em;
  margin-right: 8px;
}

/* 移动端汉堡菜单 */
.mobile-nav {
  display: none;
}
.hamburger {
  font-size: 1.4em;
  padding: 4px 8px;
}

@media (max-width: 768px) {
  .app-header {
    padding: 0 12px;
  }
  .header-left .logo {
    font-size: 1em;
  }
  .desktop-nav {
    display: none;
  }
  .mobile-nav {
    display: block;
  }
}

/* 抽屉样式 */
.drawer-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  background: rgba(0, 0, 0, 0.35);
}
.drawer-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 260px;
  height: 100%;
  background: #fff;
  box-shadow: -2px 0 16px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}
.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #e4e7ed;
}
.drawer-title {
  font-weight: 600;
  font-size: 16px;
}
.drawer-body {
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.drawer-user {
  color: #606266;
  font-size: 14px;
  padding: 8px 0 16px;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 8px;
}
.drawer-link {
  justify-content: flex-start;
  width: 100%;
}
</style>
