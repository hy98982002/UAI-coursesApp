/**
 * 表单验证工具函数
 */

// 手机号正则表达式
export const PHONE_REGEX = /^1[3-9]\d{9}$/

// 验证码正则表达式（6位数字）
export const SMS_CODE_REGEX = /^\d{6}$/

/**
 * 验证手机号格式
 * @param phone 手机号
 * @returns 验证结果对象
 */
export const validatePhone = (phone: string): { valid: boolean; message?: string } => {
  if (!phone) {
    return { valid: false, message: '请输入手机号' }
  }
  
  if (!PHONE_REGEX.test(phone)) {
    return { valid: false, message: '请输入正确的手机号格式' }
  }
  
  return { valid: true }
}

/**
 * 验证短信验证码格式
 * @param code 验证码
 * @returns 验证结果对象
 */
export const validateSmsCode = (code: string): { valid: boolean; message?: string } => {
  if (!code) {
    return { valid: false, message: '请输入验证码' }
  }
  
  if (!SMS_CODE_REGEX.test(code)) {
    return { valid: false, message: '验证码格式错误，请输入6位数字' }
  }
  
  return { valid: true }
}

/**
 * 验证密码格式
 * @param password 密码
 * @param minLength 最小长度，默认6位
 * @returns 验证结果对象
 */
export const validatePassword = (password: string, minLength: number = 6): { valid: boolean; message?: string } => {
  if (!password) {
    return { valid: false, message: '请输入密码' }
  }
  
  if (password.length < minLength) {
    return { valid: false, message: `密码长度至少为${minLength}位` }
  }
  
  return { valid: true }
}

/**
 * 验证表单字段
 * @param fields 字段数组
 * @returns 第一个验证失败的错误信息，全部通过返回null
 */
export const validateFields = (fields: Array<{ valid: boolean; message?: string }>): string | null => {
  for (const field of fields) {
    if (!field.valid) {
      return field.message || '输入格式错误'
    }
  }
  return null
} 