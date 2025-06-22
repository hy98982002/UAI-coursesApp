<!-- PaymentMethod.vue - 支付方式选择组件 -->
<template>
  <div class="mb-4">
    <h5 class="mb-3">支付方式</h5>
    <div class="row">
      <div 
        v-for="method in paymentMethods" 
        :key="method.id"
        class="col-md-4 mb-3 mb-md-0"
      >
        <div 
          :class="['payment-option', { active: method.isActive }]" 
          @click="selectPayment(method.id)"
        >
          <div class="d-flex flex-column align-items-center">
            <div class="payment-icon">
              <img 
                v-if="method.id === 'alipay'"
                src="/img/支付宝支付.png" 
                :alt="method.name"
                class="payment-img"
              >
              <svg 
                v-else-if="method.id === 'wechat'"
                class="payment-svg" 
                viewBox="0 0 1024 1024" 
                version="1.1" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path d="M692.992 347.968c4.48 0 8.96 0.128 13.376 0.32-26.816-137.6-176.32-243.648-360.32-243.648-197.76 0-360.32 135.04-360.32 307.648 0 99.712 55.872 189.248 149.376 250.688l-34.112 106.624 130.688-62.72c49.28 10.24 89.152 21.248 138.368 21.248 13.888 0 27.584-0.64 41.152-1.92-9.6-30.08-15.36-61.568-15.36-94.336 0.064-158.336 139.84-284.032 297.152-283.904z m-194.368-97.92c30.528 0 55.296 24.768 55.296 55.296s-24.768 55.296-55.296 55.296-55.296-24.768-55.296-55.296 24.768-55.296 55.296-55.296z m-262.528 110.592c-30.528 0-55.36-24.768-55.36-55.296s24.832-55.296 55.36-55.296 55.232 24.768 55.232 55.296-24.704 55.296-55.232 55.296z" fill="#09BB07"></path>
                <path d="M1024 629.76c0-146.432-138.368-265.856-294.016-265.856-164.864 0-294.72 119.424-294.72 265.856 0 146.56 129.792 265.856 294.72 265.856 34.432 0 68.992-9.024 103.68-18.048l94.72 53.376-25.92-88.96c69.632-53.376 121.536-125.056 121.536-212.224z m-391.04-55.296c-21.12 0-38.272-17.152-38.272-38.272 0-21.12 17.152-38.272 38.272-38.272 21.12 0 38.272 17.152 38.272 38.272 0 21.12-17.152 38.272-38.272 38.272z m193.28 0c-21.12 0-38.272-17.152-38.272-38.272 0-21.12 17.152-38.272 38.272-38.272 21.12 0 38.272 17.152 38.272 38.272 0 21.12-17.152 38.272-38.272 38.272z" fill="#09BB07"></path>
              </svg>
            </div>
            <span class="mt-2 small">{{ method.name }}</span>
          </div>
          <div class="selected-mark"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PaymentMethod } from '../../types/order'

interface Props {
  paymentMethods: PaymentMethod[]
  selectedMethod: string
}

defineProps<Props>()

const emit = defineEmits<{
  'select-payment': [methodId: string]
}>()

const selectPayment = (methodId: string) => {
  emit('select-payment', methodId)
}
</script>

<style scoped>
.payment-option {
  position: relative;
  border: 1px solid #dee2e6;
  border-radius: 0.75rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
}

.payment-option:hover {
  border-color: #00A0E9;
  background-color: #f0f9ff;
}

.payment-option.active {
  border-color: #00A0E9;
  background-color: #f0f9ff;
}

.payment-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
}

.payment-img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.payment-svg {
  width: 40px;
  height: 40px;
}

.selected-mark {
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 20px 20px 0;
  border-color: transparent var(--tech-blue, #166d84) transparent transparent;
  opacity: 0;
  transition: opacity 0.3s ease;
  display: none !important;
}

.payment-option.active .selected-mark {
  opacity: 0;
}
</style> 