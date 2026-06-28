<template>
  <footer class="border-t border-[var(--color-border)] bg-[var(--color-muted)]/30 px-4 py-12">
    <div class="mx-auto max-w-6xl">
      <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
        <div class="flex items-center gap-2 text-sm font-semibold">
          <Sparkles class="h-4 w-4 text-purple-600" />
          InsightForge
        </div>
        <div class="flex items-center gap-6 text-sm text-[var(--color-muted-foreground)]">
          <a href="#features" class="hover:text-[var(--color-foreground)] transition-colors">功能</a>
          <a href="#faq" class="hover:text-[var(--color-foreground)] transition-colors">常见问题</a>
          <a href="https://github.com/44552wwwww/aiplatform" target="_blank" class="hover:text-[var(--color-foreground)] transition-colors">GitHub</a>
        </div>
        <p class="text-sm text-[var(--color-muted-foreground)]">
          &copy; {{ year }} InsightForge-AI. MIT License.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
const year = new Date().getFullYear()
</script>
