/**
 * 表单验证 composable
 * 提供统一的表单验证逻辑和状态管理
 */
import { ref, reactive, computed } from 'vue'
import { validatePhone, validateSmsCode, validatePassword, validateFields } from '@/utils/validators'
import toast from '@/utils/toast'

export interface FormField {
  value: string
  error: string
  touched: boolean
}

export interface ValidationRule {
  validator: (value: string) => { valid: boolean; message?: string }
  message?: string
}

export interface FormValidationOptions {
  showToastOnError?: boolean
  validateOnChange?: boolean
}

export function useFormValidation(options: FormValidationOptions = {}) {
  const {
    showToastOnError = false,
    validateOnChange = false
  } = options

  // 表单字段状态
  const fields = reactive<Record<string, FormField>>({})
  
  // 表单是否正在提交
  const isSubmitting = ref(false)
  
  // 表单是否有错误
  const hasErrors = computed(() => {
    return Object.values(fields).some(field => field.error !== '')
  })
  
  // 表单是否全部字段都已填写
  const isComplete = computed(() => {
    return Object.values(fields).every(field => field.value.trim() !== '')
  })
  
  // 表单是否有效（无错误且完整）
  const isValid = computed(() => {
    return isComplete.value && !hasErrors.value
  })

  /**
   * 注册表单字段
   * @param fieldName 字段名
   * @param initialValue 初始值
   */
  const registerField = (fieldName: string, initialValue: string = '') => {
    fields[fieldName] = {
      value: initialValue,
      error: '',
      touched: false
    }
  }

  /**
   * 设置字段值
   * @param fieldName 字段名
   * @param value 值
   */
  const setFieldValue = (fieldName: string, value: string) => {
    if (fields[fieldName]) {
      fields[fieldName].value = value
      fields[fieldName].touched = true
      
      if (validateOnChange) {
        validateField(fieldName)
      }
    }
  }

  /**
   * 设置字段错误
   * @param fieldName 字段名
   * @param error 错误信息
   */
  const setFieldError = (fieldName: string, error: string) => {
    if (fields[fieldName]) {
      fields[fieldName].error = error
    }
  }

  /**
   * 清除字段错误
   * @param fieldName 字段名
   */
  const clearFieldError = (fieldName: string) => {
    setFieldError(fieldName, '')
  }

  /**
   * 验证单个字段
   * @param fieldName 字段名
   * @param rules 验证规则
   */
  const validateField = (fieldName: string, rules?: ValidationRule[]) => {
    const field = fields[fieldName]
    if (!field) return false

    // 清除之前的错误
    field.error = ''

    // 如果有自定义规则，使用自定义规则
    if (rules) {
      for (const rule of rules) {
        const result = rule.validator(field.value)
        if (!result.valid) {
          field.error = result.message || rule.message || '输入格式错误'
          break
        }
      }
    } else {
      // 使用内置验证规则
      let validation: { valid: boolean; message?: string }

      switch (fieldName) {
        case 'phone':
        case 'phoneNumber':
          validation = validatePhone(field.value)
          break
        case 'smsCode':
        case 'verificationCode':
          validation = validateSmsCode(field.value)
          break
        case 'password':
        case 'newPassword':
        case 'oldPassword':
          validation = validatePassword(field.value)
          break
        default:
          validation = { valid: field.value.trim() !== '', message: '此字段不能为空' }
      }

      if (!validation.valid) {
        field.error = validation.message || '输入格式错误'
      }
    }

    return field.error === ''
  }

  /**
   * 验证所有字段
   * @param customRules 自定义规则映射
   */
  const validateAll = (customRules?: Record<string, ValidationRule[]>) => {
    let isAllValid = true

    for (const fieldName in fields) {
      const rules = customRules?.[fieldName]
      const fieldValid = validateField(fieldName, rules)
      if (!fieldValid) {
        isAllValid = false
      }
    }

    // 如果开启了错误提示且有错误，显示第一个错误
    if (showToastOnError && !isAllValid) {
      const firstError = Object.values(fields).find(field => field.error)?.error
      if (firstError) {
        toast.error(firstError)
      }
    }

    return isAllValid
  }

  /**
   * 重置表单
   */
  const resetForm = () => {
    for (const fieldName in fields) {
      fields[fieldName].value = ''
      fields[fieldName].error = ''
      fields[fieldName].touched = false
    }
    isSubmitting.value = false
  }

  /**
   * 清除所有错误
   */
  const clearAllErrors = () => {
    for (const fieldName in fields) {
      fields[fieldName].error = ''
    }
  }

  /**
   * 获取字段值
   * @param fieldName 字段名
   */
  const getFieldValue = (fieldName: string) => {
    return fields[fieldName]?.value || ''
  }

  /**
   * 获取字段错误
   * @param fieldName 字段名
   */
  const getFieldError = (fieldName: string) => {
    return fields[fieldName]?.error || ''
  }

  /**
   * 字段是否已触摸
   * @param fieldName 字段名
   */
  const isFieldTouched = (fieldName: string) => {
    return fields[fieldName]?.touched || false
  }

  /**
   * 表单提交处理
   * @param submitFn 提交函数
   * @param customRules 自定义验证规则
   */
  const handleSubmit = async (
    submitFn: () => Promise<void> | void,
    customRules?: Record<string, ValidationRule[]>
  ) => {
    // 验证表单
    if (!validateAll(customRules)) {
      return false
    }

    isSubmitting.value = true

    try {
      await submitFn()
      return true
    } catch (error: any) {
      if (showToastOnError) {
        toast.error(error.message || '操作失败，请重试')
      }
      return false
    } finally {
      isSubmitting.value = false
    }
  }

  return {
    // 状态
    fields,
    isSubmitting,
    hasErrors,
    isComplete,
    isValid,

    // 方法
    registerField,
    setFieldValue,
    setFieldError,
    clearFieldError,
    validateField,
    validateAll,
    resetForm,
    clearAllErrors,
    getFieldValue,
    getFieldError,
    isFieldTouched,
    handleSubmit
  }
} 