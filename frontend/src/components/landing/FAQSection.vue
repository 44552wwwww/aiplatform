<template>
  <section id="faq" class="px-4 py-24">
    <div class="mx-auto max-w-2xl">
      <div class="mb-12 text-center">
        <h2 class="text-3xl font-bold tracking-tight">常见问题</h2>
      </div>

      <div class="space-y-3">
        <div
          v-for="(item, i) in faqs" :key="i"
          class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] shadow-sm transition-all duration-200 hover:shadow-md"
        >
          <button
            class="flex w-full items-center justify-between px-6 py-5 text-left font-medium transition-colors"
            @click="toggle(i)"
          >
            <span class="pr-4">{{ item.q }}</span>
            <ChevronDown
              class="h-5 w-5 shrink-0 text-[var(--color-muted-foreground)] transition-transform duration-200"
              :class="open === i && 'rotate-180'"
            />
          </button>
          <div
            v-if="open === i"
            class="border-t border-[var(--color-border)] px-6 pb-5 pt-4 text-sm text-[var(--color-muted-foreground)] leading-relaxed"
          >
            {{ item.a }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ChevronDown } from 'lucide-vue-next'

const open = ref<number | null>(null)
function toggle(i: number) { open.value = open.value === i ? null : i }

const faqs = [
  { q: 'InsightForge 是什么？', a: 'InsightForge 是一个基于插件架构的 AI 报告生成平台。平台提供用户系统、数据存储、AI 调度等基础设施，每个 Skill 封装一种 AI 分析能力（如八字命理、职业规划等）。' },
  { q: '如何新增一种分析类型？', a: '只需在 skills/ 目录下新建一个文件夹，编写 manifest.json（参数定义）、workflow.py（业务逻辑）、prompt.md（AI 提示词）和 renderer.py（HTML 渲染），平台自动发现并注册，无需修改任何平台代码。' },
  { q: '支持哪些 AI 模型？', a: '支持所有 OpenAI Chat Completions 兼容接口的模型，包括 OpenAI GPT-4、DeepSeek、Qwen、OpenRouter、vLLM、Ollama 等。通过环境变量切换，无需修改代码。' },
  { q: '我的数据安全吗？', a: '用户密码使用 bcrypt 哈希存储，JWT 令牌管理登录状态。每个用户只能访问自己的报告，严格的权限隔离确保数据安全。' },
]
</script>
