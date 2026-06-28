<template>
  <div class="flex min-h-screen flex-col items-center justify-center px-4 text-center" style="background: var(--bg-primary); color: var(--text-primary);">
    <div class="empty-state-icon" style="font-size: 6rem;">🔮</div>
    <h1 style="font-size: 5rem; font-weight: 800; color: var(--border-color); margin-bottom: var(--spacing-md);">404</h1>
    <p class="text-lg mb-2" style="color: var(--text-secondary);">页面不存在</p>
    <p class="text-sm mb-8" style="color: var(--text-muted);">你访问的页面消失在星空中了</p>
    <router-link to="/" class="btn btn-primary btn-lg">返回首页</router-link>
  </div>
</template>
