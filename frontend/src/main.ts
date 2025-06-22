import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './store'
import { useAuthStore } from '@/store/auth'

import '@coreui/coreui/dist/css/coreui.min.css'   // CoreUI 样式

// 引入 Bootstrap 样式
import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)
app.use(pinia)  // 先安装pinia
app.use(router)

// 初始化auth store（从localStorage恢复状态）
const authStore = useAuthStore()
authStore.initialize()

app.mount('#app')
