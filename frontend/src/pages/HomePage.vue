<template>
  <div class="page-container">
    <div class="page-header">
      <h1>AI 个性化分析平台</h1>
      <p class="subtitle">选择一项 AI 能力，生成专属分析报告</p>
    </div>

    <StateWrapper
      :loading="skillStore.loading"
      :error="error"
      :empty="!skillStore.loading && skillStore.skills.length === 0 && !error"
      empty-description="暂无可用 Skill"
      :retry="fetchSkills"
    >
      <div class="skill-grid">
        <el-card
          v-for="skill in skillStore.skills"
          :key="skill.id"
          class="skill-card"
          shadow="hover"
          @click="goSkill(skill.id)"
        >
          <div class="skill-icon">{{ getIcon(skill.icon) }}</div>
          <h3>{{ skill.display_name }}</h3>
          <p class="skill-desc">{{ skill.description || '暂无描述' }}</p>
          <el-tag size="small" type="info">{{ skill.category || '通用' }}</el-tag>
        </el-card>
      </div>
    </StateWrapper>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSkillStore } from '@/stores/skill'
import StateWrapper from '@/components/StateWrapper.vue'

const skillStore = useSkillStore()
const router = useRouter()
const error = ref<string | null>(null)

onMounted(() => {
  fetchSkills()
})

async function fetchSkills() {
  error.value = null
  try {
    await skillStore.fetchSkills()
  } catch (e: unknown) {
    error.value = (e as Error).message || '加载 Skill 列表失败'
  }
}

function goSkill(skillId: string) {
  router.push(`/skill/${skillId}`)
}

function getIcon(icon?: string): string {
  const map: Record<string, string> = {
    compass: '🔮',
    document: '📄',
    career: '💼',
    psychology: '🧠',
    study: '📚',
    business: '📊',
  }
  return map[icon || ''] || '✨'
}
</script>

<style scoped>
.subtitle {
  color: #909399;
  margin-top: 8px;
}
.skill-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
.skill-card {
  cursor: pointer;
  transition: transform 0.2s;
}
.skill-card:hover {
  transform: translateY(-4px);
}
.skill-icon {
  font-size: 2.4em;
  margin-bottom: 12px;
}
.skill-card h3 {
  margin-bottom: 8px;
  color: #1a1a2e;
}
.skill-desc {
  color: #909399;
  font-size: 0.9em;
  margin-bottom: 12px;
  min-height: 40px;
}
</style>
