<template>
  <AppLayout>
    <div class="mb-10">
      <h1 class="text-2xl font-bold tracking-tight">Skill Marketplace</h1>
      <p class="mt-2 text-sm text-[var(--color-muted-foreground)]">探索 AI 能力，一键生成专属分析报告。新 Skill 持续添加中。</p>
    </div>

    <div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="relative w-full max-w-sm">
        <Search class="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--color-muted-foreground)]" />
        <input v-model="search" type="text" placeholder="搜索 Skills..."
          class="h-11 w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-background)] pl-10 pr-4 text-sm placeholder:text-[var(--color-muted-foreground)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1" />
      </div>
      <div class="flex flex-wrap gap-2">
        <button v-for="cat in categories" :key="cat"
          class="rounded-full px-3.5 py-1.5 text-xs font-medium transition-all duration-150"
          :class="activeCategory === cat ? 'bg-purple-600 text-white shadow-sm' : 'border border-[var(--color-border)] bg-[var(--color-card)] text-[var(--color-muted-foreground)] hover:bg-[var(--color-muted)] hover:text-[var(--color-foreground)]'"
          @click="activeCategory = activeCategory === cat ? 'All' : cat">{{ cat }}</button>
      </div>
    </div>

    <p class="mb-5 text-xs text-[var(--color-muted-foreground)]">{{ filteredSkills.length }} Skill{{ filteredSkills.length !== 1 ? 's' : '' }} <span v-if="activeCategory !== 'All'"> · {{ activeCategory }}</span></p>

    <StateWrapper :loading="skillStore.loading" :error="error" :empty="filteredSkills.length === 0 && !skillStore.loading && !error"
      :empty-description="search ? '没有匹配的 Skill' : '暂无可用 Skill'" :retry="fetchSkills">
      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <SkillCard v-for="(skill, i) in filteredSkills" :key="skill.id" :skill="skill" :index="i" @click="$router.push(`/skill/${skill.id}`)" />
      </div>
    </StateWrapper>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Search } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
import StateWrapper from '@/components/shared/StateWrapper.vue'
import SkillCard from '@/components/shared/SkillCard.vue'
import { useSkillStore } from '@/stores/skill'
const skillStore = useSkillStore()
const search = ref(''); const activeCategory = ref('All'); const error = ref<string | null>(null)
const categories = computed(() => { const cats = new Set(skillStore.skills.map(s => s.category).filter(Boolean) as string[]); return ['All', ...Array.from(cats)] })
const filteredSkills = computed(() => { let list = skillStore.skills; if (activeCategory.value !== 'All') list = list.filter(s => s.category === activeCategory.value); if (search.value.trim()) { const q = search.value.toLowerCase(); list = list.filter(s => s.display_name.toLowerCase().includes(q) || s.description?.toLowerCase().includes(q) || s.category?.toLowerCase().includes(q) || s.id.toLowerCase().includes(q)) } return list })
onMounted(() => { fetchSkills() })
async function fetchSkills() { error.value = null; try { await skillStore.fetchSkills() } catch (e: unknown) { error.value = (e as Error).message || '加载失败' } }
</script>
