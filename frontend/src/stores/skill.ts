import { defineStore } from 'pinia'
import { ref } from 'vue'
import { skillApi, type SkillManifest } from '@/api/skill'

export const useSkillStore = defineStore('skill', () => {
  const skills = ref<SkillManifest[]>([])
  const loading = ref(false)

  async function fetchSkills() {
    loading.value = true
    try {
      const res = await skillApi.list()
      skills.value = res.skills
    } finally {
      loading.value = false
    }
  }

  function getSkill(id: string): SkillManifest | undefined {
    return skills.value.find((s) => s.id === id)
  }

  return { skills, loading, fetchSkills, getSkill }
})
