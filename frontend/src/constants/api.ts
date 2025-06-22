/**
 * API 路径常量
 */

// 基础路径
export const API_BASE = '/api'

// 用户认证相关接口
export const AUTH_API = {
  // 注册相关
  REGISTER: `${API_BASE}/users/auth/register/`,
  SMS_REGISTER: `${API_BASE}/users/auth/sms-register/`,
  
  // 登录相关
  LOGIN: `${API_BASE}/users/auth/login/`,
  SMS_LOGIN: `${API_BASE}/users/auth/sms-login/`,
  LOGOUT: `${API_BASE}/users/auth/logout/`,
  
  // Token相关
  REFRESH_TOKEN: `${API_BASE}/users/auth/refresh/`,
  
  // 短信相关
  SEND_SMS: `${API_BASE}/users/auth/send-sms/`,
} as const

// 用户管理相关接口
export const USER_API = {
  // 用户信息
  PROFILE: `${API_BASE}/users/user/profile/`,
  UPDATE_PROFILE: `${API_BASE}/users/user/update_profile/`,
  UPDATE_USER_PROFILE: `${API_BASE}/users/user/update_user_profile/`,
  
  // 密码管理
  CHANGE_PASSWORD: `${API_BASE}/users/user/change_password/`,
  
  // 用户设置
  SETTINGS: `${API_BASE}/users/user/settings/`,
  UPDATE_SETTINGS: `${API_BASE}/users/user/update_settings/`,
} as const

// 课程相关接口
export const COURSE_API = {
  LIST: `${API_BASE}/courses/`,
  DETAIL: (id: string) => `${API_BASE}/courses/${id}/`,
  SEARCH: `${API_BASE}/courses/search/`,
} as const

// 订单相关接口
export const ORDER_API = {
  LIST: `${API_BASE}/orders/`,
  CREATE: `${API_BASE}/orders/`,
  DETAIL: (id: string) => `${API_BASE}/orders/${id}/`,
  CANCEL: (id: string) => `${API_BASE}/orders/${id}/cancel/`,
} as const

// 购物车相关接口
export const CART_API = {
  LIST: `${API_BASE}/cart/`,
  ADD: `${API_BASE}/cart/add/`,
  REMOVE: (id: string) => `${API_BASE}/cart/${id}/remove/`,
  CLEAR: `${API_BASE}/cart/clear/`,
} as const 