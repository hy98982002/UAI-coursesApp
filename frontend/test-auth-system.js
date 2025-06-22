/**
 * 🧪 UAI认证系统快速检测脚本
 * 在浏览器控制台运行，验证P0级修改是否正确
 */

console.log('🚀 开始认证系统检测...')

// 检测1: Pinia持久化配置
function checkPiniaPeristence() {
  console.log('\n📦 检测1: Pinia持久化配置')
  
  const authData = localStorage.getItem('uai-auth')
  if (authData) {
    try {
      const parsed = JSON.parse(authData)
      console.log('✅ localStorage数据结构:', parsed)
      
      const expectedKeys = ['accessToken', 'refreshToken', 'userInfo']
      const actualKeys = Object.keys(parsed)
      const hasOnlyExpectedKeys = expectedKeys.every(key => 
        actualKeys.includes(key)
      ) && actualKeys.length <= expectedKeys.length + 1 // 允许额外的meta字段
      
      if (hasOnlyExpectedKeys) {
        console.log('✅ 持久化字段限制正确：只存储必要字段')
      } else {
        console.log('⚠️ 持久化字段检查：', {expected: expectedKeys, actual: actualKeys})
      }
    } catch (e) {
      console.log('❌ localStorage数据格式错误:', e.message)
    }
  } else {
    console.log('ℹ️ 暂无持久化数据（用户未登录）')
  }
}

// 检测2: 路由守卫配置
function checkRouteGuards() {
  console.log('\n🛡️ 检测2: 路由守卫配置')
  
  // 检查受保护的路由
  const protectedRoutes = ['/user', '/cart', '/order']
  const currentPath = window.location.pathname
  
  console.log('当前路径:', currentPath)
  console.log('受保护的路由:', protectedRoutes)
  
  // 检查是否在登录页且有redirect参数
  if (currentPath === '/login') {
    const urlParams = new URLSearchParams(window.location.search)
    const redirect = urlParams.get('redirect')
    if (redirect) {
      console.log('✅ 重定向保护生效，原始目标:', redirect)
    } else {
      console.log('ℹ️ 直接访问登录页')
    }
  }
}

// 检测3: API请求配置
function checkApiConfig() {
  console.log('\n🌐 检测3: API请求配置')
  
  // 检查API实例配置（通过检查请求记录）
  console.log('✅ API配置检查:')
  console.log('- 预期baseURL: http://localhost:8000')
  console.log('- 预期timeout: 15000ms')
  console.log('- 预期withCredentials: false')
  console.log('- 请在Network面板验证实际请求配置')
  
  // 检查环境变量
  console.log('环境变量配置:')
  console.log('- VITE_API_BASE_URL:', import.meta.env?.VITE_API_BASE_URL || '未设置')
}

// 检测4: Store状态
function checkStoreState() {
  console.log('\n📊 检测4: Store状态检查')
  
  // 尝试访问Pinia store（如果已初始化）
  try {
    const app = document.querySelector('#app').__vueParentComponent?.appContext?.app
    if (app && app.config.globalProperties.$pinia) {
      console.log('✅ Pinia实例已初始化')
    }
  } catch (e) {
    console.log('ℹ️ 无法检测Store状态（页面可能未完全加载）')
  }
}

// 检测5: Token刷新机制检查
function checkTokenRefreshMechanism() {
  console.log('\n🔄 检测5: Token刷新机制')
  
  const authData = localStorage.getItem('uai-auth')
  if (authData) {
    try {
      const parsed = JSON.parse(authData)
      if (parsed.accessToken && parsed.refreshToken) {
        console.log('✅ Token对存在，刷新机制可用')
        console.log('- accessToken长度:', parsed.accessToken.length)
        console.log('- refreshToken长度:', parsed.refreshToken.length)
        
        // 提示测试方法
        console.log('\n💡 手动测试Token刷新:')
        console.log('1. 修改accessToken值（添加 "invalid" 后缀）')
        console.log('2. 访问需要认证的页面（如 /user）')
        console.log('3. 观察Network面板的刷新请求')
      } else {
        console.log('⚠️ Token不完整')
      }
    } catch (e) {
      console.log('❌ Token数据解析失败')
    }
  } else {
    console.log('ℹ️ 无Token数据（用户未登录）')
  }
}

// 执行所有检测
function runAllChecks() {
  checkPiniaPeristence()
  checkRouteGuards()
  checkApiConfig()
  checkStoreState()
  checkTokenRefreshMechanism()
  
  console.log('\n🎯 检测完成！')
  console.log('请按照 MANUAL_TEST_GUIDE.md 进行完整测试')
}

// 导出检测函数到全局作用域，方便控制台调用
window.UAI_AUTH_CHECK = {
  runAll: runAllChecks,
  persistence: checkPiniaPeristence,
  routes: checkRouteGuards,
  api: checkApiConfig,
  store: checkStoreState,
  token: checkTokenRefreshMechanism
}

// 自动运行检测
runAllChecks()

console.log('\n🔧 可用的检测命令:')
console.log('- UAI_AUTH_CHECK.runAll() - 运行所有检测')
console.log('- UAI_AUTH_CHECK.persistence() - 只检测持久化')
console.log('- UAI_AUTH_CHECK.token() - 只检测Token机制') 