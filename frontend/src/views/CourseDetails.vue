<!-- CourseDetails.vue - 课程详情主页面组件 -->
<template>
  <div class="course-details-page">
    <!-- 登录后的导航栏 -->
    <AuthNavbar />

    <!-- 面包屑导航 -->
    <BreadcrumbNav :items="breadcrumbItems" />

    <!-- 课程详情主体 -->
    <section class="container">
      <!-- 课程封面和信息 -->
      <CourseHeroCard :courseInfo="courseInfo" />

      <!-- 选项卡和侧栏 -->
      <div class="row">
        <div class="col-lg-8">
          <CourseTabs :defaultTab="activeTab" />
        </div>
        
        <div class="col-lg-4">
          <SidebarPricingCard
            :courseInfo="sidebarCourseInfo"
            :vipDiscount="vipDiscount"
            :features="courseFeatures"
            :services="courseServices"
            :courseStats="courseStats"
          />
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="mt-5 py-4 text-center text-white">
      <div class="container">
        <p class="mb-0">&copy; 2024 UAI教育平台. 保留所有权利.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AuthNavbar from '../components/AuthNavbar.vue'
import BreadcrumbNav from '../components/BreadcrumbNav.vue'
import CourseHeroCard from '../components/CourseHeroCard.vue'
import CourseTabs from '../components/CourseTabs.vue'
import SidebarPricingCard from '../components/SidebarPricingCard.vue'
import type { BreadcrumbItem, CourseInfo } from '../types/course'

// 面包屑数据
const breadcrumbItems = ref<BreadcrumbItem[]>([
  { title: '首页', href: '/', path: '/' },
  { title: 'Unity', href: '/category/unity', path: '/category/unity' },
  { title: '零基础photoshopAI创意设计第一季' }
])

// 当前激活的标签页
const activeTab = ref('catalog')

// 课程信息
const courseInfo = ref<CourseInfo>({
  title: '零基础photoshopAI创意设计第一季',
  coverImage: '/img/py04.jpg',
  difficulty: '适合初学者',
  updatedLessons: 25,
  isFree: true,
  price: 299
})

// 侧边栏课程信息
const sidebarCourseInfo = ref({
  isFree: true,
  price: 299,
  originalPrice: 399,
  priceNote: '一次购买，永久学习'
})

// VIP优惠信息
const vipDiscount = ref({
  savedAmount: 100,
  vipPrice: 199
})

// 课程特色
const courseFeatures = ref([
  '高清视频教学',
  '源码资料下载',
  '在线答疑服务',
  '学习进度跟踪',
  '完课证书认证'
])

// 学习服务
const courseServices = ref([
  { name: '答疑服务', description: '专业讲师在线答疑，解决学习过程中的疑问' },
  { name: '社群交流', description: '加入学习社群，与同学交流学习心得' },
  { name: '实战项目', description: '真实项目实战，提升实际工作能力' },
  { name: '就业指导', description: '提供就业指导和职业规划建议' }
])

// 课程统计
const courseStats = ref({
  studentCount: '1.2K',
  rating: 4,
  lessonCount: 25
})

// 页面挂载后的初始化
onMounted(() => {
  console.log('课程详情页面已加载')
  // TODO: 根据路由参数加载课程数据
  // TODO: 检查用户登录状态
  // TODO: 记录页面访问日志
})
</script>

<style scoped>
/* 页面基础样式 */
.course-details-page {
  font-family: "Alibaba PuHuiTi", "思源黑体", sans-serif;
  background-color: #F2F7F7;
  color: #111111;
  min-height: 100vh;
}

/* 页脚样式 */
footer {
  background-color: #1E7F98 !important;
  color: #fff !important;
}

/* 移动端适配 */
@media (max-width: 991.98px) {
  .col-lg-4 {
    margin-top: 2rem;
  }
}

/* 全局样式变量 */
:root {
  --uai-tech-blue: #1E7F98;
  --uai-light-blue: #BDECFD;
  --uai-hover-blue: rgba(35, 192, 247, 0.3);
  --uai-bg-gray: #F2F7F7;
  --uai-border-gray: rgba(222, 222, 222, 0.9);
}
</style>

<style>
/* 全局样式 */
body {
  font-family: "Alibaba PuHuiTi", "思源黑体", sans-serif;
  background-color: #F2F7F7;
  color: #111111;
}

/* 确保Bootstrap图标正常显示 */
.fa, .fas, .far {
  font-family: "Font Awesome 5 Free";
}

/* 确保阿里图标正常显示 */
.iconfont {
  font-family: "iconfont" !important;
}
</style> 