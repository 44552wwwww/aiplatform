import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type UserInfo } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<UserInfo | null>(null)
  const loading = ref(false)

  const isLoggedIn = computed(() => !!token.value)

  function init() {
    try {
      const stored = localStorage.getItem('auth')
      if (stored) {
        const data = JSON.parse(stored)
        token.value = data.token
        user.value = data.user
      }
    } catch {
      // ignore
    }
  }

  function save() {
    localStorage.setItem('auth', JSON.stringify({ token: token.value, user: user.value }))
  }

  function clear() {
    token.value = null
    user.value = null
    localStorage.removeItem('auth')
    localStorage.removeItem('user')
  }

  async function register(username: string, password: string) {
    loading.value = true
    try {
      const res = await authApi.register({ username, password })
      token.value = res.access_token
      user.value = res.user
      save()
      return res
    } finally {
      loading.value = false
    }
  }

  async function login(username: string, password: string) {
    loading.value = true
    try {
      const res = await authApi.login({ username, password })
      token.value = res.access_token
      user.value = res.user
      save()
      return res
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    try {
      const u = await authApi.me()
      user.value = u
      save()
    } catch {
      clear()
    }
  }

  function logout() {
    clear()
  }

  // 初始化时从 localStorage 恢复
  init()

  return { token, user, loading, isLoggedIn, register, login, fetchMe, logout, init }
})
