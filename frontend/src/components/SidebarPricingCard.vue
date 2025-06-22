<!-- SidebarPricingCard.vue - 侧边栏价格卡片组件 -->
<template>
  <div class="course-sidebar position-sticky">
    <div class="card shadow-sm">
      <div class="card-body p-4">
        <!-- 课程价格 -->
        <div class="mb-4">
          <div class="d-flex align-items-baseline mb-2">
            <span class="h3 mb-0 fw-bold text-success">
              {{ courseInfo.isFree ? '免费' : `¥${courseInfo.price}` }}
            </span>
            <span v-if="!courseInfo.isFree && courseInfo.originalPrice" class="text-muted text-decoration-line-through ms-2">
              ¥{{ courseInfo.originalPrice }}
            </span>
          </div>
          <small class="text-muted">{{ courseInfo.priceNote }}</small>
        </div>

        <!-- VIP 优惠信息 -->
        <div v-if="vipDiscount" class="alert alert-warning mb-3">
          <div class="d-flex align-items-center">
            <i class="fas fa-crown text-warning me-2"></i>
            <div>
              <small class="mb-0">
                <strong>VIP 会员专享：</strong><br>
                立省 ¥{{ vipDiscount.savedAmount }}，仅需 ¥{{ vipDiscount.vipPrice }}
              </small>
            </div>
          </div>
        </div>

        <!-- 购买按钮组 -->
        <div class="d-grid gap-2 mb-4">
          <button 
            class="btn btn-success btn-lg"
            @click="handlePurchase"
          >
            <i class="fas fa-shopping-cart me-2"></i>
            {{ courseInfo.isFree ? '立即学习' : '立即购买' }}
          </button>
          
          <button 
            v-if="!courseInfo.isFree"
            class="btn btn-yellow-black"
            @click="handleVipPurchase"
          >
            <i class="fas fa-crown me-2"></i>
            开通VIP立即学
          </button>
          
          <button 
            class="btn btn-outline-secondary"
            @click="handleAddToCart"
          >
            <i class="far fa-heart me-2"></i>
            加入购物车
          </button>
        </div>

        <!-- 课程特色 -->
        <div class="mb-4">
          <h6 class="mb-3">课程特色</h6>
          <ul class="list-unstyled">
            <li v-for="feature in features" :key="feature" class="mb-2">
              <i class="fas fa-check text-success me-2"></i>
              <small>{{ feature }}</small>
            </li>
          </ul>
        </div>

        <!-- 服务标签 -->
        <div class="mb-4">
          <h6 class="mb-3">学习服务</h6>
          <div class="d-flex flex-wrap gap-2">
            <span 
              v-for="service in services" 
              :key="service.name"
              class="badge bg-light text-dark px-3 py-2 tag-item tag-wrapper"
            >
              {{ service.name }}
              <!-- 服务说明弹窗 -->
              <div class="service-popup">
                <div class="popup-header">
                  <h6 class="mb-2">{{ service.name }}</h6>
                </div>
                <div class="popup-content">
                  <p class="mb-0">{{ service.description }}</p>
                </div>
              </div>
            </span>
          </div>
        </div>

        <!-- 课程统计 -->
        <div class="border-top pt-3">
          <div class="row text-center">
            <div class="col-4">
              <div class="mb-1 fw-bold">{{ courseStats.studentCount }}</div>
              <small class="text-muted">学员</small>
            </div>
            <div class="col-4">
              <div class="mb-1 fw-bold">{{ courseStats.rating }}.0</div>
              <small class="text-muted">评分</small>
            </div>
            <div class="col-4">
              <div class="mb-1 fw-bold">{{ courseStats.lessonCount }}</div>
              <small class="text-muted">课时</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">


interface CourseInfo {
  isFree: boolean
  price?: number
  originalPrice?: number
  priceNote?: string
}

interface VipDiscount {
  savedAmount: number
  vipPrice: number
}

interface Service {
  name: string
  description: string
}

interface CourseStats {
  studentCount: string
  rating: number
  lessonCount: number
}

interface Props {
  courseInfo?: CourseInfo
  vipDiscount?: VipDiscount
  features?: string[]
  services?: Service[]
  courseStats?: CourseStats
}

withDefaults(defineProps<Props>(), {
  courseInfo: () => ({
    isFree: true,
    price: 299,
    originalPrice: 399,
    priceNote: '一次购买，永久学习'
  }),
  vipDiscount: () => ({
    savedAmount: 100,
    vipPrice: 199
  }),
  features: () => [
    '高清视频教学',
    '源码资料下载',
    '在线答疑服务',
    '学习进度跟踪',
    '完课证书认证'
  ],
  services: () => [
    { name: '答疑服务', description: '专业讲师在线答疑，解决学习过程中的疑问' },
    { name: '社群交流', description: '加入学习社群，与同学交流学习心得' },
    { name: '实战项目', description: '真实项目实战，提升实际工作能力' },
    { name: '就业指导', description: '提供就业指导和职业规划建议' }
  ],
  courseStats: () => ({
    studentCount: '1.2K',
    rating: 4,
    lessonCount: 25
  })
})

const handlePurchase = () => {
  console.log('立即购买')
  // TODO: 跳转到购买页面
}

const handleVipPurchase = () => {
  console.log('VIP购买')
  // TODO: 跳转到VIP购买页面
}

const handleAddToCart = () => {
  console.log('加入购物车')
  // TODO: 添加到购物车
}
</script>

<style scoped>
.course-sidebar {
  top: 80px;
  width: 300px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
}

/* VIP按钮样式 */
.btn-yellow-black {
  background-color: #ffc107 !important;
  color: #222 !important;
  border: 1px solid #ffc107 !important;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-yellow-black:hover,
.btn-yellow-black:focus {
  background-color: #ffc107 !important;
  color: #000 !important;
  border: 1px solid #ffc107 !important;
}

/* 服务标签样式 */
.tag-wrapper {
  position: relative;
  display: inline-block;
}

.service-popup {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  width: 280px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(30,127,152,0.2);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 1000;
}

.service-popup::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 8px;
  border-style: solid;
  border-color: rgba(30,127,152,0.2) transparent transparent transparent;
}

.tag-wrapper:hover .service-popup {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(-5px);
}

.popup-header h6 {
  color: #1E7F98;
  font-weight: 600;
  border-bottom: 1px solid rgba(30,127,152,0.1);
  padding-bottom: 8px;
}

.popup-content p {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

.tag-item:hover {
  background: rgba(30,127,152,0.2) !important;
  transition: all 0.3s ease;
}

/* 滚动条样式 */
.course-sidebar::-webkit-scrollbar {
  width: 8px;
}

.course-sidebar::-webkit-scrollbar-track {
  background: transparent;
}

.course-sidebar::-webkit-scrollbar-thumb {
  background-color: transparent;
  border: 1px solid var(--uai-tech-blue, #1E7F98);
  border-radius: 6px;
}

.course-sidebar::-webkit-scrollbar-thumb:hover {
  border-color: #35a4be;
}

/* Firefox兼容处理 */
.course-sidebar {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
}
</style> 