<template>
  <section id="features" class="px-4 py-24">
    <div class="mx-auto max-w-6xl">
      <div class="mb-16 text-center">
        <h2 class="text-3xl font-bold tracking-tight">强大的平台能力</h2>
        <p class="mt-3 text-[var(--color-muted-foreground)]">为 AI 报告生成而生的完整基础设施</p>
      </div>

      <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
        <Card v-for="(f, i) in features" :key="i" class="group transition-shadow hover:shadow-md">
          <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100 text-purple-600 dark:bg-purple-900/40 dark:text-purple-400">
            <component :is="f.icon" class="h-6 w-6" />
          </div>
          <h3 class="mb-2 font-semibold">{{ f.title }}</h3>
          <p class="text-sm text-[var(--color-muted-foreground)] leading-relaxed">{{ f.desc }}</p>
        </Card>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Bot, Shield, LayoutDashboard, Plug, Database, Rocket } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'

const features = [
  { icon: Bot, title: 'AI 驱动分析', desc: '接入 DeepSeek、OpenAI 等大语言模型，自动生成深度分析内容' },
  { icon: Plug, title: '插件化 Skill', desc: '新增分析类型只需添加 Skill 目录，无需修改平台代码' },
  { icon: Shield, title: 'JWT 安全认证', desc: 'bcrypt 密码哈希 + JWT 令牌，用户数据安全隔离' },
  { icon: LayoutDashboard, title: '精美 HTML 报告', desc: 'AI 生成的报告自动渲染为精美网页，支持直接查看和分享' },
  { icon: Database, title: '数据持久化', desc: 'SQLite 开发零配置，PostgreSQL 生产部署，报告永久保存' },
  { icon: Rocket, title: '一键部署', desc: 'Docker Compose 本地启动，Railway 云平台一键上线' },
]
</script>
