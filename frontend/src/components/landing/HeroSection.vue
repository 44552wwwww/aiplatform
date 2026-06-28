<template>
  <section class="relative overflow-hidden px-4 py-24 sm:py-32 lg:py-40">
    <!-- Background gradient -->
    <div class="absolute inset-0 bg-gradient-to-b from-purple-50/80 via-transparent to-transparent dark:from-purple-950/20" />
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-200/40 via-transparent to-transparent dark:from-purple-800/10" />

    <div class="relative mx-auto max-w-5xl text-center">
      <!-- Badge -->
      <div class="mb-6 inline-flex items-center gap-2 rounded-full border border-purple-200 bg-purple-50 px-4 py-1.5 text-sm font-medium text-purple-700 dark:border-purple-800 dark:bg-purple-950 dark:text-purple-300">
        <Sparkles class="h-4 w-4" />
        AI-Powered Report Generation
      </div>

      <h1 class="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
        用 AI 生成
        <span class="bg-gradient-to-r from-purple-600 to-violet-500 bg-clip-text text-transparent">个性化分析报告</span>
      </h1>

      <p class="mx-auto mt-6 max-w-2xl text-lg text-[var(--color-muted-foreground)] leading-relaxed">
        InsightForge 是一个基于插件的 AI 报告生成平台。选择分析类型、输入参数，AI 自动生成精美的 HTML 报告。支持八字命理、职业规划、简历分析等。
      </p>

      <div class="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
        <Button size="lg" class="min-w-[160px] shadow-lg shadow-purple-500/25" @click="$router.push(isLoggedIn ? '/dashboard' : '/register')">
          {{ isLoggedIn ? '进入控制台' : '免费开始使用' }}
        </Button>
        <Button size="lg" variant="outline" class="min-w-[160px]" @click="scrollTo('#features')">
          了解更多
        </Button>
      </div>

      <!-- Stats -->
      <div class="mt-16 grid grid-cols-3 gap-8 border-t border-[var(--color-border)] pt-12">
        <div v-for="stat in stats" :key="stat.label">
          <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">{{ stat.value }}</div>
          <div class="mt-1 text-sm text-[var(--color-muted-foreground)]">{{ stat.label }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const auth = useAuthStore()
const isLoggedIn = computed(() => !!auth.token)

const stats = [
  { value: '5+', label: 'AI 分析类型' },
  { value: '100%', label: '插件化架构' },
  { value: '秒级', label: '报告生成速度' },
]

function scrollTo(selector: string) {
  document.querySelector(selector)?.scrollIntoView({ behavior: 'smooth' })
}
</script>
