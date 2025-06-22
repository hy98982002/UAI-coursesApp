<template>
  <!-- 模态框遮罩层 -->
  <div class="modal-overlay" @click="closeModal">
    <!-- 模态框容器 -->
    <div class="modal-container" @click.stop>
      <!-- 关闭按钮 -->
      <span class="close-btn" @click="closeModal">
        <i>×</i>
      </span>

      <!-- 快速注册表单 -->
      <div class="form-section">
        <h4 class="text-center mt-4">快速注册</h4>
        <form class="mt-4" @submit.prevent="handleRegister">
          <div class="mb-3">
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                v-model="registerForm.phoneNumber"
                placeholder="请输入手机号"
                required
              >
            </div>
          </div>
          <div class="mb-3 mt-4">
            <div class="code-input-container">
              <input 
                type="text" 
                class="form-control" 
                v-model="registerForm.verificationCode"
                placeholder="请输入验证码"
                required
              >
              <button 
                class="verification-code-btn" 
                type="button"
                @click="sendVerificationCode"
                :disabled="countdown > 0"
              >
                {{ countdown > 0 ? `${countdown}秒后重新获取` : '获取验证码' }}
              </button>
            </div>
          </div>
          <button type="submit" class="btn btn-dark w-100 mt-4" :disabled="!isRegisterFormValid">
            完成注册
          </button>

          <div class="form-check mt-4 text-center">
            <input 
              class="form-check-input" 
              type="checkbox" 
              v-model="registerForm.agreement"
              id="agreement"
              required
            >
            <label class="form-check-label" for="agreement">
              我已阅读并同意 <a href="#" class="text-link">《用户协议与服务条款》</a>
            </label>
          </div>
        </form>
      </div>

      <!-- 底部黄色区域 -->
      <div class="yellow-footer">
        <div class="text-center mt-4" style="font-size: 17px">
          <p>
            我已有账户 <a href="#" class="text-primary" @click.prevent="switchToLogin">去登录</a>
          </p>
        </div>
      </div>
    </div>

    <!-- 提示消息 -->
    <div v-if="message" class="alert alert-info mt-3" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 定义事件
const emit = defineEmits(['close'])

// 倒计时状态
const countdown = ref(0)
let countdownTimer = null

// 提示消息
const message = ref('')

// 注册表单数据
const registerForm = ref({
  phoneNumber: '',
  verificationCode: '',
  agreement: false
})

// 表单验证计算属性
const isRegisterFormValid = computed(() => {
  return registerForm.value.phoneNumber &&
         registerForm.value.verificationCode &&
         registerForm.value.agreement
})

// 发送验证码
const sendVerificationCode = () => {
  const phoneNumber = registerForm.value.phoneNumber

  if (!phoneNumber) {
    showMessage('请先输入手机号')
    return
  }

  // 手机号格式验证
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(phoneNumber)) {
    showMessage('请输入正确的手机号码')
    return
  }

  // 开始倒计时
  startCountdown()
  
  // TODO: 调用后端API发送验证码
  console.log(`向 ${phoneNumber} 发送验证码`)
  showMessage('验证码已发送')
}

// 倒计时功能
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

// 显示提示消息
const showMessage = (msg) => {
  message.value = msg
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

// 注册处理
const handleRegister = () => {
  console.log('注册表单提交:', registerForm.value)
  
  // TODO: 调用后端API进行注册
  showMessage('注册成功！请前往个人中心设置登录密码以提高账户安全性。')
  
  // 注册成功后关闭模态框
  setTimeout(() => {
    closeModal()
  }, 2000)
}

// 关闭模态框
const closeModal = () => {
  emit('close')
}

// 切换到登录
const switchToLogin = () => {
  closeModal()
  router.push('/login')
}

// 组件销毁时清理计时器
onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
/* 模态框遮罩层 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9998;
  padding: 20px;
}

/* 模态框容器 */
.modal-container {
  max-width: 430px;
  width: 100%;
  background-color: #FBFBF6;
  border-radius: 15px;
  position: relative;
  z-index: 9999;
  animation: modalFadeIn 0.3s ease-out;
  max-height: 90vh;
  overflow-y: auto;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-50px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* 表单区域 */
.form-section {
  padding: 20px 30px;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  width: 25px;
  height: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: background-color 0.3s ease;
  z-index: 10000;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.close-btn i {
  margin-top: -4px;
  display: block;
  line-height: 1;
}

.btn-dark {
  background-color: black;
  color: white;
  border-radius: 15px;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  transition: background-color 0.3s ease;
  height: 50px;
}

.btn-dark:hover:not(:disabled) {
  background-color: #2c2c2c;
}

.btn-dark:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.form-control {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  height: 50px;
  transition: border-color 0.3s ease;
}

.form-control:hover,
.form-control:focus,
.form-control:active,
.form-control:focus-visible {
  border-color: black;
  box-shadow: none !important;
  outline: none !important;
}

.text-link {
  color: #007bff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.text-link:hover {
  color: #0056b3;
  text-decoration: none;
}

.form-check {
  font-size: 13px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.form-check-input {
  margin-top: 0.35em;
  float: none;
}

.form-check-label {
  margin-left: 0.25rem;
}

.yellow-footer {
  max-width: 430px;
  height: 80px;
  padding: 10px 20px;
  text-align: center;
  color: black;
  font-size: 16px;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  position: relative;
  background-color: #f8cc61;
  margin-top: -15px;
}

.yellow-footer a {
  color: #007bff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.yellow-footer a:hover {
  color: #0056b3;
  text-decoration: underline;
}

/* 验证码按钮样式 */
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

.code-input-container {
  position: relative;
}

/* 密码输入容器样式 */
.password-input-container {
  position: relative;
}

.password-toggle-btn {
  background: none;
  border: none;
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  cursor: pointer;
  z-index: 10;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
}

.password-toggle-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.password-toggle-btn:focus {
  outline: none;
  background-color: rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .modal-container {
    margin: 10px;
    max-height: 95vh;
  }
  
  .form-section {
    padding: 15px 20px;
  }
}
</style> 