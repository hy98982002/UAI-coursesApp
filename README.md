**#全程和我用中文交流**

# =============================

# UAI 高规范项目 Cursor Rules
# 项目结构：前后端分离（Vite + Vue3 + Django REST）
# 项目目标：低代码平台、动态菜单、权限系统、REST API、RBAC、安全审计等
# =============================

# -----------------------------
# 🧩 前端开发规则（Vite + Vue3 + TypeScript + Pinia）
# -----------------------------

- 所有页面放在 src/views 下，以模块为单位组织。
- 所有复用组件放在 src/components 下，命名统一为 PascalCase。
- 所有 axios 请求必须封装在 src/api 中，每个模块一个文件，自动附带 JWT token。
- 所有页面状态管理用 Pinia（src/store），不得用 Vuex。
- 所有 Vue 文件使用 Composition API。
- 所有菜单使用递归组件实现，权限由后端接口返回。
- 所有路由注册放在 src/router/index.ts，支持动态路由。
- 所有样式使用 Bootstrap 5.3（不要引入其他 UI 框架）。
- 所有常用函数放入 src/utils，并附带注释。

# -----------------------------
# 🛠 后端开发规则（Django 5.2 + DRF）
# -----------------------------

- 每个功能模块建立独立 app（如 users / courses / system）。
- 所有 API 使用 Django REST Framework，遵守 RESTful 风格。
- 所有用户认证使用 JWT（simplejwt），登录路径 /api/token/。
- 用户权限使用 RBAC 模型（角色 -> 权限 -> 用户），用中间表实现。
- 权限控制使用装饰器或权限类；所有视图必须考虑权限判断。
- 所有操作日志（增删改）使用 Django 中间件统一记录。
- 所有 Model 类要添加 __str__ 方法，便于管理后台展示。
- 所有 serializer 类使用 Meta.fields 精确定义，不使用 "__all__"。
- 每个 app 的路由写在自己的 urls.py，主路由在 uai_backend/urls.py 中 include。
- 所有跨域设置在 corsheaders 中配置，默认允许 localhost:5173 访问。

# -----------------------------
# 🧪 测试/部署建议
# -----------------------------

- 前端开发时默认本地运行于 http://localhost:5173
- 后端开发默认本地运行于 http://localhost:8000
- 前后端接口通过 /api/ 前缀通信
- 接口数据结构必须包含 status / data / msg 字段，便于前端统一处理
- 所有新功能开发前，先更新 rules 说明，再由 AI 帮助生成/修改代码