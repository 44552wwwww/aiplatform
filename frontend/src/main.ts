import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'element-plus/theme-chalk/base.css'
import router from './router'
import App from './App.vue'
import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// 全局 Vue 错误处理
app.config.errorHandler = (err, _instance, info) => {
  console.error('[Vue Error]', err, info)
}

app.mount('#app')
