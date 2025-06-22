# AGENTS.md - Frontend (Vue 3 + Vite + Bootstrap 5.3.6)

## 🎯 前端技术栈
- **框架**：Vue 3 (Composition API)
- **构建工具**：Vite + TypeScript
- **UI框架**：Bootstrap 5.3.6（静态引入，禁用Ant Design Pro）
- **状态管理**：Pinia
- **HTTP请求**：Axios（自封装API请求）
- **路由**：Vue Router
- **CSS预处理器**：原生CSS + Bootstrap Utility Classes

## 📁 目录结构与职责
```
frontend/src/
├── views/                         # 页面级组件
│   ├── HomeView.vue              # 首页
│   ├── Login.vue                 # 登录页
│   ├── Register.vue              # 注册页
│   ├── CourseDetails.vue         # 课程详情页
│   ├── ShoppingCart.vue          # 购物车页
│   ├── Order.vue                 # 订单页
│   └── PersonalCenter.vue        # 个人中心
├── components/                    # 可复用组件
│   ├── cart/                     # 购物车相关组件
│   ├── order/                    # 订单相关组件
│   ├── personCenter/             # 个人中心相关组件
│   ├── Navbar.vue               # 导航栏
│   ├── AuthNavbar.vue           # 认证导航栏
│   ├── LoginModal.vue           # 登录弹窗
│   ├── RegisterModal.vue        # 注册弹窗
│   ├── CourseCard.vue           # 课程卡片
│   ├── CourseHeroCard.vue       # 课程英雄卡片
│   └── ...                     # 其他通用组件
├── api/                          # Axios封装接口
│   ├── index.ts                 # Axios配置
│   ├── auth.ts                  # 认证相关API
│   ├── course.ts                # 课程相关API
│   └── ...                     # 其他模块API
├── store/                        # Pinia状态管理
│   ├── index.ts                 # Store入口
│   ├── auth.ts                  # 认证状态
│   ├── course.ts                # 课程状态
│   └── ...                     # 其他状态模块
├── router/                       # Vue Router配置
│   └── index.ts                 # 路由配置
├── utils/                        # 工具函数
│   ├── request.ts               # Axios封装
│   ├── auth.ts                  # 认证工具
│   └── ...                     # 其他工具
└── types/                        # TypeScript类型定义
    ├── api.ts                   # API接口类型
    ├── user.ts                  # 用户相关类型
    └── ...                     # 其他类型定义
```

## 🎨 样式与UI规范
### Bootstrap 5.3.6 使用约定
- **优先使用Bootstrap Utility Classes**编写样式
- **Grid System**：默认使用`row`、`col-*`实现响应式布局
- **组件样式**：优先使用Bootstrap原生组件样式
- **自定义样式**：仅在Bootstrap无法满足时添加自定义CSS

### 响应式设计
- **移动优先**：所有组件必须支持移动端视图（≤768px）
- **断点规范**：
  - `xs`: <576px
  - `sm`: ≥576px
  - `md`: ≥768px
  - `lg`: ≥992px
  - `xl`: ≥1200px

### 组件命名规范
- **文件命名**：严格使用PascalCase（如`CourseHeroCard.vue`）
- **组件名称**：与文件名保持一致
- **按功能分组**：相关组件放入对应子目录（如`cart/`、`personCenter/`）

## 💻 Vue 3 开发规范
### Composition API要求
- **严格禁止**使用Options API，必须使用Composition API
- **推荐模式**：
```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// 响应式数据
const loading = ref(false)
const userInfo = ref(null)

// 计算属性
const isLoggedIn = computed(() => !!userInfo.value)

// 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>
```

### 组件结构规范
```vue
<template>
  <!-- 使用Bootstrap classes -->
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-8">
        <!-- 主要内容 -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 导入依赖
import { ref, computed } from 'vue'
import { useAuthStore } from '@/store/auth'

// 接口和类型定义
interface Props {
  title: string
}

// Props定义
const props = defineProps<Props>()

// 响应式数据
const isVisible = ref(true)

// 计算属性
const displayTitle = computed(() => props.title.toUpperCase())
</script>

<style scoped>
/* 仅在必要时添加自定义样式 */
.custom-style {
  /* 避免与Bootstrap冲突 */
}
</style>
```

