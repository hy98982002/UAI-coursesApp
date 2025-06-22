<template>
  <div>
    <!-- 返回顶部按钮 -->
    <BackToTop />
    
    <!-- 顶部导航开始 -->
    <Navbar @openLoginModal="openLoginModal" @openRegisterModal="openRegisterModal" />
    
    <!-- 注册模态框 -->
    <RegisterModal v-if="showRegisterModal" @close="closeRegisterModal" />
    
    <!-- 登录模态框 -->
    <LoginModal v-if="showLoginModal" @close="closeLoginModal" />
    
    <!-- 轮播图开始 -->
    <section class="mt-0">
      <div class="row g-0">
        <div class="row">
          <div class="col">
            <div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
              <ol class="carousel-indicators">
                <li data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active"></li>
                <li data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1"></li>
                <li data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2"></li>
              </ol>
              <div class="carousel-inner">
                <div class="carousel-item active">
                  <img alt="..." class="d-block w-100" src="/img/l01.jpg"/>
                  <div class="carousel-caption d-none d-md-block">
                    <h4>黑悟空</h4>
                    <p>来自虚幻引擎的创造</p>
                  </div>
                </div>
                <div class="carousel-item">
                  <img alt="..." class="d-block w-100" src="/img/l02.jpg"/>
                  <div class="carousel-caption d-none d-md-block">
                    <h4>AI创意设计师</h4>
                    <p>智能设计触手可及</p>
                  </div>
                </div>
                <div class="carousel-item">
                  <img alt="..." class="d-block w-100" src="/img/l03.jpg"/>
                  <div class="carousel-caption d-none d-md-block">
                    <h4>PythonAI工程师</h4>
                    <p>掌握AI未来核心技能</p>
                  </div>
                </div>
              </div>
              <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- 轮播图结束 -->

    <!--学院标题-->
    <section class="mt-3 py-0">
      <div class="container">
        <div class="row">
          <div class="col">
            <h4 class="uai-title">UAI学院</h4>
            <p class="uai-subtitle">学AI智能辅助设计，让工作更高效</p>
          </div>
        </div>
      </div>
    </section>
    
    <!--课程分类设置-->
    <CategoryButtonGroup 
      title="免费专区" 
      :categories="freeCategories" 
    />
    
    <!-- 卡片课程展示 -->
    <section class="mt-0">
      <div class="container mt-0">
        <div class="row justify-content-center card-scale">
          <CourseCard 
            v-for="(course, index) in freeCourses" 
            :key="`free-${index}`"
            :course="course"
            :index="index"
          />
        </div>
        <!-- "查看更多"链接 -->
        <div class="row">
          <div class="col-12">
            <div style="position: relative; margin-top: -20px; margin-bottom: 30px;">
              <a href="#" class="more-link" style="margin-left: 55px; display: inline-block;">
                查看更多免费课程<span class="arrow">›</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 分割线 -->
    <hr class="section-divider"/>
    
    <!--VIP专区-->
    <CategoryButtonGroup 
      title="VIP专区" 
      :categories="vipCategories" 
    />
    
    <!-- VIP课程展示 -->
    <section class="mt-2 py-0">
      <div class="container mt-0">
        <div class="row card-scale justify-content-center">
          <CourseCard 
            v-for="(course, index) in vipCourses" 
            :key="`vip-${index}`"
            :course="course"
            :index="index"
          />
        </div>
        <div class="row">
          <div class="col-12">
            <div style="position: relative; margin-top: -20px; margin-bottom: 30px;">
              <a href="#" class="more-link" style="margin-left: 55px; display: inline-block;">
                查看更多VIP课程<span class="arrow">›</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 分割线 -->
    <hr class="section-divider"/>
    
    <!--项目实战专区-->
    <CategoryButtonGroup 
      title="项目实战专区" 
      :categories="projectCategories" 
    />
    
    <!-- 项目实战课程展示 -->
    <section class="mt-0 py-2">
      <div class="container mt-0">
        <div class="row card-scale justify-content-center">
          <CourseCard 
            v-for="(course, index) in projectCourses" 
            :key="`project-${index}`"
            :course="course"
            :index="index"
          />
        </div>
        <div class="row">
          <div class="col-12">
            <div style="position: relative; margin-top: -20px; margin-bottom: 30px;">
              <a href="#" class="more-link" style="margin-left: 55px; display: inline-block;">
                查看更多项目实战课程<span class="arrow">›</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 分割线 -->
    <hr class="section-divider"/>
    
    <!--体系课标题-->
    <section class="mt-0 py-0">
      <div class="container pt-3">
        <div class="row">
          <div class="col">
            <h4 class="uai-title3">深课训练体系专区</h4>
            <p class="uai-subtitle3">全方位的训练课程服务</p>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 体系课程展示 -->
    <section class="mt-3 py-2">
      <div class="container mt-0">
        <div class="row card-scale justify-content-center">
          <CourseCard 
            v-for="(course, index) in systemCourses" 
            :key="`system-${index}`"
            :course="course"
            :index="index"
          />
        </div>
      </div>
    </section>
    
    <!--查看更多按钮-->
    <section class="mt-2 py-2">
      <div class="container">
        <div class="row">
          <div class="col">
            <div class="col text-center">
              <button class="btn btn-outline-dark" type="button" @click="viewMoreSystemCourses">
                查看更多深课体系课程<span style="margin-left: 6px; font-size: 1.3em;">›</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 页脚 -->
    <footer class="mt-5 py-4 bg-light">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <h5>UAI 教育平台</h5>
            <p class="text-muted">让AI智能辅助设计，让工作更高效</p>
          </div>
          <div class="col-md-6">
            <div class="row">
              <div class="col-6">
                <h6>课程分类</h6>
                <ul class="list-unstyled">
                  <li><a href="#" class="text-muted">免费课程</a></li>
                  <li><a href="#" class="text-muted">VIP课程</a></li>
                  <li><a href="#" class="text-muted">项目实战</a></li>
                </ul>
              </div>
              <div class="col-6">
                <h6>帮助中心</h6>
                <ul class="list-unstyled">
                  <li><a href="#" class="text-muted">联系我们</a></li>
                  <li><a href="#" class="text-muted">用户协议</a></li>
                  <li><a href="#" class="text-muted">隐私政策</a></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <hr class="mt-4">
        <div class="row">
          <div class="col-12 text-center">
            <p class="text-muted mb-0">&copy; 2024 UAI 教育平台. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import CourseCard from '@/components/CourseCard.vue'
