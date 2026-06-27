<template>
  <div class="page-container">
    <div class="page-header">
      <el-button text @click="$router.push('/')">← 返回</el-button>
      <h1 v-if="skill">{{ skill.display_name }}</h1>
      <p v-if="skill" class="desc">{{ skill.description }}</p>
    </div>

    <el-card v-if="skill" class="form-card">
      <el-form :model="params" label-position="top" @submit.prevent="handleGenerate">
        <el-form-item
          v-for="(field, key) in skill.parameters"
          :key="key"
          :label="field.label"
          :required="field.required !== false"
        >
          <el-select
            v-if="field.type === 'select' && field.options"
            v-model="params[key]"
            :placeholder="field.placeholder || '请选择'"
            style="width:100%"
          >
            <el-option
              v-for="opt in field.options"
              :key="opt"
              :label="opt"
              :value="opt"
            />
          </el-select>
          <el-input-number
            v-else-if="field.type === 'number'"
            v-model="params[key]"
            :min="field.min"
            :max="field.max"
            :placeholder="field.placeholder"
            style="width:100%"
          />
          <el-input
            v-else
            v-model="params[key]"
            :placeholder="field.placeholder || '请输入'"
            style="width:100%"
          />
        </el-form-item>

        <div v-if="!skill.parameters" class="no-params">
          <p>此 Skill 无需额外参数，可直接生成报告。</p>
        </div>

        <el-button
          type="primary"
          size="large"
          :loading="generating"
          native-type="submit"
          style="width:100%; margin-top: 16px;"
        >
          {{ generating ? '正在生成报告...' : '生成报告' }}
        </el-button>
      </el-form>
    </el-card>

    <el-empty v-else description="Skill 不存在" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSkillStore } from '@/stores/skill'
import { reportApi } from '@/api/report'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const skillStore = useSkillStore()

const skillId = computed(() => route.params.skillId as string)
const skill = computed(() => skillStore.getSkill(skillId.value))

const params = reactive<Record<string, unknown>>({})
const generating = ref(false)

// 从 manifest 初始化参数默认值
function initDefaults() {
  const s = skill.value
  if (!s?.parameters) return
  for (const [key, field] of Object.entries(s.parameters)) {
    if (field.default !== undefined) {
      params[key] = field.default
    }
  }
}

onMounted(async () => {
  if (!skillStore.skills.length) {
    await skillStore.fetchSkills()
  }
  initDefaults()
})

async function handleGenerate() {
  generating.value = true
  try {
    const res = await reportApi.generate({
      skill_id: skillId.value,
      parameters: { ...params },
    })
    if (res.success) {
      router.push(`/report/${res.report_id}`)
    } else {
      ElMessage.error(res.error || '生成失败')
    }
  } catch (e: unknown) {
    ElMessage.error((e as Error).message || '生成失败')
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.desc {
  color: #909399;
  margin-top: 8px;
}
.form-card {
  max-width: 600px;
  margin: 0 auto;
}
.no-params {
  text-align: center;
  color: #909399;
  padding: 16px;
}
</style>
