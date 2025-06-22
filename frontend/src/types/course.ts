// course.ts - 课程相关类型定义

export interface Lesson {
  id: string
  title: string
  duration: string
  isFree?: boolean
  isCompleted?: boolean
}

export interface Chapter {
  id: string
  title: string
  lessonCount: number
  lessons: Lesson[]
  isExpanded?: boolean
}

export interface CourseInfo {
  title: string
  coverImage: string
  difficulty: string
  updatedLessons: number
  isFree: boolean
  price?: number
}

export interface Review {
  id: string
  userName: string
  userAvatar: string
  rating: number
  content: string
  date: string
}

export interface BreadcrumbItem {
  title: string
  href?: string
  path?: string
} 