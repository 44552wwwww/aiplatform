import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import AppHeader from '../AppHeader.vue'
import { useAuthStore } from '@/stores/auth'

const localStorageMock = (() => {
  let store: Record<string, string> = {}
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value },
    removeItem: (key: string) => { delete store[key] },
    clear: () => { store = {} },
  }
})()
Object.defineProperty(window, 'localStorage', { value: localStorageMock })

function createTestRouter() {
  return createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/', component: {} as any },
      { path: '/login', component: {} as any },
      { path: '/register', component: {} as any },
      { path: '/history', component: {} as any },
    ],
  })
}

describe('AppHeader', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('renders logo link', async () => {
    const pinia = createPinia()
    setActivePinia(pinia)
    const router = createTestRouter()
    router.push('/')
    await router.isReady()
    const wrapper = mount(AppHeader, {
      global: { plugins: [pinia, router] },
    })
    expect(wrapper.find('.logo').text()).toContain('InsightForge')
  })

  it('shows login/register when not authenticated', async () => {
    const pinia = createPinia()
    setActivePinia(pinia)
    const router = createTestRouter()
    router.push('/')
    await router.isReady()
    const wrapper = mount(AppHeader, {
      global: { plugins: [pinia, router] },
    })
    expect(wrapper.html()).toContain('登录')
    expect(wrapper.html()).toContain('注册')
  })

  it('shows username and logout when authenticated', async () => {
    const pinia = createPinia()
    setActivePinia(pinia)
    const auth = useAuthStore()
    auth.token = 'test-token'
    auth.user = { id: 1, username: 'demo' }

    const router = createTestRouter()
    router.push('/')
    await router.isReady()
    const wrapper = mount(AppHeader, {
      global: { plugins: [pinia, router] },
    })
    expect(wrapper.html()).toContain('demo')
    expect(wrapper.html()).toContain('我的报告')
    expect(wrapper.html()).toContain('退出')
  })

  it('shows hamburger icon on mobile', async () => {
    const pinia = createPinia()
    setActivePinia(pinia)
    const router = createTestRouter()
    router.push('/')
    await router.isReady()
    const wrapper = mount(AppHeader, {
      global: { plugins: [pinia, router] },
    })
    expect(wrapper.find('.hamburger').exists()).toBe(true)
  })
})
