import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import HistoryPage from '../HistoryPage.vue'

// Use vi.hoisted to avoid the hoisting issue with vi.mock
const { mockList, mockRemove } = vi.hoisted(() => ({
  mockList: vi.fn().mockResolvedValue({
    reports: [
      { id: 1, skill_id: 'bazi', title: '命运双鉴', created_at: '2026-01-01T00:00:00Z' },
    ],
  }),
  mockRemove: vi.fn().mockResolvedValue({}),
}))

vi.mock('@/api/report', () => ({
  reportApi: {
    list: mockList,
    remove: mockRemove,
  },
}))

function createTestRouter() {
  return createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/history', component: HistoryPage },
      { path: '/report/:reportId', component: {} as any },
    ],
  })
}

describe('HistoryPage', () => {
  beforeEach(() => {
    const pinia = createPinia()
    setActivePinia(pinia)
  })

  it('renders page title', async () => {
    const router = createTestRouter()
    router.push('/history')
    await router.isReady()

    const wrapper = mount(HistoryPage, {
      global: { plugins: [createPinia(), router] },
    })
    await new Promise(r => setTimeout(r, 100))
    expect(wrapper.html()).toContain('我的报告')
  })

  it('shows report data in table after load', async () => {
    const router = createTestRouter()
    router.push('/history')
    await router.isReady()

    const wrapper = mount(HistoryPage, {
      global: { plugins: [createPinia(), router] },
    })
    await new Promise(r => setTimeout(r, 100))
    expect(wrapper.html()).toContain('命运双鉴')
  })

  it('shows view and delete buttons', async () => {
    const router = createTestRouter()
    router.push('/history')
    await router.isReady()

    const wrapper = mount(HistoryPage, {
      global: { plugins: [createPinia(), router] },
    })
    await new Promise(r => setTimeout(r, 100))
    expect(wrapper.html()).toContain('查看')
    expect(wrapper.html()).toContain('删除')
  })
})
