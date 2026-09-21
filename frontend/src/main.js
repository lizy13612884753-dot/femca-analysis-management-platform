import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './styles/variables.css'
import './styles/dark-theme.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/user'

// 创建应用实例
const app = createApp(App)

// 使用插件
app.use(createPinia())
app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
})

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 应用启动后检查认证状态
router.isReady().then(async () => {
  const userStore = useUserStore()
  if (userStore.token) {
    await userStore.checkAuthStatus()
  }
  
  // 应用主题
  const theme = localStorage.getItem('theme') || 'light'
  const html = document.documentElement
  html.classList.remove('light', 'dark')
  
  if (theme === 'auto') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    html.classList.add(prefersDark ? 'dark' : 'light')
  } else {
    html.classList.add(theme)
  }
  
  console.log('Initial theme applied:', theme, 'HTML classes:', html.className)
})

app.mount('#app')