<template>
  <section class="px-4 py-24">
    <div class="mx-auto max-w-3xl rounded-2xl bg-gradient-to-br from-purple-600 to-violet-500 p-12 text-center text-white shadow-xl shadow-purple-500/20">
      <h2 class="text-3xl font-bold">准备好开始了吗？</h2>
      <p class="mt-3 text-purple-100">免费注册，立即体验 AI 生成的个性化报告。</p>
      <div class="mt-8">
        <Button
          size="lg"
          class="bg-white text-purple-700 hover:bg-purple-50 min-w-[160px] shadow-md"
          @click="$router.push('/register')"
        >
          创建免费账号
        </Button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import Button from '@/components/ui/Button.vue'
</script>
