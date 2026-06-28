<template>
  <AppLayout>
    <button class="mb-6 inline-flex items-center gap-1.5 text-sm text-[var(--color-muted-foreground)] transition-colors hover:text-[var(--color-foreground)]" @click="$router.push('/skills')"><ArrowLeft class="h-4 w-4" />返回 Skills</button>
    <div class="mb-8">
      <h1 class="text-2xl font-bold tracking-tight">{{ skill?.display_name }}</h1>
      <p v-if="skill?.description" class="mt-2 text-sm text-[var(--color-muted-foreground)]">{{ skill.description }}</p>
    </div>

    <div v-if="skill" class="mx-auto max-w-xl">
      <div v-if="skill.parameters && Object.keys(skill.parameters).length" class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-6 shadow-sm">
        <h3 class="mb-5 text-sm font-semibold">参数设置</h3>
        <form class="space-y-5" @submit.prevent="handleGenerate">
          <div v-for="(field, key) in skill.parameters" :key="key">
            <label class="mb-2 block text-sm font-medium">{{ field.label }}<span v-if="field.required !== false" class="ml-1 text-red-500">*</span></label>
            <select v-if="field.type === 'select' && field.options" v-model="params[key]"
              class="h-11 w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-background)] px-4 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1">
              <option value="" disabled>请选择</option>
              <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
            </select>
            <input v-else-if="field.type === 'number'" v-model.number="params[key]" type="number" :min="field.min" :max="field.max" :placeholder="field.placeholder || `请输入${field.label}`"
              class="h-11 w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-background)] px-4 text-sm placeholder:text-[var(--color-muted-foreground)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1" />
            <input v-else v-model="params[key]" type="text" :placeholder="field.placeholder || `请输入${field.label}`"
              class="h-11 w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-background)] px-4 text-sm placeholder:text-[var(--color-muted-foreground)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--color-ring)] focus:ring-offset-1" />
          </div>
          <div v-if="genError" class="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">{{ genError }}</div>
          <Button type="submit" class="w-full" :disabled="generating"><Loader2 v-if="generating" class="h-4 w-4 animate-spin" />{{ generating ? '正在生成报告...' : '生成报告' }}</Button>
        </form>
      </div>
      <div v-else class="rounded-2xl border border-[var(--color-border)] bg-[var(--color-card)] p-8 text-center shadow-sm">
        <p class="text-sm text-[var(--color-muted-foreground)]">此 Skill 无需额外参数，可直接生成报告。</p>
        <Button class="mt-5 w-full" :disabled="generating" @click="handleGenerate"><Loader2 v-if="generating" class="h-4 w-4 animate-spin" />{{ generating ? '正在生成报告...' : '生成报告' }}</Button>
      </div>
    </div>
    <EmptyState v-else description="Skill 不存在" />
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Loader2 } from 'lucide-vue-next'
import AppLayout from '@/layouts/AppLayout.vue'
import Button from '@/components/ui/Button.vue'
import EmptyState from '@/components/shared/EmptyState.vue'
import { useSkillStore } from '@/stores/skill'
import { reportApi } from '@/api/report'
const route = useRoute(); const router = useRouter(); const skillStore = useSkillStore()
const skillId = computed(() => route.params.skillId as string)
const skill = computed(() => skillStore.getSkill(skillId.value))
const params = reactive<Record<string, unknown>>({}); const generating = ref(false); const genError = ref('')
function initDefaults() { const s = skill.value; if (!s?.parameters) return; for (const [key, field] of Object.entries(s.parameters)) { if (field.default !== undefined) params[key] = field.default } }
onMounted(async () => { if (!skillStore.skills.length) await skillStore.fetchSkills(); initDefaults() })
async function handleGenerate() { genError.value = ''; generating.value = true; try { const res = await reportApi.generate({ skill_id: skillId.value, parameters: cleanParams() }); if (res.success) router.push(`/report/${res.report_id}`); else genError.value = res.error || '生成失败' } catch (e: unknown) { genError.value = (e as Error).message || '生成失败，请检查网络连接' } finally { generating.value = false } }
function cleanParams(): Record<string, unknown> { const r: Record<string, unknown> = {}; for (const [k, v] of Object.entries(params)) { if (v !== '' && v !== undefined) r[k] = v }; return r }
</script>
