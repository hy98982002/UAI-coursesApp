<template>
    <div id="backToTop" :class="{ 'show': isVisible }" @click="scrollToTop">
      <i class="fas fa-chevron-up"></i>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  
  const isVisible = ref(false);
  
  // 滚动到顶部
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };
  
  // 处理滚动事件
  const handleScroll = () => {
    const scrollY = window.scrollY;
    const pageHeight = Math.max(
      document.body.scrollHeight,
      document.body.offsetHeight,
      document.documentElement.clientHeight,
      document.documentElement.scrollHeight,
      document.documentElement.offsetHeight
    );
    
    // 当滚动超过页面高度的2/3时显示按钮
    isVisible.value = scrollY > (pageHeight * 2/3);
  };
  
  // 生命周期钩子
  onMounted(() => {
    window.addEventListener('scroll', handleScroll);
  });
  
  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll);
  });
  </script>
  
  <style scoped>
  /* 返回顶部按钮样式 */
  #backToTop {
    position: fixed;
    right: 30px;
    bottom: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.9);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 1000;
    transition: all 0.3s ease;
    opacity: 0;
    visibility: hidden;
    transform: translateY(20px);
    border: 1px solid rgba(22, 109, 132, 0.2);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
  }
  
  #backToTop:hover {
    background-color: #166d84;
    transform: translateY(0);
    box-shadow: 0 4px 15px rgba(22, 109, 132, 0.3);
  }
  
  #backToTop:hover i {
    color: #fff;
  }
  
  #backToTop i {
    font-size: 24px;
    color: #166d84;
    transition: color 0.3s ease;
  }
  
  #backToTop.show {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
  
  /* 移动设备上的样式调整 */
  @media (max-width: 768px) {
    #backToTop {
      right: 20px;
      bottom: 20px;
      width: 45px;
      height: 45px;
    }
  
    #backToTop i {
      font-size: 20px;
    }
  }
  </style>