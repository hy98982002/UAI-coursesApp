<!-- CartSummary.vue - 购物车汇总和结算组件 -->
<template>
  <div style="width: 280px;">
    <div class="checkout-section">
      <!-- 小计 -->
      <div class="subtotal">
        <span>小计</span>
        <span>¥{{ summary.subtotal.toFixed(2) }}</span>
      </div>

      <!-- 优惠券按钮 -->
      <button class="coupon-btn" @click="selectCoupon">
        <i class="fas fa-ticket-alt me-2" style="color: #0d6efd;"></i>
        {{ summary.coupon ? summary.coupon : '选择优惠券' }}
      </button>

      <!-- 最终合计 -->
      <div class="final-total d-flex justify-content-between align-items-center">
        <h5 class="mb-0" style="font-weight: bold; font-size: 18px;">最终合计</h5>
        <div class="final-price">¥{{ summary.total.toFixed(2) }}</div>
      </div>

      <!-- 结算按钮 -->
      <button class="checkout-btn" @click="checkout" :disabled="summary.total === 0">
        进行结算
        <i class="fas fa-arrow-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CartSummary } from '../../types/cart'

interface Props {
  summary: CartSummary
}

defineProps<Props>()

const emit = defineEmits<{
  'select-coupon': []
  'checkout': []
}>()

const selectCoupon = () => {
  console.log('选择优惠券')
  emit('select-coupon')
}

const checkout = () => {
  console.log('进行结算')
  emit('checkout')
}
</script>

<style scoped>
/* 右侧结算区样式优化 */
.checkout-section {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  transform: translateX(-13px) translateY(45px);
}

/* 小计行样式 */
.subtotal {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 16px;
}

/* 优惠券按钮样式 */
.coupon-btn {
  width: 100%;
  padding: 10px;
  background: rgba(22,109,132,.08);
  border: none;
  border-radius: 6px;
  color: var(--uai-tech-blue, #166d84);
  text-align: center;
  margin-top: -8px;
  margin-bottom: 22px;
  font-size: 14px;
}

.coupon-btn:hover {
  background: rgba(22,109,132,.15);
}

/* 最终合计区域 */
.final-total {
  margin-bottom: 16px;
}

.final-total h5 {
  font-size: 14px;
  font-weight: normal;
}

.final-price {
  font-size: 27px;
  font-weight: bold;
  color: #ee9900;
}

/* 结算按钮 */
.checkout-btn {
  background: #1473e6;
  transform: translateY(-10px);
  width: 100%;
  padding: 10px;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkout-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.checkout-btn:hover:not(:disabled) {
  background: #0f64d2;
}

.checkout-btn i {
  margin-left: 6px;
}
</style> 