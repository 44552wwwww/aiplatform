<template>
  <section class="px-4 py-24">
    <div class="mx-auto max-w-3xl rounded-2xl bg-gradient-to-br from-purple-600 to-violet-500 p-12 text-center text-white shadow-xl shadow-purple-500/20">
      <h2 class="text-3xl font-bold">{{ isLoggedIn ? '欢迎回来' : '准备好开始了吗？' }}</h2>
      <p class="mt-3 text-purple-100">{{ isLoggedIn ? '进入控制台，查看你的报告或探索新的 AI 能力。' : '免费注册，立即体验 AI 生成的个性化报告。' }}</p>
      <div class="mt-8">
        <Button
          size="lg"
          class="bg-white text-purple-700 hover:bg-purple-50 min-w-[160px] shadow-md"
          @click="$router.push(isLoggedIn ? '/dashboard' : '/register')"
        >
          {{ isLoggedIn ? '进入控制台' : '创建免费账号' }}
        </Button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Button from '@/components/ui/Button.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isLoggedIn = computed(() => !!auth.token)
</script>
