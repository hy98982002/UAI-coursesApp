<!-- ShoppingCart.vue - 购物车主页面组件 -->
<template>
  <div class="shopping-cart-page">
    <!-- 复用登录后的导航栏 -->
    <AuthNavbar />

    <!-- 购物车主体 -->
    <div class="container mt-4">
      <div class="d-flex">
        <!-- 左侧主要内容 -->
        <div class="main-content">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="m-0 cart-title">购物车</h5>
            <a href="#" class="text-primary clear-cart-btn" @click.prevent="clearCart">
              清空购物车
            </a>
          </div>

          <!-- 购物车内容区域 -->
          <div class="card border-0 bg-white rounded-lg p-4">
            <!-- 空购物车提示 -->
            <EmptyCart 
              v-if="cartItems.length === 0"
              @go-shopping="goShopping"
            />

            <!-- 有商品时显示表头和商品列表 -->
            <template v-else>
              <!-- 表头 -->
              <div class="d-flex border-bottom pb-3 table-header">
                <div style="width: 24px;">
                  <input 
                    type="checkbox" 
                    class="form-check-input" 
                    v-model="selectAll"
                    @change="toggleSelectAll"
                  >
                </div>
                <div class="flex-grow-1 ms-4">课程</div>
                <div style="width: 100px; text-align: right;">价格</div>
                <div class="action-column" style="width: 100px; text-align: center;">操作</div>
              </div>

              <!-- 商品列表 -->
              <CartItem
                v-for="item in cartItems"
                :key="item.id"
                :item="item"
                @selection-changed="handleSelectionChanged"
                @favorite="handleFavorite"
                @remove="handleRemove"
              />
            </template>
          </div>
        </div>

        <!-- 右侧促销结算区 -->
        <CartSummary
          v-if="cartItems.length > 0"
          :summary="cartSummary"
          @select-coupon="handleSelectCoupon"
          @checkout="handleCheckout"
        />
      </div>
    </div>

    <!-- 推荐课程部分 -->
    <RecommendSection 
      v-if="recommendCourses.length > 0"
      :courses="recommendCourses"
      @add-to-cart="addToCart"
      @view-course="viewCourse"
      @refresh="refreshRecommendations"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AuthNavbar from '../components/AuthNavbar.vue'
import CartItem from '../components/cart/CartItem.vue'
import CartSummary from '../components/cart/CartSummary.vue'
import EmptyCart from '../components/cart/EmptyCart.vue'
import RecommendSection from '../components/cart/RecommendSection.vue'
import type { CartItem as CartItemType, CartSummary as CartSummaryType, RecommendCourse } from '../types/cart'

// 数据初始化
const cartItems = ref<CartItemType[]>(getInitialCartData())
const recommendCourses = ref<RecommendCourse[]>(getRecommendData())
const selectAll = ref(false)

// 计算属性
const cartSummary = computed<CartSummaryType>(() => {
  const selectedItems = cartItems.value.filter(item => item.isSelected)
  const subtotal = selectedItems.reduce((sum, item) => sum + item.price, 0)
  const discount = 0
  const total = subtotal - discount
  
  return { subtotal, discount, total, coupon: undefined }
})

// 事件处理函数
const toggleSelectAll = () => {
  cartItems.value.forEach(item => {
    item.isSelected = selectAll.value
  })
}

const handleSelectionChanged = () => {
  selectAll.value = cartItems.value.every(item => item.isSelected)
}

const handleFavorite = (item: CartItemType) => {
  console.log('收藏商品：', item.name)
}

const handleRemove = (item: CartItemType) => {
  const index = cartItems.value.findIndex(cart => cart.id === item.id)
  if (index > -1) {
    cartItems.value.splice(index, 1)
  }
}

const clearCart = () => {
  if (confirm('确定要清空购物车吗？')) {
    cartItems.value = []
    selectAll.value = false
  }
}

const handleSelectCoupon = () => {
  console.log('选择优惠券')
}

