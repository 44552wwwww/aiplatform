<template>
  <AppLayout>
    <div class="page-header">
      <h1 class="page-title">Skill Marketplace</h1>
      <p class="page-desc">探索 AI 能力，一键生成专属分析报告。新 Skill 持续添加中。</p>
    </div>

    <!-- 搜索和分类筛选 -->
    <div class="flex flex-col gap-4 mb-8 sm:flex-row sm:items-center sm:justify-between">
      <div class="search-bar" style="max-width: 360px;">
        <span class="search-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
        </span>
        <input v-model="search" type="text" class="search-input" placeholder="搜索 Skills..." />
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="cat in categories"
          :key="cat"
          class="skill-badge"
          :class="{ '!bg-[var(--brand-primary)] !text-white': activeCategory === cat }"
          style="cursor:pointer; transition: all var(--transition-fast);"
          @click="activeCategory = activeCategory === cat ? 'All' : cat"
        >{{ cat }}</button>
      </div>
    </div>

    <p class="mb-5 text-xs text-[var(--text-muted)]">
      {{ filteredSkills.length }} Skill{{ filteredSkills.length !== 1 ? 's' : '' }}
      <span v-if="activeCategory !== 'All'"> · {{ activeCategory }}</span>
    </p>

    <!-- Loading / Error / Empty -->
    <div v-if="skillStore.loading" class="empty-state">
      <span class="loading-spinner" style="margin: 0 auto 1rem;" />
      <div class="empty-state-desc">加载中...</div>
    </div>
    <div v-else-if="error" class="empty-state">
      <div class="empty-state-icon">⚠️</div>
      <div class="empty-state-desc">{{ error }}</div>
      <button class="btn btn-primary" @click="fetchSkills">重试</button>
    </div>
    <div v-else-if="filteredSkills.length === 0" class="empty-state">
      <div class="empty-state-icon">{{ search ? '🔍' : '🧩' }}</div>
      <div class="empty-state-title">{{ search ? '没有匹配的 Skill' : '暂无可用 Skill' }}</div>
      <div class="empty-state-desc">{{ search ? '尝试其他关键词' : '' }}</div>
    </div>

    <!-- Skills Grid -->
    <div v-else class="skills-grid">
      <div v-for="skill in filteredSkills" :key="skill.id" class="skill-card glass-card" @click="$router.push(`/skill/${skill.id}`)">
        <div class="skill-card-header">
          <div class="skill-icon">{{ skillIcon(skill) }}</div>
          <span class="skill-badge">{{ skill.category || 'general' }}</span>
        </div>
        <h3 class="skill-title">{{ skill.display_name }}</h3>
        <p class="skill-desc">{{ skill.description || '暂无描述' }}</p>
        <div class="skill-footer">
          <span>By InsightForge</span>
          <span>{{ skill.version || 'v1.0.0' }}</span>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { useSkillStore } from '@/stores/skill'

const skillStore = useSkillStore()
const search = ref('')
const activeCategory = ref('All')
const error = ref<string | null>(null)

const categories = computed(() => {
  const cats = new Set(skillStore.skills.map(s => s.category).filter(Boolean) as string[])
  return ['All', ...Array.from(cats)]
})

const filteredSkills = computed(() => {
  let list = skillStore.skills
  if (activeCategory.value !== 'All') list = list.filter(s => s.category === activeCategory.value)
  if (search.value.trim()) {
    const q = search.value.toLowerCase()
    list = list.filter(s =>
      s.display_name.toLowerCase().includes(q) ||
      s.description?.toLowerCase().includes(q) ||
      s.category?.toLowerCase().includes(q) ||
      s.id.toLowerCase().includes(q)
    )
  }
  return list
})

function skillIcon(skill: { id: string; category?: string }): string {
  const icons: Record<string, string> = { bazi: '🔮', career: '💼', business: '📊', resume: '📝', psychology: '🧠' }
  return icons[skill.id] || icons[skill.category || ''] || '🧩'
}

onMounted(() => { fetchSkills() })

async function fetchSkills() {
  error.value = null
  try { await skillStore.fetchSkills() } catch (e: unknown) { error.value = (e as Error).message || '加载失败' }
}
</script>
