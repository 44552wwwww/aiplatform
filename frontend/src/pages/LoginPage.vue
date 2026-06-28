<template>
  <AuthLayout>
    <div class="auth-header">
      <div class="auth-logo">✨</div>
      <h1 class="auth-title">欢迎回来</h1>
      <p class="auth-subtitle">登录你的 InsightForge 账号</p>
    </div>
    <form class="auth-form" @submit.prevent="handleLogin">
      <div class="form-group">
        <label class="form-label">用户名</label>
        <input
          ref="usernameRef"
          v-model="form.username"
          type="text"
          class="form-input"
          placeholder="请输入用户名"
          autocomplete="username"
        />
      </div>
      <div class="form-group">
        <label class="form-label">密码</label>
        <div class="password-input-wrapper">
          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            class="form-input"
            placeholder="请输入密码"
            autocomplete="current-password"
            @keyup.enter="handleLogin"
          />
          <button type="button" class="password-toggle" @click="showPassword = !showPassword">
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>
      </div>
      <div v-if="error" class="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300 mb-4">{{ error }}</div>
      <button type="submit" class="btn btn-primary btn-lg btn-full" :class="{ 'btn-loading': loading }" :disabled="loading">
        <span v-if="loading" class="loading-spinner" />
        {{ loading ? '登录中...' : '登录' }}
      </button>
    </form>
    <div class="auth-footer">
      还没有账号？<router-link to="/register">立即注册</router-link>
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AuthLayout from '@/layouts/AuthLayout.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const usernameRef = ref<HTMLInputElement>()
const form = reactive({ username: '', password: '' })
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

onMounted(() => { usernameRef.value?.focus() })

async function handleLogin() {
  if (!form.username.trim() || !form.password) { error.value = '请填写用户名和密码'; return }
  loading.value = true; error.value = ''
  try {
    await auth.login(form.username.trim(), form.password)
    router.push((route.query.redirect as string) || '/dashboard')
  } catch (e: unknown) {
    error.value = (e as Error).message || '登录失败，请检查网络连接'
  } finally { loading.value = false }
}
</script>
