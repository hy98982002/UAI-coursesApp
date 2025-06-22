<!-- OrderInfo.vue - 订单信息展示和折叠组件 -->
<template>
  <div>
    <!-- Header with order number and collapse button -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div class="text-secondary fw-medium">
        订单: <span class="font-monospace">{{ orderInfo.orderId }}</span>
      </div>
      <button 
        class="btn btn-sm btn-outline-tech px-3"
        @click="toggleDetails"
      >
        <i :class="['fas', orderInfo.isDetailsVisible ? 'fa-chevron-up' : 'fa-chevron-down', 'me-1']"></i>
        {{ orderInfo.isDetailsVisible ? '收起' : '展开' }}
      </button>
    </div>

    <!-- Order details section - collapsible -->
    <div 
      v-show="orderInfo.isDetailsVisible" 
      class="collapse-content mb-4 transition"
    >
      <div class="bg-light rounded p-3 border-tech">
        <OrderItem 
          :product-name="orderInfo.productName"
          :product-image="orderInfo.productImage"
          :price="orderInfo.price"
          :payment-amount="orderInfo.paymentAmount"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import OrderItem from './OrderItem.vue'
import type { OrderInfo } from '../../types/order'

interface Props {
  orderInfo: OrderInfo
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'toggle-details': [isVisible: boolean]
}>()

const toggleDetails = () => {
  const newState = !props.orderInfo.isDetailsVisible
  emit('toggle-details', newState)
}
</script>

<style scoped>
.btn-outline-tech {
  color: var(--tech-blue, #166d84);
  border-color: transparent;
  background-color: transparent;
  transition: all 0.3s ease;
}

.btn-outline-tech:hover,
.btn-outline-tech:focus {
  color: var(--tech-blue-light, #1e7f98);
  background-color: var(--tech-blue-transparent, rgba(22, 109, 132, 0.1));
}

.border-tech {
  border: 1px solid rgba(22, 109, 132, 0.2);
}

.transition {
  transition: all 0.3s ease;
}

.collapse-content {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.font-monospace {
  font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
</style> 