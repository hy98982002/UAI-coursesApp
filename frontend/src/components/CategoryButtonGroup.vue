<template>
  <section class="py-0">
    <div class="container">
      <!-- 父容器用 flex+wrap 布局 -->
      <div class="d-flex flex-wrap justify-content-start btn-transform">
        <!-- 单个"按钮组单元"用一个包裹容器固定宽度 -->
        <div class="btn-wrap">
          <div class="btn-group w-100">
            <button class="btn btn-category" @click="selectCategory(title)">{{ title }}</button>
            <button class="btn btn-category dropdown-toggle dropdown-toggle-split"
                    data-bs-toggle="dropdown" aria-expanded="false" ref="dropdownToggle"></button>
            <ul class="dropdown-menu">
              <li v-for="(category, index) in categories" :key="index" class="dropdown-submenu">
                <a class="dropdown-item dropdown-toggle" href="#">{{ category.name }}</a>
                <ul class="dropdown-menu">
                  <li v-for="(subcategory, subIndex) in category.subcategories" :key="subIndex">
                    <a class="dropdown-item" href="#" @click.prevent="selectSubcategory(category.name, subcategory)">
                      {{ subcategory }}
                    </a>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  categories: {
    type: Array,
    default: () => []
  }
});

const dropdownToggle = ref(null);

// 选择主分类
const selectCategory = (category) => {
  console.log(`选择分类: ${category}`);
  // 这里可以添加选择分类的逻辑
};

// 选择子分类
const selectSubcategory = (category, subcategory) => {
  console.log(`选择子分类: ${category} - ${subcategory}`);
  // 这里可以添加选择子分类的逻辑
};

onMounted(() => {
  // 初始化子菜单交互
  const initSubmenus = () => {
    const submenus = document.querySelectorAll('.dropdown-submenu');
    
    submenus.forEach(submenu => {
      // 鼠标进入子菜单时
      submenu.addEventListener('mouseenter', () => {
        const dropdownMenu = submenu.querySelector('.dropdown-menu');
        if (dropdownMenu) {
          dropdownMenu.style.display = 'block';
        }
      });
      
      // 鼠标离开子菜单时
      submenu.addEventListener('mouseleave', () => {
        const dropdownMenu = submenu.querySelector('.dropdown-menu');
        if (dropdownMenu) {
          dropdownMenu.style.display = 'none';
        }
      });
    });
    
    // 为主下拉菜单添加鼠标事件
    const btnGroups = document.querySelectorAll('.btn-group');
    
    btnGroups.forEach(btnGroup => {
      const dropdownMenu = btnGroup.querySelector('.dropdown-menu');
      
      if (dropdownMenu) {
        // 鼠标进入按钮组时
        btnGroup.addEventListener('mouseenter', () => {
          dropdownMenu.style.display = 'block';
          const toggleButton = btnGroup.querySelector('.dropdown-toggle-split');
          if (toggleButton) {
            toggleButton.setAttribute('aria-expanded', 'true');
          }
        });
        
        // 鼠标离开按钮组时
        btnGroup.addEventListener('mouseleave', () => {
          dropdownMenu.style.display = 'none';
          const submenus = dropdownMenu.querySelectorAll('.dropdown-submenu .dropdown-menu');
          submenus.forEach(submenu => {
            submenu.style.display = 'none';
          });
          
          const toggleButton = btnGroup.querySelector('.dropdown-toggle-split');
          if (toggleButton) {
            toggleButton.setAttribute('aria-expanded', 'false');
          }
        });
      }
    });
  };
  
  // 确保DOM已完全渲染后再初始化
  setTimeout(initSubmenus, 100);
});
</script>

<style scoped>
/* 按钮组样式 */
.btn-transform {
  margin: 20px 0;
}

.btn-wrap {
  width: auto;
  min-width: 200px;
  margin-right: 20px;
  margin-bottom: 10px;
}

.btn-category {
  background: rgba(255, 255, 255, 0.9);
  color: #1a1a1a;
  border: 1px solid rgba(30, 127, 152, 0.2);
  font-weight: 500;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

.btn-category:hover {
  background: rgba(30, 127, 152, 0.1);
  border-color: #1E7F98;
  color: #1E7F98;
}

.dropdown-menu {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(30, 127, 152, 0.1);
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.dropdown-item:hover {
  background: rgba(30, 127, 152, 0.1);
  color: #1E7F98;
}

.dropdown-submenu {
  position: relative;
}

.dropdown-submenu .dropdown-menu {
  position: absolute;
  top: 0;
  left: 100%;
  margin-top: -1px;
  display: none;
}
</style> 