import { api } from './client'

export interface ReportItem {
  id: number
  skill_id: string
  title: string
  created_at: string
}

export interface ReportDetail {
  id: number
  skill_id: string
  title: string
  html: string | null
  metadata: Record<string, unknown> | null
  created_at: string
}

export interface GenerateParams {
  skill_id: string
  parameters: Record<string, unknown>
}

export interface GenerateResponse {
  report_id: string
  success: boolean
  title: string
  html: string
  metadata: Record<string, unknown>
  error: string | null
}

export interface ReportListResponse {
  reports: ReportItem[]
}

export const reportApi = {
  generate(data: GenerateParams) {
    return api.post<GenerateResponse>('/report/generate', data)
  },

  list() {
    return api.get<ReportListResponse>('/report/list')
  },

  detail(id: number) {
    return api.get<ReportDetail>(`/report/${id}`)
  },

  remove(id: number) {
    return api.delete<{ message: string }>(`/report/${id}`)
  },
}
