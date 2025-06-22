<!-- CourseRelated.vue - 相关课程组件 -->
<template>
  <div class="bg-white rounded p-3">
    <h4 class="mt-5 mb-3">相关课程推荐</h4>
    <div class="row">
      <div 
        v-for="course in relatedCourses" 
        :key="course.id"
        class="col-md-6 col-lg-4 mb-4"
      >
        <div class="card course-item h-100" @click="handleCourseClick(course)">
          <img 
            :src="course.coverImage" 
            class="card-img-top"
            :alt="course.title"
            style="height: 180px; object-fit: cover;"
          >
          <div class="card-body d-flex flex-column">
            <h6 class="card-title mb-2">{{ course.title }}</h6>
            <p class="card-text text-muted small mb-2">
              {{ course.instructor }} · {{ course.difficulty }}
            </p>
            <div class="mt-auto">
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-warning fw-bold">
                  {{ course.isFree ? '免费' : `¥${course.price}` }}
                </span>
                <small class="text-muted">{{ course.studentCount }}人学习</small>
              </div>
              <div class="mt-2">
                <div class="d-flex align-items-center">
                  <div class="stars me-2">
                    <i 
                      v-for="star in 5"
                      :key="star"
                      :class="star <= course.rating ? 'fas' : 'far'"
                      class="fa-star text-warning"
                      style="font-size: 12px;"
                    ></i>
                  </div>
                  <small class="text-muted">{{ course.rating }}.0</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface RelatedCourse {
  id: string
  title: string
  coverImage: string
  instructor: string
  difficulty: string
  price?: number
  isFree: boolean
  studentCount: number
  rating: number
}

const relatedCourses = ref<RelatedCourse[]>([
  {
    id: '1',
    title: 'Unity 3D游戏开发入门',
    coverImage: '/img/py04.jpg',
    instructor: '张老师',
    difficulty: '初级',
    isFree: false,
    price: 299,
    studentCount: 1200,
    rating: 4
  },
  {
    id: '2',
    title: 'Photoshop AI设计进阶',
    coverImage: '/img/py04.jpg',
    instructor: '李老师',  
    difficulty: '中级',
    isFree: true,
    studentCount: 800,
    rating: 5
  },
  {
    id: '3',
    title: 'Blender 3D建模基础',
    coverImage: '/img/py04.jpg',
    instructor: '王老师',
    difficulty: '初级',
    isFree: false,
    price: 199,
    studentCount: 600,
    rating: 4
  }
])

const handleCourseClick = (course: RelatedCourse) => {
  console.log('相关课程点击：', course)
  // TODO: 跳转到课程详情页
}
</script>

<style scoped>
.course-item {
  transition: all 0.3s ease;
  cursor: pointer;
}

.course-item:hover {
  background: rgba(22,109,132,0.05) !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.card-img-top {
  border-radius: 0.375rem 0.375rem 0 0;
}

.stars .fa-star {
  margin-right: 2px;
}
</style> 