<template>
  <section class="bg-[var(--color-muted)]/50 px-4 py-24">
    <div class="mx-auto max-w-4xl">
      <div class="mb-16 text-center">
        <h2 class="text-3xl font-bold tracking-tight">三步生成报告</h2>
        <p class="mt-3 text-[var(--color-muted-foreground)]">从选择到生成，几分钟完成</p>
      </div>

      <div class="space-y-8">
        <div v-for="(step, i) in steps" :key="i" class="flex gap-6">
          <div class="flex flex-col items-center">
            <div class="flex h-10 w-10 items-center justify-center rounded-full bg-purple-600 text-sm font-bold text-white shadow-lg shadow-purple-500/25">
              {{ i + 1 }}
            </div>
            <div v-if="i < steps.length - 1" class="mt-2 h-full w-px bg-[var(--color-border)]" />
          </div>
          <div class="pb-8">
            <h3 class="mb-2 font-semibold text-lg">{{ step.title }}</h3>
            <p class="text-sm text-[var(--color-muted-foreground)] leading-relaxed">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const steps = [
  { title: '注册账号', desc: '使用用户名和密码快速注册，JWT 自动管理登录状态。所有数据安全隔离，仅你可见。' },
  { title: '选择分析类型并填写参数', desc: '浏览 Skill 市场，选择感兴趣的分析类型。填写简单的参数（如出生日期、行业等），平台自动校验。' },
  { title: 'AI 生成精美报告', desc: '平台调用大语言模型进行分析，自动渲染为精美的 HTML 报告。报告保存到你的账户，随时查看或删除。' },
]
</script>