const handleCheckout = () => {
  const selectedItems = cartItems.value.filter(item => item.isSelected)
  if (selectedItems.length === 0) {
    alert('请选择要结算的商品')
    return
  }
  console.log('进行结算：', selectedItems)
}

const goShopping = () => {
  console.log('去逛逛')
}

const refreshRecommendations = () => {
  console.log('换一换推荐')
}

const viewCourse = (course: RecommendCourse) => {
  console.log('查看课程：', course.title)
}

const addToCart = (course: RecommendCourse) => {
  console.log('添加到购物车：', course.title)
}

// 数据初始化函数
function getInitialCartData(): CartItemType[] {
  return [
    {
      id: '1',
      name: 'Houdini 20.5 CHOP模块基础与案例教学',
      image: '/img/ai04.jpg',
      instructor: '小宅',
      price: 202.64,
      originalPrice: 298.00,
      rating: 4.8,
      duration: '总共32.5小时',
      category: '实战',
      badge: '热门课程',
      isSelected: false
    },
    {
      id: '2',
      name: 'Houdini 20.5 CHOP模块基础与案例教学',
      image: '/img/ai03.jpg',
      instructor: '小宅',
      price: 202.64,
      originalPrice: 298.00,
      rating: 4.8,
      duration: '总共32.5小时',
      category: '实战',
      badge: '热门课程',
      isSelected: false
    },
    {
      id: '3',
      name: 'Houdini 20.5 CHOP模块基础与案例教学',
      image: '/img/ai01.jpg',
      instructor: '小宅',
      price: 202.64,
      originalPrice: 298.00,
      rating: 4.8,
      duration: '总共32.5小时',
      category: '实战',
      badge: '热门课程',
      isSelected: false
    }
  ]
}

function getRecommendData(): RecommendCourse[] {
  return [
    {
      id: 'r1',
      title: '构建虚幻引擎的基础',
      image: '/img/u01.jpg',
      level: '入门',
      studentCount: 390,
      isFree: true,
      duration: '总共 45 小时 · 入门级别',
      features: [
        '快速入门虚幻引擎界面与功能',
        '学习基础材质、光照与场景构建',
        '掌握蓝图编程核心概念'
      ]
    },
    {
      id: 'r2',
      title: '从0-1 游戏开发全流程',
      image: '/img/u02.jpg',
      level: '基础',
      studentCount: 500,
      isFree: true,
      duration: '总共 60 小时 · 基础级别',
      features: [
        '完整的游戏开发流程讲解',
        '从策划到程序，从美术到音效',
        '实战项目带你入门游戏开发'
      ]
    }
  ]
}

onMounted(() => {
  console.log('购物车页面已加载')
})
</script>

<style scoped>
/* 页面基础样式 */
.shopping-cart-page {
  font-family: "Alibaba PuHuiTi", "思源黑体", sans-serif;
  background: #F2F7F7;
  color: #111;
  min-height: 100vh;
}

/* 主要内容区域 */
.main-content {
  width: calc(100% - 300px);
  margin-right: 20px;
}

.cart-title {
  font-size: 24px;
  font-weight: bold;
}

.clear-cart-btn {
  color: #0d6efd !important;
  font-size: 14px;
  text-decoration: none;
  transform: translate(-15px, 8px);
}

.clear-cart-btn:hover {
  text-decoration: underline;
}

.table-header {
  color: #666;
}

.action-column {
  transform: translateX(15px);
}

/* 推荐课程样式 */
.recommend-title {
  font-size: 24px;
  font-weight: bold;
  margin: 40px 0 20px 0;
  position: relative;
  transform: translateY(-30px) translateX(-3px);
}

.recommend-courses {
  transition: opacity 0.3s ease;
  transform: translateY(-30px) translateX(-40px);
}

