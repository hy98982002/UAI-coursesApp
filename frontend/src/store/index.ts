import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
/* 调用 createPinia() 创建了一个 全局状态容器。

它内部维护所有模块的 store（如 useUserStore()、useCartStore()）。

这一步等价于你创建了 Vue 应用的“数据大脑”。 */
/* 🔧 1. 它是 Pinia 的“根状态容器”
createPinia() 是 Pinia 提供的一个函数，用来 创建一个新的 Pinia 实例。这个实例可以理解为“全局状态管理的容器”，类似于 Vuex 的 createStore()。

类比解释：
就像你开一家便利店，要先创建一个仓库（pinia），后面你才能往这个仓库里存放不同种类的商品（state），这行代码就是在建仓库。 */


const pinia = createPinia()

// 使用持久化插件，自动将state持久化到localStorage
pinia.use(piniaPluginPersistedstate)

export default pinia
