<!-- EmptyCart.vue - 空购物车提示组件 -->
<template>
  <div class="empty-cart-container text-center py-5">
    <div class="empty-cart-icon mb-4">
      <i class="fas fa-shopping-cart" style="font-size: 80px; color: #ddd;"></i>
    </div>
    <h4 class="mb-3" style="color: #666;">您的购物车还是空的</h4>
    <p class="text-muted mb-4">
      快去选购您喜欢的课程吧！
    </p>
    <button 
      class="btn btn-primary px-4 py-2"
      @click="$emit('go-shopping')"
      style="background: #1E7F98; border-color: #1E7F98;"
    >
      <i class="fas fa-search me-2"></i>
      去逛逛
    </button>
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  'go-shopping': []
}>()
</script>

<style scoped>
.empty-cart-container {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.empty-cart-icon {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.btn:hover {
  background: #166d84 !important;
  border-color: #166d84 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(30, 127, 152, 0.3);
}
</style> 