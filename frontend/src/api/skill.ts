import { api } from './client'

export interface SkillManifest {
  id: string
  display_name: string
  version: string
  author?: string
  description?: string
  icon?: string
  category?: string
  entry?: string
  output?: string
  parameters?: Record<string, SkillParameter>
}

export interface SkillParameter {
  type: 'number' | 'string' | 'select' | 'textarea'
  label: string
  required?: boolean
  options?: string[]
  min?: number
  max?: number
  placeholder?: string
  default?: unknown
}

export interface SkillListResponse {
  skills: SkillManifest[]
}

export const skillApi = {
  list() {
    return api.get<SkillListResponse>('/skill/list')
  },
}
