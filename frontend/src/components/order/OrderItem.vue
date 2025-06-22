<!-- OrderItem.vue - 单个订单商品展示组件 -->
<template>
  <div class="row align-items-center">
    <div class="col-md-8 d-flex align-items-center">
      <div class="product-img-container">
        <img :src="productImage" :alt="productName" class="product-img">
        <div class="img-overlay"></div>
      </div>
      <div class="ms-3">
        <h5 class="mb-0">{{ productName }}</h5>
      </div>
    </div>
    <div class="col-md-4 text-md-end mt-3 mt-md-0">
      <div class="text-muted small">实付金额:</div>
      <div class="text-tech fw-bold h5">¥ {{ paymentAmount.toFixed(2) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  productName: string
  productImage: string
  price: number
  paymentAmount: number
}

defineProps<Props>()
</script>

<style scoped>
.product-img-container {
  position: relative;
  width: 96px;
  height: 96px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid rgba(22, 109, 132, 0.2);
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.img-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(22, 109, 132, 0.2) 0%, transparent 100%);
}

.text-tech {
  color: var(--tech-blue, #166d84);
}
</style> 