import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { AuthService, type UserInfo } from '@/services/auth'
import api from '@/utils/axios'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const accessToken = ref('')
  const refreshToken = ref('')
  const userInfo = ref<UserInfo | null>(null)

  // 计算属性
  const isAuthenticated = computed(() => !!accessToken.value)
  const isPhoneVerified = computed(() => userInfo.value?.is_phone_verified || false)
  const hasPassword = computed(() => userInfo.value?.has_password || false)
  const user = computed(() => userInfo.value)

  // 设置Token
  const setTokens = (access: string, refresh: string) => {
    accessToken.value = access
    refreshToken.value = refresh
    
    // 设置api实例默认header
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`
  }

  // 设置用户信息
  const setUserInfo = (user: UserInfo) => {
    userInfo.value = user
  }

  // 登录
  const login = async (phone: string, password: string): Promise<boolean> => {
    try {
      const { access, refresh, user } = await AuthService.login(phone, password)
      setTokens(access, refresh)
      setUserInfo(user)
      return true
    } catch (error: any) {
      console.error('登录失败:', error)
      throw error
    }
  }

  // 注册
  const register = async (phone: string, password: string, nickname?: string): Promise<boolean> => {
    try {
      await AuthService.register(phone, password, nickname)
      // 注册成功后自动登录
      return await login(phone, password)
    } catch (error: any) {
      console.error('注册失败:', error)
      throw error
    }
  }

  // 短信验证码登录
  const smsLogin = async (phone: string, smsCode: string): Promise<boolean> => {
    try {
      const { access, refresh, user } = await AuthService.smsLogin(phone, smsCode)
      setTokens(access, refresh)
      setUserInfo(user)
      return true
    } catch (error: any) {
      console.error('短信登录失败:', error)
      throw error
    }
  }

  // 短信验证码注册
  const smsRegister = async (phone: string, smsCode: string): Promise<{ success: boolean, needSetPassword?: boolean }> => {
    try {
      const { access, refresh, user, need_set_password } = await AuthService.smsRegister(phone, smsCode)
      setTokens(access, refresh)
      setUserInfo(user)
      return { success: true, needSetPassword: need_set_password }
    } catch (error: any) {
      console.error('短信注册失败:', error)
      throw error
    }
  }

  // 发送短信验证码
  const sendSmsCode = async (phone: string): Promise<boolean> => {
    try {
      await AuthService.sendSmsCode(phone)
      return true
    } catch (error: any) {
      console.error('发送验证码失败:', error)
      throw error
    }
  }

  // 刷新Token
  const refreshAccessToken = async (): Promise<boolean> => {
    try {
      const newAccessToken = await AuthService.refreshToken(refreshToken.value)
      setTokens(newAccessToken, refreshToken.value)
      return true
    } catch (error) {
      console.error('Token刷新失败:', error)
      logout()
      return false
    }
  }

  // 获取用户资料
  const fetchUserProfile = async (): Promise<void> => {
    try {
      const userProfileData = await AuthService.getUserProfile()
      setUserInfo(userProfileData)
    } catch (error) {
      console.error('获取用户资料失败:', error)
    }
  }

  // 登出
  const logout = async () => {
    try {
      // 调用后端登出接口
      await AuthService.logout()
    } catch (error) {
      console.error('后端登出失败:', error)
    }
    
    // 清理本地状态
    accessToken.value = ''
    refreshToken.value = ''
    userInfo.value = null
    
    // 清理api实例header
    delete api.defaults.headers.common['Authorization']
  }

  // 初始化：设置api实例header（持久化插件自动恢复state）
  const initialize = () => {
    if (accessToken.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
    }
  }

  return {
    // 状态
    accessToken,
    refreshToken,
    userInfo,
    
    // 计算属性
    isAuthenticated,
    isPhoneVerified,
    hasPassword,
    user,
    
    // 方法
    login,
    register,
    smsLogin,
    smsRegister,
    sendSmsCode,
    logout,
    refreshAccessToken,
    fetchUserProfile,
    setTokens,
    setUserInfo,
    initialize
  }
}, {
  persist: {
    key: 'uai-auth',
    storage: localStorage,
    pick: ['accessToken', 'refreshToken', 'userInfo']
  }
}) 