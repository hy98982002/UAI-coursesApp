<template>
    <div class="col-sm-6 col-md-3 mb-4">
      <a class="card-link-no-underline" href="javascript:void(0);">
        <div class="card h-100 card-glass">
          <img :alt="course.title" class="card-img-top" :src="course.image"/>
          <div class="card-body">
            <p class="card-text">{{ course.title }}</p>
          </div>
          <div class="card-footer">
            <small class="text-muted">{{ course.level }}</small>
            <small v-if="course.students" class="text-muted ms-2">{{ course.students }}</small>
            <span class="float-end text-success">{{ course.price }}</span>
          </div>
  
          <!-- 信息卡 - 仅当有详细信息时显示 -->
          <div v-if="course.badge && course.features" 
               class="course-pop" 
               :class="{ 'force-hide': isPopupHidden }"
               :style="getPopupPosition()">
            <h6 class="fw-bold mb-2">{{ course.title }}</h6>
            <span class="badge bg-info mb-2">{{ course.badge }}</span>
            <p class="small text-muted">{{ course.duration }}</p>
            <ul class="ps-3 small mb-3">
              <li v-for="(feature, i) in course.features" :key="i">{{ feature }}</li>
            </ul>
            <a href="javascript:void(0);" class="btn btn-sm btn-tech-blue d-block" @click="addToCart">添加入购物车</a>
            <a href="javascript:void(0);" class="close-dialog" @click.stop="closePopup">关闭对话框</a>
          </div>
        </div>
      </a>
    </div>
  </template>
  
  <script setup>
  import { ref, defineProps } from 'vue';
  
  const props = defineProps({
    course: {
      type: Object,
      required: true,
      default: () => ({
        title: '课程标题',
        image: '/placeholder.svg?height=200&width=300',
        level: '入门',
        students: '',
        price: '免费'
      })
    },
    index: {
      type: Number,
      default: 0
    }
  });
  
  const isPopupHidden = ref(false);
  
  // 关闭弹窗
  const closePopup = (event) => {
    event.preventDefault();
    isPopupHidden.value = true;
    
    // 300ms后重置状态，以便下次hover时可以再次显示
    setTimeout(() => {
      isPopupHidden.value = false;
    }, 300);
  };
  
  // 添加到购物车
  const addToCart = () => {
    console.log(`添加课程到购物车: ${props.course.title}`);
    // 这里可以添加购物车逻辑
  };
  
  // 根据卡片位置调整弹窗位置
  const getPopupPosition = () => {
    // 每行4个卡片，第4、8、12...个卡片的弹窗应该在左侧显示
    const isRightEdge = (props.index + 1) % 4 === 0;
    
    if (isRightEdge) {
      return {
        left: 'auto',
        right: 'calc(100% + 14px)',
        marginRight: '0'
      };
    }
    
    return {
      left: 'calc(100% + 14px)',
      marginLeft: '0'
    };
  };
  </script>
  
  <style scoped>
  /* 信息卡骨架 */
  .course-pop {
    position: absolute;
    top: 12px;
    margin-top: -15px;
    width: 380px;
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
  
  /* 小尖角 */
  .course-pop::before {
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
  
  /* 内容样式 */
  .course-pop h6 {
    font-size: 20px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
  }
  
  .course-pop .badge {
    background: rgba(30,127,152,0.08);
    color: #1E7F98;
    font-weight: 500;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 14px;
  }
  
  .course-pop .text-muted {
    color: #444 !important;
    font-size: 15px;
  }
  
  .course-pop ul {
    margin: 16px 0;
    padding-left: 20px;
  }
  
  .course-pop ul li {
    color: #333;
    margin-bottom: 12px;
    font-size: 15px;
    position: relative;
    list-style: none;
  }
  
  .course-pop ul li::before {
    content: "•";
    color: #1E7F98;
    font-weight: bold;
    position: absolute;
    left: -15px;
  }
  
  /* 按钮样式 */
  .course-pop .btn-tech-blue {
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
  
  .course-pop .btn-tech-blue:hover {
    background: #166d84;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(30,127,152,0.3);
  }
  
  /* 关闭按钮 */
  .course-pop .close-dialog {
    color: #666;
    font-size: 14px;
    text-align: center;
    display: block;
    margin-top: 16px;
    transition: all 0.3s ease;
  }
  
  .course-pop .close-dialog:hover {
    color: #1E7F98;
    text-decoration: none;
  }
  
  /* 仅在大屏幕上启用hover弹窗 */
  @media (min-width: 992px) {
    .card:hover .course-pop {
      opacity: 1;
      visibility: visible;
      transform: translateX(0) scale(1);
      pointer-events: auto;
    }
    
    /* 右侧卡片特殊处理 */
    .col-md-3:nth-child(4n) .course-pop::before {
      left: auto;
      right: -9px;
      transform: rotate(135deg);
    }
    
    /* 桥接功能 */
    .card:hover::after {
      content: '';
      position: absolute;
      top: 0;
      left: 100%;
      width: 24px;
      height: 100%;
    }
    
    .col-md-3:nth-child(4n) .card:hover::before {
      content: '';
      position: absolute;
      top: 0;
      right: 100%;
      width: 24px;
      height: 100%;
    }
    
    /* 确保鼠标已移到弹窗本身时也不会消失 */
    .course-pop:hover {
      opacity: 1;
      visibility: visible;
      transform: translateX(0) scale(1);
      pointer-events: auto;
    }
  }
  
  /* 添加一个用于手动控制显示状态的类 */
  .course-pop.force-hide {
    opacity: 0 !important;
    visibility: hidden !important;
    transform: translateX(12px) scale(.96) !important;
    pointer-events: none !important;
  }
  </style>