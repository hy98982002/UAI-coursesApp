<!-- AuthNavbar.vue - 用户登录后的导航栏组件 -->
<template>
  <!-- 顶部导航开始 -->
  <nav class="navbar navbar-expand-lg navbar-light bg-white">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img src="/img/logo3.png" alt="" class="logo-img">
      </a>

      <!-- 小屏和中屏时显示在右侧的图标组 -->
      <div class="d-flex d-lg-none align-items-center ms-auto me-3">
        <!-- 购物车图标 -->
        <a href="#" class="text-dark me-3">
          <i class="iconfont icon-gouwuche nav-cart-icon"></i>
        </a>
        <!-- 通知图标 -->
        <a href="#" class="text-dark position-relative mx-2">
          <i class="far fa-bell" style="font-size: 20px;"></i>
          <span v-if="hasNotifications" class="badge-dot"></span>
        </a>
        <!-- 头像 -->
        <a href="#" class="mx-2">
          <img :src="userAvatar" class="avatar-sm" alt="用户头像">
        </a>
      </div>

      <button 
        class="navbar-toggler ms-2" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarSupportedContent" 
        aria-controls="navbarSupportedContent" 
        aria-expanded="false" 
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <!-- 搜索框（小屏时显示） -->
        <form class="d-flex d-lg-none mb-3 mt-2 w-100" @submit.prevent="handleSearch">
          <div class="input-group w-100">
            <input 
              type="search" 
              class="form-control" 
              placeholder="搜索课程"
              v-model="searchQuery"
            >
            <button class="btn search-btn" type="submit">
              <i class="fas fa-search"></i>
            </button>
          </div>
        </form>

        <ul class="navbar-nav me-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">
              <span class="nav-underline">UAI学院</span>
              <span class="visually-hidden">(current)</span>
            </a>
          </li>
          <li class="nav-item dropdown">
            <a 
              class="nav-link dropdown-toggle" 
              href="#" 
              id="navbarDropdown1" 
              role="button" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <span class="nav-underline">AIGC创意师</span>
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#">AI+logo设计师</a></li>
              <li><a class="dropdown-item" href="#">AI+包装师</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#">Something else here</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a 
              class="nav-link dropdown-toggle" 
              href="#" 
              id="navbarDropdown2" 
              role="button" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <span class="nav-underline">AI编程</span>
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="#">AI+logo设计师</a></li>
              <li><a class="dropdown-item" href="#">AI+包装师</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#">Something else here</a></li>
            </ul>
          </li>
        </ul>

        <!-- 右侧整体区域（大屏时显示） -->
        <div class="d-none d-lg-flex align-items-center right-group">
          <!-- 搜索框（大屏时显示） -->
          <form class="d-flex my-2 my-lg-0 me-3" @submit.prevent="handleSearch">
            <div class="input-group">
              <input 
                type="search" 
                class="form-control" 
                placeholder="搜索课程"
                v-model="searchQuery"
              >
              <button class="btn search-btn" type="submit">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </form>

          <!-- 购物车图标 -->
          <a href="#" class="text-dark me-3" @click="handleCartClick">
            <i class="iconfont icon-gouwuche nav-cart-icon"></i>
          </a>
          
          <!-- 通知图标 -->
          <a href="#" class="text-dark position-relative mx-3" @click="handleNotificationClick">
            <i class="far fa-bell" style="font-size: 20px;"></i>
            <span v-if="hasNotifications" class="badge-dot"></span>
          </a>
          
          <!-- 用户头像下拉菜单 -->
          <div class="dropdown mx-3">
            <a 
              href="#" 
              class="dropdown-toggle" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              <img :src="userAvatar" class="avatar-sm" alt="用户头像">
            </a>
            <ul class="dropdown-menu user-dropdown">
              <li><a @click="handleProfileClick" class="dropdown-item" href="#">个人资料</a></li>
              <li><a @click="handleCoursesClick" class="dropdown-item" href="#">我的课程</a></li>
              <li><a @click="handleOrdersClick" class="dropdown-item" href="#">订单管理</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a @click="handleLogout" class="dropdown-item" href="#">退出登录</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
  <!-- 顶部导航结束 -->
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 数据定义
const searchQuery = ref('')
const hasNotifications = ref(true)
const userAvatar = ref('/img/tou03.png')

// 事件处理
const handleSearch = () => {
  console.log('搜索：', searchQuery.value)
  // TODO: 实现搜索功能
}

