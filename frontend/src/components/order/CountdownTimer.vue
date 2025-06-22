<!-- CountdownTimer.vue - 支付倒计时组件 -->
<template>
  <div class="mt-4 pt-3 border-top">
    <div class="row align-items-center">
      <div class="col-md-7 mb-3 mb-md-0">
        <div class="d-flex align-items-center text-warning">
          <i class="fas fa-exclamation-circle me-2"></i>
          <span class="small">
            已为你锁定座位，请在 
            <span class="countdown-time">{{ formattedTime }}</span> 
            内完成支付即可
          </span>
        </div>
      </div>
      <div class="col-md-5 text-md-end">
        <div class="text-muted small">应付金额:</div>
        <div class="text-tech fw-bold h4">¥ {{ paymentAmount.toFixed(2) }}</div>
      </div>
    </div>

    <div class="mt-4 text-end">
      <button 
        class="btn btn-pay btn-lg px-5 py-2"
        :disabled="isExpired"
        @click="$emit('payment')"
      >
        {{ isExpired ? '支付已过期' : '立即支付' }}
      </button>
    </div>

    <div class="mt-3 text-end">
      <span class="small text-muted">付款有问题，点击</span>
      <a href="#" class="small text-tech ms-1">咨询</a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

interface Props {
  initialSeconds: number
  paymentAmount: number
}

const props = defineProps<Props>()

const seconds = ref(props.initialSeconds)
const isExpired = ref(false)
let timer: number | null = null

const formattedTime = computed(() => {
  const minutes = Math.floor(seconds.value / 60)
  const remainingSeconds = seconds.value % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
})

const startCountdown = () => {
  timer = window.setInterval(() => {
    if (seconds.value > 0) {
      seconds.value--
    } else {
      isExpired.value = true
      if (timer) {
        clearInterval(timer)
        timer = null
      }
    }
  }, 1000)
}

const emit = defineEmits<{
  'payment': []
  'expired': []
}>()

onMounted(() => {
  startCountdown()
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
})

// 监听过期状态
computed(() => {
  if (isExpired.value) {
    emit('expired')
  }
})
</script>

<style scoped>
.countdown-time {
  font-weight: bold;
  color: #dc3545;
}

.text-tech {
  color: var(--tech-blue, #166d84);
}

.btn-pay {
  background-color: #1473e6;
  color: #fff !important;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  font-weight: 600;
  padding: 12px 28px;
  transition: background-color 0.3s ease;
  text-align: center;
  transform: translateY(-3px);
}

.btn-pay:hover:not(:disabled) {
  background-color: #0f64d2;
  color: #fff !important;
}

.btn-pay:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  transform: none;
}
</style> 