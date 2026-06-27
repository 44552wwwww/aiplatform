import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import SkillPage from '../SkillPage.vue'

// Mock stores and API
vi.mock('@/stores/skill', () => ({
  useSkillStore: () => ({
    skills: [
      {
        id: 'bazi',
        display_name: '命运双鉴',
        description: '八字分析',
        parameters: {
          year: { type: 'number', label: '出生年份', required: true, min: 1900, max: 2100, default: 1990 },
          month: { type: 'number', label: '出生月份', required: true, min: 1, max: 12, default: 1 },
          day: { type: 'number', label: '出生日期', required: true, min: 1, max: 31, default: 1 },
          hour: { type: 'number', label: '时辰', required: true, min: 0, max: 23, default: 12 },
          gender: { type: 'select', label: '性别', required: true, options: ['男', '女'], default: '男' },
        },
      },
    ],
    loading: false,
    fetchSkills: vi.fn(),
    getSkill: () => ({
      id: 'bazi',
      display_name: '命运双鉴',
      description: '八字分析',
      parameters: {
        year: { type: 'number', label: '出生年份', required: true, min: 1900, max: 2100, default: 1990 },
        month: { type: 'number', label: '出生月份', required: true, min: 1, max: 12, default: 1 },
        day: { type: 'number', label: '出生日期', required: true, min: 1, max: 31, default: 1 },
        hour: { type: 'number', label: '时辰', required: true, min: 0, max: 23, default: 12 },
        gender: { type: 'select', label: '性别', required: true, options: ['男', '女'], default: '男' },
      },
    }),
  }),
}))

vi.mock('@/api/report', () => ({
  reportApi: {
    generate: vi.fn().mockResolvedValue({
      success: true,
      report_id: '42',
      title: '命运双鉴',
      html: '<html></html>',
      metadata: {},
      error: null,
    }),
  },
}))

function createTestRouter() {
  return createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/skill/:skillId', component: SkillPage },
      { path: '/report/:reportId', component: {} as any },
    ],
  })
}

describe('SkillPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders skill name and description', async () => {
    const router = createTestRouter()
    router.push('/skill/bazi')
    await router.isReady()

    const wrapper = mount(SkillPage, {
      global: { plugins: [createPinia(), router] },
    })
    expect(wrapper.html()).toContain('命运双鉴')
    expect(wrapper.html()).toContain('八字分析')
  })

  it('renders parameter form fields from manifest', async () => {
    const router = createTestRouter()
    router.push('/skill/bazi')
    await router.isReady()

    const wrapper = mount(SkillPage, {
      global: { plugins: [createPinia(), router] },
    })
    expect(wrapper.html()).toContain('出生年份')
    expect(wrapper.html()).toContain('出生月份')
    expect(wrapper.html()).toContain('性别')
  })

  it('shows submit button', async () => {
    const router = createTestRouter()
    router.push('/skill/bazi')
    await router.isReady()

    const wrapper = mount(SkillPage, {
      global: { plugins: [createPinia(), router] },
    })
    expect(wrapper.html()).toContain('生成报告')
  })
})