const handleCartClick = () => {
  console.log('购物车点击')
  // TODO: 跳转到购物车页面
}

const handleNotificationClick = () => {
  console.log('通知点击')
  // TODO: 显示通知列表
}

const handleProfileClick = () => {
  console.log('个人资料点击')
  // TODO: 跳转到个人资料页面
}

const handleCoursesClick = () => {
  console.log('我的课程点击')
  // TODO: 跳转到我的课程页面
}

const handleOrdersClick = () => {
  console.log('订单管理点击')
  // TODO: 跳转到订单管理页面
}

const handleLogout = () => {
  console.log('退出登录')
  // TODO: 实现登出功能
}
</script>

<style scoped>
/* 通用导航文字 */
.nav-link {
  font-size: 18px;
  color: #000000 !important;
  font-weight: 400;
  text-decoration: none;
}

/* 下拉菜单箭头 */
.dropdown-toggle::after {
  border: none;
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  border-bottom: 2px solid black;
  border-right: 2px solid black;
  transform: rotate(45deg);
  margin-left: 6px;
  transition: transform 0.3s ease;
}

.dropdown-toggle[aria-expanded="true"]::after {
  transform: rotate(-135deg);
}

/* 下划线动画（仅作用于文字） */
.nav-underline {
  position: relative;
  display: inline-block;
}

.nav-underline::before {
  content: '';
  position: absolute;
  bottom: 0px;
  left: 0;
  width: 100%;
  height: 1.5px;
  background-color: #000;
  transform: scaleX(0);
  transform-origin: bottom center;
  transition: transform 0.3s ease;
}

.nav-link:hover .nav-underline::before,
.nav-link[aria-expanded="true"] .nav-underline::before {
  transform: scaleX(1);
}

/* 导航项及 Logo 布局 */
.nav-item {
  margin-left: 20px;
}

.navbar-brand {
  margin-right: 0;
  margin-left: 16px;
}

/* 右侧区域整体布局 */
.right-group {
  margin-right: 120px !important;
}

/* 移动端导航样式 */
@media (max-width: 991.98px) {
  .right-group {
    margin-right: 0 !important;
    flex-wrap: wrap;
  }

  .form-control[type="search"] {
    width: 100% !important;
    transform: none;
    margin-bottom: 10px;
  }

  .nav-icons-mobile {
    border-top: 1px solid rgba(0,0,0,0.1);
    margin-top: 10px;
    padding: 10px 0;
  }

  .nav-icons-mobile a {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
  }

  .nav-icons-mobile i {
    font-size: 20px;
    margin-bottom: 4px;
  }

  .nav-icons-mobile .small {
    font-size: 12px;
    color: #666;
  }

  .avatar-sm-mobile {
    width: 24px;
    height: 24px;
    margin-bottom: 4px;
  }

  .nav-icons-mobile .badge-dot {
    right: -2px;
    top: -2px;
  }
}

/* 搜索框 */
.form-control[type="search"] {
  border: 1.5px solid #1E7F98 !important;
  width: 450px !important;
  border-radius: 20px !important;
  transform: translateX(-50px);
}

/* 搜索框放大镜 */
.search-btn {
  border: none;
  background: none;
  padding: 8px;
  margin-left: -87px;
  z-index: 10;
  position: relative;
  color: #f0690e;
}

.search-btn:hover,
.search-btn:focus {
  outline: none;
  background-color: transparent;
}

/* 购物车图标 */
.nav-cart-icon {
  font-size: 22px;
  color: #000;
  margin-right: -2px;
}

/* 小头像 */
.avatar-sm {
  width: 34px;
  height: 34px;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 0 0 1px #e5e5e5;
  border-radius: 50%;
}

/* 红点提醒 */
.badge-dot {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 8px;
  height: 8px;
  background: #f0490e;
  border-radius: 50%;
}

/* 下拉菜单定制 */
.user-dropdown {
  border-radius: 10px;
  padding: .5rem 0;
}

.user-dropdown .dropdown-item {
  font-size: 14px;
  color: #5f6368;
}

.user-dropdown .dropdown-item:hover {
  background: rgba(30,127,152,.07);
  color: #000;
}

.user-dropdown .badge {
  font-size: 11px;
  padding: .2em .45em;
}

/* Logo 图片 */
.logo-img {
  height: 26px;
  width: auto;
  display: block;
  margin-top: -6px;
  filter: brightness(1.11);
}
</style> 