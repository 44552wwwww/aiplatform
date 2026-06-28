<template>
  <div class="min-h-screen">
    <!-- 导航栏 -->
    <nav class="navbar" :class="{ scrolled: isScrolled }">
      <div class="container">
        <div class="navbar-inner">
          <div class="navbar-logo">
            <div class="navbar-logo-icon">✨</div>
            <span>InsightForge</span>
          </div>
          <div class="navbar-links">
            <a href="#features" class="navbar-link" @click.prevent="scrollTo('#features')">功能</a>
            <a href="#faq" class="navbar-link" @click.prevent="scrollTo('#faq')">FAQ</a>
            <button class="theme-toggle" @click="toggleTheme" :title="themeLabel">
              {{ themeIcon }}
            </button>
            <template v-if="isLoggedIn">
              <button class="btn btn-ghost" @click="$router.push('/dashboard')">Dashboard</button>
            </template>
            <template v-else>
              <button class="btn btn-ghost" @click="$router.push('/login')">登录</button>
              <button class="btn btn-primary" @click="$router.push('/register')">免费注册</button>
            </template>
          </div>
          <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <div class="hero-badge">
          <span class="hero-badge-dot" />
          <span>AI 驱动的智能分析</span>
        </div>
        <h1 class="hero-title">
          <span class="text-gradient">AI 生成</span>精美分析报告
        </h1>
        <p class="hero-subtitle">
          选择分析类型、输入参数，AI 自动为你生成专业级别的结构化报告。基于插件架构，支持多种分析场景。
        </p>
        <div class="hero-cta">
          <button v-if="!isLoggedIn" class="btn btn-primary btn-lg" @click="$router.push('/register')">
            免费开始使用
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" />
            </svg>
          </button>
          <button v-else class="btn btn-primary btn-lg" @click="$router.push('/dashboard')">
            进入 Dashboard
          </button>
          <button class="btn btn-secondary btn-lg" @click="scrollTo('#features')">
            了解更多
          </button>
        </div>
      </div>
    </section>

    <!-- 统计数据 -->
    <section class="stats">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number text-gradient">5+</div>
            <div class="stat-label">AI 分析类型</div>
          </div>
          <div class="stat-item">
            <div class="stat-number text-gradient">100%</div>
            <div class="stat-label">插件化架构</div>
          </div>
          <div class="stat-item">
            <div class="stat-number text-gradient">秒级</div>
            <div class="stat-label">报告生成速度</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 功能特性 -->
    <section class="features" id="features">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">强大的平台能力</h2>
          <p class="section-subtitle">基于现代技术栈构建，为你提供稳定可靠的 AI 分析服务</p>
        </div>
        <div class="features-grid">
          <div class="feature-card glass-card" v-for="f in features" :key="f.title">
            <div class="feature-icon">{{ f.icon }}</div>
            <h3 class="feature-title">{{ f.title }}</h3>
            <p class="feature-desc">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 使用步骤 -->
    <section class="steps">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">三步生成报告</h2>
          <p class="section-subtitle">简单易用，几分钟即可获得专业分析报告</p>
        </div>
        <div class="steps-container">
          <div class="step-item" v-for="(s, i) in steps" :key="i">
            <div class="step-number">{{ i + 1 }}</div>
            <h3 class="step-title">{{ s.title }}</h3>
            <p class="step-desc">{{ s.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="faq" id="faq">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">常见问题</h2>
          <p class="section-subtitle">关于 InsightForge 的常见疑问解答</p>
        </div>
        <div class="faq-container">
          <div class="faq-item" v-for="(fq, i) in faqs" :key="i" :class="{ active: activeFaq === i }">
            <button class="faq-question" @click="activeFaq = activeFaq === i ? -1 : i">
              <span>{{ fq.q }}</span>
              <span class="faq-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </span>
            </button>
            <div class="faq-answer" ref="faqAnswers">
              <div class="faq-answer-content">{{ fq.a }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-card glass-card">
          <h2 class="cta-title">准备好开始了吗？</h2>
          <p class="cta-desc">创建免费账号，立即体验 AI 驱动的智能分析报告</p>
          <button v-if="!isLoggedIn" class="btn btn-primary btn-lg" @click="$router.push('/register')">
            创建免费账号
          </button>
          <button v-else class="btn btn-primary btn-lg" @click="$router.push('/dashboard')">
            进入 Dashboard
          </button>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <div class="footer-inner">
          <div class="navbar-logo">
            <div class="navbar-logo-icon">✨</div>
            <span>InsightForge</span>
          </div>
          <div class="footer-links">
            <a href="#" class="footer-link" @click.prevent="$router.push('/')">首页</a>
            <a href="#features" class="footer-link">功能</a>
            <a href="#faq" class="footer-link">FAQ</a>
            <a href="https://github.com/44552wwwww/aiplatform" target="_blank" class="footer-link">GitHub</a>
          </div>
          <div class="footer-copyright">© 2024 InsightForge. All rights reserved.</div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTheme } from '@/composables/useTheme'

const auth = useAuthStore()
const { theme, toggle } = useTheme()
const isLoggedIn = computed(() => !!auth.token)

const isScrolled = ref(false)
const activeFaq = ref(-1)
const mobileMenuOpen = ref(false)
const faqAnswers = ref<HTMLElement[]>([])

const themeIcon = computed(() => (theme.value === 'dark' ? '☀️' : '🌙'))
const themeLabel = computed(() => (theme.value === 'dark' ? '切换浅色主题' : '切换深色主题'))

function toggleTheme() { toggle() }

const features = [
  { icon: '🤖', title: 'AI 驱动分析', desc: '基于大语言模型，智能理解输入参数，生成深度分析内容。' },
  { icon: '🧩', title: '插件化 Skill', desc: '模块化设计，支持快速扩展新的分析类型，灵活适配各种场景。' },
  { icon: '🔐', title: 'JWT 安全认证', desc: '采用行业标准的 JWT 认证机制，保障你的账户和数据安全。' },
  { icon: '📄', title: '精美 HTML 报告', desc: '专业设计的报告模板，支持导出和分享，展示效果出众。' },
  { icon: '💾', title: '数据持久化', desc: '所有报告自动保存，随时查看历史记录，永不丢失。' },
  { icon: '🚀', title: '一键部署', desc: '基于 Docker 容器化部署，支持 Railway 等平台一键上线。' },
]

const steps = [
  { title: '注册账号', desc: '免费注册 InsightForge 账号，开启 AI 分析之旅。' },
  { title: '选择分析类型', desc: '从 Skill 市场选择你需要的分析类型，填写相关参数。' },
  { title: 'AI 生成报告', desc: 'AI 自动分析并生成精美报告，可随时查看和分享。' },
]

const faqs = [
  { q: 'InsightForge 是免费的吗？', a: '是的，基础功能完全免费。你可以注册账号并使用所有公开的 Skill 生成报告。' },
  { q: '支持哪些分析类型？', a: '目前支持八字命理等多种分析类型。平台采用插件化架构，会持续增加新的分析 Skill。' },
  { q: '生成的报告可以导出吗？', a: '可以。你可以复制报告的 HTML 代码，粘贴到任何支持 HTML 的地方使用。' },
  { q: '我的数据安全吗？', a: '我们采用 JWT 认证和加密传输，所有数据都安全存储。你可以随时删除自己的报告数据。' },
]

function scrollTo(selector: string) {
  document.querySelector(selector)?.scrollIntoView({ behavior: 'smooth' })
}

function onScroll() {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', onScroll)
  onScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>
