<template>
  <div class="auth-page">
    <div class="auth-card glass-card">
      <router-link to="/" class="auth-back">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="19" y1="12" x2="5" y2="12" />
          <polyline points="12 19 5 12 12 5" />
        </svg>
        返回首页
      </router-link>
      <slot />
    </div>
  </div>
</template>
