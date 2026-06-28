<template>
  <AuthLayout>
    <Card class="shadow-lg">
      <div class="mb-8 text-center">
        <div class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-purple-100 dark:bg-purple-900/40">
          <UserPlus class="h-6 w-6 text-purple-600 dark:text-purple-400" />
        </div>
        <h1 class="text-2xl font-bold">创建账号</h1>
        <p class="mt-2 text-sm text-[var(--color-muted-foreground)]">注册 InsightForge，开始使用 AI 生成报告</p>
      </div>

      <form class="space-y-4" @submit.prevent="handleRegister">
        <div>
          <label class="mb-1.5 block text-sm font-medium">用户名</label>
          <input
            ref="usernameRef"
            v-model="form.username"
            type="text"
            placeholder="2-50 个字符"
            autocomplete="username"
            class="flex h-10 w-full rounded-[var(--radius)] border border-[var(--color-border)] bg-[var(--color-background)] px-3 py-2 text-sm placeholder:text-[var(--color-muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1 transition-colors"
            maxlength="50"
          />
        </div>

        <div>
          <label class="mb-1.5 block text-sm font-medium">密码</label>
          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="至少 6 位"
              autocomplete="new-password"
              class="flex h-10 w-full rounded-[var(--radius)] border border-[var(--color-border)] bg-[var(--color-background)] px-3 py-2 pr-10 text-sm placeholder:text-[var(--color-muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1 transition-colors"
              maxlength="128"
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
          <div v-if="form.password" class="mt-1.5 flex gap-1">
            <div
              v-for="i in 3"
              :key="i"
              class="h-1 flex-1 rounded-full transition-colors"
              :class="strengthLevel >= i ? strengthColor : 'bg-[var(--color-border)]'"
            />
          </div>
        </div>

        <div>
          <label class="mb-1.5 block text-sm font-medium">确认密码</label>
          <input
            v-model="form.confirm"
            type="password"
            placeholder="再次输入密码"
            autocomplete="new-password"
            class="flex h-10 w-full rounded-[var(--radius)] border border-[var(--color-border)] bg-[var(--color-background)] px-3 py-2 text-sm placeholder:text-[var(--color-muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1 transition-colors"
            :class="form.confirm && form.password !== form.confirm ? 'border-red-500 focus:ring-red-400' : ''"
            @keyup.enter="handleRegister"
          />
          <p v-if="form.confirm && form.password !== form.confirm" class="mt-1 text-xs text-red-500">两次密码不一致</p>
        </div>

        <div v-if="error" class="rounded-[var(--radius)] bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">
          {{ error }}
        </div>

        <Button type="submit" class="w-full" :disabled="loading">
          <Loader2 v-if="loading" class="h-4 w-4 animate-spin" />
          {{ loading ? '注册中...' : '注册' }}
        </Button>
      </form>

      <p class="mt-6 text-center text-sm text-[var(--color-muted-foreground)]">
        已有账号？
        <router-link to="/login" class="font-medium text-purple-600 hover:text-purple-700 dark:text-purple-400 transition-colors">立即登录</router-link>
      </p>
    </Card>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { UserPlus, Eye, EyeOff, Loader2 } from 'lucide-vue-next'
import AuthLayout from '@/layouts/AuthLayout.vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
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
  if (pw.length >= 12) return 3
  if (pw.length >= 8) return 2
  if (pw.length >= 6) return 1
  return 0
})

const strengthColor = computed(() => {
  if (strengthLevel.value === 3) return 'bg-emerald-500'
  if (strengthLevel.value === 2) return 'bg-amber-500'
  return 'bg-red-400'
})

onMounted(() => {
  usernameRef.value?.focus()
})

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
    router.push('/skills')
  } catch (e: unknown) {
    error.value = (e as Error).message || '注册失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}
</script>
