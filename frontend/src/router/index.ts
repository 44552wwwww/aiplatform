import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Landing',
      component: () => import('@/pages/LandingPage.vue'),
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/pages/LoginPage.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/pages/RegisterPage.vue'),
      meta: { guest: true },
    },
    {
      path: '/skills',
      name: 'Skills',
      component: () => import('@/pages/HomePage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/skill/:skillId',
      name: 'Skill',
      component: () => import('@/pages/SkillPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/report/:reportId',
      name: 'Report',
      component: () => import('@/pages/ReportPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/history',
      name: 'History',
      component: () => import('@/pages/HistoryPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/pages/NotFoundPage.vue'),
    },
  ],
})

function getToken(): string | null {
  try {
    const stored = localStorage.getItem('auth')
    if (stored) {
      return JSON.parse(stored).token || null
    }
  } catch {
    // ignore
  }
  return null
}

router.beforeEach((to, _from, next) => {
  const token = getToken()

  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.guest && token) {
    next({ name: 'Landing' })
  } else {
    next()
  }
})

export default router
