<template>
  <div v-if="showAlert" class="password-alert">
    <div class="alert alert-info border-0 shadow-sm" role="alert">
      <div class="d-flex align-items-center">
        <i class="fas fa-shield-alt text-primary me-3" style="font-size: 1.3em;" aria-hidden="true"></i>
        <div class="flex-grow-1">
          <strong class="d-block mb-1">🔒 账户安全提醒</strong>
          <p class="mb-0 text-muted small">您还未设置登录密码，建议设置以提高账户安全性</p>
        </div>
        <div class="d-flex gap-2 ms-3">
          <button 
            class="btn btn-primary btn-sm px-3" 
            @click="goToSetPassword"
            aria-label="前往设置密码"
          >
            <i class="fas fa-key me-1"></i>
            设置密码
          </button>
          <button 
            class="btn btn-outline-secondary btn-sm" 
            @click="dismissAlert"
            aria-label="暂时关闭提醒"
            title="本次会话内不再显示"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const authStore = useAuthStore()

// 控制警告显示状态
const showAlert = ref(false)

// 计算属性：检查用户是否需要设置密码
const needSetPassword = computed(() => {
  return authStore.user && !authStore.user.has_password
})

// 检查是否应该显示警告
const checkShouldShowAlert = () => {
  if (!needSetPassword.value) {
    showAlert.value = false
    return
  }
  
  // 检查是否在本次会话中已经关闭过警告
  const dismissed = sessionStorage.getItem('password_alert_dismissed')
  showAlert.value = !dismissed
}

// 跳转到密码设置页面
const goToSetPassword = () => {
  router.push('/profile/security')
}

// 暂时关闭警告
const dismissAlert = () => {
  showAlert.value = false
  sessionStorage.setItem('password_alert_dismissed', 'true')
}

// 组件挂载时检查状态
onMounted(() => {
  checkShouldShowAlert()
})

// 暴露方法供父组件调用
defineExpose({
  checkShouldShowAlert
})
</script>

<style scoped>
.password-alert {
  margin-bottom: 1rem;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert {
  border-radius: 12px;
  background: linear-gradient(135deg, #e3f2fd 0%, #f8f9fa 100%);
  border: 1px solid #e1f5fe;
  padding: 1rem 1.25rem;
}

.btn-sm {
  font-size: 0.875rem;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border: none;
  box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
}

.btn-outline-secondary {
  border-color: #dee2e6;
  color: #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  border-color: #adb5bd;
  transform: translateY(-1px);
}

.text-primary {
  color: #007bff !important;
}

.small {
  font-size: 0.875rem;
}

.gap-2 {
  gap: 0.5rem;
}

.ms-3 {
  margin-left: 1rem;
}

.me-1 {
  margin-right: 0.25rem;
}

.me-3 {
  margin-right: 1rem;
}

.px-3 {
  padding-left: 1rem;
  padding-right: 1rem;
}
</style> 