import CategoryButtonGroup from '@/components/CategoryButtonGroup.vue'
import BackToTop from '@/components/BackToTop.vue'
import RegisterModal from '@/components/RegisterModal.vue'
import LoginModal from '@/components/LoginModal.vue'

// 路由相关
const route = useRoute()
const router = useRouter()

// 注册模态框显示状态
const showRegisterModal = ref(false)

// 登录模态框显示状态
const showLoginModal = ref(false)

// 打开注册模态框
const openRegisterModal = () => {
  showRegisterModal.value = true
}

// 关闭注册模态框
const closeRegisterModal = () => {
  showRegisterModal.value = false
}

// 打开登录模态框
const openLoginModal = () => {
  showLoginModal.value = true
}

// 关闭登录模态框
const closeLoginModal = () => {
  showLoginModal.value = false
}

// 免费课程分类
const freeCategories = ref([
  {
    name: 'AIGC创意师',
    subcategories: ['AI+logo设计师', 'AI+包装师', 'AI+品牌设计师']
  },
  {
    name: 'AI编程',
    subcategories: ['Python基础', 'AI算法', 'Web开发']
  },
  {
    name: '设计工具',
    subcategories: ['Photoshop', 'Illustrator', 'Figma']
  }
])

// VIP课程分类
const vipCategories = ref([
  {
    name: '高级AIGC',
    subcategories: ['高级AI设计', '商业案例', '项目实战']
  },
  {
    name: '专业编程',
    subcategories: ['深度学习', '机器学习', '数据分析']
  }
])

// 项目实战分类
const projectCategories = ref([
  {
    name: '真实项目',
    subcategories: ['企业合作项目', '创业项目', '毕业设计']
  },
  {
    name: '行业案例',
    subcategories: ['电商设计', '品牌设计', 'UI/UX设计']
  }
])

// 免费课程数据
const freeCourses = ref([
  {
    title: 'AI+logo设计师 0基础入门',
    image: '/img/ai01.jpg',
    level: '零基础',
    students: '1.2万人学习',
    price: '免费',
    badge: '热门课程',
    duration: '共24课时',
    features: [
      '从零开始学习AI logo设计',
      '掌握AI设计工具使用技巧',
      '学会商业logo设计思路',
      '提供实战项目练习'
    ]
  },
  {
    title: 'AI+包装师速成班',
    image: '/img/ai02.jpg',
    level: '初级',
    students: '8500人学习',
    price: '免费'
  },
  {
    title: 'Python AI基础编程',
    image: '/img/py01.jpg',
    level: '零基础',
    students: '2.1万人学习',
    price: '免费',
    badge: '推荐课程',
    duration: '共36课时',
    features: [
      'Python编程基础入门',
      'AI开发环境搭建',
      '机器学习算法基础',
      '实际案例代码实现'
    ]
  },
  {
    title: 'UI设计基础课程',
    image: '/img/u01.jpg',
    level: '入门',
    students: '1.5万人学习',
    price: '免费'
  }
])

