<template>
  <div>
    <!-- 顶部通知区域 -->
    <div class="row mb-4">
      <div class="col-md-8">
        <div class="notification-bar bg-white rounded p-3 shadow-sm">
          <div class="d-flex align-items-center">
            <span class="badge bg-danger me-3">52</span>
            <div class="flex-grow-1">
              <h6 class="mb-1">《虚幻》魔学院 · 新任务题</h6>
              <small class="text-muted">来源：《虚幻》学院 · Unreal Engine 4基础建模制作完整实战案例教程</small>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="survey-card bg-white rounded p-3 shadow-sm text-center">
          <i class="bi bi-chat-square-text fs-4 text-primary mb-2"></i>
          <div>
            <strong>调查反馈</strong>
            <br>
            <small class="text-muted">意见建议反馈，我们持续改进</small>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="stat-card bg-white rounded p-4 shadow-sm text-center">
          <i class="bi bi-send text-info fs-1 mb-3"></i>
          <h2 class="text-info mb-1">3</h2>
          <p class="text-muted mb-0">今日任务数</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="stat-card bg-white rounded p-4 shadow-sm text-center">
          <i class="bi bi-pencil text-primary fs-1 mb-3"></i>
          <h2 class="text-primary mb-1">0</h2>
          <p class="text-muted mb-0">今日学习提交</p>
        </div>
      </div>
      <div class="col-md-4">
        <div class="video-card bg-white rounded shadow-sm overflow-hidden">
          <div class="position-relative">
            <img src="/placeholder.svg" alt="Video thumbnail" class="w-100" style="height: 120px; object-fit: cover;">
            <div class="play-overlay">
              <i class="bi bi-play-circle-fill text-white fs-1"></i>
            </div>
          </div>
          <div class="p-3">
            <small class="text-muted">最近学习</small>
            <h6 class="mb-0">【基础走向高级】UE4模型</h6>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐课程区域 -->
    <div class="courses-section">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="mb-0">课程推荐</h5>
        <a href="#" class="text-decoration-none">换一换</a>
      </div>

      <!-- 使用HomeView.vue的课程卡片展示格式 -->
      <section class="mt-0">
        <div class="container-fluid mt-0">
          <div class="row justify-content-center card-scale">
            <CourseCard 
              v-for="(course, index) in recommendedCourses" 
              :key="`recommended-${index}`"
              :course="course"
              :index="index"
            />
          </div>
          <!-- "查看更多"链接 -->
          <div class="row">
            <div class="col-12">
              <div style="position: relative; margin-top: -20px; margin-bottom: 30px;">
                <a href="#" class="more-link" style="margin-left: 55px; display: inline-block;">
                  查看更多推荐课程<span class="arrow">›</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CourseCard from '@/components/CourseCard.vue'

// 推荐课程数据
const recommendedCourses = ref([
  {
    id: 1,
    title: 'RizomUV 2024 新功能官方教学（2025-05-29 更新）',
    instructor: 'ABOUTCG',
    duration: '2小时',
    views: 1727,
    price: '免费',
    originalPrice: null,
    difficulty: '初级难度',
    badges: ['新功能', '官方教学'],
    thumbnail: '/img/u01.jpg',
    provider: {
      name: 'ABOUTCG',
      logo: '/img/logo3.png'
    }
  },
  {
    id: 2,
    title: '高精度写实枪械SCR建模与贴图制作实战（Plasticity）',
    instructor: 'HX',
    duration: '22小时',
    views: 10565,
    price: '¥223.50',
    originalPrice: '¥298.00',
    difficulty: '中级难度',
    badges: ['限时限购'],
    thumbnail: '/img/u02.jpg',
    provider: {
      name: 'HX',
      logo: '/img/logo3.png'
    }
  },
  {
    id: 3,
    title: '流体水特效实义—Unreal Engine +Houdini特效实战案例教学',
    instructor: 'Collen',
    duration: '7小时',
    views: 3737,
    price: '¥175.44',
    originalPrice: '¥258.00',
    difficulty: '中级难度',
    badges: [],
    thumbnail: '/img/u03.jpg',
    provider: {
      name: 'Collen',
      logo: '/img/logo3.png'
    }
  },
  {
    id: 4,
    title: '【Blender+Unity】二次元原创角色完整金属质感美型教学',
    instructor: '阿Bolero',
    duration: '21小时',
    views: 4904,
    price: '¥189.04',
    originalPrice: '¥278.00',
    difficulty: '中级难度',
    badges: ['Blender+Unity'],
    thumbnail: '/img/u04.jpg',
    provider: {
      name: '阿Bolero',
      logo: '/img/logo3.png'
    }
  }
])
</script>

<style scoped>
.notification-bar {
  border-left: 4px solid #dc3545;
}

.survey-card:hover {
  transform: translateY(-2px);
  transition: transform 0.2s ease;
}

.stat-card {
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.video-card {
  transition: transform 0.2s ease;
}

.video-card:hover {
  transform: translateY(-2px);
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.8;
}

.more-link {
  color: #6c757d;
  text-decoration: none;
  font-size: 0.9rem;
}

.more-link:hover {
  color: #495057;
}

.arrow {
  margin-left: 5px;
  font-size: 1.2em;
}

.card-scale {
  margin-left: -15px;
  margin-right: -15px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .more-link {
    margin-left: 20px !important;
  }
}
</style> 