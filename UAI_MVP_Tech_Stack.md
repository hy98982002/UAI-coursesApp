# UAI MVP 教育平台 - 技术栈说明手册

> 本手册旨在记录 UAI 教育平台 MVP 阶段的前后端技术架构与开发规范，确保项目在 4~8 周内快速稳定上线，并为后期扩展做好准备。

## 📦 项目目标
- 快速上线（4~8 周）
- 技术规范统一、架构清晰
- 保留后续升级至企业级平台的能力

---

## 🧱 技术栈总览

### 前端（Frontend）
- 框架：Vite + Vue 3
- UI：Bootstrap 5.3（静态使用，不引入 Ant Design）
- 状态管理：Pinia
- 请求工具：Axios（封装统一请求）
- 编程风格：Composition API
- 路由：vue-router（静态配置）

### 后端（Backend）
- 语言：Python 3.12
- 框架：Django 5.2
- API：Django REST Framework
- 认证：SimpleJWT（JWT 登录鉴权）
- 后台管理：Django Admin（初期使用）

---

## 🗂 目录结构建议

```
UAIEDU_PROJECT/
├── backend/                       # Django 后端项目
│   ├── manage.py
│   ├── uai_backend/
│   ├── apps/（如 users、courses）
│   └── media/
├── frontend/                      # Vite + Vue3 前端项目
│   ├── src/
│   │   ├── views/                # 页面组件
│   │   ├── components/           # 可复用组件
│   │   ├── api/                  # axios 封装
│   │   ├── store/                # pinia
│   │   ├── router/               # vue-router
│   │   └── utils/                # 工具函数
```

---

## 🔄 前后端接口规范

- 所有接口路径前缀：`/api/`
- 请求携带 JWT：`Authorization: Bearer <token>`
- 后端统一响应格式：
```json
{
  "status": 200,
  "data": { ... },
  "msg": "成功"
}
```

---

## 🔐 权限控制（MVP阶段）

- 后端使用 Django 内建字段 `is_staff` 控制管理访问
- 暂不接入 RBAC、动态菜单等复杂机制
- 后续可平滑升级为：角色表 / 权限表 / 菜单字段 / 动态前端路由

---

## ✅ 开发规范建议

- 所有组件使用 PascalCase 命名
- 所有页面使用 Composition API（禁止 Options API）
- 所有 axios 请求统一封装在 `src/api/` 中
- 所有状态管理统一用 Pinia，放在 `src/store/` 中
- 所有后端 Model 添加 `__str__()` 方法
- 后端 Serializer 显式列出字段，不使用 `"__all__"`

---

## 🔮 后期可扩展方向（正式版）

| 功能模块 | 升级方向 |
|----------|----------|
| 管理后台 | Django Admin → Ant Design Vue Pro |
| 权限系统 | is_staff → 完整 RBAC 模型 |
| 菜单权限 | 静态菜单 → 动态菜单 + 接口控制 |
| 表单 & 页面 | 自定义 → 支持 Formily / amis 等低代码方案 |
| 审计日志 | 中间件记录操作 + 管理页面可视化 |

---

> 本手册适用于 UAI 教育平台 MVP 阶段，后期如有架构变更，请同步更新本说明文档。