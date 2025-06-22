<!-- OrderFooter.vue - 订单页面页脚组件 -->
<template>
  <footer class="bg-dark text-light small mt-5">
    <div class="container">
      <div class="row pt-2 pb-3">
        <div class="col-sm-12 col-md-10">
          <div>
            <p class="mb-2 text-muted">UAI学院是一家为就业者提供最新职场技术的在线交流平台。</p>
            <div class="text-muted">
              网站呈现内容之版权均归 小木偶（天津）文化科技有限公司所有 
              <a 
                class="text-light ms-3 me-3"
                href="https://beian.miit.gov.cn"
                target="_blank"
                rel="noopener noreferrer"
              >
                津ICP备2024023837号-1
              </a>
              <a 
                class="text-light" 
                href="https://beian.mps.gov.cn/#/query/webSearch?code=12011002024104"
                rel="noreferrer" 
                target="_blank"
              >
                <img 
                  alt="备案图标" 
                  class="me-2 mb-1" 
                  height="16" 
                  src="/img/beian.png" 
                  width="16"
                />
                津公网安备12011002024104
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// 页脚组件不需要props和逻辑
</script>

<style scoped>
footer {
  margin-top: auto;
}

.text-light:hover {
  text-decoration: none;
  opacity: 0.8;
}
</style> 