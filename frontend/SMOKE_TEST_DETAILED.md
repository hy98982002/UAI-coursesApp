# 🧪 UAI认证系统 - 详细Smoke Test

## 🎯 测试目标
验证P0级一致性修正完成后，认证系统的全链路稳定性

## 🔧 测试前准备

### 1. 环境启动
```bash
# 后端 (第一个终端)
cd backend
python manage.py runserver 8000

# 前端 (第二个终端)  
cd frontend
npm run dev
```

### 2. 浏览器设置
- 打开Chrome/Edge浏览器
- 开启开发者工具 (F12)
- 确保Network、Console、Application面板可见

## 📋 详细测试步骤

### **测试1: 自动检测脚本运行**

#### 操作步骤：
1. 访问 `http://localhost:5173`
2. 打开控制台 (Console面板)
3. 复制粘贴以下代码并回车：

```javascript
// 粘贴整个test-auth-system.js文件内容
// 或者简化版本：
fetch('/test-auth-system.js').then(r=>r.text()).then(eval)
```

#### 预期结果：
```
🚀 开始认证系统检测...

📦 检测1: Pinia持久化配置
ℹ️ 暂无持久化数据（用户未登录）

🛡️ 检测2: 路由守卫配置
当前路径: /
受保护的路由: ['/user', '/cart', '/order']

🌐 检测3: API请求配置
✅ API配置检查:
- 预期baseURL: http://localhost:8000
- 预期timeout: 15000ms
...

🎯 检测完成！
```

---

### **测试2: 路由保护机制**

#### A. 未登录保护测试
1. **直接访问受保护页面**：
   - 在地址栏输入：`http://localhost:5173/user`
   - 观察页面跳转
   
2. **检查重定向参数**：
   - 确认地址栏变为：`http://localhost:5173/login?redirect=%2Fuser`
   - 控制台无错误信息

#### B. 登录页已登录重定向
1. 先完成一次登录（参考测试4）
2. 手动访问：`http://localhost:5173/login`
3. 确认自动跳转到首页

#### 预期结果：
- ✅ 未登录时强制跳转到登录页
- ✅ 登录后访问登录页自动跳转首页
- ✅ 重定向参数正确保存

---

### **测试3: 持久化机制验证**

#### 操作步骤：
1. 完成一次登录
2. **检查localStorage**：
   - F12 → Application → Storage → Local Storage
   - 找到 `uai-auth` 键
   - 查看值的JSON结构

3. **刷新页面测试**：
   - 按F5刷新页面
   - 观察是否保持登录状态
   - 检查页面不跳转到登录页

4. **字段限制验证**：
   - 确认localStorage中只包含：
     - `accessToken`
     - `refreshToken` 
     - `userInfo`
   - 没有多余的computed属性或敏感信息

#### 预期结果：
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "userInfo": {
    "id": "...",
    "phone": "13800138000",
    "nickname": "测试用户",
    ...
  }
}
```

---

### **测试4: 双登录模式**

#### A. 密码登录
1. 访问 `http://localhost:5173/login`
2. 确认在"密码登录"模式
3. 填写表单：
   - 手机号：`13800138000`
   - 密码：`test123456`
   - 勾选用户协议
4. 点击"登录"按钮
5. **观察Network面板**：
   - 查看 `POST /api/users/auth/login/` 请求
   - 确认请求头包含正确的Content-Type
   - 确认响应状态200

#### B. 验证码登录
1. 点击切换到"手机验证码登录"
2. 输入手机号：`13800138000`
3. 点击"获取验证码"
4. **观察验证码机制**：
   - 按钮变为倒计时60秒
   - Network面板出现发送验证码请求
   - 控制台或后端日志显示验证码
5. 输入验证码并登录

#### 预期结果：
- ✅ 两种登录方式都能成功
- ✅ 登录后自动跳转到重定向页面或首页
- ✅ 验证码倒计时正常工作
- ✅ 表单验证生效（必填项、手机号格式）

---

### **测试5: Token自动刷新机制**

#### 操作步骤：
1. **完成登录获取Token**
2. **手动破坏accessToken**：
   - F12 → Application → Local Storage
   - 找到 `uai-auth` 键
   - 点击编辑，在accessToken末尾添加 `invalid`
   - 保存更改

3. **触发需要认证的请求**：
   - 访问 `http://localhost:5173/user`
   - 或在控制台执行：`fetch('/api/users/user/profile/', {headers: {Authorization: 'Bearer invalid-token'}})`

4. **观察刷新过程**：
   - Network面板观察请求序列：
     1. 401响应的原请求
     2. 自动发起的 `POST /api/users/auth/refresh/`
     3. 重新发起的原请求（带新Token）

