import { ref, watchEffect } from 'vue'

type Theme = 'light' | 'dark'

const THEME_KEY = 'insightforge-theme'
const theme = ref<Theme>((localStorage.getItem(THEME_KEY) as Theme) || 'dark')

export function useTheme() {
  watchEffect(() => {
    const root = document.documentElement
    root.setAttribute('data-theme', theme.value)
    // 同时维护 Tailwind dark class
    if (theme.value === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
    localStorage.setItem(THEME_KEY, theme.value)
  })

  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  function set(t: Theme) {
    theme.value = t
  }

  return { theme, toggle, set }
}
