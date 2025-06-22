<!-- CourseCatalog.vue - 课程目录组件 -->
<template>
  <div class="bg-white rounded p-3">
    <h4 class="mt-5 mb-3">课程目录</h4>
    <div class="catalog-wrapper rounded shadow-sm p-3">
      <ChapterItem
        v-for="(chapter, index) in chapters"
        :key="index"
        :chapter="chapter"
        @lesson-click="handleLessonClick"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import ChapterItem from './ChapterItem.vue'
import type { Chapter, Lesson } from '../types/course'

interface Props {
  chapters?: Chapter[]
}

withDefaults(defineProps<Props>(), {
  chapters: () => [
    {
      id: 'resources',
      title: '课程相关资料',
      lessonCount: 2,
      lessons: [
        {
          id: 'group',
          title: '加入交流群',
          duration: '',
          isFree: true
        },
        {
          id: 'files',
          title: '课程相关文件',
          duration: '',
          isFree: true
        }
      ]
    },
    {
      id: 'chapter1',
      title: '第一章：基本操作(免费试看)',
      lessonCount: 3,
      lessons: [
        {
          id: 'lesson1-1',
          title: '第一节：WorldMachine基础操作',
          duration: '0.2小时',
          isFree: true
        },
        {
          id: 'lesson1-2',
          title: '第二节：WorldMachine项目设置',
          duration: '0.2小时',
          isFree: true
        }
      ]
    }
  ]
})

const handleLessonClick = (lesson: Lesson) => {
  console.log('课程点击：', lesson)
  // TODO: 处理课程点击事件
}
</script>

<style scoped>
.catalog-wrapper {
  background-color: #f8f9fa;
}
</style> 