## 🔗 状态管理规范
### Pinia Store结构
```typescript
// src/store/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<UserInfo | null>(null)
  
  // Getters
  const isLoggedIn = computed(() => !!token.value)
  
  // Actions
  const login = async (credentials: LoginForm) => {
    // 登录逻辑
  }
  
  const logout = () => {
    token.value = null
    userInfo.value = null
    localStorage.removeItem('token')
  }
  
  return {
    // State
    token,
    userInfo,
    // Getters
    isLoggedIn,
    // Actions
    login,
    logout
  }
})
```

## 🌐 API接口封装规范
### Axios统一配置
```typescript
// src/api/index.ts
import axios from 'axios'
import { useAuthStore } from '@/store/auth'

const request = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

// 请求拦截器 - 自动添加JWT token
request.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

// 响应拦截器 - 统一处理响应格式
request.interceptors.response.use(
  response => {
    const { status, data, msg } = response.data
    if (status === 200) {
      return data
    } else {
      throw new Error(msg || '请求失败')
    }
  },
  error => {
    // 统一错误处理
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)
```

### API方法命名规范
```typescript
// src/api/course.ts
import request from './index'

// 获取课程列表
export const getCourseList = (params: CourseListParams) => {
  return request.get('/courses/', { params })
}

// 获取课程详情
export const getCourseDetail = (id: number) => {
  return request.get(`/courses/${id}/`)
}

// 创建订单
export const createOrder = (data: CreateOrderData) => {
  return request.post('/orders/', data)
}
```

## 🎯 组件开发规范
### 专用组件职责划分
- **`Navbar.vue`**：全站导航栏，自动判断登录状态
- **`AuthNavbar.vue`**：认证页面专用导航栏
- **`LoginModal.vue`**：登录弹窗，处理登录逻辑
- **`RegisterModal.vue`**：注册弹窗，处理注册逻辑
- **`CourseCard.vue`**：课程卡片，展示课程基本信息
- **`CourseHeroCard.vue`**：课程英雄卡片，课程详情页头部
- **`SidebarPricingCard.vue`**：侧边栏价格卡片，购买操作

### 组件通信规范
- **Props**：父组件向子组件传递数据
- **Emit**：子组件向父组件发送事件
- **Pinia Store**：跨组件状态共享
- **Provide/Inject**：深层组件通信（谨慎使用）

## 🔧 开发工具配置
### TypeScript使用要求
- **严格模式**：启用strict模式进行类型检查
- **类型定义**：所有API接口、Props、State必须定义类型
- **避免any**：禁止使用`any`类型，使用具体类型或`unknown`

### 表单处理规范
```vue
<template>
  <form @submit.prevent="handleSubmit" class="needs-validation" novalidate>
    <div class="mb-3">
      <label for="email" class="form-label">邮箱</label>
      <input 
        v-model="form.email"
        type="email" 
        class="form-control"
        :class="{ 'is-invalid': errors.email }"
        id="email" 
        required
      >
      <div v-if="errors.email" class="invalid-feedback">
        {{ errors.email }}
      </div>
    </div>
    <button type="submit" class="btn btn-primary" :disabled="loading">
      <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
      提交
    </button>
  </form>
</template>
```

## 🚀 性能优化建议
- **懒加载**：使用`defineAsyncComponent`进行组件懒加载
- **虚拟滚动**：长列表使用虚拟滚动技术
- **图片优化**：使用`loading="lazy"`属性
- **代码分割**：合理使用动态import进行代码分割

## 📱 移动端适配
- **触摸优化**：按钮最小触摸区域44px×44px
- **导航适配**：移动端使用汉堡菜单
- **表单优化**：输入框适当放大，减少误触
- **加载状态**：提供明确的加载和错误状态提示

## 🧪 测试与调试
- **开发工具**：充分利用Vue DevTools进行调试
- **API测试**：使用浏览器Network面板检查请求
- **控制台**：及时清理console.log，生产环境禁用
- **错误边界**：关键组件添加错误处理机制

## 📝 代码注释要求
```vue
<!-- 
组件说明：课程详情页面主要入口组件
功能：展示课程详细信息，包括价格、章节、评价等
作者：开发者姓名
更新时间：2024-01-01
-->
<template>
  <!-- 组件内容 -->
</template>

<script setup lang="ts">
/**
 * 获取课程详情数据
 * @param courseId 课程ID
 * @returns Promise<CourseDetail>
 */
const fetchCourseDetail = async (courseId: number) => {
  // 实现逻辑
}
</script>
``` 