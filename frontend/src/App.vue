<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // 加载外部字体和图标
  loadExternalResources()
})

// 加载外部资源
const loadExternalResources = () => {
  // 加载 Bootstrap CSS
  const bootstrapCSS = document.createElement('link')
  bootstrapCSS.rel = 'stylesheet'
  bootstrapCSS.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css'
  document.head.appendChild(bootstrapCSS)
  
  // 加载 Font Awesome
  const fontAwesome = document.createElement('link')
  fontAwesome.rel = 'stylesheet'
  fontAwesome.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
  document.head.appendChild(fontAwesome)
  
  // 加载阿里图标
  const aliIcon = document.createElement('link')
  aliIcon.rel = 'stylesheet'
  aliIcon.href = '/font/iconfont.css'
  document.head.appendChild(aliIcon)
  
  // 加载 Bootstrap JS
  const bootstrapJS = document.createElement('script')
  bootstrapJS.src = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.min.js'
  document.body.appendChild(bootstrapJS)
}
</script>

<style>
body {
  font-family: "Alibaba PuHuiTi", "思源黑体", sans-serif;
  background-color: #F2F7F7;
  color: #111111;
  padding-top: 56px;
}
</style>