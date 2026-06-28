<template>
  <div class="flex min-h-screen items-center justify-center bg-[var(--color-muted)]/30 px-4 py-12">
    <div class="w-full max-w-md">
      <div class="mb-8 text-center">
        <router-link to="/" class="inline-flex items-center gap-2 text-sm text-[var(--color-muted-foreground)] transition-colors hover:text-[var(--color-foreground)]">
          <ArrowLeft class="h-4 w-4" />
          返回首页
        </router-link>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
</script>
