<template>
  <AuthLayout>
    <Card class="shadow-lg">
      <div class="mb-8 text-center">
        <div class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-purple-100 dark:bg-purple-900/40">
          <Sparkles class="h-6 w-6 text-purple-600 dark:text-purple-400" />
        </div>
        <h1 class="text-2xl font-bold">欢迎回来</h1>
        <p class="mt-2 text-sm text-[var(--color-muted-foreground)]">登录你的 InsightForge 账号</p>
      </div>

      <form class="space-y-4" @submit.prevent="handleLogin">
        <div>
          <label class="mb-1.5 block text-sm font-medium">用户名</label>
          <input
            ref="usernameRef"
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            autocomplete="username"
            class="flex h-10 w-full rounded-[var(--radius)] border border-[var(--color-border)] bg-[var(--color-background)] px-3 py-2 text-sm placeholder:text-[var(--color-muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1 transition-colors"
          />
        </div>

        <div>
          <label class="mb-1.5 block text-sm font-medium">密码</label>
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="请输入密码"
              autocomplete="current-password"
              class="flex h-10 w-full rounded-[var(--radius)] border border-[var(--color-border)] bg-[var(--color-background)] px-3 py-2 pr-10 text-sm placeholder:text-[var(--color-muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1 transition-colors"
              @keyup.enter="handleLogin"
            />
            <button
              type="button"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] transition-colors"
              @click="showPassword = !showPassword"
            >
              <EyeOff v-if="showPassword" class="h-4 w-4" />
              <Eye v-else class="h-4 w-4" />
            </button>
          </div>
        </div>

        <div v-if="error" class="rounded-[var(--radius)] bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">
          {{ error }}
        </div>

        <Button type="submit" class="w-full" :disabled="loading">
          <Loader2 v-if="loading" class="h-4 w-4 animate-spin" />
          {{ loading ? '登录中...' : '登录' }}
        </Button>
      </form>

      <p class="mt-6 text-center text-sm text-[var(--color-muted-foreground)]">
        还没有账号？
        <router-link to="/register" class="font-medium text-purple-600 hover:text-purple-700 dark:text-purple-400 transition-colors">立即注册</router-link>
      </p>
    </Card>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Sparkles, Eye, EyeOff, Loader2 } from 'lucide-vue-next'
import AuthLayout from '@/layouts/AuthLayout.vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const usernameRef = ref<HTMLInputElement>()
const form = reactive({ username: '', password: '' })
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

onMounted(() => {
  usernameRef.value?.focus()
})

async function handleLogin() {
  if (!form.username.trim() || !form.password) {
    error.value = '请填写用户名和密码'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await auth.login(form.username.trim(), form.password)
    router.push('/dashboard')
  } catch (e: unknown) {
    error.value = (e as Error).message || '登录失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}
</script>
