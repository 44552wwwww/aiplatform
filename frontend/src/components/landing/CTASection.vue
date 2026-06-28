<template>
  <section class="px-4 py-24">
    <div class="mx-auto max-w-3xl rounded-3xl bg-gradient-to-br from-purple-600 via-violet-500 to-purple-700 p-14 text-center text-white shadow-xl shadow-purple-500/20">
      <h2 class="text-3xl font-bold">{{ isLoggedIn ? '欢迎回来' : '准备好开始了吗？' }}</h2>
      <p class="mt-4 text-purple-100 text-lg">{{ isLoggedIn ? '进入控制台，开始输出你的专属 AI 报告。' : '免费注册，立即体验 AI 生成的个性化报告。' }}</p>
      <div class="mt-8">
        <router-link :to="isLoggedIn ? '/dashboard' : '/register'"
          class="inline-flex h-12 items-center rounded-xl bg-white px-10 text-sm font-semibold text-purple-700 shadow-md transition-all hover:bg-purple-50 hover:shadow-lg active:scale-[0.98]">
          {{ isLoggedIn ? '开始输出你的报告' : '创建免费账号' }}
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isLoggedIn = computed(() => !!auth.token)
</script>