.refresh-btn {
  transform: translateY(-10px) translateX(-30px);
  display: inline-flex;
  align-items: center;
  color: var(--uai-tech-blue, #166d84);
  font-size: 14px;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 6px 12px;
  border-radius: 20px;
}

.refresh-btn:hover {
  background: rgba(22,109,132,.08);
}

.refresh-btn i {
  margin-right: 5px;
}

.recommend-card {
  border-radius: 10px;
  border: 1px solid #ddd;
  transition: all 0.3s ease-in-out;
  margin: 0 -2px;
  position: relative;
}

.recommend-card:hover {
  box-shadow: -2px 0 4px rgba(0, 0, 0, 0.08),
              2px 0 4px rgba(0, 0, 0, 0.08),
              0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 2000;
}

.recommend-card-img-top {
  border-radius: 10px 10px 0 0;
  transition: all 0.3s ease-in-out;
  height: 150px;
  object-fit: cover;
}

.recommend-card-footer {
  background: rgba(255, 255, 255, 0.75) !important;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0 0 10px 10px !important;
  position: relative;
  z-index: 1;
  margin: 0;
  padding: 0.75rem 1.25rem;
  overflow: hidden;
}

.recommend-link {
  text-decoration: none;
  color: inherit;
}

.recommend-link:hover,
.recommend-link:focus,
.recommend-link:active {
  text-decoration: none;
  color: inherit;
}

.recommend-card-glass {
  position: relative;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  overflow: visible;
  height: 100%;
}

/* 信息卡弹出效果 */
.recommend-pop {
  position: absolute;
  top: 12px;
  left: 100%;
  margin-left: 16px;
  margin-top: -15px;
  width: 340px;
  background: rgba(255,255,255,0.98);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(30,127,152,0.08);
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(30,127,152,0.06),
              0 2px 8px rgba(30,127,152,0.04),
              inset 0 0 0 1px rgba(255,255,255,0.6);
  padding: 24px;
  opacity: 0;
  visibility: hidden;
  transform: translateX(12px) scale(.96);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
  z-index: 1050;
}

.recommend-pop::before {
  content: "";
  position: absolute;
  left: -9px;
  top: 30px;
  width: 18px;
  height: 18px;
  background: rgba(255,255,255,0.98);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(30,127,152,0.08);
  border-right: none;
  border-bottom: none;
  transform: rotate(-45deg);
  box-shadow: inset 1px 1px 0 rgba(255,255,255,0.6);
}

@media (min-width: 992px) {
  .recommend-card:hover .recommend-pop {
    opacity: 1;
    visibility: visible;
    transform: translateX(0) scale(1);
    pointer-events: auto;
  }
}

.recommend-pop h6 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 16px;
  letter-spacing: 0.5px;
}

.recommend-pop .badge {
  background: rgba(30,127,152,0.08);
  color: #1E7F98;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.recommend-pop .text-muted {
  color: #444 !important;
  font-size: 15px;
}

.recommend-pop ul {
  margin: 16px 0;
  padding-left: 20px;
}

.recommend-pop ul li {
  color: #333;
  margin-bottom: 12px;
  font-size: 15px;
  position: relative;
  list-style: none;
}

.recommend-pop ul li::before {
  content: "•";
  color: #1E7F98;
  font-weight: bold;
  position: absolute;
  left: -15px;
}

.recommend-pop .btn-tech-blue {
  background: #1E7F98;
  color: #fff;
  border: none;
  border-radius: 25px;
  padding: 10px 24px;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-transform: none;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(30,127,152,0.2);
}

.recommend-pop .btn-tech-blue:hover {
  background: #166d84;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(30,127,152,0.3);
}

.recommend-pop .close-dialog {
  color: #666;
  font-size: 14px;
  text-align: center;
  display: block;
  margin-top: 16px;
  transition: all 0.3s ease;
  text-decoration: none;
}

.recommend-pop .close-dialog:hover {
  color: #1E7F98;
  text-decoration: none;
}

/* 响应式适配 */
@media (max-width: 991.98px) {
  .main-content {
    width: 100%;
    margin-right: 0;
  }
}
</style> 