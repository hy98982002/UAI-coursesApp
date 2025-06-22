<!-- CartItem.vue - 单个购物车商品项组件 -->
<template>
  <div class="d-flex align-items-center py-3 border-bottom">
    <div style="width: 24px;">
      <input 
        type="checkbox" 
        class="form-check-input" 
        v-model="item.isSelected"
        @change="$emit('selection-changed', item)"
        style="margin-left: 0; position: relative;"
      >
    </div>
    <div class="d-flex align-items-center flex-grow-1 ms-4">
      <img 
        :src="item.image" 
        :alt="item.name" 
        style="width: 120px; height: 74px; object-fit: cover;" 
        class="rounded"
      >
      <div class="ms-3">
        <h6 class="mb-1 text-light-gray">{{ item.name }}</h6>
        <div class="text-muted" style="font-size: 12px;">
          讲师：{{ item.instructor }}
        </div>
        <div class="d-flex align-items-center mt-1">
          <span 
            v-if="item.badge"
            class="badge bg-info text-white me-2" 
            style="background-color: rgba(22,109,132,0.1); color: #166d84; font-weight: normal; font-size: 12px;"
          >
            {{ item.badge }}
          </span>
          <span class="text-warning" style="font-size: 12px;">{{ item.rating }}</span>
          <div class="text-warning ms-1" style="font-size: 12px;">
            <i 
              v-for="star in 5" 
              :key="star"
              :class="star <= item.rating ? 'fas' : 'far'"
              class="fa-star"
            ></i>
          </div>
        </div>
        <div class="text-muted mt-1" style="font-size: 12px;">
          {{ item.duration }} • {{ item.category }}
        </div>
      </div>
    </div>
    <div style="width: 100px; text-align: right;">
      <div class="text-warning" style="font-size: 14px;">¥{{ item.price.toFixed(2) }}</div>
      <div 
        v-if="item.originalPrice"
        class="text-decoration-line-through" 
        style="font-size: 12px;"
      >
        原价：¥{{ item.originalPrice.toFixed(2) }}
      </div>
    </div>
    <div style="width: 100px;" class="d-flex flex-column align-items-center action-column">
      <a 
        href="#" 
        class="text-muted mb-2"
        @click.prevent="$emit('favorite', item)"
      >
        <i class="far fa-heart favorite-icon action-icon"></i>
      </a>
      <a 
        href="#" 
        class="text-muted"
        @click.prevent="$emit('remove', item)"
      >
        <i class="far fa-trash-alt action-icon"></i>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CartItem } from '../../types/cart'

interface Props {
  item: CartItem
}

defineProps<Props>()

defineEmits<{
  'selection-changed': [item: CartItem]
  'favorite': [item: CartItem]
  'remove': [item: CartItem]
}>()
</script>

<style scoped>
.text-light-gray {
  font-size: 16px;
  color: #444;
}

.action-column {
  transform: translateX(15px);
}

.action-icon {
  opacity: 0.5;
}

.favorite-icon {
  color: #f0690e;
  opacity: 0.7;
}

.action-icon:hover {
  opacity: 1;
}
</style> 