// VIP课程数据
const vipCourses = ref([
  {
    title: '高级AI商业设计实战',
    image: '/img/ai03.jpg',
    level: '高级',
    students: '3200人学习',
    price: '¥599',
    badge: 'VIP专享',
    duration: '共48课时',
    features: [
      '商业级AI设计项目',
      '一对一导师指导',
      '真实客户案例实战',
      '就业推荐服务'
    ]
  },
  {
    title: '深度学习算法精通',
    image: '/img/py02.jpg',
    level: '专业',
    students: '2800人学习',
    price: '¥899'
  },
  {
    title: '全栈AI工程师',
    image: '/img/py03.jpg',
    level: '专业',
    students: '1900人学习',
    price: '¥1299',
    badge: '就业保障',
    duration: '共120课时',
    features: [
      '前端+后端+AI全栈开发',
      '企业级项目实战',
      '简历优化指导',
      '面试技巧培训'
    ]
  },
  {
    title: 'AI产品经理训练营',
    image: '/img/ai04.jpg',
    level: '中级',
    students: '2100人学习',
    price: '¥799'
  }
])

// 项目实战课程数据
const projectCourses = ref([
  {
    title: '电商平台AI设计项目',
    image: '/img/u02.jpg',
    level: '实战',
    students: '1200人参与',
    price: '¥399',
    badge: '真实项目',
    duration: '4周完成',
    features: [
      '真实电商客户需求',
      '团队协作开发',
      '导师全程指导',
      '作品集收录'
    ]
  },
  {
    title: '智能聊天机器人开发',
    image: '/img/py04.jpg',
    level: '实战',
    students: '980人参与',
    price: '¥499'
  },
  {
    title: 'AR/VR交互设计项目',
    image: '/img/u03.jpg',
    level: '高级',
    students: '650人参与',
    price: '¥799',
    badge: '前沿技术',
    duration: '6周完成',
    features: [
      '最新AR/VR技术应用',
      '交互设计原理',
      '用户体验优化',
      '行业实际应用案例'
    ]
  },
  {
    title: '区块链应用开发',
    image: '/img/u04.jpg',
    level: '高级',
    students: '420人参与',
    price: '¥999'
  }
])

// 体系课程数据
const systemCourses = ref([
  {
    title: 'AI全栈工程师认证体系',
    image: '/img/k01.png',
    level: '体系课',
    students: '5600人学习',
    price: '¥2999',
    badge: '认证体系',
    duration: '6个月完成',
    features: [
      '完整的学习路径规划',
      '阶段性考核认证',
      '项目作品集指导',
      '就业保障服务'
    ]
  },
  {
    title: 'AIGC创意设计师认证',
    image: '/img/k02.png',
    level: '体系课',
    students: '4200人学习',
    price: '¥1999'
  },
  {
    title: 'AI产品经理认证体系',
    image: '/img/k03.png',
    level: '体系课',
    students: '3100人学习',
    price: '¥2499',
    badge: '高薪就业',
    duration: '4个月完成',
    features: [
      'AI产品设计思维',
      '数据分析能力培养',
      '团队管理技能',
      '行业人脉资源'
    ]
  },
  {
    title: 'AI算法工程师认证',
    image: '/img/k04.png',
    level: '体系课',
    students: '2800人学习',
    price: '¥3499'
  }
])

// 查看更多体系课程
const viewMoreSystemCourses = () => {
  console.log('查看更多深课体系课程')
  // 这里可以添加路由跳转逻辑
}

// 初始化轮播图
onMounted(() => {
  // 确保Bootstrap已加载
  const initCarousel = () => {
    if (window.bootstrap) {
      const carouselElement = document.querySelector('#carouselExampleCaptions')
      if (carouselElement) {
        new window.bootstrap.Carousel(carouselElement, {
          interval: 5000,
          ride: 'carousel'
        })
      }
    }
  }
  
  // 延迟初始化，确保DOM已渲染
  setTimeout(initCarousel, 500)
})
</script>

<style scoped>
/* 标题样式 */
.uai-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.uai-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.uai-title3 {
  font-size: 2.2rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.uai-subtitle3 {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 1.5rem;
}

/* 分割线样式 */
.section-divider {
  border: none;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(30, 127, 152, 0.3), transparent);
  margin: 3rem 0;
}

/* 查看更多链接样式 */
.more-link {
  color: #1E7F98;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.more-link:hover {
  color: #166d84;
  text-decoration: none;
}

.more-link .arrow {
  margin-left: 5px;
  transition: transform 0.3s ease;
}

.more-link:hover .arrow {
  transform: translateX(5px);
}

/* 卡片缩放效果 */
.card-scale {
  perspective: 1000px;
}

/* 轮播图样式优化 */
.carousel-item img {
  height: 400px;
  object-fit: cover;
}

.carousel-caption {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  border-radius: 10px;
  padding: 20px;
  bottom: 50px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .uai-title {
    font-size: 2rem;
  }
  
  .uai-subtitle {
    font-size: 1rem;
  }
  
  .carousel-item img {
    height: 250px;
  }
  
  .carousel-caption {
    bottom: 20px;
    padding: 15px;
  }
}
</style> 