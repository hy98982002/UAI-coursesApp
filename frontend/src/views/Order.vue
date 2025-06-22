<!-- Order.vue - 订单支付主页面组件 -->
<template>
  <div class="order-page">
    <div class="container-fluid bg-gradient py-5">
      <div class="row justify-content-center">
        <div class="col-12 col-md-10 col-lg-8">
          <div class="card glassmorphism">
            <div class="card-body p-md-5 p-4">
              <!-- 订单信息部分 -->
              <OrderInfo 
                :order-info="orderData.orderInfo"
                @toggle-details="handleToggleDetails"
              />

              <!-- 支付方式选择 -->
              <PaymentMethod
                :payment-methods="orderData.paymentMethods"
                :selected-method="orderData.selectedPaymentMethod"
                @select-payment="handleSelectPayment"
              />

              <!-- 倒计时和支付按钮 -->
              <CountdownTimer
                :initial-seconds="orderData.countdown.totalSeconds"
                :payment-amount="orderData.orderInfo.paymentAmount"
                @payment="handlePayment"
                @expired="handleExpired"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <OrderFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import OrderInfo from '../components/order/OrderInfo.vue'
import PaymentMethod from '../components/order/PaymentMethod.vue'
import CountdownTimer from '../components/order/CountdownTimer.vue'
import OrderFooter from '../components/order/OrderFooter.vue'
import type { OrderData } from '../types/order'

// 订单数据初始化
const orderData = ref<OrderData>({
  orderInfo: {
    orderId: '2505062044558686',
    productName: 'DeepSeek+SpringAI实战AI家庭医生应用',
    productImage: '/img/ai01.jpg',
    price: 199.00,
    paymentAmount: 199.00,
    isDetailsVisible: true
  },
  paymentMethods: [
    {
      id: 'alipay',
      name: '支付宝',
      icon: '/img/支付宝支付.png',
      isActive: true
    },
    {
      id: 'wechat',
      name: '微信支付',
      icon: 'wechat-svg',
      isActive: false
    }
  ],
  countdown: {
    totalSeconds: 36,
    minutes: 0,
    seconds: 36,
    isExpired: false
  },
  selectedPaymentMethod: 'alipay'
})

// 事件处理函数
const handleToggleDetails = (isVisible: boolean) => {
  orderData.value.orderInfo.isDetailsVisible = isVisible
}

const handleSelectPayment = (methodId: string) => {
  // 更新选中状态
  orderData.value.paymentMethods.forEach(method => {
    method.isActive = method.id === methodId
  })
  orderData.value.selectedPaymentMethod = methodId
  console.log('选择支付方式：', methodId)
}

const handlePayment = () => {
  console.log('处理支付：', {
    orderId: orderData.value.orderInfo.orderId,
    paymentMethod: orderData.value.selectedPaymentMethod,
    amount: orderData.value.orderInfo.paymentAmount
  })
  
  // TODO: 调用支付API
  alert(`使用${orderData.value.selectedPaymentMethod === 'alipay' ? '支付宝' : '微信支付'}支付 ¥${orderData.value.orderInfo.paymentAmount}`)
}

const handleExpired = () => {
  console.log('支付已过期')
  orderData.value.countdown.isExpired = true
  // TODO: 处理支付过期逻辑
}
</script>

<style scoped>
/* 页面基础样式 */
.order-page {
  font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.bg-gradient {
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f7ff 100%);
  flex: 1;
}

/* Glassmorphism 卡片 */
.glassmorphism {
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(22, 109, 132, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 0.75rem;
}

/* 响应式调整 */
@media (max-width: 767.98px) {
  .card-body {
    padding: 1.25rem;
  }
}

/* CSS 变量定义 */
:deep(.order-page) {
  --tech-blue: #166d84;
  --tech-blue-light: #1e7f98;
  --tech-blue-transparent: rgba(22, 109, 132, 0.1);
  --tech-red: #e63946;
  --tech-red-hover: #d62b39;
  --border-radius: 0.75rem;
}
</style> 