<!-- RecommendSection.vue - 推荐课程组件 -->
<template>
  <div class="container mt-3 mb-5">
    <div class="d-flex justify-content-between align-items-center">
      <h3 class="recommend-title">您可能还会喜欢</h3>
      <button class="refresh-btn" @click="$emit('refresh')">
        <i class="fas fa-sync-alt me-2"></i> 换一换
      </button>
    </div>

    <div class="row g-4 recommend-courses">
      <div 
        v-for="course in courses" 
        :key="course.id"
        class="col-sm-6 col-md-3 mb-4"
      >
        <a class="recommend-link" href="javascript:void(0);" @click="$emit('view-course', course)">
          <div class="recommend-card recommend-card-glass">
            <img 
              :alt="course.title" 
              class="card-img-top recommend-card-img-top" 
              :src="course.image"
            />
            <div class="card-body">
              <p class="card-text">{{ course.title }}</p>
            </div>
            <div class="recommend-card-footer">
              <small class="text-muted">{{ course.level }}</small>
              <small class="text-muted ms-2">{{ course.studentCount }}学员</small>
              <span class="float-end text-success">
                {{ course.isFree ? '免费' : `¥${course.price}` }}
              </span>
            </div>

            <!-- 信息卡 -->
            <div class="recommend-pop">
              <h6 class="fw-bold mb-2">{{ course.title }}</h6>
              <span class="badge bg-info text-white me-2">{{ course.level }}课程</span>
              <p class="small text-muted">{{ course.duration }}</p>
              <ul class="ps-3 small mb-3">
                <li v-for="feature in course.features" :key="feature">{{ feature }}</li>
              </ul>
              <button 
                class="btn btn-sm btn-tech-blue w-100"
                @click.stop="$emit('add-to-cart', course)"
              >
                添加入购物车
              </button>
              <a href="javascript:void(0);" class="close-dialog">关闭对话框</a>
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RecommendCourse } from '../../types/cart'

interface Props {
  courses: RecommendCourse[]
}

defineProps<Props>()

defineEmits<{
  'add-to-cart': [course: RecommendCourse]
  'view-course': [course: RecommendCourse]
  'refresh': []
}>()
</script>

<style scoped>
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
</style> 