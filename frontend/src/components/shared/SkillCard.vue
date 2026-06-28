<template>
  <div
    class="group relative cursor-pointer rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm transition-all duration-200 hover:shadow-lg hover:shadow-purple-500/5 hover:-translate-y-0.5 hover:border-purple-200 dark:hover:border-purple-800"
    @click="$emit('click')"
  >
    <div class="mb-4 flex items-start justify-between">
      <div class="flex h-12 w-12 items-center justify-center rounded-xl text-2xl" :class="iconBg">{{ displayIcon }}</div>
      <span v-if="skill.category" class="rounded-full border border-[var(--color-border)] bg-[var(--color-muted)] px-2.5 py-0.5 text-xs font-medium text-[var(--color-muted-foreground)]">{{ skill.category }}</span>
    </div>
    <h3 class="mb-1.5 text-base font-semibold leading-tight">{{ skill.display_name }}</h3>
    <p class="mb-4 line-clamp-2 text-sm leading-relaxed text-[var(--color-muted-foreground)]">{{ skill.description || '暂无描述' }}</p>
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2 text-xs text-[var(--color-muted-foreground)]">
        <span v-if="skill.author">{{ skill.author }}</span>
        <span v-if="skill.author" class="text-[var(--color-border)]">·</span>
        <span class="rounded bg-[var(--color-muted)] px-1.5 py-0.5 font-mono text-xs">v{{ skill.version }}</span>
      </div>
      <span class="flex h-7 w-7 items-center justify-center rounded-full bg-purple-50 text-purple-600 opacity-0 transition-all group-hover:opacity-100 dark:bg-purple-950 dark:text-purple-400">
        <ArrowRight class="h-4 w-4" />
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ArrowRight } from 'lucide-vue-next'
import type { SkillManifest } from '@/api/skill'

const props = defineProps<{ skill: SkillManifest; index: number }>()
defineEmits<{ click: [] }>()

const iconBgs = ['bg-purple-100 text-purple-600 dark:bg-purple-900/40 dark:text-purple-400','bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-400','bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-400','bg-amber-100 text-amber-600 dark:bg-amber-900/40 dark:text-amber-400','bg-rose-100 text-rose-600 dark:bg-rose-900/40 dark:text-rose-400','bg-cyan-100 text-cyan-600 dark:bg-cyan-900/40 dark:text-cyan-400']
const iconMap: Record<string, string> = { compass: '🔮', document: '📄', career: '💼', psychology: '🧠', study: '📚', business: '📊', code: '💻', chart: '📈', robot: '🤖', heart: '❤️', star: '⭐', globe: '🌐' }
const displayIcon = computed(() => iconMap[props.skill.icon || ''] || '✨')
const iconBg = computed(() => iconBgs[props.index % iconBgs.length])
</script>
