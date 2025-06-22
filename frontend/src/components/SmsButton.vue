<template>
  <button 
    class="verification-code-btn" 
    type="button"
    :disabled="isDisabled"
    @click="handleSendSms"
    :aria-label="buttonText"
  >
    {{ buttonText }}
  </button>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { validatePhone } from '@/utils/validators'
import { useAuthStore } from '@/store/auth'

// Props
const props = defineProps({
  phone: {
    type: String,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['success', 'error'])

// 状态
const countdown = ref(0)
const isSending = ref(false)
let countdownTimer = null

const authStore = useAuthStore()

// 计算属性
const isDisabled = computed(() => {
  return props.disabled || countdown.value > 0 || isSending.value
})

const buttonText = computed(() => {
  if (isSending.value) {
    return '发送中...'
  }
  if (countdown.value > 0) {
    return `${countdown.value}秒后重新获取`
  }
  return '获取验证码'
})

// 发送短信验证码
const handleSendSms = async () => {
  // 验证手机号
  const phoneValidation = validatePhone(props.phone)
  if (!phoneValidation.valid) {
    emit('error', phoneValidation.message)
    return
  }

  // 防止重复点击
  if (isSending.value) {
    return
  }

  isSending.value = true

  try {
    // 调用API发送验证码
    await authStore.sendSmsCode(props.phone)
    
    // 发送成功，开始倒计时
    startCountdown()
    emit('success', '验证码已发送')
  } catch (error) {
    emit('error', error.message || '验证码发送失败，请重试')
  } finally {
    isSending.value = false
  }
}

// 开始倒计时
const startCountdown = () => {
  countdown.value = 60
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
      countdownTimer = null
    }
  }, 1000)
}

// 清除倒计时（供父组件调用）
const clearCountdown = () => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
  countdown.value = 0
  isSending.value = false
}

// 组件销毁时清理定时器
onUnmounted(() => {
  clearCountdown()
})

// 暴露方法供父组件使用
defineExpose({
  clearCountdown
})
</script>

<style scoped>
.verification-code-btn {
  background-color: #f2f2f2;
  color: #007bff;
  font-weight: 500;
  font-size: 14px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  padding: 7px 14px;
  margin-right: 10px;
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.verification-code-btn:hover:not(:disabled),
.verification-code-btn:focus:not(:disabled) {
  color: #0056b3;
  background-color: #e9ecef;
  text-decoration: none;
  outline: none;
}

.verification-code-btn:disabled {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}
</style> 