#### 预期结果：
```
Console输出：
🔄 Token失效，尝试刷新...
✅ Token刷新成功，重新发起请求

Network序列：
1. GET /api/users/user/profile/ → 401
2. POST /api/users/auth/refresh/ → 200  
3. GET /api/users/user/profile/ → 200
```

---

### **测试6: Token刷新失败处理**

#### 操作步骤：
1. **同时破坏两个Token**：
   - 修改accessToken添加 `invalid`
   - 修改refreshToken添加 `invalid`

2. **触发认证请求**：
   - 访问 `/user` 页面
   - 观察失败处理流程

#### 预期结果：
- ✅ 刷新失败后自动清理localStorage
- ✅ 跳转到登录页使用 `router.replace`（不增加历史记录）
- ✅ 控制台显示：`❌ Token刷新失败，跳转到登录页`

---

### **测试7: 并发刷新保护**

#### 操作步骤（高级）：
1. 登录并破坏accessToken
2. 在控制台快速执行多个并发请求：
```javascript
// 同时发起3个需要认证的请求
Promise.all([
  fetch('/api/users/user/profile/'),
  fetch('/api/users/user/profile/'),  
  fetch('/api/users/user/profile/')
])
```

#### 预期结果：
- ✅ Network面板只显示1次refresh请求
- ✅ 3个原请求都成功重试
- ✅ 无重复刷新或竞态条件

---

### **测试8: 完整登出流程**

#### 操作步骤：
1. 确保已登录状态
2. 访问个人中心或找到登出按钮
3. 点击"退出登录"
4. **观察清理过程**：
   - Network面板查看 `POST /api/users/auth/logout/` 请求
   - localStorage被完全清空
   - 页面跳转到登录页

#### 预期结果：
- ✅ 后端收到登出请求
- ✅ 前端状态完全清理
- ✅ 无法再访问需要认证的页面

---

### **测试9: 环境配置验证**

#### 操作步骤：
1. **检查环境变量**：
   - 确认 `.env.development` 文件存在
   - 内容包含：`VITE_API_BASE_URL=http://localhost:8000`

2. **验证API配置**：
   - Network面板查看请求
   - 确认所有API请求前缀为 `http://localhost:8000/api/`
   - 超时时间为15秒
   - 请求头包含 `Accept: application/json`

#### 预期结果：
- ✅ 所有API请求使用正确的baseURL
- ✅ 没有CORS错误
- ✅ 请求头配置标准化

---

### **测试10: 错误处理验证**

#### A. 网络错误处理
1. 关闭后端服务 (`Ctrl+C`)
2. 尝试登录
3. 观察错误提示

#### B. 表单验证
1. 尝试空表单提交
2. 输入错误格式手机号
3. 不勾选用户协议提交

#### 预期结果：
- ✅ 网络错误显示友好提示
- ✅ 表单验证及时响应
- ✅ 无JavaScript错误崩溃

---

## 📊 测试结果记录

```
测试日期：2025年_月_日
测试环境：Windows 10 + Chrome
前端版本：localhost:5173
后端版本：localhost:8000

| 测试项目 | 状态 | 备注 |
|---------|------|------|
| 自动检测脚本 | ✅/❌ |  |
| 路由保护机制 | ✅/❌ |  |
| 持久化机制 | ✅/❌ |  |
| 密码登录 | ✅/❌ |  |
| 验证码登录 | ✅/❌ |  |
| Token自动刷新 | ✅/❌ |  |
| 刷新失败处理 | ✅/❌ |  |
| 并发刷新保护 | ✅/❌ |  |
| 完整登出流程 | ✅/❌ |  |
| 环境配置 | ✅/❌ |  |
| 错误处理 | ✅/❌ |  |

发现的问题：
1. _______________
2. _______________

整体评价：
□ 完全通过 - 可以开始courses模块
□ 有小问题 - 需要修复后继续
□ 有重大问题 - 需要重新设计
```

---

## ⚡ 快速检查清单

如果时间有限，至少验证以下核心功能：

1. **✅ 登录能成功，刷新页面保持状态**
2. **✅ 访问 `/user` 未登录时跳转到登录页**
3. **✅ Token过期后能自动刷新**
4. **✅ 登出后localStorage清空**
5. **✅ Network面板显示正确的API配置**

---

## 🚀 测试通过后的下一步

```bash
# 1. 提交当前认证系统
git add .
git commit -m "✅ 认证系统P0修正完成，通过Smoke Test"

# 2. 开始courses模块
cd ../backend
python manage.py startapp courses

# 3. 参考设计文档
# 查看：uai-backend-app-design.md
```

恭喜！认证系统已达到生产级稳定性，可以安心进入业务开发阶段！ 