<template>
  <div class="min-h-screen">
    <!-- Header -->
    <header class="sticky top-0 z-50 border-b border-[var(--color-border)] bg-[var(--color-background)]/80 backdrop-blur-lg">
      <div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <div class="flex items-center gap-2 font-semibold text-lg">
          <Sparkles class="h-5 w-5 text-purple-600" />
          InsightForge
        </div>
        <nav class="hidden items-center gap-6 sm:flex">
          <a href="#features" class="text-sm text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] transition-colors">功能</a>
          <a href="#faq" class="text-sm text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)] transition-colors">FAQ</a>
          <ThemeToggle />
          <Button variant="ghost" size="sm" @click="$router.push('/login')">登录</Button>
          <Button size="sm" @click="$router.push('/register')">注册</Button>
        </nav>
        <!-- Mobile nav -->
        <div class="flex items-center gap-2 sm:hidden">
          <ThemeToggle />
          <Button variant="ghost" size="sm" @click="$router.push('/login')">登录</Button>
        </div>
      </div>
    </header>

    <HeroSection />
    <FeaturesSection />
    <WorkflowSection />
    <FAQSection />
    <CTASection />
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
import Button from '@/components/ui/Button.vue'
import ThemeToggle from '@/components/shared/ThemeToggle.vue'
import HeroSection from '@/components/landing/HeroSection.vue'
import FeaturesSection from '@/components/landing/FeaturesSection.vue'
import WorkflowSection from '@/components/landing/WorkflowSection.vue'
import FAQSection from '@/components/landing/FAQSection.vue'
import CTASection from '@/components/landing/CTASection.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
</script>
