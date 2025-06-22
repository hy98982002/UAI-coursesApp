import axios, { type AxiosRequestConfig, type AxiosResponse, AxiosError, type InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '@/store/auth'
import router from '@/router'

// Token刷新锁，防止并发刷新风暴
let refreshingPromise: Promise<boolean> | null = null

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 15000,  // 增加到15秒更安全
  withCredentials: false,  // 显式声明不使用Cookie认证，使用Bearer Token
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'  // 统一Accept头
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加Token到请求头
    const authStore = useAuthStore()
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    
    console.log(`🚀 API请求: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error: AxiosError) => {
    console.error('❌ 请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`✅ API响应: ${response.config.url} - ${response.status}`)
    return response
  },
  async (error: AxiosError) => {
    const authStore = useAuthStore()
    
    if (error.response?.status === 401) {
      // Token过期或无效
      console.log('🔄 Token失效，尝试刷新...')
      
      // 如果不是刷新Token的请求，则尝试刷新Token
      if (!error.config?.url?.match(/\/api\/users\/auth\/refresh\/$/)) {
        // 使用刷新锁，防止并发刷新
        if (!refreshingPromise) {
          refreshingPromise = authStore.refreshAccessToken()
        }
        
        const refreshSuccess = await refreshingPromise
        refreshingPromise = null // 重置刷新锁
        
        if (refreshSuccess && error.config) {
          // 刷新成功，重新发起原请求
          console.log('✅ Token刷新成功，重新发起请求')
          error.config.headers.Authorization = `Bearer ${authStore.accessToken}`
          return api.request(error.config)
        } else {
          // 刷新失败，清理Authorization头避免循环
          delete api.defaults.headers.common['Authorization']
        }
      }
      
      // 刷新失败或本身就是刷新请求失败，跳转到登录页
      console.log('❌ Token刷新失败，跳转到登录页')
      authStore.logout()
      
      // 避免在登录页重复跳转，使用replace避免历史堆叠
      if (router.currentRoute.value.path !== '/login') {
        router.replace({
          path: '/login',
          query: { redirect: router.currentRoute.value.fullPath }
        })
      }
    }
    
    // 处理其他HTTP错误
    let errorMessage = '请求失败，请重试'
    
    if (error.response) {
      // 服务器返回错误响应
      const data = error.response.data as any
      errorMessage = data?.msg || data?.message || `服务器错误 (${error.response.status})`
    } else if (error.request) {
      // 网络错误
      errorMessage = '网络连接失败，请检查网络'
    }
    
    console.error(`❌ API错误: ${error.config?.url}`, errorMessage)
    
    // 可以在这里统一处理错误提示
    // 例如：ElMessage.error(errorMessage)
    
    return Promise.reject(new Error(errorMessage))
  }
)

export default api

// 导出常用的请求方法
export const get = <T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
  return api.get(url, config)
}

export const post = <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
  return api.post(url, data, config)
}

export const put = <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
  return api.put(url, data, config)
}

export const del = <T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
  return api.delete(url, config)
} 