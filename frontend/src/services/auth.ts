import api from '@/utils/axios'
import { AUTH_API, USER_API } from '@/constants/api'

// API响应的通用格式
interface ApiResponse<T = any> {
  status: number
  data: T
  msg: string
}

// 用户信息接口
export interface UserInfo {
  id: string
  phone: string
  unique_identifier: string
  nickname: string
  email?: string
  is_phone_verified: boolean
  has_password?: boolean
  profile?: {
    real_name?: string
    gender?: string
    avatar?: string
  }
}

// 登录响应
export interface LoginResponse {
  access: string
  refresh: string
  user: UserInfo
  need_set_password?: boolean
}

// 认证服务
export class AuthService {
  /**
   * 用户登录
   */
  static async login(phone: string, password: string): Promise<LoginResponse> {
    const response = await api.post<ApiResponse<LoginResponse>>(AUTH_API.LOGIN, {
      phone,
      password
    })
    
    if (response.data.status === 200) {
      return response.data.data
    } else {
      throw new Error(response.data.msg || '登录失败')
    }
  }

  /**
   * 用户注册
   */
  static async register(phone: string, password: string, nickname?: string): Promise<LoginResponse> {
    const response = await api.post<ApiResponse<LoginResponse>>(AUTH_API.REGISTER, {
      phone,
      password,
      nickname: nickname || ''
    })
    
    if (response.data.status === 201) {
      return response.data.data
    } else {
      throw new Error(response.data.msg || '注册失败')
    }
  }

  /**
   * 短信验证码注册
   */
  static async smsRegister(phone: string, smsCode: string): Promise<LoginResponse> {
    const response = await api.post<ApiResponse<LoginResponse>>(AUTH_API.SMS_REGISTER, {
      phone,
      sms_code: smsCode
    })
    
    if (response.data.status === 201) {
      return response.data.data
    } else {
      throw new Error(response.data.msg || '注册失败')
    }
  }

  /**
   * 短信验证码登录
   */
  static async smsLogin(phone: string, smsCode: string): Promise<LoginResponse> {
    const response = await api.post<ApiResponse<LoginResponse>>(AUTH_API.SMS_LOGIN, {
      phone,
      sms_code: smsCode
    })
    
    if (response.data.status === 200) {
      return response.data.data
    } else {
      throw new Error(response.data.msg || '验证码登录失败')
    }
  }

  /**
   * 刷新Token
   */
  static async refreshToken(refreshToken: string): Promise<string> {
    const response = await api.post<ApiResponse<{ access: string }>>(AUTH_API.REFRESH_TOKEN, {
      refresh: refreshToken
    })
    
    if (response.data.status === 200) {
      return response.data.data.access
    } else {
      throw new Error(response.data.msg || 'Token刷新失败')
    }
  }

  /**
   * 获取用户资料
   */
  static async getUserProfile(): Promise<UserInfo> {
    const response = await api.get<ApiResponse<UserInfo>>(USER_API.PROFILE)
    
    if (response.data.status === 200) {
      return response.data.data
    } else {
      throw new Error(response.data.msg || '获取用户资料失败')
    }
  }

  /**
   * 更新用户资料
   */
  static async updateUserProfile(profileData: Partial<UserInfo>): Promise<UserInfo> {
    const response = await api.put<ApiResponse<UserInfo>>(USER_API.UPDATE_PROFILE, profileData)
    
    if (response.data.status === 200) {
      return response.data.data
    } else {
      throw new Error(response.data.msg || '更新用户资料失败')
    }
  }

  /**
   * 发送短信验证码
   */
  static async sendSmsCode(phone: string): Promise<void> {
    const response = await api.post<ApiResponse<null>>(AUTH_API.SEND_SMS, {
      phone
    })
    
    if (response.data.status !== 200) {
      throw new Error(response.data.msg || '发送验证码失败')
    }
  }

  /**
   * 修改密码
   */
  static async changePassword(oldPassword: string, newPassword: string): Promise<void> {
    const response = await api.post<ApiResponse<null>>(USER_API.CHANGE_PASSWORD, {
      old_password: oldPassword,
      new_password: newPassword
    })
    
    if (response.data.status !== 200) {
      throw new Error(response.data.msg || '修改密码失败')
    }
  }

  /**
   * 用户登出
   */
  static async logout(): Promise<void> {
    const response = await api.post<ApiResponse<null>>(AUTH_API.LOGOUT)
    
    if (response.data.status !== 200) {
      throw new Error(response.data.msg || '登出失败')
    }
  }
} 