<template>
  <div style="background-color: black; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
    <!-- 注册容器 -->
    <div class="login-container">
      <!-- 关闭按钮 -->
      <span class="close-btn" @click="closeDialog">
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
              <SmsButton 
                :phone="registerForm.phoneNumber"
                @success="handleSmsSuccess"
                @error="handleSmsError"
              />
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
    </div>

    <!-- 底部黄色区域 -->
    <div class="yellow-footer">
      <div class="text-center mt-4" style="font-size: 17px">
        <p>
          我已有账户 <a href="#" class="text-primary" @click.prevent="goToLogin">去登录</a>
        </p>
      </div>
    </div>

    <!-- 提示消息 -->
    <div v-if="message" class="alert alert-info mt-3" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { validatePhone, validateSmsCode, validateFields } from '@/utils/validators'
import toast from '@/utils/toast'
import SmsButton from '@/components/SmsButton.vue'

const router = useRouter()

// 注册表单数据
const registerForm = ref({
  phoneNumber: '',
  verificationCode: '',
  agreement: false
})

// 表单验证计算属性
const isRegisterFormValid = computed(() => {
  const phoneValidation = validatePhone(registerForm.value.phoneNumber)
  const codeValidation = validateSmsCode(registerForm.value.verificationCode)
  
  return phoneValidation.valid && 
         codeValidation.valid && 
         registerForm.value.agreement
})

// SMS按钮事件处理
const handleSmsSuccess = (message) => {
  toast.success(message)
}

const handleSmsError = (message) => {
  toast.error(message)
}



// 注册提交
const handleRegister = async () => {
  // 表单验证
  const phoneValidation = validatePhone(registerForm.value.phoneNumber)
  const codeValidation = validateSmsCode(registerForm.value.verificationCode)
  
  const validationError = validateFields([phoneValidation, codeValidation])
  if (validationError) {
    toast.error(validationError)
    return
  }
  
  if (!registerForm.value.agreement) {
    toast.error('请先同意用户协议与服务条款')
    return
  }
  
  console.log('注册表单提交:', registerForm.value)
  
  try {
    // 调用后端API进行注册
    const authStore = useAuthStore()
    const result = await authStore.smsRegister(
      registerForm.value.phoneNumber, 
      registerForm.value.verificationCode
    )
    
    if (result.success) {
      const successMessage = result.needSetPassword 
        ? '注册成功！🎉\n为了帮您更好地管理账号，建议前往个人中心设置登录密码以提高账户安全性。'
        : '注册成功！🎉'
      
      toast.success(successMessage, {
        duration: 0, // 不自动关闭，让用户手动关闭
        closable: true
      })
      
      // 注册成功后跳转到首页
      setTimeout(() => {
        router.push('/')
      }, 3000)
    }
  } catch (error) {
    toast.error(error.message || '注册失败，请重试')
  }
}

// 跳转到登录页面
const goToLogin = () => {
  router.push('/login')
}

// 关闭对话框
const closeDialog = () => {
  console.log('关闭对话框')
  router.push('/') // 返回首页
}


</script>

<style scoped>
.login-container {
  max-width: 430px;
  background-color: #FBFBF6;
  padding: 20px 30px;
  border-radius: 15px;
  margin: auto;
  position: relative;
  z-index: 2;
}

.toggle-btn {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: white;
  color: black;
  border: 1px solid #ddd;
  border-radius: 15px;
  text-align: center;
  cursor: pointer;
  margin-top: 15px;
  -webkit-text-stroke: 0.1px black;
  transition: background-color 0.3s ease;
}

.toggle-btn:hover {
  background-color: #f8f9fa;
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

.input-group:focus-within {
  border-color: #ccc;
  box-shadow: none;
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
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.close-btn i {
  margin-top: -4px;
  display: block;
  line-height: 1;
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
  margin: auto;
  max-width: 430px;
  height: 80px;
  padding: 10px 20px;
  text-align: center;
  color: black;
  font-size: 16px;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  position: relative;
  z-index: 1;
  margin-top: -12px;
  background-color: #f8cc61;
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

.text-center {
  margin-top: 70px;
}

#form-check {
  margin-top: 25px;
  margin-bottom: 30px;
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

/* 表单动画 */
.form-section {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    margin: 20px;
    padding: 15px 20px;
  }
  
  .yellow-footer {
    margin: 20px;
    margin-top: -12px;
  }
}
</style>
