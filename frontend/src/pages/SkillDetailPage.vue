<template>
  <AppLayout>
    <a class="back-link" @click.prevent="$router.push('/skills')">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" />
      </svg>
      返回 Skills
    </a>

    <!-- Skill 详情头部 -->
    <div v-if="skill" class="skill-detail-header">
      <div class="skill-detail-icon">{{ skillIcon }}</div>
      <div>
        <h1 class="skill-detail-title">{{ skill.display_name }}</h1>
        <p class="skill-detail-desc">{{ skill.description }}</p>
      </div>
    </div>

    <!-- 参数表单 -->
    <div v-if="skill" class="mx-auto" style="max-width: 560px;">
      <div v-if="skill.parameters && Object.keys(skill.parameters).length" class="panel glass-card">
        <div class="panel-header">
          <h3 class="panel-title">参数设置</h3>
        </div>
        <form class="auth-form" @submit.prevent="handleGenerate">
          <div v-for="(field, key) in skill.parameters" :key="key" class="form-group">
            <label class="form-label">
              {{ field.label }}<span v-if="field.required !== false" style="color: #ef4444; margin-left: 2px;">*</span>
            </label>
            <select
              v-if="field.type === 'select' && field.options"
              v-model="params[key]"
              class="form-input form-select"
            >
              <option value="" disabled>请选择</option>
              <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
            </select>
            <input
              v-else-if="field.type === 'number'"
              v-model.number="params[key]"
              type="number"
              :min="field.min" :max="field.max"
              :placeholder="field.placeholder || `请输入${field.label}`"
              class="form-input"
            />
            <textarea
              v-else-if="field.type === 'textarea'"
              v-model="params[key]"
              :placeholder="field.placeholder || `请输入${field.label}`"
              class="form-input"
              rows="8"
              style="resize: vertical; min-height: 120px;"
            />
            <input
              v-else
              v-model="params[key]"
              type="text"
              :placeholder="field.placeholder || `请输入${field.label}`"
              class="form-input"
            />
          </div>
          <div v-if="genError" class="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300 mb-4">{{ genError }}</div>
          <button type="submit" class="btn btn-primary btn-lg btn-full generate-btn" :class="{ 'btn-loading': generating }" :disabled="generating">
            <span v-if="generating" class="loading-spinner" />{{ generating ? '正在生成报告...' : '✨ 生成报告' }}
          </button>
        </form>
      </div>
      <div v-else class="panel glass-card text-center" style="padding: var(--spacing-2xl);">
        <p class="text-sm text-[var(--text-secondary)]">此 Skill 无需额外参数，可直接生成报告。</p>
        <button class="btn btn-primary btn-lg btn-full" style="margin-top: var(--spacing-lg);" :class="{ 'btn-loading': generating }" :disabled="generating" @click="handleGenerate">
          <span v-if="generating" class="loading-spinner" />{{ generating ? '正在生成报告...' : '✨ 生成报告' }}
        </button>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-state-icon">🔍</div>
      <div class="empty-state-title">Skill 不存在</div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import { useSkillStore } from '@/stores/skill'
import { reportApi } from '@/api/report'

const route = useRoute()
const router = useRouter()
const skillStore = useSkillStore()
const skillId = computed(() => route.params.skillId as string)
const skill = computed(() => skillStore.getSkill(skillId.value))
const params = reactive<Record<string, unknown>>({})
const generating = ref(false)
const genError = ref('')

const skillIcon = computed(() => {
  const icons: Record<string, string> = { bazi: '🔮', career: '💼', business: '📊' }
  return icons[skill.value?.id || ''] || '🧩'
})

function initDefaults() {
  const s = skill.value
  if (!s?.parameters) return
  for (const [key, field] of Object.entries(s.parameters)) {
    if (field.default !== undefined) params[key] = field.default
  }
}

onMounted(async () => {
  if (!skillStore.skills.length) await skillStore.fetchSkills()
  initDefaults()
})

async function handleGenerate() {
  genError.value = ''
  generating.value = true
  try {
    const res = await reportApi.generate({ skill_id: skillId.value, parameters: cleanParams() })
    if (res.success) router.push(`/report/${res.report_id}`)
    else genError.value = res.error || '生成失败'
  } catch (e: unknown) {
    genError.value = (e as Error).message || '生成失败，请检查网络连接'
  } finally { generating.value = false }
}

function cleanParams(): Record<string, unknown> {
  const r: Record<string, unknown> = {}
  for (const [k, v] of Object.entries(params)) { if (v !== '' && v !== undefined) r[k] = v }
  return r
}
</script>
