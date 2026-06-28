<template>
  <AuthLayout>
    <div class="auth-header">
      <div class="auth-logo">✨</div>
      <h1 class="auth-title">创建账号</h1>
      <p class="auth-subtitle">加入 InsightForge，开启 AI 分析之旅</p>
    </div>
    <form class="auth-form" @submit.prevent="handleRegister">
      <div class="form-group">
        <label class="form-label">用户名</label>
        <input ref="usernameRef" v-model="form.username" type="text" class="form-input" placeholder="2-50 个字符" autocomplete="username" maxlength="50" />
      </div>
      <div class="form-group">
        <label class="form-label">密码</label>
        <div class="password-input-wrapper">
          <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="form-input" placeholder="至少 6 位" autocomplete="new-password" maxlength="128" />
          <button type="button" class="password-toggle" @click="showPassword = !showPassword">
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>
        <div v-if="form.password" class="mt-2 flex gap-1.5">
          <div v-for="i in 3" :key="i" class="h-1 flex-1 rounded-full transition-colors" :class="strengthLevel >= i ? strengthColor : 'bg-[var(--border-color)]'" />
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">确认密码</label>
        <div class="password-input-wrapper">
          <input v-model="form.confirm" type="password" class="form-input" placeholder="再次输入密码" autocomplete="new-password"
            :style="form.confirm && form.password !== form.confirm ? 'border-color: #ef4444;' : ''"
            @keyup.enter="handleRegister"
          />
        </div>
        <p v-if="form.confirm && form.password !== form.confirm" class="mt-1.5 text-xs text-red-500">两次密码不一致</p>
      </div>
      <div v-if="error" class="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300 mb-4">{{ error }}</div>
      <button type="submit" class="btn btn-primary btn-lg btn-full" :class="{ 'btn-loading': loading }" :disabled="loading">
        <span v-if="loading" class="loading-spinner" />{{ loading ? '注册中...' : '注册' }}
      </button>
    </form>
    <div class="auth-footer">
      已有账号？<router-link to="/login">立即登录</router-link>
    </div>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AuthLayout from '@/layouts/AuthLayout.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const usernameRef = ref<HTMLInputElement>()
const form = reactive({ username: '', password: '', confirm: '' })
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const strengthLevel = computed(() => {
  const pw = form.password
  if (pw.length >= 12) return 3; if (pw.length >= 8) return 2; if (pw.length >= 6) return 1; return 0
})
const strengthColor = computed(() => {
  if (strengthLevel.value === 3) return 'bg-emerald-500'
  if (strengthLevel.value === 2) return 'bg-amber-500'
  return 'bg-red-400'
})

onMounted(() => { usernameRef.value?.focus() })

async function handleRegister() {
  error.value = ''
  if (!form.username.trim()) { error.value = '请输入用户名'; return }
  if (form.username.trim().length < 2) { error.value = '用户名至少 2 个字符'; return }
  if (!form.password) { error.value = '请输入密码'; return }
  if (form.password.length < 6) { error.value = '密码至少 6 位'; return }
  if (form.password !== form.confirm) { error.value = '两次密码不一致'; return }
  loading.value = true
  try {
    await auth.register(form.username.trim(), form.password)
    router.push('/dashboard')
  } catch (e: unknown) {
    error.value = (e as Error).message || '注册失败，请检查网络连接'
  } finally { loading.value = false }
}
</script>
