<template>
  <section class="relative overflow-hidden px-4 pb-16 pt-28 sm:pb-20 sm:pt-36 lg:pb-28 lg:pt-44">
    <!-- Background -->
    <div class="absolute inset-0 bg-gradient-to-b from-purple-50/60 via-transparent to-transparent dark:from-purple-950/20" />
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_60%_50%_at_50%_0%,rgba(124,58,237,0.08),transparent)] dark:bg-[radial-gradient(ellipse_60%_50%_at_50%_0%,rgba(167,139,250,0.06),transparent)]" />

    <div class="relative mx-auto max-w-4xl text-center">
      <!-- Badge -->
      <div class="mb-8 inline-flex items-center gap-2 rounded-full border border-purple-200 bg-purple-50/80 px-4 py-1.5 text-sm font-medium text-purple-700 backdrop-blur-sm dark:border-purple-800 dark:bg-purple-950/60 dark:text-purple-300">
        <Sparkles class="h-4 w-4" />
        AI-Powered Report Generation Platform
      </div>

      <h1 class="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl leading-tight">
        用 AI 生成
        <span class="bg-gradient-to-r from-purple-600 via-violet-500 to-purple-600 bg-clip-text text-transparent">个性化分析报告</span>
      </h1>

      <p class="mx-auto mt-6 max-w-xl text-lg text-[var(--color-muted-foreground)] leading-relaxed">
        InsightForge 是基于插件的 AI 报告生成平台。选择分析类型、输入参数，AI 自动生成精美报告。
      </p>

      <div class="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
        <router-link :to="isLoggedIn ? '/dashboard' : '/register'"
          class="inline-flex h-12 items-center gap-2 rounded-xl bg-purple-600 px-8 text-sm font-semibold text-white shadow-lg shadow-purple-500/25 transition-all hover:bg-purple-700 hover:shadow-xl hover:shadow-purple-500/30 active:scale-[0.98]">
          {{ isLoggedIn ? '开始输出你的报告' : '免费开始使用' }}
        </router-link>
        <a href="#features"
          class="inline-flex h-12 items-center rounded-xl border border-[var(--color-border)] bg-[var(--color-card)] px-8 text-sm font-medium text-[var(--color-foreground)] shadow-sm transition-all hover:bg-[var(--color-muted)] hover:shadow-md active:scale-[0.98]">
          了解更多
        </a>
      </div>

      <!-- Stats -->
      <div class="mt-20 grid grid-cols-3 gap-6 border-t border-[var(--color-border)] pt-14">
        <div v-for="stat in stats" :key="stat.label" class="text-center">
          <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">{{ stat.value }}</div>
          <div class="mt-2 text-sm text-[var(--color-muted-foreground)]">{{ stat.label }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Sparkles } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const isLoggedIn = computed(() => !!auth.token)

const stats = [
  { value: '5+', label: 'AI 分析类型' },
  { value: '100%', label: '插件化架构' },
  { value: '秒级', label: '报告生成速度' },
]
</script>
