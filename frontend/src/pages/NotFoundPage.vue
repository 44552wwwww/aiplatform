<template>
  <div class="flex min-h-screen flex-col items-center justify-center px-4 text-center">
    <h1 class="text-8xl font-bold text-[var(--color-border)]">404</h1>
    <p class="mt-4 text-lg text-[var(--color-muted-foreground)]">页面不存在</p>
    <Button class="mt-8" @click="$router.push('/')">返回首页</Button>
  </div>
</template>

<script setup lang="ts">
import Button from '@/components/ui/Button.vue'
</script>
